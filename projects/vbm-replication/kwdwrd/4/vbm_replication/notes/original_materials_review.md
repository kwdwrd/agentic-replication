# Original Materials Review

## Overview

This document provides a comprehensive review of the replication materials from Thompson, Wu, Yoder, and Hall (2020) "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share" (PNAS).

**Repository**: https://github.com/stanford-dpl/vbm

---

## File Inventory

### Code Files (`original/code/`)

| File | Purpose |
|------|---------|
| `prep_policy_data.do` | Creates policy/treatment data for all three states |
| `prep_analysis_data.do` | Merges all data sources into final analysis dataset |
| `prep_participation_tables.do` | Prepares participation outcome data |
| `prep_gov_data.do` | Prepares gubernatorial election data |
| `prep_pres_data.do` | Prepares presidential election data |
| `prep_sen_data.do` | Prepares senatorial election data |
| `prep_citizen_voting_age_pop.do` | Prepares CVAP denominators |
| `prep_composition_data.do` | Prepares demographic composition data |
| `prep_race_composition_data.do` | Prepares race-specific composition data |
| `prep_pov_composition_data.do` | Prepares poverty composition data |
| **`make_partisan_turnout_table.do`** | **Creates Table 2 (main partisan effects)** |
| **`make_participation_table.do`** | **Creates Table 3 (participation effects)** |
| `make_partisan_effects_state_by_state_table.do` | State-by-state robustness |
| `make_participation_table_state_by_state.do` | State-by-state participation |
| `make_participation_graphs.do` | Creates event study figures |
| `make_leads_plots.do` | Pre-treatment trend tests |
| `make_age_turnout_table.do` | Age heterogeneity analysis |
| `make_race_turnout_table.do` | Race heterogeneity analysis |
| `make_pov_turnout_table.do` | Poverty heterogeneity analysis |
| `make_composition_robustness_plots.do` | Composition robustness checks |

### Modified Data Files (`original/data/modified/`)

| File | Size | Description |
|------|------|-------------|
| `analysis.dta` | 886 KB | **Main analysis dataset** (1,454 × 134) |
| `policies.dta` | 108 KB | VBM policy adoption by county-year (2,179 × 12) |
| `participation.dta` | 132 KB | Participation outcomes |
| `governor.dta` | 59 KB | Gubernatorial election results |
| `president.dta` | 42 KB | Presidential election results |
| `senator.dta` | 23 KB | Senate election results |
| `senator_wa.dta` | 19 KB | Washington Senate results |
| `county_cvap.dta` | 1.97 MB | Citizen Voting Age Population |
| `composition.dta` | 189 KB | Voter composition data |
| `composition_race.dta` | 808 KB | Race-specific composition |
| `composition_tract.dta` | 448 KB | Tract-level composition |
| `census_ses_data.dta` | 439 KB | Census SES data |
| `ca_votes_by_group.dta` | 47.6 MB | California votes by demographic group |
| `ut_votes_by_group.dta` | 10.3 MB | Utah votes by demographic group |
| `registration.csv` | 78 KB | Voter registration data |

### Raw Data Files (`original/data/raw/`)

| Directory | Contents |
|-----------|----------|
| `policies/` | Original VBM policy sources (WA from Gerber et al. 2013, UT TSV, CA CSV) |
| `gov/` | Gubernatorial election results |
| `gov_wa/` | Washington gubernatorial results |
| `pres/` | Presidential election results |
| `pres_wa/` | Washington presidential results |
| `sen_wa/` | Washington Senate results |
| `participation/` | Participation/turnout data |
| `participation_and_results_ut/` | Utah combined data |
| `population/` | Population data for CVAP |
| `registration/` | Voter registration files |
| `eavs/` | Election Administration and Voting Survey |
| `census_poverty_race/` | Census demographic data |

---

## Main Analysis Dataset (`analysis.dta`)

### Dimensions
- **Rows**: 1,454 observations
- **Columns**: 134 variables
- **Unit of analysis**: County × Year × Election Type (general elections only)

### States and Counties
| State | Counties | Years |
|-------|----------|-------|
| California | 58 | 1998-2018 |
| Utah | 29 | 1996-2018 |
| Washington | 39 | 1996-2018 |

### Key Variables

#### Identifiers
- `state`: State abbreviation (CA, UT, WA)
- `county`: County name
- `year`: Election year (even years 1996-2018)
- `county_id`: Numeric county identifier (1-126)
- `state_year_id`: Numeric state-year identifier (1-35)
- `pres`: Indicator for presidential election year

#### Treatment Variable
- `treat`: Binary indicator = 1 if county has universal VBM in that year
  - **California**: VCA adoption in 2018 (5 counties: Madera, Napa, Nevada, Sacramento, San Mateo)
  - **Utah**: County-level adoption starting 2012, mostly 2014-2018
  - **Washington**: County-level adoption 2002-2012, all by 2012

#### Partisan Outcome Variables
- `share_votes_dem`: Democratic share of total turnout (voter registration-based)
- `dem_share_gov`: Democratic two-party vote share in gubernatorial races
- `dem_share_pres`: Democratic two-party vote share in presidential races
- `dem_share_sen`: Democratic two-party vote share in Senate races

#### Participation Outcome Variables
- `turnout_share`: Ballots cast / CVAP (citizen voting age population)
- `vbm_share`: Share of votes cast by mail (California only)
- `registered`: Registered voters
- `ballots_cast`: Total ballots cast
- `cvap`: Citizen Voting Age Population

#### Trend Variables
- `year2`: Year squared (for quadratic trends)
- `year3`: Year cubed (for cubic trends)

---

## Treatment Assignment Details

### California
- **VCA (Voter's Choice Act)**: Adopted by 5 counties in 2018
  - Madera, Napa, Nevada, Sacramento, San Mateo
  - These counties switched from traditional polling places to vote centers + automatic VBM
- Additional counties eligible but did not adopt in 2018: Calaveras, Inyo, Orange, San Luis Obispo, Santa Clara, Shasta, Sierra, Sutter, Tuolumne
- VCA 2020 adopters recorded in data: Amador, Butte, El Dorado, Fresno, Los Angeles, Mariposa, Orange, Santa Clara, Tuolumne

### Utah
- **Progressive rollout**: 2012-2020
  - 2012: 1 county (Duchesne)
  - 2014: 9 counties
  - 2016: 11 counties
  - 2018: 6 counties
  - 2020: 2 counties (Carbon, Emery - not in analysis timeframe)

### Washington
- **Near-complete by 2006**: 29 counties adopted in 2006
  - 2002: 1 county (Clallam)
  - 2004: 3 counties
  - 2006: 29 counties
  - 2008: 3 counties
  - 2010: 1 county (King County)
- 2 counties show switch_year=0 (Ferry, Pierce) - never-treated or always-treated

---

## Main Analysis Workflow

### Table 2 (Partisan Outcomes) - `make_partisan_turnout_table.do`

**Outcome 1: Democratic Turnout Share (Columns 1-3)**
```stata
// Column 1: Basic DiD
reghdfe share_votes_dem treat, a(county_id state_year) vce(clust county_id)

// Column 2: Linear trends
reghdfe share_votes_dem treat, a(county_id county_id##c.year state_year) vce(clust county_id)

// Column 3: Quadratic trends
reghdfe share_votes_dem treat, a(county_id##c.year county_id##c.year2 state_year) vce(clust county_id)
```

**Outcome 2: Democratic Vote Share (Columns 4-6)**
- Reshapes data to have one row per county-year-office (governor, president, senator)
- Same three specifications as above with `dem_share` as outcome

### Table 3 (Participation Outcomes) - `make_participation_table.do`

**Outcome 1: Turnout (Columns 1-3)**
```stata
// Same three specifications with turnout_share as outcome
reghdfe turnout_share treat, a(county_id state_year) vce(clust county_id)
```

**Outcome 2: VBM Share (Columns 4-6)**
```stata
// California only (VBM share not available for UT/WA)
reghdfe vbm_share treat if state=="CA", a(county_id state_year) vce(clust county_id)
```

---

## Stata Commands Requiring Python Translation

| Stata Command | Purpose | Python Equivalent |
|--------------|---------|-------------------|
| `reghdfe` | High-dimensional fixed effects regression | `linearmodels.PanelOLS` or `pyhdfe` |
| `a(county_id state_year)` | Absorb county and state-year FE | Entity and time effects in panel model |
| `a(county_id##c.year)` | Absorb county FE + county-specific linear trends | Need to construct interaction manually |
| `a(county_id##c.year county_id##c.year2)` | Add quadratic trends | Construct year² interaction |
| `vce(clust county_id)` | Cluster SEs at county level | `cov_type='clustered'` |
| `distinct` | Count unique values | `pd.Series.nunique()` |
| `reshape long` | Wide to long transformation | `pd.melt()` or `pd.wide_to_long()` |

### Key Translation Notes

1. **Fixed Effects with Trends**: The `county_id##c.year` syntax creates county-specific slopes on the continuous year variable. In Python, this requires:
   - Creating interaction terms: `county_id * year`
   - Using within-group demeaning or including as regressors

2. **State-Year Fixed Effects**: These are not time fixed effects in the traditional panel sense - they are state×year interactions. Need to:
   - Create dummy variables for each state-year combination, OR
   - Include as additional absorbed fixed effects

3. **Clustered Standard Errors**: Use `cov_type='clustered', cluster_entity=True` in linearmodels, or manually specify clusters.

4. **Sample Restrictions**: Table 2 columns 1-3 use CA and UT only (WA lacks partisan turnout data); columns 4-6 use all states. Table 3 columns 4-6 use CA only (VBM share data).

---

## Data Quality Notes

### Missing Data Patterns
- `turnout_share`: 14.7% missing (214 obs)
- `vbm_share`: 38.7% missing (562 obs) - Utah has no VBM share data
- `share_votes_dem`: 32.2% missing (468 obs) - Washington lacks this variable
- `dem_share_gov`: 48.0% missing - not all years have gubernatorial elections
- `dem_share_pres`: 52.0% missing - only presidential years
- `dem_share_sen`: 62.6% missing - not all years/states have Senate races

### Variable Ranges
- `turnout_share`: 0.22 - 0.93 (mean 0.54)
- `vbm_share`: 0.01 - 1.00 (mean 0.58)
- `share_votes_dem`: 0.02 - 0.66 (mean 0.28)
- `dem_share_gov/pres/sen`: 0.07 - 0.90 (means ~0.38-0.43)

---

## Extension Requirements

To extend this analysis through 2024, need to collect:

1. **California**:
   - VCA adoption for 2020, 2022, 2024 (which additional counties?)
   - Election results for 2020 (presidential), 2022 (gubernatorial), 2024 (presidential)
   - Updated CVAP data

2. **Utah**:
   - By 2019, essentially all counties were VBM (limited new variation)
   - Election results for 2020, 2022, 2024

3. **Washington**:
   - 100% VBM since 2011 (no new variation)
   - Election results for 2020, 2022, 2024

4. **Note**: The extension will primarily leverage California's continued VCA rollout, as Utah and Washington provide no new treatment variation post-2018.
