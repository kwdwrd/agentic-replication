#!/usr/bin/env python3
"""
01_setup.py
Setup script for the VBM replication project.

This script:
1. Verifies the project directory structure
2. Checks for required dependencies
3. Validates the original data files
4. Creates necessary output directories

Usage:
    python code/01_setup.py
"""

import sys
from pathlib import Path

# Set project directory
PROJECT_DIR = Path(__file__).parent.parent


def check_directory_structure():
    """Verify required directories exist."""
    print("Checking directory structure...")

    required_dirs = [
        "code",
        "data",
        "data/extension",
        "data/combined",
        "original",
        "original/data/modified",
        "output",
        "output/tables",
        "output/figures",
        "notes",
        "paper",
    ]

    missing = []
    for d in required_dirs:
        path = PROJECT_DIR / d
        if not path.exists():
            missing.append(d)
            path.mkdir(parents=True, exist_ok=True)
            print(f"  Created: {d}")
        else:
            print(f"  ✓ {d}")

    return len(missing) == 0


def check_dependencies():
    """Check for required Python packages."""
    print("\nChecking dependencies...")

    packages = {
        "pandas": "Data manipulation",
        "numpy": "Numerical operations",
        "statsmodels": "Statistical models",
    }

    optional_packages = {
        "pyfixest": "Fixed effects regression (optional, recommended)",
    }

    missing = []

    for pkg, desc in packages.items():
        try:
            __import__(pkg)
            print(f"  ✓ {pkg}: {desc}")
        except ImportError:
            print(f"  ✗ {pkg}: {desc} (MISSING)")
            missing.append(pkg)

    for pkg, desc in optional_packages.items():
        try:
            __import__(pkg)
            print(f"  ✓ {pkg}: {desc}")
        except ImportError:
            print(f"  ⚠ {pkg}: {desc} (optional, not installed)")

    if missing:
        print(f"\nMissing required packages: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
        return False

    return True


def check_original_data():
    """Verify original data files exist."""
    print("\nChecking original data...")

    required_files = [
        "original/data/modified/analysis.dta",
    ]

    all_found = True
    for f in required_files:
        path = PROJECT_DIR / f
        if path.exists():
            # Get file size
            size = path.stat().st_size
            print(f"  ✓ {f} ({size:,} bytes)")
        else:
            print(f"  ✗ {f} (MISSING)")
            all_found = False

    if not all_found:
        print("\nOriginal data missing. Please ensure the original replication")
        print("materials are placed in the 'original/' directory.")

    return all_found


def check_extension_data():
    """Check extension data files."""
    print("\nChecking extension data...")

    extension_files = [
        ("data/extension/california_vca_adoption.csv", True),
        ("data/extension/three_states_2020_pres.csv", True),
        ("data/extension/treatment_extension.csv", True),
        ("data/extension/three_states_2022_gov.csv", False),  # Optional
        ("data/extension/three_states_2024_pres.csv", False),  # Optional
    ]

    for f, required in extension_files:
        path = PROJECT_DIR / f
        if path.exists():
            size = path.stat().st_size
            print(f"  ✓ {f} ({size:,} bytes)")
        elif required:
            print(f"  ⚠ {f} (not found - will be created by 03_collect_extension.py)")
        else:
            print(f"  - {f} (optional, not found)")

    return True


def main():
    """Run all setup checks."""
    print("=" * 60)
    print("VBM REPLICATION PROJECT SETUP")
    print("=" * 60)

    checks = [
        ("Directory structure", check_directory_structure),
        ("Dependencies", check_dependencies),
        ("Original data", check_original_data),
        ("Extension data", check_extension_data),
    ]

    results = {}
    for name, check_func in checks:
        results[name] = check_func()

    # Summary
    print("\n" + "=" * 60)
    print("SETUP SUMMARY")
    print("=" * 60)

    all_pass = True
    for name, passed in results.items():
        status = "✓ Pass" if passed else "✗ Fail"
        print(f"  {name}: {status}")
        if not passed:
            all_pass = False

    if all_pass:
        print("\n*** Setup complete. Ready to run analysis. ***")
        print("\nNext steps:")
        print("  1. Run: python code/00_run_all.py")
        print("  Or run individual scripts:")
        print("  2. python code/02_replicate.py")
        print("  3. python code/03_collect_extension.py")
        print("  4. python code/04_merge_extension.py")
        print("  5. python code/05_extension_analysis.py")
    else:
        print("\n*** Setup incomplete. Please address the issues above. ***")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
