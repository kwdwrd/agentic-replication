# Original Materials Review

## Repository Information
- **Source**: https://github.com/stanford-dpl/vbm
- **Paper**: Thompson, Wu, Yoder, and Hall (2020), "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share", PNAS

---

## File Inventory

### 1. Code Files (`original/code/`)

Total: 29 Stata .do files

#### Data Preparation Scripts:
| File | Purpose |
|------|---------|
| `prep_analysis_data.do` | Creates main analysis dataset by merging policy, participation, and election outcome data |
| `prep_policy_data.do` | Creates VBM treatment indicators for CA, UT, WA |
| `prep_participation_tables.do` | Prepares participation variables |
| `prep_gov_data.do` | Prepares gubernatorial election results |
| `prep_pres_data.do` | Prepares presidential election results |
| `prep_sen_data.do` | Prepares senatorial election results |
| `prep_citizen_voting_age_pop.do` | Prepares CVAP denominators for turnout |
| `prep_composition_data.do` | Prepares voter composition variables |
| `prep_composition_robustness_data.do` | Additional composition measures |
| `prep_pov_census_data.do` | Census poverty data |
| `prep_pov_composition_data.do` | Poverty composition analysis |
| `prep_race_composition_data.do` | Race composition analysis |

#### Main Analysis Scripts:
| File | Purpose | Output |
|------|---------|--------|
| `make_partisan_turnout_table.do` | **Table 2: Partisan outcomes** | partisan_effects_table.tex |
| `make_participation_table.do` | **Table 3: Participation outcomes** | participation_table.tex |
| `make_partisan_effects_state_by_state_table.do` | State-specific partisan effects | |
| `make_participation_table_state_by_state.do` | State-specific participation | |

#### Robustness and Additional Tables:
| File | Purpose |
|------|---------|
| `make_partisan_turnout_table_ca_and_ut.do` | CA and UT specific analysis |
| `make_republican_partisan_turnout_table.do` | Republican turnout analysis |
| `make_age_turnout_table.do` | Age group effects |
| `make_pov_turnout_table.do` | Poverty heterogeneity |
| `make_race_turnout_table.do` | Race heterogeneity |
| `make_participation_descriptives.do` | Descriptive statistics |
| `make_participation_graphs.do` | Event study/dynamic effects plots |
| `make_leads_plots.do` | Lead coefficient plots |
| `make_composition_robustness_plots.do` | Composition robustness figures |
| `make_pov_composition_robustness_figure.do` | Poverty robustness |
| `make_race_composition_robustness_figure.do` | Race robustness |
| `make_statewide_vote_shares_by_vbm.do` | State-level descriptives |

### 2. Modified/Analysis Data Files (`original/data/modified/`)

Total: 24 files

#### Main Analysis Dataset:
| File | Rows | Columns | Description |
|------|------|---------|-------------|
| `analysis.dta` | 1,454 | 134 | Main analysis dataset (county-year level, 1996-2018) |

#### Supporting Datasets:
| File | Description |
|------|-------------|
| `policies.dta` | VBM policy adoption dates by county |
| `participation.dta` | Turnout and VBM share variables |
| `governor.dta` | Gubernatorial election results |
| `president.dta` | Presidential election results |
| `senator.dta` | Senate election results |
| `senator_wa.dta` | Washington-specific Senate data |
| `composition.dta` | Voter composition by party |
| `composition_race.dta` | Voter composition by race |
| `composition_tract.dta` | Census tract level composition |
| `composition_age_robustness.dta` | Age composition robustness |
| `county_cvap.dta` | Citizen Voting Age Population |
| `county_voting_age_pop.dta` | Voting age population estimates |
| `census_ses_data.dta` | Census SES data |
| `ca_votes_by_group.dta` | California votes by demographic group |
| `ca_votes_by_tract.dta` | California tract-level votes |
| `ut_votes_by_group.dta` | Utah votes by demographic group |
| `ut_votes_by_tract.dta` | Utah tract-level votes |
| `us_election_results.dta` | Broader election results |
| `vote_share_analysis_for_traj_bal.dta` | Trajectory balance analysis |
| `registration.csv` | Voter registration data |
| `matched_counties_drutman.csv` | Matched counties for robustness |
| `wa_preselec.csv` | Washington pre-election data |

### 3. Original/Raw Data Files (`original/data/raw/`)

Contains subdirectories:
- `census_poverty_race/` - Census Bureau poverty and race data
- `eavs/` - Election Administration and Voting Survey
- `gov/` - Gubernatorial election results
- `gov_wa/` - Washington gubernatorial results
- `participation/` - Turnout and voting method data
- `participation_and_results_ut/` - Utah participation data
- `policies/` - VBM policy adoption records
- `population/` - Census population data
- `pres/` - Presidential election results
- `pres_wa/` - Washington presidential results
- `registration/` - Voter registration files
- `sen_wa/` - Washington Senate results

---

## Main Analysis Dataset Structure (`analysis.dta`)

### Dimensions
- **Observations**: 1,454 county-year observations
- **Variables**: 134 columns
- **Unit of Analysis**: County × Year (even years only, general elections)

### Geographic Coverage
| State | Counties | Years | Observations |
|-------|----------|-------|--------------|
| California (CA) | 58 | 1998-2018 | 638 |
| Utah (UT) | 29 | 1996-2018 | 348 |
| Washington (WA) | 39 | 1996-2018 | 468 |
| **Total** | **126** | | **1,454** |

### Key Variables

#### Identifiers:
| Variable | Type | Description |
|----------|------|-------------|
| `state` | string | State abbreviation (CA, UT, WA) |
| `county` | string | County name |
| `year` | integer | Election year (even years, 1996-2018) |
| `county_id` | integer | Numeric county identifier (1-126) |
| `state_year_id` | integer | State-year fixed effect identifier |

#### Treatment:
| Variable | Type | Description |
|----------|------|-------------|
| `treat` | binary | =1 if county has universal VBM in that year |
| `vca18` | binary | =1 if CA county adopted VCA in 2018 |
| `vca20` | binary | =1 if CA county adopted VCA in 2020 |
| `all_mail2006` | binary | =1 if WA county adopted all-mail in 2006 |
| `ut_all_mail_year` | integer | Year UT county adopted all-mail |
| `switch_year` | integer | Year county switched to VBM |

#### Outcome Variables - Partisan:
| Variable | Type | Description |
|----------|------|-------------|
| `share_votes_dem` | continuous [0,1] | Democratic share of voters (from voter file) |
| `dem_share_gov` | continuous [0,1] | Democratic two-party vote share in gubernatorial |
| `dem_share_pres` | continuous [0,1] | Democratic two-party vote share in presidential |
| `dem_share_sen` | continuous [0,1] | Democratic two-party vote share in Senate |

#### Outcome Variables - Participation:
| Variable | Type | Description |
|----------|------|-------------|
| `turnout_share` | continuous [0,1] | Ballots cast / CVAP |
| `vbm_share` | continuous [0,1] | Share of votes cast by mail |
| `ballots_cast` | integer | Total ballots cast |
| `cvap` | integer | Citizen Voting Age Population |

#### Controls/Trend Variables:
| Variable | Type | Description |
|----------|------|-------------|
| `year2` | continuous | year^2 (for quadratic trends) |
| `year3` | continuous | year^3 (for cubic trends) |

### Treatment Variation Summary

| State | N Obs with treat=0 | N Obs with treat=1 | Treatment Source |
|-------|-------------------|-------------------|------------------|
| CA | 633 | 5 | VCA 2018: 5 counties (Madera, Napa, Nevada, Sacramento, San Mateo) |
| UT | 289 | 59 | Staggered adoption 2004-2019 |
| WA | 193 | 275 | Staggered adoption 2005-2011 (100% by 2011) |

### Missing Data Summary

| Variable | Missing | Total | % Missing |
|----------|---------|-------|-----------|
| `share_votes_dem` | 468 | 1,454 | 32.2% |
| `dem_share_gov` | 698 | 1,454 | 48.0% |
| `dem_share_pres` | 756 | 1,454 | 52.0% |
| `dem_share_sen` | 910 | 1,454 | 62.6% |
| `turnout_share` | 214 | 1,454 | 14.7% |
| `vbm_share` | 562 | 1,454 | 38.7% |

Note: Missing values in partisan outcomes are structural - not all states have all election types in all years (e.g., presidential elections only in years divisible by 4).

---

## Main Analysis Workflow

### Table 2: Partisan Outcomes
**Script**: `make_partisan_turnout_table.do`

**Columns 1-3 (Democratic Turnout Share)**:
- Uses `share_votes_dem` as outcome
- Sample: CA and UT only (87 counties with voter file data)

**Columns 4-6 (Democratic Vote Share)**:
- Reshapes data to county-year-office level
- Uses `dem_share_gov`, `dem_share_pres`, `dem_share_sen`
- Sample: All three states (126 counties)

**Specifications**:
1. Basic: County FE + State×Year FE
2. Linear trends: + County×Year interaction
3. Quadratic trends: + County×Year² interaction

### Table 3: Participation Outcomes
**Script**: `make_participation_table.do`

**Columns 1-3 (Turnout)**:
- Uses `turnout_share` as outcome
- Sample: All three states

**Columns 4-6 (VBM Share)**:
- Uses `vbm_share` as outcome
- Sample: California only (58 counties)

---

## Stata Commands and Their Python Equivalents

### Core Regression Command: `reghdfe`

Stata syntax:
```stata
reghdfe outcome treat, a(county_id state_year) vce(clust county_id)
```

**Python equivalent options**:

1. **Using `linearmodels.PanelOLS`**:
```python
from linearmodels.panel import PanelOLS
# Requires panel data structure with multi-index
model = PanelOLS.from_formula('outcome ~ 1 + treat + EntityEffects + TimeEffects', data=panel_df)
result = model.fit(cov_type='clustered', cluster_entity=True)
```

2. **Using `statsmodels` with manual dummies**:
```python
import statsmodels.api as sm
# Create dummy variables for fixed effects
# Use robust clustered standard errors
model = sm.OLS(y, X).fit(cov_type='cluster', cov_kwds={'groups': county_id})
```

3. **Using `fixedeffect` package** (if available):
```python
# Direct implementation of high-dimensional fixed effects
```

### Key Translation Table

| Stata | Python Package | Python Syntax | Notes |
|-------|---------------|---------------|-------|
| `reghdfe Y X, a(fe1 fe2)` | `linearmodels` | `PanelOLS.from_formula('Y ~ X + EntityEffects')` | Need to create state_year dummies separately |
| `vce(cluster id)` | `linearmodels` | `.fit(cov_type='clustered', cluster_entity=True)` | |
| `a(county_id##c.year)` | Manual | Create county×year interaction terms | Linear trends |
| `a(county_id##c.year2)` | Manual | Create county×year² interaction terms | Quadratic trends |
| `distinct var` | `pandas` | `df[var].nunique()` | Count unique values |
| `egen group()` | `pandas` | `df.groupby().ngroup()` | Create group IDs |

### Special Considerations

1. **State×Year Fixed Effects**: The `state_year_id` variable already exists in the data
2. **County Trends**: Need to create `county_id × year` and `county_id × year²` interactions
3. **Clustered SEs**: Must cluster at county level (126 clusters)
4. **Sample Restrictions**:
   - Table 2 cols 1-3: CA and UT only (no WA partisan voter file)
   - Table 3 cols 4-6: CA only (VBM share data)

---

## Data Sources (from original code documentation)

1. **VBM Policy Data**:
   - California: Authors' coding from CA SOS records
   - Utah: Authors' manual collection
   - Washington: Gerber, Huber, and Hill (2013) replication data

2. **Election Results**:
   - MIT Election Data + Science Lab
   - State Secretary of State offices
   - Dave Leip's Atlas

3. **Voter File Data (for composition)**:
   - California: Statewide voter file
   - Utah: Statewide voter file
   - Washington: Not available (hence missing `share_votes_dem` for WA)

4. **Population/CVAP**:
   - Census Bureau CVAP estimates
   - American Community Survey

---

## Notes for Replication

1. **Package Requirements**: The original code uses Stata's `reghdfe` package (Correia 2016), which handles high-dimensional fixed effects efficiently. Python equivalent requires careful implementation.

2. **Standard Error Clustering**: Always cluster at county level (not state-year).

3. **Sample Sizes**:
   - Table 2 cols 1-3: N ≈ 520 (CA + UT with voter file data)
   - Table 2 cols 4-6: N ≈ 1,400+ (all states, multiple office types per year)
   - Table 3 cols 1-3: N ≈ 1,240 (all states)
   - Table 3 cols 4-6: N ≈ 580 (CA only, with VBM share)

4. **Data Quality**: Check for:
   - Outliers in vote shares (should be [0,1])
   - Implausible turnout rates (>100%)
   - Missing CVAP values

---

## Extension Data Requirements

To extend through 2024, we need:

1. **California**:
   - VCA adoption: Which counties joined after 2018?
   - Election results: 2020 primary (presidential), 2020 general, 2021 recall, 2022 general, 2024 general
   - CVAP: 2020 Census-based estimates

2. **Utah**:
   - Already 100% VBM by 2019 (no new variation)
   - Election results: 2020, 2022, 2024
   - CVAP updates

3. **Washington**:
   - Already 100% VBM since 2011 (no new variation)
   - Election results: 2020, 2022, 2024
   - CVAP updates

**Key extension insight**: The extension will primarily test whether California's continued VCA rollout shows similar null effects in the post-2020 period.
