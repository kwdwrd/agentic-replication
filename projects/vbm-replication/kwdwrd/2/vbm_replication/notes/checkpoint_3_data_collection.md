# Checkpoint 3: Extension Data Collection

## Summary

Data collection for the VBM extension analysis is complete. This document summarizes the data sources, collection methodology, and validation results.

## Data Collected

### 1. California VCA Adoption Data
**File:** `data/extension/california_vca_adoption.csv`

- **Source:** California Secretary of State VCA Implementation Timeline
- **Coverage:** All 58 California counties
- **Variables:** county, vca_first_year

**VCA Adoption Timeline:**
| Year | Counties Adopted | Total Treated | Notable Counties |
|------|-----------------|---------------|------------------|
| 2018 | 5 | 5 | Madera, Napa, Nevada, Sacramento, San Mateo |
| 2020 | 10 | 15 | Los Angeles, Orange, Fresno, Mariposa |
| 2022 | 12 | 27 | San Diego, Riverside, Ventura, Solano |
| 2024 | 3 | 30 | Humboldt, Imperial, Placer |
| Never | 28 | - | Rural counties, including Alpine, Modoc, etc. |

### 2. Election Results Data
**File:** `data/extension/extension_election_results.csv`

#### California (58 counties × 3 elections = 174 observations)
- **2020 Presidential:** Biden vs Trump
- **2022 Gubernatorial:** Newsom vs Dahle
- **2024 Presidential:** Harris vs Trump
- **Source:** California Secretary of State Statement of Vote Excel files

#### Utah (29 counties × 3 elections = 87 observations)
- **2020 Presidential:** Biden vs Trump (from Excel file)
- **2022 Senate:** McMullin vs Lee (from PDF canvass report)
- **2024 Presidential:** Harris vs Trump (from PDF canvass report)
- **Source:** Utah Lieutenant Governor Election Results
- **Note:** Utah has been 100% VBM since 2019 (always treated)

#### Washington (39 counties × 3 elections = 117 observations)
- **2020 Presidential:** Biden vs Trump (from GitHub repository)
- **2022 Senate:** Murray vs Smiley (estimated from county proportions)
- **2024 Presidential:** Harris vs Trump (from GitHub repository)
- **Source:** Washington Secretary of State via GitHub (tonmcg/US_County_Level_Election_Results)
- **Note:** Washington has been 100% VBM since 2011 (always treated)

**Total Observations:** 378 county-election observations

### 3. CVAP Data
**File:** `data/extension/cvap_estimates.csv`

- **Source:** Census Bureau CVAP Special Tabulation (2014-2018 ACS)
- **Coverage:** 126 counties (CA: 58, UT: 29, WA: 39)
- **Variables:** county, state, cvap_2018, cvap_2020, cvap_2022, cvap_2024

**Note:** 2020-2024 estimates are projected from 2014-2018 ACS CVAP using 1% annual growth assumption. For production analysis, the 2018-2022 ACS CVAP should be downloaded from Census when available.

## Data Quality Summary

### Validation Results
- All county counts match expected values (CA: 58, UT: 29, WA: 39)
- No missing values in election data
- No negative or zero vote counts
- Democratic vote share ranges from 9.9% to 87.0% (plausible)
- CVAP data matches election data counties perfectly

### State-Level Vote Totals (2020)
| State | Democratic | Republican | Dem Share |
|-------|------------|------------|-----------|
| CA | 11,110,250 | 6,006,429 | 64.9% |
| UT | 560,282 | 865,140 | 39.3% |
| WA | 2,369,612 | 1,584,651 | 59.9% |

## Data Limitations

1. **Washington 2022 Senate:** County-level results were estimated by distributing statewide totals (Murray: 1,741,827, Smiley: 1,299,322) proportionally based on 2020 presidential county shares. Since WA is always-treated, this primarily affects precision rather than identification.

2. **CVAP Projections:** The 2020-2024 CVAP estimates are projected from 2014-2018 ACS data. The Census 2018-2022 CVAP should be used for final analysis when available.

3. **Utah 2022 Senate:** No major Democratic candidate ran; Evan McMullin (Independent) was the primary Democratic-aligned alternative to Mike Lee. McMullin votes are coded as "dem_votes" for analysis purposes.

## Files Created

```
data/extension/
├── california_vca_adoption.csv      # VCA treatment timing
├── california_results.csv           # CA election results
├── utah_2020_pres.csv              # UT 2020 presidential
├── utah_2022_sen.csv               # UT 2022 senate
├── utah_2024_pres.csv              # UT 2024 presidential
├── utah_results.csv                # Combined UT results
├── washington_2020_pres.csv        # WA 2020 presidential
├── washington_2022_sen.csv         # WA 2022 senate (estimated)
├── washington_2024_pres.csv        # WA 2024 presidential
├── washington_results.csv          # Combined WA results
├── extension_election_results.csv  # All election results combined
└── cvap_estimates.csv              # CVAP by county
```

## Next Steps

1. **Phase 4:** Prepare extension panel dataset by merging election results with VCA adoption and CVAP data
2. **Phase 5:** Run extension regressions replicating Thompson et al. methodology
3. **Phase 6:** Write up results and compare to original findings
