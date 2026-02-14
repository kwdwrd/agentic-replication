# Replication Comparison: Original vs. Python Replicated Results

## Summary

The Python replication closely reproduces the original Stata results from Thompson et al. (2020). All point estimates match to within 0.001 (i.e., within rounding precision of the 3-decimal-place reporting in the original paper). Standard errors are very close, with minor differences attributable to slight differences in how Stata's `reghdfe` and our Python implementation handle the alternating projections algorithm and clustered standard error finite-sample corrections.

## Table 2: Partisan Outcomes

| Col | Outcome | Spec | Orig Coef | Repl Coef | Diff | Orig SE | Repl SE |
|-----|---------|------|-----------|-----------|------|---------|---------|
| 1 | Dem Turnout Share | Basic | 0.007 | 0.0072 | +0.0002 | 0.003 | 0.0031 |
| 2 | Dem Turnout Share | Linear | 0.001 | 0.0012 | +0.0002 | 0.001 | 0.0014 |
| 3 | Dem Turnout Share | Quad | 0.001 | 0.0009 | -0.0001 | 0.001 | 0.0011 |
| 4 | Dem Vote Share | Basic | 0.028 | 0.0285 | +0.0005 | 0.011 | 0.0113 |
| 5 | Dem Vote Share | Linear | 0.011 | 0.0109 | -0.0001 | 0.004 | 0.0038 |
| 6 | Dem Vote Share | Quad | 0.007 | 0.0065 | -0.0005 | 0.003 | 0.0032 |

**Assessment:** All coefficients match to within rounding of the original 3-decimal-place reporting. The largest absolute difference is 0.0005 (column 4 and column 6), which rounds to 0.000 at 3 decimal places. Standard errors are also very close, all within 0.001 of the original.

## Table 3: Participation Outcomes

| Col | Outcome | Spec | Orig Coef | Repl Coef | Diff | Orig SE | Repl SE |
|-----|---------|------|-----------|-----------|------|---------|---------|
| 1 | Turnout | Basic | 0.021 | 0.0212 | +0.0002 | 0.009 | 0.0093 |
| 2 | Turnout | Linear | 0.022 | 0.0215 | -0.0005 | 0.007 | 0.0065 |
| 3 | Turnout | Quad | 0.021 | 0.0210 | 0.0000 | 0.008 | 0.0072 |
| 4 | VBM Share | Basic | 0.186 | 0.1860 | 0.0000 | 0.027 | 0.0264 |
| 5 | VBM Share | Linear | 0.157 | 0.1575 | +0.0005 | 0.035 | 0.0329 |
| 6 | VBM Share | Quad | 0.136 | 0.1359 | -0.0001 | 0.085 | 0.0756 |

**Assessment:** Coefficients match well. The VBM share results (CA-only) match almost exactly. Turnout results also match within rounding. Standard errors are close, with the largest difference in the quadratic VBM share specification (0.085 original vs. 0.076 replicated), which may reflect differences in finite-sample degrees-of-freedom corrections in the highly saturated quadratic trend model.

## Sample Sizes

| Outcome | Original Counties | Replicated Counties | Match? |
|---------|-------------------|---------------------|--------|
| Dem Turnout Share | 87 | 87 | Yes |
| Dem Vote Share | 126 | 126 | Yes |
| Turnout | 126 | 126 | Yes |
| VBM Share | 58 | 58 | Yes |

Note: The number of elections differs slightly between our count and the original paper's. The original counts "state x year" groups conditional on being in the regression sample, while our count reflects the state-year groups present in the data. The difference is minor and does not affect results.

## Sources of Minor Differences

1. **Floating-point precision:** Our iterative demeaning algorithm converges to machine epsilon (1e-10 tolerance), but the Stata `reghdfe` implementation may use slightly different convergence criteria or a different projection algorithm (LSMR vs. alternating projections).

2. **Standard error computation:** Stata's `reghdfe` uses a specific finite-sample correction formula for clustered SEs that adjusts for the number of absorbed fixed effects. Our implementation uses the standard G/(G-1) correction without adjusting for absorbed parameters, which can lead to slight differences.

3. **Data types:** The original Stata dataset stores some variables as float32, while our Python code converts to float64. This can introduce minor numerical differences.

## Conclusion

The replication is successful. All point estimates are within rounding tolerance of the original paper's reported values. The qualitative conclusions are identical:
- VBM has no meaningful effect on Democratic turnout share (small positive in basic spec, essentially zero with trends)
- VBM has no meaningful effect on Democratic vote share (same pattern)
- VBM increases overall turnout by ~2 percentage points (robust across specifications)
- VBM mechanically increases the share of votes cast by mail (~14-19 pp in CA)
