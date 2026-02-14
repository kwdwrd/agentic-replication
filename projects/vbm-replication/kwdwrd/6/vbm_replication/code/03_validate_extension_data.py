"""
Validate extension data collection for CA, UT, WA 2020-2024
"""
import pandas as pd
import os

data_dir = '../data/extension'

def validate_file(filepath, expected_counties, state_name):
    """Validate a single election results file."""
    if not os.path.exists(filepath):
        print(f"  MISSING: {filepath}")
        return None

    df = pd.read_csv(filepath)
    n_counties = len(df)

    if n_counties != expected_counties:
        print(f"  WARNING: {filepath} has {n_counties} counties, expected {expected_counties}")
    else:
        print(f"  OK: {filepath} - {n_counties} counties")

    # Compute totals and shares if applicable
    if 'dem_votes' in df.columns and 'rep_votes' in df.columns:
        total_dem = df['dem_votes'].sum()
        total_rep = df['rep_votes'].sum()
        total_votes = df['total_votes'].sum() if 'total_votes' in df.columns else total_dem + total_rep
        dem_share = total_dem / (total_dem + total_rep) * 100
        print(f"       Total Dem: {total_dem:,}, Rep: {total_rep:,}, Total: {total_votes:,}")
        print(f"       Dem two-party share: {dem_share:.2f}%")

    return df

print("=" * 60)
print("CALIFORNIA DATA VALIDATION")
print("=" * 60)

# California: 58 counties
ca_vca = pd.read_csv(f'{data_dir}/california_vbm_adoption.csv')
print(f"\nVCA Adoption: {len(ca_vca)} counties")
print(f"  VCA counties by year: {ca_vca.groupby('vca_first_year').size().to_dict()}")

print("\nElection Results:")
validate_file(f'{data_dir}/california_results_2020_pres.csv', 58, 'California')
validate_file(f'{data_dir}/california_results_2022_gov.csv', 58, 'California')
validate_file(f'{data_dir}/california_results_2024_pres.csv', 58, 'California')

print("\nCVAP Data:")
validate_file(f'{data_dir}/california_cvap_2018_2022.csv', 58, 'California')
validate_file(f'{data_dir}/california_cvap_2020_2024.csv', 58, 'California')

print("\n" + "=" * 60)
print("UTAH DATA VALIDATION")
print("=" * 60)

# Utah: 29 counties
print("\nElection Results:")
validate_file(f'{data_dir}/utah_results_2020_pres.csv', 29, 'Utah')
validate_file(f'{data_dir}/utah_results_2024_pres.csv', 29, 'Utah')
validate_file(f'{data_dir}/utah_results_2024_gov.csv', 29, 'Utah')

# Note about Utah 2022
print("\nUtah 2022 Senate (partial data - no Dem candidate):")
if os.path.exists(f'{data_dir}/utah_results_2022_senate.csv'):
    ut2022 = pd.read_csv(f'{data_dir}/utah_results_2022_senate.csv')
    print(f"  Partial data: {len(ut2022)} counties (of 29)")
    print(f"  Note: No Democratic candidate in 2022 - McMullin ran as Independent")

print("\nCVAP Data:")
validate_file(f'{data_dir}/utah_cvap_2018_2022.csv', 29, 'Utah')
validate_file(f'{data_dir}/utah_cvap_2020_2024.csv', 29, 'Utah')

print("\n" + "=" * 60)
print("WASHINGTON DATA VALIDATION")
print("=" * 60)

# Washington: 39 counties
print("\nElection Results:")
validate_file(f'{data_dir}/washington_results_2020_pres.csv', 39, 'Washington')
validate_file(f'{data_dir}/washington_results_2020_gov.csv', 39, 'Washington')
validate_file(f'{data_dir}/washington_results_2022_sen.csv', 39, 'Washington')
validate_file(f'{data_dir}/washington_results_2024_pres.csv', 39, 'Washington')
validate_file(f'{data_dir}/washington_results_2024_gov.csv', 39, 'Washington')

print("\nCVAP Data:")
validate_file(f'{data_dir}/washington_cvap_2018_2022.csv', 39, 'Washington')
validate_file(f'{data_dir}/washington_cvap_2020_2024.csv', 39, 'Washington')

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

# Count total files
extension_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
print(f"\nTotal extension data files: {len(extension_files)}")
for f in sorted(extension_files):
    filepath = os.path.join(data_dir, f)
    size = os.path.getsize(filepath)
    print(f"  {f}: {size:,} bytes")
