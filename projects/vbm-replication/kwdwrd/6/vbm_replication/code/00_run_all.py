#!/usr/bin/env python3
"""
Master script to run all analyses for VBM replication and extension project.

Usage:
    python 00_run_all.py

This script runs all analysis steps in order:
1. Replication of Thompson et al. (2020) Tables 2 and 3
2. Extract CVAP data from Census files
3. Validate extension data collection
4. Build extension and combined datasets
5. Run extension analysis
6. Create figures for paper

Author: [Author Name]
Date: 2024
"""

import subprocess
import sys
import os

def run_script(script_name, description):
    """Run a Python script and report status."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Script: {script_name}")
    print('='*60)

    result = subprocess.run([sys.executable, script_name],
                          capture_output=False,
                          text=True)

    if result.returncode != 0:
        print(f"ERROR: {script_name} failed with return code {result.returncode}")
        return False

    print(f"SUCCESS: {description}")
    return True

def main():
    # Change to code directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    print("="*60)
    print("VBM REPLICATION AND EXTENSION PROJECT")
    print("Master Analysis Script")
    print("="*60)

    scripts = [
        ("02_replicate.py", "Replication of Thompson et al. (2020)"),
        ("extract_cvap.py", "Extract CVAP data from Census files"),
        ("03_validate_extension_data.py", "Validate extension data"),
        ("04_build_extension_dataset.py", "Build extension dataset"),
        ("05_extension_analysis_v2.py", "Run extension analysis"),
        ("06_create_figures.py", "Create figures for paper"),
    ]

    success_count = 0
    for script, description in scripts:
        if os.path.exists(script):
            if run_script(script, description):
                success_count += 1
        else:
            print(f"WARNING: {script} not found, skipping...")

    print("\n" + "="*60)
    print(f"COMPLETE: {success_count}/{len(scripts)} scripts ran successfully")
    print("="*60)

if __name__ == "__main__":
    main()
