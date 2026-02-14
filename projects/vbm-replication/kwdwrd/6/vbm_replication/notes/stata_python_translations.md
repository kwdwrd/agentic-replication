# Stata to Python Translation Notes

## Key Command Translations

| Stata Command | Python Equivalent | Notes |
|--------------|-------------------|-------|
| `reghdfe Y X, absorb(FE1 FE2) vce(cluster var)` | `linearmodels.PanelOLS` or manual demeaning + `statsmodels.OLS` | `reghdfe` uses iterative demeaning for high-dimensional FE |
| `absorb(county_id)` | Entity effects in PanelOLS, or include dummies | County fixed effects |
| `absorb(state_year)` | Time effects or dummy variables for state×year | State-by-year fixed effects |
| `absorb(county_id##c.year)` | County-specific linear time trends: interact county dummies with year | Requires manual construction |
| `absorb(county_id##c.year2)` | County-specific quadratic time trends: interact county dummies with year² | Requires manual construction |
| `vce(clust county_id)` | Clustered standard errors at county level | Use `cov_type='clustered', cluster_entity=True` or manual clustering |
| `distinct var if e(sample)` | `df[sample]['var'].nunique()` | Count distinct values |
| `reshape long` | `pd.melt()` or `pd.wide_to_long()` | Reshape wide to long |
| `merge 1:1` | `pd.merge()` with `on=` keys | Merge datasets |
| `egen group()` | `pd.factorize()` or `pd.Categorical` | Create numeric group IDs |

## Implementation Strategy

### Approach for `reghdfe` Replication

The core challenge is replicating `reghdfe` with multiple high-dimensional fixed effects and county-specific trends. Two approaches:

**Approach A: Manual demeaning + OLS**
1. Demean the outcome and treatment by county FE and state×year FE
2. For trend specifications, project out county-specific trends
3. Run OLS on demeaned data
4. Compute clustered standard errors

**Approach B: Dummy variable regression with `statsmodels`**
1. Create dummy variables for all FE
2. For trends, create county×year interaction terms
3. Run OLS with all dummies
4. Clustered SEs via `statsmodels` `cov_type='cluster'`

**Approach C: `linearmodels.PanelOLS` + auxiliary demeaning**
1. Use `PanelOLS` for entity and time effects
2. For county-specific trends, manually demean by county trends first, then use PanelOLS
3. Or use `AbsorbingLS` from `linearmodels`

**Chosen approach**: Approach B (explicit dummy variables) for transparency and exact replication. While computationally heavier, it avoids approximation issues with iterative demeaning and makes the specification fully transparent. For the dataset size here (~1500 rows), this is feasible.

For county-specific trends:
- Linear: Include `county_id * year` interaction terms (county dummies × continuous year)
- Quadratic: Add `county_id * year²` interaction terms

### Standard Error Clustering

Use `statsmodels` with `cov_type='cluster'` and `cov_kwds={'groups': county_id}`.

Alternatively, use the `linearmodels.AbsorbingLS` estimator which supports `absorbing` effects and clustered standard errors directly.

### Package Requirements

- `pandas`: Data manipulation
- `numpy`: Numerical operations
- `statsmodels`: OLS regression, clustered standard errors
- `linearmodels`: Panel data models, absorbing regression
- `pyreadstat`: Reading Stata .dta files
- `matplotlib` + `seaborn`: Visualization
- `scipy`: Statistical tests
