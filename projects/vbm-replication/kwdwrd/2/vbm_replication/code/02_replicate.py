"""
02_replicate.py

Replication of Thompson et al. (2020) Tables 2 and 3
"Universal vote-by-mail has no impact on partisan turnout or vote share"

This script replicates the main results using the original data.
Uses linearmodels.PanelOLS for proper handling of high-dimensional fixed effects.
"""

import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# LOAD DATA
# =============================================================================

def load_data():
    """Load the original analysis dataset."""
    df = pd.read_stata('original/data/modified/analysis.dta')
    # Create state_year string for reference
    df['state_year'] = df['state'] + '_' + df['year'].astype(str)
    return df


def prepare_dem_voteshare_data(df):
    """
    Prepare pooled democratic vote share data (gubernatorial, presidential, senatorial).
    This matches the Stata reshape in the original code for Table 2 cols 4-6.
    """
    keep_cols = ['state', 'county', 'county_id', 'year', 'treat', 'year2', 'state_year_id']
    dem_cols = ['dem_share_gov', 'dem_share_pres', 'dem_share_sen']

    # Reshape long
    df_long = df[keep_cols + dem_cols].melt(
        id_vars=keep_cols,
        value_vars=dem_cols,
        var_name='office',
        value_name='dem_share'
    )
    df_long['office'] = df_long['office'].str.replace('dem_share_', '')
    df_long = df_long.dropna(subset=['dem_share'])

    return df_long


# =============================================================================
# REGRESSION FUNCTIONS
# =============================================================================

def run_panel_regression(df, y_var, x_var='treat', sample_filter=None, trend_type='none'):
    """
    Run two-way fixed effects panel regression with clustered standard errors.

    Implements: Y_cst = beta*treat + county_FE + state_year_FE + [trends] + epsilon
    Clustered SEs at county level.

    Parameters:
    -----------
    df : DataFrame
    y_var : str - outcome variable
    x_var : str - treatment variable (default 'treat')
    sample_filter : Series of bool or None - rows to include
    trend_type : str - 'none', 'linear', or 'quadratic'

    Returns:
    --------
    dict with coef, se, n_obs, n_counties, n_elections
    """

    # Apply sample filter
    if sample_filter is not None:
        sample = df[sample_filter].copy()
    else:
        sample = df.copy()

    # Select needed columns and drop missing
    cols_needed = [y_var, x_var, 'county_id', 'state_year_id', 'year', 'year2']
    sample = sample[cols_needed].dropna().copy()

    if len(sample) == 0:
        return None

    # Ensure numeric types
    sample[y_var] = sample[y_var].astype(float)
    sample[x_var] = sample[x_var].astype(float)
    sample['county_id'] = sample['county_id'].astype(int)
    sample['state_year_id'] = sample['state_year_id'].astype(int)
    sample['year'] = sample['year'].astype(float)
    sample['year2'] = sample['year2'].astype(float)

    # Build exogenous variables
    exog_cols = [x_var]

    # Add county-specific trends if requested
    if trend_type in ['linear', 'quadratic']:
        # Demean year within county for numerical stability
        sample['year_dm'] = sample['year'] - sample.groupby('county_id')['year'].transform('mean')
        exog_cols.append('year_dm')

        # Create county-specific linear trend interactions
        # We use the absorbed FE approach: include year interacted with county dummies
        # But PanelOLS doesn't directly support this, so we add as exog variables
        county_ids = sorted(sample['county_id'].unique())
        for i, cid in enumerate(county_ids[1:]):  # Drop first for identification
            col_name = f'ctrend_{cid}'
            sample[col_name] = ((sample['county_id'] == cid).astype(float) * sample['year_dm']).values
            exog_cols.append(col_name)

    if trend_type == 'quadratic':
        sample['year2_dm'] = sample['year2'] - sample.groupby('county_id')['year2'].transform('mean')
        county_ids = sorted(sample['county_id'].unique())
        for i, cid in enumerate(county_ids[1:]):
            col_name = f'ctrend2_{cid}'
            sample[col_name] = ((sample['county_id'] == cid).astype(float) * sample['year2_dm']).values
            exog_cols.append(col_name)

    # Set up panel index
    sample = sample.reset_index(drop=True)
    sample['entity'] = sample['county_id']
    sample['time'] = sample['state_year_id']
    sample = sample.set_index(['entity', 'time'])

    # Prepare exogenous variables with constant
    exog = sample[exog_cols].copy()
    exog = sm.add_constant(exog, has_constant='add')

    # Run PanelOLS with entity and time effects
    try:
        model = PanelOLS(
            dependent=sample[y_var],
            exog=exog,
            entity_effects=True,
            time_effects=True,
            drop_absorbed=True
        )
        results = model.fit(cov_type='clustered', cluster_entity=True)

        coef = results.params[x_var]
        se = results.std_errors[x_var]
    except Exception as e:
        # Fallback to manual demeaning approach
        print(f"  Warning: PanelOLS failed ({e}), using fallback")
        return run_manual_twfe(df, y_var, x_var, sample_filter, trend_type)

    return {
        'coef': coef,
        'se': se,
        'n_obs': int(results.nobs),
        'n_counties': sample.index.get_level_values('entity').nunique(),
        'n_elections': sample.index.get_level_values('time').nunique()
    }


def run_manual_twfe(df, y_var, x_var='treat', sample_filter=None, trend_type='none'):
    """
    Fallback: Manual two-way fixed effects via within transformation.
    """

    # Apply sample filter
    if sample_filter is not None:
        sample = df[sample_filter].copy()
    else:
        sample = df.copy()

    cols_needed = [y_var, x_var, 'county_id', 'state_year_id', 'year', 'year2']
    sample = sample[cols_needed].dropna().copy()

    if len(sample) == 0:
        return None

    # Ensure numeric
    for col in cols_needed:
        sample[col] = sample[col].astype(float)
    sample['county_id'] = sample['county_id'].astype(int)
    sample['state_year_id'] = sample['state_year_id'].astype(int)

    # Within transformation: demean by county and state-year
    # First demean by county
    for var in [y_var, x_var]:
        sample[f'{var}_dm1'] = sample[var] - sample.groupby('county_id')[var].transform('mean')

    # Then demean by state-year
    for var in [y_var, x_var]:
        sample[f'{var}_dm'] = sample[f'{var}_dm1'] - sample.groupby('state_year_id')[f'{var}_dm1'].transform('mean')

    # Add back the grand mean (not strictly necessary but cleaner)
    y = sample[f'{y_var}_dm']
    X = sample[[f'{x_var}_dm']]

    if trend_type != 'none':
        # Add demeaned trends
        sample['year_dm'] = sample['year'] - sample.groupby('county_id')['year'].transform('mean')
        sample['year_dm'] = sample['year_dm'] - sample.groupby('state_year_id')['year_dm'].transform('mean')
        X = pd.concat([X, sample[['year_dm']]], axis=1)

    if trend_type == 'quadratic':
        sample['year2_dm'] = sample['year2'] - sample.groupby('county_id')['year2'].transform('mean')
        sample['year2_dm'] = sample['year2_dm'] - sample.groupby('state_year_id')['year2_dm'].transform('mean')
        X = pd.concat([X, sample[['year2_dm']]], axis=1)

    # OLS on demeaned data
    model = sm.OLS(y, X)
    # Clustered SEs - need to adjust DoF for absorbed FEs
    n_counties = sample['county_id'].nunique()
    n_state_years = sample['state_year_id'].nunique()

    results = model.fit(cov_type='cluster', cov_kwds={'groups': sample['county_id']})

    return {
        'coef': results.params[f'{x_var}_dm'],
        'se': results.bse[f'{x_var}_dm'],
        'n_obs': len(sample),
        'n_counties': n_counties,
        'n_elections': n_state_years
    }


# =============================================================================
# TABLE 2: PARTISAN OUTCOMES
# =============================================================================

def replicate_table2(df):
    """
    Replicate Table 2: Partisan Outcomes

    Columns 1-3: Democratic Turnout Share (CA + UT only)
    Columns 4-6: Democratic Vote Share (all states, gubernatorial)
    """

    print("\n" + "="*70)
    print("TABLE 2: PARTISAN OUTCOMES REPLICATION")
    print("="*70)

    results = {}

    # ----- DEMOCRATIC TURNOUT SHARE (Columns 1-3) -----
    print("\n--- Democratic Turnout Share (CA + UT only) ---")

    filter_ca_ut = df['state'].isin(['CA', 'UT'])

    trend_types = ['none', 'linear', 'quadratic']
    for i, trend in enumerate(trend_types, 1):
        res = run_panel_regression(
            df=df,
            y_var='share_votes_dem',
            sample_filter=filter_ca_ut,
            trend_type=trend
        )
        if res:
            results[f'dem_turnout_col{i}'] = res
            print(f"  Col {i} ({trend:10s}): coef = {res['coef']:8.4f}, se = ({res['se']:.4f}), "
                  f"N = {res['n_obs']}, counties = {res['n_counties']}")

    # ----- DEMOCRATIC VOTE SHARE (Columns 4-6) -----
    # Pooled across gubernatorial, presidential, and senatorial elections
    print("\n--- Democratic Vote Share (pooled gov/pres/sen, all states) ---")

    df_long = prepare_dem_voteshare_data(df)

    for i, trend in enumerate(trend_types, 4):
        res = run_panel_regression(
            df=df_long,
            y_var='dem_share',
            sample_filter=None,
            trend_type=trend
        )
        if res:
            results[f'dem_voteshare_col{i}'] = res
            print(f"  Col {i} ({trend:10s}): coef = {res['coef']:8.4f}, se = ({res['se']:.4f}), "
                  f"N = {res['n_obs']}, counties = {res['n_counties']}")

    return results


# =============================================================================
# TABLE 3: PARTICIPATION OUTCOMES
# =============================================================================

def replicate_table3(df):
    """
    Replicate Table 3: Participation Outcomes

    Columns 1-3: Turnout Share (all states)
    Columns 4-6: VBM Share (CA only)
    """

    print("\n" + "="*70)
    print("TABLE 3: PARTICIPATION OUTCOMES REPLICATION")
    print("="*70)

    results = {}

    # ----- TURNOUT SHARE (Columns 1-3) -----
    print("\n--- Turnout Share (all states) ---")

    trend_types = ['none', 'linear', 'quadratic']
    for i, trend in enumerate(trend_types, 1):
        res = run_panel_regression(
            df=df,
            y_var='turnout_share',
            sample_filter=None,
            trend_type=trend
        )
        if res:
            results[f'turnout_col{i}'] = res
            print(f"  Col {i} ({trend:10s}): coef = {res['coef']:8.4f}, se = ({res['se']:.4f}), "
                  f"N = {res['n_obs']}, counties = {res['n_counties']}")

    # ----- VBM SHARE (Columns 4-6) -----
    print("\n--- VBM Share (CA only) ---")

    filter_ca = df['state'] == 'CA'

    for i, trend in enumerate(trend_types, 4):
        res = run_panel_regression(
            df=df,
            y_var='vbm_share',
            sample_filter=filter_ca,
            trend_type=trend
        )
        if res:
            results[f'vbm_col{i}'] = res
            print(f"  Col {i} ({trend:10s}): coef = {res['coef']:8.4f}, se = ({res['se']:.4f}), "
                  f"N = {res['n_obs']}, counties = {res['n_counties']}")

    return results


# =============================================================================
# COMPARISON
# =============================================================================

def get_original_values():
    """Return the original paper's reported values."""

    # Table 2 - Partisan Outcomes
    original_table2 = {
        'dem_turnout_col1': {'coef': 0.007, 'se': 0.003, 'n_counties': 87},
        'dem_turnout_col2': {'coef': 0.001, 'se': 0.001, 'n_counties': 87},
        'dem_turnout_col3': {'coef': 0.001, 'se': 0.001, 'n_counties': 87},
        'dem_voteshare_col4': {'coef': 0.028, 'se': 0.011, 'n_counties': 126},
        'dem_voteshare_col5': {'coef': 0.011, 'se': 0.004, 'n_counties': 126},
        'dem_voteshare_col6': {'coef': 0.007, 'se': 0.003, 'n_counties': 126},
    }

    # Table 3 - Participation Outcomes
    original_table3 = {
        'turnout_col1': {'coef': 0.021, 'se': 0.009, 'n_counties': 126},
        'turnout_col2': {'coef': 0.022, 'se': 0.007, 'n_counties': 126},
        'turnout_col3': {'coef': 0.021, 'se': 0.008, 'n_counties': 126},
        'vbm_col4': {'coef': 0.186, 'se': 0.027, 'n_counties': 58},
        'vbm_col5': {'coef': 0.157, 'se': 0.035, 'n_counties': 58},
        'vbm_col6': {'coef': 0.136, 'se': 0.085, 'n_counties': 58},
    }

    return original_table2, original_table3


def print_comparison(replicated, original, table_name):
    """Print comparison between original and replicated results."""

    print(f"\n{'='*80}")
    print(f"COMPARISON: {table_name}")
    print("="*80)
    print(f"{'Key':<20} {'Original Coef':>14} {'Replicated Coef':>16} {'Difference':>12} {'Match?':>8}")
    print("-"*80)

    for key in sorted(original.keys()):
        orig = original[key]
        if key in replicated:
            repl = replicated[key]
            diff = repl['coef'] - orig['coef']
            # Consider a match if within 10% or 0.005 absolute
            match = abs(diff) < max(0.1 * abs(orig['coef']), 0.005)
            match_str = "YES" if match else "NO"
            print(f"{key:<20} {orig['coef']:>8.4f} ({orig['se']:.3f}) "
                  f"{repl['coef']:>8.4f} ({repl['se']:.3f}) {diff:>12.4f} {match_str:>8}")
        else:
            print(f"{key:<20} {orig['coef']:>8.4f} ({orig['se']:.3f}) {'N/A':>16} {'N/A':>12} {'N/A':>8}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":

    print("="*70)
    print("REPLICATION OF THOMPSON ET AL. (2020)")
    print("Universal vote-by-mail has no impact on partisan turnout or vote share")
    print("="*70)

    print("\nLoading data...")
    df = load_data()
    print(f"Loaded {len(df)} observations from analysis.dta")
    print(f"  - CA: {(df['state']=='CA').sum()} obs, {df[df['state']=='CA']['county'].nunique()} counties")
    print(f"  - UT: {(df['state']=='UT').sum()} obs, {df[df['state']=='UT']['county'].nunique()} counties")
    print(f"  - WA: {(df['state']=='WA').sum()} obs, {df[df['state']=='WA']['county'].nunique()} counties")

    # Run replications
    table2_results = replicate_table2(df)
    table3_results = replicate_table3(df)

    # Get original values
    orig_table2, orig_table3 = get_original_values()

    # Print comparisons
    print_comparison(table2_results, orig_table2, "TABLE 2 - Partisan Outcomes")
    print_comparison(table3_results, orig_table3, "TABLE 3 - Participation Outcomes")

    # Save results to CSV
    print("\n" + "="*70)
    print("SAVING RESULTS")
    print("="*70)

    all_results = {**table2_results, **table3_results}
    all_original = {**orig_table2, **orig_table3}

    rows = []
    for key in sorted(all_original.keys()):
        orig = all_original[key]
        repl = all_results.get(key, {})
        rows.append({
            'specification': key,
            'original_coef': orig['coef'],
            'original_se': orig['se'],
            'original_counties': orig.get('n_counties', ''),
            'replicated_coef': repl.get('coef', np.nan),
            'replicated_se': repl.get('se', np.nan),
            'replicated_n_obs': repl.get('n_obs', np.nan),
            'replicated_counties': repl.get('n_counties', np.nan),
            'difference': repl.get('coef', np.nan) - orig['coef'] if repl else np.nan
        })

    results_df = pd.DataFrame(rows)
    results_df.to_csv('output/tables/replication_comparison.csv', index=False)
    print("Saved to output/tables/replication_comparison.csv")

    # Also save formatted tables
    # Table 2 formatted
    table2_formatted = []
    for outcome in ['dem_turnout', 'dem_voteshare']:
        row = {'outcome': outcome}
        for col in [1, 2, 3] if outcome == 'dem_turnout' else [4, 5, 6]:
            key = f'{outcome}_col{col}'
            if key in all_results:
                row[f'col{col}_coef'] = all_results[key]['coef']
                row[f'col{col}_se'] = all_results[key]['se']
        table2_formatted.append(row)

    pd.DataFrame(table2_formatted).to_csv('output/tables/table2_replication.csv', index=False)

    # Table 3 formatted
    table3_formatted = []
    for outcome in ['turnout', 'vbm']:
        row = {'outcome': outcome}
        for col in [1, 2, 3] if outcome == 'turnout' else [4, 5, 6]:
            key = f'{outcome}_col{col}'
            if key in all_results:
                row[f'col{col}_coef'] = all_results[key]['coef']
                row[f'col{col}_se'] = all_results[key]['se']
        table3_formatted.append(row)

    pd.DataFrame(table3_formatted).to_csv('output/tables/table3_replication.csv', index=False)
    print("Saved table2_replication.csv and table3_replication.csv")

    print("\nReplication complete!")
