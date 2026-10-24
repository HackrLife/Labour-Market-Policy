"""Command line: labobs list | ingest | status."""

from __future__ import annotations

import argparse
import json
import sys

from .ingest import STATUS, run
from .registry import iter_datasets, load_registry


def main(argv=None):
    ap = argparse.ArgumentParser(prog="labobs")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("list", "ingest"):
        p = sub.add_parser(name)
        p.add_argument("--source")
        p.add_argument("--dataset")
        p.add_argument("--domain")
    sub.add_parser("status")
    a = ap.parse_args(argv)

    if a.cmd == "list":
        reg = load_registry()
        n = 0
        for s, d in iter_datasets(reg, a.source, a.dataset, a.domain):
            print(f"{d.key:55} {d.frequency:10} {','.join(d.domains):30} {'✓' if d.verified else '?'}")
            n += 1
        print(f"\n{n} datasets across {len(reg)} sources")
    elif a.cmd == "ingest":
        res = run(a.source, a.dataset, a.domain)
        bad = [r for r in res if r["status"] in ("failed", "rejected")]
        print(f"\n{len(res)} datasets: {sum(r['status']=='published' for r in res)} published, "
              f"{sum(r['status']=='unchanged' for r in res)} unchanged, {len(bad)} failed/rejected")
        sys.exit(0)  # failures are reported, not fatal: one dead endpoint must not block the rest
    elif a.cmd == "status":
        print(json.dumps(json.loads(STATUS.read_text()) if STATUS.exists() else {}, indent=2))


if __name__ == "__main__":
    main()
