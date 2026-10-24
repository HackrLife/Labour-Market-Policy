"""Load and validate the source registry (registry/sources/*.yaml).

Each YAML file describes one publisher. Each dataset entry names a connector
and its parameters, the domain(s) it serves, its licence, and whether its
identifiers have been confirmed by a successful pull (`verified`).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from . import REGISTRY_DIR

DOMAINS = {
    "employment",      # employment, unemployment, participation, hours
    "vacancies",       # job openings, vacancy rates, hires
    "wages",           # earnings, wage indices, labour costs
    "migration",       # migrant stocks, flows, remittances, foreign-born labour
    "adjustment",      # flows, displacement, mobility, sectoral reallocation
    "macro",           # labour share, productivity, output, prices
    "micro",           # occupations, tasks, skills, AI exposure
    "demography",      # population, fertility, dependency ratios
    "housing",         # housing costs as labour-market constraint
}

REDISTRIBUTION = {"open", "attribution", "restricted"}


@dataclass
class Dataset:
    source: str
    id: str
    title: str
    connector: str
    params: dict[str, Any]
    domains: list[str]
    frequency: str = "unknown"
    verified: bool = False
    notes: str = ""

    @property
    def key(self) -> str:
        return f"{self.source}/{self.id}"


@dataclass
class Source:
    id: str
    publisher: str
    homepage: str
    licence: str
    redistribution: str
    release_calendar: str = ""
    datasets: list[Dataset] = field(default_factory=list)


class RegistryError(ValueError):
    pass


def _load_file(path: Path) -> Source:
    raw = yaml.safe_load(path.read_text())
    try:
        src = Source(
            id=raw["id"],
            publisher=raw["publisher"],
            homepage=raw["homepage"],
            licence=raw["licence"],
            redistribution=raw["redistribution"],
            release_calendar=raw.get("release_calendar", ""),
        )
    except KeyError as e:
        raise RegistryError(f"{path.name}: missing source field {e}") from e
    if src.redistribution not in REDISTRIBUTION:
        raise RegistryError(f"{path.name}: redistribution must be one of {REDISTRIBUTION}")
    seen = set()
    for d in raw.get("datasets", []):
        try:
            ds = Dataset(
                source=src.id,
                id=d["id"],
                title=d["title"],
                connector=d["connector"],
                params=d.get("params", {}),
                domains=d["domains"],
                frequency=d.get("frequency", "unknown"),
                verified=bool(d.get("verified", False)),
                notes=d.get("notes", ""),
            )
        except KeyError as e:
            raise RegistryError(f"{path.name}: dataset missing field {e}: {d}") from e
        bad = set(ds.domains) - DOMAINS
        if bad:
            raise RegistryError(f"{ds.key}: unknown domains {bad}")
        if ds.id in seen:
            raise RegistryError(f"{ds.key}: duplicate dataset id")
        seen.add(ds.id)
        src.datasets.append(ds)
    return src


def load_registry(directory: Path | None = None) -> dict[str, Source]:
    directory = directory or (REGISTRY_DIR / "sources")
    sources: dict[str, Source] = {}
    for path in sorted(directory.glob("*.yaml")):
        src = _load_file(path)
        if src.id in sources:
            raise RegistryError(f"duplicate source id {src.id}")
        sources[src.id] = src
    return sources


def iter_datasets(sources: dict[str, Source], source: str | None = None,
                  dataset: str | None = None, domain: str | None = None):
    for s in sources.values():
        if source and s.id != source:
            continue
        for d in s.datasets:
            if dataset and d.id != dataset:
                continue
            if domain and domain not in d.domains:
                continue
            yield s, d
