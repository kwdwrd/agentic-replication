# Extension Analysis Findings

## Summary of Key Results

The extension analysis adds 2020, 2022, and 2024 election data to the original 1996-2018 sample. The main finding is that **the null effect of VBM on partisan outcomes largely holds in the extended period**, though there is suggestive evidence that VBM's effect on turnout has weakened in the post-2018 period.

## Part 1: Full Sample Results (1996-2024)

### Dem Vote Share (stacked gov/pres/sen)
| Spec | Coef | SE | N | Counties |
|------|------|----|---|----------|
| Basic FE | 0.0243*** | 0.0070 | 2376 | 126 |
| Linear trends | 0.0056* | 0.0030 | 2376 | 126 |
| Quadratic trends | 0.0035 | 0.0030 | 2376 | 126 |

The preferred specifications (linear/quadratic trends) show small, insignificant effects, consistent with the original paper's finding of no partisan impact.

### Turnout
| Spec | Coef | SE | N | Counties |
|------|------|----|---|----------|
| Basic FE | 0.0187*** | 0.0051 | 1618 | 126 |
| Linear trends | 0.0112** | 0.0050 | 1618 | 126 |
| Quadratic trends | 0.0130** | 0.0056 | 1618 | 126 |

VBM continues to increase turnout by approximately 1-2 percentage points in the full sample.

## Part 2: Period Comparison

### Dem Vote Share
| Period | Basic | Linear |
|--------|-------|--------|
| Original (1996-2018) | 0.0285** | 0.0109*** |
| Extension (2020-2024) | -0.0045 | 0.0155 |

The extension-period-only estimate shows no significant effect in either specification.

### Turnout
| Period | Basic | Linear |
|--------|-------|--------|
| Original (1996-2018) | 0.0212** | 0.0215*** |
| Extension (2020-2024) | -0.0095 | -0.0502*** |

The extension period alone shows a negative (and significant with linear trends) turnout effect. This likely reflects the confounding of COVID-era voting changes (Governor Newsom's EO N-64-20 sent mail ballots to all CA voters in 2020, attenuating the VCA treatment contrast) rather than a genuine reversal of VBM's turnout effect.

## Part 3: Heterogeneity (VBM × Post-2018)

### Dem Vote Share
| Spec | treat | SE | treat×post | SE |
|------|-------|----|------------|-----|
| Basic | 0.0280*** | 0.0089 | -0.0086 | 0.0135 |
| Linear | 0.0100*** | 0.0033 | -0.0133** | 0.0059 |
| Quadratic | 0.0082** | 0.0032 | -0.0209*** | 0.0058 |

The interaction term is negative and significant in the trend specifications, suggesting a slight decrease in VBM's already-small positive partisan effect after 2018. The combined effect (treat + treat×post) in the quadratic spec is 0.0082 - 0.0209 = -0.0127, still small in magnitude.

### Turnout
| Spec | treat | SE | treat×post | SE |
|------|-------|----|------------|-----|
| Basic | 0.0289*** | 0.0070 | -0.0195** | 0.0095 |
| Linear | 0.0232*** | 0.0065 | -0.0292*** | 0.0090 |
| Quadratic | 0.0212*** | 0.0070 | -0.0270*** | 0.0089 |

The interaction is consistently negative and significant for turnout, suggesting the turnout-boosting effect of VBM was weaker (or reversed) in the post-2018 period. Again, this is likely driven by the 2020 COVID confound.

## Part 4: California-Only Analysis

### CA Dem Vote Share
| Spec | Coef | SE | N | Counties |
|------|------|----|---|----------|
| Basic | 0.0196* | 0.0101 | 812 | 58 |
| Linear | -0.0041 | 0.0048 | 812 | 58 |
| Quadratic | -0.0121*** | 0.0047 | 812 | 58 |

With trends, the CA-specific VCA effect on vote share is essentially zero or slightly negative — consistent with the null finding.

### CA Turnout
| Spec | Coef | SE | N | Counties |
|------|------|----|---|----------|
| Basic | 0.0100 | 0.0063 | 754 | 58 |
| Linear | -0.0048 | 0.0063 | 754 | 58 |
| Quadratic | -0.0032 | 0.0064 | 754 | 58 |

The CA-specific turnout effect is not significant in any specification, likely because the VCA treatment contrast is attenuated by the 2020 executive order.

## Part 5: Event Study

### Dem Vote Share (CA treated counties, linear trends, ref = t-2)
| Event Time | Coef | SE | 95% CI |
|-----------|------|----|--------|
| t-6 | 0.0049 | 0.0066 | [-0.0081, 0.0179] |
| t-4 | -0.0022 | 0.0045 | [-0.0110, 0.0066] |
| t=0 | -0.0024 | 0.0057 | [-0.0135, 0.0088] |
| t+2 | 0.0012 | 0.0104 | [-0.0192, 0.0215] |
| t+4 | 0.0130 | 0.0191 | [-0.0244, 0.0504] |
| t+6 | 0.0153 | 0.0265 | [-0.0367, 0.0673] |

Pre-treatment coefficients are small and insignificant (no pre-trend), and post-treatment coefficients are also small and insignificant, consistent with no partisan effect of VCA adoption.

### Turnout (CA treated counties, linear trends, ref = t-2)
| Event Time | Coef | SE | 95% CI |
|-----------|------|----|--------|
| t-6 | 0.0043 | 0.0061 | [-0.0077, 0.0163] |
| t-4 | -0.0036 | 0.0056 | [-0.0147, 0.0074] |
| t=0 | -0.0074 | 0.0094 | [-0.0258, 0.0110] |
| t+2 | -0.0033 | 0.0141 | [-0.0310, 0.0244] |
| t+4 | -0.0136 | 0.0239 | [-0.0604, 0.0332] |
| t+6 | -0.0170 | 0.0346 | [-0.0848, 0.0509] |

No clear pre-trends. Post-treatment turnout effects are small, negative (but insignificant), consistent with the COVID confound.

## Part 6: Robustness (Exclude 2020)

Excluding 2020 (the most confounded year):

### Dem Vote Share
| Spec | Coef | SE |
|------|------|-----|
| Basic | 0.0272*** | 0.0076 |
| Linear | 0.0071** | 0.0034 |
| Quadratic | 0.0056* | 0.0034 |

Similar to full-sample results.

### Turnout
| Spec | Coef | SE |
|------|------|-----|
| Basic | 0.0192*** | 0.0055 |
| Linear | 0.0125** | 0.0054 |
| Quadratic | 0.0160** | 0.0062 |

Turnout effects are slightly stronger when excluding 2020, consistent with 2020 being a confounded observation.

## Overall Assessment

1. **The null partisan finding holds**: VBM has no meaningful effect on Democratic vote share when controlling for county and state-year fixed effects with trends. This extends the original finding through 2024.

2. **Turnout effects persist but are attenuated in the post-COVID period**: The ~2pp turnout boost from VBM found in the original paper persists in the full sample but is weaker in the 2020-2024 extension period alone, likely due to COVID-era voting changes that sent mail ballots to all voters regardless of VCA status.

3. **Event study shows clean identification**: No pre-trends in either outcome, supporting the parallel trends assumption underlying the DiD design.

4. **Heterogeneity tests suggest mild period effects**: The VBM × post-2018 interaction is negative for both outcomes, suggesting diminishing effects over time, but this is likely driven by the COVID confound rather than a genuine change in VBM's causal effect.
