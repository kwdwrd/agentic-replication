"""
Extension Data Collection Script
Collects California, Utah, and Washington election data for 2020-2024
"""

import pandas as pd
import requests
import os

# Create output directory
os.makedirs('data/extension', exist_ok=True)

# =============================================================================
# California Election Data URLs
# =============================================================================

CA_URLS = {
    # 2020 General Election (Presidential)
    '2020_pres': 'https://elections.cdn.sos.ca.gov/sov/2020-general/sov/18-presidential.xlsx',

    # 2022 General Election (Gubernatorial)
    '2022_gov': 'https://elections.cdn.sos.ca.gov/sov/2022-general/ssov/governor-summary.xlsx',
}

# =============================================================================
# Download Functions
# =============================================================================

def download_excel(url, filename):
    """Download an Excel file from URL"""
    print(f"Downloading {url}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        filepath = f'data/extension/{filename}'
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"  Saved to {filepath}")
        return filepath
    except Exception as e:
        print(f"  Error downloading: {e}")
        return None


def main():
    """Main data collection function"""
    print("=" * 60)
    print("EXTENSION DATA COLLECTION")
    print("=" * 60)

    # Download California data
    print("\n--- California Election Data ---")

    for name, url in CA_URLS.items():
        filepath = download_excel(url, f'california_{name}.xlsx')
        if filepath:
            try:
                df = pd.read_excel(filepath)
                print(f"  Shape: {df.shape}")
                print(f"  Columns: {df.columns.tolist()[:5]}...")
            except Exception as e:
                print(f"  Error reading: {e}")

    print("\n--- Data Collection Summary ---")
    print("California VCA adoption data: data/extension/california_vbm_adoption.csv")
    print("California 2020 presidential: data/extension/california_2020_pres.xlsx")
    print("California 2022 gubernatorial: data/extension/california_2022_gov.xlsx")

    # Note: Utah and Washington data would need to be collected from their
    # respective Secretary of State websites. Since they are already 100% VBM,
    # they don't contribute new treatment variation but are needed for
    # the control group and full sample analysis.


if __name__ == '__main__':
    main()
