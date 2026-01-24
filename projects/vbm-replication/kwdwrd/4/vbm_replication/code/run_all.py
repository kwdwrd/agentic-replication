#!/usr/bin/env python3
"""
run_all.py

Master script to run the complete VBM replication and extension analysis.
Executes all analysis scripts in order.

Usage:
    python code/run_all.py
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CODE_DIR = PROJECT_ROOT / "code"

def run_script(script_name, description):
    """Run a Python script and report status."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Script: {script_name}")
    print('='*60)

    script_path = CODE_DIR / script_name
    result = subprocess.run([sys.executable, str(script_path)], cwd=PROJECT_ROOT)

    if result.returncode != 0:
        print(f"\nERROR: {script_name} failed with return code {result.returncode}")
        sys.exit(1)

    print(f"\n{script_name} completed successfully")


def main():
    print("="*60)
    print("VBM REPLICATION AND EXTENSION ANALYSIS")
    print("Thompson et al. (2020) PNAS")
    print("="*60)

    # Step 1: Examine original data
    run_script("01_examine_original.py", "Step 1: Examine Original Data")

    # Step 2: Replicate original findings
    run_script("02_replicate.py", "Step 2: Replicate Original Findings")

    # Step 3: Generate extension data (for 2020-2024)
    run_script("03_collect_extension.py", "Step 3: Generate Extension Data")

    # Step 4: Prepare combined dataset
    run_script("04_prepare_data.py", "Step 4: Prepare Combined Dataset")

    # Step 5: Extension analysis
    run_script("05_extension_analysis.py", "Step 5: Extension Analysis")

    print("\n" + "="*60)
    print("ALL ANALYSES COMPLETED SUCCESSFULLY")
    print("="*60)

    print("\nOutputs saved to:")
    print("  - output/tables/  (CSV result tables)")
    print("  - output/figures/ (Event study plot)")
    print("\nKey result files:")
    print("  - table2_replication.csv     (Dem vote share replication)")
    print("  - table3_replication.csv     (Turnout replication)")
    print("  - extension_main_results.csv (Extended sample results)")
    print("  - extension_heterogeneity.csv (Period interaction tests)")
    print("  - event_study.png            (Event study figure)")


if __name__ == "__main__":
    main()
