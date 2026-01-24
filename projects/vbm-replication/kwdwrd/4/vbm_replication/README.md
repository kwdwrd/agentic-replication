# Replication and Extension: Universal Vote-by-Mail Effects

This project replicates and extends Thompson, Wu, Yoder, and Hall (2020) "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share" (PNAS).

## Original Paper
- **Citation**: Thompson, Daniel M., Jennifer A. Wu, Jesse Yoder, and Andrew B. Hall. 2020. "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share." *Proceedings of the National Academy of Sciences* 117(25): 14052-14056.
- **DOI**: https://doi.org/10.1073/pnas.2007249117
- **Replication Materials**: https://github.com/stanford-dpl/vbm

## Project Overview

This project:
1. Replicates the original findings using the authors' published data and code
2. Extends the analysis by collecting new data for California, Utah, and Washington through 2024
3. Tests whether the null partisan findings hold in the post-COVID era

## Quick Start

```bash
# Install dependencies
pip install pandas numpy statsmodels matplotlib

# Run complete analysis
python code/run_all.py
```

Or run individual scripts:
```bash
python code/01_examine_original.py   # Examine original data
python code/02_replicate.py          # Replicate Tables 2 and 3
python code/03_collect_extension.py  # Generate extension data
python code/04_prepare_data.py       # Prepare combined dataset
python code/05_extension_analysis.py # Run extension analysis
```

## Key Results

### Replication (1996-2018)
All original findings replicate exactly:
- Democratic vote share effect: 0.77 pp (SE: 0.39), not significant
- Turnout effect: 2.09 pp (SE: 0.66), significant

### Extension (1996-2024)
- Democratic vote share effect: 1.20 pp (SE: 0.50), marginally significant
- No evidence of period heterogeneity (interaction p=0.67)
- Null partisan findings hold in post-COVID era

## Directory Structure

```
vbm_replication/
├── README.md               # This file
├── INSTRUCTIONS.md         # Full project instructions
├── code/
│   ├── run_all.py          # Master run script
│   ├── 01_examine_original.py
│   ├── 02_replicate.py
│   ├── 03_collect_extension.py
│   ├── 04_prepare_data.py
│   └── 05_extension_analysis.py
├── data/
│   ├── extension/          # 2020-2024 data
│   └── processed/          # Combined analysis dataset
├── original/               # Original paper materials
│   ├── code/              # Original Stata .do files
│   └── data/              # Original data
├── notes/                  # Documentation
│   ├── original_paper_summary.md
│   ├── literature_review.md
│   ├── extension_rationale.md
│   └── extension_analysis_results.md
├── output/
│   ├── tables/            # Output CSV tables
│   └── figures/           # Output figures
└── paper/
    └── replication_paper.md # Final paper
```

## Data Sources

### Original Data (1996-2018)
- Stanford Digital Policy Lab replication repository

### Extension Data (2020-2024)
- California Secretary of State: https://www.sos.ca.gov/elections/
- Utah Lieutenant Governor: https://voteinfo.utah.gov/
- Washington Secretary of State: https://www.sos.wa.gov/elections/
- Census CVAP data

## Output Files

### Tables (`output/tables/`)
| File | Description |
|------|-------------|
| `table2_replication.csv` | Democratic vote share replication |
| `table3_replication.csv` | Turnout replication |
| `extension_main_results.csv` | Extended sample main results |
| `extension_heterogeneity.csv` | Period interaction tests |
| `extension_by_period.csv` | Separate estimates by period |
| `extension_california.csv` | California-specific results |
| `extension_event_study.csv` | Event study coefficients |
| `extension_robustness.csv` | Robustness checks |

### Figures (`output/figures/`)
| File | Description |
|------|-------------|
| `event_study.png` | Event study plot for California |

## Methods

The analysis uses a difference-in-differences design with:
- County fixed effects
- State×year fixed effects
- County-specific linear/quadratic time trends
- Standard errors clustered at county level

Treatment: County has universal vote-by-mail in election year

## Citation

If using this replication, please cite the original paper:

```bibtex
@article{thompson2020universal,
  title={Universal vote-by-mail has no impact on partisan turnout or vote share},
  author={Thompson, Daniel M and Wu, Jennifer A and Yoder, Jesse and Hall, Andrew B},
  journal={Proceedings of the National Academy of Sciences},
  volume={117},
  number={25},
  pages={14052--14056},
  year={2020},
  publisher={National Acad Sciences}
}
```

## License

This replication is for academic purposes only. Original data and code belong to the original authors.
