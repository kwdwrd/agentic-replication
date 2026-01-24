"""
04_prepare_data.py

Merge extension data (2020-2024) with original data (1996-2018) to create
a unified analysis dataset for the VBM replication and extension study.

This script:
1. Loads original analysis data
2. Loads extension data files
3. Standardizes variable names across datasets
4. Constructs analysis variables (vote shares, turnout, treatment)
5. Appends extension to original
6. Creates summary statistics
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Set paths
PROJECT_ROOT = Path(__file__).parent.parent
ORIGINAL_DATA = PROJECT_ROOT / "original" / "data" / "modified"
EXTENSION_DATA = PROJECT_ROOT / "data" / "extension"
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "output" / "tables"

PROCESSED_DATA.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_original_data():
    """Load and prepare original analysis data (1996-2018)."""
    print("Loading original data...")
    df = pd.read_stata(ORIGINAL_DATA / "analysis.dta")

    # Keep relevant columns
    cols_to_keep = [
        'state', 'county', 'year', 'treat',
        'dem_share_gov', 'dem_share_pres', 'dem_share_sen',
        'turnout_share', 'vbm_share', 'share_votes_dem',
        'cvap', 'ballots_cast'
    ]
    cols_available = [c for c in cols_to_keep if c in df.columns]
    df = df[cols_available].copy()

    # Add period indicator
    df['period'] = 'original'
    df['post_2018'] = 0

    print(f"  Loaded {len(df)} original observations")
    return df


def load_extension_data():
    """Load and merge all extension data files."""
    print("\nLoading extension data...")

    # Load election results
    ca_results = pd.read_csv(EXTENSION_DATA / "california_results_2020_2024.csv")
    ut_results = pd.read_csv(EXTENSION_DATA / "utah_results_2020_2024.csv")
    wa_results = pd.read_csv(EXTENSION_DATA / "washington_results_2020_2024.csv")

    # Combine all results
    results = pd.concat([ca_results, ut_results, wa_results], ignore_index=True)
    print(f"  Loaded {len(results)} election result observations")

    # Load VCA adoption data for California
    vca = pd.read_csv(EXTENSION_DATA / "california_vbm_adoption.csv")
    print(f"  Loaded VCA adoption data for {len(vca)} CA counties")

    # Load CVAP data
    cvap = pd.read_csv(EXTENSION_DATA / "cvap_2020_2024.csv")
    print(f"  Loaded {len(cvap)} CVAP observations")

    return results, vca, cvap


def construct_treatment_variable(df, vca):
    """
    Construct treatment variable for extension data.

    Treatment = 1 if county has universal VBM in that year:
    - California: VCA adopted (year >= vca_first_year)
    - Utah: All counties 100% VBM by 2019
    - Washington: All counties 100% VBM since 2011
    """
    print("\nConstructing treatment variable...")

    # Merge VCA adoption for California
    df = df.merge(
        vca[['county', 'vca_first_year']],
        on='county',
        how='left'
    )

    # Initialize treatment
    df['treat'] = 0

    # California: treated if year >= vca_first_year
    ca_mask = df['state'] == 'CA'
    df.loc[ca_mask, 'treat'] = (df.loc[ca_mask, 'year'] >= df.loc[ca_mask, 'vca_first_year']).astype(int)

    # Utah: all counties VBM by 2019 (treat = 1 for all 2020+ observations)
    ut_mask = df['state'] == 'UT'
    df.loc[ut_mask, 'treat'] = 1

    # Washington: all counties VBM since 2011 (treat = 1 for all observations)
    wa_mask = df['state'] == 'WA'
    df.loc[wa_mask, 'treat'] = 1

    # Clean up
    df = df.drop(columns=['vca_first_year'], errors='ignore')

    # Report treatment rates
    for state in ['CA', 'UT', 'WA']:
        state_df = df[df['state'] == state]
        treat_rate = state_df['treat'].mean()
        print(f"  {state} treatment rate: {treat_rate:.2%}")

    return df


def construct_outcome_variables(df):
    """
    Construct outcome variables from election results.

    - dem_share: Democratic two-party vote share
    - turnout_share: Total votes / CVAP
    """
    print("\nConstructing outcome variables...")

    # Two-party Democratic vote share
    df['dem_share'] = df['dem_votes'] / (df['dem_votes'] + df['rep_votes'])

    # Verify calculations
    print(f"  dem_share range: [{df['dem_share'].min():.3f}, {df['dem_share'].max():.3f}]")

    return df


def merge_cvap(df, cvap):
    """Merge CVAP data with election results."""
    print("\nMerging CVAP data...")

    df = df.merge(
        cvap,
        on=['state', 'county', 'year'],
        how='left'
    )

    # Calculate turnout
    df['turnout_share'] = df['total_votes'] / df['cvap']

    # Cap turnout at 1.0 (some small counties may exceed due to CVAP estimation)
    df['turnout_share'] = df['turnout_share'].clip(upper=1.0)

    print(f"  turnout_share range: [{df['turnout_share'].min():.3f}, {df['turnout_share'].max():.3f}]")

    return df


def prepare_extension_for_merge(results, vca, cvap):
    """Prepare extension data with all variables needed for analysis."""

    # Construct treatment
    df = construct_treatment_variable(results, vca)

    # Construct outcomes
    df = construct_outcome_variables(df)

    # Merge CVAP and calculate turnout
    df = merge_cvap(df, cvap)

    # Add period indicators
    df['period'] = 'extension'
    df['post_2018'] = 1

    # Reshape to match original data structure
    # Original has separate columns for gov/pres/sen vote shares
    # We'll create those columns based on office

    # Create vote share columns by office
    df['dem_share_gov'] = np.where(df['office'] == 'governor', df['dem_share'], np.nan)
    df['dem_share_pres'] = np.where(df['office'] == 'president', df['dem_share'], np.nan)
    df['dem_share_sen'] = np.where(df['office'] == 'senate', df['dem_share'], np.nan)

    # For the extension, we don't have partisan turnout share (would need voter file)
    df['share_votes_dem'] = np.nan

    # We don't have VBM share data for extension
    df['vbm_share'] = np.nan

    # Add ballots_cast
    df['ballots_cast'] = df['total_votes']

    return df


def create_county_ids(df):
    """Create numeric county IDs consistent with original data."""
    print("\nCreating county IDs...")

    # Load original to get county_id mapping
    original = pd.read_stata(ORIGINAL_DATA / "analysis.dta")
    county_map = original[['state', 'county', 'county_id']].drop_duplicates()

    # Merge county_id
    df = df.merge(county_map, on=['state', 'county'], how='left')

    # Check for any missing
    missing = df['county_id'].isna().sum()
    if missing > 0:
        print(f"  Warning: {missing} observations missing county_id")

    return df


def create_state_year_ids(df):
    """Create state-year identifiers."""
    print("Creating state-year identifiers...")

    df['state_year'] = df['state'] + '_' + df['year'].astype(int).astype(str)

    # Create numeric state_year_id
    state_years = df['state_year'].unique()
    state_year_map = {sy: i+1 for i, sy in enumerate(sorted(state_years))}
    df['state_year_id'] = df['state_year'].map(state_year_map)

    return df


def append_datasets(original, extension):
    """Append extension data to original data."""
    print("\nAppending datasets...")

    # Standardize columns
    common_cols = [
        'state', 'county', 'year', 'treat',
        'dem_share_gov', 'dem_share_pres', 'dem_share_sen',
        'turnout_share', 'vbm_share', 'share_votes_dem',
        'cvap', 'ballots_cast', 'period', 'post_2018'
    ]

    # Ensure both have the same columns
    for col in common_cols:
        if col not in original.columns:
            original[col] = np.nan
        if col not in extension.columns:
            extension[col] = np.nan

    # Select and order columns
    original = original[common_cols]
    extension = extension[common_cols]

    # Append
    combined = pd.concat([original, extension], ignore_index=True)

    print(f"  Original: {len(original)} obs")
    print(f"  Extension: {len(extension)} obs")
    print(f"  Combined: {len(combined)} obs")

    return combined


def create_analysis_dataset(combined):
    """Final preparation of analysis dataset."""
    print("\nFinalizing analysis dataset...")

    # Sort
    combined = combined.sort_values(['state', 'county', 'year']).reset_index(drop=True)

    # Create IDs
    combined = create_county_ids(combined)
    combined = create_state_year_ids(combined)

    # Create trend variables
    combined['year2'] = combined['year'] ** 2

    # Create presidential year indicator
    combined['pres'] = (combined['year'] % 4 == 0).astype(int)

    return combined


def create_summary_statistics(df):
    """Create summary statistics table for the extended sample."""
    print("\nCreating summary statistics...")

    # Overall stats
    stats = []

    # By period
    for period in ['original', 'extension']:
        period_df = df[df['period'] == period]

        # By state
        for state in ['CA', 'UT', 'WA']:
            state_df = period_df[period_df['state'] == state]

            if len(state_df) > 0:
                stats.append({
                    'Period': period,
                    'State': state,
                    'N_Obs': len(state_df),
                    'N_Counties': state_df['county'].nunique(),
                    'Years': f"{int(state_df['year'].min())}-{int(state_df['year'].max())}",
                    'Treat_Rate': state_df['treat'].mean(),
                    'Mean_Turnout': state_df['turnout_share'].mean(),
                    'Mean_Dem_Share_Pres': state_df['dem_share_pres'].mean(),
                    'Mean_Dem_Share_Gov': state_df['dem_share_gov'].mean()
                })

    stats_df = pd.DataFrame(stats)

    # Save
    stats_df.to_csv(OUTPUT_DIR / 'summary_stats_extended.csv', index=False)

    return stats_df


def main():
    print("=" * 60)
    print("PREPARING EXTENDED ANALYSIS DATASET")
    print("=" * 60)

    # Load data
    original = load_original_data()
    results, vca, cvap = load_extension_data()

    # Prepare extension data
    extension = prepare_extension_for_merge(results, vca, cvap)

    # Append datasets
    combined = append_datasets(original, extension)

    # Final preparation
    combined = create_analysis_dataset(combined)

    # Save combined dataset
    combined.to_csv(PROCESSED_DATA / 'full_analysis_data.csv', index=False)
    print(f"\nSaved combined dataset to {PROCESSED_DATA / 'full_analysis_data.csv'}")

    # Create summary statistics
    stats = create_summary_statistics(combined)

    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    print(stats.to_string(index=False))

    # Additional diagnostics
    print("\n" + "=" * 60)
    print("DATASET DIAGNOSTICS")
    print("=" * 60)

    print(f"\nTotal observations: {len(combined)}")
    print(f"Total counties: {combined['county_id'].nunique()}")
    print(f"Years: {sorted(combined['year'].unique())}")

    print("\nObservations by period:")
    print(combined.groupby('period').size())

    print("\nTreatment by state and period:")
    print(combined.groupby(['period', 'state'])['treat'].mean().unstack())

    print("\nMissing data:")
    for col in ['turnout_share', 'dem_share_pres', 'dem_share_gov', 'dem_share_sen', 'share_votes_dem', 'vbm_share']:
        n_miss = combined[col].isna().sum()
        pct_miss = 100 * n_miss / len(combined)
        print(f"  {col}: {n_miss} ({pct_miss:.1f}%)")


if __name__ == "__main__":
    main()
