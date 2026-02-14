"""
04_merge_data.py
Merge original analysis data (1996-2018) with extension data (2020-2024)
to create the full analysis dataset.

Key variables constructed:
- treat: VBM treatment indicator (1 when county has universal VBM)
- county_id: Unique county identifier (consistent with original)
- state_year_id: State-by-year fixed effect group (extends original numbering)
- year2: year^2 (for quadratic trends)
- dem_share_gov, dem_share_pres, dem_share_sen: Office-specific Dem vote shares
- share_votes_dem: Dem voter registration share (original only; missing for extension)
- turnout_share: Turnout as fraction of CVAP
- vbm_share: Share of ballots cast by mail (CA only; not available for extension)
"""

import pandas as pd
import numpy as np
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

###############################################################################
# 1. Load original data
###############################################################################
print("=== Loading original analysis data ===")
orig = pd.read_stata(os.path.join(ROOT, 'original', 'data', 'modified', 'analysis.dta'))
print(f"  Original: {len(orig)} rows, years {int(orig['year'].min())}-{int(orig['year'].max())}")
print(f"  Counties: {orig['county_id'].nunique()} (county_id 1-{orig['county_id'].max()})")
print(f"  State-years: {orig['state_year_id'].nunique()} (state_year_id 1-{orig['state_year_id'].max()})")

# Build county_id lookup from original data
county_lookup = orig.groupby(['state', 'county'])['county_id'].first().reset_index()
county_lookup_dict = {(r['state'], r['county']): int(r['county_id'])
                      for _, r in county_lookup.iterrows()}
max_county_id = int(orig['county_id'].max())

# Build state_year_id lookup from original
sy_lookup = orig.groupby(['state', 'year'])['state_year_id'].first().reset_index()
sy_lookup_dict = {(r['state'], int(r['year'])): int(r['state_year_id'])
                  for _, r in sy_lookup.iterrows()}
max_sy_id = int(orig['state_year_id'].max())

###############################################################################
# 2. Load extension data
###############################################################################
print("\n=== Loading extension data ===")
ext = pd.read_csv(os.path.join(ROOT, 'data', 'extension', 'extension_election_data.csv'))
print(f"  Extension: {len(ext)} rows, years {ext['year'].unique()}")

# Load VCA adoption data
vca = pd.read_csv(os.path.join(ROOT, 'data', 'extension', 'california_vbm_adoption.csv'))
vca_dict = {}
for _, r in vca.iterrows():
    if pd.notna(r['vca_first_year']) and r['vca_first_year'] != '':
        vca_dict[r['county']] = int(float(r['vca_first_year']))

###############################################################################
# 3. Construct treatment variable for extension years
###############################################################################
print("\n=== Constructing treatment variable ===")


def get_treat(state, county, year):
    """Determine VBM treatment status."""
    if state == 'WA':
        # WA: all counties VBM since 2012
        return 1
    elif state == 'UT':
        # UT: all counties VBM by 2019
        return 1
    elif state == 'CA':
        # CA: VCA adoption is staggered
        if county in vca_dict:
            return 1 if year >= vca_dict[county] else 0
        else:
            # Also need to check: Governor Newsom's EO N-64-20 made all CA
            # counties mail all-mail ballots in 2020. This means ALL CA
            # counties were de facto all-mail in 2020. However, to maintain
            # consistency with the VCA-based treatment definition (structural
            # policy change), we code treat=1 only for VCA counties.
            # Non-VCA counties in 2020 received ballots due to executive
            # order, not permanent policy adoption.
            return 0
    return 0


ext['treat'] = ext.apply(lambda r: get_treat(r['state'], r['county'], r['year']), axis=1)

# Report treatment
for year in [2020, 2022, 2024]:
    for state in ['CA', 'UT', 'WA']:
        sub = ext[(ext['year'] == year) & (ext['state'] == state)]
        nt = sub['treat'].sum()
        n = len(sub)
        if n > 0:
            print(f"  {state} {year}: {nt}/{n} treated")

###############################################################################
# 4. Assign county_id and state_year_id
###############################################################################
print("\n=== Assigning IDs ===")

# county_id: use same mapping as original
ext['county_id'] = ext.apply(
    lambda r: county_lookup_dict.get((r['state'], r['county']), np.nan), axis=1)

missing_cid = ext['county_id'].isna().sum()
if missing_cid > 0:
    missing = ext[ext['county_id'].isna()][['state', 'county']].drop_duplicates()
    print(f"  WARNING: {missing_cid} rows missing county_id:")
    print(missing.to_string())
else:
    print(f"  All {len(ext)} extension rows matched to county_id")

# state_year_id: extend from max original value
next_sy_id = max_sy_id + 1
for state in ['CA', 'UT', 'WA']:
    for year in [2020, 2022, 2024]:
        key = (state, year)
        if key not in sy_lookup_dict:
            sy_lookup_dict[key] = next_sy_id
            next_sy_id += 1

ext['state_year_id'] = ext.apply(
    lambda r: sy_lookup_dict.get((r['state'], int(r['year'])), np.nan), axis=1)

print(f"  New state_year_id range: {max_sy_id + 1} - {next_sy_id - 1}")
print(f"  Total state_year groups: {next_sy_id - 1}")

###############################################################################
# 5. Map extension election results to original variable names
###############################################################################
print("\n=== Mapping election outcomes ===")

# The extension has dem_voteshare which is the two-party Dem share for:
# - Governor races in CA (2022)
# - Presidential races (2020, 2024 for all; some states)
# - Senate races in UT/WA (2022)
# Map to dem_share_gov, dem_share_pres, dem_share_sen

ext['dem_share_gov'] = np.nan
ext['dem_share_pres'] = np.nan
ext['dem_share_sen'] = np.nan

# CA: 2020 presidential, 2022 governor, 2024 presidential
ca_mask = ext['state'] == 'CA'
ext.loc[ca_mask & (ext['year'] == 2020), 'dem_share_pres'] = \
    ext.loc[ca_mask & (ext['year'] == 2020), 'dem_voteshare'].values
ext.loc[ca_mask & (ext['year'] == 2022), 'dem_share_gov'] = \
    ext.loc[ca_mask & (ext['year'] == 2022), 'dem_voteshare'].values
ext.loc[ca_mask & (ext['year'] == 2024), 'dem_share_pres'] = \
    ext.loc[ca_mask & (ext['year'] == 2024), 'dem_voteshare'].values

# UT: 2020 presidential, 2022 senate, 2024 presidential
ut_mask = ext['state'] == 'UT'
ext.loc[ut_mask & (ext['year'] == 2020), 'dem_share_pres'] = \
    ext.loc[ut_mask & (ext['year'] == 2020), 'dem_voteshare'].values
ext.loc[ut_mask & (ext['year'] == 2022), 'dem_share_sen'] = \
    ext.loc[ut_mask & (ext['year'] == 2022), 'dem_voteshare'].values
ext.loc[ut_mask & (ext['year'] == 2024), 'dem_share_pres'] = \
    ext.loc[ut_mask & (ext['year'] == 2024), 'dem_voteshare'].values

# WA: 2020 presidential, 2022 senate, 2024 presidential
wa_mask = ext['state'] == 'WA'
ext.loc[wa_mask & (ext['year'] == 2020), 'dem_share_pres'] = \
    ext.loc[wa_mask & (ext['year'] == 2020), 'dem_voteshare'].values
ext.loc[wa_mask & (ext['year'] == 2022), 'dem_share_sen'] = \
    ext.loc[wa_mask & (ext['year'] == 2022), 'dem_voteshare'].values
ext.loc[wa_mask & (ext['year'] == 2024), 'dem_share_pres'] = \
    ext.loc[wa_mask & (ext['year'] == 2024), 'dem_voteshare'].values

# Report coverage
for col in ['dem_share_gov', 'dem_share_pres', 'dem_share_sen']:
    n = ext[col].notna().sum()
    print(f"  {col}: {n}/{len(ext)} non-null")

# Turnout
ext['turnout_share'] = ext['turnout']

# share_votes_dem: Not available for extension (voter registration data)
ext['share_votes_dem'] = np.nan

# vbm_share: Not available for extension
ext['vbm_share'] = np.nan

# CVAP
ext['cvap'] = ext['cvap_approx']

###############################################################################
# 6. Construct year2
###############################################################################
ext['year2'] = ext['year'].astype(float) ** 2

###############################################################################
# 7. Select and align columns for merge
###############################################################################
print("\n=== Preparing merge ===")

# Columns needed for analysis
merge_cols = ['county', 'state', 'year', 'county_id', 'state_year_id', 'treat',
              'year2', 'share_votes_dem', 'dem_share_gov', 'dem_share_pres',
              'dem_share_sen', 'turnout_share', 'vbm_share', 'cvap']

# Check that all columns exist in both
for c in merge_cols:
    if c not in orig.columns:
        print(f"  WARNING: {c} not in original data")
    if c not in ext.columns:
        print(f"  WARNING: {c} not in extension data")

# Select matching columns from original
orig_subset = orig[merge_cols].copy()
ext_subset = ext[merge_cols].copy()

# Ensure matching dtypes
for c in merge_cols:
    if c in ['county', 'state']:
        orig_subset[c] = orig_subset[c].astype(str)
        ext_subset[c] = ext_subset[c].astype(str)
    else:
        orig_subset[c] = pd.to_numeric(orig_subset[c], errors='coerce')
        ext_subset[c] = pd.to_numeric(ext_subset[c], errors='coerce')

# Add period indicator
orig_subset['period'] = 'original'
ext_subset['period'] = 'extension'

###############################################################################
# 8. Concatenate
###############################################################################
print("\n=== Merging datasets ===")
full = pd.concat([orig_subset, ext_subset], ignore_index=True)

# Sort
full = full.sort_values(['state', 'county', 'year']).reset_index(drop=True)

print(f"  Full dataset: {len(full)} rows")
print(f"  Original: {len(orig_subset)} rows ({int(orig_subset['year'].min())}-{int(orig_subset['year'].max())})")
print(f"  Extension: {len(ext_subset)} rows ({int(ext_subset['year'].min())}-{int(ext_subset['year'].max())})")

###############################################################################
# 9. Validation
###############################################################################
print("\n" + "=" * 70)
print("MERGED DATASET VALIDATION")
print("=" * 70)

# County counts
print("\nCounty coverage:")
for state in ['CA', 'UT', 'WA']:
    sub = full[full['state'] == state]
    n_counties = sub['county_id'].nunique()
    year_range = f"{int(sub['year'].min())}-{int(sub['year'].max())}"
    n_years = sub['year'].nunique()
    print(f"  {state}: {n_counties} counties, {n_years} years ({year_range})")

# Year coverage
print("\nObservations by year:")
year_tab = full.groupby(['year', 'period']).size().reset_index(name='n')
for _, r in year_tab.iterrows():
    print(f"  {int(r['year'])} ({r['period']}): {r['n']} obs")

# Treatment summary
print("\nTreatment (treat=1) by state-year:")
treat_tab = full.groupby(['state', 'year'])['treat'].agg(['sum', 'count']).reset_index()
treat_tab.columns = ['state', 'year', 'n_treated', 'n_total']
for _, r in treat_tab.iterrows():
    if r['n_treated'] > 0:
        print(f"  {r['state']} {int(r['year'])}: {int(r['n_treated'])}/{int(r['n_total'])} treated")

# Key variable coverage
print("\nVariable coverage (non-null):")
for col in ['share_votes_dem', 'dem_share_gov', 'dem_share_pres', 'dem_share_sen',
            'turnout_share', 'vbm_share', 'cvap']:
    orig_n = full[(full['period'] == 'original') & full[col].notna()].shape[0]
    ext_n = full[(full['period'] == 'extension') & full[col].notna()].shape[0]
    print(f"  {col}: orig={orig_n}, ext={ext_n}, total={orig_n + ext_n}")

# State_year_id uniqueness
print(f"\nTotal state_year groups: {full['state_year_id'].nunique()}")
print(f"County_id range: {int(full['county_id'].min())}-{int(full['county_id'].max())}")
print(f"State_year_id range: {int(full['state_year_id'].min())}-{int(full['state_year_id'].max())}")

# CA treatment ramp
print("\nCA VCA treatment counts over time:")
ca = full[full['state'] == 'CA']
for yr in sorted(ca['year'].unique()):
    nt = int(ca[ca['year'] == yr]['treat'].sum())
    total = len(ca[ca['year'] == yr])
    print(f"  {int(yr)}: {nt}/{total} treated")

###############################################################################
# 10. Save
###############################################################################
out_path = os.path.join(ROOT, 'data', 'processed', 'full_analysis_data.csv')
os.makedirs(os.path.dirname(out_path), exist_ok=True)
full.to_csv(out_path, index=False)
print(f"\nSaved to {out_path}")
print(f"Final shape: {full.shape}")
