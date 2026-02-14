# Original Data Examination

## Main Analysis Dataset: `analysis.dta`

**Dimensions:** 1,454 rows × 134 columns

**Structure:** County-year panel for general elections only

### Coverage

| State | Counties | Years | Obs |
|-------|----------|-------|-----|
| CA | 58 | 1998–2018 (11 years; missing 1996) | 638 |
| UT | 29 | 1996–2018 (12 years) | 348 |
| WA | 39 | 1996–2018 (12 years) | 468 |
| **Total** | **126** | | **1,454** |

Note: CA has fewer observations (11 per county vs 12) because 1996 data is missing for CA.

### Key Outcome Variables

| Variable | N valid | N missing | Mean | SD | Min | Max | States |
|----------|---------|-----------|------|-----|-----|-----|--------|
| share_votes_dem | 986 | 468 | 0.284 | 0.176 | 0.016 | 0.658 | CA, UT |
| dem_share_gov | 756 | 698 | 0.428 | 0.156 | 0.079 | 0.882 | CA, UT, WA |
| dem_share_pres | 698 | 756 | 0.430 | 0.168 | 0.070 | 0.902 | CA, UT, WA |
| dem_share_sen | 544 | 910 | 0.379 | 0.155 | 0.078 | 0.742 | UT, WA (no CA) |
| turnout_share | 1,240 | 214 | 0.542 | 0.121 | 0.225 | 0.935 | CA, UT, WA |
| vbm_share | 892 | 562 | 0.583 | 0.246 | 0.008 | 1.000 | CA, WA (no UT) |

### Treatment Variable

Total: 339 treated observations (23.3%), 1,115 untreated (76.7%)

| State | N treated | Years with treatment | Pattern |
|-------|-----------|---------------------|---------|
| CA | 5 | 2018 only (5 VCA counties) | Late, minimal variation |
| UT | 59 | 2012 (1), 2014 (10), 2016 (21), 2018 (27) | Staggered rollout |
| WA | 275 | 1996–2018, all 39 by 2012 | Extensive staggered |

### Panel Balance

- Most counties have 12 observations (all 12 election years)
- 58 counties (all CA) have 11 observations (missing 1996)
- The panel is nearly balanced
