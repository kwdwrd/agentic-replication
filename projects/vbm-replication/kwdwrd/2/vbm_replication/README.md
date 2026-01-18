# Replication and Extension: Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share

## Overview

This project replicates and extends Thompson, Wu, Yoder, and Hall (2020), "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share," published in *PNAS*.

**Original paper**: https://www.pnas.org/doi/10.1073/pnas.2007249117
**Original replication materials**: https://github.com/stanford-dpl/vbm

## Project Structure

```
vbm_replication/
├── README.md
├── INSTRUCTIONS.md
├── requirements.txt
├── original/                    # Original paper materials
│   ├── code/                    # Stata .do files
│   ├── data/
│   │   ├── raw/                 # Original source data
│   │   └── modified/            # Cleaned analysis datasets
│   └── paper/
├── code/                        # Python analysis code
├── data/
│   ├── raw/                     # Downloaded data
│   ├── processed/               # Cleaned datasets
│   └── extension/               # New 2020-2024 data
├── notes/                       # Documentation
├── output/
│   ├── tables/
│   ├── figures/
│   └── paper/
└── logs/
```

## Replication Summary

### Original Paper Findings

The paper uses a difference-in-differences design exploiting staggered adoption of universal vote-by-mail (VBM) across counties in California, Utah, and Washington from 1996-2018.

**Key findings:**
- VBM has no significant effect on Democratic turnout share or vote share
- VBM increases overall turnout by ~2 percentage points
- VBM dramatically increases the share of ballots cast by mail

### Extension

This project extends the analysis through 2024 to test whether:
1. The null partisan findings hold in the post-COVID era
2. Results are robust to the politicization of mail voting after 2020

## Data Sources

- **Original**: Replication materials from Stanford-DPL GitHub repository
- **Extension**:
  - California Secretary of State election results
  - California VCA adoption data
  - Utah Lieutenant Governor election results
  - Washington Secretary of State election results
  - Census CVAP data (2020-based)

## Requirements

```bash
pip install -r requirements.txt
```

## Running the Analysis

```bash
# 1. Examine original data
python code/01_examine_original.py

# 2. Replicate original results
python code/02_replicate.py

# 3. Collect extension data
python code/03_collect_extension.py

# 4. Prepare merged dataset
python code/04_prepare_data.py

# 5. Run extension analysis
python code/05_extension_analysis.py

# 6. Create figures
python code/06_figures.py

# 7. Format tables
python code/07_tables.py
```

## Citation

Original paper:
```
Thompson, D. M., Wu, J. A., Yoder, J., & Hall, A. B. (2020). Universal vote-by-mail
has no impact on partisan turnout or vote share. Proceedings of the National Academy
of Sciences, 117(25), 14052-14056.
```

## Author

Replication and extension analysis conducted in January 2026.
