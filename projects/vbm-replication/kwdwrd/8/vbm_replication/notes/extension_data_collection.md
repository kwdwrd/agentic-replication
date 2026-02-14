# Extension Data Collection Summary

## Overview

This document summarizes the data collection process for extending Thompson et al. (2020) analysis to 2020-2024.

## Data Sources

### 1. California Voter's Choice Act (VCA) Adoption
- **File**: `data/extension/california_vbm_adoption.csv`
- **Source**: California Secretary of State
- **Content**: VCA adoption year for all 58 California counties
- **Key Statistics**:
  - 30 counties adopted VCA (as of 2024)
  - 28 counties have not adopted VCA
  - First adoption: 2018 (5 counties: Madera, Napa, Nevada, Sacramento, San Mateo)
  - Most recent: 2024 (4 counties: Plumas, San Benito, Sutter, Yuba)

### 2. Presidential Election Results (2020-2024)
- **File**: `data/extension/pres_results_2020_2024.csv`
- **Source**: tonmcg/US_County_Level_Election_Results_08-24 (GitHub)
- **Original Source**: Various state election offices
- **Content**: County-level presidential vote totals
- **Coverage**:
  - California: 58 counties x 2 elections = 116 observations
  - Utah: 29 counties x 2 elections = 58 observations
  - Washington: 39 counties x 2 elections = 78 observations
- **Variables**: state_name, county_fips, county_name, votes_gop, votes_dem, total_votes, per_gop, per_dem

### 3. California Governor 2022
- **File**: `data/extension/ca_2022_gov_county.csv`
- **Source**: MIT Election Lab (MEDSL) 2022-elections-official
- **Content**: County-level gubernatorial vote totals
- **Candidates**: Gavin Newsom (D), Brian Dahle (R)
- **Coverage**: 58 California counties

### 4. Utah Senate 2022
- **File**: `data/extension/ut_2022_senate_county.csv`
- **Source**: MIT Election Lab (MEDSL) 2022-elections-official
- **Content**: County-level Senate vote totals
- **Candidates**: Mike Lee (R), Evan McMullin (I), James Hansen (L), Tommy Williams
- **Coverage**: 29 Utah counties

### 5. Washington Senate 2022
- **File**: `data/extension/wa_2022_senate_county.csv`
- **Source**: MIT Election Lab (MEDSL) 2022-elections-official
- **Content**: County-level Senate vote totals
- **Candidates**: Patty Murray (D), Tiffany Smiley (R)
- **Coverage**: 39 Washington counties

### 6. Citizen Voting Age Population (CVAP)
- **File**: `data/extension/cvap_county_2016_2020.csv`
- **Source**: U.S. Census Bureau CVAP Special Tabulation (2016-2020 ACS 5-Year)
- **Content**: CVAP estimates with margins of error
- **Coverage**:
  - California: 58 counties
  - Utah: 29 counties
  - Washington: 39 counties
- **Variables**: county, state, fips, cvap_2020, cvap_moe_2020

## Raw Data Files (for reference)

Additional raw data files in `data/extension/`:

| File | Description | Size |
|------|-------------|------|
| `countypres_2020.csv` | Full 2020 presidential results (all states) | 348 KB |
| `countypres_2024.csv` | Full 2024 presidential results (all states) | 352 KB |
| `CA_2022_final.csv` | California 2022 precinct-level data | 217 MB |
| `UT-cleaned.csv` | Utah 2022 precinct-level data | 18 MB |
| `2022-wa-local-precinct-general.csv` | Washington 2022 precinct-level data | 75 MB |
| `County.csv` | Full CVAP data (all counties) | 4.3 MB |

## Data Validation

All datasets have been validated:
- County counts match expected values for each state
- No missing counties in any dataset
- Party labels are consistent across datasets
- FIPS codes can be used for merging

## Notes for Extension Analysis

1. **Treatment Definition**: For California, treatment = VCA adoption year
2. **Outcome Variables**:
   - Democratic vote share (presidential, gubernatorial, Senate)
   - Turnout share (requires merging with CVAP)
3. **Time Periods**:
   - 2020: Presidential election
   - 2022: Gubernatorial/Senate elections
   - 2024: Presidential election
4. **Control Group**:
   - California counties that have not adopted VCA
   - Utah and Washington counties (all-VBM since before 2018)

## Next Steps

1. Merge all datasets into unified panel
2. Calculate Democratic vote shares and turnout rates
3. Apply difference-in-differences estimation
4. Compare results to original Thompson et al. (2020) findings
