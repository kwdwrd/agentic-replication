# Extension Rationale: Extending Thompson et al. (2020) through 2024

This document explains the motivation for extending the original analysis from 1996-2018 to include elections through 2024.

---

## 1. What Changed After 2018?

### COVID-19 Pandemic and Emergency VBM Expansion
The COVID-19 pandemic fundamentally transformed the landscape of American elections:

- **Emergency expansions**: Many states temporarily expanded VBM access for the 2020 election to reduce COVID-19 transmission at polling places
- **Record VBM usage**: The share of voters using convenience voting jumped by 29.3 percentage points between 2016 and 2020
- **Partisan polarization around VBM**: Former President Trump and Republican officials opposed VBM expansion, while Democrats supported it, making VBM a partisan issue for the first time

### VBM Becoming a Partisan Issue
Prior to 2020, VBM was largely a nonpartisan administrative matter. The pandemic changed this:

- **Partisan messaging**: 59% of Democrats voted by mail in 2020 compared to only 30% of Republicans
- **Legal battles**: Republicans challenged VBM expansions in court
- **Legitimacy concerns**: Claims of VBM fraud became central to post-election disputes

This partisan polarization around VBM raises important questions: Do the null partisan findings from Thompson et al. (2020) hold when VBM itself has become partisan?

### Continued California Voter's Choice Act Rollout
California provides substantial new treatment variation for the extension:

**VCA Adoption Timeline**:

| Year | Counties Adopting | Cumulative Counties |
|------|-------------------|---------------------|
| 2018 | 5 (Madera, Napa, Nevada, Sacramento, San Mateo) | 5 |
| 2020 | 9 (Amador, Butte, Calaveras, El Dorado, Fresno, Los Angeles, Mariposa, Orange, Santa Clara, Tuolumne) | 14-15 |
| 2022 | Additional counties | ~20+ |
| 2024 | Additional counties | 29-30 |

This continued rollout provides the primary source of new treatment variation for the extension.

---

## 2. What New Variation Exists?

### California: Primary Source of New Variation
California's staggered VCA adoption continues to provide within-state variation:

- **2020**: Major additions including Los Angeles County (largest county in US) and Orange County
- **2022**: Additional county adoptions
- **2024**: Further expansion to approximately 30 counties

The VCA model mails every registered voter a ballot and establishes vote centers, making it a strong form of universal VBM.

### Utah: Limited New Variation
- By 2018-2019, nearly all Utah counties had adopted universal VBM
- Only 2 counties (Carbon, Emery) adopted in 2020
- **Implication**: Utah provides comparison counties but minimal new treatment variation post-2018

### Washington: No New Variation
- Washington has been 100% VBM statewide since 2011
- All 39 counties were treated before the extension period
- **Implication**: Washington serves as a fully-treated comparison but provides no new variation

### Summary of New Variation
| State | New Treatment Variation 2020-2024 | Role in Extension |
|-------|-----------------------------------|-------------------|
| California | Substantial (15+ new VCA counties) | Primary analysis |
| Utah | Minimal (2 counties in 2020) | Supporting comparison |
| Washington | None (fully treated since 2011) | Control comparison |

---

## 3. Research Questions for the Extension

### Primary Research Question
**Do the null partisan effects documented by Thompson et al. (2020) hold in the post-COVID period (2020-2024)?**

This is the central question motivating the extension. The original study found no partisan effects in "normal times" but explicitly noted that effects might differ during COVID-19.

### Secondary Research Questions

1. **Is there evidence of heterogeneous effects by time period?**
   - Does VBM have different effects pre-2018 vs. post-2018?
   - Can we detect changes in the VBM-partisan relationship after VBM became politically polarized?

2. **Do event study patterns look similar pre- and post-2018?**
   - Are pre-trends similar in both periods?
   - Are treatment effects of similar magnitude?

3. **Does the continued California VCA rollout show similar patterns?**
   - Do the large 2020 adopters (LA, Orange) show similar effects to the 2018 pioneers?
   - Are there heterogeneous effects by county characteristics?

4. **How does the turnout effect compare to pre-2018?**
   - Does the ~2 percentage point turnout increase persist?
   - Did pandemic-era VBM expansions have larger turnout effects?

---

## 4. Limitations to Acknowledge

### Less New Variation Than Original Paper
The original paper benefited from extensive staggered adoption across all three states over many years. The extension has:
- Most variation coming from California only
- Utah and Washington contributing minimal new identification
- Fewer pre-treatment periods for new adopters

### Cannot Separate VBM Effects from COVID Effects in 2020
The 2020 election was unprecedented in many ways:
- Pandemic conditions fundamentally altered voting behavior
- Both parties mobilized intensively around VBM
- Turnout was historically high regardless of voting method

**Implication**: Any estimated VBM effects in 2020 may be confounded with pandemic effects. The extension can test whether effects in 2022 and 2024 (post-pandemic) differ from 2020.

### Post-2020 Period May Have Different Dynamics
Several factors suggest the post-2020 VBM environment differs from pre-2020:
- VBM is now politically polarized
- Many states implemented new VBM restrictions
- Voter behavior may have permanently shifted

### California-Specific Results May Not Generalize
Since California provides most of the new variation, findings may be specific to:
- California's political environment
- VCA's specific implementation features
- Western US context

### Potential for Treatment Effect Heterogeneity
Recent methodological work (Goodman-Bacon 2021; Callaway & Sant'Anna 2021) shows that two-way fixed effects estimators can be biased when treatment effects vary across cohorts. This is relevant because:
- Early adopters (2018 VCA counties) may have different effects than late adopters (2020-2024)
- Pandemic-era adopters may face different conditions than pre-pandemic adopters

---

## 5. Expected Contributions of the Extension

Despite these limitations, the extension will provide:

1. **First rigorous test of VBM effects in post-COVID period**
   - Literature has been largely descriptive about 2020
   - This will be among the first causal analyses extending past 2020

2. **Evidence on whether VBM's partisan neutrality persists**
   - The original finding of null partisan effects was influential
   - Testing whether this holds post-polarization is policy-relevant

3. **Updated estimates incorporating major new adopters**
   - Los Angeles County alone has more voters than many states
   - Including these large counties improves external validity

4. **Methodological template for future VBM research**
   - Demonstrates how to extend published analyses
   - Provides replication code that others can build on

---

## 6. Data Requirements for Extension

### Election Results Needed

| State | Elections | Years | Office |
|-------|-----------|-------|--------|
| California | General | 2020, 2022, 2024 | President, Governor, Senator |
| Utah | General | 2020, 2022, 2024 | President, Senator |
| Washington | General | 2020, 2022, 2024 | President, Senator |

### VBM Policy Data Needed

- California VCA adoption dates for all 58 counties
- Verification that Utah/Washington remained 100% VBM
- Any county-level policy changes

### Demographic Data Needed

- Updated CVAP (Citizen Voting Age Population) from 2020 Census
- Consistent with original paper's turnout denominator

### Voter File Data (If Available)

- California and Utah voter files for partisan turnout share
- Note: This may be difficult to obtain
