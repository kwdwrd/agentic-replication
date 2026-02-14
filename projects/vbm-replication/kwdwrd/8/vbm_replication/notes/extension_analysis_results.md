# Extension Analysis Results

## Overview

This document summarizes the extension analysis results for Thompson et al. (2020) using California Voter's Choice Act (VCA) adoption data from 2020-2024.

## Main Findings

### 1. Democratic Presidential Vote Share (2020-2024)

| Outcome | Coefficient | SE | t-stat | p-value | N | Clusters |
|---------|-------------|-----|--------|---------|---|----------|
| Dem Share (Pres) | -0.0134 | 0.0079 | -1.69 | 0.096 | 116 | 58 |

**Interpretation**: VCA adoption is associated with a 1.3 percentage point *decrease* in Democratic presidential vote share, though this is only marginally significant (p=0.096). This is larger in magnitude than the original Thompson et al. finding (-0.001, SE: 0.005) but still consistent with no substantial partisan effect.

### 2. Voter Turnout (2020-2024)

| Outcome | Coefficient | SE | t-stat | p-value | N | Clusters |
|---------|-------------|-----|--------|---------|---|----------|
| Turnout (Pres) | 0.0059 | 0.0065 | 0.90 | 0.373 | 116 | 58 |

**Interpretation**: VCA adoption is associated with a 0.6 percentage point increase in turnout, but this is not statistically significant. This is similar to the original Thompson et al. finding (0.001, SE: 0.006) and confirms that VCA does not substantially increase turnout.

### 3. Gubernatorial Results (2022 Cross-Section)

| Outcome | Coefficient | SE | t-stat | p-value | N |
|---------|-------------|-----|--------|---------|---|
| Dem Share (Gov 2022) | 0.0998 | 0.0411 | 2.43 | 0.018 | 58 |
| Turnout (Gov 2022) | 0.0121 | 0.0238 | 0.51 | 0.613 | 58 |

**Caution**: The gubernatorial results come from a single cross-section (2022) without county fixed effects. The positive coefficient for Democratic vote share likely reflects *selection* - VCA-adopting counties tend to be more Democratic-leaning. This is NOT a causal estimate and should be interpreted with caution.

## Comparison with Original Thompson et al. (2020)

| Outcome | Original (1996-2018) | Extension (2020-2024) |
|---------|---------------------|----------------------|
| Dem Share (Pres) | -0.001 (0.005) | -0.013 (0.008)* |
| Dem Share (Gov) | -0.002 (0.008) | N/A (cross-section only) |
| Dem Share (Sen) | -0.010 (0.009) | N/A |
| Turnout | 0.001 (0.006) | 0.006 (0.007) |

## Key Conclusions

1. **Partisan Effects Remain Null**: Consistent with Thompson et al. (2020), we find no evidence that VCA adoption systematically benefits Democrats in presidential elections. The marginally significant negative coefficient actually suggests, if anything, a small disadvantage for Democrats.

2. **Turnout Effects Remain Null**: VCA adoption does not appear to substantially increase turnout, consistent with the original findings.

3. **COVID-19 Context**: These results span the COVID-19 pandemic period when many jurisdictions expanded mail voting. The null findings suggest that even in this context of heightened VBM usage, partisan effects remain minimal.

4. **Limitations**:
   - Small sample size (58 California counties)
   - Limited temporal variation (only 2020 and 2024 presidential elections)
   - Some counties adopted VCA between elections, creating treatment variation
   - Cannot fully control for county-specific trends with only 2 time periods

## Data Summary

### Treatment Status by Year

| Year | Treated Counties | Control Counties |
|------|-----------------|------------------|
| 2020 | 15 | 43 |
| 2024 | 30 | 28 |

### Mean Outcomes by Treatment Status

| Group | Dem Share (Pres) | Turnout (Pres) |
|-------|-----------------|----------------|
| VCA Counties | 0.55 | 0.75 |
| Non-VCA Counties | 0.47 | 0.68 |
| Difference | 0.08 | 0.07 |

Note: These raw differences reflect selection, not causal effects. VCA-adopting counties tend to be more urban and Democratic-leaning.

## Files Generated

- `output/tables/extension_results.csv`: Regression results
- `output/tables/extension_summary_stats.csv`: Summary statistics by year
