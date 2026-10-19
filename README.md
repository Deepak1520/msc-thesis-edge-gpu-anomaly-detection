# Lightweight AI for Detecting Irregular Behavior in GPU Node Telemetry

MSc Data Science thesis, University of Göttingen / GWDG.
Author: Deepak Budha · Supervisor: Michael Bidollahkhani · 1st reviewer: Prof. Dr. Julian Kunkel

The thesis compares lightweight anomaly detectors (Isolation Forest, Dense Autoencoder) for
structural GPU failures ("fallen off bus") in production HPC telemetry, compresses them, and
measures the trade-off between detection quality and resource use on a CPU-only companion node.
Current proposal: [thesis/updated_thesis_proposal.pdf](thesis/updated_thesis_proposal.pdf).

## Layout

```
config/       pipeline settings (window, thresholds, seed)
data/         not in git, see "Data" below
  raw/        Zenodo dataset as downloaded, never edited
  extracted/  unpacked CSVs           (src/unzip.py)
  interim/    merged per-node tables  (preprocessing)
  processed/  train/val/test tables   (preprocessing)
src/          reusable code; paths.py defines every folder path
notebooks/    exploration, numbered in the order the work was done
reports/      small results for the thesis: tables, figures, data card
literature/   papers
thesis/       proposal, literature review, drafts
```

Everything in `data/` except `raw/` can be deleted and rebuilt from `raw/`.

## Data

GWDG GPU Node Telemetry Dataset, https://doi.org/10.5281/zenodo.19052367.
Download it and place its contents in `data/raw/` so that it contains
`telemetry/`, `metadata/`, `docs/`, `manifest.csv` and `incident_events.csv`.

## Setup

```bash
pip install -r requirements.txt
python src/unzip.py data/raw/telemetry --out data/extracted
```

Notebooks find the repo root themselves, so they run from any working directory.
In code, import paths from `src.paths` instead of writing them out:

```python
from src.paths import DATA_RAW, EXTRACTED
```

## Notebooks

| Notebook | What it covers |
|---|---|
| 01_eda_incident_events | Incident log: 69 incidents, 26 nodes, categories, same-day clusters |
| 02_provenance_audit | Which incidents have telemetry (15 of 69, 7 nodes); writes `reports/incident_telemetry_audit.csv` |
| 03_telemetry_first_look | First telemetry file, metric list, first t0 detector run |
