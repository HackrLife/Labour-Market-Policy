"""Validation and revision tracking for a newly normalised table.

Checks run on every new vintage. Hard failures stop the processed table being
replaced; warnings are recorded in the run report for the curator to review.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

REQUIRED = ["ref_area", "indicator", "period", "value"]
KEY_EXCLUDE = {"value", "obs_status", "note_classif", "note_indicator", "note_source",
               "preliminary", "area_name", "indicator_label", "obs_flag", "conf_status"}


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    stats: dict = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.errors


def key_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if c not in KEY_EXCLUDE]


def validate(new: pd.DataFrame, old: pd.DataFrame | None) -> Report:
    rep = Report()
    missing = [c for c in REQUIRED if c not in new.columns]
    if missing:
        rep.errors.append(f"missing required columns {missing}")
        return rep
    if new.empty:
        rep.errors.append("table is empty")
        return rep

    vals = pd.to_numeric(new["value"], errors="coerce")
    numeric_share = float(vals.notna().mean())
    rep.stats.update(rows=len(new), numeric_share=round(numeric_share, 4),
                     areas=int(new["ref_area"].nunique()),
                     indicators=int(new["indicator"].nunique()),
                     period_min=str(new["period"].min()), period_max=str(new["period"].max()))
    if numeric_share < 0.5:
        rep.warnings.append(f"only {numeric_share:.0%} of values are numeric")

    keys = key_columns(new)
    dups = int(new.duplicated(keys).sum())
    if dups:
        rep.warnings.append(f"{dups} duplicate rows on key {keys}")

    if old is None or old.empty:
        rep.stats["first_vintage"] = True
        return rep

    if len(new) < 0.8 * len(old):
        rep.errors.append(f"row count fell {len(old)} -> {len(new)} (>20%); possible truncated pull")

    common = [k for k in keys if k in old.columns]
    if not common:
        rep.warnings.append("schema changed; no common key columns with previous vintage")
        return rep
    a = old[common + ["value"]].copy()
    b = new[common + ["value"]].copy()
    for d in (a, b):
        d[common] = d[common].astype(str)
        d["value"] = pd.to_numeric(d["value"], errors="coerce")
    m = a.merge(b, on=common, how="outer", suffixes=("_old", "_new"), indicator=True)
    both = m[m["_merge"] == "both"]
    changed = both[~((both["value_old"] - both["value_new"]).abs().fillna(0) < 1e-9)
                   & ~(both["value_old"].isna() & both["value_new"].isna())]
    rep.stats.update(
        added=int((m["_merge"] == "right_only").sum()),
        removed=int((m["_merge"] == "left_only").sum()),
        revised=int(len(changed)),
        new_period_max=str(new["period"].max()),
        old_period_max=str(old["period"].max()),
    )
    if len(both) and len(changed) / len(both) > 0.25:
        rep.warnings.append(f"{len(changed)} of {len(both)} observations revised (>25%): benchmark revision?")
    return rep
