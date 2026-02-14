"""
Build extension dataset for 2020-2024 elections
Merges with original data structure for combined analysis
"""
import pandas as pd
import numpy as np

# Load original data to get county IDs and structure
original = pd.read_stata('../original/data/modified/analysis.dta')

# Get unique counties from original data
counties_orig = original.groupby(['state', 'county']).agg({
    'county_id': 'first'
}).reset_index()

print(f"Original data: {len(counties_orig)} unique counties")
print(f"  CA: {len(counties_orig[counties_orig['state']=='CA'])}")
print(f"  UT: {len(counties_orig[counties_orig['state']=='UT'])}")
print(f"  WA: {len(counties_orig[counties_orig['state']=='WA'])}")

# ============================================================
# LOAD EXTENSION DATA
# ============================================================

data_dir = '../data/extension'

# California VCA adoption
ca_vca = pd.read_csv(f'{data_dir}/california_vbm_adoption.csv')
ca_vca_counties = set(ca_vca['county'].values)

# California election results
ca_2020_pres = pd.read_csv(f'{data_dir}/california_results_2020_pres.csv')
ca_2022_gov = pd.read_csv(f'{data_dir}/california_results_2022_gov.csv')
ca_2024_pres = pd.read_csv(f'{data_dir}/california_results_2024_pres.csv')

# Utah election results
ut_2020_pres = pd.read_csv(f'{data_dir}/utah_results_2020_pres.csv')
ut_2024_pres = pd.read_csv(f'{data_dir}/utah_results_2024_pres.csv')
ut_2024_gov = pd.read_csv(f'{data_dir}/utah_results_2024_gov.csv')

# Washington election results
wa_2020_pres = pd.read_csv(f'{data_dir}/washington_results_2020_pres.csv')
wa_2020_gov = pd.read_csv(f'{data_dir}/washington_results_2020_gov.csv')
wa_2022_sen = pd.read_csv(f'{data_dir}/washington_results_2022_sen.csv')
wa_2024_pres = pd.read_csv(f'{data_dir}/washington_results_2024_pres.csv')
wa_2024_gov = pd.read_csv(f'{data_dir}/washington_results_2024_gov.csv')

# CVAP data (use 2020-2024 estimates for extension period)
ca_cvap = pd.read_csv(f'{data_dir}/california_cvap_2020_2024.csv')
ut_cvap = pd.read_csv(f'{data_dir}/utah_cvap_2020_2024.csv')
wa_cvap = pd.read_csv(f'{data_dir}/washington_cvap_2020_2024.csv')

# ============================================================
# BUILD EXTENSION ROWS
# ============================================================

def compute_dem_share(dem_votes, rep_votes):
    """Compute Democratic two-party vote share."""
    total = dem_votes + rep_votes
    return np.where(total > 0, dem_votes / total, np.nan)

def get_vca_treatment(county, year, vca_df):
    """Determine if county is treated (VCA) in given year."""
    match = vca_df[vca_df['county'] == county]
    if len(match) == 0:
        return 0  # Not a VCA county
    first_year = match['vca_first_year'].values[0]
    return 1 if year >= first_year else 0

extension_rows = []

# ------------------------------------------------------------
# CALIFORNIA 2020, 2022, 2024
# ------------------------------------------------------------

for county in ca_2020_pres['county'].unique():
    county_id = counties_orig[(counties_orig['state']=='CA') &
                               (counties_orig['county']==county)]['county_id'].values
    if len(county_id) == 0:
        print(f"Warning: CA county '{county}' not found in original data")
        continue
    county_id = county_id[0]

    cvap_row = ca_cvap[ca_cvap['county'] == county]
    cvap = cvap_row['cvap'].values[0] if len(cvap_row) > 0 else np.nan

    # 2020 Presidential
    pres_2020 = ca_2020_pres[ca_2020_pres['county'] == county]
    if len(pres_2020) > 0:
        row = {
            'state': 'CA',
            'county': county,
            'county_id': county_id,
            'year': 2020,
            'prim_or_gen': 'general',
            'pres': 1,
            'treat': get_vca_treatment(county, 2020, ca_vca),
            'cvap': cvap,
            'ballots_cast': pres_2020['total_votes'].values[0],
            'ballots_cast_dem_pres': pres_2020['dem_votes'].values[0],
            'ballots_cast_rep_pres': pres_2020['rep_votes'].values[0],
            'dem_share_pres': compute_dem_share(
                pres_2020['dem_votes'].values[0],
                pres_2020['rep_votes'].values[0]
            ),
            'dem_share_gov': np.nan,
            'dem_share_sen': np.nan,
        }
        extension_rows.append(row)

    # 2022 Governor
    gov_2022 = ca_2022_gov[ca_2022_gov['county'] == county]
    if len(gov_2022) > 0:
        row = {
            'state': 'CA',
            'county': county,
            'county_id': county_id,
            'year': 2022,
            'prim_or_gen': 'general',
            'pres': 0,
            'treat': get_vca_treatment(county, 2022, ca_vca),
            'cvap': cvap,
            'ballots_cast': gov_2022['total_votes'].values[0],
            'ballots_cast_dem_gov': gov_2022['dem_votes'].values[0],
            'ballots_cast_rep_gov': gov_2022['rep_votes'].values[0],
            'dem_share_pres': np.nan,
            'dem_share_gov': compute_dem_share(
                gov_2022['dem_votes'].values[0],
                gov_2022['rep_votes'].values[0]
            ),
            'dem_share_sen': np.nan,
        }
        extension_rows.append(row)

    # 2024 Presidential
    pres_2024 = ca_2024_pres[ca_2024_pres['county'] == county]
    if len(pres_2024) > 0:
        row = {
            'state': 'CA',
            'county': county,
            'county_id': county_id,
            'year': 2024,
            'prim_or_gen': 'general',
            'pres': 1,
            'treat': get_vca_treatment(county, 2024, ca_vca),
            'cvap': cvap,
            'ballots_cast': pres_2024['total_votes'].values[0],
            'ballots_cast_dem_pres': pres_2024['dem_votes'].values[0],
            'ballots_cast_rep_pres': pres_2024['rep_votes'].values[0],
            'dem_share_pres': compute_dem_share(
                pres_2024['dem_votes'].values[0],
                pres_2024['rep_votes'].values[0]
            ),
            'dem_share_gov': np.nan,
            'dem_share_sen': np.nan,
        }
        extension_rows.append(row)

# ------------------------------------------------------------
# UTAH 2020, 2024
# (Skip 2022 - no Democratic candidate)
# Utah has universal VBM since 2019, so treat=1 for all
# ------------------------------------------------------------

for county in ut_2020_pres['county'].unique():
    county_id = counties_orig[(counties_orig['state']=='UT') &
                               (counties_orig['county']==county)]['county_id'].values
    if len(county_id) == 0:
        print(f"Warning: UT county '{county}' not found in original data")
        continue
    county_id = county_id[0]

    cvap_row = ut_cvap[ut_cvap['county'] == county]
    cvap = cvap_row['cvap'].values[0] if len(cvap_row) > 0 else np.nan

    # 2020 Presidential
    pres_2020 = ut_2020_pres[ut_2020_pres['county'] == county]
    if len(pres_2020) > 0:
        row = {
            'state': 'UT',
            'county': county,
            'county_id': county_id,
            'year': 2020,
            'prim_or_gen': 'general',
            'pres': 1,
            'treat': 1,  # Utah has universal VBM since 2019
            'cvap': cvap,
            'ballots_cast': pres_2020['total_votes'].values[0],
            'ballots_cast_dem_pres': pres_2020['dem_votes'].values[0],
            'ballots_cast_rep_pres': pres_2020['rep_votes'].values[0],
            'dem_share_pres': compute_dem_share(
                pres_2020['dem_votes'].values[0],
                pres_2020['rep_votes'].values[0]
            ),
            'dem_share_gov': np.nan,
            'dem_share_sen': np.nan,
        }
        extension_rows.append(row)

    # 2024 Presidential
    pres_2024 = ut_2024_pres[ut_2024_pres['county'] == county]
    gov_2024 = ut_2024_gov[ut_2024_gov['county'] == county]
    if len(pres_2024) > 0:
        dem_share_gov = np.nan
        if len(gov_2024) > 0:
            dem_share_gov = compute_dem_share(
                gov_2024['dem_votes'].values[0],
                gov_2024['rep_votes'].values[0]
            )
        row = {
            'state': 'UT',
            'county': county,
            'county_id': county_id,
            'year': 2024,
            'prim_or_gen': 'general',
            'pres': 1,
            'treat': 1,
            'cvap': cvap,
            'ballots_cast': pres_2024['total_votes'].values[0],
            'ballots_cast_dem_pres': pres_2024['dem_votes'].values[0],
            'ballots_cast_rep_pres': pres_2024['rep_votes'].values[0],
            'dem_share_pres': compute_dem_share(
                pres_2024['dem_votes'].values[0],
                pres_2024['rep_votes'].values[0]
            ),
            'dem_share_gov': dem_share_gov,
            'dem_share_sen': np.nan,
        }
        extension_rows.append(row)

# ------------------------------------------------------------
# WASHINGTON 2020, 2022, 2024
# Washington has universal VBM since 2011, so treat=1 for all
# ------------------------------------------------------------

for county in wa_2020_pres['county'].unique():
    county_id = counties_orig[(counties_orig['state']=='WA') &
                               (counties_orig['county']==county)]['county_id'].values
    if len(county_id) == 0:
        print(f"Warning: WA county '{county}' not found in original data")
        continue
    county_id = county_id[0]

    cvap_row = wa_cvap[wa_cvap['county'] == county]
    cvap = cvap_row['cvap'].values[0] if len(cvap_row) > 0 else np.nan

    # 2020 Presidential & Governor
    pres_2020 = wa_2020_pres[wa_2020_pres['county'] == county]
    gov_2020 = wa_2020_gov[wa_2020_gov['county'] == county]
    if len(pres_2020) > 0:
        dem_share_gov = np.nan
        if len(gov_2020) > 0:
            dem_share_gov = compute_dem_share(
                gov_2020['dem_votes'].values[0],
                gov_2020['rep_votes'].values[0]
            )
        row = {
            'state': 'WA',
            'county': county,
            'county_id': county_id,
            'year': 2020,
            'prim_or_gen': 'general',
            'pres': 1,
            'treat': 1,
            'cvap': cvap,
            'ballots_cast': pres_2020['total_votes'].values[0],
            'ballots_cast_dem_pres': pres_2020['dem_votes'].values[0],
            'ballots_cast_rep_pres': pres_2020['rep_votes'].values[0],
            'dem_share_pres': compute_dem_share(
                pres_2020['dem_votes'].values[0],
                pres_2020['rep_votes'].values[0]
            ),
            'dem_share_gov': dem_share_gov,
            'dem_share_sen': np.nan,
        }
        extension_rows.append(row)

    # 2022 Senate
    sen_2022 = wa_2022_sen[wa_2022_sen['county'] == county]
    if len(sen_2022) > 0:
        row = {
            'state': 'WA',
            'county': county,
            'county_id': county_id,
            'year': 2022,
            'prim_or_gen': 'general',
            'pres': 0,
            'treat': 1,
            'cvap': cvap,
            'ballots_cast': sen_2022['total_votes'].values[0],
            'ballots_cast_dem_pres': np.nan,
            'ballots_cast_rep_pres': np.nan,
            'dem_share_pres': np.nan,
            'dem_share_gov': np.nan,
            'dem_share_sen': compute_dem_share(
                sen_2022['dem_votes'].values[0],
                sen_2022['rep_votes'].values[0]
            ),
        }
        extension_rows.append(row)

    # 2024 Presidential & Governor
    pres_2024 = wa_2024_pres[wa_2024_pres['county'] == county]
    gov_2024 = wa_2024_gov[wa_2024_gov['county'] == county]
    if len(pres_2024) > 0:
        dem_share_gov = np.nan
        if len(gov_2024) > 0:
            dem_share_gov = compute_dem_share(
                gov_2024['dem_votes'].values[0],
                gov_2024['rep_votes'].values[0]
            )
        row = {
            'state': 'WA',
            'county': county,
            'county_id': county_id,
            'year': 2024,
            'prim_or_gen': 'general',
            'pres': 1,
            'treat': 1,
            'cvap': cvap,
            'ballots_cast': pres_2024['total_votes'].values[0],
            'ballots_cast_dem_pres': pres_2024['dem_votes'].values[0],
            'ballots_cast_rep_pres': pres_2024['rep_votes'].values[0],
            'dem_share_pres': compute_dem_share(
                pres_2024['dem_votes'].values[0],
                pres_2024['rep_votes'].values[0]
            ),
            'dem_share_gov': dem_share_gov,
            'dem_share_sen': np.nan,
        }
        extension_rows.append(row)

# ============================================================
# CREATE EXTENSION DATAFRAME
# ============================================================

extension_df = pd.DataFrame(extension_rows)

# Compute turnout share
extension_df['turnout_share'] = extension_df['ballots_cast'] / extension_df['cvap']

# Add year squared for trend specifications
extension_df['year2'] = extension_df['year'] ** 2

# Create state-year identifier
extension_df['state_year'] = extension_df['state'] + '_' + extension_df['year'].astype(str)

print("\n" + "=" * 60)
print("EXTENSION DATASET SUMMARY")
print("=" * 60)

print(f"\nTotal rows: {len(extension_df)}")
print(f"\nRows by state and year:")
print(extension_df.groupby(['state', 'year']).size().unstack(fill_value=0))

print(f"\nTreatment status by state and year:")
print(extension_df.groupby(['state', 'year'])['treat'].mean().unstack())

print(f"\nMean Democratic presidential share by state:")
pres_only = extension_df[extension_df['pres']==1]
print(pres_only.groupby('state')['dem_share_pres'].mean())

print(f"\nMean turnout share by state and year:")
print(extension_df.groupby(['state', 'year'])['turnout_share'].mean().unstack())

# Save extension dataset
extension_df.to_csv('../data/extension/extension_analysis.csv', index=False)
print(f"\nSaved extension dataset to data/extension/extension_analysis.csv")

# ============================================================
# CREATE COMBINED DATASET (ORIGINAL + EXTENSION)
# ============================================================

# Select columns that exist in both datasets
common_cols = ['state', 'county', 'county_id', 'year', 'prim_or_gen', 'pres',
               'treat', 'cvap', 'ballots_cast', 'dem_share_pres', 'dem_share_gov',
               'dem_share_sen', 'turnout_share', 'year2']

# Prepare original data
original_subset = original[common_cols].copy()

# Prepare extension data
extension_subset = extension_df[common_cols].copy()

# Combine
combined = pd.concat([original_subset, extension_subset], ignore_index=True)
combined = combined.sort_values(['state', 'county', 'year']).reset_index(drop=True)

# Create new state-year IDs
combined['state_year'] = combined['state'] + '_' + combined['year'].astype(str)
state_years = combined['state_year'].unique()
state_year_map = {sy: i for i, sy in enumerate(sorted(state_years))}
combined['state_year_id'] = combined['state_year'].map(state_year_map)

print("\n" + "=" * 60)
print("COMBINED DATASET SUMMARY")
print("=" * 60)

print(f"\nTotal rows: {len(combined)}")
print(f"\nRows by year:")
print(combined.groupby('year').size())

print(f"\nTreatment status over time:")
print(combined.groupby(['state', 'year'])['treat'].mean().unstack())

# Save combined dataset
combined.to_csv('../data/combined_analysis.csv', index=False)
print(f"\nSaved combined dataset to data/combined_analysis.csv")

# Also save a California-only dataset for primary analysis
ca_combined = combined[combined['state'] == 'CA'].copy()
ca_combined.to_csv('../data/california_analysis.csv', index=False)
print(f"Saved California-only dataset to data/california_analysis.csv ({len(ca_combined)} rows)")
