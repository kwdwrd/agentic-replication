# Extension Rationale

## What Changed After 2018?

The original Thompson et al. (2020) paper analyzes data through 2018. Several major developments since then warrant extending the analysis:

### 1. COVID-19 Pandemic and Emergency VBM Expansion (2020)

The COVID-19 pandemic fundamentally changed the landscape of mail voting in America:

- **Emergency expansions**: Many states temporarily expanded VBM access for the 2020 election
- **Dramatic usage increase**: Mail voting share surged nationwide in 2020
- **Health considerations**: In-person voting carried real or perceived health risks

### 2. VBM Became a Partisan Issue

Before 2020, VBM was largely viewed as a nonpartisan election administration choice. This changed dramatically:

- **Presidential rhetoric**: President Trump repeatedly claimed without evidence that VBM would lead to fraud and prevent Republicans from winning
- **Partisan polarization**: Surveys found a nearly 20 percentage point gap between Democrats and Republicans in VBM preferences by mid-2020
- **Behavioral sorting**: Democrats became much more likely to vote by mail; Republicans more likely to vote in person
- **January 6, 2021**: The 2020 election and its mail voting provisions became central to political conflict

### 3. Continued California Voter's Choice Act Rollout

California provides the key new treatment variation for this extension:

| Election Cycle | Counties Adopting VCA | Cumulative Total | Share of CA Voters |
|----------------|----------------------|------------------|-------------------|
| 2018 | 5 | 5 | ~15% |
| 2020 | 10 | 15 | ~50% |
| 2022 | 12 | 27 | ~70% |
| 2024 | 3 | 30 | ~78% |

**VCA Adoption by Year:**

*2018 (5 counties):*
- Madera, Napa, Nevada, Sacramento, San Mateo

*2020 (10 additional counties):*
- Amador, Butte, Calaveras, El Dorado, Fresno, Los Angeles, Mariposa, Orange, Santa Clara, Tuolumne

*2022 (12 additional counties):*
- Humboldt, Imperial, Kings, Marin, Merced, Placer, Riverside, San Benito, San Diego, Santa Cruz, Sonoma, Stanislaus

*2024 (3 additional counties):*
- Alameda, Ventura, Yolo

### 4. Utah and Washington: No New Variation

Both states were fully VBM by 2019:
- **Utah**: All 29 counties were using all-mail voting by 2019
- **Washington**: Has been 100% VBM statewide since 2011

These states contribute to the analysis as fully-treated units but do not provide new treatment variation for identification.

---

## What New Variation Exists?

### California: Primary Source of Extension Variation

California provides substantial new variation:

**Treated observations (VCA adoption):**
- 5 counties × 3 elections (2020, 2022, 2024) = 15 newly treated obs from 2018 cohort
- 10 counties × 2 elections (2022, 2024) = 20 newly treated obs from 2020 cohort
- 12 counties × 1 election (2024) = 12 newly treated obs from 2022 cohort
- 3 counties × 0 post-treatment elections = 0 from 2024 cohort

**Control observations (non-VCA):**
- The remaining non-VCA counties serve as controls
- Control pool shrinks over time as more counties adopt

### Identification Challenges

1. **Diminishing control group**: By 2024, only 28 CA counties remain non-VCA
2. **Selection into adoption**: Counties that adopt VCA may differ systematically from those that don't
3. **COVID confounding**: The 2020 election cannot cleanly separate VBM effects from pandemic effects

---

## Research Questions for the Extension

### Primary Question
**Do the null partisan effects found by Thompson et al. (2020) hold in the post-COVID period (2020-2024)?**

Hypotheses:
- **H0 (Null hypothesis)**: VBM continues to have no systematic partisan effects
- **H1a**: VBM now favors Democrats (due to partisan sorting into vote mode)
- **H1b**: VBM now favors Republicans (if expanded access mobilizes rural/conservative areas)

### Secondary Questions

1. **Is there evidence of heterogeneous effects by time period?**
   - Test whether the VBM coefficient differs significantly between 1996-2018 and 2020-2024
   - Estimate VBM × Post2018 interaction

2. **Do event study patterns look similar across periods?**
   - Compare pre-trend coefficients before vs. after 2018
   - Examine if treatment effect dynamics have changed

3. **Are California-specific effects consistent with overall findings?**
   - California is the only state with new variation
   - Test robustness to California-only analysis

---

## Limitations to Acknowledge

### 1. Less New Variation Than Original Paper

The original paper benefited from:
- Washington's staggered 2005-2011 rollout (39 counties, many adoption events)
- Utah's staggered 2004-2019 rollout (29 counties, many adoption events)
- California's 2018 VCA pilot (5 counties)

The extension has:
- Only California providing new variation
- Utah and Washington fully treated (no new identifying variation)
- Fewer "clean" adoption events to identify effects

### 2. Post-2020 Period May Have Different Dynamics

The political environment has changed:
- VBM is now politically polarizing
- Voters may sort into vote mode based on partisanship
- This could create compositional changes even without turnout effects

### 3. Cannot Separate VBM Effects from COVID Effects in 2020

The 2020 election presents unique challenges:
- Many voters changed behavior due to pandemic, regardless of VBM policies
- Turnout surged to historic levels
- Partisan composition of voters differed from typical elections

**Implication**: The 2020 election may need to be analyzed separately or excluded in robustness checks.

### 4. Potential for Ceiling Effects

With most CA counties now using VCA:
- VBM share may be approaching ceiling in treated counties
- Marginal effects of adoption may differ from early adopters
- Late adopters may be systematically different

---

## Extension Design Summary

### Data to Collect

| State | Elections | Counties | Treatment Variation |
|-------|-----------|----------|---------------------|
| California | 2020, 2022, 2024 | 58 | Yes (VCA rollout) |
| Utah | 2020, 2022, 2024 | 29 | No (already 100% VBM) |
| Washington | 2020, 2022, 2024 | 39 | No (already 100% VBM) |

### Analyses to Conduct

1. **Full sample estimation** (1996-2024)
   - Compare to original 1996-2018 results

2. **Period heterogeneity tests**
   - VBM × Post2018 interactions
   - Separate estimates by period

3. **California-specific analysis**
   - Exploit continued VCA rollout
   - Event study around VCA adoption

4. **Robustness checks**
   - Exclude 2020 (COVID year)
   - Different fixed effects structures
   - Comparison to Callaway-Sant'Anna estimator

### Expected Findings

Based on prior literature and theory:

1. **Partisan effects**: Likely to remain null or small
   - Even post-COVID studies find no partisan advantage
   - Partisan sorting into vote mode ≠ partisan turnout advantage

2. **Turnout effects**: May be smaller than original estimates
   - Novelty effects may have dissipated
   - 2020 turnout surge confounds estimation

3. **VBM share effects**: Mechanical increase continues
   - Voters adopt mail voting when offered
   - Effect may be larger in extension due to COVID habituation

---

## Contribution of This Extension

### Academic Contribution

1. **External validity test**: Does the null finding replicate in new data?
2. **Temporal stability**: Are VBM effects stable over time?
3. **Post-COVID evidence**: First extension of Thompson et al. methodology to 2020-2024

### Policy Contribution

1. **Inform ongoing VBM debates**: Provide updated evidence for policymakers
2. **Address partisan concerns**: Test whether politicization of VBM changed its effects
3. **California-specific insights**: Relevant for largest state's continued VCA expansion
