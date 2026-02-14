# Data Preparation Summary

## Datasets Created

### 1. Extension Dataset (`data/extension/extension_analysis.csv`)
- **Rows:** 349
- **Years:** 2020, 2022, 2024
- **Coverage:**
  - California: 58 counties × 3 years = 174 rows
  - Utah: 29 counties × 2 years = 58 rows (2022 excluded - no Dem candidate)
  - Washington: 39 counties × 3 years = 117 rows

### 2. Combined Dataset (`data/combined_analysis.csv`)
- **Rows:** 1,803
- **Years:** 1996-2024 (15 election cycles)
- **Coverage:** Original data (1996-2018) + Extension (2020-2024)

### 3. California-Only Dataset (`data/california_analysis.csv`)
- **Rows:** 812
- **Years:** 1998-2024 (CA not in 1996 original data)
- **Purpose:** Primary analysis of VCA effects within California

## Treatment Variable (`treat`)

### California
Treatment = 1 if county has adopted Voter's Choice Act (VCA) by election year

| Year | Treated Counties | Treatment Rate |
|------|-----------------|----------------|
| 2018 | 5 | 8.6% |
| 2020 | 15 | 25.9% |
| 2022 | 27 | 46.6% |
| 2024 | 29 | 50.0% |

### Utah
- Treatment = 1 for all counties in 2020+
- Universal vote-by-mail implemented statewide in 2019
- No within-state variation for DiD

### Washington
- Treatment = 1 for all counties in 2012+
- Universal vote-by-mail since 2011
- No within-state variation for DiD in extension period

## Key Variables

| Variable | Description | Availability |
|----------|-------------|--------------|
| `dem_share_pres` | Dem two-party share, Presidential | Presidential years |
| `dem_share_gov` | Dem two-party share, Governor | Non-presidential years |
| `dem_share_sen` | Dem two-party share, Senate | WA 2022 only |
| `turnout_share` | Ballots cast / CVAP | All observations |
| `treat` | VBM treatment indicator | All observations |
| `cvap` | Citizen Voting Age Population | All observations |

## Turnout Summary (Extension Period)

| State | 2020 | 2022 | 2024 |
|-------|------|------|------|
| CA | 66.1% | 46.0% | 61.4% |
| UT | 68.0% | - | 71.3% |
| WA | 72.3% | 56.8% | 70.7% |

Notes:
- 2022 shows typical midterm turnout decline
- All states show high presidential year turnout (2020, 2024)
- WA consistently has highest turnout

## Analysis Strategy

### Primary Analysis: California VCA
- Staggered difference-in-differences within California
- Treated: VCA counties (staggered adoption 2018-2024)
- Control: Non-VCA counties
- Fixed effects: County FE + Year FE
- Specifications: Basic, linear trends, quadratic trends

### Secondary Analysis: Cross-State Comparison
- Compare treated (VCA/universal VBM) vs untreated periods
- Longer time series including original data (1996-2018)
- State × Year fixed effects

### Limitations
1. Utah 2022 excluded from partisan analysis (no Dem candidate)
2. UT and WA have no within-state variation in extension period
3. COVID-19 may confound 2020 turnout effects
4. VBM_share variable not available for extension period
