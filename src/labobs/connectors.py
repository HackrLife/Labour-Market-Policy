"""Connectors: fetch a dataset's payload and normalise it to the tidy schema.

Tidy schema (processed layer). Required columns:
  ref_area   ISO3 / publisher area code (e.g. AUS, USA, EA20, WLD)
  indicator  publisher indicator or series code
  period     YYYY, YYYY-Qn, YYYY-MM or YYYY-MM-DD
  value      float
Optional columns are kept as published dimensions (sex, age, classif1, unit,
obs_status, ...). Column names are lower-cased.

Every connector returns a Fetched object; normalise() turns a payload into a
DataFrame. Connectors never edit values. Unit conversion, seasonal adjustment
or harmonisation belong in notebooks so they stay visible.
"""

from __future__ import annotations

import gzip
import io
import json
import os
import time
import zipfile
from dataclasses import dataclass
from typing import Callable

import pandas as pd
import requests

USER_AGENT = (
    "labour-observatory/0.1 (non-commercial research; "
    f"contact: {os.environ.get('LABOBS_CONTACT', 'see github.com/HackrLife/labour-observatory')})"
)
TIMEOUT = 120


@dataclass
class Fetched:
    payload: bytes
    ext: str
    url: str


def _get(url: str, headers: dict | None = None, params: dict | None = None,
         retries: int = 3) -> requests.Response:
    h = {"User-Agent": USER_AGENT}
    h.update(headers or {})
    last = None
    for i in range(retries):
        try:
            r = requests.get(url, headers=h, params=params, timeout=TIMEOUT)
            if r.status_code == 200:
                return r
            last = f"HTTP {r.status_code}: {r.text[:300]}"
            if r.status_code in (400, 401, 403, 404):
                break
        except requests.RequestException as e:
            last = str(e)
        time.sleep(2 ** i * 3)
    raise ConnectorError(f"GET {url} failed: {last}")


class ConnectorError(RuntimeError):
    pass


# ---------------------------------------------------------------- World Bank
def fetch_worldbank(p: dict) -> Fetched:
    ind = p["indicator"]
    base = f"https://api.worldbank.org/v2/country/all/indicator/{ind}"
    rows, page, pages = [], 1, 1
    while page <= pages:
        r = _get(base, params={"format": "json", "per_page": 20000, "page": page})
        meta, data = r.json()
        pages = meta["pages"]
        rows.extend(data or [])
        page += 1
    return Fetched(json.dumps(rows).encode(), "json", base)


def norm_worldbank(b: bytes, p: dict) -> pd.DataFrame:
    rows = json.loads(b)
    df = pd.DataFrame(
        {
            "ref_area": [r.get("countryiso3code") or r["country"]["id"] for r in rows],
            "area_name": [r["country"]["value"] for r in rows],
            "indicator": [r["indicator"]["id"] for r in rows],
            "period": [r["date"] for r in rows],
            "value": [r["value"] for r in rows],
        }
    )
    return df


# ---------------------------------------------------------------- ILOSTAT bulk
ILO_BULK = "https://rplumber.ilo.org/data/indicator/"


def fetch_ilostat(p: dict) -> Fetched:
    # rplumber is the ILOSTAT data API used by the official Rilostat package.
    url = p.get("url") or ILO_BULK
    params = {"id": p["indicator"], "format": ".csv.gz", "type": "code"}
    r = _get(url, params=params)
    return Fetched(r.content, "csv.gz", r.url)


def norm_ilostat(b: bytes, p: dict) -> pd.DataFrame:
    raw = gzip.decompress(b) if b[:2] == b"\x1f\x8b" else b
    df = pd.read_csv(io.BytesIO(raw), low_memory=False)
    df.columns = [c.lower() for c in df.columns]
    return df.rename(columns={"time": "period", "obs_value": "value"})


# ---------------------------------------------------------------- SDMX (CSV)
SDMX_CSV_ACCEPT = "application/vnd.sdmx.data+csv; charset=utf-8"


def fetch_sdmx(p: dict) -> Fetched:
    headers = {"Accept": p.get("accept", SDMX_CSV_ACCEPT)}
    r = _get(p["url"], headers=headers, params=p.get("query"))
    return Fetched(r.content, "csv", r.url)


AREA_COLS = ["ref_area", "geo", "region", "country", "location"]


def norm_sdmx(b: bytes, p: dict) -> pd.DataFrame:
    df = pd.read_csv(io.BytesIO(b), low_memory=False)
    df.columns = [c.lower().split(":")[0].strip() for c in df.columns]
    area = next((c for c in AREA_COLS if c in df.columns), None)
    ren = {"time_period": "period", "obs_value": "value"}
    if area and area != "ref_area":
        ren[area] = "ref_area"
    df = df.rename(columns=ren)
    if "indicator" not in df.columns:
        df["indicator"] = p.get("indicator_label") or p.get("dataflow", "")
    if "ref_area" not in df.columns:
        df["ref_area"] = p.get("ref_area", "")
    return df


# ---------------------------------------------------------------- BLS API v2
BLS_API = "https://api.bls.gov/publicAPI/v2/timeseries/data/"


def fetch_bls(p: dict) -> Fetched:
    key = os.environ.get("BLS_API_KEY")
    span = 20 if key else 10
    batch = 50 if key else 25
    start, end = int(p.get("start_year", 2000)), int(p.get("end_year", time.gmtime().tm_year))
    series = p["series"]
    out = []
    for i in range(0, len(series), batch):
        for y0 in range(start, end + 1, span):
            body = {"seriesid": series[i:i + batch], "startyear": str(y0),
                    "endyear": str(min(y0 + span - 1, end))}
            if key:
                body["registrationkey"] = key
            r = requests.post(BLS_API, json=body, timeout=TIMEOUT,
                              headers={"User-Agent": USER_AGENT})
            j = r.json()
            if j.get("status") != "REQUEST_SUCCEEDED":
                raise ConnectorError(f"BLS: {j.get('status')} {j.get('message')}")
            out.extend(j["Results"]["series"])
    return Fetched(json.dumps(out).encode(), "json", BLS_API)


def _bls_period(year: str, period: str) -> str | None:
    if period.startswith("M") and period != "M13":
        return f"{year}-{period[1:]}"
    if period.startswith("Q") and period != "Q05":
        return f"{year}-Q{int(period[1:])}"
    if period in ("A01", "M13", "Q05"):
        return year
    return None


def norm_bls(b: bytes, p: dict) -> pd.DataFrame:
    recs = []
    labels = p.get("labels", {})
    for s in json.loads(b):
        sid = s["seriesID"]
        for d in s["data"]:
            per = _bls_period(d["year"], d["period"])
            if per is None:
                continue
            try:
                v = float(d["value"])
            except ValueError:
                v = None
            recs.append({"ref_area": "USA", "indicator": sid,
                         "indicator_label": labels.get(sid, ""), "period": per,
                         "value": v, "preliminary": any(f.get("code") == "P"
                                                        for f in d.get("footnotes", []) if f)})
    df = pd.DataFrame(recs)
    return df.drop_duplicates(["indicator", "period"]).sort_values(["indicator", "period"])


# ---------------------------------------------------------------- FRED (keyless graph CSV)
def fetch_fred(p: dict) -> Fetched:
    frames = {}
    for sid in p["series"]:
        r = _get("https://fred.stlouisfed.org/graph/fredgraph.csv", params={"id": sid})
        frames[sid] = r.text
    return Fetched(json.dumps(frames).encode(), "json", "https://fred.stlouisfed.org/graph/fredgraph.csv")


def norm_fred(b: bytes, p: dict) -> pd.DataFrame:
    out = []
    for sid, text in json.loads(b).items():
        df = pd.read_csv(io.StringIO(text))
        df.columns = ["period", "value"]
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df["indicator"] = sid
        df["ref_area"] = p.get("ref_area", "USA")
        out.append(df)
    return pd.concat(out, ignore_index=True)


# ---------------------------------------------------------------- generic file
class MissingKey(RuntimeError):
    pass


def _secret_params(p: dict) -> tuple[dict, dict, list[str]]:
    """Resolve API keys from environment variables named in key_env / header_env."""
    query, headers, secrets = dict(p.get("query") or {}), dict(p.get("headers") or {}), []
    for param, env in (p.get("key_env") or {}).items():
        val = os.environ.get(env)
        if not val:
            raise MissingKey(f"environment variable {env} not set")
        query[param] = val
        secrets.append(val)
    for header, env in (p.get("header_env") or {}).items():
        val = os.environ.get(env)
        if not val:
            raise MissingKey(f"environment variable {env} not set")
        headers[header] = val
        secrets.append(val)
    return query, headers, secrets


def _mask(url: str, secrets: list[str]) -> str:
    for s in secrets:
        url = url.replace(s, "***")
    return url


def fetch_http(p: dict) -> Fetched:
    query, headers, secrets = _secret_params(p)
    r = _get(p["url"], headers=headers, params=query or None)
    return Fetched(r.content, p.get("ext", p["url"].split("?")[0].rsplit(".", 1)[-1].lower()),
                   _mask(r.url, secrets))


ONS_MONTHS = {m: f"{i:02d}" for i, m in enumerate(
    ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"], 1)}


def parse_ons_ts(b: bytes, p: dict) -> pd.DataFrame:
    """ONS time-series generator CSV: metadata rows, then mixed annual/quarterly/monthly rows."""
    text = b.decode("utf-8-sig")
    meta, rows = {}, []
    for line in text.splitlines():
        parts = [x.strip().strip('"') for x in line.split('","')] if line.startswith('"') else line.split(",")
        if len(parts) < 2:
            continue
        k, v = parts[0].strip('"'), parts[1].strip('"')
        tok = k.split()
        if tok and tok[0].isdigit() and len(tok[0]) == 4:
            if len(tok) == 1:
                per, freq = tok[0], "A"
            elif tok[1].startswith("Q"):
                per, freq = f"{tok[0]}-{tok[1]}", "Q"
            elif tok[1][:3].upper() in ONS_MONTHS:
                per, freq = f"{tok[0]}-{ONS_MONTHS[tok[1][:3].upper()]}", "M"
            else:
                continue
            rows.append({"period": per, "freq": freq, "value": pd.to_numeric(v, errors="coerce")})
        else:
            meta[k] = v
    df = pd.DataFrame(rows)
    keep = p.get("freq")
    if keep:
        df = df[df["freq"] == keep]
    df["indicator"] = meta.get("CDID", p.get("indicator", ""))
    df["indicator_label"] = meta.get("Title", "")
    df["unit"] = meta.get("Unit", "")
    return df


def parse_sidra(b: bytes, p: dict) -> pd.DataFrame:
    """IBGE SIDRA /values JSON: first record is a header mapping codes to labels."""
    recs = json.loads(b)
    header, data = recs[0], recs[1:]
    df = pd.DataFrame(data).rename(columns={k: v for k, v in header.items()})
    df.columns = [str(c).strip() for c in df.columns]
    return df


def parse_json_records(b: bytes, p: dict) -> pd.DataFrame:
    obj = json.loads(b)
    for k in p.get("records_path", []):
        obj = obj[k]
    return pd.DataFrame(obj)


def norm_http(b: bytes, p: dict) -> pd.DataFrame | None:
    kind = p.get("parse", "none")
    if kind == "none":
        return None
    if kind == "csv":
        df = pd.read_csv(io.BytesIO(b), low_memory=False, skiprows=p.get("skiprows", 0))
    elif kind == "zip_csv":
        with zipfile.ZipFile(io.BytesIO(b)) as z:
            df = pd.read_csv(z.open(p["member"]), sep=p.get("sep", ","), low_memory=False)
    elif kind == "xlsx":
        df = pd.read_excel(io.BytesIO(b), sheet_name=p.get("sheet", 0), header=p.get("header", 0))
    elif kind == "ons_ts":
        df = parse_ons_ts(b, p)
    elif kind == "sidra":
        df = parse_sidra(b, p)
    elif kind == "json_records":
        df = parse_json_records(b, p)
    else:
        raise ConnectorError(f"unknown parse kind {kind}")
    # map publisher columns onto the tidy schema: params.rename {publisher_col: tidy_col}
    df = df.rename(columns=p.get("rename", {}))
    df.columns = [str(c).lower() for c in df.columns]
    for col, default in (("ref_area", p.get("ref_area", "")), ("indicator", p.get("indicator", ""))):
        if col not in df.columns:
            df[col] = default
    if "value" in df.columns:
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df


CONNECTORS: dict[str, tuple[Callable[[dict], Fetched], Callable[[bytes, dict], pd.DataFrame | None]]] = {
    "worldbank": (fetch_worldbank, norm_worldbank),
    "ilostat": (fetch_ilostat, norm_ilostat),
    "sdmx": (fetch_sdmx, norm_sdmx),
    "bls": (fetch_bls, norm_bls),
    "fred": (fetch_fred, norm_fred),
    "http": (fetch_http, norm_http),
}
