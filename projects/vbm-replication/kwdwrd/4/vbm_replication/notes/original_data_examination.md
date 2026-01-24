# Original Data Examination

This document provides detailed examination of the original analysis dataset.

## 1. Dataset Dimensions

- **Rows**: 1454
- **Columns**: 134
- **Unit of analysis**: County-year (general elections)

## 2. Geographic Coverage

| State | Counties | Observations |
|-------|----------|-------------|
| CA | 58 | 638 |
| UT | 29 | 348 |
| WA | 39 | 468 |
| **Total** | **124** | **1454** |

## 3. Temporal Coverage

- **Years**: 1996 - 2018
- **Election years**: [1996, 1998, 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018]

## 4. Treatment Variable

The `treat` variable equals 1 if a county has universal VBM in that year.

### Treatment Rate by State and Year

| Year | CA | UT | WA |
|------|----|----|----|
| 1996 | - | 0.00 | 0.03 |
| 1998 | 0.00 | 0.00 | 0.03 |
| 2000 | 0.00 | 0.00 | 0.03 |
| 2002 | 0.00 | 0.00 | 0.05 |
| 2004 | 0.00 | 0.00 | 0.13 |
| 2006 | 0.00 | 0.00 | 0.87 |
| 2008 | 0.00 | 0.00 | 0.95 |
| 2010 | 0.00 | 0.00 | 0.97 |
| 2012 | 0.00 | 0.03 | 1.00 |
| 2014 | 0.00 | 0.34 | 1.00 |
| 2016 | 0.00 | 0.72 | 1.00 |
| 2018 | 0.09 | 0.93 | 1.00 |

## 5. Key Outcome Variables

### Summary Statistics

| Variable | N | Mean | Std | Min | Max |
|----------|---|------|-----|-----|-----|
| share_votes_dem | 986 | 0.284 | 0.176 | 0.016 | 0.658 |
| dem_share_gov | 756 | 0.428 | 0.156 | 0.079 | 0.882 |
| dem_share_pres | 698 | 0.430 | 0.168 | 0.070 | 0.902 |
| dem_share_sen | 544 | 0.379 | 0.155 | 0.078 | 0.741 |
| turnout_share | 1240 | 0.542 | 0.121 | 0.225 | 0.935 |
| vbm_share | 892 | 0.583 | 0.246 | 0.008 | 1.000 |

### Variable Availability by State

| Variable | CA | UT | WA |
|----------|----|----|----|
| share_votes_dem | 638 | 348 | 0 |
| turnout_share | 580 | 348 | 312 |
| vbm_share | 580 | 0 | 312 |

## 6. Sample Sizes for Key Regressions

| Table | Outcome | States | N Obs | N Counties |
|-------|---------|--------|-------|------------|
| Table 2, Cols 1-3 | Dem turnout share | CA, UT | 986 | 87 |
| Table 2, Cols 4-6 | Dem vote share | All | 1318 | 126 |
| Table 3, Cols 1-3 | Turnout | All | 1240 | 126 |
| Table 3, Cols 4-6 | VBM share | CA | 580 | 58 |

## 7. California VCA Adoption

- **VCA 2018 counties** (5): Madera, Napa, Nevada, Sacramento, San Mateo
- **VCA 2020 eligible** (15): Amador, Butte, Calaveras, El Dorado, Fresno, Los Angeles, Madera, Mariposa, Napa, Nevada, Orange, Sacramento, San Mateo, Santa Clara, Tuolumne

## 8. Missing Data Patterns

| Variable | Missing | Pct Missing |
|----------|---------|-------------|
| treat | 0 | 0.0% |
| turnout_share | 214 | 14.7% |
| vbm_share | 562 | 38.7% |
| share_votes_dem | 468 | 32.2% |
| dem_share_gov | 698 | 48.0% |
| dem_share_pres | 756 | 52.0% |
| dem_share_sen | 910 | 62.6% |
