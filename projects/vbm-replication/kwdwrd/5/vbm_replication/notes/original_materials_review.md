# Original Materials Review

## File Inventory

### Code Files (`original/code/`)

| File | Purpose |
|------|---------|
| `prep_policy_data.do` | Creates VBM policy/treatment data for WA, UT, CA |
| `prep_analysis_data.do` | Merges all data sources into `analysis.dta` |
| `prep_participation_tables.do` | Cleans participation data (turnout, VBM share) for CA, WA, UT |
| `prep_citizen_voting_age_pop.do` | Prepares CVAP denominators |
| `prep_gov_data.do` | Cleans gubernatorial election results |
| `prep_pres_data.do` | Cleans presidential election results |
| `prep_sen_data.do` | Cleans senatorial election results |
| `prep_composition_data.do` | Prepares voter composition data |
| `prep_composition_robustness_data.do` | Prepares composition robustness checks |
| `prep_pov_census_data.do` | Prepares poverty/census data |
| `prep_pov_composition_data.do` | Prepares poverty composition data |
| `prep_race_composition_data.do` | Prepares race composition data |
| **`make_partisan_turnout_table.do`** | **Produces Table 2: Partisan outcomes (key file)** |
| **`make_participation_table.do`** | **Produces Table 3: Participation outcomes (key file)** |
| `make_partisan_turnout_table_ca_and_ut.do` | CA-UT only partisan analysis |
| `make_participation_descriptives.do` | Descriptive statistics for participation |
| `make_participation_graphs.do` | Participation figures |
| `make_participation_table_state_by_state.do` | State-by-state participation results |
| `make_partisan_effects_state_by_state_table.do` | State-by-state partisan results |
| `make_republican_partisan_turnout_table.do` | Republican turnout share analysis |
| `make_leads_plots.do` | Lead/lag event study plots |
| `make_age_turnout_table.do` | Age-group turnout analysis |
| `make_race_turnout_table.do` | Race-group turnout analysis |
| `make_pov_turnout_table.do` | Poverty-group turnout analysis |
| `make_composition_robustness_plots.do` | Composition robustness figures |
| `make_pov_composition_robustness_figure.do` | Poverty composition robustness |
| `make_race_composition_robustness_figure.do` | Race composition robustness |
| `make_statewide_vote_shares_by_vbm.do` | Statewide vote share descriptives |
| `data_collection/` | Directory with data collection scripts |

### Modified Data Files (`original/data/modified/`)

| File | Rows | Cols | Description |
|------|------|------|-------------|
| **`analysis.dta`** | 1,454 | 134 | **Main analysis dataset (merged, general elections, <2020)** |
| `policies.dta` | 2,179 | 12 | VBM policy/treatment indicators |
| `participation.dta` | 1,240 | 17 | Turnout and VBM share data |
| `governor.dta` | 1,317 | 7 | Gubernatorial election results |
| `president.dta` | 911 | 7 | Presidential election results |
| `senator.dta` | 544 | 5 | Senatorial election results (CA, UT) |
| `senator_wa.dta` | 427 | 5 | WA senatorial results |
| `composition.dta` | 2,798 | 13 | Voter composition by party/age |
| `composition_race.dta` | 2,798 | 61 | Race composition data |
| `composition_tract.dta` | 2,798 | 33 | Tract-level composition |
| `composition_age_robustness.dta` | 2,798 | 39 | Age composition robustness |
| `county_cvap.dta` | 41,808 | 6 | County CVAP estimates |
| `county_voting_age_pop.dta` | 158,746 | 7 | County voting-age population |
| `census_ses_data.dta` | 10,103 | 7 | Census SES data |
| `vote_share_analysis_for_traj_bal.dta` | 2,355 | 14 | Trajectory balance analysis |
| `ca_votes_by_group.dta` | 767,695 | 5 | CA votes by demographic group |
| `ca_votes_by_tract.dta` | 250,772 | 4 | CA votes by tract |
| `ut_votes_by_group.dta` | 174,952 | 5 | UT votes by demographic group |
| `ut_votes_by_tract.dta` | 21,436 | 4 | UT votes by tract |
| `us_election_results.dta` | 60,712 | 10 | Nationwide election results |
| `registration.csv` | 1,276 | 11 | Voter registration data |
| `matched_counties_drutman.csv` | 32 | 9 | Matched counties for robustness |
| `wa_preselec.csv` | 2,443 | 8 | WA pre-election data |

### Original Raw Data (`original/data/raw/`)

| Directory | Contents |
|-----------|----------|
| `census_poverty_race/` | Census poverty and race data |
| `eavs/` | Election Administration and Voting Survey |
| `gov/` | Gubernatorial election results |
| `gov_wa/` | WA gubernatorial results |
| `participation/` | CA participation data (CSVs) |
| `participation_and_results_ut/` | UT election participation/results |
| `policies/` | VBM policy data (WA, UT, CA) |
| `population/` | Population data |
| `pres/` | Presidential election results |
| `pres_wa/` | WA presidential results |
| `registration/` | Voter registration data |
| `sen_wa/` | WA senatorial results |

## Main Analysis Workflow

### Data Preparation Pipeline
1. `prep_policy_data.do` → Creates treatment indicators for each county-year
2. `prep_participation_tables.do` → Cleans turnout/VBM data
3. `prep_citizen_voting_age_pop.do` → Creates CVAP denominators
4. `prep_gov_data.do`, `prep_pres_data.do`, `prep_sen_data.do` → Election results
5. `prep_composition_data.do` → Voter composition
6. **`prep_analysis_data.do`** → Merges all above into `analysis.dta`
   - Merges policies, participation, governor, president, senator, composition
   - Drops primaries (keeps general elections only)
   - Creates ID variables: `county_id`, `state_year_id`, `election_id`
   - Creates `year2 = year^2` and `year3 = year^3`
   - Drops year >= 2020
   - Saves as `analysis.dta`

### Analysis Pipeline
7. **`make_partisan_turnout_table.do`** → Table 2 (partisan outcomes)
8. **`make_participation_table.do`** → Table 3 (participation outcomes)
9. Additional robustness files for supplementary tables

## Key Variable Definitions

### From `analysis.dta` (1,454 obs, 126 counties, 1996-2018)

| Variable | Definition | Source |
|----------|-----------|--------|
| `state` | State abbreviation (CA, UT, WA) | Policy data |
| `county` | County name | Policy data |
| `year` | Election year (even years only) | Policy data |
| `county_id` | Numeric county identifier (1-126) | Generated |
| `state_year_id` | Numeric state-year identifier (1-36) | Generated |
| `treat` | =1 if universal VBM in effect | Policy data |
| `share_votes_dem` | Democratic share of total ballots cast | Composition data (CA, UT only) |
| `dem_share_gov` | Dem two-party vote share, governor | Governor data |
| `dem_share_pres` | Dem two-party vote share, president | President data |
| `dem_share_sen` | Dem two-party vote share, senator | Senator data |
| `turnout_share` | Ballots cast / CVAP | Participation data |
| `vbm_share` | Mail ballots / total ballots | Participation data |
| `vbm` | Number of mail ballots | Participation data |
| `ballots_cast` | Total ballots cast | Participation data |
| `cvap` | Citizen voting-age population | Census data |
| `cvap_approx` | Approximate CVAP (for turnout denominator) | Census data |
| `registered` | Registered voters | Participation data |
| `year2` | year^2 (for quadratic trends) | Generated |
| `year3` | year^3 | Generated |
| `vca18` | =1 if CA county was VCA-eligible in 2018 | CA policy data |
| `vca20` | =1 if CA county was VCA-eligible in 2020 | CA policy data |
| `all_mail2006` | =1 if WA county switched in 2006 | WA policy data |
| `ut_all_mail_year` | Year UT county adopted VBM | UT policy data |

### Treatment Coding

- **California**: `treat = 1` only in 2018 for 5 VCA counties (Madera, Napa, Nevada, Sacramento, San Mateo)
- **Utah**: Staggered adoption 2012-2018 (1 county in 2012, 10 by 2014, 21 by 2016, 27 by 2018)
- **Washington**: Staggered adoption 1996-2012 (1 county in 1996, expanding to all 39 by 2012)

### Observations by State
- CA: 638 (58 counties × ~11 years)
- UT: 348 (29 counties × 12 years)
- WA: 468 (39 counties × 12 years)

### Key Data Notes
- `share_votes_dem` available for CA and UT only (986 non-null out of 1,454) — this is why Table 2 cols 1-3 have only 87 counties
- `dem_share_gov/pres/sen` available for all states but only certain years
- Table 2 cols 4-6 reshape the `dem_share_*` columns long, getting 126 counties
- `turnout_share` available for 1,240 obs (not all county-years have participation data)
- `vbm_share` restricted to CA for Table 3 cols 4-6 (892 non-null, but CA-only filter)

## Stata Commands Requiring Python Translation

| Stata Command | Usage in Original | Python Equivalent | Notes |
|--------------|-------------------|-------------------|-------|
| `reghdfe Y treat, a(county_id state_year) vce(clust county_id)` | All main specifications | `linearmodels.AbsorbingLS` or manual demeaning + `statsmodels.OLS` with clustered SEs | High-dimensional FE regression |
| `a(county_id)` | County fixed effects | Entity effects in panel model | 126 county dummies |
| `a(state_year)` | State×Year fixed effects | Time effects (state-year groups) | 35-36 state-year dummies |
| `a(county_id##c.year)` | County-specific linear trends | County × year interactions | county_id dummies + county_id × year |
| `a(county_id##c.year county_id##c.year2)` | County-specific quadratic trends | County × year + county × year² | Adds county_id × year² |
| `vce(clust county_id)` | Clustered standard errors | `cov_type='clustered', cluster_entity=True` or manual clustering | Cluster at county level |
| `distinct` | Count unique values | `nunique()` | For reporting N counties, elections |
| `reshape long` | Reshape dem_share variables | `pd.melt()` or `pd.wide_to_long()` | For Table 2 cols 4-6 |
| `merge 1:1` | Merge datasets | `pd.merge()` | Data preparation |
| `egen group()` | Create group IDs | `pd.factorize()` or `groupby().ngroup()` | For FE identifiers |

### Key Implementation Notes

1. **`reghdfe` equivalent**: The `linearmodels.AbsorbingLS` class can handle multiple sets of absorbed fixed effects. Alternatively, can use manual within-transformation or dummy variable approach with `statsmodels.OLS`.

2. **County-specific trends**: `county_id##c.year` in Stata means county FE + county×year interactions. In Python, create `county_id × year` interaction terms and absorb them.

3. **Clustered SEs**: Must cluster at county level (126 clusters). Use `linearmodels` built-in clustering or `statsmodels` with `cov_type='cluster'`.

4. **Sample restrictions**:
   - Table 2 cols 1-3: Only where `share_votes_dem` is non-missing (CA + UT = 87 counties)
   - Table 2 cols 4-6: All states, reshaped long on `dem_share_gov/pres/sen`
   - Table 3 cols 1-3: All states where `turnout_share` non-missing (126 counties)
   - Table 3 cols 4-6: CA only, `vbm_share` (58 counties)
