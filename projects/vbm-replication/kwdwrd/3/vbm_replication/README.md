# VBM Replication and Extension Project

## Overview

This project replicates and extends Thompson, Wu, Yoder, and Hall (2020), "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share," published in *PNAS*. The extension includes the 2020 presidential election and California's continued Voter's Choice Act (VCA) expansion.

**Main Finding**: The null partisan effect of universal vote-by-mail is robust to including the 2020 presidential election. The California-specific difference-in-differences estimate is -0.004 (SE = 0.007), statistically indistinguishable from zero.

## Original Paper

- **Citation**: Thompson, Daniel M., Jennifer A. Wu, Jesse Yoder, and Andrew B. Hall. 2020. "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share." *Proceedings of the National Academy of Sciences* 117(25): 14052-14056.
- **DOI**: https://doi.org/10.1073/pnas.2007249117
- **Replication Materials**: https://github.com/stanford-dpl/vbm

## Project Structure

```
vbm_replication/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
│
├── code/                        # Analysis code (Python)
│   ├── 00_run_all.py           # Master script to run all analyses
│   ├── 01_setup.py             # Setup and verification script
│   ├── 02_replicate.py         # Replicate original findings
│   ├── 03_collect_extension.py # Collect extension data
│   ├── 04_merge_extension.py   # Merge and prepare extension dataset
│   └── 05_extension_analysis.py # Run extension analysis
│
├── data/
│   ├── extension/              # Extension data (2020-2024)
│   │   ├── california_vca_adoption.csv
│   │   ├── three_states_2020_pres.csv
│   │   └── treatment_extension.csv
│   └── combined/               # Combined datasets
│       ├── analysis_extended.csv
│       ├── analysis_extended_pres.csv
│       └── analysis_extended.dta
│
├── original/                   # Original replication materials
│   ├── code/                   # Original Stata .do files
│   └── data/modified/          # Original analysis dataset
│
├── notes/                      # Documentation
│   ├── original_paper_summary.md
│   ├── literature_review.md
│   ├── extension_rationale.md
│   ├── replication_comparison.md
│   ├── extension_data_validation.md
│   ├── extension_dataset_documentation.md
│   └── extension_analysis_results.md
│
├── output/
│   └── tables/                 # Output tables (CSV)
│       ├── replication_comparison.csv
│       ├── extension_extended_panel.csv
│       ├── extension_california.csv
│       ├── extension_heterogeneity.csv
│       ├── extension_event_study.csv
│       ├── extension_robustness.csv
│       └── extension_summary.csv
│
└── paper/                      # Paper files
    ├── main.tex               # Main paper
    ├── appendix.tex           # Online appendix
    └── references.bib         # Bibliography
```

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Verify setup
python code/01_setup.py

# 3. Run all analyses
python code/00_run_all.py

# Or run individual scripts:
python code/02_replicate.py         # Replicate original
python code/03_collect_extension.py # Collect extension data
python code/04_merge_extension.py   # Merge datasets
python code/05_extension_analysis.py # Extension analysis
```

## Key Results

### Replication (Table 2: Democratic Vote Share)
| Outcome | Original | Replicated | Match |
|---------|----------|------------|-------|
| Presidential | 0.006 (0.016) | 0.006 (0.016) | ✓ |
| Gubernatorial | -0.006 (0.012) | -0.006 (0.012) | ✓ |

### Extension Analysis
| Specification | Coefficient | Std. Error | N |
|--------------|-------------|------------|---|
| Original (2000-2016) | 0.031 | 0.014 | 630 |
| Extended (2000-2020) | 0.017 | 0.008 | 756 |
| California DiD | -0.004 | 0.007 | 116 |
| California only | 0.002 | 0.010 | 348 |

## Data Sources

### Original Data
- Stanford Democracy and Polarization Lab replication repository
- 126 counties (58 CA, 29 UT, 39 WA), 1996-2018

### Extension Data
- **2020 Presidential Results**: MIT Election Data + Science Lab
- **California VCA Adoption**: California Secretary of State
- **Treatment Status**: State election office records

## Requirements

- Python 3.8+
- pandas >= 1.5.0
- numpy >= 1.20.0
- statsmodels >= 0.13.0
- pyfixest >= 0.10.0 (recommended)

## Citation

If you use this replication, please cite both the original paper and this replication:

```bibtex
@article{thompson2020,
  title={Universal vote-by-mail has no impact on partisan turnout or vote share},
  author={Thompson, Daniel M and Wu, Jennifer A and Yoder, Jesse and Hall, Andrew B},
  journal={Proceedings of the National Academy of Sciences},
  volume={117},
  number={25},
  pages={14052--14056},
  year={2020}
}
```

## License

This replication is for academic purposes. Original data and code are subject to the terms of the original replication package.
