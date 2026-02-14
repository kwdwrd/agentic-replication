"""
05_extension_analysis.py
Extension analysis: Re-estimate Thompson et al. (2020) specifications
on full 1996-2024 dataset, run heterogeneity tests, CA-specific analysis,
event studies, and robustness checks.

Output: CSV tables in output/tables/
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, 'data', 'processed', 'full_analysis_data.csv')
OUTPUT_DIR = os.path.join(ROOT, 'output', 'tables')
os.makedirs(OUTPUT_DIR, exist_ok=True)

###############################################################################
# Load data
###############################################################################
print("Loading full analysis data...")
df = pd.read_csv(DATA_PATH)
print(f"  {len(df)} rows, years {int(df['year'].min())}-{int(df['year'].max())}")
print(f"  Counties: {df['county_id'].nunique()}, State-years: {df['state_year_id'].nunique()}")
print()

# Ensure correct types
df['county_id'] = df['county_id'].astype(int)
df['state_year_id'] = df['state_year_id'].astype(int)
df['treat'] = df['treat'].astype(float)
df['year'] = df['year'].astype(float)
df['year2'] = df['year'] ** 2

###############################################################################
# Core regression function (same as replication)
###############################################################################

def run_reghdfe(data, yvar, xvars, fe_list, cluster_var,
                add_linear_trend=False, add_quad_trend=False):
    """
    Two-way FE regression with optional county-specific trends.
    xvars can be a string (single var) or list of strings (multiple vars).
    Returns dict with coefficients, SEs, etc.
    """
    if isinstance(xvars, str):
        xvars = [xvars]

    # Drop missing on y and all x vars
    all_vars = [yvar] + xvars
    subset = data.dropna(subset=all_vars).copy().reset_index(drop=True)
    n = len(subset)
    if n == 0:
        return None

    y = subset[yvar].values.astype(float)
    X = np.column_stack([subset[v].values.astype(float) for v in xvars])
    k = X.shape[1]

    county_ids = subset['county_id'].values.astype(int)
    state_year_ids = subset['state_year_id'].values.astype(int)
    years = subset['year'].values.astype(float)
    years2 = years ** 2
    cluster = subset[cluster_var].values.astype(int)

    # Iterative demeaning
    y_res = y.copy()
    X_res = X.copy()

    for iteration in range(200):
        y_old = y_res.copy()
        X_old = X_res.copy()

        # Demean by county_id
        for cid in np.unique(county_ids):
            mask = county_ids == cid
            y_res[mask] -= y_res[mask].mean()
            for j in range(k):
                X_res[mask, j] -= X_res[mask, j].mean()

        # Demean by state_year_id
        for syid in np.unique(state_year_ids):
            mask = state_year_ids == syid
            y_res[mask] -= y_res[mask].mean()
            for j in range(k):
                X_res[mask, j] -= X_res[mask, j].mean()

        # Linear trends
        if add_linear_trend:
            for cid in np.unique(county_ids):
                mask = county_ids == cid
                if mask.sum() > 1:
                    t = years[mask]
                    t_dm = t - t.mean()
                    denom = (t_dm ** 2).sum()
                    if denom > 0:
                        beta_y = (t_dm * y_res[mask]).sum() / denom
                        y_res[mask] -= beta_y * t_dm
                        for j in range(k):
                            beta_x = (t_dm * X_res[mask, j]).sum() / denom
                            X_res[mask, j] -= beta_x * t_dm

        # Quadratic trends
        if add_quad_trend:
            for cid in np.unique(county_ids):
                mask = county_ids == cid
                if mask.sum() > 2:
                    t = years[mask]
                    t2 = years2[mask]
                    T = np.column_stack([t - t.mean(), t2 - t2.mean()])
                    try:
                        proj = T @ np.linalg.solve(T.T @ T, T.T)
                        y_res[mask] -= proj @ y_res[mask]
                        for j in range(k):
                            X_res[mask, j] -= proj @ X_res[mask, j]
                    except np.linalg.LinAlgError:
                        pass

        # Convergence
        y_change = np.max(np.abs(y_res - y_old))
        x_change = np.max(np.abs(X_res - X_old))
        if y_change < 1e-10 and x_change < 1e-10:
            break

    # OLS on demeaned data
    XtX = X_res.T @ X_res
    try:
        XtX_inv = np.linalg.inv(XtX)
    except np.linalg.LinAlgError:
        return None
    beta = XtX_inv @ (X_res.T @ y_res)
    residuals = y_res - X_res @ beta

    # Clustered standard errors
    unique_clusters = np.unique(cluster)
    G = len(unique_clusters)

    # Meat of sandwich
    meat = np.zeros((k, k))
    for c in unique_clusters:
        mask = cluster == c
        score = X_res[mask].T @ residuals[mask]  # k x 1
        meat += np.outer(score, score)

    # Sandwich: V = (G/(G-1)) * XtX_inv @ meat @ XtX_inv
    correction = G / (G - 1)
    V = correction * XtX_inv @ meat @ XtX_inv
    se = np.sqrt(np.diag(V))

    result = {
        'n_obs': n,
        'n_counties': len(np.unique(county_ids)),
        'n_clusters': G,
    }
    for j, v in enumerate(xvars):
        result[f'coef_{v}'] = beta[j]
        result[f'se_{v}'] = se[j]
        result[f'pval_{v}'] = 2 * (1 - _norm_cdf(abs(beta[j] / se[j])))

    return result


def _norm_cdf(x):
    """Standard normal CDF approximation."""
    from math import erf, sqrt
    return 0.5 * (1 + erf(x / sqrt(2)))


def fmt_coef(coef, se, stars=True):
    """Format coefficient with significance stars."""
    pval = 2 * (1 - _norm_cdf(abs(coef / se)))
    s = f"{coef:.4f}"
    if stars:
        if pval < 0.01:
            s += "***"
        elif pval < 0.05:
            s += "**"
        elif pval < 0.1:
            s += "*"
    return s


###############################################################################
# PART 1: Main results on full sample (extended Table 2 & 3)
###############################################################################
print("=" * 70)
print("PART 1: MAIN RESULTS ON FULL SAMPLE (1996-2024)")
print("=" * 70)

# --- Extended Table 2: Partisan outcomes ---
print("\n--- Extended Table 2: Partisan Outcomes ---")

# Cols 1-3: Dem registration share (share_votes_dem) — CA + UT only
# Note: This variable is only available for original period (1996-2018)
# So we can't extend cols 1-3. We report this as a limitation.
for spec_name, lt, qt in [('basic', False, False),
                           ('linear', True, False),
                           ('quad', True, True)]:
    r = run_reghdfe(df, 'share_votes_dem', 'treat',
                    ['county_id', 'state_year_id'], 'county_id',
                    add_linear_trend=lt, add_quad_trend=qt)
    if r:
        print(f"  Dem Reg Share {spec_name}: coef={r['coef_treat']:.4f}, "
              f"SE={r['se_treat']:.4f}, N={r['n_obs']}")

# Cols 4-6: Dem vote share (stacked gov/pres/sen) — all states, extended
print()
df_vote = df[['state', 'county', 'county_id', 'year', 'year2',
              'state_year_id', 'treat',
              'dem_share_gov', 'dem_share_pres', 'dem_share_sen']].copy()
df_long = pd.melt(df_vote,
                  id_vars=['state', 'county', 'county_id', 'year', 'year2',
                           'state_year_id', 'treat'],
                  value_vars=['dem_share_gov', 'dem_share_pres', 'dem_share_sen'],
                  var_name='office', value_name='dem_share')
df_long = df_long.dropna(subset=['dem_share']).reset_index(drop=True)

# Need unique state_year_id for the stacked data
# Each state-year-office combination needs a unique ID for the state_year FE
df_long['state_year_office'] = (df_long['state'] + '_' +
                                 df_long['year'].astype(int).astype(str) + '_' +
                                 df_long['office'])
df_long['state_year_office_id'] = pd.factorize(df_long['state_year_office'])[0] + 1
# Override state_year_id with the office-specific version
df_long_orig_syid = df_long['state_year_id'].copy()
df_long['state_year_id'] = df_long['state_year_office_id']

table2_results = []
for spec_name, lt, qt in [('basic', False, False),
                           ('linear', True, False),
                           ('quad', True, True)]:
    r = run_reghdfe(df_long, 'dem_share', 'treat',
                    ['county_id', 'state_year_id'], 'county_id',
                    add_linear_trend=lt, add_quad_trend=qt)
    if r:
        print(f"  Dem Vote Share {spec_name}: coef={r['coef_treat']:.4f}, "
              f"SE={r['se_treat']:.4f}, N={r['n_obs']}, counties={r['n_counties']}")
        table2_results.append({
            'outcome': 'dem_vote_share',
            'spec': spec_name,
            'coef': r['coef_treat'],
            'se': r['se_treat'],
            'n_obs': r['n_obs'],
            'n_counties': r['n_counties'],
        })

# --- Extended Table 3: Participation outcomes ---
print("\n--- Extended Table 3: Participation Outcomes ---")

# Cols 1-3: Turnout (all states, extended)
table3_results = []
for spec_name, lt, qt in [('basic', False, False),
                           ('linear', True, False),
                           ('quad', True, True)]:
    r = run_reghdfe(df, 'turnout_share', 'treat',
                    ['county_id', 'state_year_id'], 'county_id',
                    add_linear_trend=lt, add_quad_trend=qt)
    if r:
        print(f"  Turnout {spec_name}: coef={r['coef_treat']:.4f}, "
              f"SE={r['se_treat']:.4f}, N={r['n_obs']}, counties={r['n_counties']}")
        table3_results.append({
            'outcome': 'turnout',
            'spec': spec_name,
            'coef': r['coef_treat'],
            'se': r['se_treat'],
            'n_obs': r['n_obs'],
            'n_counties': r['n_counties'],
        })

# Cols 4-6: VBM share (CA only, original period only — no extension data)
for spec_name, lt, qt in [('basic', False, False),
                           ('linear', True, False),
                           ('quad', True, True)]:
    r = run_reghdfe(df, 'vbm_share', 'treat',
                    ['county_id', 'state_year_id'], 'county_id',
                    add_linear_trend=lt, add_quad_trend=qt)
    if r:
        print(f"  VBM Share {spec_name}: coef={r['coef_treat']:.4f}, "
              f"SE={r['se_treat']:.4f}, N={r['n_obs']}")

###############################################################################
# PART 2: Period comparison (original vs extension)
###############################################################################
print("\n" + "=" * 70)
print("PART 2: PERIOD COMPARISON (ORIGINAL vs EXTENSION)")
print("=" * 70)

# Run separately on original-period and extension-period data
for period_name, period_filter in [('Original (1996-2018)', 'original'),
                                     ('Extension (2020-2024)', 'extension')]:
    print(f"\n--- {period_name} ---")
    pdata = df[df['period'] == period_filter].copy()

    # Dem vote share (stacked)
    pv = pdata[['state', 'county', 'county_id', 'year', 'year2',
                'state_year_id', 'treat',
                'dem_share_gov', 'dem_share_pres', 'dem_share_sen']].copy()
    pl = pd.melt(pv,
                 id_vars=['state', 'county', 'county_id', 'year', 'year2',
                          'state_year_id', 'treat'],
                 value_vars=['dem_share_gov', 'dem_share_pres', 'dem_share_sen'],
                 var_name='office', value_name='dem_share')
    pl = pl.dropna(subset=['dem_share']).reset_index(drop=True)
    pl['syo'] = pl['state'] + '_' + pl['year'].astype(int).astype(str) + '_' + pl['office']
    pl['state_year_id'] = pd.factorize(pl['syo'])[0] + 1

    for spec_name, lt, qt in [('basic', False, False),
                               ('linear', True, False)]:
        r = run_reghdfe(pl, 'dem_share', 'treat',
                        ['county_id', 'state_year_id'], 'county_id',
                        add_linear_trend=lt, add_quad_trend=qt)
        if r:
            print(f"  Dem Vote Share {spec_name}: coef={r['coef_treat']:.4f}, "
                  f"SE={r['se_treat']:.4f}, N={r['n_obs']}")

    # Turnout
    for spec_name, lt, qt in [('basic', False, False),
                               ('linear', True, False)]:
        r = run_reghdfe(pdata, 'turnout_share', 'treat',
                        ['county_id', 'state_year_id'], 'county_id',
                        add_linear_trend=lt, add_quad_trend=qt)
        if r:
            print(f"  Turnout {spec_name}: coef={r['coef_treat']:.4f}, "
                  f"SE={r['se_treat']:.4f}, N={r['n_obs']}")

###############################################################################
# PART 3: Heterogeneity — VBM x Post-2018 interaction
###############################################################################
print("\n" + "=" * 70)
print("PART 3: HETEROGENEITY — VBM x POST-2018")
print("=" * 70)

df['post2018'] = (df['year'] > 2018).astype(float)
df['treat_x_post'] = df['treat'] * df['post2018']

# Dem vote share (stacked)
df_long2 = pd.melt(
    df[['state', 'county', 'county_id', 'year', 'year2',
        'state_year_id', 'treat', 'post2018', 'treat_x_post',
        'dem_share_gov', 'dem_share_pres', 'dem_share_sen']],
    id_vars=['state', 'county', 'county_id', 'year', 'year2',
             'state_year_id', 'treat', 'post2018', 'treat_x_post'],
    value_vars=['dem_share_gov', 'dem_share_pres', 'dem_share_sen'],
    var_name='office', value_name='dem_share')
df_long2 = df_long2.dropna(subset=['dem_share']).reset_index(drop=True)
df_long2['syo'] = (df_long2['state'] + '_' +
                    df_long2['year'].astype(int).astype(str) + '_' +
                    df_long2['office'])
df_long2['state_year_id'] = pd.factorize(df_long2['syo'])[0] + 1

print("\nDem Vote Share with interaction:")
for spec_name, lt, qt in [('basic', False, False),
                           ('linear', True, False),
                           ('quad', True, True)]:
    r = run_reghdfe(df_long2, 'dem_share', ['treat', 'treat_x_post'],
                    ['county_id', 'state_year_id'], 'county_id',
                    add_linear_trend=lt, add_quad_trend=qt)
    if r:
        print(f"  {spec_name}:")
        print(f"    treat: coef={r['coef_treat']:.4f}, SE={r['se_treat']:.4f}")
        print(f"    treat_x_post: coef={r['coef_treat_x_post']:.4f}, "
              f"SE={r['se_treat_x_post']:.4f}")

# Turnout with interaction
print("\nTurnout with interaction:")
for spec_name, lt, qt in [('basic', False, False),
                           ('linear', True, False),
                           ('quad', True, True)]:
    r = run_reghdfe(df, 'turnout_share', ['treat', 'treat_x_post'],
                    ['county_id', 'state_year_id'], 'county_id',
                    add_linear_trend=lt, add_quad_trend=qt)
    if r:
        print(f"  {spec_name}:")
        print(f"    treat: coef={r['coef_treat']:.4f}, SE={r['se_treat']:.4f}")
        print(f"    treat_x_post: coef={r['coef_treat_x_post']:.4f}, "
              f"SE={r['se_treat_x_post']:.4f}")

###############################################################################
# PART 4: California-only analysis (VCA stagger)
###############################################################################
print("\n" + "=" * 70)
print("PART 4: CALIFORNIA-ONLY ANALYSIS")
print("=" * 70)

ca = df[df['state'] == 'CA'].copy()
# Reset state_year_id for CA only
ca['state_year_id'] = pd.factorize(ca['year'])[0] + 1

# Dem vote share - stacked
ca_vote = ca[['state', 'county', 'county_id', 'year', 'year2',
              'state_year_id', 'treat',
              'dem_share_gov', 'dem_share_pres', 'dem_share_sen']].copy()
ca_long = pd.melt(ca_vote,
                  id_vars=['state', 'county', 'county_id', 'year', 'year2',
                           'state_year_id', 'treat'],
                  value_vars=['dem_share_gov', 'dem_share_pres', 'dem_share_sen'],
                  var_name='office', value_name='dem_share')
ca_long = ca_long.dropna(subset=['dem_share']).reset_index(drop=True)
ca_long['syo'] = ca_long['year'].astype(int).astype(str) + '_' + ca_long['office']
ca_long['state_year_id'] = pd.factorize(ca_long['syo'])[0] + 1

print("\nCA Dem Vote Share:")
for spec_name, lt, qt in [('basic', False, False),
                           ('linear', True, False),
                           ('quad', True, True)]:
    r = run_reghdfe(ca_long, 'dem_share', 'treat',
                    ['county_id', 'state_year_id'], 'county_id',
                    add_linear_trend=lt, add_quad_trend=qt)
    if r:
        print(f"  {spec_name}: coef={r['coef_treat']:.4f}, "
              f"SE={r['se_treat']:.4f}, N={r['n_obs']}, counties={r['n_counties']}")

# CA turnout
print("\nCA Turnout:")
for spec_name, lt, qt in [('basic', False, False),
                           ('linear', True, False),
                           ('quad', True, True)]:
    r = run_reghdfe(ca, 'turnout_share', 'treat',
                    ['county_id', 'state_year_id'], 'county_id',
                    add_linear_trend=lt, add_quad_trend=qt)
    if r:
        print(f"  {spec_name}: coef={r['coef_treat']:.4f}, "
              f"SE={r['se_treat']:.4f}, N={r['n_obs']}, counties={r['n_counties']}")

###############################################################################
# PART 5: Event study (CA VCA adoption)
###############################################################################
print("\n" + "=" * 70)
print("PART 5: EVENT STUDY (CA VCA ADOPTION)")
print("=" * 70)

# Load VCA adoption data to get first treatment year
vca = pd.read_csv(os.path.join(ROOT, 'data', 'extension', 'california_vbm_adoption.csv'))
vca_years = {}
for _, r in vca.iterrows():
    if pd.notna(r['vca_first_year']) and r['vca_first_year'] != '':
        vca_years[r['county']] = int(float(r['vca_first_year']))

# Create event time variable for CA counties
ca_es = ca.copy()
ca_es['first_treat_year'] = ca_es['county'].map(vca_years)

# For never-treated, set first_treat_year to a large value (inf)
ca_es['ever_treated'] = ca_es['first_treat_year'].notna().astype(int)
ca_es.loc[ca_es['first_treat_year'].isna(), 'first_treat_year'] = 9999

ca_es['event_time'] = ca_es['year'] - ca_es['first_treat_year']

# Only include treated counties in event study
ca_es_treated = ca_es[ca_es['ever_treated'] == 1].copy()

# Create lead/lag dummies: leads (pre-treatment): -6,-4,-2
# lags (post-treatment): 0, 2, 4, 6
# Reference period: event_time = -2 (omitted)
# Only even event times since elections are biennial

# Reset state_year_id for this subset
ca_es_treated['state_year_id'] = pd.factorize(ca_es_treated['year'])[0] + 1

# Create event time dummies
event_times = sorted(ca_es_treated['event_time'].unique())
print(f"Event times in data: {[int(e) for e in event_times]}")

# Select event times to include (exclude reference = -2)
# Use: -6, -4, 0, 2, 4, 6 (omit -2)
event_dummies = []
for et in [-6, -4, 0, 2, 4, 6]:
    col_name = f'et_{et}' if et < 0 else f'et_plus_{et}'
    ca_es_treated[col_name] = (ca_es_treated['event_time'] == et).astype(float)
    event_dummies.append(col_name)

# Stack vote share outcomes
ca_es_vote = ca_es_treated[['state', 'county', 'county_id', 'year', 'year2',
                             'state_year_id',
                             'dem_share_gov', 'dem_share_pres', 'dem_share_sen']
                            + event_dummies].copy()
ca_es_long = pd.melt(ca_es_vote,
                     id_vars=['state', 'county', 'county_id', 'year', 'year2',
                              'state_year_id'] + event_dummies,
                     value_vars=['dem_share_gov', 'dem_share_pres', 'dem_share_sen'],
                     var_name='office', value_name='dem_share')
ca_es_long = ca_es_long.dropna(subset=['dem_share']).reset_index(drop=True)
ca_es_long['syo'] = ca_es_long['year'].astype(int).astype(str) + '_' + ca_es_long['office']
ca_es_long['state_year_id'] = pd.factorize(ca_es_long['syo'])[0] + 1

# Run event study regression
print("\nEvent Study: Dem Vote Share (CA treated counties only)")
r = run_reghdfe(ca_es_long, 'dem_share', event_dummies,
                ['county_id', 'state_year_id'], 'county_id',
                add_linear_trend=True, add_quad_trend=False)
if r:
    print(f"  N={r['n_obs']}, counties={r['n_counties']}")
    print(f"  Event time coefficients (ref = -2):")
    es_results = []
    for ed in event_dummies:
        coef = r[f'coef_{ed}']
        se = r[f'se_{ed}']
        et = int(ed.replace('et_', '').replace('plus_', ''))
        print(f"    t={et:+d}: {fmt_coef(coef, se)} ({se:.4f})")
        es_results.append({
            'event_time': et,
            'coef': coef,
            'se': se,
            'ci_lower': coef - 1.96 * se,
            'ci_upper': coef + 1.96 * se,
        })

    es_df = pd.DataFrame(es_results)
    es_df.to_csv(os.path.join(OUTPUT_DIR, 'event_study_dem_voteshare.csv'), index=False)
    print(f"  Saved event study results")

# Event study for turnout
print("\nEvent Study: Turnout (CA treated counties only)")
r_turn = run_reghdfe(ca_es_treated, 'turnout_share', event_dummies,
                     ['county_id', 'state_year_id'], 'county_id',
                     add_linear_trend=True, add_quad_trend=False)
if r_turn:
    print(f"  N={r_turn['n_obs']}, counties={r_turn['n_counties']}")
    print(f"  Event time coefficients (ref = -2):")
    es_turn_results = []
    for ed in event_dummies:
        coef = r_turn[f'coef_{ed}']
        se = r_turn[f'se_{ed}']
        et = int(ed.replace('et_', '').replace('plus_', ''))
        print(f"    t={et:+d}: {fmt_coef(coef, se)} ({se:.4f})")
        es_turn_results.append({
            'event_time': et,
            'coef': coef,
            'se': se,
            'ci_lower': coef - 1.96 * se,
            'ci_upper': coef + 1.96 * se,
        })

    es_turn_df = pd.DataFrame(es_turn_results)
    es_turn_df.to_csv(os.path.join(OUTPUT_DIR, 'event_study_turnout.csv'), index=False)

###############################################################################
# PART 6: Robustness — exclude 2020 (COVID year)
###############################################################################
print("\n" + "=" * 70)
print("PART 6: ROBUSTNESS — EXCLUDE 2020")
print("=" * 70)

df_no2020 = df[df['year'] != 2020].copy()

# Stacked vote share without 2020
dv_no2020 = df_no2020[['state', 'county', 'county_id', 'year', 'year2',
                        'state_year_id', 'treat',
                        'dem_share_gov', 'dem_share_pres', 'dem_share_sen']].copy()
dl_no2020 = pd.melt(dv_no2020,
                    id_vars=['state', 'county', 'county_id', 'year', 'year2',
                             'state_year_id', 'treat'],
                    value_vars=['dem_share_gov', 'dem_share_pres', 'dem_share_sen'],
                    var_name='office', value_name='dem_share')
dl_no2020 = dl_no2020.dropna(subset=['dem_share']).reset_index(drop=True)
dl_no2020['syo'] = (dl_no2020['state'] + '_' +
                     dl_no2020['year'].astype(int).astype(str) + '_' +
                     dl_no2020['office'])
dl_no2020['state_year_id'] = pd.factorize(dl_no2020['syo'])[0] + 1

print("\nDem Vote Share (excl. 2020):")
for spec_name, lt, qt in [('basic', False, False),
                           ('linear', True, False),
                           ('quad', True, True)]:
    r = run_reghdfe(dl_no2020, 'dem_share', 'treat',
                    ['county_id', 'state_year_id'], 'county_id',
                    add_linear_trend=lt, add_quad_trend=qt)
    if r:
        print(f"  {spec_name}: coef={r['coef_treat']:.4f}, "
              f"SE={r['se_treat']:.4f}, N={r['n_obs']}")

print("\nTurnout (excl. 2020):")
for spec_name, lt, qt in [('basic', False, False),
                           ('linear', True, False),
                           ('quad', True, True)]:
    r = run_reghdfe(df_no2020, 'turnout_share', 'treat',
                    ['county_id', 'state_year_id'], 'county_id',
                    add_linear_trend=lt, add_quad_trend=qt)
    if r:
        print(f"  {spec_name}: coef={r['coef_treat']:.4f}, "
              f"SE={r['se_treat']:.4f}, N={r['n_obs']}")

###############################################################################
# Save summary tables
###############################################################################
print("\n" + "=" * 70)
print("SAVING RESULTS")
print("=" * 70)

# Compile all results into comprehensive tables
all_results = []

# Re-run everything systematically to compile
print("\nCompiling all results...")

# Full sample results
for outcome_name, data_obj, yvar in [
    ('Dem Vote Share (stacked)', df_long, 'dem_share'),
]:
    for spec_name, lt, qt in [('basic', False, False),
                               ('linear', True, False),
                               ('quad', True, True)]:
        r = run_reghdfe(data_obj, yvar, 'treat',
                        ['county_id', 'state_year_id'], 'county_id',
                        add_linear_trend=lt, add_quad_trend=qt)
        if r:
            all_results.append({
                'sample': 'Full (1996-2024)',
                'outcome': outcome_name,
                'spec': spec_name,
                'coef': r['coef_treat'],
                'se': r['se_treat'],
                'n_obs': r['n_obs'],
                'n_counties': r['n_counties'],
            })

for outcome_name, yvar in [('Turnout', 'turnout_share')]:
    for spec_name, lt, qt in [('basic', False, False),
                               ('linear', True, False),
                               ('quad', True, True)]:
        r = run_reghdfe(df, yvar, 'treat',
                        ['county_id', 'state_year_id'], 'county_id',
                        add_linear_trend=lt, add_quad_trend=qt)
        if r:
            all_results.append({
                'sample': 'Full (1996-2024)',
                'outcome': outcome_name,
                'spec': spec_name,
                'coef': r['coef_treat'],
                'se': r['se_treat'],
                'n_obs': r['n_obs'],
                'n_counties': r['n_counties'],
            })

results_df = pd.DataFrame(all_results)
results_df.to_csv(os.path.join(OUTPUT_DIR, 'extension_main_results.csv'), index=False)
print(f"Saved extension_main_results.csv")

print("\nDone.")
