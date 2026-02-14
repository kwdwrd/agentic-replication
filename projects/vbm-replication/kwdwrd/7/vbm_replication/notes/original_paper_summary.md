# Original Paper Summary

## Citation

Thompson, Daniel M., Jennifer A. Wu, Jesse Yoder, and Andrew B. Hall. 2020. "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share." *Proceedings of the National Academy of Sciences* 117(25): 14052-14056.

DOI: 10.1073/pnas.2007249117

---

## 1. Research Question

**Causal Question**: Does universal vote-by-mail (VBM) affect partisan electoral outcomes?

Specifically, the paper asks:
1. Does VBM change the partisan composition of the electorate (who turns out)?
2. Does VBM change election results (which party wins more votes)?
3. Does VBM affect overall turnout levels?

**Policy Relevance**: The paper was published during the COVID-19 pandemic when policymakers were considering emergency expansions of VBM to protect public health during elections. Claims from both parties suggested VBM would advantage their opponents:
- President Trump claimed VBM would prevent Republican victories
- Some argued Democrats might face disadvantages with VBM

The paper provides evidence to evaluate these competing claims.

---

## 2. Identification Strategy

### Source of Variation

The identification strategy exploits **staggered county-level adoption** of universal VBM within three states:
- **California**: Voter's Choice Act allowed counties to opt into VBM starting 2018
- **Utah**: Counties adopted VBM between 2012-2020
- **Washington**: Counties adopted VBM between 2005-2011 (100% by 2011)

### Estimating Equation

The paper estimates the following difference-in-differences specification:

```
Y_cst = β(VBM_cst) + γ_cs + δ_st + ε_cst
```

Where:
- **Y_cst** = Outcome in county c, state s, election t
- **VBM_cst** = 1 if county has universal VBM, 0 otherwise
- **γ_cs** = County fixed effects (absorb time-invariant county characteristics)
- **δ_st** = State × Year fixed effects (absorb state-specific election shocks)
- **ε_cst** = Error term (clustered at county level)
- **β** = Causal effect of VBM on outcome (coefficient of interest)

### Key Identifying Assumption

**Parallel Trends**: In the absence of VBM adoption, treated and control counties within the same state would have followed parallel outcome trajectories.

This assumption is supported by:
1. **Lead specifications**: Testing for differential pre-trends shows no anticipatory effects
2. **Flexible trends**: Results robust to adding county-specific linear and quadratic time trends

### Why Staggered County-Level Rollout is Valuable

1. **Within-state comparisons**: State × Year fixed effects absorb confounds that vary at the state-year level (e.g., candidate quality, national partisan tides)

2. **Multiple timing groups**: Variation in when counties adopt provides robustness against single-event confounds

3. **Policy-relevant variation**: Counties opt-in to VBM, mimicking real policy implementation

---

## 3. Data

### Geographic Scope

| State | Counties | Treatment Timing |
|-------|----------|------------------|
| California | 58 | VCA adoption: 5 counties in 2018 |
| Utah | 29 | Staggered: 2012-2020 |
| Washington | 39 | Staggered: 2005-2011 |
| **Total** | **126** | |

### Time Period

- **Original analysis**: 1996-2018 (election years only)
- California: 1998-2018
- Utah: 1996-2018
- Washington: 1996-2016

### Unit of Analysis

County-election (e.g., Alameda County, CA in the 2018 gubernatorial election)

### Key Outcome Variables

**Partisan Outcomes (Table 2)**:
1. **Democratic share of turnout**: Proportion of voters who are registered Democrats
   - Available for CA and UT only (uses voter file data)
2. **Democratic two-party vote share**: Dem votes / (Dem + Rep votes)
   - Available for all three states (official election results)

**Participation Outcomes (Table 3)**:
1. **Turnout**: Total ballots cast / Citizen Voting Age Population (CVAP)
2. **VBM share**: Share of votes cast by mail
   - Available for CA only

### Data Sources

- California Secretary of State (election results, VBM data)
- Utah Lieutenant Governor (election results)
- Washington Secretary of State (election results)
- Voter file data from CA and UT (party registration)
- Census Bureau CVAP estimates (denominator for turnout)
- Gerber, Huber, and Hill (2013) Washington replication data

---

## 4. Main Specifications

### Specification 1: Basic Difference-in-Differences

```
Y_cst = β(VBM_cst) + γ_cs + δ_st + ε_cst
```

- County fixed effects
- State × Year fixed effects
- Standard errors clustered by county

### Specification 2: Linear County Trends

```
Y_cst = β(VBM_cst) + γ_cs + δ_st + (θ_c × t) + ε_cst
```

- Adds county-specific linear time trends
- Allows each county to have its own trajectory

### Specification 3: Quadratic County Trends

```
Y_cst = β(VBM_cst) + γ_cs + δ_st + (θ_c × t) + (φ_c × t²) + ε_cst
```

- Adds county-specific quadratic time trends
- Most flexible specification

---

## 5. Key Findings

### Table 2: Partisan Outcomes

| Outcome | Basic | Linear Trends | Quad Trends |
|---------|-------|---------------|-------------|
| **Dem Turnout Share** | | | |
| Coefficient | 0.007 | 0.001 | 0.001 |
| Std. Error | (0.003) | (0.001) | (0.001) |
| Counties | 87 | 87 | 87 |
| **Dem Vote Share** | | | |
| Coefficient | 0.028 | 0.011 | 0.007 |
| Std. Error | (0.011) | (0.004) | (0.003) |
| Counties | 126 | 126 | 126 |

**Interpretation**:
- Basic specification shows small positive effects, but these are driven by pre-existing trends
- With trend controls, effects become close to zero and statistically insignificant
- VBM does not meaningfully change partisan composition or vote shares

### Table 3: Participation Outcomes

| Outcome | Basic | Linear Trends | Quad Trends |
|---------|-------|---------------|-------------|
| **Turnout** | | | |
| Coefficient | 0.021 | 0.022 | 0.021 |
| Std. Error | (0.009) | (0.007) | (0.008) |
| Counties | 126 | 126 | 126 |
| **VBM Share** | | | |
| Coefficient | 0.186 | 0.157 | 0.136 |
| Std. Error | (0.027) | (0.035) | (0.085) |
| Counties | 58 | 58 | 58 |

**Interpretation**:
- VBM increases overall turnout by ~2 percentage points (robust across specifications)
- VBM substantially increases the share of ballots cast by mail (~14-19 pp)
- This is a "first stage" showing the policy meaningfully changes voting behavior

---

## 6. Robustness Checks

### 6.1 State-by-State Analysis

The authors estimate the main specification separately for each state:
- **California**: Limited variation (only 5 treated county-years)
- **Utah**: Most staggered variation; results consistent with pooled estimates
- **Washington**: Earliest adopter; results consistent

### 6.2 Event Study / Lead Specifications

- Test for pre-trends by including leads of the treatment indicator
- Find no evidence of differential trends before VBM adoption
- This supports the parallel trends assumption

### 6.3 Election Type Heterogeneity

- Presidential vs. gubernatorial vs. senatorial elections
- Results consistent across election types

### 6.4 Voter Composition Analysis

- Examine whether VBM changes who votes (beyond party)
- Look at demographic composition effects
- Find minimal effects on voter composition by age, race, socioeconomic status

---

## 7. Conclusions

### Main Findings

1. **No partisan effects**: Universal VBM does not advantage either party
   - Democratic turnout share: essentially zero effect
   - Democratic vote share: essentially zero effect

2. **Modest turnout increase**: VBM increases turnout by ~2 percentage points
   - Consistent with prior literature
   - Represents meaningful participation gains

3. **Strong "first stage"**: VBM substantially increases mail ballot usage
   - Shows the policy meaningfully changes how people vote
   - Necessary condition for any downstream effects

### Caveats Emphasized by Authors

1. **Normal times vs. pandemic**: Results describe effects in non-emergency contexts; pandemic conditions may differ

2. **Causal vs. correlation**: The diff-in-diff design identifies causal effects, not just correlations

3. **Universal VBM vs. other reforms**: Results apply to universal VBM (ballots mailed to all voters), not necessarily to "no-excuse" absentee voting or other lesser reforms

### Policy Implications

- Universal VBM can safely expand without advantaging either party
- Concerns about partisan manipulation through VBM are not supported by evidence
- VBM may be a way to increase participation while maintaining electoral neutrality
