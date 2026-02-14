# Replication Comparison: Original vs. Python Implementation

## Overview

This document compares the original Stata results from Thompson et al. (2020) with our Python replication.

---

## Table 2: Partisan Outcomes

### Democratic Turnout Share (Columns 1-3)

| Specification | Original β (SE) | Replicated β (SE) | Difference | % Diff |
|--------------|-----------------|-------------------|------------|--------|
| Basic | 0.007 (0.003) | 0.007 (0.003) | +0.0002 | +2.9% |
| Linear Trends | 0.001 (0.001) | 0.001 (0.001) | +0.0001 | +10.0% |
| Quadratic Trends | 0.001 (0.001) | 0.001 (0.001) | -0.0001 | -10.0% |

**Sample**: 986 observations, 87 counties (CA and UT only)

### Democratic Vote Share (Columns 4-6)

| Specification | Original β (SE) | Replicated β (SE) | Difference | % Diff |
|--------------|-----------------|-------------------|------------|--------|
| Basic | 0.028 (0.011) | 0.028 (0.011) | +0.0005 | +1.8% |
| Linear Trends | 0.011 (0.004) | 0.011 (0.004) | -0.0001 | -0.9% |
| Quadratic Trends | 0.007 (0.003) | 0.007 (0.003) | -0.0001 | -1.4% |

**Sample**: 1,998 observations, 126 counties (all three states, reshaped long)

---

## Table 3: Participation Outcomes

### Turnout (Columns 1-3)

| Specification | Original β (SE) | Replicated β (SE) | Difference | % Diff |
|--------------|-----------------|-------------------|------------|--------|
| Basic | 0.021 (0.009) | 0.021 (0.009) | +0.0002 | +1.0% |
| Linear Trends | 0.022 (0.007) | 0.022 (0.006) | -0.0005 | -2.3% |
| Quadratic Trends | 0.021 (0.008) | 0.022 (0.007) | +0.0013 | +6.2% |

**Sample**: 1,240 observations, 126 counties

### VBM Share (Columns 4-6)

| Specification | Original β (SE) | Replicated β (SE) | Difference | % Diff |
|--------------|-----------------|-------------------|------------|--------|
| Basic | 0.186 (0.027) | 0.186 (0.026) | +0.0000 | +0.0% |
| Linear Trends | 0.157 (0.035) | 0.156 (0.033) | -0.0008 | -0.5% |
| Quadratic Trends | 0.136 (0.085) | 0.136 (0.073) | -0.0002 | -0.1% |

**Sample**: 580 observations, 58 counties (CA only)

---

## Assessment

### Replication Success

**Overall Assessment: SUCCESSFUL REPLICATION**

All point estimates are within 0.002 of the original values. The largest percentage difference is 10% for the Democratic Turnout Share with linear trends, but this is a very small coefficient (0.001), so the absolute difference is negligible.

### Sources of Minor Differences

1. **Numerical precision**: Stata and Python may use different numerical algorithms for iterative demeaning and matrix inversion

2. **Standard error calculation**: Small differences in the degrees of freedom correction for clustered standard errors

3. **Trend implementation**: The exact implementation of county-specific trends may differ slightly between Stata's `reghdfe` and our manual Python implementation

### Key Findings Confirmed

The replication confirms the original paper's key findings:

1. **Null partisan effects**: VBM has essentially zero effect on Democratic turnout share (0.001 with trends) and Democratic vote share (0.007-0.011)

2. **Modest turnout increase**: VBM increases turnout by approximately 2.1-2.2 percentage points

3. **Strong first stage**: VBM increases mail ballot usage by 13.6-18.6 percentage points in California

---

## Technical Notes

### Python Implementation Details

1. **Fixed Effects Absorption**: Implemented iterative demeaning (alternating projections) to absorb two-way fixed effects (county + state×year)

2. **County-Specific Trends**:
   - Linear trends: Created interaction of county dummies with normalized year
   - Quadratic trends: Added county dummies interacted with year²
   - Used Frisch-Waugh-Lovell to partial out trends

3. **Clustered Standard Errors**: Implemented sandwich estimator with Stata's default small-sample correction: (G/(G-1)) × ((N-1)/(N-K))

### Data Transformation for Table 2, Columns 4-6

The original Stata code reshapes the data from wide to long format:
```stata
reshape long dem_share, i(state county year) j(office) s
```

This combines `dem_share_gov`, `dem_share_pres`, and `dem_share_sen` into a single `dem_share` variable with an `office` indicator. We replicated this using `pandas.melt()`.

---

## Conclusion

The Python replication successfully reproduces the original Stata results. The analysis code is now validated and ready for use in the extension analysis with new 2020-2024 data.
