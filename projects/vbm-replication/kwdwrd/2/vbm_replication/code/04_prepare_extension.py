"""
04_prepare_extension.py

Prepare the extension panel dataset for DiD analysis of VBM effects.
Mirrors the data structure from the original Thompson et al. (2020) replication.
"""

import pandas as pd
import numpy as np
import os

# =============================================================================
# LOAD DATA
# =============================================================================

print("="*70)
print("PHASE 4: EXTENSION DATA PREPARATION")
print("="*70)

# Load election results
election_data = pd.read_csv('data/extension/extension_election_results.csv')
print(f"\nLoaded election data: {len(election_data)} observations")

# Load California VCA adoption data
ca_vca = pd.read_csv('data/extension/california_vca_adoption.csv')
print(f"Loaded CA VCA adoption data: {len(ca_vca)} counties")

# Load CVAP data
cvap_data = pd.read_csv('data/extension/cvap_estimates.csv')
print(f"Loaded CVAP data: {len(cvap_data)} counties")

# =============================================================================
# CREATE TREATMENT VARIABLES
# =============================================================================

print("\n" + "-"*70)
print("Creating treatment variables...")
print("-"*70)

# For California: treatment = VCA adoption
# For Utah and Washington: always treated (100% VBM)

# Create treatment timing for all states
treatment_timing = []

# California VCA adoption
for _, row in ca_vca.iterrows():
    treatment_timing.append({
        'county': row['county'],
        'state': 'CA',
        'treat_year': row['vca_first_year'] if row['vca_first_year'] != 9999 else np.inf
    })

# Utah: 100% VBM since 2019
utah_counties = election_data[election_data['state'] == 'UT']['county'].unique()
for county in utah_counties:
    treatment_timing.append({
        'county': county,
        'state': 'UT',
        'treat_year': 2019  # Utah adopted universal VBM in 2019
    })

# Washington: 100% VBM since 2011
wa_counties = election_data[election_data['state'] == 'WA']['county'].unique()
for county in wa_counties:
    treatment_timing.append({
        'county': county,
        'state': 'WA',
        'treat_year': 2011  # Washington adopted universal VBM in 2011
    })

treatment_df = pd.DataFrame(treatment_timing)
print(f"Treatment timing created for {len(treatment_df)} counties")

# =============================================================================
# MERGE DATA
# =============================================================================

print("\n" + "-"*70)
print("Merging datasets...")
print("-"*70)

# Merge election data with treatment timing
panel = election_data.merge(treatment_df, on=['county', 'state'], how='left')
print(f"After treatment merge: {len(panel)} observations")

# Merge with CVAP data
# First, reshape CVAP to long format
cvap_long = pd.melt(
    cvap_data,
    id_vars=['county', 'state'],
    value_vars=['cvap_2020', 'cvap_2022', 'cvap_2024'],
    var_name='year_var',
    value_name='cvap'
)
cvap_long['year'] = cvap_long['year_var'].str.extract(r'(\d{4})').astype(int)
cvap_long = cvap_long.drop(columns=['year_var'])

panel = panel.merge(cvap_long, on=['county', 'state', 'year'], how='left')
print(f"After CVAP merge: {len(panel)} observations")

# Check for missing CVAP
missing_cvap = panel['cvap'].isna().sum()
if missing_cvap > 0:
    print(f"  WARNING: {missing_cvap} observations missing CVAP")

# =============================================================================
# CREATE ANALYSIS VARIABLES
# =============================================================================

print("\n" + "-"*70)
print("Creating analysis variables...")
print("-"*70)

# Treatment indicator: treat = 1 if VBM adopted by election year
panel['treat'] = (panel['year'] >= panel['treat_year']).astype(int)

# Vote share variables
panel['dem_share'] = panel['dem_votes'] / (panel['dem_votes'] + panel['rep_votes'])
panel['rep_share'] = panel['rep_votes'] / (panel['dem_votes'] + panel['rep_votes'])

# Turnout (using CVAP as denominator)
panel['turnout'] = panel['total_votes'] / panel['cvap']

# Log variables (following original paper)
panel['log_cvap'] = np.log(panel['cvap'])

# Create county identifier for fixed effects
panel['county_id'] = panel['state'] + '_' + panel['county']

# Create state-year identifier for fixed effects
panel['state_year'] = panel['state'] + '_' + panel['year'].astype(str)

# Create numeric indices for panel estimation
panel['county_idx'] = pd.Categorical(panel['county_id']).codes
panel['state_year_idx'] = pd.Categorical(panel['state_year']).codes

# Year indicators
for year in [2020, 2022, 2024]:
    panel[f'year_{year}'] = (panel['year'] == year).astype(int)

# State indicators
for state in ['CA', 'UT', 'WA']:
    panel[f'state_{state}'] = (panel['state'] == state).astype(int)

print("Variables created:")
print(f"  - treat: Treatment indicator (VBM adopted)")
print(f"  - dem_share: Democratic vote share")
print(f"  - turnout: Turnout rate (total_votes/cvap)")
print(f"  - county_id: County identifier for FE")
print(f"  - state_year: State-year identifier for FE")

# =============================================================================
# TREATMENT STATUS SUMMARY
# =============================================================================

print("\n" + "-"*70)
print("Treatment status summary...")
print("-"*70)

# Treatment by state and year
print("\nTreatment counts by state and year:")
treat_summary = panel.groupby(['state', 'year'])['treat'].agg(['sum', 'count'])
treat_summary['pct_treated'] = (treat_summary['sum'] / treat_summary['count'] * 100).round(1)
print(treat_summary)

# California-specific: variation in treatment
ca_panel = panel[panel['state'] == 'CA']
print("\nCalifornia treatment variation:")
for year in sorted(ca_panel['year'].unique()):
    year_data = ca_panel[ca_panel['year'] == year]
    n_treated = year_data['treat'].sum()
    n_total = len(year_data)
    print(f"  {year}: {n_treated}/{n_total} counties treated ({n_treated/n_total*100:.1f}%)")

# =============================================================================
# DATA QUALITY CHECKS
# =============================================================================

print("\n" + "-"*70)
print("Data quality checks...")
print("-"*70)

# Check for implausible values
print("\nTurnout statistics:")
print(f"  Min: {panel['turnout'].min():.3f}")
print(f"  Max: {panel['turnout'].max():.3f}")
print(f"  Mean: {panel['turnout'].mean():.3f}")
print(f"  Median: {panel['turnout'].median():.3f}")

# Turnout > 1 is suspicious (could indicate CVAP underestimate or data issues)
high_turnout = panel[panel['turnout'] > 1]
if len(high_turnout) > 0:
    print(f"\n  WARNING: {len(high_turnout)} observations with turnout > 100%")
    print(high_turnout[['county', 'state', 'year', 'turnout']].head(10))

print("\nDemocratic vote share statistics:")
print(f"  Min: {panel['dem_share'].min():.3f}")
print(f"  Max: {panel['dem_share'].max():.3f}")
print(f"  Mean: {panel['dem_share'].mean():.3f}")

# Check balance
print("\nPanel balance check:")
obs_per_county = panel.groupby('county_id').size()
print(f"  Observations per county: min={obs_per_county.min()}, max={obs_per_county.max()}")
if obs_per_county.min() != obs_per_county.max():
    print("  WARNING: Unbalanced panel")
else:
    print("  Panel is balanced")

# =============================================================================
# SAVE PREPARED DATA
# =============================================================================

print("\n" + "-"*70)
print("Saving prepared dataset...")
print("-"*70)

# Select columns for analysis
analysis_cols = [
    'county', 'state', 'year', 'office',
    'dem_votes', 'rep_votes', 'total_votes', 'cvap',
    'treat', 'treat_year',
    'dem_share', 'rep_share', 'turnout',
    'log_cvap',
    'county_id', 'state_year',
    'county_idx', 'state_year_idx',
    'year_2020', 'year_2022', 'year_2024',
    'state_CA', 'state_UT', 'state_WA'
]

panel_out = panel[analysis_cols].copy()
panel_out.to_csv('data/extension/extension_panel.csv', index=False)
print(f"Saved: data/extension/extension_panel.csv ({len(panel_out)} observations)")

# Also save California-only panel for focused analysis
ca_panel_out = panel_out[panel_out['state'] == 'CA'].copy()
ca_panel_out.to_csv('data/extension/california_panel.csv', index=False)
print(f"Saved: data/extension/california_panel.csv ({len(ca_panel_out)} observations)")

# =============================================================================
# SUMMARY STATISTICS
# =============================================================================

print("\n" + "="*70)
print("SUMMARY STATISTICS")
print("="*70)

print("\nPanel dimensions:")
print(f"  Total observations: {len(panel_out)}")
print(f"  Counties: {panel_out['county_id'].nunique()}")
print(f"  Years: {sorted(panel_out['year'].unique())}")
print(f"  States: {sorted(panel_out['state'].unique())}")

print("\nKey variables (mean by treatment status):")
for var in ['dem_share', 'turnout']:
    treated = panel_out[panel_out['treat'] == 1][var].mean()
    control = panel_out[panel_out['treat'] == 0][var].mean()
    print(f"  {var}:")
    print(f"    Treated: {treated:.4f}")
    print(f"    Control: {control:.4f}")
    print(f"    Difference: {treated - control:.4f}")

print("\nKey variables (mean by state):")
state_means = panel_out.groupby('state')[['dem_share', 'turnout', 'treat']].mean()
print(state_means.round(4))

print("\n" + "="*70)
print("DATA PREPARATION COMPLETE")
print("="*70)
