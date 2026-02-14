# Summary of Thompson, Wu, Yoder, and Hall (2020)

**Full Citation:** Thompson, Daniel M., Jennifer A. Wu, Jesse Yoder, and Andrew B. Hall. 2020. "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share." *Proceedings of the National Academy of Sciences* 117(25): 14052-14056. DOI: 10.1073/pnas.2007249117.

## 1. Research Question

**Causal question:** Does the adoption of universal vote-by-mail (VBM)---where all registered voters are mailed ballots---affect partisan electoral outcomes?

Specifically, the paper asks three questions:
1. Does universal VBM affect either party's share of turnout (i.e., the partisan composition of the electorate)?
2. Does universal VBM affect either party's vote share?
3. Does universal VBM affect overall turnout levels?

**Policy relevance:** The paper was published during the COVID-19 pandemic, when expanding mail voting was being debated as a way to protect public health while maintaining democratic participation. Claims that VBM systematically favors Democrats were widespread among Republican politicians and commentators, while some Democratic advocates argued it would boost their party's fortunes. The paper provides rigorous evidence to evaluate these competing claims.

## 2. Identification Strategy

**Source of variation:** The paper exploits the staggered county-level rollout of universal vote-by-mail within three US states: California, Utah, and Washington. Different counties within these states adopted universal VBM at different times, creating within-state variation in treatment timing.

**Key identifying assumption:** Parallel trends---counties that did not (yet) adopt VBM provide valid counterfactuals for the trends that would have been observed in treated counties had they not adopted VBM. Formally, in the absence of treatment, trends in electoral outcomes would have been similar across counties within the same state.

**Why staggered county-level rollout is valuable:**
- Within-state comparisons control for state-level confounds (e.g., statewide campaigns, political climate)
- State-by-year fixed effects absorb all state-level time-varying shocks
- County fixed effects absorb all time-invariant county characteristics
- The staggered timing provides multiple "experiments" rather than a single before/after comparison
- Multiple states with different political contexts strengthen external validity

**Treatment details by state:**
- **Washington:** Counties adopted VBM between 1996 and 2012, with most switching around 2005-2008 and all 39 counties treated by 2012.
- **Utah:** Counties adopted VBM between 2012 and 2018, with staggered adoption across 29 counties.
- **California:** Five counties (Madera, Napa, Nevada, Sacramento, San Mateo) adopted the Voter's Choice Act for the 2018 election, representing the initial rollout of VCA.

## 3. Data

**Three states included:** California (58 counties), Utah (29 counties), and Washington (39 counties), for a total of 126 counties.

**Why these states:** They are the only three US states where universal VBM was adopted in a staggered, county-level fashion (rather than statewide all at once, as in Oregon or Colorado). This staggered rollout within states is essential for the difference-in-differences identification strategy.

**Time period:** 1996-2018 (general elections in even years only).

**Unit of analysis:** County-election (county × year).

**Key outcome variables:**
1. **Democratic turnout share** (`share_votes_dem`): The share of total ballots cast by registered Democrats. Available for CA and UT only (87 counties), since WA does not have partisan registration.
2. **Democratic two-party vote share** (`dem_share`): Democratic share of the two-party vote for governor, president, or senator. Data reshaped long across office types to maximize observations. Available for all 126 counties.
3. **Turnout** (`turnout_share`): Total ballots cast divided by citizen voting-age population (CVAP). Available for all 126 counties.
4. **VBM share** (`vbm_share`): Share of total ballots cast by mail. Available for CA only (58 counties).

**Number of observations in main analysis:**
- Dem turnout share: 986 obs, 87 counties, 23 elections
- Dem vote share: ~1,454+ obs (reshaped long), 126 counties, ~35 elections
- Turnout: 1,240 obs, 126 counties, ~30 elections
- VBM share: CA only subset

## 4. Main Specifications

**Estimating equation:**

```
Y_cst = beta * VBM_cst + gamma_cs + delta_st + epsilon_cst
```

Where:
- `Y_cst` = outcome variable for county c in state s at election time t
- `VBM_cst` = treatment indicator (= 1 if universal VBM is in effect for county c in state s at time t, 0 otherwise)
- `gamma_cs` = county fixed effects (absorb all time-invariant county characteristics)
- `delta_st` = state x year fixed effects (absorb all state-level time-varying shocks, so identification comes from within-state variation in treatment timing)
- `epsilon_cst` = error term, clustered at the county level

**Three specifications for each outcome:**
1. **Basic:** County FE + State x Year FE only (as above)
2. **Linear county trends:** Adds county-specific linear time trends (`county_id x year` interactions)
3. **Quadratic county trends:** Adds county-specific linear and quadratic time trends (`county_id x year` + `county_id x year^2` interactions)

**Estimation command:** `reghdfe` in Stata, which implements OLS with high-dimensional fixed effects (absorbed via the method of alternating projections). Standard errors clustered at the county level using `vce(cluster county_id)`.

## 5. Key Findings

### Table 2: Partisan Outcomes

| Outcome | (1) Basic | (2) Linear Trends | (3) Quad Trends |
|---------|-----------|-------------------|-----------------|
| **Dem Turnout Share** | | | |
| VBM coefficient | 0.007 | 0.001 | 0.001 |
| Clustered SE | (0.003) | (0.001) | (0.001) |
| Counties | 87 | 87 | 87 |
| **Dem Vote Share** | | | |
| VBM coefficient | 0.028 | 0.011 | 0.007 |
| Clustered SE | (0.011) | (0.004) | (0.003) |
| Counties | 126 | 126 | 126 |

**Interpretation:**
- The basic specification shows small positive coefficients (0.7 pp for Dem turnout share, 2.8 pp for Dem vote share), but these are likely driven by pre-existing trends.
- Adding county-specific linear or quadratic trends attenuates the estimates dramatically, suggesting the basic specification captures differential trends rather than causal effects.
- With trends, the estimates are economically small (0.1 pp for Dem turnout share, 0.7-1.1 pp for Dem vote share) and generally not distinguishable from zero given the standard errors.
- The authors emphasize that inclusion of county trends is important because counties that adopted VBM may have been on different political trajectories.

### Table 3: Participation Outcomes

| Outcome | (1) Basic | (2) Linear Trends | (3) Quad Trends |
|---------|-----------|-------------------|-----------------|
| **Turnout** | | | |
| VBM coefficient | 0.021 | 0.022 | 0.021 |
| Clustered SE | (0.009) | (0.007) | (0.008) |
| Counties | 126 | 126 | 126 |
| **VBM Share** | | | |
| VBM coefficient | 0.186 | 0.157 | 0.136 |
| Clustered SE | (0.027) | (0.035) | (0.085) |
| Counties | 58 | 58 | 58 |

**Interpretation:**
- Turnout increases by approximately 2 percentage points across all specifications. This estimate is remarkably stable across specifications (0.021-0.022), suggesting it reflects a genuine causal effect rather than differential trends.
- VBM share increases by 14-19 percentage points (CA only), confirming that the policy mechanically shifts vote mode.
- The turnout effect is consistent with prior estimates from Gerber, Huber, and Hill (2013) for Washington.

## 6. Robustness Checks

The paper includes several robustness checks in the supplementary materials:

1. **State-by-state results:** The main specifications are estimated separately for each state (CA, UT, WA). Results are "reassuringly similar" across states, suggesting the findings are not driven by any single state.

2. **Event study / leads and lags:** The authors estimate event study specifications with leads of treatment to test for pre-trends. They find no evidence that VBM affects outcomes *before* adoption, supporting the parallel trends assumption.

3. **Republican turnout share:** Estimated separately as an additional partisan outcome. Results mirror the Democratic turnout share findings.

4. **Age-specific turnout:** The composition of the electorate by age group is examined. VBM does not appear to differentially mobilize younger or older voters in a way that systematically favors one party.

5. **Race-specific turnout:** Similar composition analysis by racial group.

6. **Poverty-based analysis:** Composition analysis by neighborhood poverty level.

7. **Alternative fixed effects structures:** More flexible fixed effects specifications.

8. **CA-and-UT only analysis:** Since WA lacks partisan registration data, the partisan turnout analysis is inherently limited to CA and UT. The paper verifies results hold in this subsample.
