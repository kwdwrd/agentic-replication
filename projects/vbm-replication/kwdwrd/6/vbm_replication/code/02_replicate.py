"""
02_replicate.py
Replicate Tables 2 and 3 from Thompson, Wu, Yoder, and Hall (2020)
"Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share"
PNAS 117(25): 14052-14056

Uses the original analysis.dta from the replication materials.
Implements reghdfe-equivalent regressions in Python using linearmodels.AbsorbingLS.
"""

import pandas as pd
import numpy as np
import pyreadstat
import warnings
from linearmodels.iv import AbsorbingLS
from linearmodels.iv.absorbing import Interaction
import os

warnings.filterwarnings('ignore')

# Paths
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, 'original', 'data', 'modified', 'analysis.dta')
OUTPUT_DIR = os.path.join(ROOT, 'output', 'tables')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_data():
    """Load the original analysis dataset."""
    df, meta = pyreadstat.read_dta(DATA_PATH)
    df['county_id'] = df['county_id'].astype(int)
    df['state_year_id'] = df['state_year_id'].astype(int)
    return df


def run_regression(sample, outcome, treat_var, spec, cluster_col='county_id',
                   state_year_col='state_year_id', label=""):
    """
    Run AbsorbingLS regression matching reghdfe specifications.

    Specs:
    - 'basic': county FE + state×year FE
    - 'linear': county FE + county-specific linear year trend + state×year FE
    - 'quad': county-specific linear + quadratic year trends + state×year FE
      (county FE is subsumed by county##c.year)
    """
    sample = sample.dropna(subset=[outcome, treat_var]).copy().reset_index(drop=True)

    y = sample[outcome]
    x = sample[[treat_var]]
    clusters = sample[cluster_col]

    # Build absorb DataFrame (pure categorical FE)
    # Build interactions list (category × continuous interactions)
    if spec == 'basic':
        # absorb(county_id state_year)
        absorb_df = pd.DataFrame({
            'county': pd.Categorical(sample['county_id']),
            'state_year': pd.Categorical(sample[state_year_col])
        })
        interactions = None

    elif spec == 'linear':
        # absorb(county_id county_id##c.year state_year)
        # county_id is in absorb; county_id##c.year as interaction; state_year in absorb
        absorb_df = pd.DataFrame({
            'county': pd.Categorical(sample['county_id']),
            'state_year': pd.Categorical(sample[state_year_col])
        })
        interact_county_year = Interaction(
            cat=pd.Series(pd.Categorical(sample['county_id'])),
            cont=sample[['year']]
        )
        interactions = interact_county_year

    elif spec == 'quad':
        # absorb(county_id##c.year county_id##c.year2 state_year)
        # county FE is subsumed by county##c.year (since the interaction
        # includes a county-specific intercept implicitly through demeaning).
        # But to be safe, include county FE in absorb too.
        absorb_df = pd.DataFrame({
            'county': pd.Categorical(sample['county_id']),
            'state_year': pd.Categorical(sample[state_year_col])
        })
        interact_county_year = Interaction(
            cat=pd.Series(pd.Categorical(sample['county_id'])),
            cont=sample[['year']]
        )
        interact_county_year2 = Interaction(
            cat=pd.Series(pd.Categorical(sample['county_id'])),
            cont=sample[['year2']]
        )
        interactions = [interact_county_year, interact_county_year2]
    else:
        raise ValueError(f"Unknown spec: {spec}")

    mod = AbsorbingLS(y, x, absorb=absorb_df, interactions=interactions)
    res = mod.fit(cov_type='clustered', clusters=clusters)

    beta = res.params[treat_var]
    se = res.std_errors[treat_var]
    n = int(res.nobs)
    n_counties = sample['county_id'].nunique()
    n_elections = sample[state_year_col].nunique()

    if label:
        print(f"  {label}: beta={beta:.4f}, SE={se:.4f}, N={n}, "
              f"Counties={n_counties}, Elections={n_elections}")

    return {
        'beta': beta, 'se': se, 'n': n,
        'n_counties': n_counties, 'n_elections': n_elections
    }


def replicate_table2(df):
    """
    Replicate Table 2: Partisan Outcomes
    Cols 1-3: Dem Turnout Share (share_votes_dem) — CA + UT only, 87 counties
    Cols 4-6: Dem Vote Share (dem_share, reshaped long) — all states, 126 counties
    """
    print("\n" + "=" * 70)
    print("TABLE 2 REPLICATION: Partisan Outcomes")
    print("=" * 70)

    results = {}

    # --- Columns 1-3: Dem Turnout Share ---
    print("\nColumns 1-3: Dem Turnout Share (share_votes_dem)")
    print("  Sample: CA + UT (WA lacks this variable)")

    sample = df.dropna(subset=['share_votes_dem']).copy()
    print(f"  Obs: {len(sample)}, States: {sorted(sample['state'].unique())}, "
          f"Counties: {sample['county_id'].nunique()}")

    for i, spec in enumerate(['basic', 'linear', 'quad'], 1):
        r = run_regression(sample, 'share_votes_dem', 'treat', spec,
                           label=f"Col {i} ({spec})")
        results[f'col{i}'] = r

    # --- Columns 4-6: Dem Vote Share (reshaped long) ---
    print("\nColumns 4-6: Dem Vote Share (dem_share, reshaped)")
    print("  Sample: All states, pooled across gov/pres/sen")

    # Reshape: stack dem_share_gov, dem_share_pres, dem_share_sen
    id_vars = ['state', 'county', 'county_id', 'year', 'state_year_id',
               'treat', 'year2', 'year3']
    reshape_df = df[id_vars + ['dem_share_gov', 'dem_share_pres', 'dem_share_sen']].copy()

    long_df = pd.melt(
        reshape_df,
        id_vars=id_vars,
        value_vars=['dem_share_gov', 'dem_share_pres', 'dem_share_sen'],
        var_name='office',
        value_name='dem_share'
    )
    long_df = long_df.dropna(subset=['dem_share']).copy()
    print(f"  Obs after reshape: {len(long_df)}, "
          f"Counties: {long_df['county_id'].nunique()}")

    # Note: state_year_id was constructed from the original data. In the
    # reshaped data the same state_year applies to all offices, which matches
    # the Stata behavior (reshape doesn't change state_year).

    for i, spec in enumerate(['basic', 'linear', 'quad'], 4):
        spec_name = ['basic', 'linear', 'quad'][i - 4]
        r = run_regression(long_df, 'dem_share', 'treat', spec_name,
                           label=f"Col {i} ({spec_name})")
        results[f'col{i}'] = r

    return results


def replicate_table3(df):
    """
    Replicate Table 3: Participation Outcomes
    Cols 1-3: Turnout Share (turnout_share) — all states, 126 counties
    Cols 4-6: VBM Share (vbm_share) — CA only, 58 counties
    """
    print("\n" + "=" * 70)
    print("TABLE 3 REPLICATION: Participation Outcomes")
    print("=" * 70)

    results = {}

    # --- Columns 1-3: Turnout Share ---
    print("\nColumns 1-3: Turnout Share (turnout_share)")
    print("  Sample: All states")

    sample = df.dropna(subset=['turnout_share']).copy()
    print(f"  Obs: {len(sample)}, Counties: {sample['county_id'].nunique()}")

    for i, spec in enumerate(['basic', 'linear', 'quad'], 1):
        r = run_regression(sample, 'turnout_share', 'treat', spec,
                           label=f"Col {i} ({spec})")
        results[f'col{i}'] = r

    # --- Columns 4-6: VBM Share (CA only) ---
    print("\nColumns 4-6: VBM Share (vbm_share)")
    print("  Sample: CA only")

    sample_ca = df[df['state'] == 'CA'].dropna(subset=['vbm_share']).copy()

    # For CA only, state_year_id contains only CA values
    # Re-factorize so it's consecutive within this subsample
    sample_ca = sample_ca.copy()
    sample_ca['state_year_ca'] = pd.factorize(
        sample_ca['year'].astype(str)
    )[0]

    print(f"  Obs: {len(sample_ca)}, Counties: {sample_ca['county_id'].nunique()}")

    for i, spec in enumerate(['basic', 'linear', 'quad'], 4):
        spec_name = ['basic', 'linear', 'quad'][i - 4]
        r = run_regression(sample_ca, 'vbm_share', 'treat', spec_name,
                           state_year_col='state_year_ca',
                           label=f"Col {i} ({spec_name})")
        results[f'col{i}'] = r

    return results


def main():
    print("Loading original analysis data...")
    df = load_data()
    print(f"Loaded: {df.shape[0]} rows x {df.shape[1]} columns")

    # Replicate Tables
    t2_results = replicate_table2(df)
    t3_results = replicate_table3(df)

    # Save raw results
    for tname, results in [('table2', t2_results), ('table3', t3_results)]:
        rows = []
        for col, r in results.items():
            rows.append({
                'Column': col, 'Beta': r['beta'], 'SE': r['se'],
                'N': r['n'], 'Counties': r['n_counties'],
                'Elections': r['n_elections']
            })
        pd.DataFrame(rows).to_csv(
            os.path.join(OUTPUT_DIR, f'{tname}_replication.csv'), index=False
        )

    # Comparison with original
    original_t2 = {
        'col1': (0.007, 0.003), 'col2': (0.001, 0.001), 'col3': (0.001, 0.001),
        'col4': (0.028, 0.011), 'col5': (0.011, 0.004), 'col6': (0.007, 0.003)
    }
    original_t3 = {
        'col1': (0.021, 0.009), 'col2': (0.022, 0.007), 'col3': (0.021, 0.008),
        'col4': (0.186, 0.027), 'col5': (0.157, 0.035), 'col6': (0.136, 0.085)
    }

    print("\n" + "=" * 70)
    print("COMPARISON WITH ORIGINAL PAPER")
    print("=" * 70)

    outcomes_t2 = ['Dem Turn Share'] * 3 + ['Dem Vote Share'] * 3
    outcomes_t3 = ['Turnout Share'] * 3 + ['VBM Share'] * 3
    specs = ['Basic', 'Linear', 'Quad'] * 2

    comparison_rows = []
    for table, orig, repl, outcomes in [
        ('Table 2', original_t2, t2_results, outcomes_t2),
        ('Table 3', original_t3, t3_results, outcomes_t3)
    ]:
        print(f"\n{table}:")
        print(f"{'Col':<6} {'Outcome':<18} {'Spec':<8} "
              f"{'Orig β(SE)':<16} {'Repl β(SE)':<18} {'Δβ':<10}")
        print("-" * 76)
        for i, col in enumerate(['col1', 'col2', 'col3', 'col4', 'col5', 'col6']):
            orig_b, orig_se = orig[col]
            repl_b = repl[col]['beta']
            repl_se = repl[col]['se']
            diff_b = repl_b - orig_b
            print(f"{col:<6} {outcomes[i]:<18} {specs[i]:<8} "
                  f"{orig_b:>6.3f}({orig_se:.3f})  "
                  f"{repl_b:>7.4f}({repl_se:.4f})  "
                  f"{diff_b:>+8.4f}")
            comparison_rows.append({
                'Table': table, 'Column': col, 'Outcome': outcomes[i],
                'Spec': specs[i],
                'Original_Beta': orig_b, 'Original_SE': orig_se,
                'Replicated_Beta': round(repl_b, 4),
                'Replicated_SE': round(repl_se, 4),
                'Diff_Beta': round(diff_b, 4),
                'N': repl[col]['n'],
                'Counties': repl[col]['n_counties'],
                'Elections': repl[col]['n_elections']
            })

    comp_df = pd.DataFrame(comparison_rows)
    comp_df.to_csv(os.path.join(OUTPUT_DIR, 'replication_comparison.csv'), index=False)
    print(f"\nResults saved to {OUTPUT_DIR}/")


if __name__ == '__main__':
    main()
