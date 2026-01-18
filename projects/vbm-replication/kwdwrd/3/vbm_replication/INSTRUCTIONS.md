# VBM Replication Project - Instructions

## Overview

This project replicates Thompson, Wu, Yoder, and Hall (2020), "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share," PNAS.

## Stata to Python Translation Guide

### Core Regression Command: `reghdfe`

The original Stata code uses `reghdfe` for high-dimensional fixed effects regression. In Python, we use `linearmodels.PanelOLS`.

**Example Stata Code (Table 2, Column 1):**
```stata
reghdfe share_votes_dem treat, ///
    a(county_id state_year) vce(clust county_id)
```

**Python Equivalent:**
```python
from linearmodels.panel import PanelOLS
import pandas as pd

# Set multi-index for panel
df_panel = df.set_index(['county_id', 'state_year_id'])

# Define dependent and independent variables
y = df_panel['share_votes_dem']
X = df_panel[['treat']]

# Estimate with entity and time fixed effects
model = PanelOLS(y, X, entity_effects=True, time_effects=True)
result = model.fit(cov_type='clustered', cluster_entity=True)

print(f"Coefficient: {result.params['treat']:.4f}")
print(f"SE: {result.std_errors['treat']:.4f}")
```

### Fixed Effects Specifications

| Stata Absorb | Python Equivalent | Description |
|--------------|-------------------|-------------|
| `a(county_id)` | `entity_effects=True` | County fixed effects |
| `a(state_year)` | `time_effects=True` | State×year fixed effects |
| `a(county_id##c.year)` | Manual demeaning or interaction | County-specific linear trends |

### County-Specific Trends

For specifications with county-specific linear/quadratic trends (Columns 2-3), we need to:
1. Create county×year interaction terms
2. Either include them as controls or demean the data

**Approach 1: Manual demeaning within counties**
```python
# Remove county-specific linear trends
df['year_centered'] = df.groupby('county_id')['year'].transform(lambda x: x - x.mean())
# Then regress residualized outcome on residualized treatment
```

**Approach 2: Include as additional fixed effects**
```python
# Create county-specific year dummies or interactions
df['county_year'] = df['county_id'].astype(str) + '_' + df['year'].astype(str)
```

### Clustered Standard Errors

Stata: `vce(cluster county_id)`
Python: `fit(cov_type='clustered', cluster_entity=True)`

Note: `cluster_entity=True` clusters on the first index level (county_id in our setup).

### Key Data Preparation Steps

1. **Load Stata files**: Use `pd.read_stata()`
2. **Filter to general elections**: Already done in analysis.dta
3. **Create state_year**: `df['state_year'] = df['state'] + '_' + df['year'].astype(str)`
4. **Handle missing values**: Different outcomes have different coverage

### Expected Results

**Table 2 - Partisan Outcomes:**
| Outcome | Basic | Linear Trends | Quad Trends |
|---------|-------|---------------|-------------|
| Dem turnout share | 0.007 (0.003) | 0.001 (0.001) | 0.001 (0.001) |
| Dem vote share | 0.028 (0.011) | 0.011 (0.004) | 0.007 (0.003) |

**Table 3 - Participation Outcomes:**
| Outcome | Basic | Linear Trends | Quad Trends |
|---------|-------|---------------|-------------|
| Turnout | 0.021 (0.009) | 0.022 (0.007) | 0.021 (0.008) |
| VBM share | 0.186 (0.027) | 0.157 (0.035) | 0.136 (0.085) |

## Running the Analysis

1. Install requirements: `pip install -r requirements.txt`
2. Run scripts in numerical order:
   - `00_setup.py` - Set paths and import packages
   - `01_examine_original.py` - Review original data
   - `02_replicate.py` - Replicate Tables 2 and 3
   - `03_collect_extension.py` - Collect 2020-2024 data
   - `04_prepare_data.py` - Merge extension data
   - `05_extension_analysis.py` - Run extended analysis
   - `06_figures.py` - Create figures
   - `07_tables.py` - Format tables

## File Locations

- **Original code**: `original/code/`
- **Original data**: `original/data/modified/` (analysis-ready)
- **Our code**: `code/`
- **Extension data**: `data/extension/`
- **Outputs**: `output/tables/`, `output/figures/`
- **Documentation**: `notes/`
