"""
01_examine_original.py

Examine the original analysis data from Thompson et al. (2020)
to understand structure, variables, and prepare for replication.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Set paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "original" / "data" / "modified"
OUTPUT_DIR = PROJECT_ROOT / "notes"

def main():
    # Load main analysis dataset
    print("=" * 60)
    print("EXAMINING ORIGINAL ANALYSIS DATA")
    print("=" * 60)

    analysis = pd.read_stata(DATA_DIR / "analysis.dta")

    # Basic dimensions
    print(f"\n1. DIMENSIONS")
    print(f"   Rows: {analysis.shape[0]}")
    print(f"   Columns: {analysis.shape[1]}")

    # States and counties
    print(f"\n2. GEOGRAPHIC COVERAGE")
    print(f"   States: {sorted(analysis['state'].unique())}")
    for state in sorted(analysis['state'].unique()):
        n_counties = analysis[analysis['state'] == state]['county'].nunique()
        print(f"   - {state}: {n_counties} counties")

    # Years
    print(f"\n3. TEMPORAL COVERAGE")
    print(f"   Years: {sorted(analysis['year'].unique())}")
    print(f"   Number of years: {analysis['year'].nunique()}")

    # Treatment variable
    print(f"\n4. TREATMENT VARIABLE ('treat')")
    print(f"   Overall treatment rate: {analysis['treat'].mean():.3f}")
    print(f"\n   Treatment by state and year:")
    treat_by_state_year = analysis.groupby(['state', 'year'])['treat'].mean().unstack(level=0)
    print(treat_by_state_year.to_string())

    # Key outcome variables
    print(f"\n5. KEY OUTCOME VARIABLES")

    # Partisan outcomes
    print(f"\n   a) Partisan Turnout Share (share_votes_dem):")
    print(f"      - Available for: {analysis[analysis['share_votes_dem'].notna()]['state'].unique()}")
    print(f"      - N non-missing: {analysis['share_votes_dem'].notna().sum()}")
    print(f"      - Mean: {analysis['share_votes_dem'].mean():.3f}")
    print(f"      - Std: {analysis['share_votes_dem'].std():.3f}")
    print(f"      - Range: [{analysis['share_votes_dem'].min():.3f}, {analysis['share_votes_dem'].max():.3f}]")

    # Vote share outcomes
    print(f"\n   b) Democratic Vote Share Variables:")
    for var in ['dem_share_gov', 'dem_share_pres', 'dem_share_sen']:
        if var in analysis.columns:
            n_obs = analysis[var].notna().sum()
            mean_val = analysis[var].mean()
            print(f"      - {var}: N={n_obs}, Mean={mean_val:.3f}")

    # Participation outcomes
    print(f"\n   c) Turnout Share (turnout_share):")
    print(f"      - N non-missing: {analysis['turnout_share'].notna().sum()}")
    print(f"      - Mean: {analysis['turnout_share'].mean():.3f}")
    print(f"      - Std: {analysis['turnout_share'].std():.3f}")

    print(f"\n   d) VBM Share (vbm_share):")
    print(f"      - Available for: {analysis[analysis['vbm_share'].notna()]['state'].unique()}")
    print(f"      - N non-missing: {analysis['vbm_share'].notna().sum()}")
    print(f"      - Mean: {analysis['vbm_share'].mean():.3f}")

    # Fixed effect variables
    print(f"\n6. FIXED EFFECT VARIABLES")
    print(f"   - county_id: {analysis['county_id'].nunique()} unique values")
    print(f"   - state_year_id: {analysis['state_year_id'].nunique()} unique values")

    # Trend variables
    print(f"\n7. TREND VARIABLES")
    print(f"   - year: {analysis['year'].min()} to {analysis['year'].max()}")
    print(f"   - year2 (year squared): present = {'year2' in analysis.columns}")

    # Sample sizes for key regressions
    print(f"\n8. SAMPLE SIZES FOR KEY REGRESSIONS")

    # Table 2, Cols 1-3: share_votes_dem (CA and UT only)
    sample_partisan_turnout = analysis[
        (analysis['share_votes_dem'].notna()) &
        (analysis['state'].isin(['CA', 'UT']))
    ]
    print(f"   Table 2, Cols 1-3 (Dem turnout share, CA+UT):")
    print(f"      - N obs: {len(sample_partisan_turnout)}")
    print(f"      - N counties: {sample_partisan_turnout['county_id'].nunique()}")

    # Table 2, Cols 4-6: dem_share (all states, reshaped)
    # Need to check how many observations have at least one office
    sample_vote_share = analysis[
        (analysis['dem_share_gov'].notna()) |
        (analysis['dem_share_pres'].notna()) |
        (analysis['dem_share_sen'].notna())
    ]
    print(f"   Table 2, Cols 4-6 (Dem vote share, all states):")
    print(f"      - N county-years with any vote share: {len(sample_vote_share)}")
    print(f"      - N counties: {sample_vote_share['county_id'].nunique()}")

    # Table 3, Cols 1-3: turnout_share (all states)
    sample_turnout = analysis[analysis['turnout_share'].notna()]
    print(f"   Table 3, Cols 1-3 (Turnout, all states):")
    print(f"      - N obs: {len(sample_turnout)}")
    print(f"      - N counties: {sample_turnout['county_id'].nunique()}")

    # Table 3, Cols 4-6: vbm_share (CA only)
    sample_vbm = analysis[(analysis['vbm_share'].notna()) & (analysis['state'] == 'CA')]
    print(f"   Table 3, Cols 4-6 (VBM share, CA only):")
    print(f"      - N obs: {len(sample_vbm)}")
    print(f"      - N counties: {sample_vbm['county_id'].nunique()}")

    # Check for California VCA counties
    print(f"\n9. CALIFORNIA VCA ADOPTION")
    ca_data = analysis[analysis['state'] == 'CA']
    vca_counties_2018 = ca_data[ca_data['vca18'] == 1]['county'].unique()
    print(f"   VCA 2018 counties: {list(vca_counties_2018)}")

    # Summary statistics table
    print(f"\n10. SUMMARY STATISTICS")
    summary_vars = ['treat', 'turnout_share', 'vbm_share', 'share_votes_dem',
                    'dem_share_gov', 'dem_share_pres']
    summary_stats = analysis[summary_vars].describe()
    print(summary_stats.to_string())

    # Save examination results to markdown
    save_examination_results(analysis, OUTPUT_DIR / "original_data_examination.md")

    print(f"\n" + "=" * 60)
    print("Examination complete. Results saved to notes/original_data_examination.md")
    print("=" * 60)

def save_examination_results(df, output_path):
    """Save detailed examination results to markdown file."""

    with open(output_path, 'w') as f:
        f.write("# Original Data Examination\n\n")
        f.write("This document provides detailed examination of the original analysis dataset.\n\n")

        f.write("## 1. Dataset Dimensions\n\n")
        f.write(f"- **Rows**: {df.shape[0]}\n")
        f.write(f"- **Columns**: {df.shape[1]}\n")
        f.write(f"- **Unit of analysis**: County-year (general elections)\n\n")

        f.write("## 2. Geographic Coverage\n\n")
        f.write("| State | Counties | Observations |\n")
        f.write("|-------|----------|-------------|\n")
        for state in sorted(df['state'].unique()):
            state_data = df[df['state'] == state]
            f.write(f"| {state} | {state_data['county'].nunique()} | {len(state_data)} |\n")
        f.write(f"| **Total** | **{df['county'].nunique()}** | **{len(df)}** |\n\n")

        f.write("## 3. Temporal Coverage\n\n")
        f.write(f"- **Years**: {min(df['year'])} - {max(df['year'])}\n")
        f.write(f"- **Election years**: {sorted(df['year'].unique())}\n\n")

        f.write("## 4. Treatment Variable\n\n")
        f.write("The `treat` variable equals 1 if a county has universal VBM in that year.\n\n")
        f.write("### Treatment Rate by State and Year\n\n")
        treat_pivot = df.groupby(['year', 'state'])['treat'].mean().unstack()
        f.write("| Year | CA | UT | WA |\n")
        f.write("|------|----|----|----|\n")
        for year in sorted(df['year'].unique()):
            row = f"| {year} |"
            for state in ['CA', 'UT', 'WA']:
                if state in treat_pivot.columns and year in treat_pivot.index:
                    val = treat_pivot.loc[year, state]
                    if pd.notna(val):
                        row += f" {val:.2f} |"
                    else:
                        row += " - |"
                else:
                    row += " - |"
            f.write(row + "\n")
        f.write("\n")

        f.write("## 5. Key Outcome Variables\n\n")
        f.write("### Summary Statistics\n\n")
        f.write("| Variable | N | Mean | Std | Min | Max |\n")
        f.write("|----------|---|------|-----|-----|-----|\n")
        for var in ['share_votes_dem', 'dem_share_gov', 'dem_share_pres', 'dem_share_sen',
                    'turnout_share', 'vbm_share']:
            if var in df.columns:
                n = df[var].notna().sum()
                mean = df[var].mean()
                std = df[var].std()
                min_val = df[var].min()
                max_val = df[var].max()
                f.write(f"| {var} | {n} | {mean:.3f} | {std:.3f} | {min_val:.3f} | {max_val:.3f} |\n")
        f.write("\n")

        f.write("### Variable Availability by State\n\n")
        f.write("| Variable | CA | UT | WA |\n")
        f.write("|----------|----|----|----|\n")
        for var in ['share_votes_dem', 'turnout_share', 'vbm_share']:
            row = f"| {var} |"
            for state in ['CA', 'UT', 'WA']:
                state_data = df[df['state'] == state]
                n_avail = state_data[var].notna().sum()
                row += f" {n_avail} |"
            f.write(row + "\n")
        f.write("\n")

        f.write("## 6. Sample Sizes for Key Regressions\n\n")
        f.write("| Table | Outcome | States | N Obs | N Counties |\n")
        f.write("|-------|---------|--------|-------|------------|\n")

        # Table 2, Cols 1-3
        sample = df[(df['share_votes_dem'].notna()) & (df['state'].isin(['CA', 'UT']))]
        f.write(f"| Table 2, Cols 1-3 | Dem turnout share | CA, UT | {len(sample)} | {sample['county_id'].nunique()} |\n")

        # Table 2, Cols 4-6 (need to count reshaped observations)
        sample = df[(df['dem_share_gov'].notna()) | (df['dem_share_pres'].notna()) | (df['dem_share_sen'].notna())]
        f.write(f"| Table 2, Cols 4-6 | Dem vote share | All | {len(sample)} | {sample['county_id'].nunique()} |\n")

        # Table 3, Cols 1-3
        sample = df[df['turnout_share'].notna()]
        f.write(f"| Table 3, Cols 1-3 | Turnout | All | {len(sample)} | {sample['county_id'].nunique()} |\n")

        # Table 3, Cols 4-6
        sample = df[(df['vbm_share'].notna()) & (df['state'] == 'CA')]
        f.write(f"| Table 3, Cols 4-6 | VBM share | CA | {len(sample)} | {sample['county_id'].nunique()} |\n")
        f.write("\n")

        f.write("## 7. California VCA Adoption\n\n")
        ca_data = df[df['state'] == 'CA']
        vca18 = ca_data[ca_data['vca18'] == 1]['county'].unique()
        vca20 = ca_data[ca_data['vca20'] == 1]['county'].unique()
        f.write(f"- **VCA 2018 counties** (5): {', '.join(sorted(vca18))}\n")
        f.write(f"- **VCA 2020 eligible** ({len(vca20)}): {', '.join(sorted(vca20))}\n\n")

        f.write("## 8. Missing Data Patterns\n\n")
        f.write("| Variable | Missing | Pct Missing |\n")
        f.write("|----------|---------|-------------|\n")
        for var in ['treat', 'turnout_share', 'vbm_share', 'share_votes_dem',
                    'dem_share_gov', 'dem_share_pres', 'dem_share_sen']:
            if var in df.columns:
                n_miss = df[var].isna().sum()
                pct_miss = 100 * n_miss / len(df)
                f.write(f"| {var} | {n_miss} | {pct_miss:.1f}% |\n")

if __name__ == "__main__":
    main()
