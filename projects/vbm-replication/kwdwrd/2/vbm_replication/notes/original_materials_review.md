# Original Replication Materials Review

## 1. File Inventory

### Code Files (`original/code/`)

**Main Analysis Scripts (Tables 2 and 3):**
- `make_partisan_turnout_table.do` - Produces Table 2 (partisan outcomes)
- `make_participation_table.do` - Produces Table 3 (participation outcomes)

**Data Preparation Scripts:**
- `prep_analysis_data.do` - Merges all data sources into main analysis dataset
- `prep_policy_data.do` - Prepares VBM policy adoption data for CA, UT, WA
- `prep_gov_data.do` - Prepares gubernatorial election results
- `prep_pres_data.do` - Prepares presidential election results
- `prep_participation_tables.do` - Prepares participation metrics
- `prep_citizen_voting_age_pop.do` - Prepares CVAP data
- `prep_composition_data.do` - Prepares voter composition data

**Additional Analysis Scripts:**
- `make_partisan_effects_state_by_state_table.do` - State-specific results
- `make_participation_table_state_by_state.do` - State-specific participation
- `make_leads_plots.do` - Creates event study plots
- `make_age_turnout_table.do` - Age-specific analysis
- `make_race_turnout_table.do` - Race-specific analysis
- `make_pov_turnout_table.do` - Poverty-specific analysis

### Modified Data Files (`original/data/modified/`)

| File | Description | Rows | Columns |
|------|-------------|------|---------|
| `analysis.dta` | Main analysis dataset | 1,454 | 134 |
| `policies.dta` | VBM policy adoption dates | 2,179 | 12 |
| `participation.dta` | Turnout and VBM usage | 1,240 | 17 |
| `governor.dta` | Gubernatorial results | - | - |
| `president.dta` | Presidential results | - | - |
| `senator.dta` | Senatorial results | - | - |
| `county_cvap.dta` | Citizen voting age population | - | - |
| `composition.dta` | Voter composition data | - | - |

### Raw Data Files (`original/data/raw/`)

**Policy Data:**
- `policies/VBM Policies - policies.csv` - California VCA adoption (58 counties)
- `policies/utah_counties_vbm_switch.tsv` - Utah VBM adoption dates (29 counties)
- `policies/WA-County-VotesCast.csv` - Washington VBM data from Gerber, Huber, and Hill (2013)

**Election Data:**
- `gov/` - Gubernatorial election results
- `pres/` - Presidential election results
- `sen_wa/` - Washington senatorial results
- `participation_and_results_ut/` - Utah participation data
- `participation/` - Participation/turnout data

**Population Data:**
- `population/` - CVAP data by county
- `census_poverty_race/` - Census demographic data

## 2. Main Analysis Workflow

### Data Preparation Pipeline:
1. `prep_policy_data.do`: Creates treatment variable from VBM adoption dates
2. `prep_participation_tables.do`: Merges turnout, VBM share data
3. `prep_gov_data.do`, `prep_pres_data.do`: Merge election results
4. `prep_analysis_data.do`: Combines all sources, creates final analysis dataset

### Analysis Workflow:
1. Load `analysis.dta`
2. Run regressions with `reghdfe` command
3. Store coefficients and standard errors
4. Output formatted LaTeX tables

## 3. Key Variable Definitions

### Identification Variables:
- `state`: State abbreviation (CA, UT, WA)
- `county`: County name
- `year`: Election year (1996-2018 in original)
- `county_id`: Numeric county identifier for fixed effects
- `state_year`: State-year interaction for fixed effects

### Treatment Variable:
- `treat`: = 1 if county has universal VBM in effect, 0 otherwise
  - **California**: Based on Voter's Choice Act (VCA) adoption
    - 2018: 5 counties (Madera, Napa, Nevada, Sacramento, San Mateo)
  - **Utah**: Based on county-level all-mail adoption
    - Staggered 2012-2018 (27 of 29 counties by 2018)
  - **Washington**: Based on county-level VBM-only adoption
    - Mostly 2006 (29 counties), others 1996-2012

### Outcome Variables:
- `share_votes_dem`: Democratic share of total votes cast (party registration turnout measure)
- `dem_share_gov`: Democratic two-party vote share in gubernatorial elections
- `dem_share_pres`: Democratic two-party vote share in presidential elections
- `dem_share_sen`: Democratic two-party vote share in senatorial elections
- `turnout_share`: Total ballots cast / CVAP
- `vbm_share`: Share of votes cast by mail

### Control Variables:
- `year2`: year^2 (for quadratic trends)
- `year3`: year^3

## 4. Stata Commands and Python Equivalents

### Main Regression Command:

**Stata `reghdfe`:**
```stata
reghdfe share_votes_dem treat, ///
    a(county_id state_year) vce(clust county_id)
```

**Python equivalent using `linearmodels`:**
```python
from linearmodels.panel import PanelOLS
import pandas as pd

# Set multi-index for panel data
df = df.set_index(['county_id', 'year'])

# Basic specification
model = PanelOLS(
    dependent=df['share_votes_dem'],
    exog=df[['treat']],
    entity_effects=True,  # county_id FE
    time_effects=True     # Need to handle state_year differently
)
result = model.fit(cov_type='clustered', cluster_entity=True)
```

**Note on state_year fixed effects:**
The original uses `state_year` which is state×year interaction. This is NOT simple time fixed effects. Implementation options:
1. Create dummy variables for each state-year
2. Use formula-based approach with `statsmodels`
3. Manually demean by state-year

### Specifications Summary:

| Column | Fixed Effects | County Trends |
|--------|---------------|---------------|
| 1/4 | county_id, state_year | None |
| 2/5 | county_id, state_year | Linear (county×year) |
| 3/6 | county_id, state_year | Quadratic (county×year, county×year²) |

### Python Package Requirements:
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `statsmodels` - Regression analysis
- `linearmodels` - Panel data with high-dimensional FE
- `scipy` - Statistical tests

## 5. Data Structure Summary

### Sample Coverage:
- **States**: California (58 counties), Utah (29 counties), Washington (39 counties)
- **Total counties**: 126
- **Years**: 1996-2018 (general elections only, even years)
- **Observations**: 1,454 county-year observations

### Treatment Timing:
- **California**: 5 counties treated in 2018 only (VCA)
- **Utah**: Staggered 2012-2018 (27 counties by 2018)
- **Washington**: Mostly 2006, some earlier/later (all treated by 2012)

### Key Variation:
- Most variation comes from Washington (staggered 1996-2012)
- Utah provides additional staggered variation (2012-2018)
- California provides limited variation (only 5 counties in 2018)

## 6. Notes for Replication

1. **Dem turnout share** (Table 2, cols 1-3) only uses CA and UT (87 counties) because WA lacks party registration data

2. **VBM share** (Table 3, cols 4-6) only uses CA (58 counties) because UT and WA are 100% VBM by design

3. **Standard errors** are clustered at county level in all specifications

4. The paper uses `reghdfe` which efficiently handles high-dimensional fixed effects. Python alternatives:
   - `linearmodels.PanelOLS` with `absorb` parameter
   - Manual demeaning approach
   - `pyhdfe` package

5. For the extension, need to collect:
   - California VCA adoption through 2024
   - Election results 2020-2024 for all three states
   - Updated CVAP from 2020 Census
