# Original Paper Summary

## Citation

Thompson, Daniel M., Jennifer A. Wu, Jesse Yoder, and Andrew B. Hall. 2020. "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share." *Proceedings of the National Academy of Sciences* 117(25): 14052-14056.

DOI: https://doi.org/10.1073/pnas.2007249117

---

## 1. Research Question

**Primary Question**: Does implementing universal vote-by-mail (VBM) policies affect partisan election outcomes?

**Specific Questions**:
1. Does universal VBM change the partisan composition of the electorate (who turns out)?
2. Does universal VBM change which party wins elections (vote share)?
3. Does universal VBM affect overall turnout levels?

**Policy Relevance**: As of 2020, only a handful of states used universal VBM (Oregon, Washington, Colorado, Hawaii, Utah). The COVID-19 pandemic raised urgent questions about whether expanding VBM would advantage one party, with Republicans frequently claiming it would benefit Democrats and some Democrats believing the same. The paper provides empirical evidence to inform this policy debate.

---

## 2. Identification Strategy

### Source of Variation

The paper exploits **staggered county-level adoption of universal VBM** across three states:
- **Washington**: Counties adopted VBM between 2002-2010 (statewide by 2011)
- **Utah**: Counties adopted VBM between 2012-2018
- **California**: Five counties adopted the Voter's Choice Act in 2018

### Difference-in-Differences Design

The key identifying assumption is **parallel trends**: absent VBM adoption, treated and control counties within the same state would have followed parallel outcome trajectories.

**Why staggered county-level rollout is valuable**:
1. Counties within the same state face the same statewide political environment
2. State-by-year fixed effects absorb state-specific electoral shocks (competitive races, ballot initiatives, etc.)
3. Different adoption timing provides multiple "experiments"
4. Can test for pre-treatment trends to validate the design

### Key Identifying Assumption

Counties that adopted VBM earlier vs. later did not differ systematically in ways that would independently affect partisan outcomes. The paper provides evidence supporting this:
- No significant pre-treatment trends in outcomes
- Results robust to including county-specific time trends

---

## 3. Data

### States and Time Period
| State | Years | Counties | Notes |
|-------|-------|----------|-------|
| California | 1998-2018 | 58 | VCA adopted by 5 counties in 2018 |
| Utah | 1996-2018 | 29 | Gradual adoption 2012-2018 |
| Washington | 1996-2018 | 39 | Staggered adoption 2002-2010 |

### Unit of Analysis
- **County-election** (county c in state s in election year t)
- General elections only (primaries excluded)
- Governor, president, and senate races

### Key Outcome Variables

**Partisan Outcomes (Table 2)**:
1. **Democratic share of turnout**: Proportion of voters registered as Democrats among those who cast ballots (California and Utah only; registration data unavailable for Washington)
2. **Democratic two-party vote share**: Democratic votes / (Democratic + Republican votes) in gubernatorial, presidential, and senatorial races

**Participation Outcomes (Table 3)**:
1. **Turnout**: Ballots cast / Citizen Voting Age Population (CVAP)
2. **VBM share**: Proportion of ballots cast by mail (California only)

### Sample Sizes
- 126 counties total
- 87 counties for partisan turnout share (CA + UT only)
- 986-1,881 county-election observations depending on outcome

---

## 4. Main Specifications

### Estimating Equation

```
Y_cst = β(VBM_cst) + γ_cs + δ_st + ε_cst
```

Where:
- **Y_cst**: Outcome in county c, state s, election year t
- **VBM_cst**: Treatment indicator (=1 if county has universal VBM)
- **γ_cs**: County fixed effects (absorb time-invariant county characteristics)
- **δ_st**: State × year fixed effects (absorb state-specific electoral conditions)
- **ε_cst**: Error term, clustered at county level

### Specification Variations

**Column 1**: Basic diff-in-diff (county FE + state×year FE)

**Column 2**: Add county-specific linear time trends
```
Y_cst = β(VBM_cst) + γ_cs + δ_st + (county_c × year_t) + ε_cst
```

**Column 3**: Add county-specific quadratic time trends
```
Y_cst = β(VBM_cst) + γ_cs + δ_st + (county_c × year_t) + (county_c × year_t²) + ε_cst
```

The trend specifications allow for the possibility that different counties were on different trajectories prior to VBM adoption.

---

## 5. Key Findings

### Table 2: Partisan Outcomes

| Outcome | Basic (1) | Linear Trends (2) | Quad Trends (3) |
|---------|-----------|-------------------|-----------------|
| **Dem Turnout Share** | 0.007 (0.003) | 0.001 (0.001) | 0.001 (0.001) |
| **Dem Vote Share** | 0.028 (0.011) | 0.011 (0.004) | 0.007 (0.003) |

**Interpretation**:
- Basic specification shows small positive coefficients (0.7pp for turnout share, 2.8pp for vote share)
- Effects attenuate substantially with trend controls
- With linear/quadratic trends, effects are near zero and not meaningfully significant
- Authors conclude: "VBM does not have meaningful partisan effects"

### Table 3: Participation Outcomes

| Outcome | Basic (1) | Linear Trends (2) | Quad Trends (3) |
|---------|-----------|-------------------|-----------------|
| **Turnout** | 0.021 (0.009) | 0.022 (0.007) | 0.021 (0.008) |
| **VBM Share** | 0.186 (0.027) | 0.157 (0.035) | 0.136 (0.085) |

**Interpretation**:
- VBM increases overall turnout by ~2 percentage points (robust across specifications)
- This is consistent with prior literature (Gerber et al. 2013 found 2-4pp)
- VBM increases the share of ballots cast by mail by 14-19 percentage points (California)
- The turnout effect is modest but statistically significant

---

## 6. Robustness Checks

### Event Study / Pre-trend Analysis
- Estimated leads of the treatment variable
- Found no significant effects in pre-treatment periods
- Supports parallel trends assumption

### State-by-State Analysis
- Estimated effects separately for each state
- Results consistently null across all three states
- Addresses concern that results driven by one state

### Alternative Outcomes
- Republican turnout share (symmetric null result)
- Different race types (governor, president, senate)

### County-Specific Trends
- Linear and quadratic county trends
- Results robust (and typically smaller) with trends

### Sample Restrictions
- Different time periods
- Different subsets of counties

---

## 7. Limitations Acknowledged

1. **"Normal times" caveat**: Analysis covers elections before COVID-19. Effects could differ during a pandemic when in-person voting carries health risks.

2. **Universal VBM only**: Results apply to universal VBM (ballots mailed to all voters). Effects of lesser reforms (no-excuse absentee) may differ.

3. **County-level analysis**: Cannot detect effects that occur within counties but average out.

4. **Limited California variation**: Only 5 California counties adopted VCA by 2018, limiting statistical power for that state.

5. **Cannot isolate mechanisms**: Null partisan effect could reflect genuine neutrality OR offsetting effects (VBM mobilizes both parties equally).

---

## 8. Conclusions

**Main takeaways**:
1. Universal VBM does not systematically advantage either party
2. VBM modestly increases overall turnout (~2pp)
3. VBM increases the share of votes cast by mail
4. Results contradict partisan claims that VBM helps Democrats

**Policy implications**: Expanding VBM during COVID-19 would likely not change which party wins, though it would allow more people to vote safely by mail.

**Caveats for extension**: The paper explicitly notes results come from "normal times" - the post-COVID period may show different patterns as VBM became a partisan issue.
