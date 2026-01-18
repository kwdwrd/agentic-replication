#!/usr/bin/env python3
"""
04_merge_extension.py
Phase 4: Merge and prepare extension dataset

This script merges the extension data (2020-2024) with the original Thompson et al. (2020)
analysis dataset, creating a combined panel for extended analysis.

Key tasks:
1. Load original analysis.dta (1996-2018)
2. Load extension data (2020, 2022, 2024)
3. Create consistent identifiers (county_id, state_year_id)
4. Compute outcome variables for extension years
5. Apply treatment variable for California VCA expansion
6. Output combined dataset
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Set paths
PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "data"
ORIGINAL_DIR = PROJECT_DIR / "original" / "data" / "modified"
EXTENSION_DIR = DATA_DIR / "extension"
OUTPUT_DIR = DATA_DIR / "combined"

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_original_data():
    """Load and prepare original analysis dataset."""
    print("Loading original analysis.dta...")
    df = pd.read_stata(ORIGINAL_DIR / "analysis.dta")

    print(f"  Original shape: {df.shape}")
    print(f"  Years: {sorted(df['year'].unique())}")
    print(f"  Counties: {df['county'].nunique()}")

    # Keep key variables for extension analysis
    key_vars = [
        'state', 'county', 'year', 'prim_or_gen', 'treat',
        'vca18', 'vca20', 'vca_eligible18', 'vca_eligible20',
        'all_mail2006', 'ut_all_mail_year', 'switch_year',
        'registered', 'ballots_cast', 'eligible', 'cvap',
        'vbm_share', 'turnout_share', 'turnout_of_reg',
        'dem_share_gov', 'dem_share_pres', 'dem_share_sen',
        'share_votes_dem', 'share_votes_rep',
        'county_id', 'state_year_id', 'pres', 'prim'
    ]

    # Keep only variables that exist
    existing_vars = [v for v in key_vars if v in df.columns]
    df = df[existing_vars].copy()

    return df


def load_extension_data():
    """Load extension data for 2020-2024."""
    print("\nLoading extension data...")

    # Load 2020 presidential results
    pres_2020 = pd.read_csv(EXTENSION_DIR / "three_states_2020_pres.csv")
    print(f"  2020 presidential: {len(pres_2020)} counties")

    # Load treatment extension
    treatment = pd.read_csv(EXTENSION_DIR / "treatment_extension.csv")
    print(f"  Treatment extension: {len(treatment)} county-years")

    # Load VCA adoption data
    vca = pd.read_csv(EXTENSION_DIR / "california_vca_adoption.csv")
    print(f"  VCA counties: {len(vca)}")

    return pres_2020, treatment, vca


def create_extension_panel(pres_2020, treatment, vca, original_df):
    """Create extension panel dataset for 2020, 2022, 2024."""
    print("\nCreating extension panel...")

    # Get unique counties from original data
    counties = original_df[['state', 'county']].drop_duplicates()
    print(f"  Counties to extend: {len(counties)}")

    # Create panel structure for extension years
    extension_years = [2020, 2022, 2024]

    # Cross product: counties x years
    panels = []
    for year in extension_years:
        panel = counties.copy()
        panel['year'] = year
        panels.append(panel)

    extension_df = pd.concat(panels, ignore_index=True)
    print(f"  Extension panel shape: {extension_df.shape}")

    # Merge treatment indicator
    extension_df = extension_df.merge(
        treatment[['state', 'county', 'year', 'treat', 'vca_first_year']],
        on=['state', 'county', 'year'],
        how='left'
    )

    # Merge 2020 presidential results
    pres_2020_subset = pres_2020[['state', 'county', 'dem_votes', 'rep_votes', 'total_votes']].copy()
    pres_2020_subset['year'] = 2020

    extension_df = extension_df.merge(
        pres_2020_subset,
        on=['state', 'county', 'year'],
        how='left'
    )

    # Calculate Democratic share for president (2020)
    extension_df['dem_share_pres'] = np.where(
        extension_df['year'] == 2020,
        extension_df['dem_votes'] / (extension_df['dem_votes'] + extension_df['rep_votes']),
        np.nan
    )

    # Set pres indicator
    extension_df['pres'] = extension_df['year'].isin([2020, 2024]).astype(int)
    extension_df['prim'] = 0  # All extension years are general elections
    extension_df['prim_or_gen'] = 'gen'

    # Clean up
    extension_df = extension_df.drop(columns=['dem_votes', 'rep_votes', 'total_votes'], errors='ignore')

    return extension_df


def assign_identifiers(df, original_df):
    """Assign county_id and state_year_id consistent with original data."""
    print("\nAssigning identifiers...")

    # Get existing county_id mapping from original data
    county_map = original_df[['state', 'county', 'county_id']].drop_duplicates()
    print(f"  County IDs from original: {len(county_map)}")

    # Get max state_year_id from original
    max_state_year_id = original_df['state_year_id'].max()
    print(f"  Max original state_year_id: {max_state_year_id}")

    # Create new state_year_id for extension years
    extension_state_years = df[['state', 'year']].drop_duplicates().sort_values(['state', 'year'])
    extension_state_years['state_year_id'] = range(
        int(max_state_year_id) + 1,
        int(max_state_year_id) + 1 + len(extension_state_years)
    )

    # Merge identifiers
    df = df.merge(county_map, on=['state', 'county'], how='left')
    df = df.merge(extension_state_years, on=['state', 'year'], how='left')

    return df


def combine_datasets(original_df, extension_df):
    """Combine original and extension datasets."""
    print("\nCombining datasets...")

    # Get common columns
    common_cols = list(set(original_df.columns) & set(extension_df.columns))
    print(f"  Common columns: {len(common_cols)}")

    # Ensure extension_df has all columns from original (fill with NaN if missing)
    for col in original_df.columns:
        if col not in extension_df.columns:
            extension_df[col] = np.nan

    # Reorder columns to match
    extension_df = extension_df[original_df.columns]

    # Combine
    combined = pd.concat([original_df, extension_df], ignore_index=True)

    # Sort by county and year
    combined = combined.sort_values(['state', 'county', 'year']).reset_index(drop=True)

    print(f"  Combined shape: {combined.shape}")
    print(f"  Year range: {combined['year'].min()} - {combined['year'].max()}")

    return combined


def validate_combined_data(combined_df):
    """Validate the combined dataset."""
    print("\n" + "="*60)
    print("VALIDATION CHECKS")
    print("="*60)

    # Check year coverage
    years = sorted(combined_df['year'].unique())
    print(f"\n1. Year coverage: {years}")

    # Check county counts by state
    print("\n2. Counties by state:")
    county_counts = combined_df.groupby('state')['county'].nunique()
    for state, count in county_counts.items():
        print(f"   {state}: {count} counties")

    # Check treatment variable
    print("\n3. Treatment by year and state:")
    treat_summary = combined_df.groupby(['year', 'state'])['treat'].mean()
    print(treat_summary.unstack().round(3))

    # Check outcome availability
    print("\n4. Outcome variable coverage:")
    outcomes = ['dem_share_pres', 'dem_share_gov', 'turnout_share', 'share_votes_dem']
    for outcome in outcomes:
        if outcome in combined_df.columns:
            coverage = combined_df.groupby('year')[outcome].apply(lambda x: x.notna().sum())
            print(f"\n   {outcome}:")
            print(f"   {coverage.to_dict()}")

    # Check for identifier consistency
    print("\n5. Identifier checks:")
    print(f"   Unique county_id: {combined_df['county_id'].nunique()}")
    print(f"   Unique state_year_id: {combined_df['state_year_id'].nunique()}")

    # Check for duplicates
    dup_count = combined_df.duplicated(subset=['county_id', 'year', 'pres']).sum()
    print(f"   Duplicate county-year-pres combinations: {dup_count}")

    return True


def create_analysis_ready_subset(combined_df):
    """Create analysis-ready subset focusing on presidential years."""
    print("\nCreating analysis-ready subset...")

    # Filter to presidential years only (like original analysis)
    pres_years = [2000, 2004, 2008, 2012, 2016, 2020, 2024]
    pres_df = combined_df[combined_df['year'].isin(pres_years)].copy()

    print(f"  Presidential years subset: {pres_df.shape}")

    # For extension analysis, focus on California where VCA varies
    ca_df = pres_df[pres_df['state'] == 'CA'].copy()
    print(f"  California only: {ca_df.shape}")

    return pres_df, ca_df


def main():
    """Main execution."""
    print("="*60)
    print("PHASE 4: MERGE AND PREPARE EXTENSION DATASET")
    print("="*60)

    # Load data
    original_df = load_original_data()
    pres_2020, treatment, vca = load_extension_data()

    # Create extension panel
    extension_df = create_extension_panel(pres_2020, treatment, vca, original_df)

    # Assign identifiers
    extension_df = assign_identifiers(extension_df, original_df)

    # Combine datasets
    combined_df = combine_datasets(original_df, extension_df)

    # Validate
    validate_combined_data(combined_df)

    # Create analysis subsets
    pres_df, ca_df = create_analysis_ready_subset(combined_df)

    # Save outputs
    print("\nSaving outputs...")

    combined_df.to_csv(OUTPUT_DIR / "analysis_extended.csv", index=False)
    print(f"  Saved: analysis_extended.csv ({combined_df.shape})")

    pres_df.to_csv(OUTPUT_DIR / "analysis_extended_pres.csv", index=False)
    print(f"  Saved: analysis_extended_pres.csv ({pres_df.shape})")

    ca_df.to_csv(OUTPUT_DIR / "analysis_extended_ca_pres.csv", index=False)
    print(f"  Saved: analysis_extended_ca_pres.csv ({ca_df.shape})")

    # Also save as Stata format for cross-validation
    try:
        combined_df.to_stata(OUTPUT_DIR / "analysis_extended.dta", write_index=False)
        print(f"  Saved: analysis_extended.dta")
    except Exception as e:
        print(f"  Note: Could not save Stata format ({e})")

    print("\n" + "="*60)
    print("PHASE 4 COMPLETE")
    print("="*60)

    return combined_df, pres_df, ca_df


if __name__ == "__main__":
    main()
