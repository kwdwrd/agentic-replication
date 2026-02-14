"""
02_replicate.py
Replicate Tables 2 and 3 from Thompson et al. (2020)
Using manual fixed effects implementation for robustness
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

from linearmodels.panel import PanelOLS
import statsmodels.api as sm

# Set paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, 'original', 'data', 'modified')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output', 'tables')

os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_analysis_data():
    """Load the main analysis dataset"""
    path = os.path.join(DATA_DIR, 'analysis.dta')
    return pd.read_stata(path)


def create_state_year_var(df):
    """Create state_year string variable for fixed effects"""
    df = df.copy()
    df['state_year'] = df['state'] + '_' + df['year'].astype(str)
    return df


def absorb_fe_iterative(y, x, fe_groups, max_iter=1000, tol=1e-10):
    """
    Iteratively demean y and x by multiple FE groups.
    This implements the within transformation for multiple FE.
    """
    y_dm = y.copy().astype(float)
    x_dm = x.copy().astype(float)

    for iteration in range(max_iter):
        y_old = y_dm.copy()

        for fe in fe_groups:
            # Demean y by this FE group
            y_means = pd.Series(y_dm).groupby(fe).transform('mean')
            y_dm = y_dm - y_means.values

            # Demean x by this FE group
            x_means = pd.Series(x_dm).groupby(fe).transform('mean')
            x_dm = x_dm - x_means.values

        # Check convergence
        if np.max(np.abs(y_dm - y_old)) < tol:
            break

    return y_dm, x_dm


def clustered_se(X, residuals, clusters):
    """
    Compute cluster-robust standard errors.

    X: design matrix (n x k)
    residuals: OLS residuals (n,)
    clusters: cluster identifiers (n,)
    """
    n = len(residuals)
    k = X.shape[1]

    # Get unique clusters
    unique_clusters = np.unique(clusters)
    n_clusters = len(unique_clusters)

    # Compute bread: (X'X)^{-1}
    XtX = X.T @ X
    XtX_inv = np.linalg.inv(XtX)

    # Compute meat: sum over clusters of X_g' * e_g * e_g' * X_g
    meat = np.zeros((k, k))
    for c in unique_clusters:
        mask = clusters == c
        X_c = X[mask]
        e_c = residuals[mask]
        # Outer product of cluster's score
        score_c = X_c.T @ e_c
        meat += np.outer(score_c, score_c)

    # Small sample correction (Stata's default)
    # G/(G-1) * (N-1)/(N-K) where G = n_clusters, N = n, K = k
    correction = (n_clusters / (n_clusters - 1)) * ((n - 1) / (n - k))

    # Sandwich variance
    V = correction * XtX_inv @ meat @ XtX_inv

    return np.sqrt(np.diag(V))


def run_twfe_regression(df, y_var, treat_var, fe_vars, cluster_var,
                        county_var='county_id', year_var='year',
                        linear_trend=False, quad_trend=False):
    """
    Run two-way fixed effects regression with optional county trends.

    Parameters:
    -----------
    df : DataFrame
    y_var : str - outcome variable
    treat_var : str - treatment variable
    fe_vars : list - fixed effect variables
    cluster_var : str - clustering variable
    linear_trend : bool - include county-specific linear trends
    quad_trend : bool - include county-specific quadratic trends
    """

    # Prepare data
    keep_vars = [y_var, treat_var, cluster_var, county_var, year_var] + fe_vars
    keep_vars = list(set(keep_vars))  # Remove duplicates

    df_clean = df[keep_vars].dropna().copy()

    n_obs = len(df_clean)
    n_counties = df_clean[county_var].nunique()

    # Get cluster and FE group arrays
    clusters = df_clean[cluster_var].values

    # Create FE group arrays
    fe_group_arrays = [df_clean[fe].values for fe in fe_vars]

    # Handle county-specific trends
    if linear_trend or quad_trend:
        # Create county dummies interacted with year
        counties = df_clean[county_var].values
        years = df_clean[year_var].values

        # Normalize year for numerical stability
        year_mean = years.mean()
        year_normalized = (years - year_mean)

        if linear_trend:
            # Create county-specific linear trends
            # For each county, create interaction: county_dummy * year
            unique_counties = np.unique(counties)
            trend_cols = []
            for c in unique_counties:
                trend_col = (counties == c).astype(float) * year_normalized
                trend_cols.append(trend_col)
            linear_trends = np.column_stack(trend_cols)
            # Demean trends within existing FE structure
            # (simplified: just include as additional regressors after FE absorption)

        if quad_trend:
            year_sq = year_normalized ** 2
            quad_cols = []
            for c in unique_counties:
                quad_col = (counties == c).astype(float) * year_sq
                quad_cols.append(quad_col)
            quad_trends = np.column_stack(quad_cols)

    # Extract outcome and treatment
    y = df_clean[y_var].values.astype(float)
    x = df_clean[treat_var].values.astype(float)

    # Absorb fixed effects
    y_dm, x_dm = absorb_fe_iterative(y, x, fe_group_arrays)

    # If we have trends, we need to partial them out too
    if linear_trend:
        # Demean each trend column
        trends_dm = np.zeros_like(linear_trends)
        for i in range(linear_trends.shape[1]):
            _, trends_dm[:, i] = absorb_fe_iterative(np.zeros(n_obs), linear_trends[:, i], fe_group_arrays)

        # Partial out trends from y and x using FWL
        # Regress y_dm on trends_dm, get residuals
        trends_with_const = sm.add_constant(trends_dm)
        y_resid = sm.OLS(y_dm, trends_with_const).fit().resid
        x_resid = sm.OLS(x_dm, trends_with_const).fit().resid

        y_dm = y_resid
        x_dm = x_resid

    if quad_trend:
        # Demean each quad trend column
        qtrends_dm = np.zeros_like(quad_trends)
        for i in range(quad_trends.shape[1]):
            _, qtrends_dm[:, i] = absorb_fe_iterative(np.zeros(n_obs), quad_trends[:, i], fe_group_arrays)

        # Partial out from y_dm and x_dm
        qtrends_with_const = sm.add_constant(qtrends_dm)
        y_dm = sm.OLS(y_dm, qtrends_with_const).fit().resid
        x_dm = sm.OLS(x_dm, qtrends_with_const).fit().resid

    # OLS on demeaned data
    X = x_dm.reshape(-1, 1)
    X_with_const = sm.add_constant(X)

    model = sm.OLS(y_dm, X_with_const).fit()

    beta = model.params[1]
    residuals = model.resid

    # Clustered standard errors
    se = clustered_se(X_with_const, residuals, clusters)[1]

    # Count state-years for reporting
    n_elections = df_clean['state_year'].nunique() if 'state_year' in df_clean.columns else len(fe_vars)

    return {
        'beta': beta,
        'se': se,
        'n_obs': n_obs,
        'n_counties': n_counties,
        'n_elections': n_elections
    }


def replicate_table2(df):
    """
    Replicate Table 2: Partisan Outcomes
    """

    results = {}

    print("\n" + "="*70)
    print("REPLICATING TABLE 2: PARTISAN OUTCOMES")
    print("="*70)

    # Prepare data
    df = create_state_year_var(df)

    # --- Columns 1-3: Democratic Turnout Share ---
    df_turnout = df[df['share_votes_dem'].notna()].copy()
    print(f"\nDem Turnout Share sample: {len(df_turnout)} obs, {df_turnout['county_id'].nunique()} counties")

    # Column 1: Basic
    print("\nColumn 1: Basic (county FE + state-year FE)")
    res = run_twfe_regression(df_turnout, 'share_votes_dem', 'treat',
                              ['county_id', 'state_year'], 'county_id')
    results['dem_turnout_basic'] = res
    print(f"  Beta: {res['beta']:.4f}, SE: {res['se']:.4f}, N: {res['n_obs']}")

    # Column 2: Linear trends
    print("\nColumn 2: With linear county trends")
    res = run_twfe_regression(df_turnout, 'share_votes_dem', 'treat',
                              ['county_id', 'state_year'], 'county_id',
                              linear_trend=True)
    results['dem_turnout_linear'] = res
    print(f"  Beta: {res['beta']:.4f}, SE: {res['se']:.4f}, N: {res['n_obs']}")

    # Column 3: Quadratic trends
    print("\nColumn 3: With quadratic county trends")
    res = run_twfe_regression(df_turnout, 'share_votes_dem', 'treat',
                              ['county_id', 'state_year'], 'county_id',
                              linear_trend=True, quad_trend=True)
    results['dem_turnout_quad'] = res
    print(f"  Beta: {res['beta']:.4f}, SE: {res['se']:.4f}, N: {res['n_obs']}")

    # --- Columns 4-6: Democratic Vote Share (reshaped) ---
    print("\n" + "-"*50)
    print("Preparing Dem Vote Share data (reshape long)...")

    # Reshape dem_share_gov, dem_share_pres, dem_share_sen to long format
    df_vote = df[['state', 'county', 'county_id', 'year', 'state_year', 'treat',
                  'dem_share_gov', 'dem_share_pres', 'dem_share_sen']].copy()

    df_vote_long = pd.melt(df_vote,
                           id_vars=['state', 'county', 'county_id', 'year', 'state_year', 'treat'],
                           value_vars=['dem_share_gov', 'dem_share_pres', 'dem_share_sen'],
                           var_name='office', value_name='dem_share')

    df_vote_long = df_vote_long[df_vote_long['dem_share'].notna()].copy()
    print(f"Dem Vote Share sample: {len(df_vote_long)} obs, {df_vote_long['county_id'].nunique()} counties")

    # Column 4: Basic
    print("\nColumn 4: Basic (county FE + state-year FE)")
    res = run_twfe_regression(df_vote_long, 'dem_share', 'treat',
                              ['county_id', 'state_year'], 'county_id')
    results['dem_vote_basic'] = res
    print(f"  Beta: {res['beta']:.4f}, SE: {res['se']:.4f}, N: {res['n_obs']}")

    # Column 5: Linear trends
    print("\nColumn 5: With linear county trends")
    res = run_twfe_regression(df_vote_long, 'dem_share', 'treat',
                              ['county_id', 'state_year'], 'county_id',
                              linear_trend=True)
    results['dem_vote_linear'] = res
    print(f"  Beta: {res['beta']:.4f}, SE: {res['se']:.4f}, N: {res['n_obs']}")

    # Column 6: Quadratic trends
    print("\nColumn 6: With quadratic county trends")
    res = run_twfe_regression(df_vote_long, 'dem_share', 'treat',
                              ['county_id', 'state_year'], 'county_id',
                              linear_trend=True, quad_trend=True)
    results['dem_vote_quad'] = res
    print(f"  Beta: {res['beta']:.4f}, SE: {res['se']:.4f}, N: {res['n_obs']}")

    return results


def replicate_table3(df):
    """
    Replicate Table 3: Participation Outcomes
    """

    results = {}

    print("\n" + "="*70)
    print("REPLICATING TABLE 3: PARTICIPATION OUTCOMES")
    print("="*70)

    df = create_state_year_var(df)

    # --- Columns 1-3: Turnout ---
    df_turnout = df[df['turnout_share'].notna()].copy()
    print(f"\nTurnout sample: {len(df_turnout)} obs, {df_turnout['county_id'].nunique()} counties")

    # Column 1: Basic
    print("\nColumn 1: Basic (county FE + state-year FE)")
    res = run_twfe_regression(df_turnout, 'turnout_share', 'treat',
                              ['county_id', 'state_year'], 'county_id')
    results['turnout_basic'] = res
    print(f"  Beta: {res['beta']:.4f}, SE: {res['se']:.4f}, N: {res['n_obs']}")

    # Column 2: Linear trends
    print("\nColumn 2: With linear county trends")
    res = run_twfe_regression(df_turnout, 'turnout_share', 'treat',
                              ['county_id', 'state_year'], 'county_id',
                              linear_trend=True)
    results['turnout_linear'] = res
    print(f"  Beta: {res['beta']:.4f}, SE: {res['se']:.4f}, N: {res['n_obs']}")

    # Column 3: Quadratic trends
    print("\nColumn 3: With quadratic county trends")
    res = run_twfe_regression(df_turnout, 'turnout_share', 'treat',
                              ['county_id', 'state_year'], 'county_id',
                              linear_trend=True, quad_trend=True)
    results['turnout_quad'] = res
    print(f"  Beta: {res['beta']:.4f}, SE: {res['se']:.4f}, N: {res['n_obs']}")

    # --- Columns 4-6: VBM Share (CA only) ---
    print("\n" + "-"*50)
    df_vbm = df[(df['state'] == 'CA') & (df['vbm_share'].notna())].copy()
    print(f"VBM Share sample (CA only): {len(df_vbm)} obs, {df_vbm['county_id'].nunique()} counties")

    # Column 4: Basic
    print("\nColumn 4: Basic (county FE + state-year FE)")
    res = run_twfe_regression(df_vbm, 'vbm_share', 'treat',
                              ['county_id', 'state_year'], 'county_id')
    results['vbm_basic'] = res
    print(f"  Beta: {res['beta']:.4f}, SE: {res['se']:.4f}, N: {res['n_obs']}")

    # Column 5: Linear trends
    print("\nColumn 5: With linear county trends")
    res = run_twfe_regression(df_vbm, 'vbm_share', 'treat',
                              ['county_id', 'state_year'], 'county_id',
                              linear_trend=True)
    results['vbm_linear'] = res
    print(f"  Beta: {res['beta']:.4f}, SE: {res['se']:.4f}, N: {res['n_obs']}")

    # Column 6: Quadratic trends
    print("\nColumn 6: With quadratic county trends")
    res = run_twfe_regression(df_vbm, 'vbm_share', 'treat',
                              ['county_id', 'state_year'], 'county_id',
                              linear_trend=True, quad_trend=True)
    results['vbm_quad'] = res
    print(f"  Beta: {res['beta']:.4f}, SE: {res['se']:.4f}, N: {res['n_obs']}")

    return results


def create_comparison_table(results_t2, results_t3):
    """Create comparison table with original and replicated results"""

    # Original Table 2 results from paper
    original_t2 = {
        'dem_turnout_basic': {'beta': 0.007, 'se': 0.003},
        'dem_turnout_linear': {'beta': 0.001, 'se': 0.001},
        'dem_turnout_quad': {'beta': 0.001, 'se': 0.001},
        'dem_vote_basic': {'beta': 0.028, 'se': 0.011},
        'dem_vote_linear': {'beta': 0.011, 'se': 0.004},
        'dem_vote_quad': {'beta': 0.007, 'se': 0.003},
    }

    # Original Table 3 results from paper
    original_t3 = {
        'turnout_basic': {'beta': 0.021, 'se': 0.009},
        'turnout_linear': {'beta': 0.022, 'se': 0.007},
        'turnout_quad': {'beta': 0.021, 'se': 0.008},
        'vbm_basic': {'beta': 0.186, 'se': 0.027},
        'vbm_linear': {'beta': 0.157, 'se': 0.035},
        'vbm_quad': {'beta': 0.136, 'se': 0.085},
    }

    print("\n" + "="*70)
    print("COMPARISON: ORIGINAL vs REPLICATED")
    print("="*70)

    print("\n" + "-"*70)
    print("TABLE 2: PARTISAN OUTCOMES")
    print("-"*70)
    print(f"{'Outcome':<20} {'Spec':<10} {'Original':>15} {'Replicated':>15} {'Diff':>10}")
    print("-"*70)

    for key in ['dem_turnout_basic', 'dem_turnout_linear', 'dem_turnout_quad',
                'dem_vote_basic', 'dem_vote_linear', 'dem_vote_quad']:
        outcome = 'Dem Turnout' if 'turnout' in key else 'Dem Vote'
        spec = key.rsplit('_', 1)[1].title()

        orig = original_t2[key]['beta']
        orig_se = original_t2[key]['se']
        repl = results_t2[key]['beta']
        repl_se = results_t2[key]['se']
        diff = repl - orig

        print(f"{outcome:<20} {spec:<10} {orig:>6.3f} ({orig_se:.3f}) {repl:>6.3f} ({repl_se:.3f}) {diff:>+8.4f}")

    print("\n" + "-"*70)
    print("TABLE 3: PARTICIPATION OUTCOMES")
    print("-"*70)
    print(f"{'Outcome':<20} {'Spec':<10} {'Original':>15} {'Replicated':>15} {'Diff':>10}")
    print("-"*70)

    for key in ['turnout_basic', 'turnout_linear', 'turnout_quad',
                'vbm_basic', 'vbm_linear', 'vbm_quad']:
        outcome = 'Turnout' if 'turnout' in key else 'VBM Share'
        spec = key.rsplit('_', 1)[1].title()

        orig = original_t3[key]['beta']
        orig_se = original_t3[key]['se']
        repl = results_t3[key]['beta']
        repl_se = results_t3[key]['se']
        diff = repl - orig

        print(f"{outcome:<20} {spec:<10} {orig:>6.3f} ({orig_se:.3f}) {repl:>6.3f} ({repl_se:.3f}) {diff:>+8.4f}")

    return original_t2, original_t3


def save_results(results_t2, results_t3, original_t2, original_t3):
    """Save results to CSV files"""

    # Table 2
    rows = []
    for key in ['dem_turnout_basic', 'dem_turnout_linear', 'dem_turnout_quad',
                'dem_vote_basic', 'dem_vote_linear', 'dem_vote_quad']:
        rows.append({
            'outcome': key.rsplit('_', 1)[0],
            'specification': key.rsplit('_', 1)[1],
            'original_beta': original_t2[key]['beta'],
            'original_se': original_t2[key]['se'],
            'replicated_beta': results_t2[key]['beta'],
            'replicated_se': results_t2[key]['se'],
            'n_obs': results_t2[key]['n_obs'],
            'n_counties': results_t2[key]['n_counties']
        })

    df_t2 = pd.DataFrame(rows)
    df_t2['difference'] = df_t2['replicated_beta'] - df_t2['original_beta']
    df_t2['pct_diff'] = (df_t2['difference'] / df_t2['original_beta'] * 100).round(1)
    df_t2.to_csv(os.path.join(OUTPUT_DIR, 'table2_replication.csv'), index=False)

    # Table 3
    rows = []
    for key in ['turnout_basic', 'turnout_linear', 'turnout_quad',
                'vbm_basic', 'vbm_linear', 'vbm_quad']:
        rows.append({
            'outcome': key.rsplit('_', 1)[0],
            'specification': key.rsplit('_', 1)[1],
            'original_beta': original_t3[key]['beta'],
            'original_se': original_t3[key]['se'],
            'replicated_beta': results_t3[key]['beta'],
            'replicated_se': results_t3[key]['se'],
            'n_obs': results_t3[key]['n_obs'],
            'n_counties': results_t3[key]['n_counties']
        })

    df_t3 = pd.DataFrame(rows)
    df_t3['difference'] = df_t3['replicated_beta'] - df_t3['original_beta']
    df_t3['pct_diff'] = (df_t3['difference'] / df_t3['original_beta'] * 100).round(1)
    df_t3.to_csv(os.path.join(OUTPUT_DIR, 'table3_replication.csv'), index=False)

    print(f"\nResults saved to:")
    print(f"  {os.path.join(OUTPUT_DIR, 'table2_replication.csv')}")
    print(f"  {os.path.join(OUTPUT_DIR, 'table3_replication.csv')}")


if __name__ == "__main__":
    print("Loading data...")
    df = load_analysis_data()

    # Replicate Table 2
    results_t2 = replicate_table2(df)

    # Replicate Table 3
    results_t3 = replicate_table3(df)

    # Compare to original
    original_t2, original_t3 = create_comparison_table(results_t2, results_t3)

    # Save results
    save_results(results_t2, results_t3, original_t2, original_t3)
