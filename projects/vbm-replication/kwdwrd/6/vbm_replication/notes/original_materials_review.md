# Original Materials Review

## File Inventory

### Code Files (`original/code/`)

**Data Preparation Scripts:**

| File | Purpose |
|------|---------|
| `prep_policy_data.do` | Constructs VBM treatment variable from WA, UT, CA policy data. Creates `policies.dta` |
| `prep_analysis_data.do` | Merges policies, participation, governor, president, senator, composition data into `analysis.dta`. Drops primaries, creates IDs, restricts to year < 2020 |
| `prep_participation_tables.do` | Cleans CA participation CSVs, WA replication data, UT election results. Merges CVAP. Creates `participation.dta` |
| `prep_citizen_voting_age_pop.do` | Processes Census CVAP county estimates (2005-2018 ACS waves, 2000 Census). Creates `county_cvap.dta` |
| `prep_gov_data.do` | Cleans CA/UT/WA gubernatorial election results by county. Creates `governor.dta` |
| `prep_pres_data.do` | Cleans presidential election results by county. Creates `president.dta` |
| `prep_sen_data.do` | Cleans senatorial election results. Creates `senator.dta` and `senator_wa.dta` |
| `prep_composition_data.do` | Prepares voter composition data (party registration shares). Creates `composition.dta` |
| `prep_composition_robustness_data.do` | Prepares robustness data for composition analysis |
| `prep_race_composition_data.do` | Race-specific composition data |
| `prep_pov_composition_data.do` | Poverty-specific composition data |
| `prep_pov_census_data.do` | Census poverty data |

**Analysis Scripts:**

| File | Purpose | Produces |
|------|---------|----------|
| `make_partisan_turnout_table.do` | **Table 2**: Dem turnout share (cols 1-3) and Dem vote share (cols 4-6) | `partisan_effects_table.tex` |
| `make_participation_table.do` | **Table 3**: Turnout share (cols 1-3) and VBM share (cols 4-6) | `participation_table.tex` |
| `make_partisan_turnout_table_ca_and_ut.do` | Table S3: CA and UT only partisan results | `partisan_effects_table_ca_and_ut.tex` |
| `make_partisan_effects_state_by_state_table.do` | State-by-state partisan effects | State-specific tables |
| `make_participation_table_state_by_state.do` | State-by-state participation effects | State-specific participation tables |
| `make_participation_descriptives.do` | Descriptive statistics for participation | Descriptives |
| `make_participation_graphs.do` | Participation trend graphs | Figures |
| `make_leads_plots.do` | Event study / leads plots | Lead figures |
| `make_composition_robustness_plots.do` | Robustness composition plots | Robustness figures |
| `make_age_turnout_table.do` | Age group turnout analysis | Age table |
| `make_pov_turnout_table.do` | Poverty-related turnout table | Poverty table |
| `make_race_turnout_table.do` | Race-related turnout table | Race table |
| `make_republican_partisan_turnout_table.do` | Republican partisan turnout | Rep table |
| `make_statewide_vote_shares_by_vbm.do` | Descriptive vote shares by VBM status | Descriptives |
| `make_pov_composition_robustness_figure.do` | Poverty composition robustness | Robustness figure |
| `make_race_composition_robustness_figure.do` | Race composition robustness | Robustness figure |

**Data Collection:**

| File | Purpose |
|------|---------|
| `data_collection/prep_voter_files_sherlock.do` | Script for processing voter files on Stanford Sherlock cluster |

### Raw Data Files (`original/data/raw/`)

| Directory | Contents |
|-----------|----------|
| `census_poverty_race/` | Census poverty and race data |
| `eavs/` | Election Administration and Voting Survey data |
| `gov/` | Gubernatorial election results (CA, by year) |
| `gov_wa/` | Washington gubernatorial results |
| `participation/` | CA participation data CSVs |
| `participation_and_results_ut/` | Utah election data |
| `policies/` | VBM policy adoption data (WA replication data, UT switch dates, CA VCA status) |
| `population/` | Census CVAP data files |
| `pres/` | Presidential election data |
| `pres_wa/` | Washington presidential data |
| `registration/` | Voter registration data |
| `sen_wa/` | Washington senatorial data |

### Modified/Analysis Data Files (`original/data/modified/`)

| File | Size | Description |
|------|------|-------------|
| `analysis.dta` | 886 KB | **Main analysis dataset** (1454 × 134). County-year panel, general elections only, 1996-2018 |
| `policies.dta` | 108 KB | VBM policy treatment indicators by county-year |
| `participation.dta` | 132 KB | Participation outcomes (turnout, VBM share, registration) |
| `governor.dta` | 59 KB | Gubernatorial election results by county |
| `president.dta` | 42 KB | Presidential election results by county |
| `senator.dta` | 23 KB | Senate election results by county |
| `senator_wa.dta` | 19 KB | Washington senate election results |
| `county_cvap.dta` | 1.97 MB | County-level Citizen Voting Age Population estimates |
| `county_voting_age_pop.dta` | 9.69 MB | Voting age population (broader) |
| `composition.dta` | 189 KB | Party registration composition data |
| `composition_race.dta` | 808 KB | Race-specific composition |
| `composition_tract.dta` | 448 KB | Tract-level composition |
| `composition_age_robustness.dta` | 494 KB | Age robustness data |
| `census_ses_data.dta` | 439 KB | Census SES data |
| `registration.csv` | 78 KB | Registration data |
| `ca_votes_by_group.dta` | 47.6 MB | CA votes by demographic group (individual-level) |
| `ca_votes_by_tract.dta` | 11.3 MB | CA votes by tract |
| `ut_votes_by_group.dta` | 10.3 MB | UT votes by group |
| `ut_votes_by_tract.dta` | 864 KB | UT votes by tract |
| `us_election_results.dta` | 4.5 MB | US-wide election results |
| `vote_share_analysis_for_traj_bal.dta` | 195 KB | Vote share data for trajectory balance |
| `matched_counties_drutman.csv` | 1.9 KB | Matched counties list |
| `wa_preselec.csv` | 169 KB | WA pre-election data |

## Main Analysis Dataset Structure

**analysis.dta** (1454 rows × 134 columns)

- **Unit of analysis**: County-year (general elections only)
- **States**: CA (58 counties), UT (29 counties), WA (39 counties) = 126 total counties
- **Years**: 1996, 1998, 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018
- **Not a balanced panel**: Different numbers of observations per county depending on data availability

### Key Variable Definitions

**Identifiers:**
- `state`: State abbreviation (CA, UT, WA)
- `county`: County name
- `year`: Election year
- `county_id`: Numeric county identifier (1-126)
- `state_year_id`: Numeric state×year identifier (labeled `state_year` in code)
- `pres`: =1 if presidential election year

**Treatment:**
- `treat`: =1 if county has universal vote-by-mail in that year
  - CA: =1 for 5 VCA counties (Madera, Napa, Nevada, Sacramento, San Mateo) in 2018 only
  - UT: =1 for counties that adopted all-mail (staggered, 2012-2018)
  - WA: =1 for counties with VBM-only (staggered, 1996-2008; all counties by 2011)
- `vca18`, `vca20`: CA Voter's Choice Act adoption flags
- `ut_all_mail_year`: Year UT county switched to all-mail
- `switch_year`: WA county switch year
- `all_mail2006`: WA flag for counties that were all-mail by 2006

**Outcomes - Partisan (Table 2):**
- `share_votes_dem`: Democratic share of all votes cast (turnout composition). Only available for CA and UT (87 counties), NOT WA
- `dem_share_gov`: Democratic two-party vote share in gubernatorial elections
- `dem_share_pres`: Democratic two-party vote share in presidential elections
- `dem_share_sen`: Democratic two-party vote share in senatorial elections
- For Table 2 cols 4-6, the code reshapes `dem_share_gov`, `dem_share_pres`, `dem_share_sen` into a long format stacked variable `dem_share`

**Outcomes - Participation (Table 3):**
- `turnout_share`: Ballots cast / CVAP (approximate citizen voting age population)
- `vbm_share`: Share of ballots cast by mail (only CA, cols 4-6)

**Controls/Trends:**
- `year2`: year^2 (for quadratic trends)
- `year3`: year^3

## Main Analysis Workflow

### Data Assembly (`prep_analysis_data.do`):
1. Load `policies.dta` (treatment variable)
2. Merge with `participation.dta` (turnout outcomes)
3. Merge with `governor.dta`, `president.dta`, `senator.dta` (vote shares)
4. Merge with `composition.dta`, `composition_tract.dta`, `composition_race.dta`
5. Drop primaries (`prim_or_gen == "primary"`)
6. Create identifiers: `county_id`, `state_year_id`, `election_id`, `county_type_id`
7. Create `year2`, `year3`
8. Restrict to `year < 2020`
9. Save as `analysis.dta`

### Table 2 Estimation (`make_partisan_turnout_table.do`):

**Columns 1-3 (Dem Turnout Share):**
- Uses `analysis.dta` directly
- Outcome: `share_votes_dem`
- Sample: CA + UT only (87 counties; WA lacks this variable)
- Col 1: `reghdfe share_votes_dem treat, a(county_id state_year) vce(clust county_id)`
- Col 2: `reghdfe share_votes_dem treat, a(county_id county_id##c.year state_year) vce(clust county_id)`
- Col 3: `reghdfe share_votes_dem treat, a(county_id##c.year county_id##c.year2 state_year) vce(clust county_id)`

**Columns 4-6 (Dem Vote Share):**
- Reshapes data: `reshape long dem_share, i(state county year) j(office) s`
  - Creates stacked dataset with `dem_share_gov`, `dem_share_pres`, `dem_share_sen` → `dem_share`
- Sample: All 126 counties (all three states)
- Col 4: `reghdfe dem_share treat, a(county_id state_year) vce(clust county_id)`
- Col 5: `reghdfe dem_share treat, a(county_id state_year county_id##c.year) vce(clust county_id)`
- Col 6: `reghdfe dem_share treat, a(state_year county_id county_id##c.year county_id##c.year2) vce(clust county_id)`

### Table 3 Estimation (`make_participation_table.do`):

**Columns 1-3 (Turnout Share):**
- Uses `analysis.dta` directly
- Outcome: `turnout_share`
- Sample: All 126 counties
- Same FE structure as Table 2

**Columns 4-6 (VBM Share):**
- Outcome: `vbm_share`
- Sample: CA only (`if state=="CA"`, 58 counties)
- Same FE structure as Table 2

### Key `reghdfe` Specification Details

The Stata `reghdfe` command (by Sergio Correia) implements OLS with multiple high-dimensional fixed effects via iterative demeaning (Method of Alternating Projections).

**Absorbed fixed effects by specification:**

| Spec | `absorb()` terms | Interpretation |
|------|-------------------|----------------|
| Basic (no trends) | `county_id state_year` | County FE + State×Year FE |
| Linear trends | `county_id county_id##c.year state_year` | County FE + County-specific linear time trend + State×Year FE |
| Quadratic trends | `county_id##c.year county_id##c.year2 state_year` | County-specific linear + quadratic time trends + State×Year FE |

Note: In the linear trend spec, `county_id##c.year` includes both the county FE and the county×year interaction, but `county_id` is also listed separately. Since `reghdfe` handles this via projection, including `county_id` redundantly with `county_id##c.year` is harmless.

In the quadratic spec, `county_id##c.year` (which includes the county FE level) plus `county_id##c.year2` gives both county FE, county-specific linear, and county-specific quadratic trends.

**Standard errors:** Clustered at `county_id` level throughout.

## Treatment Patterns

| State | First treated year | Last untreated year | N treated obs | Treatment source |
|-------|--------------------|---------------------|---------------|------------------|
| CA | 2018 | 2016 | 5 (5 counties × 1 year) | Voter's Choice Act (5 pilot counties in 2018) |
| UT | 2012 | varies | 59 (staggered) | County-level adoption of all-mail voting |
| WA | 1996 | varies | 275 (staggered) | County-level adoption of all-mail, all by 2011 |

## Stata-to-Python Translation Notes

See `notes/stata_python_translations.md` for detailed translations.
