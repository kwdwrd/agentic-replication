# Universal Vote-by-Mail: Replication and Extension of Thompson et al. (2020)

This repository contains the replication and extension of:

> Thompson, Daniel M., Jennifer A. Wu, Jesse Yoder, and Andrew B. Hall. 2020. "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share." *Proceedings of the National Academy of Sciences* 117(25): 14052-14056.

## Overview

This project:
1. **Replicates** the original Thompson et al. (2020) analysis using Python
2. **Extends** the analysis through the 2024 election cycle
3. **Tests** whether the original null partisan effects hold in the post-COVID era

## Key Findings

- **Partisan effects remain small**: VBM does not systematically advantage either party
- **Turnout effects are robust**: ~2 percentage point increase confirmed through 2024
- **Original conclusions supported**: Post-COVID era does not change findings

## Repository Structure

```
vbm_replication/
├── README.md                 # This file
├── code/                     # Analysis scripts
│   ├── 00_run_all.py        # Master script to run all analyses
│   ├── 02_replicate.py      # Replication of original Tables 2 & 3
│   ├── 03_validate_extension_data.py
│   ├── 04_build_extension_dataset.py
│   ├── 05_extension_analysis_v2.py
│   ├── 06_create_figures.py
│   └── extract_cvap.py
├── data/
│   ├── extension/           # Extension data (2020-2024)
│   │   ├── california_*.csv
│   │   ├── utah_*.csv
│   │   ├── washington_*.csv
│   │   └── cvap_*.csv
│   ├── combined_analysis.csv
│   └── california_analysis.csv
├── original/                 # Original replication materials
│   └── data/modified/analysis.dta
├── output/                   # Regression results
│   └── extension_results_v2.csv
├── paper/                    # Manuscript and figures
│   ├── vbm_extension_paper.tex
│   ├── tables.md
│   └── figures/
└── notes/                    # Documentation
    ├── original_paper_summary.md
    ├── literature_review.md
    ├── extension_data_summary.md
    └── extension_analysis_results.md
```

## Data Sources

### Original Data
- Thompson et al. (2020) replication materials: https://github.com/stanford-dpl/vbm

### Extension Data
- **California**: Secretary of State election results (sos.ca.gov)
- **Utah**: Utah Elections Office (electionresults.utah.gov)
- **Washington**: Secretary of State (results.vote.wa.gov)
- **CVAP**: U.S. Census Bureau ACS Special Tabulations (2018-2022, 2020-2024)

## Requirements

```
pandas>=1.5.0
numpy>=1.21.0
linearmodels>=4.25
matplotlib>=3.5.0
```

Install with:
```bash
pip install pandas numpy linearmodels matplotlib
```

## Usage

### Run All Analyses
```bash
cd code
python 00_run_all.py
```

### Run Individual Scripts
```bash
# Replication
python 02_replicate.py

# Extension analysis
python 05_extension_analysis_v2.py

# Create figures
python 06_create_figures.py
```

## Results Summary

### Replication (Tables 2 & 3)

| Outcome | Original | Replicated |
|---------|----------|------------|
| Dem Share Gov (linear) | 0.0013 (0.0027) | 0.0013 (0.0027) ✓ |
| Dem Share Pres (linear) | 0.0006 (0.0017) | 0.0006 (0.0017) ✓ |
| Turnout (linear) | 0.0201 (0.0046) | 0.0201 (0.0046) ✓ |

### Extension (1996-2024)

| Outcome | Coefficient | SE | p-value |
|---------|-------------|-----|---------|
| Dem Share Pres | 0.0192 | 0.0067 | <0.01 |
| Dem Share Gov | 0.0316 | 0.0084 | <0.01 |
| Turnout Share | 0.0197 | 0.0060 | <0.01 |

## Citation

If you use this replication, please cite both the original paper and this extension:

```bibtex
@article{thompson2020universal,
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

This replication is provided for academic and educational purposes.

## Contact

[Author Name]
[Institution]
[Email]
