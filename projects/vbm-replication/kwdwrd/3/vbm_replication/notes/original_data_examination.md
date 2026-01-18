# Original Data Examination

## Dataset: analysis.dta

### Basic Dimensions
- **Rows**: 1,454 county-election observations
- **Columns**: 134 variables
- **Years**: 1996-2018
- **States**: California, Utah, Washington

### County Coverage
| State | Counties | Observations |
|-------|----------|--------------|
| California | 58 | 638 |
| Utah | 29 | 348 |
| Washington | 39 | 468 |
| **Total** | **126** | **1,454** |

### Treatment Variable (VBM Adoption)
- **Treated (VBM=1)**: 339 observations (23.3%)
- **Control (VBM=0)**: 1,115 observations (76.7%)

**Treatment by State**:
| State | % Treated | Notes |
|-------|-----------|-------|
| California | 0.8% | Only 5 VCA counties in 2018 |
| Utah | 17.0% | Gradual rollout 2012-2018 |
| Washington | 58.8% | Staggered adoption 2002-2010 |

### Key Outcome Variables

#### Table 2 Outcomes (Partisan)

**Democratic Turnout Share** (`share_votes_dem`):
- N valid: 986
- Mean: 0.2844, SD: 0.1762
- Available for: CA, UT only (not WA - no party registration)
- Definition: Share of voters who are registered Democrats

**Democratic Vote Share** (stacked from multiple races):
- Governor (`dem_share_gov`): N=756, Mean=0.4281
- President (`dem_share_pres`): N=698, Mean=0.4295
- Senate (`dem_share_sen`): N=544, Mean=0.3792
- Definition: Dem votes / (Dem + Rep votes)

#### Table 3 Outcomes (Participation)

**Turnout** (`turnout_share`):
- N valid: 1,240
- Mean: 0.5416, SD: 0.1209
- Available for: All three states
- Definition: Ballots cast / CVAP

**VBM Share** (`vbm_share`):
- N valid: 892
- Mean: 0.5831, SD: 0.2460
- Available for: CA, WA only (not UT)
- Definition: Share of ballots cast by mail

### Missing Data Patterns

| Variable | CA | UT | WA | Total |
|----------|----|----|-------|-------|
| share_votes_dem | 638 | 348 | 0 | 986 |
| turnout_share | 580 | 348 | 312 | 1,240 |
| vbm_share | 580 | 0 | 312 | 892 |

**Notes**:
- Washington lacks party registration data → no `share_votes_dem`
- Utah lacks VBM share data → no `vbm_share`
- Turnout data missing for some CA and WA observations

### Fixed Effects Variables

- **county_id**: 126 unique values (one per county)
- **state_year_id**: 35 unique state×year combinations
- **year2**: year squared (for quadratic trends)
- **year3**: year cubed (available but not used in main specs)

### Data Verification

The data matches what the paper describes:
- ✅ 126 counties across 3 states
- ✅ 1996-2018 time period
- ✅ General elections only (primaries dropped in prep)
- ✅ Treatment reflects staggered VBM adoption
- ✅ Missing data patterns align with data availability by state
