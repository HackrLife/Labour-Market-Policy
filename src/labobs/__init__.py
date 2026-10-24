"""labobs — Labour Observatory ingestion, validation and analysis toolkit."""

from pathlib import Path

__version__ = "0.1.0"

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
REGISTRY_DIR = REPO_ROOT / "registry"
LOG_DIR = REPO_ROOT / "logs"
