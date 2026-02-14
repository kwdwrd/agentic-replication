"""
04_prepare_data.py
Merge extension data with original data and prepare for analysis.

This script:
1. Loads original analysis data (1996-2018)
2. Loads extension data (2020-2024)
3. Standardizes variable names
4. Constructs analysis variables
5. Creates combined dataset
6. Generates summary statistics
"""

import pandas as pd
import numpy as np
import os

# Set paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGINAL_DATA_DIR = os.path.join(PROJECT_ROOT, 'original', 'data', 'modified')
EXTENSION_DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'extension')
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output', 'tables')

os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_original_data():
    """Load and prepare original analysis data"""
    print("Loading original analysis data...")

    # Load main analysis file
    df = pd.read_stata(os.path.join(ORIGINAL_DATA_DIR, 'analysis.dta'))

    # Keep only general elections (as in original paper)
    df = df[df['prim_or_gen'] == 'general'].copy()

    print(f"  Original data: {len(df)} observations")
    print(f"  Years: {df['year'].min()} - {df['year'].max()}")
    print(f"  States: {df['state'].unique()}")

    return df


def load_extension_data():
    """Load and combine extension data files"""
    print("\nLoading extension data...")

    # Load election results
    ca_results = pd.read_csv(os.path.join(EXTENSION_DATA_DIR, 'california_election_results.csv'))
    ut_results = pd.read_csv(os.path.join(EXTENSION_DATA_DIR, 'utah_election_results.csv'))
    wa_results = pd.read_csv(os.path.join(EXTENSION_DATA_DIR, 'washington_election_results.csv'))

    # Combine election results
    election_results = pd.concat([ca_results, ut_results, wa_results], ignore_index=True)
    print(f"  Election results: {len(election_results)} observations")

    # Load VBM/VCA adoption data
    ca_vca = pd.read_csv(os.path.join(EXTENSION_DATA_DIR, 'california_vca_adoption.csv'))
    ut_vbm = pd.read_csv(os.path.join(EXTENSION_DATA_DIR, 'utah_vbm_adoption.csv'))

    # Load CVAP data
    cvap = pd.read_csv(os.path.join(EXTENSION_DATA_DIR, 'cvap_2020.csv'))

    return election_results, ca_vca, ut_vbm, cvap


def prepare_extension_panel(election_results, ca_vca, ut_vbm, cvap):
    """
    Prepare extension data in panel format matching original data structure.

    Key variables to create:
    - state, county, year
    - treat (VBM treatment indicator)
    - dem_share (Democratic two-party vote share)
    - total_votes (ballots cast)
    - cvap (citizen voting age population)
    - turnout_share (total_votes / cvap)
    """
    print("\nPreparing extension panel data...")

    # Start with election results
    df = election_results.copy()

    # Rename columns to match original
    df = df.rename(columns={
        'dem_votes': 'ballots_cast_dem',
        'rep_votes': 'ballots_cast_rep',
        'total_votes': 'ballots_cast'
    })

    # Create dem_share (already calculated, but recalculate for consistency)
    df['dem_share'] = df['ballots_cast_dem'] / (df['ballots_cast_dem'] + df['ballots_cast_rep'])

    # Merge VBM/VCA adoption data
    # California VCA
    ca_vca_merge = ca_vca[['county', 'vca_first_year']].copy()
    ca_vca_merge = ca_vca_merge.rename(columns={'vca_first_year': 'vbm_first_year'})
    ca_vca_merge['state'] = 'CA'

    # Utah VBM
    ut_vbm_merge = ut_vbm[['county', 'vbm_first_year']].copy()
    ut_vbm_merge['state'] = 'UT'

    # Washington - all VBM since 2011
    wa_counties = df[df['state'] == 'WA']['county'].unique()
    wa_vbm_merge = pd.DataFrame({
        'county': wa_counties,
        'vbm_first_year': 2011,  # All WA counties VBM by 2011
        'state': 'WA'
    })

    # Combine VBM adoption data
    vbm_adoption = pd.concat([ca_vca_merge, ut_vbm_merge, wa_vbm_merge], ignore_index=True)

    # Merge VBM adoption with election results
    df = df.merge(vbm_adoption, on=['state', 'county'], how='left')

    # Create treatment indicator
    # treat = 1 if year >= vbm_first_year (and vbm_first_year is not null)
    df['treat'] = 0
    mask = df['vbm_first_year'].notna() & (df['year'] >= df['vbm_first_year'])
    df.loc[mask, 'treat'] = 1

    # Merge CVAP data
    df = df.merge(cvap, on=['state', 'county'], how='left')
    df = df.rename(columns={'cvap_2020': 'cvap'})

    # Calculate turnout share
    df['turnout_share'] = df['ballots_cast'] / df['cvap']

    # Create state_year variable
    df['state_year'] = df['state'] + '_' + df['year'].astype(str)

    # Create prim_or_gen (all general elections in extension)
    df['prim_or_gen'] = 'general'

    # Add period indicator
    df['period'] = 'extension'
    df['post_2018'] = 1

    print(f"  Extension panel: {len(df)} observations")
    print(f"  Treated observations: {df['treat'].sum()}")

    return df


def create_county_ids(df_orig, df_ext):
    """
    Create consistent county IDs across original and extension data.
    """
    print("\nCreating county IDs...")

    # Get unique counties from original data
    orig_counties = df_orig[['state', 'county', 'county_id']].drop_duplicates()

    # Merge county_id into extension data
    df_ext = df_ext.merge(
        orig_counties[['state', 'county', 'county_id']],
        on=['state', 'county'],
        how='left'
    )

    # Check for any missing county_ids
    missing = df_ext['county_id'].isna().sum()
    if missing > 0:
        print(f"  WARNING: {missing} observations missing county_id")
        # These would be new counties not in original data (shouldn't happen)

    return df_ext


def combine_datasets(df_orig, df_ext):
    """
    Combine original and extension datasets.
    """
    print("\nCombining datasets...")

    # Add period indicator to original
    df_orig = df_orig.copy()
    df_orig['period'] = 'original'
    df_orig['post_2018'] = 0

    # Select columns to keep (common to both datasets)
    keep_cols = [
        'state', 'county', 'county_id', 'year', 'prim_or_gen',
        'treat', 'dem_share', 'ballots_cast', 'cvap', 'turnout_share',
        'state_year', 'period', 'post_2018'
    ]

    # For original data, we need to create/rename some columns
    df_orig_subset = df_orig.copy()

    # Create state_year if not exists
    if 'state_year' not in df_orig_subset.columns:
        df_orig_subset['state_year'] = df_orig_subset['state'] + '_' + df_orig_subset['year'].astype(str)

    # Check which columns exist
    available_cols = [c for c in keep_cols if c in df_orig_subset.columns or c in df_ext.columns]

    # For dem_share in original, we need to handle the different office types
    # The original paper uses dem_share from governor/president/senate races
    # We'll use the same approach - reshape to long if needed

    # Actually, let's keep the original structure and just add the extension
    # We'll use dem_share_gov, dem_share_pres, etc. from original

    # Simpler approach: keep all original columns and add extension with matching columns
    # Create dem_share column in original from available dem_share_* columns
    if 'dem_share' not in df_orig_subset.columns:
        # Use governor races as primary (like original paper's main analysis)
        df_orig_subset['dem_share'] = df_orig_subset['dem_share_gov']

    # Get ballots_cast from original if available
    if 'ballots_cast' not in df_orig_subset.columns:
        # Use existing column names from original data
        pass  # ballots_cast should exist

    # Select and align columns
    common_cols = ['state', 'county', 'county_id', 'year', 'prim_or_gen', 'treat',
                   'turnout_share', 'state_year', 'period', 'post_2018']

    # Add dem_share columns
    for col in ['dem_share', 'dem_share_gov', 'dem_share_pres']:
        if col in df_orig_subset.columns:
            common_cols.append(col)

    # Add other useful columns
    for col in ['cvap', 'ballots_cast', 'vbm_share', 'share_votes_dem']:
        if col in df_orig_subset.columns:
            common_cols.append(col)

    # Prepare extension data with matching columns
    df_ext_subset = df_ext.copy()

    # Add missing columns to extension with NaN
    for col in common_cols:
        if col not in df_ext_subset.columns:
            df_ext_subset[col] = np.nan

    # For extension, set dem_share_gov = dem_share for governor years
    df_ext_subset['dem_share_gov'] = np.where(
        df_ext_subset['office'] == 'governor',
        df_ext_subset['dem_share'],
        np.nan
    )
    df_ext_subset['dem_share_pres'] = np.where(
        df_ext_subset['office'] == 'presidential',
        df_ext_subset['dem_share'],
        np.nan
    )

    # Get only common columns that exist in both
    final_cols = [c for c in common_cols if c in df_orig_subset.columns]

    # Add columns that exist in extension
    for col in ['dem_share_gov', 'dem_share_pres', 'dem_share', 'office']:
        if col not in final_cols and col in df_ext_subset.columns:
            final_cols.append(col)
            if col not in df_orig_subset.columns:
                df_orig_subset[col] = np.nan

    # Ensure both dataframes have the same columns
    for col in final_cols:
        if col not in df_orig_subset.columns:
            df_orig_subset[col] = np.nan
        if col not in df_ext_subset.columns:
            df_ext_subset[col] = np.nan

    # Combine
    df_combined = pd.concat([
        df_orig_subset[final_cols],
        df_ext_subset[final_cols]
    ], ignore_index=True)

    # Sort by state, county, year
    df_combined = df_combined.sort_values(['state', 'county', 'year']).reset_index(drop=True)

    # Create year^2 for quadratic trends
    df_combined['year2'] = df_combined['year'] ** 2

    # Create state_year_id
    df_combined['state_year_id'] = pd.factorize(df_combined['state_year'])[0]

    print(f"  Combined dataset: {len(df_combined)} observations")
    print(f"  Original period: {(df_combined['period'] == 'original').sum()}")
    print(f"  Extension period: {(df_combined['period'] == 'extension').sum()}")

    return df_combined


def create_summary_statistics(df):
    """
    Create summary statistics table for the extended sample.
    """
    print("\nCreating summary statistics...")

    stats = []

    # Overall statistics
    for period in ['original', 'extension', 'all']:
        if period == 'all':
            subset = df
            period_label = 'Full Sample'
        else:
            subset = df[df['period'] == period]
            period_label = f"{period.title()} ({subset['year'].min()}-{subset['year'].max()})"

        for state in ['CA', 'UT', 'WA', 'All']:
            if state == 'All':
                state_subset = subset
            else:
                state_subset = subset[subset['state'] == state]

            if len(state_subset) == 0:
                continue

            stats.append({
                'period': period_label,
                'state': state,
                'n_obs': len(state_subset),
                'n_counties': state_subset['county_id'].nunique() if 'county_id' in state_subset.columns else state_subset['county'].nunique(),
                'n_elections': state_subset['year'].nunique(),
                'pct_treated': state_subset['treat'].mean() * 100 if 'treat' in state_subset.columns else np.nan,
                'mean_turnout': state_subset['turnout_share'].mean() if 'turnout_share' in state_subset.columns else np.nan,
                'mean_dem_share': state_subset['dem_share'].mean() if 'dem_share' in state_subset.columns else np.nan,
            })

    stats_df = pd.DataFrame(stats)

    # Save
    outpath = os.path.join(OUTPUT_DIR, 'summary_stats_extended.csv')
    stats_df.to_csv(outpath, index=False)
    print(f"  Saved: {outpath}")

    return stats_df


def print_summary(df, stats_df):
    """Print summary of the combined dataset"""

    print("\n" + "="*70)
    print("COMBINED DATASET SUMMARY")
    print("="*70)

    print("\n1. OBSERVATIONS BY PERIOD AND STATE")
    print("-"*50)
    period_state = df.groupby(['period', 'state']).size().unstack(fill_value=0)
    print(period_state)

    print("\n2. TREATMENT STATUS BY PERIOD AND STATE")
    print("-"*50)
    treat_summary = df.groupby(['period', 'state'])['treat'].agg(['sum', 'mean'])
    treat_summary.columns = ['n_treated', 'pct_treated']
    treat_summary['pct_treated'] = (treat_summary['pct_treated'] * 100).round(1)
    print(treat_summary)

    print("\n3. YEARS COVERED")
    print("-"*50)
    print(f"Original period: {df[df['period']=='original']['year'].min()} - {df[df['period']=='original']['year'].max()}")
    print(f"Extension period: {df[df['period']=='extension']['year'].min()} - {df[df['period']=='extension']['year'].max()}")
    print(f"All years: {sorted(df['year'].unique())}")

    print("\n4. KEY OUTCOME VARIABLES")
    print("-"*50)
    for var in ['turnout_share', 'dem_share']:
        if var in df.columns:
            valid = df[var].notna()
            print(f"\n{var}:")
            print(f"  N: {valid.sum()}")
            print(f"  Mean: {df.loc[valid, var].mean():.4f}")
            print(f"  Std: {df.loc[valid, var].std():.4f}")

    print("\n5. SUMMARY STATISTICS TABLE")
    print("-"*50)
    print(stats_df.to_string(index=False))


def main():
    """Main function to prepare combined dataset"""

    print("="*70)
    print("PREPARING COMBINED ANALYSIS DATASET")
    print("="*70)

    # Load data
    df_orig = load_original_data()
    election_results, ca_vca, ut_vbm, cvap = load_extension_data()

    # Prepare extension panel
    df_ext = prepare_extension_panel(election_results, ca_vca, ut_vbm, cvap)

    # Create county IDs
    df_ext = create_county_ids(df_orig, df_ext)

    # Combine datasets
    df_combined = combine_datasets(df_orig, df_ext)

    # Create summary statistics
    stats_df = create_summary_statistics(df_combined)

    # Print summary
    print_summary(df_combined, stats_df)

    # Save combined dataset
    outpath = os.path.join(PROCESSED_DATA_DIR, 'full_analysis_data.csv')
    df_combined.to_csv(outpath, index=False)
    print(f"\nSaved combined dataset: {outpath}")
    print(f"  Total observations: {len(df_combined)}")

    return df_combined, stats_df


if __name__ == "__main__":
    df, stats = main()
