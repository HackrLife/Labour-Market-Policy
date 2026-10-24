"""Every dataset key used by a notebook must exist in the registry."""
import json
import re
import unittest
from pathlib import Path

from labobs.registry import load_registry

ROOT = Path(__file__).resolve().parents[1]


class TestNotebookKeys(unittest.TestCase):
    def test_keys_registered(self):
        reg = load_registry()
        known = {d.key for s in reg.values() for d in s.datasets}
        pat = re.compile(r'(?:load|vintage|raw_payload)\("([a-z0-9_]+/[a-z0-9_]+)"')
        missing = set()
        for nb in ROOT.glob("notebooks/**/*.ipynb"):
            text = "".join("".join(c["source"]) for c in json.loads(nb.read_text())["cells"])
            for key in pat.findall(text):
                if key not in known:
                    missing.add(f"{nb.relative_to(ROOT)}: {key}")
        self.assertFalse(missing, "\n".join(sorted(missing)))


if __name__ == "__main__":
    unittest.main()
