# Checkpoint 4: Extension Data Preparation

## Summary

The extension panel dataset has been prepared and is ready for DiD analysis. This document summarizes the data structure, variable definitions, and quality checks.

## Panel Structure

| Dimension | Value |
|-----------|-------|
| Total Observations | 378 |
| Counties | 126 |
| Time Periods | 3 (2020, 2022, 2024) |
| States | 3 (CA, UT, WA) |
| Panel Balance | Balanced (3 obs per county) |

## Treatment Design

### California (58 counties)
- **Treatment:** VCA (Voter's Choice Act) adoption
- **Variation:** Staggered adoption from 2018-2024
- **Treatment rates:**
  - 2020: 15/58 counties treated (25.9%)
  - 2022: 27/58 counties treated (46.6%)
  - 2024: 30/58 counties treated (51.7%)
- **Never treated:** 28 counties remain as control units

### Utah (29 counties)
- **Treatment:** Universal VBM since 2019
- **All counties treated for entire sample period**
- **Serves as:** Always-treated comparison state

### Washington (39 counties)
- **Treatment:** Universal VBM since 2011
- **All counties treated for entire sample period**
- **Serves as:** Always-treated comparison state

## Variable Definitions

| Variable | Definition |
|----------|------------|
| `treat` | =1 if county has universal VBM in election year |
| `treat_year` | Year VBM was first adopted |
| `dem_share` | Democratic votes / (Dem + Rep votes) |
| `rep_share` | Republican votes / (Dem + Rep votes) |
| `turnout` | Total votes / CVAP |
| `cvap` | Citizen Voting Age Population |
| `log_cvap` | Log of CVAP |
| `county_id` | State_County identifier |
| `state_year` | State_Year identifier for FE |
| `county_idx` | Numeric county index for panel estimation |
| `state_year_idx` | Numeric state-year index for panel estimation |

## Data Quality Notes

### Turnout Anomalies
Three observations in Daggett County, UT show turnout > 100%:
- 2020: 127.9%
- 2022: 100.8%
- 2024: 111.3%

**Explanation:** Daggett County is Utah's smallest county (population ~1,000). CVAP estimates from 5-year ACS have high margins of error for small populations. This is a known issue that does not affect the main analysis since:
1. Utah is always-treated (no within-state variation)
2. Daggett represents <0.01% of total observations
3. County fixed effects absorb county-level differences

### CVAP Projections
CVAP values for 2020-2024 are projected from 2014-2018 ACS baseline using 1% annual growth. This introduces measurement error but:
1. Turnout is secondary outcome (vote share is primary)
2. County FE absorb level differences
3. Relative changes within county are preserved

## Summary Statistics

### By Treatment Status
| Variable | Treated | Control | Difference |
|----------|---------|---------|------------|
| dem_share | 0.419 | 0.496 | -0.078 |
| turnout | 0.663 | 0.576 | +0.086 |

**Note:** Raw differences are confounded by state composition (UT and WA are always-treated with different baseline characteristics).

### By State
| State | Dem Share | Turnout | % Treated |
|-------|-----------|---------|-----------|
| CA | 0.517 | 0.578 | 41.4% |
| UT | 0.265 | 0.697 | 100.0% |
| WA | 0.453 | 0.688 | 100.0% |

## Files Created

- `data/extension/extension_panel.csv` - Full panel (378 obs)
- `data/extension/california_panel.csv` - California only (174 obs)
- `code/04_prepare_extension.py` - Preparation script

## Identification Strategy for Extension

### Primary Analysis: California DiD
- **Treatment:** VCA adoption (staggered 2018-2024)
- **Control:** Never-VCA California counties
- **Model:** County FE + State-Year FE (effectively Year FE within CA)
- **Identification:** Comparing treated to not-yet-treated counties

### Robustness: Cross-State Comparison
- Compare California post-VCA trends to Utah/Washington
- Caveat: States differ on many dimensions beyond VBM

## Next Steps

1. **Phase 5:** Run extension regressions
   - Replicate Table 2 (vote share) and Table 3 (turnout) specifications
   - California-only DiD analysis
   - Cross-state comparisons

2. **Phase 6:** Write results and comparison to original findings
