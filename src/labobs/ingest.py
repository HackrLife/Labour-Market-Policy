"""Ingest runner: fetch -> store raw vintage -> normalise -> validate -> publish.

Produces, per run:
  logs/runs/<date>.json      machine-readable report for every dataset touched
  DATA_CHANGELOG.md          human-readable entry for each new vintage
  registry/status.json       last attempt / last success per dataset
"""

from __future__ import annotations

import datetime as dt
import json
import traceback

import pandas as pd

from . import LOG_DIR, REGISTRY_DIR, REPO_ROOT
from .connectors import CONNECTORS, MissingKey
from .registry import iter_datasets, load_registry
from .storage import processed_path, store_raw
from .validate import validate

STATUS = REGISTRY_DIR / "status.json"
CHANGELOG = REPO_ROOT / "DATA_CHANGELOG.md"


def _load_json(path, default):
    return json.loads(path.read_text()) if path.exists() else default


def ingest_one(src, ds, today: dt.date) -> dict:
    res = {"dataset": ds.key, "title": ds.title, "started": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
    fetch, norm = CONNECTORS[ds.connector]
    if "TBD" in json.dumps(ds.params):
        res["status"] = "skipped_unconfigured"
        return res
    try:
        fetched = fetch(ds.params)
    except MissingKey as e:
        res.update(status="skipped_no_key", error=str(e))
        return res
    dom = ds.domains[0]
    is_new, meta = store_raw(dom, src.id, ds.id, fetched.payload, fetched.ext, fetched.url,
                             src.redistribution, today)
    res.update(new_vintage=is_new, sha256=meta["sha256"][:12], bytes=meta["bytes"])
    if not is_new:
        res["status"] = "unchanged"
        return res

    df = norm(fetched.payload, ds.params)
    if df is None:
        res["status"] = "stored_raw_only"
        return res
    df.insert(0, "dataset", ds.id)
    df.insert(0, "source", src.id)
    out = processed_path(dom, src.id, ds.id)
    old = pd.read_csv(out, low_memory=False) if out.exists() else None
    rep = validate(df, old)
    res.update(validation={"errors": rep.errors, "warnings": rep.warnings, "stats": rep.stats})
    if not rep.ok:
        res["status"] = "rejected"
        return res
    if src.redistribution == "restricted":
        res["status"] = "validated_not_published"
        return res
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    res["status"] = "published"
    return res


def run(source=None, dataset=None, domain=None, today: dt.date | None = None) -> list[dict]:
    today = today or dt.date.today()
    reg = load_registry()
    status = _load_json(STATUS, {})
    results = []
    for src, ds in iter_datasets(reg, source, dataset, domain):
        try:
            r = ingest_one(src, ds, today)
        except Exception as e:  # one failure must not stop the run
            r = {"dataset": ds.key, "status": "failed", "error": f"{type(e).__name__}: {e}",
                 "trace": traceback.format_exc(limit=3)}
        results.append(r)
        st = status.setdefault(ds.key, {})
        st["last_attempt"] = today.isoformat()
        st["last_status"] = r["status"]
        if r["status"] in ("published", "unchanged", "stored_raw_only", "validated_not_published"):
            st["last_success"] = today.isoformat()
            st["confirmed"] = True
        if r.get("new_vintage") and r["status"] == "published":
            st["last_new_vintage"] = today.isoformat()
        print(f"[{r['status']:>22}] {ds.key}" + (f"  {r.get('error', '')}" if r["status"] == "failed" else ""))

    STATUS.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n")
    LOG_DIR.joinpath("runs").mkdir(parents=True, exist_ok=True)
    LOG_DIR.joinpath("runs", f"{today.isoformat()}.json").write_text(json.dumps(results, indent=2) + "\n")
    _append_changelog(results, today)
    return results


def _append_changelog(results, today):
    new = [r for r in results if r["status"] == "published"]
    failed = [r for r in results if r["status"] in ("failed", "rejected")]
    if not new and not failed:
        return
    lines = [f"\n## {today.isoformat()}\n"]
    for r in new:
        s = r.get("validation", {}).get("stats", {})
        detail = (f"first vintage, {s.get('rows')} rows, {s.get('period_min')}–{s.get('period_max')}"
                  if s.get("first_vintage") else
                  f"{s.get('added', 0)} added, {s.get('revised', 0)} revised, latest period {s.get('new_period_max')}")
        lines.append(f"- **{r['dataset']}** — {detail}")
        for w in r.get("validation", {}).get("warnings", []):
            lines.append(f"  - ⚠ {w}")
    for r in failed:
        why = r.get("error") or "; ".join(r.get("validation", {}).get("errors", []))
        lines.append(f"- ✗ **{r['dataset']}** {r['status']}: {why}")
    if not CHANGELOG.exists():
        CHANGELOG.write_text("# Data changelog\n\nEvery new vintage, revision summary and failed pull, newest last.\n")
    with CHANGELOG.open("a") as f:
        f.write("\n".join(lines) + "\n")
