# Project Instructions

This file contains the detailed instructions for the replication and extension project.

See the main project README.md for an overview.

## Key Stata-to-Python Translation Notes

### reghdfe → Python

The original Stata code uses `reghdfe` for high-dimensional fixed effects regression. In Python, the equivalent approaches are:

1. **linearmodels.PanelOLS**: Best for standard two-way fixed effects
   ```python
   from linearmodels.panel import PanelOLS
   mod = PanelOLS(y, X, entity_effects=True, time_effects=True)
   result = mod.fit(cov_type='clustered', cluster_entity=True)
   ```

2. **Manual demeaning + OLS**: For county-specific trends
   - Demean variables within county
   - Include state-year dummies
   - Add county × year and county × year² terms

### Key Specifications

**Table 2 (Partisan Effects)**:
- Columns 1-3: `share_votes_dem ~ treat` with county FE + state×year FE + trends
- Columns 4-6: `dem_share ~ treat` (reshaped to office level)

**Table 3 (Participation Effects)**:
- Columns 1-3: `turnout_share ~ treat` with county FE + state×year FE + trends
- Columns 4-6: `vbm_share ~ treat` (California only)

### Fixed Effects Structure

1. **Basic (no trends)**: `a(county_id state_year)`
   - County fixed effects absorb time-invariant county characteristics
   - State-year fixed effects absorb state-specific shocks in each year

2. **Linear trends**: `a(county_id##c.year state_year)`
   - Adds county-specific linear time trends
   - Accounts for differential pre-treatment trends

3. **Quadratic trends**: `a(county_id##c.year county_id##c.year2 state_year)`
   - Adds county-specific quadratic time trends
   - More flexible but may overfit

### Clustering

All standard errors clustered at county level (126 clusters total).
