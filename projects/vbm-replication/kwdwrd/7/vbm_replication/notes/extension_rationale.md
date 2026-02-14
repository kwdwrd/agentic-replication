# Extension Rationale

## Overview

This document explains the motivation, research questions, and limitations of extending Thompson et al. (2020) from 2018 to 2024.

---

## 1. What Changed After 2018?

### 1.1 COVID-19 Pandemic and Emergency VBM Expansion

The COVID-19 pandemic fundamentally altered the landscape of vote-by-mail in the United States:

- **Spring 2020**: Many states expanded VBM access for primary elections as emergency public health measure
- **Fall 2020**: Record numbers of Americans voted by mail (46% of total votes, up from 24% in 2016)
- **Partisan messaging**: VBM became highly politicized, with President Trump repeatedly claiming mail voting would lead to "massive fraud"

**Key question**: Did the pandemic-era politicization of VBM change its causal effects on partisan outcomes?

### 1.2 VBM Becoming a Partisan Issue

Before 2020, VBM was relatively non-partisan:
- Oregon (all-mail since 2000) is a blue state
- Utah (majority-mail by 2019) is a red state
- Both parties used VBM without major controversy

After 2020:
- Strong partisan gap in VBM preferences emerged (~20 pp difference)
- In 2020, 59% of Democrats voted by mail vs. only 30% of Republicans
- VBM became associated with Democratic voting in public discourse

### 1.3 Continued California Voter's Choice Act Rollout

California's Voter's Choice Act provides the primary source of new treatment variation:

| Year | VCA Counties | New Adopters |
|------|--------------|--------------|
| 2018 | 5 | Madera, Napa, Nevada, Sacramento, San Mateo |
| 2020 | 15 | +10 counties including Los Angeles, Orange, Santa Clara |
| 2022 | ~30 | Additional counties joined |
| 2024 | ~40+ | Further expansion |

The California rollout continues to provide staggered adoption that can be used for difference-in-differences identification.

---

## 2. What New Variation Exists?

### 2.1 California: Primary Source of New Variation

California is the key state for the extension because:

1. **Continued VCA rollout**: Counties continued opting into VCA through 2024
2. **Large population**: California has 58 counties with substantial vote totals
3. **Policy variation**: Unlike UT and WA, not yet 100% adopted

**New treated observations in California**:
- 2018: 5 counties × 1 election = 5 treated county-elections
- 2020: 15 counties × 1 election = 15 treated county-elections
- 2022: ~30 counties × 1 election = ~30 treated county-elections
- 2024: ~40 counties × 1 election = ~40 treated county-elections

### 2.2 Utah: Limited New Variation

Utah moved to 100% vote-by-mail by 2019-2020:
- All 29 counties now conduct elections by mail
- No new within-state variation available
- Still useful as always-treated comparison group

**Status**:
- 2 counties adopted in 2020, completing statewide adoption
- No new variation after 2020

### 2.3 Washington: No New Variation

Washington has been 100% vote-by-mail since 2011:
- All 39 counties use VBM
- No new variation since original study period
- Useful only as always-treated comparison group

**Status**: No change since 2011

### 2.4 Summary of New Variation

| State | 2020 | 2022 | 2024 | Total New Variation |
|-------|------|------|------|---------------------|
| California | +10 counties | +15 counties | +10 counties | Substantial |
| Utah | +2 counties (completes) | None | None | Minimal |
| Washington | None | None | None | None |

**Implication**: The extension primarily tests California's continued VCA rollout. Results for Utah and Washington will reflect post-2018 outcome changes for always-treated counties, not new treatment effects.

---

## 3. Research Questions for the Extension

### 3.1 Primary Research Question

**Do the null partisan effects of VBM hold in the post-COVID period?**

Thompson et al. (2020) found that VBM had essentially zero effect on:
- Democratic share of turnout
- Democratic vote share

The extension tests whether these null findings persist in an era when VBM has become highly politicized.

### 3.2 Secondary Research Questions

1. **Is there evidence of heterogeneous effects by time period?**
   - Do VBM effects differ between 1996-2018 and 2020-2024?
   - Can we detect a structural break around COVID?

2. **Do event study patterns look similar pre- and post-2018?**
   - Are pre-trends flat in both periods?
   - Are post-treatment dynamics similar?

3. **Are effects driven by California specifically?**
   - California provides most new variation
   - Do California-specific estimates differ from pooled estimates?

4. **Does the 2020 election show different patterns?**
   - 2020 was unusual (pandemic, high turnout, polarization)
   - Sensitivity analysis dropping 2020

---

## 4. Limitations to Acknowledge

### 4.1 Less New Variation Than Original Paper

The original paper (1996-2018) had substantial staggered variation:
- Utah: Counties adopting 2012-2018
- Washington: Counties adopting 2005-2011
- California: 5 counties in 2018

The extension (2020-2024) has more limited variation:
- Utah: Essentially complete by 2020
- Washington: Complete since 2011
- California: Continued adoption, but from higher baseline

**Implication**: Statistical power for detecting effects may be lower in the extension period.

### 4.2 Post-2020 Period May Have Different Dynamics

Several factors make 2020-2024 potentially different from 1996-2018:

1. **Partisan sorting by voting method**: Democrats and Republicans may now systematically choose different voting methods regardless of VBM availability

2. **Selection into VBM adoption**: Counties that adopted VCA later may differ systematically from early adopters

3. **Changed salience**: VBM was a low-salience issue before 2020; now highly salient

### 4.3 Cannot Separate VBM Effects from COVID Effects in 2020

The 2020 election occurred during a pandemic that affected turnout in multiple ways:
- Health concerns may have changed turnout decisions
- In-person voting was seen as risky
- Mobilization efforts differed dramatically

**Implication**: Effects estimated for 2020 may reflect COVID impacts, not VBM policy impacts. Sensitivity analyses dropping 2020 are important.

### 4.4 Staggered DiD Concerns

Recent econometrics literature (Goodman-Bacon 2021; Callaway and Sant'Anna 2021; Sun and Abraham 2021) highlights potential problems with two-way fixed effects estimators in staggered adoption settings:

1. **Forbidden comparisons**: TWFE may compare newly-treated to already-treated units
2. **Heterogeneous effects**: If effects vary over time, TWFE can be biased
3. **Negative weights**: Some treatment effects may receive negative weight

**Implication**: Extension analysis should consider modern DiD estimators as robustness checks.

### 4.5 Limited Generalizability

The analysis covers only three states:
- California, Utah, Washington are not nationally representative
- All three are Western states
- Results may not generalize to states with different political contexts or electoral infrastructure

---

## 5. Hypotheses and Predictions

### 5.1 Null Hypothesis (Based on Prior Literature)

**H0**: VBM continues to have null effects on partisan outcomes in the post-COVID period.

Rationale:
- The policy mechanism (mailing ballots) hasn't changed
- If partisan balance results from offsetting effects on different voter groups, this should persist
- Barber and Holbein (2020) and Amlani and Collitt (2022) found null effects in 2020

### 5.2 Alternative Hypothesis

**H1**: VBM effects on partisan outcomes may differ in the post-COVID period.

Possible mechanisms:
- Partisan sorting: Democrats may disproportionately use VBM when available, changing composition
- Mobilization: Party mobilization strategies may have adapted to VBM availability
- Selection: Late VCA adopters may differ from early adopters

### 5.3 Expected Findings

Based on the literature and theoretical considerations:

1. **Turnout effects**: Expect continued positive effect (~2 pp) on turnout
2. **VBM share effects**: Expect continued large positive effect on VBM usage
3. **Partisan effects**: Expect null effects, consistent with original paper
4. **Heterogeneity**: Possible that 2020 shows different patterns due to pandemic

---

## 6. Contribution of the Extension

### 6.1 What This Adds to Knowledge

1. **Post-COVID evidence**: First systematic extension of Thompson et al. to post-pandemic period
2. **Continued California rollout**: Tests whether effects change as more counties adopt VCA
3. **Methodological exercise**: Demonstrates replication and extension workflow

### 6.2 Policy Relevance

1. **Ongoing VBM debates**: Evidence on whether VBM remained electorally neutral during partisan polarization
2. **Future policy decisions**: Whether states should expand or restrict VBM
3. **Election administration**: Understanding how voting methods affect participation

### 6.3 Limitations of Contribution

1. **Descriptive, not causal, for some analyses**: With less new variation, some analyses will be more descriptive
2. **Single study**: Findings should be considered alongside other post-2020 VBM research
3. **Western states only**: Limited geographic scope
