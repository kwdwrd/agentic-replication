# Original Data Examination

## Main Analysis Dataset: `analysis.dta`

### Dimensions
- **Rows**: 1,454 county-year observations
- **Columns**: 134 variables

### Geographic Coverage

| State | Counties | Years | Observations |
|-------|----------|-------|--------------|
| California (CA) | 58 | 1998-2018 (11 elections) | 638 |
| Utah (UT) | 29 | 1996-2018 (12 elections) | 348 |
| Washington (WA) | 39 | 1996-2018 (12 elections) | 468 |
| **Total** | **126** | | **1,454** |

### Treatment Distribution

| State | Untreated (VBM=0) | Treated (VBM=1) | Notes |
|-------|-------------------|-----------------|-------|
| CA | 633 | 5 | VCA 2018: 5 pilot counties |
| UT | 289 | 59 | Staggered adoption 2004-2019 |
| WA | 193 | 275 | Staggered 2005-2011, 100% by 2011 |

### Key Outcome Variables

| Variable | N (non-missing) | Mean | Std Dev | Min | Max |
|----------|-----------------|------|---------|-----|-----|
| `share_votes_dem` | 986 | 0.284 | 0.176 | 0.016 | 0.658 |
| `dem_share_gov` | 756 | 0.428 | 0.156 | 0.079 | 0.882 |
| `dem_share_pres` | 698 | 0.430 | 0.168 | 0.070 | 0.902 |
| `dem_share_sen` | 544 | 0.379 | 0.155 | 0.078 | 0.742 |
| `turnout_share` | 1,240 | 0.542 | 0.121 | 0.225 | 0.935 |
| `vbm_share` | 892 | 0.583 | 0.246 | 0.008 | 1.000 |

### Fixed Effects Identifiers

- `county_id`: 1-126 (unique numeric ID for each county)
- `state_year_id`: 1-35 (unique ID for each state-year combination)
- `year`: 1996-2018 (even years only)
- `year2`: year squared (for quadratic trends)

### Sample Notes

1. **Democratic Turnout Share** (`share_votes_dem`):
   - Available for CA and UT only (986 obs, 87 counties)
   - Washington lacks voter file access

2. **Democratic Vote Share** (`dem_share_*`):
   - Available for all states
   - Missing values are structural (not all states have all races each year)
   - Reshaped to county-year-office level for analysis (1,998 obs)

3. **Turnout Rate** (`turnout_share`):
   - Available for all states (1,240 obs, 126 counties)
   - Some missing due to CVAP data availability

4. **VBM Share** (`vbm_share`):
   - Analysis restricted to CA only (580 obs, 58 counties)
   - Utah and Washington data not used for this outcome

### Data Quality Checks

1. **Vote shares**: All within [0, 1] range ✓
2. **Turnout rates**: All within [0, 1] range ✓
3. **Treatment indicator**: Binary (0/1) only ✓
4. **Missing patterns**: Consistent with structural data availability
