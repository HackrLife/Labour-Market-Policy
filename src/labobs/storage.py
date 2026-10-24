"""Vintage-aware storage, organised by data type (domain).

Layout:
  data/<domain>/<source>/<dataset>/vintages/<YYYY-MM-DD>/payload.<ext>  untouched download
  data/<domain>/<source>/<dataset>/vintages/<YYYY-MM-DD>/meta.json     url, sha256, size, fetched_at
  data/<domain>/<source>/<dataset>/latest.csv                         tidy table, latest vintage
  data/<domain>/curated/<series>.csv                                  hand-curated historical series
  data/manifest.json                                                  one entry per dataset

<domain> is the dataset's primary domain (first entry in its `domains` list).
A new raw vintage is written only when the payload hash changes, so each
folder under vintages/ is a distinct release. Payloads above MAX_RAW_BYTES,
or from sources whose terms restrict redistribution, are not committed; their
hash and URL are kept so the vintage stays auditable and re-fetchable.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path

from . import DATA_DIR

MAX_RAW_BYTES = 40 * 1024 * 1024
MANIFEST = DATA_DIR / "manifest.json"


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}


def save_manifest(m: dict) -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(m, indent=2, sort_keys=True) + "\n")


def dataset_dir(domain: str, source: str, dataset: str) -> Path:
    return DATA_DIR / domain / source / dataset


def store_raw(domain: str, source: str, dataset: str, payload: bytes, ext: str, url: str,
              redistribution: str, today: dt.date | None = None) -> tuple[bool, dict]:
    """Store payload as a new vintage if it differs from the last one. Returns (is_new, meta)."""
    today = today or dt.date.today()
    digest = sha256(payload)
    m = load_manifest()
    key = f"{source}/{dataset}"
    prev = m.get(key, {})
    if prev.get("sha256") == digest:
        return False, prev

    vdir = dataset_dir(domain, source, dataset) / "vintages" / today.isoformat()
    vdir.mkdir(parents=True, exist_ok=True)
    committed = len(payload) <= MAX_RAW_BYTES and redistribution != "restricted"
    if committed:
        (vdir / f"payload.{ext}").write_bytes(payload)
    meta = {
        "domain": domain,
        "source": source,
        "dataset": dataset,
        "vintage": today.isoformat(),
        "url": url,
        "sha256": digest,
        "bytes": len(payload),
        "ext": ext,
        "payload_committed": committed,
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "previous_vintage": prev.get("vintage"),
    }
    (vdir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    m[key] = meta
    save_manifest(m)
    return True, meta


def processed_path(domain: str, source: str, dataset: str) -> Path:
    return dataset_dir(domain, source, dataset) / "latest.csv"
