"""Parse BLS OEWS May 2025 News Release Table 1 (text of the BLS news release table) into title, employment, indent.
Wrapped titles (a line with no numeric columns followed by a continuation line) are joined."""
import re
import pandas as pd
from pathlib import Path
HERE = Path(__file__).resolve().parent
t = open(HERE / 'inputs' / 'ocwage_t01.txt', encoding='utf-8').read()
pat = re.compile(r'^(\s*)(\S.*?)\s*(?:\.{2,})?\s+([\d,]{3,})\s+\S+\s+\S+\s+\S+\s*$')
rows, started, pending = [], False, None
for line in t.splitlines():
    if line.strip().startswith('All occupations'):
        started = True
    if not started or not line.strip():
        continue
    if line.strip().startswith('1 Annual wages'):
        break
    if pending is not None:
        line = pending[0] + pending[1].strip() + ' ' + line.strip()
        pending = None
    m = pat.match(line)
    if m:
        title = m.group(2).rstrip('. ').strip()
        rows.append((title, int(m.group(3).replace(',', '')), len(m.group(1))))
    else:
        ind = len(line) - len(line.lstrip())
        pending = (' ' * ind, line)
df = pd.DataFrame(rows, columns=['title', 'emp', 'indent'])
df.to_csv(HERE / 'inputs' / 't01_parsed.csv', index=False)
print(len(df), df.emp.iloc[0])
