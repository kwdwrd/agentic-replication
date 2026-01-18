# Extension Dataset Documentation

## Overview

This document describes the extended analysis dataset created for the Thompson et al. (2020) replication and extension project.

## Dataset Files

| File | Description | Shape |
|------|-------------|-------|
| `analysis_extended.csv` | Full panel 1996-2024, all election types | 1,832 × 28 |
| `analysis_extended_pres.csv` | Presidential years only | 882 × 28 |
| `analysis_extended_ca_pres.csv` | California, presidential years | 406 × 28 |
| `analysis_extended.dta` | Stata format of full panel | 1,832 × 28 |

## Panel Structure

### Time Coverage
- **Original period**: 1996-2018 (from Thompson et al.)
- **Extension period**: 2020, 2022, 2024

### Geographic Coverage
| State | Counties | Notes |
|-------|----------|-------|
| California | 58 | VCA adoption varies by county |
| Utah | 29 | 100% VBM since 2019 |
| Washington | 39 | 100% VBM since 2011 |

Total: 126 counties × 15 years = 1,832 county-year observations

## Treatment Variable

The `treat` variable indicates universal VBM adoption:

### California (VCA Expansion)
| Year | Treated Counties | Cumulative |
|------|-----------------|------------|
| 2018 | 5 | 5 |
| 2020 | +10 | 15 |
| 2022 | +12 | 27 |
| 2024 | +2 | 29 |

### Utah
- All 29 counties treated from 2019 onwards

### Washington
- All 39 counties treated from 2011 onwards

## Key Variables

### Identifiers
- `state`: State abbreviation (CA, UT, WA)
- `county`: County name
- `year`: Election year
- `county_id`: Numeric county identifier (1-126)
- `state_year_id`: Numeric state×year identifier (1-44)

### Treatment
- `treat`: Binary indicator for VBM adoption (0/1)

### Outcomes
- `dem_share_pres`: Democratic two-party vote share, presidential election
- `dem_share_gov`: Democratic two-party vote share, gubernatorial election
- `dem_share_sen`: Democratic two-party vote share, Senate election
- `turnout_share`: Turnout as share of CVAP
- `vbm_share`: Share of ballots cast by mail
- `share_votes_dem`: Democratic share of registered voters (CA/UT only)

### Election Type
- `pres`: Presidential election indicator (0/1)
- `prim`: Primary election indicator (0/1)
- `prim_or_gen`: Primary or general election ("prim"/"gen")

## Data Availability by Year

### Democratic Vote Share (Presidential)
| Year | Counties with Data |
|------|-------------------|
| 2000 | 126 |
| 2004 | 126 |
| 2008 | 126 |
| 2012 | 126 |
| 2016 | 126 |
| 2020 | 126 ✓ (extension) |
| 2024 | 0 (placeholder) |

### Turnout Data
- Complete for original period (1996-2018)
- Incomplete for extension period (requires CVAP data)

## Analytical Notes

### Primary Extension Analysis
Given data availability, the primary extension analysis should focus on:

1. **2020 Presidential Election**: Complete county-level data for all three states
2. **California VCA Expansion**: Staggered treatment from 5 counties (2018) to 15 counties (2020)

### Identification Strategy
- **California**: Within-state variation exploiting VCA rollout timing
- **Cross-state**: Compare California VCA counties to Utah/Washington (always-treated)

### Limitations
1. **2022/2024 data gaps**: Gubernatorial and presidential results not yet collected
2. **CVAP unavailable**: Turnout denominators require Census Bureau data
3. **Washington party registration**: No party registration limits some outcome variables

## Validation Checks

1. ✓ All 126 counties from original study included
2. ✓ No duplicate county-year combinations
3. ✓ Treatment variable correctly reflects VCA adoption timing
4. ✓ 2020 presidential vote shares computed correctly
5. ✓ Identifiers consistent with original data structure
