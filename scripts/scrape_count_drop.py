"""
scrapeCountDrop onset-detection function.

Implements the alignment rule from Bidollahkhani, Nordsiek & Kunkel (2026),
"When GPUs Fail Quietly": t0 is derived from Prometheus scrape payload
collapse, using a 600s expected scrape interval and a 3000s dropout
threshold. t0 is defined as the LAST GOOD scrape timestamp immediately
before the gap (not the moment the gap ends).

Usage:
    from scrape_count_drop import detect_scrape_collapse

    result = detect_scrape_collapse("path/to/incident_tidy.csv")
    print(result)
"""
import pandas as pd


def detect_scrape_collapse(
    filepath_or_df,
    time_col: str = "timeUtc",
    node_col: str = "node",
    expected_interval_s: int = 600,
    gap_threshold_s: int = 3000,
):
    """
    Detects scrape-payload collapse events (candidate GPU detachment onsets)
    in a telemetry file, per-node.

    Parameters
    ----------
    filepath_or_df : str or pd.DataFrame
        Path to a tidy incident telemetry CSV, or an already-loaded DataFrame.
    time_col : str
        Name of the timestamp column.
    node_col : str
        Name of the node identifier column.
    expected_interval_s : int
        Expected scrape cadence in seconds (paper default: 600s / 10 min).
    gap_threshold_s : int
        Gap size beyond which a scrape is considered "collapsed"
        (paper default: 3000s / 50 min).

    Returns
    -------
    pd.DataFrame with columns:
        node, t0, gap_start, gap_end, gap_seconds, n_gaps_found
    One row per detected gap, per node. Empty DataFrame if no node
    exceeds the threshold anywhere in the file.
    """
    if isinstance(filepath_or_df, str):
        df = pd.read_csv(filepath_or_df, parse_dates=[time_col])
    else:
        df = filepath_or_df.copy()
        if not pd.api.types.is_datetime64_any_dtype(df[time_col]):
            df[time_col] = pd.to_datetime(df[time_col])

    results = []

    for node, group in df.groupby(node_col):
        # Long-format data has many rows per timestamp (one per metric/gpu).
        # Scrape cadence is a per-node pipeline property, so dedupe timestamps.
        timestamps = group[time_col].drop_duplicates().sort_values().reset_index(drop=True)

        if len(timestamps) < 2:
            continue

        diffs = timestamps.diff().dt.total_seconds()

        gap_mask = diffs > gap_threshold_s
        gap_indices = diffs[gap_mask].index

        n_gaps = len(gap_indices)

        for idx in gap_indices:
            t0 = timestamps.iloc[idx - 1]        # last good scrape before the gap
            gap_end = timestamps.iloc[idx]        # first scrape after resuming
            gap_seconds = diffs.iloc[idx]

            results.append({
                "node": node,
                "t0": t0,
                "gap_start": t0,
                "gap_end": gap_end,
                "gap_seconds": gap_seconds,
                "n_gaps_found": n_gaps,
            })

    return pd.DataFrame(results)


if __name__ == "__main__":
    # Quick self-test against the mock file with a known injected gap.
    result = detect_scrape_collapse("C:\Personal\data\extracted\ggpu121_2025-02-10_gpu-error_tidy.csv")
    print("Detected collapse(s):")
    print(result.to_string(index=False))