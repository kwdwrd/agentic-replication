"""
02_replicate.py

Replicate Tables 2 and 3 from Thompson, Wu, Yoder, and Hall (2020)
"Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share"

This script implements the difference-in-differences specifications:
1. Basic: County FE + State×Year FE
2. Linear trends: + County-specific linear time trends
3. Quadratic trends: + County-specific quadratic time trends
"""

import pandas as pd
import numpy as np
from pathlib import Path
import statsmodels.api as sm
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "original" / "data" / "modified"
OUTPUT_DIR = PROJECT_ROOT / "output" / "tables"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    """Load and prepare the analysis dataset."""
    df = pd.read_stata(DATA_DIR / "analysis.dta")

    # Create state_year identifier for FE
    df['state_year'] = df['state'] + '_' + df['year'].astype(int).astype(str)

    # Ensure year variables are numeric
    df['year'] = df['year'].astype(float)
    df['year2'] = df['year'] ** 2

    return df


def run_twfe_regression(df, y_var, treat_var='treat', county_var='county_id',
                        state_year_var='state_year', cluster_var='county_id',
                        trend_type='none'):
    """
    Run two-way fixed effects regression with optional county trends.

    Uses the Frisch-Waugh-Lovell approach:
    1. Demean by county (absorb county FE)
    2. Demean by state-year (absorb state×year FE)
    3. Optionally residualize on county-specific trends

    Parameters:
    -----------
    df : DataFrame
        Analysis data
    y_var : str
        Outcome variable name
    treat_var : str
        Treatment variable name
    county_var : str
        County identifier for county FE
    state_year_var : str
        State-year identifier for state×year FE
    cluster_var : str
        Variable for clustering standard errors
    trend_type : str
        'none', 'linear', or 'quadratic' for county-specific trends

    Returns:
    --------
    dict with coefficient, se, n_obs, n_clusters
    """
    # Select relevant columns and drop missing
    # Use set to avoid duplicate columns (cluster_var may equal county_var)
    cols_needed = list(set([y_var, treat_var, county_var, state_year_var, cluster_var, 'year']))
    sample = df[cols_needed].dropna().copy().reset_index(drop=True)

    # Step 1: Demean by county (within transformation)
    y_dm = sample[y_var] - sample.groupby(county_var)[y_var].transform('mean')
    treat_dm = sample[treat_var] - sample.groupby(county_var)[treat_var].transform('mean')

    # Step 2: Demean by state-year
    sample['y_dm'] = y_dm
    sample['treat_dm'] = treat_dm
    y_dm2 = sample['y_dm'] - sample.groupby(state_year_var)['y_dm'].transform('mean')
    treat_dm2 = sample['treat_dm'] - sample.groupby(state_year_var)['treat_dm'].transform('mean')

    # Step 3: Handle trends
    if trend_type == 'none':
        y_final = y_dm2
        x_final = treat_dm2
    else:
        # Center year for numerical stability
        year_centered = sample['year'] - sample['year'].mean()

        if trend_type == 'linear':
            # Residualize on county-specific linear trends
            sample['y_dm2'] = y_dm2
            sample['treat_dm2'] = treat_dm2
            sample['year_c'] = year_centered

            # For each county, regress demeaned var on year and take residuals
            y_resid = []
            treat_resid = []

            for county in sample[county_var].unique():
                mask = sample[county_var] == county
                county_data = sample[mask]

                if len(county_data) < 2:
                    y_resid.extend(county_data['y_dm2'].tolist())
                    treat_resid.extend(county_data['treat_dm2'].tolist())
                    continue

                X = sm.add_constant(county_data['year_c'])

                # Residualize y
                try:
                    model_y = sm.OLS(county_data['y_dm2'], X).fit()
                    y_resid.extend(model_y.resid.tolist())
                except:
                    y_resid.extend(county_data['y_dm2'].tolist())

                # Residualize treatment
                try:
                    model_t = sm.OLS(county_data['treat_dm2'], X).fit()
                    treat_resid.extend(model_t.resid.tolist())
                except:
                    treat_resid.extend(county_data['treat_dm2'].tolist())

            y_final = pd.Series(y_resid, index=sample.index)
            x_final = pd.Series(treat_resid, index=sample.index)

        elif trend_type == 'quadratic':
            # Residualize on county-specific quadratic trends
            sample['y_dm2'] = y_dm2
            sample['treat_dm2'] = treat_dm2
            sample['year_c'] = year_centered
            sample['year_c2'] = year_centered ** 2

            y_resid = []
            treat_resid = []

            for county in sample[county_var].unique():
                mask = sample[county_var] == county
                county_data = sample[mask]

                if len(county_data) < 3:
                    y_resid.extend(county_data['y_dm2'].tolist())
                    treat_resid.extend(county_data['treat_dm2'].tolist())
                    continue

                X = sm.add_constant(county_data[['year_c', 'year_c2']])

                # Residualize y
                try:
                    model_y = sm.OLS(county_data['y_dm2'], X).fit()
                    y_resid.extend(model_y.resid.tolist())
                except:
                    y_resid.extend(county_data['y_dm2'].tolist())

                # Residualize treatment
                try:
                    model_t = sm.OLS(county_data['treat_dm2'], X).fit()
                    treat_resid.extend(model_t.resid.tolist())
                except:
                    treat_resid.extend(county_data['treat_dm2'].tolist())

            y_final = pd.Series(y_resid, index=sample.index)
            x_final = pd.Series(treat_resid, index=sample.index)

    # Final regression: y = beta * x (no constant needed after demeaning)
    # Add constant for numerical stability
    X = sm.add_constant(x_final)
    model = sm.OLS(y_final, X, missing='drop')

    # Clustered standard errors
    clusters = sample[cluster_var]
    results = model.fit(cov_type='cluster', cov_kwds={'groups': clusters})

    # Extract coefficient on treatment (second parameter, after constant)
    coef = results.params.iloc[1]
    se = results.bse.iloc[1]
    pval = results.pvalues.iloc[1]

    return {
        'coef': coef,
        'se': se,
        'pval': pval,
        'n_obs': int(results.nobs),
        'n_clusters': clusters.nunique()
    }


def replicate_table2(df):
    """
    Replicate Table 2: Partisan Effects

    Columns 1-3: Democratic share of turnout (CA and UT only)
    Columns 4-6: Democratic vote share (all states, reshaped to office level)
    """
    print("\n" + "=" * 60)
    print("REPLICATING TABLE 2: PARTISAN EFFECTS")
    print("=" * 60)

    results = {}

    # Columns 1-3: Democratic turnout share
    print("\nColumns 1-3: Democratic Turnout Share (CA & UT)")
    print("-" * 40)

    # Filter to CA and UT where share_votes_dem is available
    sample_turnout = df[(df['state'].isin(['CA', 'UT'])) & (df['share_votes_dem'].notna())].copy()
    print(f"Sample size: {len(sample_turnout)} obs, {sample_turnout['county_id'].nunique()} counties")

    for i, trend in enumerate(['none', 'linear', 'quadratic'], 1):
        result = run_twfe_regression(
            sample_turnout,
            y_var='share_votes_dem',
            treat_var='treat',
            county_var='county_id',
            state_year_var='state_year',
            cluster_var='county_id',
            trend_type=trend
        )
        results[f'dem_turnout_col{i}'] = result
        print(f"  Col {i} ({trend:10s}): coef = {result['coef']:.4f}, se = {result['se']:.4f}, n = {result['n_obs']}")

    # Columns 4-6: Democratic vote share (reshaped)
    print("\nColumns 4-6: Democratic Vote Share (all states)")
    print("-" * 40)

    # Need to reshape data to have one row per county-year-office
    vote_share_long = []
    for idx, row in df.iterrows():
        for office, var in [('gov', 'dem_share_gov'), ('pres', 'dem_share_pres'), ('sen', 'dem_share_sen')]:
            if pd.notna(row[var]):
                vote_share_long.append({
                    'state': row['state'],
                    'county': row['county'],
                    'year': row['year'],
                    'county_id': row['county_id'],
                    'state_year': row['state_year'],
                    'treat': row['treat'],
                    'office': office,
                    'dem_share': row[var]
                })

    sample_voteshare = pd.DataFrame(vote_share_long)
    print(f"Sample size: {len(sample_voteshare)} obs, {sample_voteshare['county_id'].nunique()} counties")

    for i, trend in enumerate(['none', 'linear', 'quadratic'], 1):
        result = run_twfe_regression(
            sample_voteshare,
            y_var='dem_share',
            treat_var='treat',
            county_var='county_id',
            state_year_var='state_year',
            cluster_var='county_id',
            trend_type=trend
        )
        col_num = i + 3
        results[f'dem_voteshare_col{col_num}'] = result
        print(f"  Col {col_num} ({trend:10s}): coef = {result['coef']:.4f}, se = {result['se']:.4f}, n = {result['n_obs']}")

    return results


def replicate_table3(df):
    """
    Replicate Table 3: Participation Effects

    Columns 1-3: Turnout (all states)
    Columns 4-6: VBM share (CA only)
    """
    print("\n" + "=" * 60)
    print("REPLICATING TABLE 3: PARTICIPATION EFFECTS")
    print("=" * 60)

    results = {}

    # Columns 1-3: Turnout
    print("\nColumns 1-3: Turnout Share (all states)")
    print("-" * 40)

    sample_turnout = df[df['turnout_share'].notna()].copy()
    print(f"Sample size: {len(sample_turnout)} obs, {sample_turnout['county_id'].nunique()} counties")

    for i, trend in enumerate(['none', 'linear', 'quadratic'], 1):
        result = run_twfe_regression(
            sample_turnout,
            y_var='turnout_share',
            treat_var='treat',
            county_var='county_id',
            state_year_var='state_year',
            cluster_var='county_id',
            trend_type=trend
        )
        results[f'turnout_col{i}'] = result
        print(f"  Col {i} ({trend:10s}): coef = {result['coef']:.4f}, se = {result['se']:.4f}, n = {result['n_obs']}")

    # Columns 4-6: VBM share (CA only)
    print("\nColumns 4-6: VBM Share (CA only)")
    print("-" * 40)

    sample_vbm = df[(df['state'] == 'CA') & (df['vbm_share'].notna())].copy()
    print(f"Sample size: {len(sample_vbm)} obs, {sample_vbm['county_id'].nunique()} counties")

    for i, trend in enumerate(['none', 'linear', 'quadratic'], 1):
        result = run_twfe_regression(
            sample_vbm,
            y_var='vbm_share',
            treat_var='treat',
            county_var='county_id',
            state_year_var='state_year',
            cluster_var='county_id',
            trend_type=trend
        )
        col_num = i + 3
        results[f'vbm_col{col_num}'] = result
        print(f"  Col {col_num} ({trend:10s}): coef = {result['coef']:.4f}, se = {result['se']:.4f}, n = {result['n_obs']}")

    return results


def get_original_results():
    """
    Original results from the published paper (Tables 2 and 3).
    """
    original_table2 = {
        'dem_turnout': {
            'col1': {'coef': 0.007, 'se': 0.003},
            'col2': {'coef': 0.001, 'se': 0.001},
            'col3': {'coef': 0.001, 'se': 0.001}
        },
        'dem_voteshare': {
            'col4': {'coef': 0.028, 'se': 0.011},
            'col5': {'coef': 0.011, 'se': 0.004},
            'col6': {'coef': 0.007, 'se': 0.003}
        }
    }

    original_table3 = {
        'turnout': {
            'col1': {'coef': 0.021, 'se': 0.009},
            'col2': {'coef': 0.022, 'se': 0.007},
            'col3': {'coef': 0.021, 'se': 0.008}
        },
        'vbm_share': {
            'col4': {'coef': 0.186, 'se': 0.027},
            'col5': {'coef': 0.157, 'se': 0.035},
            'col6': {'coef': 0.136, 'se': 0.085}
        }
    }

    return original_table2, original_table3


def save_results(table2_results, table3_results, original_table2, original_table3):
    """Save replication results to CSV."""

    # Table 2 comparison
    table2_comparison = []

    # Dem turnout share (cols 1-3)
    for col_num in [1, 2, 3]:
        key = f'dem_turnout_col{col_num}'
        orig_key = f'col{col_num}'
        if key in table2_results:
            rep = table2_results[key]
            orig = original_table2['dem_turnout'][orig_key]
            table2_comparison.append({
                'Outcome': 'Dem Turnout Share',
                'Column': col_num,
                'Specification': ['Basic', 'Linear', 'Quadratic'][col_num-1],
                'Original_Coef': orig['coef'],
                'Original_SE': orig['se'],
                'Replicated_Coef': round(rep['coef'], 4),
                'Replicated_SE': round(rep['se'], 4),
                'Coef_Diff': round(rep['coef'] - orig['coef'], 4),
                'N_Obs': rep['n_obs'],
                'N_Clusters': rep['n_clusters']
            })

    # Dem vote share (cols 4-6)
    for col_num in [4, 5, 6]:
        key = f'dem_voteshare_col{col_num}'
        orig_key = f'col{col_num}'
        if key in table2_results:
            rep = table2_results[key]
            orig = original_table2['dem_voteshare'][orig_key]
            table2_comparison.append({
                'Outcome': 'Dem Vote Share',
                'Column': col_num,
                'Specification': ['Basic', 'Linear', 'Quadratic'][col_num-4],
                'Original_Coef': orig['coef'],
                'Original_SE': orig['se'],
                'Replicated_Coef': round(rep['coef'], 4),
                'Replicated_SE': round(rep['se'], 4),
                'Coef_Diff': round(rep['coef'] - orig['coef'], 4),
                'N_Obs': rep['n_obs'],
                'N_Clusters': rep['n_clusters']
            })

    df_table2 = pd.DataFrame(table2_comparison)
    df_table2.to_csv(OUTPUT_DIR / 'table2_replication.csv', index=False)

    # Table 3 comparison
    table3_comparison = []

    # Turnout (cols 1-3)
    for col_num in [1, 2, 3]:
        key = f'turnout_col{col_num}'
        orig_key = f'col{col_num}'
        if key in table3_results:
            rep = table3_results[key]
            orig = original_table3['turnout'][orig_key]
            table3_comparison.append({
                'Outcome': 'Turnout',
                'Column': col_num,
                'Specification': ['Basic', 'Linear', 'Quadratic'][col_num-1],
                'Original_Coef': orig['coef'],
                'Original_SE': orig['se'],
                'Replicated_Coef': round(rep['coef'], 4),
                'Replicated_SE': round(rep['se'], 4),
                'Coef_Diff': round(rep['coef'] - orig['coef'], 4),
                'N_Obs': rep['n_obs'],
                'N_Clusters': rep['n_clusters']
            })

    # VBM share (cols 4-6)
    for col_num in [4, 5, 6]:
        key = f'vbm_col{col_num}'
        orig_key = f'col{col_num}'
        if key in table3_results:
            rep = table3_results[key]
            orig = original_table3['vbm_share'][orig_key]
            table3_comparison.append({
                'Outcome': 'VBM Share',
                'Column': col_num,
                'Specification': ['Basic', 'Linear', 'Quadratic'][col_num-4],
                'Original_Coef': orig['coef'],
                'Original_SE': orig['se'],
                'Replicated_Coef': round(rep['coef'], 4),
                'Replicated_SE': round(rep['se'], 4),
                'Coef_Diff': round(rep['coef'] - orig['coef'], 4),
                'N_Obs': rep['n_obs'],
                'N_Clusters': rep['n_clusters']
            })

    df_table3 = pd.DataFrame(table3_comparison)
    df_table3.to_csv(OUTPUT_DIR / 'table3_replication.csv', index=False)

    return df_table2, df_table3


def main():
    print("=" * 60)
    print("REPLICATION OF THOMPSON ET AL. (2020)")
    print("Universal Vote-by-Mail Has No Impact on Partisan")
    print("Turnout or Vote Share")
    print("=" * 60)

    # Load data
    print("\nLoading data...")
    df = load_data()
    print(f"Loaded {len(df)} observations")

    # Get original results for comparison
    original_table2, original_table3 = get_original_results()

    # Replicate Table 2
    table2_results = replicate_table2(df)

    # Replicate Table 3
    table3_results = replicate_table3(df)

    # Save results
    print("\n" + "=" * 60)
    print("SAVING RESULTS")
    print("=" * 60)
    df_table2, df_table3 = save_results(table2_results, table3_results,
                                         original_table2, original_table3)

    # Print comparison
    print("\nTABLE 2 REPLICATION COMPARISON:")
    print(df_table2.to_string(index=False))

    print("\nTABLE 3 REPLICATION COMPARISON:")
    print(df_table3.to_string(index=False))

    print(f"\nResults saved to:")
    print(f"  - {OUTPUT_DIR / 'table2_replication.csv'}")
    print(f"  - {OUTPUT_DIR / 'table3_replication.csv'}")


if __name__ == "__main__":
    main()
