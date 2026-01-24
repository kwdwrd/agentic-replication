# Summary of Thompson, Wu, Yoder, and Hall (2020)

**Full Citation**: Thompson, Daniel M., Jennifer A. Wu, Jesse Yoder, and Andrew B. Hall. 2020. "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share." *Proceedings of the National Academy of Sciences* 117(25): 14052-14056.

**DOI**: https://doi.org/10.1073/pnas.2007249117

---

## 1. Research Question

### Primary Question
Does universal vote-by-mail (VBM) affect partisan electoral outcomes—specifically, does it change either party's share of turnout or either party's vote share?

### Policy Relevance
The paper was written during the COVID-19 pandemic when many scholars and policymakers were urging expanded VBM to safeguard elections. However, there were competing claims about partisan effects:
- Some Republicans argued that expanded VBM would disadvantage their party
- Some Democrats worried that VBM might disadvantage lower-income and minority voters who historically rely more on in-person voting

The paper provides rigorous causal evidence to adjudicate these competing claims. The findings suggest that universal VBM does not fundamentally advantage either party, contradicting popular claims in the media and supporting the conventional wisdom of election administration experts.

---

## 2. Identification Strategy

### Source of Variation
The paper exploits **staggered county-level adoption** of universal VBM within three states:
- **California**: Voter's Choice Act (VCA) allowed counties to adopt universal VBM starting in 2018
- **Utah**: Counties progressively adopted all-mail elections from 2012-2018
- **Washington**: Counties switched to all-mail elections from 2002-2012

### Key Identifying Assumption
**Parallel trends assumption**: In the absence of VBM adoption, treated and control counties within the same state would have followed similar trajectories in partisan outcomes.

The authors test this assumption through:
1. **Leads analysis**: Testing for pre-treatment effects (anticipatory effects)
2. **Flexible trend specifications**: Including county-specific linear and quadratic time trends

### Why Staggered County-Level Rollout is Valuable
1. **Within-state comparisons**: Comparing counties within the same state controls for state-level factors (election administration, political climate, candidate quality)
2. **Variation in timing**: Different counties adopt at different times, allowing the use of not-yet-treated counties as controls
3. **Multiple states**: Replication across three states with different political contexts strengthens external validity
4. **Avoids selection on observables**: Unlike studies of absentee voters who self-select into VBM, this design compares administratively-assigned treatment

---

## 3. Data

### States Included and Rationale
| State | Counties | Why Included |
|-------|----------|--------------|
| California | 58 | VCA rollout starting 2018; largest state with recent variation |
| Utah | 29 | Progressive county-level adoption 2012-2018 |
| Washington | 39 | Complete rollout 2002-2012; provides longer post-treatment period |

These are the only three states with staggered county-level rollouts of universal VBM during the study period.

### Time Period
**1996-2018** (even years only, covering general elections)
- Includes gubernatorial, presidential, and senatorial elections
- 12 election cycles per state (with some variation by state)

### Key Outcome Variables

| Variable | Definition | Source |
|----------|------------|--------|
| Democratic turnout share | Share of total voter turnout registered as Democratic | L2 voter files (CA, UT only) |
| Democratic vote share | Democratic two-party vote share in statewide races | Secretary of State election results |
| Turnout rate | Ballots cast / Citizen Voting Age Population | Election results + Census CVAP |
| VBM share | Share of ballots cast by mail | Election results (CA, WA only) |

### Unit of Analysis
**County-year-election** (general elections only)
- 126 counties total (58 CA + 29 UT + 39 WA)
- ~1,454 county-year observations in the main analysis

---

## 4. Main Specifications

### Estimating Equation

$$Y_{cst} = \beta \cdot VBM_{cst} + \gamma_{cs} + \delta_{st} + \varepsilon_{cst}$$

Where:
- $Y_{cst}$ = Outcome for county $c$ in state $s$ at time $t$
- $VBM_{cst}$ = 1 if county has universal vote-by-mail, 0 otherwise
- $\gamma_{cs}$ = County fixed effects (absorbs time-invariant county characteristics)
- $\delta_{st}$ = State-by-year fixed effects (absorbs state-specific shocks each year)
- $\varepsilon_{cst}$ = Error term, clustered at county level

### Specification Variations

**Specification 1: Basic difference-in-differences**
- County FE + State×Year FE
- No county-specific trends

**Specification 2: With linear county trends**
- Adds county-specific linear time trends: $\gamma_{cs} \cdot t$
- Accounts for differential pre-treatment trends

**Specification 3: With quadratic county trends**
- Adds county-specific quadratic time trends: $\gamma_{cs} \cdot t + \gamma_{cs} \cdot t^2$
- Most flexible specification

### Interpretation
The coefficient $\beta$ represents the **average treatment effect on the treated (ATT)**—the effect of adopting universal VBM on partisan outcomes, averaged across all county-years that adopted.

---

## 5. Key Findings

### Table 2: Partisan Outcomes

| Outcome | (1) Basic | (2) Linear Trends | (3) Quadratic Trends |
|---------|-----------|-------------------|----------------------|
| **Dem Turnout Share** | | | |
| Coefficient | 0.007 | 0.001 | 0.001 |
| Std. Error | (0.003) | (0.001) | (0.001) |
| Counties | 87 | 87 | 87 |
| **Dem Vote Share** | | | |
| Coefficient | 0.028 | 0.011 | 0.007 |
| Std. Error | (0.011) | (0.004) | (0.003) |
| Counties | 126 | 126 | 126 |

**Interpretation**:
- Effects on Democratic turnout share are small (0.1-0.7 percentage points) and statistically indistinguishable from zero in trend specifications
- Effects on Democratic vote share attenuate substantially with flexible trends (from 2.8 pp to 0.7 pp)
- The attenuation suggests the basic specification may capture pre-existing trends rather than causal effects

### Table 3: Participation Outcomes

| Outcome | (1) Basic | (2) Linear Trends | (3) Quadratic Trends |
|---------|-----------|-------------------|----------------------|
| **Turnout** | | | |
| Coefficient | 0.021 | 0.022 | 0.021 |
| Std. Error | (0.009) | (0.007) | (0.008) |
| Counties | 126 | 126 | 126 |
| **VBM Share** | | | |
| Coefficient | 0.186 | 0.157 | 0.136 |
| Std. Error | (0.027) | (0.035) | (0.085) |
| Counties | 58 | 58 | 58 |

**Interpretation**:
- Turnout increases by ~2.1 percentage points, robust across specifications
- VBM share increases by 14-19 percentage points (strong first stage)
- Turnout effect is consistent with prior literature (Gerber, Huber, and Hill 2013)

---

## 6. Robustness Checks

### State-by-State Results
- Results are "substantively similar" when estimated separately for each state
- No evidence of larger effects in Washington (most extensive VBM expansion)

### Leads Analysis (Pre-Treatment Trends)
- Tests whether VBM shows effects in the elections *before* adoption
- Finding: No evidence of anticipatory effects, supporting parallel trends assumption

### Alternative Outcomes
- Republican turnout share: Symmetric null effects
- Individual office results (governor, president, senator): Consistent patterns

### Heterogeneity Tests
- By age groups
- By racial composition
- By poverty rates
- No systematic evidence of differential effects across subgroups

---

## 7. Limitations Acknowledged by Authors

1. **"Normal times" only**: Analysis covers 1996-2018, before COVID-19. Effects during a pandemic may differ.

2. **Cannot extrapolate to nationwide implementation**: Results are from three Western states that may not generalize.

3. **Universal vs. no-excuse VBM**: Study examines the strongest form of VBM (ballots mailed to all voters). Less expansive reforms may have different effects.

4. **Cannot address all concerns**: Does not address administrative feasibility, costs, or potential effects on minority voters in different contexts.

---

## 8. Key Takeaways for Replication

### To Replicate Table 2:
1. Use `analysis.dta` dataset
2. Outcome 1: `share_votes_dem` (CA and UT only—WA lacks this variable)
3. Outcome 2: Reshape to office-level, use `dem_share_gov`, `dem_share_pres`, `dem_share_sen`
4. Treatment: `treat` variable
5. Fixed effects: `county_id` and `state_year` (or construct state×year dummies)
6. Trends: Interact `county_id` with `year` and `year2`
7. Cluster SEs at `county_id`

### To Replicate Table 3:
1. Outcome 1: `turnout_share` (all states)
2. Outcome 2: `vbm_share` (CA only)
3. Same FE and trend specifications as Table 2

### Key Stata Commands to Translate:
```stata
reghdfe Y treat, a(county_id state_year) vce(clust county_id)
reghdfe Y treat, a(county_id##c.year state_year) vce(clust county_id)
reghdfe Y treat, a(county_id##c.year county_id##c.year2 state_year) vce(clust county_id)
```
