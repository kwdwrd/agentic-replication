"""
03_collect_extension.py
Extension Data Collection for VBM Replication

This script documents the data collection process for extending
Thompson et al. (2020) through 2024.

Data Sources:
- 2020 Presidential: GitHub (tonmcg/US_County_Level_Election_Results_08-20)
- 2022 Gubernatorial: California/Utah/Washington Secretary of State
- 2024 Presidential: State Secretary of State offices
- CVAP: U.S. Census Bureau

Note: Due to access restrictions, some data is compiled from multiple sources
and may require manual verification.
"""

import pandas as pd
import numpy as np
import os

# Paths
DATA_DIR = 'data'
EXTENSION_DIR = 'data/extension'
RAW_DIR = 'data/raw'

os.makedirs(EXTENSION_DIR, exist_ok=True)

# =============================================================================
# CALIFORNIA VCA ADOPTION
# =============================================================================

def create_vca_adoption_data():
    """
    Create California VCA adoption timeline.

    Sources:
    - California Secretary of State (sos.ca.gov)
    - League of Women Voters of California
    - Public Policy Institute of California
    """

    vca_data = {
        'county': [
            # 2018 (original 5)
            'Madera', 'Napa', 'Nevada', 'Sacramento', 'San Mateo',
            # 2020 (10 additional)
            'Amador', 'Butte', 'Calaveras', 'El Dorado', 'Fresno',
            'Los Angeles', 'Mariposa', 'Orange', 'Santa Clara', 'Tuolumne',
            # 2022 (12 additional - 11 announced + Kings)
            'Alameda', 'Kings', 'Marin', 'Merced', 'Riverside',
            'San Benito', 'San Diego', 'Santa Cruz', 'Sonoma',
            'Stanislaus', 'Ventura', 'Yolo',
            # 2024 (2 additional)
            'Humboldt', 'Placer'
        ],
        'vca_first_year': [
            # 2018
            2018, 2018, 2018, 2018, 2018,
            # 2020
            2020, 2020, 2020, 2020, 2020,
            2020, 2020, 2020, 2020, 2020,
            # 2022
            2022, 2022, 2022, 2022, 2022,
            2022, 2022, 2022, 2022,
            2022, 2022, 2022,
            # 2024
            2024, 2024
        ]
    }

    df = pd.DataFrame(vca_data)
    df['state'] = 'CA'
    df['source'] = 'CA Secretary of State'

    return df


# =============================================================================
# EXTENSION ELECTION DATA
# =============================================================================

def load_2020_presidential():
    """Load 2020 presidential results (already downloaded)."""

    df = pd.read_csv(f'{RAW_DIR}/countypres_2000-2020.csv')

    # Filter to our three states
    states = {'California': 'CA', 'Utah': 'UT', 'Washington': 'WA'}
    df = df[df['state_name'].isin(states.keys())].copy()

    # Clean up
    df['county'] = df['county_name'].str.replace(' County', '')
    df['state'] = df['state_name'].map(states)

    out = df[['state', 'county', 'votes_dem', 'votes_gop', 'total_votes']].copy()
    out.columns = ['state', 'county', 'dem_votes', 'rep_votes', 'total_votes']
    out['year'] = 2020
    out['office'] = 'president'

    return out


def create_placeholder_2022_2024():
    """
    Create placeholder structure for 2022 and 2024 data.

    These would need to be filled in from:
    - California: sos.ca.gov Statement of Vote
    - Utah: vote.utah.gov
    - Washington: sos.wa.gov
    """

    # Get county list from 2020 data
    df_2020 = load_2020_presidential()
    counties = df_2020[['state', 'county']].drop_duplicates()

    # 2022 gubernatorial placeholder
    df_2022 = counties.copy()
    df_2022['year'] = 2022
    df_2022['office'] = 'governor'
    df_2022['dem_votes'] = np.nan
    df_2022['rep_votes'] = np.nan
    df_2022['total_votes'] = np.nan
    df_2022['data_status'] = 'placeholder'

    # 2024 presidential placeholder
    df_2024 = counties.copy()
    df_2024['year'] = 2024
    df_2024['office'] = 'president'
    df_2024['dem_votes'] = np.nan
    df_2024['rep_votes'] = np.nan
    df_2024['total_votes'] = np.nan
    df_2024['data_status'] = 'placeholder'

    return df_2022, df_2024


# =============================================================================
# CVAP DATA
# =============================================================================

def create_cvap_placeholder():
    """
    Create placeholder for CVAP data.

    Source: U.S. Census Bureau
    https://www.census.gov/programs-surveys/decennial-census/about/voting-rights/cvap.html

    For 2020-2024, use 2020 Census-based estimates.
    """

    df_2020 = load_2020_presidential()
    counties = df_2020[['state', 'county']].drop_duplicates()

    cvap = counties.copy()
    cvap['cvap_2020'] = np.nan
    cvap['cvap_source'] = 'Census 2020 CVAP estimates (to be added)'

    return cvap


# =============================================================================
# VBM TREATMENT VARIABLE
# =============================================================================

def create_treatment_variable():
    """
    Create VBM treatment variable for extension period.

    Treatment = 1 if county has universal vote-by-mail

    California: VCA adoption (varies by county)
    Utah: 100% VBM since 2019
    Washington: 100% VBM since 2011
    """

    # California VCA adoption
    vca = create_vca_adoption_data()

    # Get all CA counties from 2020 data
    df_2020 = load_2020_presidential()
    ca_counties = df_2020[df_2020['state'] == 'CA']['county'].unique()

    # Create treatment for each year
    years = [2020, 2022, 2024]
    records = []

    for county in ca_counties:
        vca_year = vca[vca['county'] == county]['vca_first_year'].values
        vca_year = vca_year[0] if len(vca_year) > 0 else 9999  # Never adopted

        for year in years:
            records.append({
                'state': 'CA',
                'county': county,
                'year': year,
                'treat': 1 if year >= vca_year else 0,
                'vca_first_year': vca_year if vca_year < 9999 else np.nan
            })

    # Utah: all counties VBM since 2019
    ut_counties = df_2020[df_2020['state'] == 'UT']['county'].unique()
    for county in ut_counties:
        for year in years:
            records.append({
                'state': 'UT',
                'county': county,
                'year': year,
                'treat': 1,  # All VBM
                'vca_first_year': np.nan
            })

    # Washington: all counties VBM since 2011
    wa_counties = df_2020[df_2020['state'] == 'WA']['county'].unique()
    for county in wa_counties:
        for year in years:
            records.append({
                'state': 'WA',
                'county': county,
                'year': year,
                'treat': 1,  # All VBM
                'vca_first_year': np.nan
            })

    return pd.DataFrame(records)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("="*70)
    print("EXTENSION DATA COLLECTION")
    print("="*70)

    # VCA adoption data
    print("\n1. California VCA Adoption Data")
    vca = create_vca_adoption_data()
    vca.to_csv(f'{EXTENSION_DIR}/california_vca_adoption.csv', index=False)
    print(f"   VCA counties by year:")
    print(vca.groupby('vca_first_year').size())

    # 2020 Presidential
    print("\n2. 2020 Presidential Results")
    pres_2020 = load_2020_presidential()
    pres_2020.to_csv(f'{EXTENSION_DIR}/three_states_2020_pres.csv', index=False)
    print(f"   Counties by state: {dict(pres_2020.groupby('state').size())}")

    # 2022 and 2024 placeholders
    print("\n3. 2022 and 2024 Placeholders")
    df_2022, df_2024 = create_placeholder_2022_2024()
    df_2022.to_csv(f'{EXTENSION_DIR}/three_states_2022_gov_PLACEHOLDER.csv', index=False)
    df_2024.to_csv(f'{EXTENSION_DIR}/three_states_2024_pres_PLACEHOLDER.csv', index=False)
    print("   Created placeholder files (need manual data entry)")

    # CVAP placeholder
    print("\n4. CVAP Data Placeholder")
    cvap = create_cvap_placeholder()
    cvap.to_csv(f'{EXTENSION_DIR}/cvap_PLACEHOLDER.csv', index=False)
    print("   Created CVAP placeholder (need Census data)")

    # Treatment variable
    print("\n5. Treatment Variable for Extension")
    treat = create_treatment_variable()
    treat.to_csv(f'{EXTENSION_DIR}/treatment_extension.csv', index=False)
    print(f"   Treatment by state-year:")
    print(treat.groupby(['state', 'year'])['treat'].mean())

    print("\n" + "="*70)
    print("DATA COLLECTION SUMMARY")
    print("="*70)
    print("""
Files created in data/extension/:
1. california_vca_adoption.csv - VCA adoption dates (COMPLETE)
2. three_states_2020_pres.csv - 2020 presidential results (COMPLETE)
3. three_states_2022_gov_PLACEHOLDER.csv - 2022 gubernatorial (PLACEHOLDER)
4. three_states_2024_pres_PLACEHOLDER.csv - 2024 presidential (PLACEHOLDER)
5. cvap_PLACEHOLDER.csv - CVAP estimates (PLACEHOLDER)
6. treatment_extension.csv - VBM treatment variable (COMPLETE)

NOTE: Placeholder files need to be filled with actual data from:
- California: sos.ca.gov
- Utah: vote.utah.gov
- Washington: sos.wa.gov
- CVAP: census.gov
""")
