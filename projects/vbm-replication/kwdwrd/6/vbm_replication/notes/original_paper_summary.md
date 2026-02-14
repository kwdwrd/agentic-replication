# Original Paper Summary

**Thompson, Daniel M., Jennifer A. Wu, Jesse Yoder, and Andrew B. Hall. 2020. "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share." *Proceedings of the National Academy of Sciences* 117(25): 14052–14056.**

## 1. Research Question

**What causal question does the paper address?**

Does universal vote-by-mail (VBM)—where every registered voter is automatically mailed a ballot—affect the partisan composition of the electorate or the partisan vote share in elections?

The paper addresses three specific sub-questions:
1. Does universal VBM change the Democratic (or Republican) share of voters who turn out?
2. Does universal VBM change the Democratic two-party vote share?
3. Does universal VBM affect overall turnout rates?

**Why does it matter (policy relevance)?**

The paper was published in June 2020, as COVID-19 drove urgent debates about expanding mail voting for the November 2020 election. President Trump claimed universal VBM would ensure "you'd never have a Republican elected in this country again," while some Democrats worried it could disadvantage their voters. The paper provides rigorous causal evidence to evaluate these claims, finding they are not supported by the data.

## 2. Identification Strategy

**Source of variation:**

The paper exploits the staggered county-level rollout of universal VBM across three US states:
- **Washington**: Counties adopted all-mail elections at different times from 1996 through 2011, when the entire state switched. This provides the most variation.
- **Utah**: Counties adopted all-mail elections in a staggered fashion from approximately 2012 through 2019.
- **California**: Five pilot counties adopted the Voter's Choice Act (VCA) for the 2018 election, replacing traditional polling places with vote centers and mailing all registered voters a ballot.

**Key identifying assumption (parallel trends):**

The trends in electoral outcomes in counties that had not yet adopted VBM provide valid counterfactuals for the trends that would have been observed in the adopting counties, had they not adopted VBM. Formally:

> E[Y(0)_{ct} | VBM = 1, county, year] - E[Y(0)_{ct-1} | VBM = 1, county, year-1] = E[Y(0)_{ct} | VBM = 0, county, year] - E[Y(0)_{ct-1} | VBM = 0, county, year-1]

**Why is the staggered county-level rollout valuable?**

1. Within-state variation controls for all state-level confounders (state laws, political environment, statewide candidates)
2. Staggered timing allows different counties to serve as controls at different times, improving identification
3. County fixed effects control for all time-invariant county characteristics
4. State×year fixed effects control for all state-level shocks in any given year
5. County-specific time trends can be added to further relax the parallel trends assumption

## 3. Data

**Three states included:**
- **California** (58 counties): 1998–2018 (gubernatorial election results; participation data excludes 2000)
- **Utah** (29 counties): 1996–2018
- **Washington** (39 counties): 1996–2016

These are the three states that implemented universal VBM through staggered county-level adoption as of the paper's writing. Oregon, Colorado, and Hawaii adopted statewide VBM without county-level staggering.

**Time period:** 1996–2018, general elections only (primaries excluded)

**Unit of analysis:** County-election year

**Key outcome variables:**

| Variable | Definition | Available for |
|----------|------------|---------------|
| Dem turnout share | Democratic share of all voters who turn out (from voter files with party registration) | CA, UT only (87 counties) |
| Dem vote share | Democratic two-party vote share (pooled across gubernatorial, presidential, senatorial races) | All 3 states (126 counties) |
| Turnout | Ballots cast / Citizen Voting Age Population (CVAP) | All 3 states (126 counties) |
| VBM share | Share of ballots cast by mail | CA only (58 counties) |

**Data sources:**
- Election results: State Secretary of State offices
- Voter files: L2 data vendor (CA and UT), providing individual-level party registration and turnout history
- Washington turnout data: Gerber, Huber, and Hill (2013)
- CVAP: Census Bureau American Community Survey estimates

## 4. Main Specifications

**Estimating equation:**

```
Y_cst = β(VBM_cst) + γ_cs + δ_st + ε_cst
```

Where:
- `Y_cst`: Outcome for county c in state s in year t
- `VBM_cst`: Binary indicator = 1 if county c has universal VBM in year t
- `γ_cs`: County fixed effects (absorb all time-invariant county characteristics)
- `δ_st`: State × year fixed effects (absorb all state-level temporal variation)
- `ε_cst`: Error term, clustered at county level
- `β`: The causal effect of VBM adoption on outcome Y

**Three specifications estimated:**

1. **Basic**: County FE + State×Year FE (as above)
2. **Linear trends**: Add county-specific linear time trends (`γ_cs × t`)
3. **Quadratic trends**: Add county-specific linear + quadratic time trends (`γ_cs × t + γ_cs × t²`)

The linear and quadratic trend specifications relax the parallel trends assumption by allowing each county to follow its own trend. The coefficient β then identifies the VBM effect from deviations from these county-specific trends.

**Standard errors:** Clustered at the county level throughout, accounting for serial correlation within counties.

**Stata implementation:** `reghdfe` (Correia, 2017) with `absorb()` for fixed effects and `vce(cluster county_id)` for clustered standard errors.

## 5. Key Findings

### Table 2 — Partisan Outcomes

| | Dem Turnout Share | | | Dem Vote Share | | |
|---|---|---|---|---|---|---|
| | (1) Basic | (2) Linear | (3) Quad | (4) Basic | (5) Linear | (6) Quad |
| VBM | 0.007 | 0.001 | 0.001 | 0.028 | 0.011 | 0.007 |
| SE | (0.003) | (0.001) | (0.001) | (0.011) | (0.004) | (0.003) |
| Counties | 87 | 87 | 87 | 126 | 126 | 126 |
| Elections | 23 | 23 | 23 | 30 | 30 | 30 |

**Interpretation:**
- The basic specification (col 1) shows a 0.7 pp increase in Democratic turnout share, but this attenuates to 0.1 pp with county trends (cols 2-3). The authors describe this as "a truly negligible effect."
- Democratic vote share shows a 2.8 pp increase in the basic specification (col 4), attenuating to 0.7-1.1 pp with trends (cols 5-6). These estimates are "nowhere near the magnitude necessary to represent a major, permanent electoral shift."
- The attenuation with county trends suggests the basic estimates partly reflect pre-existing differential trends.

### Table 3 — Participation Outcomes

| | Turnout | | | VBM Share | | |
|---|---|---|---|---|---|---|
| | (1) Basic | (2) Linear | (3) Quad | (4) Basic | (5) Linear | (6) Quad |
| VBM | 0.021 | 0.022 | 0.021 | 0.186 | 0.157 | 0.136 |
| SE | (0.009) | (0.007) | (0.008) | (0.027) | (0.035) | (0.085) |
| Counties | 126 | 126 | 126 | 58 | 58 | 58 |
| Elections | 30 | 30 | 30 | 10 | 10 | 10 |

**Interpretation:**
- Turnout increases by about 2.1-2.2 pp across all specifications—remarkably stable. This confirms prior estimates (Gerber et al. 2013).
- VBM share increases by 14-19 pp, showing voters embrace mail voting when available.

## 6. Robustness Checks

**Event study / anticipatory effects tests:**
- The authors plot coefficients on leads of the outcome variables (future VBM adoption) to test whether trends diverged before treatment. They find "no anticipatory effects," validating the parallel trends assumption.

**County-specific time trends:**
- Linear and quadratic trends are included in all main specifications. The stability of turnout estimates and the attenuation of partisan estimates under trends supports the design.

**State-by-state results (Supplementary Tables S8-S9):**
- Results estimated separately for CA, UT, and WA. The authors report "similarly null" effects across all three states, with "no evidence of a larger effect of VBM expansion in Washington, the state with the most extreme expansion."

**Alternative outcomes:**
- Republican turnout share analyzed separately (mirror image of Democratic share)
- Age-group turnout composition
- Race and poverty composition of the electorate

**Key caveat from the authors:**
The evidence applies to "normally administered" elections. The effect of VBM "relative to the counterfactual of an in-person election during COVID-19 might be quite different."
