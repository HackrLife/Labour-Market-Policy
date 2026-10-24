"""Summarise executed notebooks: which ran cleanly, which raised, and the first error.

Writes Markdown to stdout (the analysis workflow saves it as notebooks/HEALTH.md).
"""

import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "notebooks"
rows = []
for nb in sorted(root.rglob("*.ipynb")):
    cells = json.loads(nb.read_text())["cells"]
    errs = [o for c in cells if c["cell_type"] == "code" for o in c.get("outputs", [])
            if o.get("output_type") == "error"]
    ran = any(c.get("execution_count") for c in cells if c["cell_type"] == "code")
    status = "not run" if not ran else ("error" if errs else "ok")
    first = f"{errs[0]['ename']}: {errs[0]['evalue'][:120]}" if errs else ""
    rows.append((nb.relative_to(root).as_posix(), status, first))

ok = sum(r[1] == "ok" for r in rows)
print(f"# Notebook health\n\n{ok} of {len(rows)} notebooks executed without errors.\n")
print("| Notebook | Status | First error |\n|---|---|---|")
for r in rows:
    print(f"| `{r[0]}` | {r[1]} | {r[2].replace('|', '/')} |")
sys.exit(0)
