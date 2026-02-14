# Original Paper Summary

## Citation

Thompson, Daniel M., Jennifer A. Wu, Jesse Yoder, and Andrew B. Hall. 2020. "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share." *Proceedings of the National Academy of Sciences* 117(25): 14052-14056.

DOI: 10.1073/pnas.2007249117

---

## 1. Research Question

**Central Question**: Does universal vote-by-mail (VBM)—a policy under which every registered voter is automatically mailed a ballot before an election—affect partisan electoral outcomes?

**Specific questions addressed:**
1. Does VBM change which party's supporters turn out to vote?
2. Does VBM change the vote shares received by Democratic vs. Republican candidates?
3. Does VBM affect overall turnout levels?

**Policy Relevance**:
- VBM expansion became highly salient during the COVID-19 pandemic
- President Trump claimed VBM would prevent Republicans from winning elections
- Democratic operatives expressed concerns VBM might disadvantage their voters
- The paper provides the "most comprehensive confirmation to date of VBM's neutral partisan effects"

---

## 2. Identification Strategy

### Source of Variation
The paper exploits **staggered county-level adoption** of universal VBM within three U.S. states:
- **California**: Voter's Choice Act (VCA) began in 2018 with 5 pilot counties
- **Utah**: Counties adopted VBM between 2004-2019
- **Washington**: Counties adopted VBM between 2005-2011 (100% by 2011)

### Key Identifying Assumption: Parallel Trends
Counties that adopted VBM would have followed the same outcome trajectories as non-adopting counties in the absence of treatment.

### Why This Design Works
1. **Within-state comparisons**: Counties within the same state face identical candidate choices in state-wide races, eliminating candidate quality as a confounder
2. **State-by-year fixed effects**: Absorb all state-specific time shocks
3. **County fixed effects**: Absorb all time-invariant county characteristics
4. **Staggered timing**: Different adoption times across counties provide multiple treatment cohorts

### Threats to Identification
- Counties may adopt VBM for reasons correlated with trends in outcomes
- Authors address this by:
  - Testing for pre-trends using lead coefficients
  - Including county-specific linear and quadratic time trends
  - Examining state-by-state results

---

## 3. Data

### Geographic Coverage
| State | Counties | Time Period | Treatment Variation |
|-------|----------|-------------|---------------------|
| California | 58 | 1998-2018 | VCA 2018: 5 counties adopted |
| Utah | 29 | 1996-2018 | Staggered 2004-2019 |
| Washington | 39 | 1996-2018 | Staggered 2005-2011 (100% by 2011) |
| **Total** | **126** | **1996-2018** | |

### Unit of Analysis
County-election observations (even-numbered years, general elections)

### Sample Sizes by Analysis
- Partisan turnout (CA + UT only): ~520 observations, 87 counties
- Democratic vote share (all states): ~1,400 observations, 126 counties
- Turnout (all states): ~1,240 observations, 126 counties
- VBM share (CA only): ~580 observations, 58 counties

### Key Outcome Variables

**Partisan Outcomes:**
- `share_votes_dem`: Democratic share of voters (from voter registration files)
  - Available for CA and UT only (no WA voter file access)
- `dem_share_gov/pres/sen`: Democratic two-party vote share in gubernatorial, presidential, and Senate races

**Participation Outcomes:**
- `turnout_share`: Total ballots cast / Citizen Voting Age Population (CVAP)
- `vbm_share`: Share of ballots cast by mail (CA only)

### Data Sources
- Election results: State Secretaries of State, MIT Election Data + Science Lab
- Voter file data: California and Utah statewide voter files
- Population: Census Bureau CVAP estimates
- VBM policy adoption: Authors' coding from state records; Washington data from Gerber, Huber, and Hill (2013)

---

## 4. Main Specifications

### Estimating Equation

**Basic Difference-in-Differences:**
```
Y_cst = β(VBM_cst) + γ_c + δ_st + ε_cst
```

Where:
- Y_cst = outcome for county c in state s at time t
- VBM_cst = 1 if county c has universal VBM at time t, 0 otherwise
- γ_c = county fixed effects (absorb time-invariant county characteristics)
- δ_st = state-by-year fixed effects (absorb state-specific time shocks)
- ε_cst = error term, clustered at county level
- β = **causal effect of VBM** (parameter of interest)

**With County-Specific Linear Trends:**
```
Y_cst = β(VBM_cst) + γ_c + δ_st + (γ_c × t) + ε_cst
```

**With County-Specific Quadratic Trends:**
```
Y_cst = β(VBM_cst) + γ_c + δ_st + (γ_c × t) + (γ_c × t²) + ε_cst
```

### Interpretation
- County FE: Compare within-county changes over time
- State×Year FE: Compare counties in the same state facing the same election
- County trends: Allow each county to follow its own trajectory, relaxing parallel trends

---

## 5. Key Findings

### Table 2: Partisan Outcomes

**Democratic Turnout Share (CA + UT, 87 counties):**

| Specification | Coefficient | SE | 95% CI |
|---------------|-------------|-----|--------|
| (1) Basic | 0.007 | 0.003 | [0.001, 0.013] |
| (2) Linear trends | 0.001 | 0.001 | [-0.001, 0.003] |
| (3) Quadratic trends | 0.001 | 0.001 | [-0.001, 0.003] |

**Democratic Vote Share (all 126 counties):**

| Specification | Coefficient | SE | 95% CI |
|---------------|-------------|-----|--------|
| (4) Basic | 0.028 | 0.011 | [0.006, 0.050] |
| (5) Linear trends | 0.011 | 0.004 | [0.003, 0.019] |
| (6) Quadratic trends | 0.007 | 0.003 | [0.001, 0.013] |

**Interpretation**:
- Basic specification shows small positive effects, but these attenuate dramatically with county trends
- Preferred specifications (with trends) show effects near zero and precisely estimated
- 95% CIs exclude large effects in either direction

### Table 3: Participation Outcomes

**Turnout Rate (all 126 counties):**

| Specification | Coefficient | SE | 95% CI |
|---------------|-------------|-----|--------|
| (1) Basic | 0.021 | 0.009 | [0.003, 0.039] |
| (2) Linear trends | 0.022 | 0.007 | [0.008, 0.036] |
| (3) Quadratic trends | 0.021 | 0.008 | [0.005, 0.037] |

**VBM Share (CA only, 58 counties):**

| Specification | Coefficient | SE | 95% CI |
|---------------|-------------|-----|--------|
| (4) Basic | 0.186 | 0.027 | [0.132, 0.240] |
| (5) Linear trends | 0.157 | 0.035 | [0.087, 0.227] |
| (6) Quadratic trends | 0.136 | 0.085 | [-0.034, 0.306] |

**Interpretation**:
- Turnout increases by ~2 percentage points, robust across specifications
- VBM share increases by 14-19 percentage points (voters adopt mail voting when available)

---

## 6. Robustness Checks

### Pre-Trends / Leads Analysis
- Authors estimate coefficients on "leads" (years before adoption)
- No significant pre-adoption divergence, supporting parallel trends assumption

### State-by-State Results
- Results remain "similarly null" across all three states
- Even Washington (most extreme implementation) shows no partisan effects

### Alternative Samples
- Results robust to excluding individual states
- California + Utah only analysis yields similar conclusions

### Compositional Analysis
- Examine effects on voter composition by age, race, party registration
- No significant changes in electorate composition

---

## 7. Key Conclusions

1. **No partisan advantage**: "Claims that VBM fundamentally advantages one party over the other appear overblown"

2. **Modest turnout increase**: VBM increases overall participation by ~2 percentage points

3. **Voters adopt mail voting**: When VBM is available, voters shift from in-person to mail voting

4. **Caveats**:
   - Results apply to "normal times" before COVID-19
   - Cannot extrapolate to nationwide implementation
   - Study examines universal VBM, not no-excuse absentee voting

---

## 8. Implications for Extension

The original paper covers 1996-2018. Key developments since then:

1. **COVID-19 pandemic (2020)**: Dramatically increased VBM usage nationwide; VBM became politically polarizing

2. **California VCA expansion**: Many more counties adopted VCA in 2020, 2022, 2024
   - 2018: 5 counties
   - 2020: +10 counties (15 total)
   - 2022: +12 counties (27 total)
   - 2024: +3 counties (30 total)

3. **Utah and Washington**: Both states were 100% VBM by 2019, so no new variation

**Key question for extension**: Do the null partisan findings hold in the post-COVID era when VBM became politically polarizing?
