# Original Data Examination

## Main Analysis Dataset: `analysis.dta`

- **Dimensions:** 1,454 rows x 134 columns
- **Unit of observation:** county x election year (general elections only)
- **States:** CA, UT, WA (3 states)
- **Years:** 1996-2018 (even years only; CA starts 1998)
- **Counties:** 126 unique (58 CA + 29 UT + 39 WA)

## Observations by State

| State | N obs | Counties | Year range |
|-------|-------|----------|------------|
| CA | 638 | 58 | 1998-2018 |
| UT | 348 | 29 | 1996-2018 |
| WA | 468 | 39 | 1996-2018 |

## Key Outcome Variables

| Variable | N valid | N missing | % missing | Mean | SD | Min | Max |
|----------|---------|-----------|-----------|------|-----|-----|-----|
| share_votes_dem | 986 | 468 | 32.2% | 0.284 | 0.176 | 0.016 | 0.658 |
| dem_share_gov | 756 | 698 | 48.0% | 0.428 | 0.156 | 0.079 | 0.882 |
| dem_share_pres | 698 | 756 | 52.0% | 0.430 | 0.168 | 0.070 | 0.902 |
| dem_share_sen | 544 | 910 | 62.6% | 0.379 | 0.155 | 0.078 | 0.742 |
| turnout_share | 1,240 | 214 | 14.7% | 0.542 | 0.121 | 0.225 | 0.935 |
| vbm_share | 892 | 562 | 38.7% | 0.583 | 0.246 | 0.008 | 1.000 |

### Notes on Missing Data
- `share_votes_dem`: Available for CA and UT only (WA lacks partisan registration). 986 = 638 CA + 348 UT.
- `dem_share_gov`: Not available in non-gubernatorial years; varies by state.
- `dem_share_pres`: Only available in presidential years (2000, 2004, 2008, 2012, 2016).
- `dem_share_sen`: Available only when there is a Senate race.
- `turnout_share`: Missing for some early years where CVAP data is unavailable.
- `vbm_share`: Available for CA and WA (not UT in early years).

## Treatment Variable

| State | Year | Treated counties | Total counties | % treated |
|-------|------|-----------------|----------------|-----------|
| CA | 2018 | 5 | 58 | 8.6% |
| UT | 2012 | 1 | 29 | 3.4% |
| UT | 2014 | 10 | 29 | 34.5% |
| UT | 2016 | 21 | 29 | 72.4% |
| UT | 2018 | 27 | 29 | 93.1% |
| WA | 1996-2004 | 1-5 | 39 | 2.6-12.8% |
| WA | 2006 | 34 | 39 | 87.2% |
| WA | 2008 | 37 | 39 | 94.9% |
| WA | 2010 | 38 | 39 | 97.4% |
| WA | 2012-2018 | 39 | 39 | 100% |

## ID Variables

- `county_id`: 1-126 (unique across states)
- `state_year_id`: 1-36 (note: 36 rather than 36 because CA starts in 1998, not 1996)
  - Actual count in data: 35 unique state-year groups
- `year2`: year^2 (for quadratic county trends)
- `year3`: year^3 (present but not used in main specifications)
