#!/usr/bin/env python3
"""
00_run_all.py
Master script to run the complete replication and extension analysis.

This script executes all analysis steps in order:
1. Replicate original findings (02_replicate.py)
2. Collect extension data (03_collect_extension.py)
3. Merge and prepare extension dataset (04_merge_extension.py)
4. Run extension analysis (05_extension_analysis.py)

Usage:
    python code/00_run_all.py

Requirements:
    - Python 3.8+
    - pandas, numpy, pyfixest, statsmodels
    - Original data in original/data/modified/analysis.dta
"""

import subprocess
import sys
from pathlib import Path
import time

# Set project directory
PROJECT_DIR = Path(__file__).parent.parent
CODE_DIR = PROJECT_DIR / "code"


def run_script(script_name, description):
    """Run a Python script and capture output."""
    script_path = CODE_DIR / script_name

    print("\n" + "=" * 70)
    print(f"RUNNING: {description}")
    print(f"Script: {script_name}")
    print("=" * 70 + "\n")

    start_time = time.time()

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(PROJECT_DIR),
        capture_output=True,
        text=True
    )

    elapsed = time.time() - start_time

    # Print output
    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print("STDERR:", result.stderr)

    if result.returncode != 0:
        print(f"\n*** ERROR: {script_name} failed with return code {result.returncode} ***")
        return False

    print(f"\nCompleted in {elapsed:.1f} seconds")
    return True


def main():
    """Run all analysis scripts."""
    print("=" * 70)
    print("VBM REPLICATION AND EXTENSION - MASTER RUN SCRIPT")
    print("Thompson et al. (2020) Replication")
    print("=" * 70)

    scripts = [
        ("02_replicate.py", "Phase 2: Replicate Original Findings"),
        ("03_collect_extension.py", "Phase 3: Collect Extension Data"),
        ("04_merge_extension.py", "Phase 4: Merge and Prepare Extension Dataset"),
        ("05_extension_analysis.py", "Phase 5: Extension Analysis"),
    ]

    results = {}
    all_success = True

    for script, description in scripts:
        success = run_script(script, description)
        results[script] = success
        if not success:
            all_success = False
            print(f"\n*** Stopping due to error in {script} ***")
            break

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    for script, success in results.items():
        status = "✓ Success" if success else "✗ Failed"
        print(f"  {script}: {status}")

    if all_success:
        print("\n*** ALL ANALYSES COMPLETED SUCCESSFULLY ***")

        # List output files
        print("\nOutput files created:")
        output_dir = PROJECT_DIR / "output" / "tables"
        if output_dir.exists():
            for f in sorted(output_dir.glob("*.csv")):
                print(f"  - output/tables/{f.name}")

        data_dir = PROJECT_DIR / "data" / "combined"
        if data_dir.exists():
            for f in sorted(data_dir.glob("*")):
                print(f"  - data/combined/{f.name}")

    return 0 if all_success else 1


if __name__ == "__main__":
    sys.exit(main())
