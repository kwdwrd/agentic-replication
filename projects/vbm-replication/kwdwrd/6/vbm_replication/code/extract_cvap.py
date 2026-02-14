"""
Extract CVAP (Citizen Voting Age Population) for CA, UT, WA counties
from the Census Bureau ACS Special Tabulation files
"""
import pandas as pd

def extract_cvap(input_file, suffix):
    """Extract CVAP data for CA, UT, WA from a Census CVAP county file."""
    cvap = pd.read_csv(input_file, encoding='latin-1')

    # Filter to Total rows only (lnnumber == 1)
    cvap_total = cvap[cvap['lnnumber'] == 1].copy()

    # Extract state FIPS from geoid (format: 0500000US{state_fips}{county_fips})
    cvap_total['state_fips'] = cvap_total['geoid'].str.extract(r'0500000US(\d{2})\d{3}')
    cvap_total['county_fips'] = cvap_total['geoid'].str.extract(r'0500000US\d{2}(\d{3})')

    # Filter to CA (06), UT (49), WA (53)
    states = {'06': 'California', '49': 'Utah', '53': 'Washington'}
    cvap_states = cvap_total[cvap_total['state_fips'].isin(states.keys())].copy()

    # Extract county name from geoname
    cvap_states['county'] = cvap_states['geoname'].str.extract(r'^([^,]+) County,')[0]

    # Select relevant columns
    cvap_out = cvap_states[['state_fips', 'county_fips', 'county', 'cvap_est', 'cvap_moe']].copy()
    cvap_out['state'] = cvap_out['state_fips'].map(states)
    cvap_out = cvap_out.rename(columns={'cvap_est': 'cvap', 'cvap_moe': 'cvap_moe'})

    # Save by state
    for fips, state_name in states.items():
        state_data = cvap_out[cvap_out['state_fips'] == fips][['county', 'cvap', 'cvap_moe']]
        filename = f'../data/extension/{state_name.lower()}_cvap_{suffix}.csv'
        state_data.to_csv(filename, index=False)
        print(f"Saved {len(state_data)} counties for {state_name} ({suffix})")

    # Also save combined file
    cvap_out_full = cvap_out[['state', 'county', 'cvap', 'cvap_moe']]
    cvap_out_full.to_csv(f'../data/extension/cvap_ca_ut_wa_{suffix}.csv', index=False)
    print(f"Saved combined file with {len(cvap_out_full)} total counties")
    return cvap_out_full

# Process both datasets
print("=== 2018-2022 ACS CVAP ===")
cvap_2018_2022 = extract_cvap('../data/extension/cvap_county_2018_2022.csv', '2018_2022')

print("\n=== 2020-2024 ACS CVAP ===")
cvap_2020_2024 = extract_cvap('../data/extension/cvap_county_2020_2024.csv', '2020_2024')
