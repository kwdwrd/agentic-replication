# Extension Rationale

## 1. What Changed After 2018?

### COVID-19 Pandemic and Emergency VBM Expansion

The 2020 general election was conducted in the midst of the COVID-19 pandemic, which triggered widespread emergency expansions of mail voting nationwide. Several states mailed all registered voters a ballot for the first time, and many others adopted no-excuse absentee voting. The pandemic fundamentally altered the context of VBM:

- **Dramatic increase in mail voting nationally**: In 2020, approximately 46% of all ballots were cast by mail, up from approximately 24% in 2016 (US Census Bureau CPS November Supplement).
- **Emergency adoption**: States like New Jersey, Nevada, and Vermont mailed ballots to all registered voters for the first time.
- **Behavioral shift**: Even in states where VBM was already available, usage rates surged as voters sought to avoid in-person exposure.

### VBM Becoming a Partisan Issue

Before 2020, VBM was a relatively nonpartisan issue in election administration. The COVID-19 era sharply changed this:

- President Trump repeatedly claimed (without evidence) that mail voting was rife with fraud and would disadvantage Republicans.
- Lockhart et al. (2020) documented a near-doubling of the partisan gap in VBM preferences between April and June 2020.
- In the 2020 election, Democrats voted by mail at dramatically higher rates than Republicans, while Republicans favored in-person voting—a behavioral divergence that had not existed at this scale before.
- This partisan divergence in *mode of voting* raised the question of whether VBM's previously null partisan *effects* would persist.

### Continued California Voter's Choice Act Rollout

California's Voter's Choice Act (VCA), signed in 2016, allowed counties to opt in to a new election administration model where every registered voter is mailed a ballot and traditional polling places are replaced by vote centers. The rollout has been staggered:

- **2018**: 5 pilot counties (Madera, Napa, Nevada, Sacramento, San Mateo)
- **2020**: Additional counties adopted VCA
- **2022**: More counties joined
- **2024**: Near-universal adoption

This continued rollout provides the primary source of new within-state variation for the extension.

## 2. What New Variation Exists?

### California: Primary Source of New Variation

California is the key state for the extension because it still has variation in VCA adoption across counties in the 2020–2024 period. However, this variation is limited:

- By 2020, most large counties had adopted VCA
- By 2024, nearly all eligible counties have adopted
- The remaining variation comes from the timing of adoption in mid-sized and smaller counties

This means the extension's identifying variation is narrower than the original paper's, which benefited from the extensive staggered adoption in Washington (1996–2011) and Utah (2012–2018).

### Utah: No New Variation

Utah completed its transition to 100% vote-by-mail by 2019. All 29 counties conduct all-mail elections. There is no new treatment variation—Utah is a "fully treated" state for the extension period. Utah election results are still useful as treated observations but cannot identify the VBM effect on their own.

### Washington: No New Variation

Washington completed its transition to 100% VBM with a 2011 law. All 39 counties are treated throughout the extension period. Like Utah, Washington provides treated observations but no new identifying variation.

### Summary of Available Variation

| State | Original period variation | Extension period variation |
|-------|--------------------------|--------------------------|
| California | 5 VCA counties in 2018 vs. 53 non-VCA | Some counties switch in 2020/2022/2024 vs. non-VCA counties |
| Utah | Staggered adoption 2012–2018 across 29 counties | No new variation (100% VBM since 2019) |
| Washington | Staggered adoption 1996–2011 across 39 counties | No new variation (100% VBM since 2011) |

## 3. Research Questions for the Extension

### Primary Questions

1. **Do the null partisan effects hold in the post-COVID period?**
   - The original paper found VBM does not affect partisan turnout share or vote share. Does this hold when VBM is adopted in a politically polarized environment?
   - Extension tests this using California's continued VCA rollout (2020–2024).

2. **Is there evidence of heterogeneous effects by time period?**
   - Estimate models with VBM × Post-2018 interaction terms.
   - β₂ in the model Y = β₁(VBM) + β₂(VBM × Post2018) + ... tests whether the VBM effect changed.
   - A significant β₂ would suggest the post-COVID context altered VBM's effects.

3. **Do event study patterns look similar pre- and post-2018?**
   - For California VCA adopters, plot event study coefficients around the adoption year.
   - Compare the pattern for 2018 adopters (pre-COVID) vs. 2020+ adopters (peri/post-COVID).

### Secondary Questions

4. **What are the turnout effects of VBM in the post-COVID period?**
   - The original ~2 pp turnout effect may differ when baseline turnout is high (2020 was record turnout) or when the electorate has already adapted to mail voting.

5. **Do the results differ for California specifically?**
   - California-only analysis isolates the VCA expansion effect with the most variation.

## 4. Limitations to Acknowledge

### Less New Variation Than Original Paper

The original paper benefited from Washington's extensive staggered adoption (1996–2011) across all 39 counties, providing hundreds of treated observations with clean pre/post comparisons. The extension relies primarily on California's VCA rollout, which involves fewer switching counties in a shorter time span. This reduces statistical power and precision.

### Cannot Separate VBM Effects from COVID Effects in 2020

The 2020 election was unprecedented in many ways beyond VBM expansion: record turnout driven by intense political mobilization, pandemic-induced behavioral changes, and dramatic shifts in how people vote (even in non-VBM counties, absentee/mail voting surged). It is impossible to cleanly separate the effect of a county switching to VCA from the broader 2020 election environment.

A key robustness check is to drop 2020 from the extension sample and focus on 2022 and 2024, which represent more "normal" election environments.

### Post-2020 Period May Have Different Dynamics

Even after COVID-19 subsided, the partisan polarization around mail voting persisted. Republicans remain more skeptical of VBM and less likely to use it, while Democrats embrace it. This changed behavioral landscape means the *mechanism* through which VBM affects outcomes may differ from the pre-2020 period, even if the net effect remains null.

### Potential Changes in County Composition

Redistricting after the 2020 Census, demographic shifts, and migration patterns (especially in California) may confound comparisons across the 2018–2024 period. County fixed effects control for time-invariant characteristics, but the composition of a county's electorate may change in ways correlated with VCA adoption.

### Data Comparability Across Periods

Extending the analysis requires constructing comparable variables across periods. Key concerns:
- CVAP estimates come from different Census/ACS vintages (pre-2020 from 2010-based estimates, post-2020 from 2020-based estimates)
- Election result formats may differ across California's changing data systems
- Voter file formats and party registration coding may change

## 5. What This Extension Adds

Despite these limitations, the extension provides value in several ways:

1. **Post-COVID evidence**: The literature has extensive evidence from 2020 specifically (Yoder et al. 2021, McGhee et al. 2022) but less on whether the null partisan effects persist in subsequent elections (2022, 2024) as mail voting normalizes.

2. **Methodological exercise**: Replicating and extending a published paper tests the robustness of the original findings to new data and demonstrates the value of pre-registered designs.

3. **California VCA evaluation**: The continued VCA rollout provides a policy-relevant natural experiment. Understanding VCA's effects matters for California election administration and for other states considering similar reforms.

4. **Updated effect sizes**: Even if we cannot precisely identify VBM effects in the extension period, comparing the magnitude of coefficients across periods is informative about the stability of the null finding.
