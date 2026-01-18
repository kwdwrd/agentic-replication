# Extension Rationale: Extending Thompson et al. (2020) Through 2024

## 1. What Changed After 2018?

### COVID-19 Pandemic and Emergency VBM Expansion
The COVID-19 pandemic in 2020 fundamentally changed the context for vote-by-mail:
- Many states implemented emergency VBM expansions
- The 2020 general election saw unprecedented mail voting (46% of ballots nationally)
- Public health concerns made mail voting a safety issue, not just convenience

### VBM Became a Partisan Issue
Before 2020, VBM was largely a nonpartisan administrative reform. After 2020:
- President Trump repeatedly claimed VBM was prone to fraud and favored Democrats
- Republican state legislatures restricted mail voting in several states
- Democratic voters became more likely to use mail voting than Republicans
- Partisan polarization on VBM attitudes: 10 pp gap in April 2020 doubled to 20 pp by June 2020 (Stewart et al., 2020)

### Continued California Voter's Choice Act Rollout
California's VCA continued expanding after 2018:

| Year | New VCA Counties | Cumulative Counties |
|------|------------------|---------------------|
| 2018 | 5 (Madera, Napa, Nevada, Sacramento, San Mateo) | 5 |
| 2020 | 10 (Amador, Butte, Calaveras, El Dorado, Fresno, Los Angeles, Mariposa, Orange, Santa Clara, Tuolumne) | 15 |
| 2022 | 12 (Alameda, Kings, Marin, Merced, Riverside, San Benito, San Diego, Santa Cruz, Sonoma, Stanislaus, Ventura, Yolo) | 27 |
| 2024 | 3 (Humboldt, Imperial, Placer) | 30 |

This provides substantial new variation for the extension analysis.

### Utah and Washington: Full Adoption
- **Utah**: By 2019, all 29 counties had adopted universal VBM (remaining 2 counties: Carbon, Emery adopted in 2020)
- **Washington**: Already 100% VBM since 2011

These states provide no new VBM adoption variation but serve as useful comparisons.

---

## 2. What New Variation Exists?

### California: Primary Source of New Variation
California provides the most valuable new variation:
- **25 counties** adopted VCA between 2020-2024 (vs. 5 in original paper)
- **Large counties** included: Los Angeles (10M residents), San Diego, Orange, Riverside
- **Variation in adoption timing**: 2020, 2022, 2024 waves
- **78% of CA voters** now in VCA counties

### Utah: Limited New Variation
- Only 2 counties (Carbon, Emery) adopted VBM after the original study period
- These are small, rural counties
- Limited statistical power for Utah-specific extension

### Washington: No New Variation
- 100% VBM since 2011
- Useful only as a comparison group (always-treated)
- Methodologically, serves as a "fully treated" control

### Summary of New Variation

| State | Original VBM Adopters (by 2018) | New VBM Adopters (2020-2024) | Total |
|-------|--------------------------------|------------------------------|-------|
| California | 5 | 25 | 30 |
| Utah | 27 | 2 | 29 |
| Washington | 39 | 0 | 39 |

---

## 3. Research Questions for the Extension

### Primary Question
**Do the null partisan effects of VBM hold in the post-COVID period?**

The original paper found no partisan effects in 1996-2018. The extension tests whether this finding holds when:
- VBM has become politically polarized
- Differential partisan usage of mail vs. in-person voting exists
- The political context has changed dramatically

### Secondary Questions

1. **Is there evidence of heterogeneous effects by time period?**
   - Compare pre-2018 vs. post-2018 VBM effects
   - Test for interaction: VBM × Post2018

2. **Do event study patterns look similar pre- and post-2018?**
   - Visual inspection of dynamic effects
   - Test for anticipatory effects in new period

3. **Are California's VCA effects consistent with earlier Washington/Utah effects?**
   - California provides most new variation
   - Test whether larger, more diverse counties show different effects

4. **Does the 2020 election show different patterns than 2022/2024?**
   - 2020 was uniquely affected by COVID
   - May want to test sensitivity to dropping 2020

---

## 4. Limitations to Acknowledge

### Less New Variation Than Original Paper
- Original paper: Exploited staggered adoption across all three states over 20+ years
- Extension: Primarily California VCA adoption (Utah/WA fully treated)
- Statistical power may be lower for detecting small effects

### Post-2020 Period May Have Different Dynamics
- Behavioral responses to VBM may have changed
- Republican voters may systematically avoid mail voting
- This could either reveal or mask partisan effects

### Cannot Separate VBM Effects from COVID Effects in 2020
- 2020 election was unprecedented in many ways
- Turnout effects may reflect pandemic mobilization, not VBM
- VBM effects may be confounded with:
  - COVID-related mobilization/demobilization
  - Trump on the ballot
  - Heightened partisan engagement

### Selection into VCA Adoption
- California counties self-selected into VCA
- May be systematic differences (larger, more Democratic counties adopted earlier)
- Diff-in-diff addresses this if parallel trends hold, but should test

### Methodological Considerations
- Staggered DiD literature (Goodman-Bacon, 2021; Callaway & Sant'Anna, 2021) raises concerns about TWFE
- Original paper's estimates may be biased if treatment effects are heterogeneous
- Extension should consider alternative estimators as robustness check

---

## 5. Expected Contributions

### Scientific Contribution
1. **Temporal external validity**: Tests whether null partisan findings generalize beyond "normal times"
2. **Methodological replication**: Confirms original code produces original results
3. **Updated estimates**: Provides estimates for policy-relevant post-COVID period

### Policy Relevance
1. **Informs ongoing VBM debates**: Provides evidence for current policy discussions
2. **Addresses partisan concerns**: Tests whether partisan fears have materialized
3. **California-specific evidence**: Directly relevant to ongoing VCA expansion

### Methodological Contribution
1. **Transparency**: Fully reproducible analysis in Python
2. **Modern methods**: Opportunity to apply recent staggered DiD advances
3. **Data contribution**: Compiled extension dataset for future research
