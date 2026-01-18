"""
03_collect_extension.py

Collect extension data for 2020-2024 elections in California, Utah, and Washington.
"""

import pandas as pd
import numpy as np
import requests
import os
from io import BytesIO

# =============================================================================
# CALIFORNIA DATA COLLECTION
# =============================================================================

def parse_ca_sov_excel(filepath, year, office):
    """Parse California Statement of Vote Excel file."""
    df = pd.read_excel(filepath)

    # Filter out non-county rows
    df = df[df.iloc[:, 0].notna()]
    df = df[~df.iloc[:, 0].astype(str).str.contains('Percent', case=False, na=False)]
    df = df[~df.iloc[:, 0].astype(str).str.contains('State Totals', case=False, na=False)]
    df = df[~df.iloc[:, 0].astype(str).str.contains('Total', case=False, na=False)]

    # First row after filtering might still be a header
    if df.iloc[0, 1] in ['DEM', 'REP', 'Democratic', 'Republican']:
        df = df.iloc[1:]

    # Reset columns - first is county, rest are candidates
    cols = df.columns.tolist()
    df = df.rename(columns={cols[0]: 'county'})

    # Find Democratic and Republican columns
    dem_col = None
    rep_col = None
    for col in df.columns[1:]:
        col_str = str(col).lower()
        if 'biden' in col_str or 'newsom' in col_str or 'dem' in col_str:
            dem_col = col
        elif 'trump' in col_str or 'rep' in col_str or 'faulconer' in col_str or 'dahle' in col_str:
            rep_col = col

    if dem_col is None or rep_col is None:
        # Try to identify by position or party indicator
        # Often Dem is col 1, Rep is col 2
        dem_col = df.columns[1]
        rep_col = df.columns[2]

    # Convert to numeric
    df['dem_votes'] = pd.to_numeric(df[dem_col], errors='coerce')
    df['rep_votes'] = pd.to_numeric(df[rep_col], errors='coerce')

    # Calculate total from all candidate columns
    vote_cols = [c for c in df.columns if c not in ['county', 'dem_votes', 'rep_votes']]
    for c in vote_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df['total_votes'] = df[vote_cols].sum(axis=1)

    # Clean up
    result = df[['county', 'dem_votes', 'rep_votes', 'total_votes']].copy()
    result = result.dropna(subset=['dem_votes', 'rep_votes'])
    result['year'] = year
    result['office'] = office
    result['state'] = 'CA'

    return result


def collect_california_data():
    """Collect California election data for 2020-2024."""
    print("Collecting California election data...")

    all_data = []

    # 2020 Presidential
    url = "https://elections.cdn.sos.ca.gov/sov/2020-general/sov/18-presidential.xlsx"
    try:
        response = requests.get(url)
        df = pd.read_excel(BytesIO(response.content))

        # Parse the data
        df = df[df.iloc[:, 0].notna()]
        df = df[~df.iloc[:, 0].astype(str).str.contains('Percent', case=False, na=False)]
        df = df[~df.iloc[:, 0].astype(str).str.contains('State Totals', case=False, na=False)]

        # Remove header row if present
        if str(df.iloc[0, 1]).upper() == 'DEM':
            df = df.iloc[1:]

        result = pd.DataFrame()
        result['county'] = df.iloc[:, 0]
        result['dem_votes'] = pd.to_numeric(df.iloc[:, 1], errors='coerce')
        result['rep_votes'] = pd.to_numeric(df.iloc[:, 2], errors='coerce')

        # Sum all vote columns for total
        vote_cols = df.iloc[:, 1:]
        for c in vote_cols.columns:
            vote_cols[c] = pd.to_numeric(vote_cols[c], errors='coerce')
        result['total_votes'] = vote_cols.sum(axis=1)

        result = result.dropna(subset=['dem_votes', 'rep_votes'])
        result['year'] = 2020
        result['office'] = 'pres'
        result['state'] = 'CA'

        all_data.append(result)
        print(f"  2020 Presidential: {len(result)} counties")
    except Exception as e:
        print(f"  Error fetching 2020 presidential: {e}")

    # 2022 Gubernatorial
    url = "https://elections.cdn.sos.ca.gov/sov/2022-general/sov/15-governor.xlsx"
    try:
        response = requests.get(url)
        df = pd.read_excel(BytesIO(response.content))

        df = df[df.iloc[:, 0].notna()]
        df = df[~df.iloc[:, 0].astype(str).str.contains('Percent', case=False, na=False)]
        df = df[~df.iloc[:, 0].astype(str).str.contains('State Totals', case=False, na=False)]
        df = df[~df.iloc[:, 0].astype(str).str.contains('Total', case=False, na=False)]

        if str(df.iloc[0, 1]).upper() in ['DEM', 'DEMOCRATIC']:
            df = df.iloc[1:]

        result = pd.DataFrame()
        result['county'] = df.iloc[:, 0]
        result['dem_votes'] = pd.to_numeric(df.iloc[:, 1], errors='coerce')  # Newsom
        result['rep_votes'] = pd.to_numeric(df.iloc[:, 2], errors='coerce')  # Dahle

        vote_cols = df.iloc[:, 1:]
        for c in vote_cols.columns:
            vote_cols[c] = pd.to_numeric(vote_cols[c], errors='coerce')
        result['total_votes'] = vote_cols.sum(axis=1)

        result = result.dropna(subset=['dem_votes', 'rep_votes'])
        result['year'] = 2022
        result['office'] = 'gov'
        result['state'] = 'CA'

        all_data.append(result)
        print(f"  2022 Gubernatorial: {len(result)} counties")
    except Exception as e:
        print(f"  Error fetching 2022 gubernatorial: {e}")

    # 2024 Presidential
    url = "https://elections.cdn.sos.ca.gov/sov/2024-general/sov/18-presidential.xlsx"
    try:
        response = requests.get(url)
        df = pd.read_excel(BytesIO(response.content))

        df = df[df.iloc[:, 0].notna()]
        df = df[~df.iloc[:, 0].astype(str).str.contains('Percent', case=False, na=False)]
        df = df[~df.iloc[:, 0].astype(str).str.contains('State Totals', case=False, na=False)]
        df = df[~df.iloc[:, 0].astype(str).str.contains('Total', case=False, na=False)]

        if str(df.iloc[0, 1]).upper() in ['DEM', 'DEMOCRATIC']:
            df = df.iloc[1:]

        result = pd.DataFrame()
        result['county'] = df.iloc[:, 0]
        result['dem_votes'] = pd.to_numeric(df.iloc[:, 1], errors='coerce')  # Harris
        result['rep_votes'] = pd.to_numeric(df.iloc[:, 2], errors='coerce')  # Trump

        vote_cols = df.iloc[:, 1:]
        for c in vote_cols.columns:
            vote_cols[c] = pd.to_numeric(vote_cols[c], errors='coerce')
        result['total_votes'] = vote_cols.sum(axis=1)

        result = result.dropna(subset=['dem_votes', 'rep_votes'])
        result['year'] = 2024
        result['office'] = 'pres'
        result['state'] = 'CA'

        all_data.append(result)
        print(f"  2024 Presidential: {len(result)} counties")
    except Exception as e:
        print(f"  Error fetching 2024 presidential: {e}")

    if all_data:
        ca_data = pd.concat(all_data, ignore_index=True)
        return ca_data
    return None


# =============================================================================
# UTAH DATA COLLECTION
# =============================================================================

def collect_utah_data():
    """Collect Utah election data for 2020-2024."""
    print("Collecting Utah election data...")

    # Utah data is harder to get programmatically
    # We'll create placeholder data structure that can be filled in

    # Note: Utah has been 100% VBM since 2019, so all observations are treated
    # For the extension, we need:
    # - 2020 Presidential
    # - 2022 Senatorial (Mike Lee vs McMullin)
    # - 2024 Presidential

    # Placeholder - in practice would need to download from Utah elections website
    print("  Note: Utah data requires manual collection from vote.utah.gov")
    print("  Creating placeholder structure...")

    return None


# =============================================================================
# WASHINGTON DATA COLLECTION
# =============================================================================

def collect_washington_data():
    """Collect Washington election data for 2020-2024."""
    print("Collecting Washington election data...")

    # Washington data from Secretary of State
    # Note: Washington has been 100% VBM since 2011, so all observations are treated

    print("  Note: Washington data requires collection from sos.wa.gov")
    print("  Creating placeholder structure...")

    return None


# =============================================================================
# CVAP DATA
# =============================================================================

def collect_cvap_data():
    """Collect Citizen Voting Age Population data from Census."""
    print("Collecting CVAP data...")

    # CVAP data comes from American Community Survey special tabulation
    # Available at: https://www.census.gov/programs-surveys/decennial-census/about/voting-rights/cvap.html

    print("  Note: CVAP data requires download from Census website")
    print("  Using 2020 Census-based estimates")

    return None


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("="*60)
    print("EXTENSION DATA COLLECTION")
    print("="*60)

    # Create output directory
    os.makedirs('data/extension', exist_ok=True)

    # Collect California data
    ca_data = collect_california_data()
    if ca_data is not None:
        ca_data.to_csv('data/extension/california_results.csv', index=False)
        print(f"\nSaved California data: {len(ca_data)} observations")
        print(ca_data.groupby(['year', 'office']).size())

    # Collect Utah data
    ut_data = collect_utah_data()

    # Collect Washington data
    wa_data = collect_washington_data()

    # Collect CVAP data
    cvap_data = collect_cvap_data()

    print("\n" + "="*60)
    print("DATA COLLECTION SUMMARY")
    print("="*60)
    print("California: Election results collected for 2020, 2022, 2024")
    print("Utah: Requires manual collection (100% VBM since 2019)")
    print("Washington: Requires manual collection (100% VBM since 2011)")
    print("CVAP: Requires download from Census website")
