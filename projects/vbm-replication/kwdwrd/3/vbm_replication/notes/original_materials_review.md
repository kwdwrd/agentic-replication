# Original Materials Review

## Repository Information

- **Source**: https://github.com/stanford-dpl/vbm
- **Authors**: Thompson, Wu, Yoder, and Hall (2020)
- **Paper**: "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share"

## File Inventory

### Code Files (original/code/)

#### Main Analysis Scripts (Tables 2 and 3)
| File | Description |
|------|-------------|
| `make_partisan_turnout_table.do` | **Table 2**: Partisan outcomes (Dem turnout share, Dem vote share) |
| `make_participation_table.do` | **Table 3**: Participation outcomes (turnout, VBM share) |

#### Supporting Analysis Scripts
| File | Description |
|------|-------------|
| `make_participation_table_state_by_state.do` | State-specific participation results |
| `make_partisan_effects_state_by_state_table.do` | State-specific partisan effects |
| `make_partisan_turnout_table_ca_and_ut.do` | CA and UT specific analysis |
| `make_republican_partisan_turnout_table.do` | Republican turnout analysis |
| `make_age_turnout_table.do` | Age-specific turnout effects |
| `make_pov_turnout_table.do` | Poverty-specific turnout effects |
| `make_race_turnout_table.do` | Race-specific turnout effects |
| `make_leads_plots.do` | Pre-treatment leads/lags event study |
| `make_participation_graphs.do` | Visual participation trends |
| `make_composition_robustness_plots.do` | Composition robustness checks |
| `make_statewide_vote_shares_by_vbm.do` | Statewide vote share calculations |

#### Data Preparation Scripts
| File | Description |
|------|-------------|
| `prep_analysis_data.do` | Master file creating analysis.dta |
| `prep_policy_data.do` | VBM policy adoption dates |
| `prep_participation_tables.do` | Participation variables |
| `prep_gov_data.do` | Gubernatorial election data |
| `prep_pres_data.do` | Presidential election data |
| `prep_sen_data.do` | Senatorial election data |
| `prep_citizen_voting_age_pop.do` | CVAP data |
| `prep_composition_data.do` | Voter composition data |

### Modified Data Files (original/data/modified/)

#### Main Analysis Dataset
| File | Dimensions | Description |
|------|------------|-------------|
| `analysis.dta` | 1,454 × 134 | Main analysis dataset (general elections only) |

#### Component Datasets
| File | Dimensions | Description |
|------|------------|-------------|
| `policies.dta` | 2,179 × 12 | VBM adoption policies by county-year |
| `participation.dta` | 1,240 × 17 | Turnout and VBM share data |
| `governor.dta` | 1,317 × 7 | Gubernatorial election results |
| `president.dta` | 911 × 7 | Presidential election results |
| `senator.dta` | 544 × 5 | Senatorial election results |
| `composition.dta` | - | Voter composition by party |
| `county_cvap.dta` | - | Citizen Voting Age Population |

### Raw Data Files (original/data/raw/)
- `census_poverty_race/` - Census demographic data
- `eavs/` - Election Administration and Voting Survey
- `gov/`, `gov_wa/` - Raw gubernatorial results
- `participation/` - Raw participation data
- `pres/`, `pres_wa/` - Raw presidential results
- `sen_wa/` - Raw senatorial results (Washington)
- `policies/` - VBM policy adoption data
- `population/` - Population estimates
- `registration/` - Voter registration data

## Key Variable Definitions

### Treatment Variable
- **`treat`**: Binary indicator = 1 if county has universal vote-by-mail in that year
  - Washington: Staggered county-level adoption 2002-2010 (all counties VBM by 2011)
  - Utah: Staggered county-level adoption 2012-2018
  - California: Voter's Choice Act (VCA) adoption starting 2018 (5 counties in 2018)

### Outcome Variables

**Partisan Outcomes (Table 2):**
- **`share_votes_dem`**: Democratic share of turnout (registered Dem votes / total votes) - CA and UT only
- **`dem_share_gov`**: Dem two-party vote share in gubernatorial elections
- **`dem_share_pres`**: Dem two-party vote share in presidential elections
- **`dem_share_sen`**: Dem two-party vote share in senatorial elections

**Participation Outcomes (Table 3):**
- **`turnout_share`**: Turnout rate = ballots_cast / CVAP
- **`vbm_share`**: Share of votes cast by mail (CA only)

### Fixed Effects Variables
- **`county_id`**: Unique county identifier (126 total: 58 CA + 29 UT + 39 WA)
- **`state_year_id`**: State × year fixed effects (35 unique values)
- **`year`**: Election year (1996-2018)
- **`year2`**: year^2 for quadratic trends
- **`year3`**: year^3

### VBM Adoption Variables
- **`switch_year`**: Year county adopted universal VBM (Washington)
- **`ut_all_mail_year`**: Year county adopted VBM (Utah)
- **`vca18`**: =1 if California county adopted VCA for 2018
- **`vca20`**: =1 if California county eligible for VCA 2020 (forward-looking)

## Data Coverage Summary

### By State
| State | Counties | Years | Observations |
|-------|----------|-------|--------------|
| California | 58 | 1998-2018 | 638 |
| Washington | 39 | 1996-2018 | 468 |
| Utah | 29 | 1996-2018 | 348 |
| **Total** | **126** | - | **1,454** |

### Treatment Status
- Total treated observations: 339 (23.3%)
- Untreated observations: 1,115 (76.7%)

**Treatment by State:**
| State | % Treated | Notes |
|-------|-----------|-------|
| California | 0.8% | Only 5 VCA counties in 2018 |
| Utah | 17.0% | Gradual rollout 2012-2018 |
| Washington | 58.8% | Most counties VBM by 2006-2010 |

## Main Analysis Workflow

1. **Data Preparation** (`prep_analysis_data.do`):
   - Merge policies, participation, governor, president, senator, composition data
   - Drop primary elections (keep general only)
   - Create county_id, state_year_id fixed effects
   - Create year^2, year^3 for trends
   - Keep years < 2020

2. **Table 2 - Partisan Effects** (`make_partisan_turnout_table.do`):
   - **Columns 1-3**: Dem turnout share (share_votes_dem)
     - Uses `reghdfe` with county + state×year FE
     - Column 1: No trends
     - Column 2: Linear county trends
     - Column 3: Quadratic county trends
   - **Columns 4-6**: Dem vote share
     - Reshape data to stack governor, president, senator outcomes
     - Same specifications as columns 1-3

3. **Table 3 - Participation Effects** (`make_participation_table.do`):
   - **Columns 1-3**: Turnout (turnout_share)
   - **Columns 4-6**: VBM share (California only)
   - Same fixed effects structure

## Stata Commands Used

| Stata Command | Purpose | Python Equivalent |
|--------------|---------|-------------------|
| `reghdfe` | High-dimensional fixed effects regression | `linearmodels.PanelOLS` with `absorb_effects` or manual demeaning |
| `vce(cluster county_id)` | Clustered standard errors | `cov_type='clustered'` with `cluster_entity` |
| `absorb(county_id state_year)` | Fixed effects | Entity + time effects in panel model |
| `absorb(county_id##c.year)` | County-specific linear trends | Create interaction manually |
| `distinct` | Count unique values | `pd.nunique()` |
| `reshape long` | Reshape data | `pd.melt()` |
| `merge 1:1` | Merge datasets | `pd.merge()` |
| `egen group()` | Create group identifiers | `pd.factorize()` |

## Notes for Replication

1. **Sample restrictions**: Only general elections (no primaries), years 1996-2018

2. **Missing data patterns**:
   - `share_votes_dem` only available for CA and UT (not WA) - 986 non-null
   - `vbm_share` only available for CA - 892 non-null
   - Different N across columns reflects data availability

3. **Standard errors**: Always clustered at county level

4. **Fixed effects structure**:
   - County FE: Absorbs time-invariant county characteristics
   - State×Year FE: Absorbs state-specific electoral shocks (e.g., competitive races)
   - County trends: Allows county-specific trajectories

5. **The `reghdfe` package**: Stata package for efficient estimation with multiple high-dimensional fixed effects. In Python, can use `linearmodels.PanelOLS` with entity/time effects, or manually demean data.
