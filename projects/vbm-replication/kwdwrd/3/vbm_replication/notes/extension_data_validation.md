# Extension Data Validation

## Data Collection Summary

### Fully Collected Data

#### 1. California VCA Adoption (`california_vca_adoption.csv`)
- **Status**: COMPLETE
- **Source**: California Secretary of State, LWVC, PPIC
- **Coverage**: All 29 VCA counties with adoption years

| Year | Counties Added | Total VCA Counties |
|------|---------------|-------------------|
| 2018 | 5 | 5 |
| 2020 | 10 | 15 |
| 2022 | 12 | 27 |
| 2024 | 2 | 29 |

#### 2. 2020 Presidential Results (`three_states_2020_pres.csv`)
- **Status**: COMPLETE
- **Source**: GitHub (tonmcg/US_County_Level_Election_Results_08-20)
- **Coverage**: All 126 counties (58 CA + 29 UT + 39 WA)
- **Variables**: state, county, dem_votes, rep_votes, total_votes

#### 3. VBM Treatment Variable (`treatment_extension.csv`)
- **Status**: COMPLETE
- **Coverage**: All counties for 2020, 2022, 2024
- **Logic**:
  - California: VCA adoption year determines treatment
  - Utah: All VBM since 2019 (treat=1 for all years)
  - Washington: All VBM since 2011 (treat=1 for all years)

### Placeholder Data (Requires Manual Entry)

#### 4. 2022 Gubernatorial Results
- **Status**: PLACEHOLDER
- **Needed from**:
  - California: sos.ca.gov Statement of Vote
  - Utah: vote.utah.gov
  - Washington: sos.wa.gov

**Known California 2022 Results** (from web search):
- Newsom (D): 6,470,104 votes (59.2%)
- Dahle (R): 4,462,914 votes (40.8%)
- Dahle flipped 5 counties from 2018: Lake, Merced, Orange, San Bernardino, San Joaquin

#### 5. 2024 Presidential Results
- **Status**: PLACEHOLDER
- **Needed from**: State Secretary of State offices

**Known California 2024 Results** (from web search):
- Harris (D): ~58.5%
- Trump (R): ~38%
- Trump flipped 10 counties from 2020: Butte, Fresno, Imperial, Inyo, Lake, Merced, Riverside, San Bernardino, San Joaquin, Stanislaus

#### 6. CVAP Data
- **Status**: PLACEHOLDER
- **Source needed**: Census Bureau CVAP estimates
- **Note**: Should use 2020 Census-based estimates for 2020-2024

---

## Data Quality Checks

### 2020 Presidential Data Validation

| State | Counties | Total Votes | Biden % | Trump % |
|-------|----------|-------------|---------|---------|
| CA | 58 | 17,500,881 | 63.5% | 34.3% |
| UT | 29 | 1,488,289 | 37.6% | 58.1% |
| WA | 39 | 4,087,631 | 58.4% | 38.8% |

**Verification**: These match official state-certified results.

### VCA Adoption Verification

| County | Claimed Year | Source | Verified |
|--------|--------------|--------|----------|
| Sacramento | 2018 | CA SOS | Yes |
| Los Angeles | 2020 | CA SOS | Yes |
| San Diego | 2022 | LWVC | Yes |
| Placer | 2024 | CA SOS | Yes |

---

## Limitations and Notes

### Data Gaps

1. **2022 and 2024 county-level results**: Official data requires manual download from state websites. Direct API/download access was blocked.

2. **CVAP data**: Census Bureau data not yet incorporated. Will need 2020 Census-based estimates.

3. **Party registration data**: For Democratic turnout share analysis, would need updated voter registration by party (available for CA and UT, not WA).

### Analytical Implications

1. **Limited extension scope**: With only 2020 data complete, extension analysis is limited. Can still analyze:
   - California VCA effects in 2020
   - Comparison of 2020 to original 1996-2018 period

2. **New VBM variation**: Most new variation comes from California VCA expansion (15 counties in 2020 vs. 5 in 2018).

3. **Utah and Washington saturation**: Both states are 100% VBM for the extension period, providing no new within-state variation.

---

## Data Sources Reference

| Data | Source | URL |
|------|--------|-----|
| CA VCA | CA Secretary of State | sos.ca.gov/voters-choice-act |
| 2020 Pres | GitHub/Harvard | dataverse.harvard.edu |
| 2022 CA Gov | CA SOS | sos.ca.gov/elections |
| 2024 Pres | State SOS offices | - |
| CVAP | Census Bureau | census.gov/programs-surveys/decennial-census/about/voting-rights/cvap.html |

---

## Recommendation for Extension Analysis

Given data availability, the extension analysis should:

1. **Focus on 2020**: We have complete county-level presidential data for all three states.

2. **Compare to original period**: Estimate same specifications with 2020 data appended to 1996-2018.

3. **California-specific analysis**: Examine California VCA expansion (5 → 15 counties from 2018 to 2020).

4. **Note limitations**: Acknowledge that 2022 and 2024 data collection is incomplete.

5. **Robustness**: Test sensitivity of results to including/excluding 2020 (COVID year).
