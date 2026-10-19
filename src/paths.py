"""
Single source of truth for project paths.

Import from notebooks and scripts instead of hardcoding paths:

    from src.paths import DATA_RAW, EXTRACTED, INTERIM
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# data/raw: the Zenodo dataset as downloaded, never edited
DATA = ROOT / "data"
DATA_RAW = DATA / "raw"
TELEMETRY_RAW = DATA_RAW / "telemetry"     # *_tidy.csv.bz2
METADATA = DATA_RAW / "metadata"           # *_meta.json
DOCS = DATA_RAW / "docs"
MANIFEST = DATA_RAW / "manifest.csv"
INCIDENTS = DATA_RAW / "incident_events.csv"

# derived data, can always be regenerated from data/raw
EXTRACTED = DATA / "extracted"             # unpacked *_tidy.csv (src/unzip.py)
INTERIM = DATA / "interim"                 # merged per-node timelines
PROCESSED = DATA / "processed"             # train/val/test feature tables

# small results that go into the thesis or to the supervisor
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"

CONFIG = ROOT / "config"
