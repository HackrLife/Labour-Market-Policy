"""Read helpers for notebooks.

    from labobs.load import load, vintage, curated
    df = load("worldbank/unemployment_youth")
    print(vintage("worldbank/unemployment_youth"))   # release date and hash of the data in use
"""

from __future__ import annotations

import pandas as pd

from . import DATA_DIR
from .registry import load_registry
from .storage import load_manifest, processed_path


def _locate(key: str):
    source, dataset = key.split("/", 1)
    reg = load_registry()
    if source not in reg:
        raise KeyError(f"source {source!r} not in registry/sources/")
    ds = next((d for d in reg[source].datasets if d.id == dataset), None)
    if ds is None:
        raise KeyError(f"dataset {key!r} not in registry")
    return ds.domains[0], source, dataset


def load(key: str, **filters) -> pd.DataFrame:
    """Load the latest tidy table for 'source/dataset'. Keyword filters match column values."""
    path = processed_path(*_locate(key))
    if not path.exists():
        raise FileNotFoundError(f"{key}: no processed data yet ({path}). Run `labobs ingest --source "
                                f"{key.split('/')[0]} --dataset {key.split('/')[1]}` or wait for the daily run.")
    df = pd.read_csv(path, low_memory=False)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    for col, val in filters.items():
        vals = val if isinstance(val, (list, tuple, set)) else [val]
        df = df[df[col].isin(vals)]
    return df


def vintage(key: str) -> dict:
    return load_manifest().get(key, {})


def raw_payload(key: str):
    """Path to the latest committed raw payload (for zip/xlsx sources parsed in notebooks)."""
    m = vintage(key)
    if not m:
        raise FileNotFoundError(f"{key}: no vintage yet")
    domain, source, dataset = _locate(key)
    p = DATA_DIR / domain / source / dataset / "vintages" / m["vintage"] / f"payload.{m['ext']}"
    if not p.exists():
        raise FileNotFoundError(f"{key}: payload not committed (size or licence); re-fetch from {m['url']}")
    return p


def curated(domain: str, name: str) -> pd.DataFrame:
    """Load a hand-curated historical series from data/<domain>/curated/<name>.csv."""
    return pd.read_csv(DATA_DIR / domain / "curated" / f"{name}.csv")
