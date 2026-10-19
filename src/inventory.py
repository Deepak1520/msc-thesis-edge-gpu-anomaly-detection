"""
Metric inventory: one row per metric with its plane, kind and handling flags.

Writes reports/metric_planes.csv, which every later preprocessing step reads
instead of re-deciding how to treat a metric.

Run from the repo root:
    python -m src.inventory
"""
import json

import pandas as pd

from src.paths import EXTRACTED, METADATA, REPORTS

# counters that do not follow the Prometheus *_total naming convention
EXTRA_COUNTERS = {
    "DCGM_FI_DEV_TOTAL_ENERGY_CONSUMPTION",
    "DCGM_FI_DEV_PCIE_REPLAY_COUNTER",
}

# label-only metrics: constant 1, their text labels were removed by sanitization
DROP_SUFFIXES = ("_info", "_sensor_label", "_chip_names")


def plane_of(metric: str) -> str:
    if metric.startswith("DCGM_"):
        return "GPU"
    if metric.startswith("node_"):
        return "OS"
    if metric.startswith(("scrape_", "promhttp_")):
        return "OBS"
    if metric.startswith("ipmi_"):
        return "IPMI"
    return "OTHER"


def kind_of(metric: str) -> str:
    # DCGM_FI_DEV_XID_ERRORS is deliberately a gauge: it holds the last XID code, not a count
    if metric.endswith("_total") or metric in EXTRA_COUNTERS:
        return "counter"
    return "gauge"


def incident_files() -> list[str]:
    """Stems of the 16 incident-scoped files (the node-wide-totals files are not telemetry)."""
    stems = []
    for meta_path in sorted(METADATA.glob("*_meta.json")):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if meta["inputType"] == "label-heavy-prometheus":
            stems.append(meta_path.name.replace("_meta.json", ""))
    return stems


def scan_file(stem: str) -> pd.DataFrame:
    """Per metric: max rows per (timestamp, gpu), number of GPUs, timestamps present."""
    df = pd.read_csv(
        EXTRACTED / f"{stem}_tidy.csv",
        usecols=["timeUtc", "metric", "gpu"],
        dtype=str,
    )
    df["gpu"] = df["gpu"].fillna("")
    per_key = df.groupby(["metric", "gpu", "timeUtc"]).size()
    out = pd.DataFrame({
        "max_rows_per_ts": per_key.groupby(level="metric").max(),
        "n_gpus": df[df["gpu"] != ""].groupby("metric")["gpu"].nunique(),
        "n_timestamps": df.groupby("metric")["timeUtc"].nunique(),
    })
    out["n_gpus"] = out["n_gpus"].fillna(0).astype(int)
    out["file"] = stem
    return out.reset_index()


def main():
    stems = incident_files()
    print(f"scanning {len(stems)} incident files")
    scans = []
    for stem in stems:
        scans.append(scan_file(stem))
        print(f"  {stem}")
    scans = pd.concat(scans, ignore_index=True)

    inv = scans.groupby("metric").agg(
        n_files=("file", "nunique"),
        max_rows_per_ts=("max_rows_per_ts", "max"),
        n_gpus=("n_gpus", "max"),
    ).reset_index()

    inv["plane"] = inv["metric"].map(plane_of)
    inv["kind"] = inv["metric"].map(kind_of)
    inv["per_gpu"] = inv["n_gpus"] > 0
    inv["multi_row"] = inv["max_rows_per_ts"] > 1
    inv["keep"] = ~inv["metric"].str.endswith(DROP_SUFFIXES) & (inv["n_files"] == len(stems))
    inv["note"] = ""
    inv.loc[inv["n_files"] < len(stems), "note"] = "missing in some files"
    inv.loc[inv["metric"].str.endswith(DROP_SUFFIXES), "note"] = "label-only metric"
    inv.loc[inv["metric"] == "DCGM_FI_DEV_XID_ERRORS", "note"] = "last XID code, not a count"

    cols = ["metric", "plane", "kind", "per_gpu", "n_gpus", "multi_row",
            "max_rows_per_ts", "n_files", "keep", "note"]
    inv = inv[cols].sort_values(["plane", "metric"])
    REPORTS.mkdir(exist_ok=True)
    inv.to_csv(REPORTS / "metric_planes.csv", index=False)

    print(f"\nwrote {REPORTS / 'metric_planes.csv'} ({len(inv)} metrics)")
    print(inv.groupby(["plane", "kind"]).size().unstack(fill_value=0))
    print("\nkept:", inv["keep"].sum(), "| dropped:", (~inv["keep"]).sum())
    print("multi_row metrics:", inv["multi_row"].sum())
    print(inv.loc[inv["multi_row"], ["metric", "kind", "max_rows_per_ts", "keep"]].to_string(index=False))


if __name__ == "__main__":
    main()
