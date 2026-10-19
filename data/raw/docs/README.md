# GWDG GPU Node Telemetry Dataset
Observability-Aware Early Warning for GPU Detachment Failures
Dataset DOI: https://doi.org/10.5281/zenodo.19052367
Version: 1.0.0

This dataset contains sanitized time-series telemetry from production GPU-equipped HPC nodes
at the GWDG infrastructure, aligned with operator-curated GPU failure incidents
(January 2025 to February 2026).

It accompanies the paper:

"When GPUs Fail Quietly: Observability-Aware Early Warning Beyond Numeric Telemetry"

## Purpose
The dataset enables reproducible research on early warning for GPU instability,
particularly detachment-class failures where the dominant signal is structural
observability collapse (metric disappearance, scrape degradation, monitoring gaps).

## Contents
- GPU telemetry (NVIDIA DCGM metrics)
- Node/OS telemetry (Prometheus node exporter)
- Monitoring pipeline metrics (scrape indicators)
- Scheduler state signals (Slurm exporter)
- Incident catalog with timing windows
- Dataset manifest

## Directory Structure

- telemetry/ : time-series telemetry tables (tidy format, compressed)
- metadata/  : metadata describing extraction and context per file
- manifest.csv : dataset coverage and statistics
- incident_events.csv : incident timing and categorization

## File Types
- `*_tidy.csv.bz2`  
  Tidy telemetry tables (time-series)

- `*_meta.json`  
  Metadata describing telemetry extraction

- `incident_events.csv`  
  Incident timing and categorization extracted from SLURM/syslog reports

- `manifest.csv`  
  Dataset coverage and statistics

## Loading Example (Python)
```python
import pandas as pd

df = pd.read_csv("ggpu121_2025-02-10_gpu-error_tidy.csv.bz2")
```

## Authors and Maintainers
This dataset was prepared and released by:
- Michael Bidollahkhani — University of Göttingen  
- Freja Nordsiek — GWDG  
- Julian M. Kunkel — GWDG / University of Göttingen  

> For questions regarding the dataset or its use, please contact:
> Michael Bidollahkhani  
> michael.bkhani@uni-goettingen.de

## Citation

If you use this dataset, please cite:

Bidollahkhani, M., Nordsiek, F., & Kunkel, J. M. (2026).
GWDG GPU Node Telemetry Dataset for Observability-Aware Early Warning of GPU Detachment Failures (2025–2026).
Zenodo. https://doi.org/10.5281/zenodo.19052367