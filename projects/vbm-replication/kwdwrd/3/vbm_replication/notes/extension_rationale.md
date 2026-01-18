# Extension Rationale

## 1. What Changed After 2018?

### COVID-19 Pandemic and Emergency VBM Expansion
The 2020 election occurred during the COVID-19 pandemic, fundamentally changing the context for vote-by-mail:
- Many states temporarily expanded mail voting options for health/safety reasons
- Unprecedented numbers of Americans voted by mail in 2020
- In-person voting carried real health risks, particularly for older voters

### VBM Became a Partisan Issue
Unlike the "normal times" analyzed by Thompson et al. (2020), VBM became highly politically charged:
- President Trump repeatedly claimed mail voting would lead to fraud
- Democrats largely supported VBM expansion
- Lockhart et al. (2020) documented a 10-20 percentage point partisan gap in VBM preferences
- This partisan polarization could potentially affect who uses VBM and electoral outcomes

### Continued California Voter's Choice Act Rollout
California provides the primary source of new variation for the extension:

| Year | New VCA Counties | Total VCA Counties | Notes |
|------|------------------|-------------------|-------|
| 2018 | 5 | 5 | Madera, Napa, Nevada, Sacramento, San Mateo |
| 2020 | 10 | 15 | Added: Amador, Butte, Calaveras, El Dorado, Fresno, Los Angeles, Mariposa, Orange, Santa Clara, Tuolumne |
| 2022 | 13 | 28 | Added: Alameda, Humboldt, Kings, Marin, Merced, Riverside, San Benito, San Diego, Santa Cruz, Sonoma, Stanislaus, Ventura, Yolo |
| 2024 | 2 | 30 | Added: Imperial, Placer |

**Key insight**: Los Angeles and Orange Counties—two of California's largest—adopted VCA in 2020, providing substantial new variation.

---

## 2. What New Variation Exists?

### California (Primary Source of Variation)
California offers substantial new treatment variation:
- 25 additional counties adopted VCA between 2020-2024
- VCA counties now comprise ~78% of California's registered voters
- Major population centers (LA, Orange, San Diego) adopted VCA
- Staggered rollout continues the natural experiment

**Available comparisons**:
- VCA counties in 2020 vs. non-VCA counties (within California)
- VCA counties in 2022 vs. non-VCA counties
- Event study around VCA adoption timing

### Utah (Limited New Variation)
- By 2019, all 29 Utah counties had adopted universal VBM
- No new within-state variation for 2020-2024
- Utah serves as an "always treated" comparison group
- Can still contribute to overall estimates but not provide new identifying variation

### Washington (No New Variation)
- Washington has been 100% VBM statewide since 2011
- All 39 counties were already treated throughout the original sample
- Washington serves as an "always treated" state
- Useful for checking that results hold with full saturation

**Summary**: The extension's identifying variation comes almost entirely from California's continued VCA rollout. Utah and Washington provide limited additional information.

---

## 3. Research Questions for the Extension

### Primary Questions

**Q1: Do the null partisan effects hold in the post-COVID period?**
- Thompson et al. found no partisan effects in 1996-2018
- Does this hold for 2020-2024 when VBM became a partisan issue?
- Amlani & Collitt (2022) suggest null effects persist, but with different design

**Q2: Is there evidence of heterogeneous effects by time period?**
- Interaction test: Does VBM × Post-2018 differ from zero?
- If the coefficient on the interaction is significant, effects may have changed

**Q3: Do event study patterns look similar pre- and post-2018?**
- Compare pre-treatment dynamics for early vs. late adopters
- Test whether parallel trends assumption still holds
- Check for anticipation effects or delayed responses

### Secondary Questions

**Q4: Did VBM effects differ in the COVID election year (2020) specifically?**
- 2020 was unprecedented—should we treat it separately?
- Robustness check dropping 2020

**Q5: Are effects different for large vs. small counties?**
- LA and Orange County adoption in 2020 provides high-profile test
- Population-weighted vs. unweighted estimates may differ

---

## 4. Limitations to Acknowledge

### Methodological Limitations

**Less new variation than original paper**:
- Original paper: Staggered adoption across 3 states, 1996-2018
- Extension: Primarily California VCA rollout, 2020-2024
- Fewer treated counties to identify effects from

**Post-2020 period may have different dynamics**:
- VBM is now more common nationwide
- Partisan sorting into VBM vs. in-person voting
- Different voter composition using VBM in post-COVID era

**Cannot separate VBM effects from COVID effects in 2020**:
- 2020 election was unusual in many ways beyond VBM
- Turnout was at historic highs regardless of VBM
- Impossible to isolate VBM effects from other 2020 factors

### Data Limitations

**Potential data availability issues**:
- Recent elections may not have finalized/certified data
- CVAP data based on 2020 Census may not be available for all counties
- Party registration data availability may vary

**Different elections in extension period**:
- 2020: Presidential + California recall (2021)
- 2022: Gubernatorial
- 2024: Presidential
- Need to account for election type in specifications

### Interpretation Limitations

**Generalizability concerns**:
- California is a heavily Democratic state
- VCA is a specific form of VBM (vote centers + mailed ballots)
- Results may not generalize to other states or other VBM systems

**Selection into VCA adoption**:
- Counties chose to adopt VCA—they were not randomly assigned
- Early adopters may differ from late adopters
- Need to examine pre-trends carefully

---

## 5. Expected Findings

Based on prior literature and the nature of the extension, we expect:

1. **Replication will succeed**: Our Python replication should match original Stata results closely

2. **Null partisan effects will persist**: Thompson et al., Amlani & Collitt, and other studies all find null partisan effects. We expect the same.

3. **Modest turnout effects**: ~2 percentage point increase, consistent with prior literature

4. **No significant period heterogeneity**: VBM × Post-2018 interaction likely insignificant

5. **Parallel trends will hold**: Pre-treatment dynamics should be similar for VCA adopters

However, we remain open to surprising findings, particularly given the changed political context around VBM post-2020.

---

## 6. Contribution of the Extension

### What This Adds

1. **Post-COVID test of null partisan effects**: Most rigorous test of whether VBM → partisan advantage in the polarized post-2020 environment

2. **Extended California analysis**: More VCA counties = more statistical power for California-specific effects

3. **Methodological exercise**: Demonstrates Python replication of Stata-based research, valuable for reproducibility

4. **Updated evidence for policy debates**: VBM remains contentious; updated evidence is valuable

### What This Cannot Do

1. Cannot definitively separate VBM effects from COVID effects
2. Cannot speak to VBM effects in other states (only CA, UT, WA)
3. Cannot address concerns about fraud or election integrity (not in the data)
4. Cannot identify mechanisms (why VBM is neutral, not just that it is)
