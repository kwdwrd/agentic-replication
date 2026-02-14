"""
05_extension_analysis.py
Extension analysis: Run original specifications on extended data (1996-2024)

This script:
1. Runs main results with extended data (Task 5.1)
2. Tests for heterogeneous effects by period (Task 5.2)
3. Runs separate estimates by period (Task 5.3)
4. California-specific analysis (Task 5.4)
5. Event study specification (Task 5.5)
6. Robustness checks (Task 5.6)
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

import statsmodels.api as sm

# Set paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGINAL_DATA_DIR = os.path.join(PROJECT_ROOT, 'original', 'data', 'modified')
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output', 'tables')

os.makedirs(OUTPUT_DIR, exist_ok=True)


# =============================================================================
# Core regression functions (from 02_replicate.py)
# =============================================================================

def absorb_fe_iterative(y, x, fe_groups, max_iter=1000, tol=1e-10):
    """Iteratively demean y and x by multiple FE groups."""
    y_dm = y.copy().astype(float)
    x_dm = x.copy().astype(float)

    for iteration in range(max_iter):
        y_old = y_dm.copy()

        for fe in fe_groups:
            y_means = pd.Series(y_dm).groupby(fe).transform('mean')
            y_dm = y_dm - y_means.values
            x_means = pd.Series(x_dm).groupby(fe).transform('mean')
            x_dm = x_dm - x_means.values

        if np.max(np.abs(y_dm - y_old)) < tol:
            break

    return y_dm, x_dm


def absorb_fe_matrix(X, fe_groups, max_iter=1000, tol=1e-10):
    """Absorb FE from a matrix of covariates."""
    X_dm = X.copy().astype(float)

    for iteration in range(max_iter):
        X_old = X_dm.copy()

        for fe in fe_groups:
            for col in range(X_dm.shape[1]):
                col_means = pd.Series(X_dm[:, col]).groupby(fe).transform('mean')
                X_dm[:, col] = X_dm[:, col] - col_means.values

        if np.max(np.abs(X_dm - X_old)) < tol:
            break

    return X_dm


def clustered_se(X, residuals, clusters):
    """Compute cluster-robust standard errors."""
    n = len(residuals)
    k = X.shape[1]

    unique_clusters = np.unique(clusters)
    n_clusters = len(unique_clusters)

    XtX = X.T @ X
    XtX_inv = np.linalg.inv(XtX)

    meat = np.zeros((k, k))
    for c in unique_clusters:
        mask = clusters == c
        X_c = X[mask]
        e_c = residuals[mask]
        score_c = X_c.T @ e_c
        meat += np.outer(score_c, score_c)

    correction = (n_clusters / (n_clusters - 1)) * ((n - 1) / (n - k))
    V = correction * XtX_inv @ meat @ XtX_inv

    return np.sqrt(np.diag(V))


def run_twfe_regression(df, y_var, treat_var, fe_vars, cluster_var,
                        county_var='county_id', year_var='year',
                        linear_trend=False, quad_trend=False,
                        additional_covariates=None):
    """
    Run two-way fixed effects regression with optional county trends.
    """
    keep_vars = [y_var, treat_var, cluster_var, county_var, year_var] + fe_vars
    if additional_covariates:
        keep_vars += additional_covariates
    keep_vars = list(set(keep_vars))

    df_clean = df[keep_vars].dropna().copy()

    n_obs = len(df_clean)
    n_counties = df_clean[county_var].nunique()

    clusters = df_clean[cluster_var].values
    fe_group_arrays = [df_clean[fe].values for fe in fe_vars]

    if linear_trend or quad_trend:
        counties = df_clean[county_var].values
        years = df_clean[year_var].values
        year_mean = years.mean()
        year_normalized = (years - year_mean)

        if linear_trend:
            unique_counties = np.unique(counties)
            trend_cols = []
            for c in unique_counties:
                trend_col = (counties == c).astype(float) * year_normalized
                trend_cols.append(trend_col)
            linear_trends = np.column_stack(trend_cols)

        if quad_trend:
            year_sq = year_normalized ** 2
            quad_cols = []
            for c in unique_counties:
                quad_col = (counties == c).astype(float) * year_sq
                quad_cols.append(quad_col)
            quad_trends = np.column_stack(quad_cols)

    y = df_clean[y_var].values.astype(float)
    x = df_clean[treat_var].values.astype(float)

    y_dm, x_dm = absorb_fe_iterative(y, x, fe_group_arrays)

    # Handle additional covariates
    if additional_covariates:
        X_cov = df_clean[additional_covariates].values
        X_cov_dm = absorb_fe_matrix(X_cov, fe_group_arrays)

        # Partial out additional covariates
        X_cov_with_const = sm.add_constant(X_cov_dm)
        y_dm = sm.OLS(y_dm, X_cov_with_const).fit().resid
        x_dm = sm.OLS(x_dm, X_cov_with_const).fit().resid

    if linear_trend:
        trends_dm = np.zeros_like(linear_trends)
        for i in range(linear_trends.shape[1]):
            _, trends_dm[:, i] = absorb_fe_iterative(np.zeros(n_obs), linear_trends[:, i], fe_group_arrays)
        trends_with_const = sm.add_constant(trends_dm)
        y_dm = sm.OLS(y_dm, trends_with_const).fit().resid
        x_dm = sm.OLS(x_dm, trends_with_const).fit().resid

    if quad_trend:
        qtrends_dm = np.zeros_like(quad_trends)
        for i in range(quad_trends.shape[1]):
            _, qtrends_dm[:, i] = absorb_fe_iterative(np.zeros(n_obs), quad_trends[:, i], fe_group_arrays)
        qtrends_with_const = sm.add_constant(qtrends_dm)
        y_dm = sm.OLS(y_dm, qtrends_with_const).fit().resid
        x_dm = sm.OLS(x_dm, qtrends_with_const).fit().resid

    X = x_dm.reshape(-1, 1)
    X_with_const = sm.add_constant(X)

    model = sm.OLS(y_dm, X_with_const).fit()
    beta = model.params[1]
    residuals = model.resid
    se = clustered_se(X_with_const, residuals, clusters)[1]

    n_elections = df_clean['state_year'].nunique() if 'state_year' in df_clean.columns else np.nan

    return {
        'beta': beta,
        'se': se,
        'n_obs': n_obs,
        'n_counties': n_counties,
        'n_elections': n_elections
    }


def run_twfe_multiple_treatments(df, y_var, treat_vars, fe_vars, cluster_var,
                                  county_var='county_id', year_var='year',
                                  linear_trend=False, quad_trend=False):
    """
    Run TWFE with multiple treatment variables (for interaction models).
    """
    keep_vars = [y_var, cluster_var, county_var, year_var] + treat_vars + fe_vars
    keep_vars = list(set(keep_vars))

    df_clean = df[keep_vars].dropna().copy()
    n_obs = len(df_clean)
    n_counties = df_clean[county_var].nunique()

    clusters = df_clean[cluster_var].values
    fe_group_arrays = [df_clean[fe].values for fe in fe_vars]

    if linear_trend or quad_trend:
        counties = df_clean[county_var].values
        years = df_clean[year_var].values
        year_mean = years.mean()
        year_normalized = (years - year_mean)

        if linear_trend:
            unique_counties = np.unique(counties)
            trend_cols = []
            for c in unique_counties:
                trend_col = (counties == c).astype(float) * year_normalized
                trend_cols.append(trend_col)
            linear_trends = np.column_stack(trend_cols)

        if quad_trend:
            year_sq = year_normalized ** 2
            quad_cols = []
            for c in unique_counties:
                quad_col = (counties == c).astype(float) * year_sq
                quad_cols.append(quad_col)
            quad_trends = np.column_stack(quad_cols)

    # Extract outcome and treatments
    y = df_clean[y_var].values.astype(float)
    X_treat = df_clean[treat_vars].values.astype(float)

    # Absorb FE from y
    y_dm = y.copy()
    for iteration in range(1000):
        y_old = y_dm.copy()
        for fe in fe_group_arrays:
            y_means = pd.Series(y_dm).groupby(fe).transform('mean')
            y_dm = y_dm - y_means.values
        if np.max(np.abs(y_dm - y_old)) < 1e-10:
            break

    # Absorb FE from each treatment variable
    X_treat_dm = absorb_fe_matrix(X_treat, fe_group_arrays)

    # Partial out trends if needed
    if linear_trend:
        trends_dm = np.zeros_like(linear_trends)
        for i in range(linear_trends.shape[1]):
            _, trends_dm[:, i] = absorb_fe_iterative(np.zeros(n_obs), linear_trends[:, i], fe_group_arrays)
        trends_with_const = sm.add_constant(trends_dm)
        y_dm = sm.OLS(y_dm, trends_with_const).fit().resid
        for j in range(X_treat_dm.shape[1]):
            X_treat_dm[:, j] = sm.OLS(X_treat_dm[:, j], trends_with_const).fit().resid

    if quad_trend:
        qtrends_dm = np.zeros_like(quad_trends)
        for i in range(quad_trends.shape[1]):
            _, qtrends_dm[:, i] = absorb_fe_iterative(np.zeros(n_obs), quad_trends[:, i], fe_group_arrays)
        qtrends_with_const = sm.add_constant(qtrends_dm)
        y_dm = sm.OLS(y_dm, qtrends_with_const).fit().resid
        for j in range(X_treat_dm.shape[1]):
            X_treat_dm[:, j] = sm.OLS(X_treat_dm[:, j], qtrends_with_const).fit().resid

    # OLS regression
    X_with_const = sm.add_constant(X_treat_dm)
    model = sm.OLS(y_dm, X_with_const).fit()

    betas = model.params[1:]  # exclude constant
    residuals = model.resid
    ses = clustered_se(X_with_const, residuals, clusters)[1:]

    results = {}
    for i, var in enumerate(treat_vars):
        results[var] = {'beta': betas[i], 'se': ses[i]}
    results['n_obs'] = n_obs
    results['n_counties'] = n_counties

    return results


# =============================================================================
# Data loading and preparation
# =============================================================================

def load_extended_data():
    """Load the combined extended dataset."""
    path = os.path.join(PROCESSED_DATA_DIR, 'full_analysis_data.csv')
    df = pd.read_csv(path)

    # Create state_year if not exists
    if 'state_year' not in df.columns:
        df['state_year'] = df['state'] + '_' + df['year'].astype(str)

    # Ensure county_id is integer
    df['county_id'] = df['county_id'].fillna(-1).astype(int)

    print(f"Loaded extended data: {len(df)} observations")
    print(f"  Original period: {(df['period'] == 'original').sum()}")
    print(f"  Extension period: {(df['period'] == 'extension').sum()}")
    print(f"  Years: {df['year'].min()} - {df['year'].max()}")

    return df


def load_original_data():
    """Load original analysis data for comparison."""
    path = os.path.join(ORIGINAL_DATA_DIR, 'analysis.dta')
    df = pd.read_stata(path)
    df['state_year'] = df['state'] + '_' + df['year'].astype(str)
    return df


# =============================================================================
# Task 5.1: Main results with extended data
# =============================================================================

def run_extended_main_results(df):
    """
    Re-estimate Tables 2 and 3 using full 1996-2024 sample.
    """
    print("\n" + "="*70)
    print("TASK 5.1: MAIN RESULTS WITH EXTENDED DATA (1996-2024)")
    print("="*70)

    results = {'table2': {}, 'table3': {}}

    # ----- Table 2 style: Partisan outcomes -----
    print("\n--- Table 2 Style: Partisan Outcomes ---")

    # Democratic vote share (using dem_share column)
    df_vote = df[df['dem_share'].notna()].copy()
    print(f"\nDem Vote Share sample: {len(df_vote)} obs, {df_vote['county_id'].nunique()} counties")

    for spec, linear, quad in [('basic', False, False), ('linear', True, False), ('quad', True, True)]:
        res = run_twfe_regression(df_vote, 'dem_share', 'treat',
                                  ['county_id', 'state_year'], 'county_id',
                                  linear_trend=linear, quad_trend=quad)
        results['table2'][f'dem_share_{spec}'] = res
        print(f"  {spec}: beta={res['beta']:.4f}, se={res['se']:.4f}, N={res['n_obs']}")

    # ----- Table 3 style: Participation outcomes -----
    print("\n--- Table 3 Style: Participation Outcomes ---")

    # Turnout (using turnout_share)
    df_turnout = df[df['turnout_share'].notna()].copy()
    print(f"\nTurnout sample: {len(df_turnout)} obs, {df_turnout['county_id'].nunique()} counties")

    for spec, linear, quad in [('basic', False, False), ('linear', True, False), ('quad', True, True)]:
        res = run_twfe_regression(df_turnout, 'turnout_share', 'treat',
                                  ['county_id', 'state_year'], 'county_id',
                                  linear_trend=linear, quad_trend=quad)
        results['table3'][f'turnout_{spec}'] = res
        print(f"  {spec}: beta={res['beta']:.4f}, se={res['se']:.4f}, N={res['n_obs']}")

    return results


# =============================================================================
# Task 5.2: Heterogeneous effects by period
# =============================================================================

def test_heterogeneous_effects(df):
    """
    Test whether VBM effects differ between original and extension periods.
    Interact VBM treatment with post_2018 indicator.
    """
    print("\n" + "="*70)
    print("TASK 5.2: HETEROGENEOUS EFFECTS BY PERIOD")
    print("="*70)

    results = {}

    # Create interaction term: treat × post_2018
    df = df.copy()
    df['treat_x_post2018'] = df['treat'] * df['post_2018']

    # ----- Democratic vote share -----
    print("\n--- Democratic Vote Share ---")
    df_vote = df[df['dem_share'].notna()].copy()

    for spec, linear, quad in [('basic', False, False), ('linear', True, False), ('quad', True, True)]:
        res = run_twfe_multiple_treatments(
            df_vote, 'dem_share', ['treat', 'treat_x_post2018'],
            ['county_id', 'state_year'], 'county_id',
            linear_trend=linear, quad_trend=quad
        )
        results[f'dem_share_{spec}'] = res
        print(f"  {spec}:")
        print(f"    VBM (main):       beta={res['treat']['beta']:.4f}, se={res['treat']['se']:.4f}")
        print(f"    VBM × Post2018:   beta={res['treat_x_post2018']['beta']:.4f}, se={res['treat_x_post2018']['se']:.4f}")

    # ----- Turnout -----
    print("\n--- Turnout ---")
    df_turnout = df[df['turnout_share'].notna()].copy()

    for spec, linear, quad in [('basic', False, False), ('linear', True, False), ('quad', True, True)]:
        res = run_twfe_multiple_treatments(
            df_turnout, 'turnout_share', ['treat', 'treat_x_post2018'],
            ['county_id', 'state_year'], 'county_id',
            linear_trend=linear, quad_trend=quad
        )
        results[f'turnout_{spec}'] = res
        print(f"  {spec}:")
        print(f"    VBM (main):       beta={res['treat']['beta']:.4f}, se={res['treat']['se']:.4f}")
        print(f"    VBM × Post2018:   beta={res['treat_x_post2018']['beta']:.4f}, se={res['treat_x_post2018']['se']:.4f}")

    return results


# =============================================================================
# Task 5.3: Separate estimates by period
# =============================================================================

def run_separate_period_estimates(df):
    """
    Run separate estimates for original period (1996-2018) and extension (2020-2024).
    """
    print("\n" + "="*70)
    print("TASK 5.3: SEPARATE ESTIMATES BY PERIOD")
    print("="*70)

    results = {'original': {}, 'extension': {}}

    for period in ['original', 'extension']:
        print(f"\n--- {period.upper()} PERIOD ---")
        df_period = df[df['period'] == period].copy()

        # Democratic vote share
        df_vote = df_period[df_period['dem_share'].notna()].copy()
        if len(df_vote) > 0:
            print(f"\nDem Vote Share: {len(df_vote)} obs")
            for spec, linear, quad in [('basic', False, False), ('linear', True, False), ('quad', True, True)]:
                try:
                    res = run_twfe_regression(df_vote, 'dem_share', 'treat',
                                              ['county_id', 'state_year'], 'county_id',
                                              linear_trend=linear, quad_trend=quad)
                    results[period][f'dem_share_{spec}'] = res
                    print(f"  {spec}: beta={res['beta']:.4f}, se={res['se']:.4f}")
                except Exception as e:
                    print(f"  {spec}: Error - {str(e)[:50]}")
                    results[period][f'dem_share_{spec}'] = {'beta': np.nan, 'se': np.nan, 'n_obs': 0}

        # Turnout
        df_turnout = df_period[df_period['turnout_share'].notna()].copy()
        if len(df_turnout) > 0:
            print(f"\nTurnout: {len(df_turnout)} obs")
            for spec, linear, quad in [('basic', False, False), ('linear', True, False), ('quad', True, True)]:
                try:
                    res = run_twfe_regression(df_turnout, 'turnout_share', 'treat',
                                              ['county_id', 'state_year'], 'county_id',
                                              linear_trend=linear, quad_trend=quad)
                    results[period][f'turnout_{spec}'] = res
                    print(f"  {spec}: beta={res['beta']:.4f}, se={res['se']:.4f}")
                except Exception as e:
                    print(f"  {spec}: Error - {str(e)[:50]}")
                    results[period][f'turnout_{spec}'] = {'beta': np.nan, 'se': np.nan, 'n_obs': 0}

    return results


# =============================================================================
# Task 5.4: California-specific analysis
# =============================================================================

def run_california_analysis(df):
    """
    California-specific analysis - primary source of new treatment variation.
    """
    print("\n" + "="*70)
    print("TASK 5.4: CALIFORNIA-SPECIFIC ANALYSIS")
    print("="*70)

    results = {}

    # California only
    df_ca = df[df['state'] == 'CA'].copy()
    print(f"\nCalifornia sample: {len(df_ca)} observations")
    print(f"  Original period: {(df_ca['period'] == 'original').sum()}")
    print(f"  Extension period: {(df_ca['period'] == 'extension').sum()}")
    print(f"  Treated: {df_ca['treat'].sum()}")

    # Democratic vote share
    print("\n--- Democratic Vote Share (CA only) ---")
    df_vote = df_ca[df_ca['dem_share'].notna()].copy()

    for spec, linear, quad in [('basic', False, False), ('linear', True, False), ('quad', True, True)]:
        try:
            res = run_twfe_regression(df_vote, 'dem_share', 'treat',
                                      ['county_id', 'state_year'], 'county_id',
                                      linear_trend=linear, quad_trend=quad)
            results[f'ca_dem_share_{spec}'] = res
            print(f"  {spec}: beta={res['beta']:.4f}, se={res['se']:.4f}, N={res['n_obs']}")
        except Exception as e:
            print(f"  {spec}: Error - {str(e)[:50]}")
            results[f'ca_dem_share_{spec}'] = {'beta': np.nan, 'se': np.nan, 'n_obs': 0}

    # Turnout
    print("\n--- Turnout (CA only) ---")
    df_turnout = df_ca[df_ca['turnout_share'].notna()].copy()

    for spec, linear, quad in [('basic', False, False), ('linear', True, False), ('quad', True, True)]:
        try:
            res = run_twfe_regression(df_turnout, 'turnout_share', 'treat',
                                      ['county_id', 'state_year'], 'county_id',
                                      linear_trend=linear, quad_trend=quad)
            results[f'ca_turnout_{spec}'] = res
            print(f"  {spec}: beta={res['beta']:.4f}, se={res['se']:.4f}, N={res['n_obs']}")
        except Exception as e:
            print(f"  {spec}: Error - {str(e)[:50]}")
            results[f'ca_turnout_{spec}'] = {'beta': np.nan, 'se': np.nan, 'n_obs': 0}

    return results


# =============================================================================
# Task 5.5: Event study
# =============================================================================

def run_event_study(df):
    """
    Event study specification - estimate effects by years since treatment.
    """
    print("\n" + "="*70)
    print("TASK 5.5: EVENT STUDY SPECIFICATION")
    print("="*70)

    # Need to load VBM adoption timing for event study
    # For California, use VCA adoption years
    # For simplicity, create event time relative to treatment

    # Load California VCA adoption data
    ca_vca_path = os.path.join(PROJECT_ROOT, 'data', 'extension', 'california_vca_adoption.csv')
    if os.path.exists(ca_vca_path):
        ca_vca = pd.read_csv(ca_vca_path)
    else:
        print("VCA adoption data not found. Skipping event study.")
        return {}

    # Focus on California which has variation
    df_ca = df[df['state'] == 'CA'].copy()

    # Merge VCA adoption year
    df_ca = df_ca.merge(ca_vca[['county', 'vca_first_year']], on='county', how='left')

    # Create event time (years since VCA adoption)
    df_ca['event_time'] = df_ca['year'] - df_ca['vca_first_year']

    # For non-adopters, event_time is undefined
    df_ca.loc[df_ca['vca_first_year'].isna(), 'event_time'] = np.nan

    # Bin event time: -3 or earlier, -2, -1, 0, 1, 2, 3+
    # Convert to string to avoid categorical issues
    event_binned = pd.cut(
        df_ca['event_time'],
        bins=[-np.inf, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, np.inf],
        labels=['pre_3plus', 'pre_2', 'pre_1', 't0', 'post_1', 'post_2', 'post_3plus']
    ).astype(str)
    df_ca['event_time_binned'] = event_binned

    # Never-treated counties get a special category
    df_ca.loc[df_ca['vca_first_year'].isna(), 'event_time_binned'] = 'never_treated'

    print(f"\nEvent time distribution:")
    print(df_ca['event_time_binned'].value_counts())

    results = {'event_study': {}}

    # Create event time dummies (omit pre_1 as reference)
    df_es = df_ca[df_ca['dem_share'].notna()].copy()

    event_times = ['pre_3plus', 'pre_2', 't0', 'post_1', 'post_2', 'post_3plus']
    for et in event_times:
        df_es[f'event_{et}'] = (df_es['event_time_binned'] == et).astype(int)

    print(f"\nEvent study sample: {len(df_es)} obs")

    # Run event study regression (basic specification)
    treat_vars = [f'event_{et}' for et in event_times]

    try:
        res = run_twfe_multiple_treatments(
            df_es, 'dem_share', treat_vars,
            ['county_id', 'state_year'], 'county_id',
            linear_trend=False, quad_trend=False
        )

        print("\n--- Event Study: Democratic Vote Share ---")
        print("(Reference: t-1)")
        for et in event_times:
            var = f'event_{et}'
            print(f"  {et}: beta={res[var]['beta']:.4f}, se={res[var]['se']:.4f}")
            results['event_study'][et] = res[var]
        results['event_study']['n_obs'] = res['n_obs']
        results['event_study']['n_counties'] = res['n_counties']

    except Exception as e:
        print(f"Event study error: {str(e)}")

    return results


# =============================================================================
# Task 5.6: Robustness checks
# =============================================================================

def run_robustness_checks(df):
    """
    Robustness checks: drop 2020, alternative specifications.
    """
    print("\n" + "="*70)
    print("TASK 5.6: ROBUSTNESS CHECKS")
    print("="*70)

    results = {}

    # ----- Drop 2020 (COVID election) -----
    print("\n--- Robustness: Drop 2020 ---")
    df_no2020 = df[df['year'] != 2020].copy()

    df_vote = df_no2020[df_no2020['dem_share'].notna()].copy()
    print(f"Sample without 2020: {len(df_vote)} obs")

    for spec, linear, quad in [('basic', False, False), ('linear', True, False), ('quad', True, True)]:
        res = run_twfe_regression(df_vote, 'dem_share', 'treat',
                                  ['county_id', 'state_year'], 'county_id',
                                  linear_trend=linear, quad_trend=quad)
        results[f'no2020_dem_share_{spec}'] = res
        print(f"  {spec}: beta={res['beta']:.4f}, se={res['se']:.4f}")

    # ----- Drop 2020: Turnout -----
    df_turnout = df_no2020[df_no2020['turnout_share'].notna()].copy()
    print(f"\nTurnout sample without 2020: {len(df_turnout)} obs")

    for spec, linear, quad in [('basic', False, False), ('linear', True, False), ('quad', True, True)]:
        res = run_twfe_regression(df_turnout, 'turnout_share', 'treat',
                                  ['county_id', 'state_year'], 'county_id',
                                  linear_trend=linear, quad_trend=quad)
        results[f'no2020_turnout_{spec}'] = res
        print(f"  {spec}: beta={res['beta']:.4f}, se={res['se']:.4f}")

    # ----- Extension period only (2020-2024) -----
    print("\n--- Robustness: Extension Period Only (2020-2024) ---")
    df_ext = df[df['period'] == 'extension'].copy()

    df_vote = df_ext[df_ext['dem_share'].notna()].copy()
    print(f"Extension only: {len(df_vote)} obs")

    if len(df_vote) > 10:  # Need sufficient observations
        for spec, linear, quad in [('basic', False, False)]:
            try:
                res = run_twfe_regression(df_vote, 'dem_share', 'treat',
                                          ['county_id', 'state_year'], 'county_id',
                                          linear_trend=linear, quad_trend=quad)
                results[f'ext_only_dem_share_{spec}'] = res
                print(f"  {spec}: beta={res['beta']:.4f}, se={res['se']:.4f}")
            except Exception as e:
                print(f"  {spec}: Error - {str(e)[:50]}")

    return results


# =============================================================================
# Save results
# =============================================================================

def save_extension_results(all_results):
    """Save all extension analysis results."""

    # Main results
    rows = []
    for table_key in ['table2', 'table3']:
        if table_key in all_results.get('main', {}):
            for spec_key, res in all_results['main'][table_key].items():
                rows.append({
                    'table': table_key,
                    'outcome': spec_key.rsplit('_', 1)[0],
                    'specification': spec_key.rsplit('_', 1)[1],
                    'beta': res.get('beta', np.nan),
                    'se': res.get('se', np.nan),
                    'n_obs': res.get('n_obs', np.nan),
                    'n_counties': res.get('n_counties', np.nan)
                })

    if rows:
        df_main = pd.DataFrame(rows)
        outpath = os.path.join(OUTPUT_DIR, 'extension_main_results.csv')
        df_main.to_csv(outpath, index=False)
        print(f"\nSaved: {outpath}")

    # Heterogeneous effects
    rows = []
    for spec_key, res in all_results.get('heterogeneous', {}).items():
        if isinstance(res, dict) and 'treat' in res:
            rows.append({
                'outcome': spec_key.rsplit('_', 1)[0],
                'specification': spec_key.rsplit('_', 1)[1],
                'treat_beta': res['treat']['beta'],
                'treat_se': res['treat']['se'],
                'treat_x_post2018_beta': res['treat_x_post2018']['beta'],
                'treat_x_post2018_se': res['treat_x_post2018']['se'],
                'n_obs': res.get('n_obs', np.nan),
                'n_counties': res.get('n_counties', np.nan)
            })

    if rows:
        df_het = pd.DataFrame(rows)
        outpath = os.path.join(OUTPUT_DIR, 'extension_heterogeneous_effects.csv')
        df_het.to_csv(outpath, index=False)
        print(f"Saved: {outpath}")

    # Period-specific results
    rows = []
    for period in ['original', 'extension']:
        if period in all_results.get('by_period', {}):
            for spec_key, res in all_results['by_period'][period].items():
                rows.append({
                    'period': period,
                    'outcome': spec_key.rsplit('_', 1)[0],
                    'specification': spec_key.rsplit('_', 1)[1],
                    'beta': res.get('beta', np.nan),
                    'se': res.get('se', np.nan),
                    'n_obs': res.get('n_obs', np.nan)
                })

    if rows:
        df_period = pd.DataFrame(rows)
        outpath = os.path.join(OUTPUT_DIR, 'extension_by_period.csv')
        df_period.to_csv(outpath, index=False)
        print(f"Saved: {outpath}")

    # California analysis
    rows = []
    for spec_key, res in all_results.get('california', {}).items():
        rows.append({
            'outcome': spec_key.replace('ca_', '').rsplit('_', 1)[0],
            'specification': spec_key.rsplit('_', 1)[1],
            'beta': res.get('beta', np.nan),
            'se': res.get('se', np.nan),
            'n_obs': res.get('n_obs', np.nan)
        })

    if rows:
        df_ca = pd.DataFrame(rows)
        outpath = os.path.join(OUTPUT_DIR, 'extension_california.csv')
        df_ca.to_csv(outpath, index=False)
        print(f"Saved: {outpath}")

    # Event study
    if 'event_study' in all_results and 'event_study' in all_results['event_study']:
        rows = []
        es = all_results['event_study']['event_study']
        for key, val in es.items():
            if isinstance(val, dict):
                rows.append({
                    'event_time': key,
                    'beta': val.get('beta', np.nan),
                    'se': val.get('se', np.nan)
                })

        if rows:
            df_es = pd.DataFrame(rows)
            outpath = os.path.join(OUTPUT_DIR, 'extension_event_study.csv')
            df_es.to_csv(outpath, index=False)
            print(f"Saved: {outpath}")

    # Robustness
    rows = []
    for spec_key, res in all_results.get('robustness', {}).items():
        rows.append({
            'check': spec_key.split('_')[0],
            'outcome': '_'.join(spec_key.split('_')[1:-1]),
            'specification': spec_key.rsplit('_', 1)[1],
            'beta': res.get('beta', np.nan),
            'se': res.get('se', np.nan),
            'n_obs': res.get('n_obs', np.nan)
        })

    if rows:
        df_robust = pd.DataFrame(rows)
        outpath = os.path.join(OUTPUT_DIR, 'extension_robustness.csv')
        df_robust.to_csv(outpath, index=False)
        print(f"Saved: {outpath}")


# =============================================================================
# Main
# =============================================================================

def main():
    """Run all extension analyses."""

    print("="*70)
    print("VOTE-BY-MAIL EXTENSION ANALYSIS (1996-2024)")
    print("="*70)

    # Load data
    df = load_extended_data()

    # Store all results
    all_results = {}

    # Task 5.1: Main results with extended data
    all_results['main'] = run_extended_main_results(df)

    # Task 5.2: Heterogeneous effects
    all_results['heterogeneous'] = test_heterogeneous_effects(df)

    # Task 5.3: Separate estimates by period
    all_results['by_period'] = run_separate_period_estimates(df)

    # Task 5.4: California-specific analysis
    all_results['california'] = run_california_analysis(df)

    # Task 5.5: Event study
    all_results['event_study'] = run_event_study(df)

    # Task 5.6: Robustness checks
    all_results['robustness'] = run_robustness_checks(df)

    # Save all results
    save_extension_results(all_results)

    # Summary
    print("\n" + "="*70)
    print("EXTENSION ANALYSIS COMPLETE")
    print("="*70)
    print("\nKey findings summary:")
    print("-"*50)

    # Main results summary
    if 'main' in all_results and 'table2' in all_results['main']:
        res = all_results['main']['table2'].get('dem_share_quad', {})
        print(f"Dem vote share (full sample, quad): {res.get('beta', np.nan):.4f} ({res.get('se', np.nan):.4f})")

    if 'main' in all_results and 'table3' in all_results['main']:
        res = all_results['main']['table3'].get('turnout_quad', {})
        print(f"Turnout (full sample, quad): {res.get('beta', np.nan):.4f} ({res.get('se', np.nan):.4f})")

    # Heterogeneity
    if 'heterogeneous' in all_results:
        res = all_results['heterogeneous'].get('dem_share_quad', {})
        if 'treat_x_post2018' in res:
            print(f"\nVBM × Post2018 interaction (dem share, quad): {res['treat_x_post2018']['beta']:.4f} ({res['treat_x_post2018']['se']:.4f})")

    return all_results


if __name__ == "__main__":
    results = main()
