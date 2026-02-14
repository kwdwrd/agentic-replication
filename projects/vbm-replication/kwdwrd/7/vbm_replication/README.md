# VBM Replication and Extension Project

## Overview

This project replicates and extends Thompson, Wu, Yoder, and Hall (2020), "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share," published in *Proceedings of the National Academy of Sciences*.

**Original paper**: https://www.pnas.org/doi/10.1073/pnas.2007249117
**Original replication materials**: https://github.com/stanford-dpl/vbm

## Key Findings

### Replication
- Successfully replicated all main findings from Tables 2 and 3
- All coefficient estimates within 0.002 of published values
- Confirms VBM has no impact on partisan outcomes (original period 1996-2018)

### Extension (2020-2024)
- Extended analysis through 2024, adding 378 county-year observations
- **Democratic vote share**: 0.5pp effect (SE = 0.4pp, p > 0.10) with quadratic trends
- **Turnout**: 1.5pp effect (SE = 0.6pp) - smaller than original 2.1pp
- **VBM × Post2018 interaction**: Not significant (-0.005, SE = 0.008)
- **Conclusion**: Null partisan effects persist in post-COVID era

## Project Structure

```
vbm_replication/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── original/                    # Original paper materials
│   ├── code/                    # Original Stata .do files
│   └── data/
│       ├── raw/                 # Original raw data
│       └── modified/            # Original cleaned datasets (analysis.dta)
├── code/                        # Python analysis code
│   ├── 01_examine_original.py   # Examine original data structure
│   ├── 02_replicate.py          # Replicate Tables 2 and 3
│   ├── 03_collect_extension.py  # Collect 2020-2024 data
│   ├── 04_prepare_data.py       # Merge original and extension
│   └── 05_extension_analysis.py # Run extension analyses
├── data/
│   ├── extension/               # New 2020-2024 data
│   │   ├── california_results_*.csv
│   │   ├── california_vca_adoption.csv
│   │   ├── utah_results_*.csv
│   │   ├── washington_results_*.csv
│   │   └── cvap_data.csv
│   └── processed/               # Merged analysis datasets
│       └── full_analysis_data.csv
├── notes/                       # Documentation
│   ├── original_materials_review.md
│   ├── original_paper_summary.md
│   ├── literature_review.md
│   ├── extension_rationale.md
│   ├── replication_comparison.md
│   └── checkpoint5_extension_analysis.md
├── output/
│   └── tables/                  # Analysis output tables
│       ├── extension_main_results.csv
│       ├── extension_heterogeneous_effects.csv
│       ├── extension_by_period.csv
│       ├── extension_california.csv
│       └── extension_robustness.csv
├── paper/                       # Final paper
│   ├── vbm_extension_paper.md   # Main paper text
│   └── tables.md                # Formatted tables
└── logs/                        # Execution logs
```

## Reproduction Instructions

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Ensure original data is available
# (analysis.dta should be in original/data/modified/)
```

### Run Analysis

Execute code files in numerical order:

```bash
cd vbm_replication

# 1. Examine original data
python code/01_examine_original.py

# 2. Replicate original findings
python code/02_replicate.py

# 3. Collect extension data (2020-2024)
python code/03_collect_extension.py

# 4. Prepare merged dataset
python code/04_prepare_data.py

# 5. Run extension analysis
python code/05_extension_analysis.py
```

### Output

Results are saved to:
- `output/tables/` - CSV files with regression results
- `paper/` - Final paper and formatted tables

## Data Sources

### Original Data (1996-2018)
- Thompson et al. (2020) replication materials from Stanford DPL
- 1,454 county-year observations
- 126 counties (CA: 58, UT: 29, WA: 39)

### Extension Data (2020-2024)
- **California Secretary of State**: County-level election results, VCA adoption status
- **Utah Lieutenant Governor**: County-level election results
- **Washington Secretary of State**: County-level election results
- **U.S. Census Bureau**: Citizen Voting Age Population (CVAP) estimates

## Methodology

### Identification Strategy
Two-way fixed effects with staggered treatment timing:

```
Y_cst = β·VBM_cst + γ_cs + δ_st + Σ(α_c·t + φ_c·t²) + ε_cst
```

- County fixed effects (γ_cs)
- State × Year fixed effects (δ_st)
- County-specific linear and quadratic trends
- Standard errors clustered at county level

### Implementation
- Manual iterative demeaning for fixed effects absorption
- Cluster-robust standard errors with Stata's finite-sample correction
- Python implementation verified against original Stata results

## Results Summary

| Outcome | Original (1996-2018) | Extension (2020-2024) | Full (1996-2024) |
|---------|---------------------|----------------------|------------------|
| Dem Vote Share (quad) | 0.007 (0.007) | ~0.000 (0.003) | 0.005 (0.004) |
| Turnout (quad) | 0.022 (0.007)** | ~0.000 (0.004) | 0.015 (0.006)* |

*Standard errors in parentheses. ** p < 0.01, * p < 0.05*

## Citation

If you use this replication, please cite:

```
Thompson, D. M., Wu, J. A., Yoder, J., & Hall, A. B. (2020).
Universal vote-by-mail has no impact on partisan turnout or vote share.
Proceedings of the National Academy of Sciences, 117(25), 14052-14056.
```

## License

This replication is for academic purposes only. Original data and code remain property of the original authors.
