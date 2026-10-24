"""Shared helpers for analysis notebooks: selection, reshaping, charts, change tables.

Kept deliberately small so each notebook's analytical choices stay visible in
the notebook itself.
"""

from __future__ import annotations

import pandas as pd

FOCUS = ["WLD", "AUS", "USA", "GBR", "DEU", "FRA", "ITA", "ESP", "JPN", "KOR",
         "CHN", "IND", "IDN", "BRA", "ZAF", "CAN"]
FOCUS_NAMES = {"WLD": "World", "AUS": "Australia", "USA": "United States", "GBR": "United Kingdom",
               "DEU": "Germany", "FRA": "France", "ITA": "Italy", "ESP": "Spain", "JPN": "Japan",
               "KOR": "Korea", "CHN": "China", "IND": "India", "IDN": "Indonesia", "BRA": "Brazil",
               "ZAF": "South Africa", "CAN": "Canada"}


def select(df: pd.DataFrame, **filters) -> pd.DataFrame:
    for col, val in filters.items():
        if col not in df.columns:
            raise KeyError(f"column {col!r} not in table; available: {list(df.columns)}")
        vals = val if isinstance(val, (list, tuple, set)) else [val]
        df = df[df[col].isin(vals)]
    return df


def pivot(df: pd.DataFrame, columns: str = "ref_area", index: str = "period",
          values: str = "value") -> pd.DataFrame:
    p = df.pivot_table(index=index, columns=columns, values=values, aggfunc="mean")
    return p.sort_index()


def latest(df: pd.DataFrame, by: str | list[str] = "ref_area") -> pd.DataFrame:
    """Most recent non-missing observation per group, with the prior observation and change."""
    by = [by] if isinstance(by, str) else by
    d = df.dropna(subset=["value"]).sort_values("period")
    last = d.groupby(by).tail(1).set_index(by)
    prev = d.groupby(by).nth(-2).set_index(by) if len(d) else last.iloc[0:0]
    out = last[["period", "value"]].rename(columns={"period": "latest_period", "value": "latest"})
    out["previous_period"] = prev["period"]
    out["previous"] = prev["value"]
    out["change"] = out["latest"] - out["previous"]
    return out.sort_values("latest", ascending=False)


def plot_lines(p: pd.DataFrame, title: str, ylabel: str, source: str, names: dict | None = None,
               ax=None):
    import matplotlib.pyplot as plt
    ax = ax or plt.subplots(figsize=(10, 5))[1]
    names = names or FOCUS_NAMES
    for c in p.columns:
        s = p[c].dropna()
        if s.empty:
            continue
        ax.plot(s.index.astype(str), s.values, label=names.get(c, c), linewidth=1.6)
    ax.set_title(title, loc="left", fontsize=12, fontweight="bold")
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)
    ticks = list(p.index.astype(str))
    step = max(1, len(ticks) // 10)
    ax.set_xticks(ticks[::step])
    ax.tick_params(axis="x", rotation=45)
    ax.legend(frameon=False, fontsize=8, ncol=2)
    ax.figure.text(0.01, -0.02, f"Source: {source}", fontsize=8, color="#555")
    ax.figure.tight_layout()
    return ax


def plot_bars(s: pd.Series, title: str, xlabel: str, source: str, names: dict | None = None):
    import matplotlib.pyplot as plt
    names = names or FOCUS_NAMES
    s = s.dropna().sort_values()
    fig, ax = plt.subplots(figsize=(9, max(3, 0.32 * len(s))))
    ax.barh([names.get(i, i) for i in s.index], s.values, color="#1a73e8")
    ax.set_title(title, loc="left", fontsize=12, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.grid(axis="x", alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(0.01, -0.02, f"Source: {source}", fontsize=8, color="#555")
    fig.tight_layout()
    return ax


def to_annual(df: pd.DataFrame) -> pd.DataFrame:
    """Average sub-annual periods (YYYY-MM, YYYY-Qn) to calendar years."""
    d = df.copy()
    d["period"] = d["period"].astype(str).str[:4]
    keys = [c for c in d.columns if c not in ("value",)]
    return d.groupby(keys, dropna=False, as_index=False)["value"].mean()
