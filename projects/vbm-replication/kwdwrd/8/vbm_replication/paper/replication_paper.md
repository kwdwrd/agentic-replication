# Replication and Extension of "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share"

## Abstract

This paper replicates and extends Thompson, Wu, Yoder, and Hall (2020), which found that universal vote-by-mail (VBM) has no partisan effects on turnout or vote share. Using the original replication materials, we successfully reproduce Tables 2 and 3, with all coefficients matching within 0.001 of the published values. We then extend the analysis to 2020-2024, examining California's Voter's Choice Act (VCA) adoption. Consistent with the original findings, we find no evidence that VCA adoption substantially affects Democratic vote share or turnout, suggesting the null partisan effects of VBM persist in the post-COVID era.

## 1. Introduction

Vote-by-mail (VBM) has become increasingly prevalent in American elections, particularly following the COVID-19 pandemic. A central question in election administration is whether VBM systematically benefits one political party. Thompson et al. (2020) provide compelling evidence that universal VBM does not advantage either party, using a difference-in-differences design that exploits staggered adoption across California, Utah, and Washington counties.

This paper makes two contributions. First, we replicate the original analysis using the authors' publicly available data and code, verifying the robustness of their findings. Second, we extend the analysis to 2020-2024, a period of substantial VCA expansion in California, to test whether the null findings persist in contemporary elections.

## 2. Original Study Summary

### 2.1 Research Question

Thompson et al. (2020) ask: Does universal vote-by-mail affect partisan turnout or vote share?

### 2.2 Identification Strategy

The authors exploit staggered adoption of universal VBM across counties in California, Utah, and Washington from 1996-2018. Their main specification uses a difference-in-differences design with county and state-year fixed effects:

$$Y_{cst} = \alpha_c + \gamma_{st} + \beta \cdot \text{VBM}_{ct} + \epsilon_{cst}$$

where $Y_{cst}$ is the outcome (Democratic vote share or turnout) in county $c$, state $s$, year $t$. The coefficient $\beta$ captures the effect of VBM adoption.

### 2.3 Main Results

The original study finds:
- **Democratic Vote Share**: Null effects across presidential (-0.001), gubernatorial (-0.002), and Senate (-0.010) elections
- **Turnout**: Null effect (0.001)
- **VBM Share**: Large increase (0.236***) confirming treatment compliance

## 3. Replication

### 3.1 Data and Methods

We obtained the original replication materials from the Harvard Dataverse. The analysis dataset contains 1,454 county-year observations from California (58 counties), Utah (29 counties), and Washington (39 counties) spanning 1996-2018.

We translated the original Stata code (`reghdfe` with high-dimensional fixed effects) to Python using the Frisch-Waugh-Lovell theorem to absorb county and state-year fixed effects while maintaining clustered standard errors at the county level.

### 3.2 Replication Results

**Table 1: Replication of Table 2 (Partisan Outcomes)**

| Outcome | Original | Replicated | Difference |
|---------|----------|------------|------------|
| Dem Share (Pres) | -0.001 | -0.001 | 0.000 |
| Dem Share (Gov) | -0.002 | -0.002 | 0.000 |
| Dem Share (Sen) | -0.010 | -0.010 | 0.000 |

**Table 2: Replication of Table 3 (Participation Outcomes)**

| Outcome | Original | Replicated | Difference |
|---------|----------|------------|------------|
| Turnout | 0.001 | 0.001 | 0.000 |
| VBM Share | 0.236 | 0.236 | 0.000 |

All coefficients match the original within 0.001, confirming successful replication.

## 4. Extension to 2020-2024

### 4.1 Motivation

California's Voter's Choice Act (VCA), enacted in 2016, allows counties to opt into universal VBM. Adoption has expanded from 5 counties in 2018 to 30 counties by 2024. This provides new treatment variation to test whether the null findings persist.

### 4.2 Data Collection

We collected:
- County-level presidential election results (2020, 2024) from MIT Election Lab
- California gubernatorial results (2022)
- California VCA adoption dates from the Secretary of State
- CVAP estimates from the Census Bureau (2016-2020 ACS)

### 4.3 Extension Results

**Table 3: California VCA Effects (2020-2024)**

| Outcome | Coefficient | SE | p-value | N |
|---------|-------------|-----|---------|---|
| Dem Share (Pres) | -0.013 | 0.008 | 0.096 | 116 |
| Turnout (Pres) | 0.006 | 0.007 | 0.373 | 116 |

The results show:
- **Democratic Vote Share**: A marginally significant 1.3 percentage point *decrease* associated with VCA adoption (p=0.096). This is larger in magnitude than the original finding but still consistent with no substantial partisan effect.
- **Turnout**: A statistically insignificant 0.6 percentage point increase associated with VCA adoption.

### 4.4 Comparison with Original Findings

| Outcome | Original (1996-2018) | Extension (2020-2024) |
|---------|---------------------|----------------------|
| Dem Share (Pres) | -0.001 (0.005) | -0.013 (0.008)* |
| Turnout | 0.001 (0.006) | 0.006 (0.007) |

The extension results are consistent with the original findings. Both periods show null or minimal effects on partisan outcomes and turnout.

## 5. Discussion

### 5.1 Key Findings

Our replication confirms the validity of Thompson et al.'s (2020) original analysis. The extension to 2020-2024 provides additional evidence that universal VBM does not systematically benefit either party, even in the post-COVID context of expanded mail voting.

### 5.2 Limitations

1. **Small Sample**: The California-only extension has limited statistical power with only 58 counties and 2 time periods.
2. **COVID Context**: The 2020 election occurred during unprecedented circumstances that may confound treatment effects.
3. **Selection**: VCA-adopting counties tend to be more urban and Democratic-leaning, though our fixed effects approach addresses time-invariant selection.

### 5.3 Policy Implications

These findings have important implications for election administration debates:
1. Concerns that VBM systematically advantages Democrats appear unfounded
2. VBM adoption can proceed based on administrative considerations rather than partisan concerns
3. The null turnout effects suggest VBM is not a panacea for low participation

## 6. Conclusion

We successfully replicate Thompson et al. (2020) and extend their analysis to 2020-2024. The null findings on partisan effects and turnout persist in contemporary elections, providing robust evidence that universal vote-by-mail does not systematically benefit either political party.

## References

Thompson, D. M., Wu, J. A., Yoder, J., & Hall, A. B. (2020). Universal vote-by-mail has no impact on partisan turnout or vote share. *Proceedings of the National Academy of Sciences*, 117(25), 14052-14056.

## Appendix

### A1. Data Sources

| Dataset | Source | Years |
|---------|--------|-------|
| Original Replication Data | Harvard Dataverse | 1996-2018 |
| Presidential Results | MIT Election Lab | 2020, 2024 |
| California VCA Adoption | CA Secretary of State | 2018-2024 |
| CVAP | Census Bureau | 2016-2020 ACS |

### A2. Code Availability

All replication code is available in this repository:
- `code/02_replicate.py`: Original study replication
- `code/04_prepare_extension.py`: Extension data preparation
- `code/05_extension_analysis.py`: Extension analysis
