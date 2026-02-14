"""
04_prepare_extension.py

Prepare extension dataset by merging election results with VCA adoption data
and CVAP for California, Utah, and Washington (2020-2024).
"""

import pandas as pd
import numpy as np
import os

# Set working directory
os.chdir('/Users/kylew/git/agentic-replication/projects/vbm-replication/kwdwrd/8/vbm_replication')

print("=" * 60)
print("PHASE 4: PREPARE EXTENSION DATASET")
print("=" * 60)

# =============================================================================
# 1. Load all data sources
# =============================================================================
print("\n1. Loading data sources...")

# Presidential results 2020-2024
pres = pd.read_csv('data/extension/pres_results_2020_2024.csv')
print(f"   Presidential results: {len(pres)} rows")

# California Governor 2022
ca_gov = pd.read_csv('data/extension/ca_2022_gov_county.csv')
print(f"   CA Governor 2022: {len(ca_gov)} rows")

# Utah Senate 2022
ut_sen = pd.read_csv('data/extension/ut_2022_senate_county.csv')
print(f"   UT Senate 2022: {len(ut_sen)} rows")

# Washington Senate 2022
wa_sen = pd.read_csv('data/extension/wa_2022_senate_county.csv')
print(f"   WA Senate 2022: {len(wa_sen)} rows")

# California VCA adoption
vca = pd.read_csv('data/extension/california_vbm_adoption.csv')
print(f"   CA VCA adoption: {len(vca)} rows")

# CVAP data
cvap = pd.read_csv('data/extension/cvap_county_2016_2020.csv')
print(f"   CVAP data: {len(cvap)} rows")

# =============================================================================
# 2. Process Presidential Results
# =============================================================================
print("\n2. Processing presidential results...")

def process_pres_results(df):
    """Process presidential results to calculate Democratic vote share."""
    df = df.copy()
    df['dem_share_pres'] = df['votes_dem'] / df['total_votes']
    df['total_votes_pres'] = df['total_votes']

    # Standardize county names
    df['county'] = df['county_name'].str.replace(' County', '', regex=False).str.upper()
    df['state'] = df['state_name']

    return df[['state', 'county', 'county_fips', 'year', 'dem_share_pres', 'total_votes_pres']]

pres_clean = process_pres_results(pres)
print(f"   Processed presidential results: {len(pres_clean)} rows")

# =============================================================================
# 3. Process 2022 Results
# =============================================================================
print("\n3. Processing 2022 results...")

# California Governor 2022
def process_ca_gov(df):
    """Process CA governor results to calculate Democratic vote share."""
    # Pivot to get one row per county
    pivot = df.pivot_table(
        index='county_name',
        columns='party_simplified',
        values='votes',
        aggfunc='sum'
    ).reset_index()

    pivot['total_votes_gov'] = pivot['DEMOCRAT'] + pivot['REPUBLICAN']
    pivot['dem_share_gov'] = pivot['DEMOCRAT'] / pivot['total_votes_gov']
    pivot['county'] = pivot['county_name'].str.upper()
    pivot['state'] = 'California'
    pivot['year'] = 2022

    return pivot[['state', 'county', 'year', 'dem_share_gov', 'total_votes_gov']]

ca_gov_clean = process_ca_gov(ca_gov)
print(f"   CA Governor 2022: {len(ca_gov_clean)} rows")

# Utah Senate 2022
def process_ut_sen(df):
    """Process UT senate results (Mike Lee vs McMullin)."""
    # Filter to main candidates only
    main_candidates = df[df['candidate'].isin(['MIKE LEE', 'EVAN MCMULLIN'])]

    # Pivot to get one row per county
    pivot = main_candidates.pivot_table(
        index='county_name',
        columns='candidate',
        values='votes',
        aggfunc='sum'
    ).reset_index()

    pivot['total_votes_sen'] = pivot['MIKE LEE'] + pivot['EVAN MCMULLIN']
    # Note: McMullin was the main challenger (independent) - use as "non-Republican" share
    pivot['dem_share_sen'] = pivot['EVAN MCMULLIN'] / pivot['total_votes_sen']
    pivot['county'] = pivot['county_name'].str.upper()
    pivot['state'] = 'Utah'
    pivot['year'] = 2022

    return pivot[['state', 'county', 'year', 'dem_share_sen', 'total_votes_sen']]

ut_sen_clean = process_ut_sen(ut_sen)
print(f"   UT Senate 2022: {len(ut_sen_clean)} rows")

# Washington Senate 2022
def process_wa_sen(df):
    """Process WA senate results (Murray vs Smiley)."""
    # Filter to main candidates only
    main_candidates = df[df['candidate'].isin(['PATTY MURRAY', 'TIFFANY SMILEY'])]

    # Pivot to get one row per county
    pivot = main_candidates.pivot_table(
        index='county_name',
        columns='candidate',
        values='votes',
        aggfunc='sum'
    ).reset_index()

    pivot['total_votes_sen'] = pivot['PATTY MURRAY'] + pivot['TIFFANY SMILEY']
    pivot['dem_share_sen'] = pivot['PATTY MURRAY'] / pivot['total_votes_sen']
    pivot['county'] = pivot['county_name'].str.upper()
    pivot['state'] = 'Washington'
    pivot['year'] = 2022

    return pivot[['state', 'county', 'year', 'dem_share_sen', 'total_votes_sen']]

wa_sen_clean = process_wa_sen(wa_sen)
print(f"   WA Senate 2022: {len(wa_sen_clean)} rows")

# =============================================================================
# 4. Process VCA Adoption Data
# =============================================================================
print("\n4. Processing VCA adoption data...")

def process_vca(df):
    """Process VCA adoption to create treatment variable."""
    df = df.copy()
    df['county'] = df['county'].str.upper()
    df['state'] = 'California'

    # Create binary treatment variable (adopted VCA)
    df['vca_adopted'] = (df['vca_first_year'] < 9999).astype(int)
    df['vca_year'] = df['vca_first_year'].replace(9999, np.nan)

    return df[['state', 'county', 'vca_adopted', 'vca_year', 'vca_first_year']]

vca_clean = process_vca(vca)
print(f"   VCA adoption: {len(vca_clean)} rows")

# =============================================================================
# 5. Process CVAP Data
# =============================================================================
print("\n5. Processing CVAP data...")

def process_cvap(df):
    """Process CVAP data for turnout calculations."""
    df = df.copy()
    df['county'] = df['county'].str.upper()

    return df[['state', 'county', 'fips', 'cvap_2020']]

cvap_clean = process_cvap(cvap)
print(f"   CVAP: {len(cvap_clean)} rows")

# =============================================================================
# 6. Create Panel Dataset
# =============================================================================
print("\n6. Creating panel dataset...")

# Create base panel with all county-year combinations
years = [2020, 2022, 2024]
states = ['California', 'Utah', 'Washington']

# Start with presidential results as base
panel = pres_clean.copy()

# Add 2022 rows for each state
for state in states:
    state_counties = panel[panel['state'] == state]['county'].unique()
    for county in state_counties:
        fips = panel[(panel['state'] == state) & (panel['county'] == county)]['county_fips'].iloc[0]
        new_row = pd.DataFrame({
            'state': [state],
            'county': [county],
            'county_fips': [fips],
            'year': [2022],
            'dem_share_pres': [np.nan],
            'total_votes_pres': [np.nan]
        })
        panel = pd.concat([panel, new_row], ignore_index=True)

panel = panel.sort_values(['state', 'county', 'year']).reset_index(drop=True)
print(f"   Base panel: {len(panel)} rows")

# Merge CA governor results
panel = panel.merge(
    ca_gov_clean,
    on=['state', 'county', 'year'],
    how='left'
)

# Merge UT senate results
panel = panel.merge(
    ut_sen_clean[['state', 'county', 'year', 'dem_share_sen', 'total_votes_sen']],
    on=['state', 'county', 'year'],
    how='left',
    suffixes=('', '_ut')
)

# Merge WA senate results
wa_sen_for_merge = wa_sen_clean[['state', 'county', 'year', 'dem_share_sen', 'total_votes_sen']].copy()
wa_sen_for_merge.columns = ['state', 'county', 'year', 'dem_share_sen_wa', 'total_votes_sen_wa']
panel = panel.merge(
    wa_sen_for_merge,
    on=['state', 'county', 'year'],
    how='left'
)

# Combine senate results
panel['dem_share_sen'] = panel['dem_share_sen'].fillna(panel['dem_share_sen_wa'])
panel['total_votes_sen'] = panel['total_votes_sen'].fillna(panel['total_votes_sen_wa'])
panel = panel.drop(columns=['dem_share_sen_wa', 'total_votes_sen_wa'])

# Merge VCA adoption data (for California only)
panel = panel.merge(
    vca_clean,
    on=['state', 'county'],
    how='left'
)

# For Utah and Washington, all counties are all-VBM
panel.loc[panel['state'] == 'Utah', 'vca_adopted'] = 1
panel.loc[panel['state'] == 'Utah', 'vca_year'] = 2012  # Utah went all-VBM in 2012
panel.loc[panel['state'] == 'Washington', 'vca_adopted'] = 1
panel.loc[panel['state'] == 'Washington', 'vca_year'] = 2011  # WA went all-VBM in 2011

# Merge CVAP data
panel = panel.merge(
    cvap_clean,
    on=['state', 'county'],
    how='left'
)

# =============================================================================
# 7. Create Treatment Variables
# =============================================================================
print("\n7. Creating treatment variables...")

# Treatment indicator: county has adopted VBM/VCA by election year
def calc_treatment(row):
    """Calculate whether county was treated (VBM) by given election year."""
    if pd.isna(row['vca_year']):
        return 0
    return 1 if row['year'] >= row['vca_year'] else 0

panel['treat'] = panel.apply(calc_treatment, axis=1)

# For CA, also create "newly treated" indicator for extension analysis
panel['treat_new_ca'] = 0
ca_mask = panel['state'] == 'California'
panel.loc[ca_mask, 'treat_new_ca'] = panel.loc[ca_mask].apply(
    lambda x: 1 if (pd.notna(x['vca_year']) and x['year'] >= x['vca_year'] and x['vca_year'] >= 2018) else 0,
    axis=1
)

# =============================================================================
# 8. Calculate Turnout
# =============================================================================
print("\n8. Calculating turnout...")

# Presidential turnout
panel['turnout_pres'] = panel['total_votes_pres'] / panel['cvap_2020']

# Governor turnout (CA only)
panel['turnout_gov'] = panel['total_votes_gov'] / panel['cvap_2020']

# Senate turnout
panel['turnout_sen'] = panel['total_votes_sen'] / panel['cvap_2020']

# =============================================================================
# 9. Create State-Year Fixed Effects
# =============================================================================
print("\n9. Creating fixed effects...")

panel['state_year'] = panel['state'] + '_' + panel['year'].astype(str)
panel['county_id'] = panel['state'] + '_' + panel['county']

# =============================================================================
# 10. Summary Statistics
# =============================================================================
print("\n10. Summary Statistics")
print("=" * 60)

print(f"\nPanel dimensions: {len(panel)} rows x {len(panel.columns)} columns")
print(f"\nObservations by state-year:")
print(panel.groupby(['state', 'year']).size().unstack(fill_value=0))

print(f"\nTreatment status by state-year:")
print(panel.groupby(['state', 'year'])['treat'].mean().unstack())

print(f"\nNew CA treatment by year:")
print(panel[panel['state'] == 'California'].groupby('year')['treat_new_ca'].sum())

print(f"\nKey outcome variables (means):")
print(f"   dem_share_pres: {panel['dem_share_pres'].mean():.4f}")
print(f"   dem_share_gov:  {panel['dem_share_gov'].mean():.4f}")
print(f"   dem_share_sen:  {panel['dem_share_sen'].mean():.4f}")
print(f"   turnout_pres:   {panel['turnout_pres'].mean():.4f}")

# =============================================================================
# 11. Save Dataset
# =============================================================================
print("\n11. Saving dataset...")

# Save full panel
panel.to_csv('data/extension/extension_panel.csv', index=False)
print(f"   Saved: data/extension/extension_panel.csv")

# Save California-only panel for DiD analysis
ca_panel = panel[panel['state'] == 'California'].copy()
ca_panel.to_csv('data/extension/extension_panel_ca.csv', index=False)
print(f"   Saved: data/extension/extension_panel_ca.csv ({len(ca_panel)} rows)")

# Create analysis-ready dataset with complete cases
analysis_vars = ['county_id', 'state', 'county', 'year', 'state_year',
                 'treat', 'treat_new_ca', 'dem_share_pres', 'turnout_pres', 'cvap_2020']
analysis = panel.dropna(subset=['dem_share_pres', 'turnout_pres'])
analysis.to_csv('data/extension/extension_analysis.csv', index=False)
print(f"   Saved: data/extension/extension_analysis.csv ({len(analysis)} rows)")

print("\n" + "=" * 60)
print("PHASE 4 COMPLETE")
print("=" * 60)

# Display final panel structure
print("\nFinal panel columns:")
for col in panel.columns:
    non_null = panel[col].notna().sum()
    print(f"   {col}: {non_null}/{len(panel)} non-null")
