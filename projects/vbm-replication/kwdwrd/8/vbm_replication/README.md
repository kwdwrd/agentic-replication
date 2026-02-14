# Replication and Extension: Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share

This project replicates and extends Thompson, Wu, Yoder, and Hall (2020), "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share" (PNAS).

## Key Findings

### Replication (1996-2018)
- Successfully replicated Tables 2 and 3 from the original paper
- All coefficients match within 0.001 of published values
- Confirms null effects of VBM on partisan outcomes

### Extension (2020-2024)
- Extended analysis to California's Voter's Choice Act adoption
- **Democratic Vote Share**: -0.013 (SE: 0.008), marginally significant
- **Turnout**: 0.006 (SE: 0.007), not significant
- Results consistent with original null findings

## Project Structure

```
vbm_replication/
├── README.md                    # This file
├── original/                    # Original paper materials
│   └── vbm_turnout_replication/ # Cloned from authors' GitHub
├── code/                        # Analysis scripts
│   ├── 02_replicate.py          # Replication of Tables 2 and 3
│   ├── 03_collect_extension.py  # Extension data collection
│   ├── 04_prepare_extension.py  # Extension data preparation
│   └── 05_extension_analysis.py # Extension analysis
├── data/
│   └── extension/               # Extension datasets (2020-2024)
├── notes/                       # Documentation
│   ├── original_materials_review.md
│   ├── original_paper_summary.md
│   ├── literature_review.md
│   ├── extension_rationale.md
│   ├── replication_comparison.md
│   ├── extension_data_collection.md
│   └── extension_analysis_results.md
├── output/
│   └── tables/                  # Generated tables
└── paper/
    └── replication_paper.md     # Final replication paper
```

## Reproduction Instructions

1. Install dependencies:
   ```bash
   pip install pandas numpy statsmodels scipy
   ```

2. Run analysis scripts in order:
   ```bash
   python code/02_replicate.py
   python code/04_prepare_extension.py
   python code/05_extension_analysis.py
   ```

## Data Sources

| Dataset | Source | Coverage |
|---------|--------|----------|
| Original Data | Thompson et al. (2020) Dataverse | 1996-2018 |
| Presidential Results | MIT Election Lab | 2020, 2024 |
| CA VCA Adoption | CA Secretary of State | 2018-2024 |
| CVAP | Census Bureau ACS | 2016-2020 |

## Original Paper Reference

Thompson, D. M., Wu, J. A., Yoder, J., & Hall, A. B. (2020). Universal vote-by-mail has no impact on partisan turnout or vote share. *Proceedings of the National Academy of Sciences*, 117(25), 14052-14056.

## Original Replication Materials

https://github.com/stanford-dpl/vbm
