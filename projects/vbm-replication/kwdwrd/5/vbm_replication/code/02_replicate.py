"""
02_replicate.py
Replicate Tables 2 and 3 from Thompson, Wu, Yoder, and Hall (2020)
using the original analysis.dta dataset.

Approach: Use dummy variable OLS with statsmodels for two-way FE,
and manual within-transformation for specifications with county trends.
Standard errors clustered at county level throughout.
"""

import pandas as pd
import numpy as np
import os
import warnings
import statsmodels.api as sm
from scipy import linalg
warnings.filterwarnings('ignore')

# Paths
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, 'original', 'data', 'modified', 'analysis.dta')
OUTPUT_DIR = os.path.join(ROOT, 'output', 'tables')
os.makedirs(OUTPUT_DIR, exist_ok=True)

###############################################################################
# Load data
###############################################################################
print("Loading analysis.dta...")
df = pd.read_stata(DATA_PATH)
print(f"  Loaded {df.shape[0]} rows x {df.shape[1]} columns")
print(f"  States: {sorted(df['state'].unique())}")
print(f"  Years: {sorted(df['year'].unique())}")
print(f"  Counties: {df['county_id'].nunique()}")
print()

###############################################################################
# Helper: Demean within groups (Frisch-Waugh-Lovell for FE)
###############################################################################

def demean_by_groups(data, vars_to_demean, group_vars):
    """Demean variables within groups defined by group_vars."""
    result = data[vars_to_demean].copy()
    for gv in group_vars:
        group_means = data.groupby(gv)[vars_to_demean].transform('mean')
        result = result - group_means
    # For multi-way FE, iterate demeaning until convergence (alternating projections)
    if len(group_vars) > 1:
        for iteration in range(100):
            old = result.copy()
            for gv in group_vars:
                group_means = result.copy()
                group_means[gv] = data[gv].values
                gm = group_means.groupby(gv)[vars_to_demean].transform('mean')
                result = result - gm
            change = (result - old).abs().max().max()
            if change < 1e-10:
                break
    return result


def run_reghdfe(data, yvar, xvar, fe_list, cluster_var,
                add_linear_trend=False, add_quad_trend=False):
    """
    Replicate Stata's reghdfe using projection/demeaning approach.

    For county-specific trends: We residualize y and x on all FE
    including county x year and county x year^2 interactions,
    then run OLS on residuals with clustered SEs.
    """
    # Drop missing
    subset = data.dropna(subset=[yvar, xvar]).copy()
    subset = subset.reset_index(drop=True)

    n = len(subset)
    y = subset[yvar].values.astype(float)
    x = subset[xvar].values.astype(float)
    cluster = subset[cluster_var].values

    # Build projection matrices via iterative demeaning
    # Variables to demean: y, x, and any continuous interaction terms
    county_ids = subset['county_id'].values.astype(int)
    state_year_ids = subset['state_year_id'].values.astype(int)
    years = subset['year'].values.astype(float)
    years2 = years ** 2

    # Iterative demeaning for multi-way FE with interactions
    y_res = y.copy()
    x_res = x.copy()

    for iteration in range(200):
        y_old = y_res.copy()
        x_old = x_res.copy()

        # Demean by county_id
        for cid in np.unique(county_ids):
            mask = county_ids == cid
            y_res[mask] -= y_res[mask].mean()
            x_res[mask] -= x_res[mask].mean()

        # Demean by state_year_id
        for syid in np.unique(state_year_ids):
            mask = state_year_ids == syid
            y_res[mask] -= y_res[mask].mean()
            x_res[mask] -= x_res[mask].mean()

        # If linear trends: project out county-specific linear trends
        if add_linear_trend:
            for cid in np.unique(county_ids):
                mask = county_ids == cid
                if mask.sum() > 1:
                    t = years[mask]
                    # Project out linear trend for this county
                    t_dm = t - t.mean()
                    denom = (t_dm ** 2).sum()
                    if denom > 0:
                        beta_y = (t_dm * y_res[mask]).sum() / denom
                        y_res[mask] -= beta_y * t_dm
                        beta_x = (t_dm * x_res[mask]).sum() / denom
                        x_res[mask] -= beta_x * t_dm

        # If quadratic trends: also project out county-specific quadratic
        if add_quad_trend:
            for cid in np.unique(county_ids):
                mask = county_ids == cid
                if mask.sum() > 2:
                    t = years[mask]
                    t2 = years2[mask]
                    # Project out linear + quadratic for this county
                    T = np.column_stack([t - t.mean(), t2 - t2.mean()])
                    # Orthogonalize
                    try:
                        proj = T @ np.linalg.solve(T.T @ T, T.T)
                        y_res[mask] -= proj @ y_res[mask]
                        x_res[mask] -= proj @ x_res[mask]
                    except np.linalg.LinAlgError:
                        pass

        # Check convergence
        y_change = np.max(np.abs(y_res - y_old))
        x_change = np.max(np.abs(x_res - x_old))
        if y_change < 1e-10 and x_change < 1e-10:
            break

    # OLS on demeaned data: y_res = beta * x_res + e
    beta = (x_res * y_res).sum() / (x_res * x_res).sum()
    residuals = y_res - beta * x_res

    # Clustered standard errors
    unique_clusters = np.unique(cluster)
    n_clusters = len(unique_clusters)

    # Meat of the sandwich
    # For each cluster, compute sum of x_res * residual
    score_sum = np.zeros(n_clusters)
    for i, c in enumerate(unique_clusters):
        mask = cluster == c
        score_sum[i] = (x_res[mask] * residuals[mask]).sum()

    # Variance: (G/(G-1)) * (N-1)/(N-K) * sum(s_g^2) / (sum(x^2))^2
    # Where K = 1 (just beta) but with FE absorbed
    xxinv = 1.0 / (x_res * x_res).sum()
    meat = (score_sum ** 2).sum()
    # Small-sample correction: G/(G-1)
    correction = n_clusters / (n_clusters - 1)
    var_beta = correction * xxinv * meat * xxinv
    se = np.sqrt(var_beta)

    n_counties = len(np.unique(county_ids))
    state_year_str = np.array([f"{s}_{int(y)}" for s, y in
                               zip(subset['state'].values, subset['year'].values)])
    n_elections = len(np.unique(state_year_str))

    return {
        'coef': beta,
        'se': se,
        'n_obs': n,
        'n_counties': n_counties,
        'n_elections': n_elections,
        'ci_lower': beta - 1.96 * se,
        'ci_upper': beta + 1.96 * se,
    }


###############################################################################
# Prepare data
###############################################################################
df['county_id'] = df['county_id'].astype(int)
df['state_year_id'] = df['state_year_id'].astype(int)
df['treat'] = df['treat'].astype(float)
df['year'] = df['year'].astype(float)
df['year2'] = df['year'].astype(float) ** 2
df['state_year_str'] = df['state'] + '_' + df['year'].astype(int).astype(str)

# For Table 2 cols 4-6: reshape dem_share long across offices
df_vote = df[['state', 'county', 'county_id', 'year', 'year2',
              'state_year_id', 'treat', 'state_year_str',
              'dem_share_gov', 'dem_share_pres', 'dem_share_sen']].copy()

df_long = pd.melt(
    df_vote,
    id_vars=['state', 'county', 'county_id', 'year', 'year2',
             'state_year_id', 'treat', 'state_year_str'],
    value_vars=['dem_share_gov', 'dem_share_pres', 'dem_share_sen'],
    var_name='office',
    value_name='dem_share'
)
df_long = df_long.dropna(subset=['dem_share']).copy()
print(f"Reshaped vote share data: {df_long.shape[0]} rows, "
      f"{df_long['county_id'].nunique()} counties")
print()

###############################################################################
# TABLE 2: Partisan Outcomes
###############################################################################
print("=" * 70)
print("TABLE 2: PARTISAN OUTCOMES")
print("=" * 70)
print()

results_t2 = {}

# Columns 1-3: Democratic Turnout Share (CA + UT only)
print("--- Dem Turnout Share (cols 1-3) ---")
for spec_name, linear, quad in [('basic', False, False),
                                ('linear', True, False),
                                ('quad', True, True)]:
    res = run_reghdfe(
        data=df,
        yvar='share_votes_dem',
        xvar='treat',
        fe_list=['county_id', 'state_year_id'],
        cluster_var='county_id',
        add_linear_trend=linear,
        add_quad_trend=quad,
    )
    results_t2[f'dem_turnout_{spec_name}'] = res
    print(f"  {spec_name}: coef={res['coef']:.4f}, SE={res['se']:.4f}, "
          f"N={res['n_obs']}, counties={res['n_counties']}, "
          f"elections={res['n_elections']}")

print()

# Columns 4-6: Democratic Vote Share (all 3 states, reshaped long)
print("--- Dem Vote Share (cols 4-6) ---")
for spec_name, linear, quad in [('basic', False, False),
                                ('linear', True, False),
                                ('quad', True, True)]:
    res = run_reghdfe(
        data=df_long,
        yvar='dem_share',
        xvar='treat',
        fe_list=['county_id', 'state_year_id'],
        cluster_var='county_id',
        add_linear_trend=linear,
        add_quad_trend=quad,
    )
    results_t2[f'dem_voteshare_{spec_name}'] = res
    print(f"  {spec_name}: coef={res['coef']:.4f}, SE={res['se']:.4f}, "
          f"N={res['n_obs']}, counties={res['n_counties']}, "
          f"elections={res['n_elections']}")

print()

###############################################################################
# TABLE 3: Participation Outcomes
###############################################################################
print("=" * 70)
print("TABLE 3: PARTICIPATION OUTCOMES")
print("=" * 70)
print()

results_t3 = {}

# Columns 1-3: Turnout (all 3 states)
print("--- Turnout (cols 1-3) ---")
for spec_name, linear, quad in [('basic', False, False),
                                ('linear', True, False),
                                ('quad', True, True)]:
    res = run_reghdfe(
        data=df,
        yvar='turnout_share',
        xvar='treat',
        fe_list=['county_id', 'state_year_id'],
        cluster_var='county_id',
        add_linear_trend=linear,
        add_quad_trend=quad,
    )
    results_t3[f'turnout_{spec_name}'] = res
    print(f"  {spec_name}: coef={res['coef']:.4f}, SE={res['se']:.4f}, "
          f"N={res['n_obs']}, counties={res['n_counties']}, "
          f"elections={res['n_elections']}")

print()

# Columns 4-6: VBM Share (CA only)
print("--- VBM Share (cols 4-6, CA only) ---")
df_ca = df[df['state'] == 'CA'].copy()
for spec_name, linear, quad in [('basic', False, False),
                                ('linear', True, False),
                                ('quad', True, True)]:
    res = run_reghdfe(
        data=df_ca,
        yvar='vbm_share',
        xvar='treat',
        fe_list=['county_id', 'state_year_id'],
        cluster_var='county_id',
        add_linear_trend=linear,
        add_quad_trend=quad,
    )
    results_t3[f'vbm_share_{spec_name}'] = res
    print(f"  {spec_name}: coef={res['coef']:.4f}, SE={res['se']:.4f}, "
          f"N={res['n_obs']}, counties={res['n_counties']}, "
          f"elections={res['n_elections']}")

print()

###############################################################################
# Save results
###############################################################################

# Table 2
t2_rows = []
for col_idx, (key, orig_coef, orig_se) in enumerate([
    ('dem_turnout_basic', 0.007, 0.003),
    ('dem_turnout_linear', 0.001, 0.001),
    ('dem_turnout_quad', 0.001, 0.001),
    ('dem_voteshare_basic', 0.028, 0.011),
    ('dem_voteshare_linear', 0.011, 0.004),
    ('dem_voteshare_quad', 0.007, 0.003),
]):
    r = results_t2[key]
    t2_rows.append({
        'Column': col_idx + 1,
        'Outcome': 'Dem Turnout Share' if col_idx < 3 else 'Dem Vote Share',
        'Specification': ['Basic', 'Linear Trends', 'Quad Trends'][col_idx % 3],
        'Original_Coef': orig_coef,
        'Original_SE': orig_se,
        'Replicated_Coef': round(r['coef'], 4),
        'Replicated_SE': round(r['se'], 4),
        'Difference_Coef': round(r['coef'] - orig_coef, 4),
        'N_obs': r['n_obs'],
        'N_counties': r['n_counties'],
        'N_elections': r['n_elections'],
    })

df_t2 = pd.DataFrame(t2_rows)
df_t2.to_csv(os.path.join(OUTPUT_DIR, 'table2_replication.csv'), index=False)
print("Table 2 saved to output/tables/table2_replication.csv")

# Table 3
t3_rows = []
for col_idx, (key, orig_coef, orig_se) in enumerate([
    ('turnout_basic', 0.021, 0.009),
    ('turnout_linear', 0.022, 0.007),
    ('turnout_quad', 0.021, 0.008),
    ('vbm_share_basic', 0.186, 0.027),
    ('vbm_share_linear', 0.157, 0.035),
    ('vbm_share_quad', 0.136, 0.085),
]):
    r = results_t3[key]
    t3_rows.append({
        'Column': col_idx + 1,
        'Outcome': 'Turnout' if col_idx < 3 else 'VBM Share',
        'Specification': ['Basic', 'Linear Trends', 'Quad Trends'][col_idx % 3],
        'Original_Coef': orig_coef,
        'Original_SE': orig_se,
        'Replicated_Coef': round(r['coef'], 4),
        'Replicated_SE': round(r['se'], 4),
        'Difference_Coef': round(r['coef'] - orig_coef, 4),
        'N_obs': r['n_obs'],
        'N_counties': r['n_counties'],
        'N_elections': r['n_elections'],
    })

df_t3 = pd.DataFrame(t3_rows)
df_t3.to_csv(os.path.join(OUTPUT_DIR, 'table3_replication.csv'), index=False)
print("Table 3 saved to output/tables/table3_replication.csv")

print()
print("=" * 70)
print("REPLICATION COMPARISON")
print("=" * 70)

print("\nTable 2:")
print(df_t2[['Column', 'Outcome', 'Specification', 'Original_Coef',
             'Replicated_Coef', 'Difference_Coef', 'Original_SE',
             'Replicated_SE']].to_string(index=False))

print("\nTable 3:")
print(df_t3[['Column', 'Outcome', 'Specification', 'Original_Coef',
             'Replicated_Coef', 'Difference_Coef', 'Original_SE',
             'Replicated_SE']].to_string(index=False))
