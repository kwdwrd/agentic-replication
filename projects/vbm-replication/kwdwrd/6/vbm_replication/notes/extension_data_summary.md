# Extension Data Collection Summary

## Overview

This document summarizes the extension data collected for California, Utah, and Washington for the 2020-2024 election cycles.

## Data Files Created

### California (58 counties)

| File | Description | Records |
|------|-------------|---------|
| `california_vbm_adoption.csv` | VCA adoption dates by county | 29 VCA counties |
| `california_results_2020_pres.csv` | 2020 Presidential (Biden vs Trump) | 58 counties |
| `california_results_2022_gov.csv` | 2022 Governor (Newsom vs Dahle) | 58 counties |
| `california_results_2024_pres.csv` | 2024 Presidential (Harris vs Trump) | 58 counties |
| `california_cvap_2018_2022.csv` | CVAP 2018-2022 ACS estimates | 58 counties |
| `california_cvap_2020_2024.csv` | CVAP 2020-2024 ACS estimates | 58 counties |

**VCA Adoption Timeline:**
- 2018: 5 counties (Madera, Napa, Nevada, Sacramento, San Mateo)
- 2020: 10 additional counties
- 2022: 12 additional counties
- 2024: 2 additional counties
- Total: 29 of 58 counties have adopted VCA

### Utah (29 counties)

| File | Description | Records |
|------|-------------|---------|
| `utah_results_2020_pres.csv` | 2020 Presidential (Biden vs Trump) | 29 counties |
| `utah_results_2024_pres.csv` | 2024 Presidential (Harris vs Trump) | 29 counties |
| `utah_results_2024_gov.csv` | 2024 Governor (Reyes vs Cox) | 29 counties |
| `utah_results_2022_senate.csv` | 2022 Senate (McMullin vs Lee) - PARTIAL | 8 counties |
| `utah_cvap_2018_2022.csv` | CVAP 2018-2022 ACS estimates | 29 counties |
| `utah_cvap_2020_2024.csv` | CVAP 2020-2024 ACS estimates | 29 counties |

**Important Note on Utah 2022:**
- No Democratic candidate in the 2022 Senate race
- Evan McMullin ran as Independent, endorsed by Utah Democratic Party
- Only partial county-level data available from news sources
- **Recommendation:** Exclude Utah 2022 from `dem_share_sen` analysis; use for turnout only

**Utah VBM Status:**
- Utah implemented universal vote-by-mail statewide in 2019
- All 29 counties are "treated" in 2020+ elections
- No within-state variation for difference-in-differences design

### Washington (39 counties)

| File | Description | Records |
|------|-------------|---------|
| `washington_results_2020_pres.csv` | 2020 Presidential (Biden vs Trump) | 39 counties |
| `washington_results_2020_gov.csv` | 2020 Governor (Inslee vs Culp) | 39 counties |
| `washington_results_2022_sen.csv` | 2022 Senate (Murray vs Smiley) | 39 counties |
| `washington_results_2024_pres.csv` | 2024 Presidential (Harris vs Trump) | 39 counties |
| `washington_results_2024_gov.csv` | 2024 Governor (Ferguson vs Reichert) | 39 counties |
| `washington_cvap_2018_2022.csv` | CVAP 2018-2022 ACS estimates | 39 counties |
| `washington_cvap_2020_2024.csv` | CVAP 2020-2024 ACS estimates | 39 counties |

**Washington VBM Status:**
- Washington has been universal vote-by-mail since 2011
- All 39 counties are "treated" throughout the study period
- No within-state variation for difference-in-differences design

## Validation Results

### California Statewide Totals (Two-Party Vote Share)
| Election | Democratic | Republican | Dem Share |
|----------|-----------|------------|-----------|
| 2020 Pres | 11,110,250 | 6,006,429 | 64.91% |
| 2022 Gov | 6,470,104 | 4,462,914 | 59.18% |
| 2024 Pres | 9,276,179 | 6,081,697 | 60.40% |

### Utah Statewide Totals (Two-Party Vote Share)
| Election | Democratic | Republican | Dem Share |
|----------|-----------|------------|-----------|
| 2020 Pres | 560,282 | 865,140 | 39.31% |
| 2024 Pres | 562,566 | 883,818 | 38.89% |
| 2024 Gov | 420,514 | 781,431 | 34.99% |

### Washington Statewide Totals (Two-Party Vote Share)
| Election | Democratic | Republican | Dem Share |
|----------|-----------|------------|-----------|
| 2020 Pres | 2,369,612 | 1,584,651 | 59.93% |
| 2020 Gov | 2,294,243 | 1,749,066 | 56.74% |
| 2022 Sen | 1,741,827 | 1,299,322 | 57.28% |
| 2024 Pres | 2,245,849 | 1,530,923 | 59.46% |
| 2024 Gov | 2,143,368 | 1,709,818 | 55.63% |

## Data Sources

### California
- California Secretary of State Election Results (sos.ca.gov)
- VCA adoption: California Secretary of State, League of Women Voters reports

### Utah
- Utah Election Results Portal (electionresults.utah.gov)
- County canvass reports (PDFs)
- News sources (NBC News, Salt Lake Tribune) for 2022 partial data

### Washington
- Washington Secretary of State Election Results (results.vote.wa.gov)
- All data retrieved from official state portal

### CVAP Data
- U.S. Census Bureau Citizen Voting Age Population Special Tabulation
- 2018-2022 ACS 5-Year estimates
- 2020-2024 ACS 5-Year estimates (most recent)

## Implications for Extension Analysis

### California: Full Difference-in-Differences Analysis Possible
- Staggered VCA adoption provides treatment variation
- Can compare VCA vs non-VCA counties within California
- Rich outcome data available (presidential, gubernatorial)

### Utah & Washington: Limited Variation
- Both states have universal VBM statewide
- No within-state control group available
- Can contribute to:
  - Pre-post comparisons (if merging with original data)
  - Cross-state comparisons with non-VBM states
  - Turnout trends over time

### Recommended Analysis Strategy
1. **Primary analysis:** California VCA counties (treatment) vs non-VCA counties (control)
2. **Robustness check:** All three states, comparing to national trends
3. **Exclude Utah 2022 Senate** from partisan outcome analysis due to lack of Democratic candidate
