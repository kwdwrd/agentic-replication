# Universal Vote-by-Mail and Partisan Outcomes: A Replication and Extension Through 2024

Replication and extension of Thompson, Wu, Yoder, and Hall (2020), "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share," *PNAS* 117(25): 14052-14056.

## Project Structure

```
vbm_replication/
├── code/
│   ├── 02_replicate.py          # Replicates Tables 2 and 3 from original paper
│   ├── 03_collect_extension.py  # Collects extension data (2020-2024)
│   ├── 04_merge_data.py         # Merges original + extension into analysis dataset
│   └── 05_extension_analysis.py # Extension analysis (main, heterogeneity, event study)
├── data/
│   ├── raw/                     # Raw collected data (election results, precinct data)
│   ├── processed/               # Merged analysis dataset
│   │   └── full_analysis_data.csv
│   └── extension/               # Extension-specific data
│       ├── extension_election_data.csv
│       └── california_vbm_adoption.csv
├── original/
│   ├── code/                    # Original Stata .do files from replication archive
│   ├── data/
│   │   ├── raw/                 # Original raw data files
│   │   └── modified/            # Original processed data (analysis.dta)
│   └── paper/                   # Original paper PDF
├── output/
│   ├── tables/                  # Result tables (CSV)
│   │   ├── table1_replication_comparison.csv
│   │   ├── table2_replication.csv
│   │   ├── table3_replication.csv
│   │   ├── table2_extension_main.csv
│   │   ├── table3_period_comparison.csv
│   │   ├── table4_heterogeneity.csv
│   │   ├── table5_california_only.csv
│   │   ├── table7_robustness_no2020.csv
│   │   ├── event_study_dem_voteshare.csv
│   │   ├── event_study_turnout.csv
│   │   └── extension_main_results.csv
│   └── paper/
│       └── paper.md             # Full paper manuscript
├── notes/
│   ├── original_materials_review.md
│   ├── original_paper_summary.md
│   ├── original_data_examination.md
│   ├── literature_review.md
│   ├── extension_rationale.md
│   ├── replication_comparison.md
│   └── extension_findings.md
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`

Install dependencies:
```bash
pip install -r requirements.txt
```

## Reproduction

Scripts should be run in order from the `vbm_replication/` directory:

```bash
# 1. Replicate original Tables 2 and 3
python code/02_replicate.py

# 2. Collect extension data (2020-2024)
#    Note: Raw data files must be present in data/raw/
python code/03_collect_extension.py

# 3. Merge original and extension data
python code/04_merge_data.py

# 4. Run extension analysis
python code/05_extension_analysis.py
```

Step 1 requires `original/data/modified/analysis.dta` from the Thompson et al. replication archive.

Steps 2-4 require the raw extension data files in `data/raw/`, which were collected from:
- California Secretary of State (county-level certified results)
- `tonmcg/US_County_Level_Election_Results_08-24` on GitHub (presidential county data)
- OpenElections (Utah 2022 precinct data)
- Washington Secretary of State (2022 Senate results)

## Data Sources

| Source | Coverage | Files |
|--------|----------|-------|
| Thompson et al. replication archive | 1996-2018, CA/UT/WA | `original/data/modified/analysis.dta` |
| CA Secretary of State | 2020/2022/2024 CA elections | `data/raw/california_county_election_results.csv` |
| tonmcg GitHub | 2020/2024 presidential | `data/raw/tonmcg_2020.csv`, `tonmcg_2024.csv` |
| OpenElections | 2022 UT Senate (precinct) | `data/raw/ut_2022_precinct.csv` |
| WA Secretary of State | 2022 WA Senate | Hardcoded in `03_collect_extension.py` |
| CA Secretary of State | VCA participating counties | `data/extension/california_vbm_adoption.csv` |

## Key Findings

1. **Replication succeeds:** All 12 original estimates reproduced within rounding tolerance (max difference: 0.0005).

2. **Null partisan effect holds through 2024:** VBM effect on Dem vote share is 0.004 (SE = 0.003) with quadratic trends on full 1996-2024 sample.

3. **Turnout effect persists but is attenuated post-2018:** Pooled turnout effect ~1.3pp; interaction with post-2018 indicator is negative, likely reflecting COVID-era confounding (CA Executive Order N-64-20).

4. **Clean event study:** No pre-trends for either partisan outcomes or turnout around CA VCA adoption.

## Original Paper

Thompson, Daniel M., Jennifer A. Wu, Jesse Yoder, and Andrew B. Hall. 2020. "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share." *Proceedings of the National Academy of Sciences* 117(25): 14052-14056. DOI: 10.1073/pnas.2007249117.

Replication archive: https://github.com/stanford-dpl/vbm
