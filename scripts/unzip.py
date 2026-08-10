"""
Batch-decompress all .bz2 files in a folder (e.g. the GWDG telemetry
folder full of *_tidy.csv.bz2 files).

Usage:
    python batch_unbz2.py "C:\\Personal\\19052367\\...\\telemetry"
    python batch_unbz2.py "C:\\...\\telemetry" --out "C:\\...\\telemetry_extracted"
    python batch_unbz2.py "C:\\...\\telemetry" --keep   # keep the .bz2 originals (default)

Each file.csv.bz2 becomes file.csv in the output folder.
"""

import argparse
import bz2
import shutil
import sys
from pathlib import Path


def decompress_all(source_dir: Path, out_dir: Path):
    bz2_files = sorted(source_dir.glob("*.bz2"))

    if not bz2_files:
        print(f"No .bz2 files found in {source_dir}")
        return

    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Found {len(bz2_files)} .bz2 file(s) in {source_dir}\n")

    succeeded, failed = [], []

    for bz2_path in bz2_files:
        # strip the .bz2 suffix -> e.g. foo.csv.bz2 -> foo.csv
        target_name = bz2_path.stem
        target_path = out_dir / target_name

        try:
            with bz2.open(bz2_path, "rb") as f_in, open(target_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
            print(f"[OK]     {bz2_path.name} -> {target_path}")
            succeeded.append(bz2_path.name)
        except Exception as e:
            print(f"[FAILED] {bz2_path.name}: {e}")
            failed.append(bz2_path.name)

    print(f"\nDone. {len(succeeded)} succeeded, {len(failed)} failed.")
    if failed:
        print("Failed files:", ", ".join(failed))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch-decompress .bz2 files in a folder.")
    parser.add_argument("source_dir", type=str, help="Folder containing .bz2 files")
    parser.add_argument(
        "--out", type=str, default=None,
        help="Destination folder for decompressed files (default: same folder, "
             "a new 'extracted' subfolder is created to avoid mixing with originals)"
    )
    args = parser.parse_args()

    source = Path(args.source_dir).expanduser().resolve()
    if not source.is_dir():
        print(f"Error: {source} is not a directory")
        sys.exit(1)

    out = Path(args.out).expanduser().resolve() if args.out else source / "extracted"

    decompress_all(source, out)