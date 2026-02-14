"""
01_examine_original.py
Examine the original analysis data from Thompson et al. (2020)
"""

import pandas as pd
import numpy as np
import os

# Set paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, 'original', 'data', 'modified')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'notes')

def load_analysis_data():
    """Load the main analysis dataset"""
    path = os.path.join(DATA_DIR, 'analysis.dta')
    return pd.read_stata(path)

def examine_data(df):
    """Generate comprehensive data examination report"""

    report = []
    report.append("=" * 70)
    report.append("ORIGINAL DATA EXAMINATION")
    report.append("=" * 70)

    # Basic dimensions
    report.append(f"\n1. DIMENSIONS")
    report.append("-" * 40)
    report.append(f"Rows: {df.shape[0]:,}")
    report.append(f"Columns: {df.shape[1]}")

    # Key variables
    report.append(f"\n2. KEY VARIABLE NAMES")
    report.append("-" * 40)
    key_vars = ['state', 'county', 'year', 'prim_or_gen', 'treat',
                'share_votes_dem', 'dem_share_gov', 'dem_share_pres',
                'turnout_share', 'vbm_share', 'cvap',
                'county_id', 'state_year_id', 'year2']
    for v in key_vars:
        if v in df.columns:
            report.append(f"  {v}: present")
        else:
            report.append(f"  {v}: MISSING")

    # Geographic coverage
    report.append(f"\n3. GEOGRAPHIC COVERAGE")
    report.append("-" * 40)
    for state in ['CA', 'UT', 'WA']:
        state_df = df[df['state'] == state]
        n_counties = state_df['county'].nunique()
        n_obs = len(state_df)
        report.append(f"{state}: {n_counties} counties, {n_obs} observations")
    report.append(f"Total: {df['county'].nunique()} counties, {len(df)} observations")

    # Time coverage
    report.append(f"\n4. TIME COVERAGE")
    report.append("-" * 40)
    years = sorted(df['year'].unique())
    report.append(f"Years: {min(years)} - {max(years)}")
    report.append(f"Election years: {years}")
    report.append(f"Number of elections: {len(years)}")

    # Election types
    report.append(f"\n5. ELECTION TYPES")
    report.append("-" * 40)
    report.append(str(df['prim_or_gen'].value_counts()))

    # Treatment variable
    report.append(f"\n6. TREATMENT VARIABLE (treat)")
    report.append("-" * 40)
    report.append(f"Overall: {df['treat'].mean():.3f} treated")
    for state in ['CA', 'UT', 'WA']:
        state_df = df[df['state'] == state]
        pct = state_df['treat'].mean() * 100
        n_treated = state_df['treat'].sum()
        report.append(f"{state}: {n_treated:.0f} treated obs ({pct:.1f}%)")

    # Key outcome variables - summary statistics
    report.append(f"\n7. KEY OUTCOME VARIABLES - SUMMARY STATISTICS")
    report.append("-" * 40)

    outcomes = {
        'share_votes_dem': 'Dem Turnout Share (CA, UT only)',
        'dem_share_gov': 'Dem Vote Share (Governor)',
        'dem_share_pres': 'Dem Vote Share (President)',
        'turnout_share': 'Turnout (ballots/CVAP)',
        'vbm_share': 'VBM Share (CA only)'
    }

    for var, desc in outcomes.items():
        if var in df.columns:
            valid = df[var].notna()
            report.append(f"\n{var} - {desc}")
            report.append(f"  N: {valid.sum()}")
            report.append(f"  Mean: {df.loc[valid, var].mean():.4f}")
            report.append(f"  Std: {df.loc[valid, var].std():.4f}")
            report.append(f"  Min: {df.loc[valid, var].min():.4f}")
            report.append(f"  Max: {df.loc[valid, var].max():.4f}")

    # Missing values
    report.append(f"\n8. MISSING VALUES FOR KEY VARIABLES")
    report.append("-" * 40)
    for var in outcomes.keys():
        if var in df.columns:
            missing = df[var].isna().sum()
            pct = missing / len(df) * 100
            report.append(f"{var}: {missing} missing ({pct:.1f}%)")

    # Fixed effects IDs
    report.append(f"\n9. FIXED EFFECTS STRUCTURE")
    report.append("-" * 40)
    report.append(f"Unique county_id: {df['county_id'].nunique()}")
    report.append(f"Unique state_year_id: {df['state_year_id'].nunique()}")

    # Sample sizes for Table 2 and Table 3
    report.append(f"\n10. SAMPLE SIZES FOR REPLICATION")
    report.append("-" * 40)

    # Table 2: Dem turnout share (CA, UT only with share_votes_dem)
    t2_dem_turnout = df[df['share_votes_dem'].notna()]
    report.append(f"\nTable 2, Cols 1-3 (Dem Turnout Share):")
    report.append(f"  Sample: CA and UT with share_votes_dem")
    report.append(f"  N: {len(t2_dem_turnout)}")
    report.append(f"  Counties: {t2_dem_turnout['county_id'].nunique()}")

    # Table 2: Dem vote share (all states, governor races)
    # Looking at the code, they use dem_share which combines gov/pres/sen
    # Let's check what dem_share variable exists
    if 'dem_share' in df.columns:
        t2_vote_share = df[df['dem_share'].notna()]
        report.append(f"\nTable 2, Cols 4-6 (Dem Vote Share):")
        report.append(f"  N: {len(t2_vote_share)}")
        report.append(f"  Counties: {t2_vote_share['county_id'].nunique()}")
    else:
        # Need to construct dem_share from gov/pres/sen
        report.append(f"\nNote: dem_share not directly available, need to construct")

    # Table 3: Turnout (all states)
    t3_turnout = df[df['turnout_share'].notna()]
    report.append(f"\nTable 3, Cols 1-3 (Turnout):")
    report.append(f"  N: {len(t3_turnout)}")
    report.append(f"  Counties: {t3_turnout['county_id'].nunique()}")

    # Table 3: VBM share (CA only)
    t3_vbm = df[(df['state'] == 'CA') & (df['vbm_share'].notna())]
    report.append(f"\nTable 3, Cols 4-6 (VBM Share, CA only):")
    report.append(f"  N: {len(t3_vbm)}")
    report.append(f"  Counties: {t3_vbm['county_id'].nunique()}")

    return "\n".join(report)

def save_report(report, filename):
    """Save report to file"""
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, 'w') as f:
        f.write(report)
    print(f"Report saved to: {path}")

if __name__ == "__main__":
    # Load data
    print("Loading analysis data...")
    df = load_analysis_data()

    # Generate examination report
    print("Examining data...")
    report = examine_data(df)

    # Print report
    print(report)

    # Save report
    save_report(report, 'original_data_examination.md')
