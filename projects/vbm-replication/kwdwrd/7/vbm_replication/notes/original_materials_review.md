# Original Materials Review

## Overview

This document reviews the replication materials from Thompson, Wu, Yoder, and Hall (2020), "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share," published in PNAS.

**Repository source**: https://github.com/stanford-dpl/vbm

---

## 1. File Inventory

### 1.1 Code Files (original/code/)

| File | Purpose |
|------|---------|
| `prep_policy_data.do` | Creates treatment (VBM) indicators by county-year |
| `prep_analysis_data.do` | Merges all datasets into final analysis file |
| `prep_participation_tables.do` | Prepares participation data |
| `prep_gov_data.do` | Prepares gubernatorial election data |
| `prep_pres_data.do` | Prepares presidential election data |
| `prep_sen_data.do` | Prepares senatorial election data |
| `prep_citizen_voting_age_pop.do` | Prepares CVAP denominator data |
| `prep_composition_data.do` | Prepares voter composition data |
| **`make_partisan_turnout_table.do`** | **Creates Table 2 (partisan outcomes)** |
| **`make_participation_table.do`** | **Creates Table 3 (participation outcomes)** |
| `make_partisan_effects_state_by_state_table.do` | State-by-state robustness |
| `make_participation_table_state_by_state.do` | State-by-state participation |
| `make_leads_plots.do` | Creates event study plots |
| Other `make_*.do` files | Additional tables and figures |

### 1.2 Modified/Analysis Data Files (original/data/modified/)

| File | Rows | Cols | Description |
|------|------|------|-------------|
| **`analysis.dta`** | 1,454 | 134 | **Main analysis dataset** |
| `policies.dta` | 2,179 | 12 | VBM policy coding by county-year |
| `participation.dta` | 1,240 | 17 | Turnout and VBM share data |
| `governor.dta` | 1,317 | 7 | Gubernatorial election results |
| `president.dta` | 911 | 7 | Presidential election results |
| `senator.dta` | 544 | 5 | Senate election results |
| `senator_wa.dta` | 427 | 5 | Washington senate results |
| `county_cvap.dta` | 41,808 | 6 | Citizen voting age population |
| `composition.dta` | 2,798 | 13 | Voter composition by party |
| `ca_votes_by_group.dta` | 767,695 | 5 | CA votes by demographic group |
| `ut_votes_by_group.dta` | 174,952 | 5 | UT votes by demographic group |

### 1.3 Original/Raw Data Files (original/data/raw/)

| Folder | Contents |
|--------|----------|
| `policies/` | VBM policy data (CSV) including CA VCA adoption |
| `gov/` | Gubernatorial election results (CA, UT) |
| `gov_wa/` | Washington gubernatorial results |
| `pres/` | Presidential election results |
| `pres_wa/` | Washington presidential results |
| `sen_wa/` | Washington senate results |
| `participation/` | Turnout and VBM usage data |
| `participation_and_results_ut/` | Utah combined data |
| `population/` | Census population data |
| `eavs/` | Election Administration and Voting Survey data |
| `registration/` | Voter registration data (PDFs and CSVs) |
| `census_poverty_race/` | Census demographic data |

---

## 2. Main Analysis Workflow

### 2.1 Data Preparation Flow

```
1. prep_policy_data.do
   - Creates VBM treatment indicator by state-county-year
   - CA: VCA adoption (2018: 5 counties; 2020: 15 counties)
   - UT: Staggered adoption (2012-2020)
   - WA: Staggered adoption (2006-2011, 100% by 2011)

2. prep_participation_tables.do
   - Merges turnout data
   - Calculates turnout_share = ballots_cast / cvap
   - Calculates vbm_share = vbm / ballots_cast

3. prep_gov_data.do, prep_pres_data.do, prep_sen_data.do
   - Calculate dem_share = dem_votes / (dem_votes + rep_votes)

4. prep_composition_data.do
   - Calculates share_votes_dem = dem_voters / total_voters

5. prep_analysis_data.do
   - Merges all datasets
   - Creates fixed effect IDs (county_id, state_year_id)
   - Creates trend variables (year2 = year^2)
   - Filters to year < 2020
```

### 2.2 Analysis Flow (Tables 2 & 3)

```
make_partisan_turnout_table.do (Table 2):
   - Outcome 1: share_votes_dem (Dem turnout share) - CA & UT only
   - Outcome 2: dem_share (Dem two-party vote share) - all states
   - 3 specifications each: basic, linear trends, quadratic trends

make_participation_table.do (Table 3):
   - Outcome 1: turnout_share - all states
   - Outcome 2: vbm_share - CA only
   - 3 specifications each
```

---

## 3. Key Variable Definitions

### 3.1 Treatment Variable

| Variable | Definition |
|----------|------------|
| `treat` | =1 if universal VBM in effect for that county-year |

**California**: `treat = 1` if county adopted Voter's Choice Act (VCA)
- 2018: Madera, Napa, Nevada, Sacramento, San Mateo (5 counties)
- 2020: Additional 10 counties joined (15 total)

**Utah**: `treat = 1` if year >= `ut_all_mail_year`
- Staggered adoption 2012-2020 across 29 counties

**Washington**: `treat = 1` if year >= `switch_year`
- 29 counties switched in 2006
- Remaining 10 counties by 2011
- 100% VBM statewide by 2011

### 3.2 Outcome Variables

| Variable | Definition | Sample |
|----------|------------|--------|
| `share_votes_dem` | Democratic share of total voters | CA, UT |
| `dem_share_gov` | Dem / (Dem + Rep) in governor race | CA, UT, WA |
| `dem_share_pres` | Dem / (Dem + Rep) in presidential race | CA, UT, WA |
| `dem_share_sen` | Dem / (Dem + Rep) in senate race | WA |
| `turnout_share` | Total ballots / CVAP | CA, UT, WA |
| `vbm_share` | VBM ballots / Total ballots | CA only |

### 3.3 Fixed Effects Variables

| Variable | Definition |
|----------|------------|
| `county_id` | Unique county identifier (1-126) |
| `state_year` | State × Year combination |
| `year` | Election year |
| `year2` | year^2 (for quadratic trends) |

---

## 4. Sample Characteristics

### 4.1 Geographic Coverage

| State | Counties | Years | Observations |
|-------|----------|-------|--------------|
| California | 58 | 1996-2018 | 638 |
| Utah | 29 | 1996-2018 | 348 |
| Washington | 39 | 1996-2018 | 468 |
| **Total** | **126** | **12 elections** | **1,454** |

### 4.2 Treatment Variation

| State | Treated Obs | % Treated | Treatment Timing |
|-------|-------------|-----------|------------------|
| California | 5 | 0.8% | 2018 only (VCA) |
| Utah | 59 | 17.0% | Staggered 2012-2018 |
| Washington | 275 | 58.8% | Staggered 2006-2011 |

### 4.3 Missing Data

| Variable | Missing | Notes |
|----------|---------|-------|
| `share_votes_dem` | 468 | WA not available |
| `dem_share_gov` | 698 | Not all state-years |
| `dem_share_pres` | 756 | Presidential years only |
| `turnout_share` | 214 | Some county-years missing |
| `vbm_share` | 562 | CA only |
| `cvap` | 718 | Some years missing |

---

## 5. Stata Commands Used

### 5.1 Main Regression Command

```stata
reghdfe outcome treat, absorb(fixed_effects) vce(cluster county_id)
```

**`reghdfe`** is a Stata package for high-dimensional fixed effects regression.

### 5.2 Specification Details

**Specification 1: Basic**
```stata
reghdfe Y treat, a(county_id state_year) vce(clust county_id)
```

**Specification 2: Linear County Trends**
```stata
reghdfe Y treat, a(county_id county_id##c.year state_year) vce(clust county_id)
```

**Specification 3: Quadratic County Trends**
```stata
reghdfe Y treat, a(county_id##c.year county_id##c.year2 state_year) vce(clust county_id)
```

### 5.3 Key Stata Syntax

| Stata | Meaning |
|-------|---------|
| `a()` / `absorb()` | Fixed effects to absorb (demean) |
| `county_id##c.year` | County-specific linear time trend |
| `vce(clust county_id)` | Cluster standard errors by county |
| `distinct` | Count unique values |

---

## 6. Python Translation Plan

### 6.1 Required Packages

| Stata | Python Equivalent |
|-------|-------------------|
| `reghdfe` | `linearmodels.PanelOLS` or custom implementation |
| `cluster()` | `cov_type='clustered'` parameter |
| `absorb()` | `entity_effects=True`, `time_effects=True` |

### 6.2 Implementation Approach

**Option A: linearmodels package**
```python
from linearmodels.panel import PanelOLS

# Set index for panel structure
data = data.set_index(['county_id', 'state_year'])

# Basic specification
mod = PanelOLS(data['outcome'], data[['treat']],
               entity_effects=True, time_effects=True)
result = mod.fit(cov_type='clustered', cluster_entity=True)
```

**Option B: statsmodels with dummy variables**
```python
import statsmodels.formula.api as smf

# Create dummies manually
formula = 'outcome ~ treat + C(county_id) + C(state_year)'
mod = smf.ols(formula, data=data).fit(cov_type='cluster',
                                       cov_kwds={'groups': data['county_id']})
```

**Challenge: County-specific time trends**
- Stata's `county_id##c.year` creates county-specific slopes
- In Python, need to create interaction terms manually or use specialized packages

### 6.3 Alternative: PyFixest

The `pyfixest` package provides Stata-like syntax for high-dimensional fixed effects:
```python
import pyfixest as pf
result = pf.feols('outcome ~ treat | county_id + state_year',
                  data=data, vcov={'CRV1': 'county_id'})
```

---

## 7. Notes and Caveats

1. **Data filtering**: Original analysis uses `keep if year < 2020` - the 2020 data is collected but not used

2. **Partial observability**:
   - `share_votes_dem` (partisan turnout) only available for CA and UT
   - `vbm_share` only available for CA

3. **Treatment timing**:
   - California has very limited treatment variation in the original period (only 2018)
   - Washington had no new variation after 2011
   - Utah provides the most staggered variation

4. **Trend specifications**: The quadratic trend models can be computationally intensive with many county-specific trends

5. **Standard errors**: All specifications cluster at the county level (126 clusters)
