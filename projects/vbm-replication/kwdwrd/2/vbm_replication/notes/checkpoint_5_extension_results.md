# Checkpoint 5: Extension Analysis Results

## Summary

This document presents the results of extending Thompson et al. (2020) "Universal vote-by-mail has no impact on partisan turnout or vote share" to 2020-2024 elections.

## Extension Design

### Data Coverage
- **Time period:** 2020, 2022, 2024 elections
- **States:** California (58 counties), Utah (29 counties), Washington (39 counties)
- **Treatment:** California VCA (Voter's Choice Act) adoption
- **Comparison:** Always-treated states (UT since 2019, WA since 2011)

### Identification Strategy
1. **Primary:** California DiD with staggered VCA adoption
   - Treated: Counties that adopted VCA
   - Control: Never-VCA counties within California
   - County FE + Year FE

2. **Supplementary:** Cross-state comparison (limited value due to confounding)

## Main Results

### California-Only Analysis (Primary Specification)

| Outcome | Coefficient | SE | p-value | Significant? |
|---------|------------|-----|---------|--------------|
| Democratic Vote Share | -0.0086 | 0.0103 | 0.407 | No |
| Turnout | -0.0048 | 0.0098 | 0.626 | No |

**Interpretation:** VCA adoption in California has no statistically significant effect on either partisan vote share or turnout.

### All-States Analysis (Cross-State Comparison)

| Outcome | Coefficient | SE | p-value | Significant? |
|---------|------------|-----|---------|--------------|
| Democratic Vote Share | -0.0316 | 0.0099 | 0.002 | Yes*** |
| Turnout | -0.0236 | 0.0093 | 0.012 | Yes** |

**Interpretation:** The cross-state analysis shows significant negative effects, but this comparison is confounded by state-level differences unrelated to VBM policy.

## Comparison with Original Paper

| Outcome | Original (1996-2018) | Extension CA (2020-2024) | Consistent? |
|---------|---------------------|-------------------------|-------------|
| Dem Vote Share | 0.01-0.03 (ns) | -0.009 (ns) | YES |
| Turnout | +0.02** | -0.005 (ns) | PARTIAL |

### Key Finding: Partisan Effects
**CONSISTENT:** Both the original paper and extension find **no significant partisan effect** of VBM/VCA adoption. Point estimates are near zero in both analyses.

### Turnout Effects
**DIFFERENT:** The original paper found a significant +2pp turnout increase from VBM. The extension finds no turnout effect from VCA.

Possible explanations:
1. **COVID-19 effect:** 2020 saw unprecedented turnout due to pandemic, potentially masking VCA effects
2. **VCA vs VBM:** VCA includes voting centers, which may have different turnout dynamics than pure VBM
3. **Saturation:** By 2020, California had already expanded vote-by-mail substantially, limiting marginal gains

## Treatment Variation Analysis

### California VCA Adoption Timeline
| Year | Counties Treated | Cumulative % |
|------|-----------------|--------------|
| 2018 | 5 | 8.6% |
| 2020 | 15 | 25.9% |
| 2022 | 27 | 46.6% |
| 2024 | 30 | 51.7% |
| Never | 28 | - (control) |

### Mean Outcomes by Treatment Status and Year

**Democratic Vote Share:**
| Year | Treated | Control | Difference |
|------|---------|---------|------------|
| 2020 | 0.549 | 0.550 | -0.001 |
| 2022 | 0.535 | 0.444 | +0.092 |
| 2024 | 0.558 | 0.471 | +0.087 |

**Note:** Raw differences are not causal estimates; they reflect selection into treatment.

**Turnout:**
| Year | Treated | Control | Difference |
|------|---------|---------|------------|
| 2020 | 0.699 | 0.663 | +0.036 |
| 2022 | 0.468 | 0.451 | +0.018 |
| 2024 | 0.621 | 0.582 | +0.039 |

## Limitations

1. **COVID-19 Pandemic:** The 2020 election was unprecedented; all states expanded mail voting options regardless of VCA status

2. **VCA vs Universal VBM:** VCA includes voting centers and early voting, not just mail ballots; different mechanism than studied in original

3. **Short Panel:** Only 3 time periods (vs. 8+ in original) limits statistical power

4. **Selection into Treatment:** VCA adoption may correlate with county characteristics that independently affect outcomes

5. **CVAP Estimation:** Used projected CVAP values which introduce measurement error in turnout calculations

## Conclusions

### Main Finding
**The original paper's central conclusion holds:** Universal/expanded mail voting does not significantly shift partisan outcomes. Democrats do not systematically benefit (or lose) from expanded vote-by-mail access.

### Nuance on Turnout
The turnout finding is less robust in the extension period. This may reflect:
- Unique COVID-19 dynamics in 2020
- Differences between VCA and pure VBM
- California having already achieved high VBM rates pre-VCA

### Policy Implications
1. VBM/VCA expansion remains politically neutral
2. Concerns about partisan advantage from mail voting are not supported
3. Turnout effects may be context-dependent

## Files Generated

- `output/tables/extension_results.csv` - Regression coefficients and statistics
- `code/05_run_extension.py` - Extension analysis script
- `data/extension/extension_panel.csv` - Analysis dataset
