"""
Replication of Thompson et al. (2020) Tables 2 and 3
"Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share"

This script replicates the main results using Python equivalents of Stata's reghdfe.
Uses Frisch-Waugh-Lovell theorem to absorb high-dimensional fixed effects.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# Helper Functions
# =============================================================================

def reghdfe_with_trends(df, y_var, treat_var, trend_type, cluster_var):
    """
    Regression with county and state-year fixed effects plus county-specific trends

    Uses Frisch-Waugh-Lovell theorem:
    1. Residualize y on all fixed effects and trends
    2. Residualize treat on all fixed effects and trends
    3. Regress residualized y on residualized treat

    trend_type: 'none', 'linear', 'quadratic'
    """
    # Prepare data - ensure numeric types
    # Use set to avoid duplicate columns if cluster_var is same as county_id
    required_cols = list(set([y_var, treat_var, 'county_id', 'state_year', 'year', 'year2', cluster_var]))
    df_clean = df[required_cols].dropna().copy()

    # Convert to proper numeric types
    df_clean[y_var] = df_clean[y_var].astype(float)
    df_clean[treat_var] = df_clean[treat_var].astype(float)
    df_clean['year'] = df_clean['year'].astype(float)
    df_clean['year2'] = df_clean['year2'].astype(float)

    n_obs = len(df_clean)
    n_clusters = df_clean[cluster_var].nunique()

    # Create state-year dummies (as float)
    state_year_dummies = pd.get_dummies(df_clean['state_year'], prefix='sy', drop_first=True).astype(float)

    # Create county dummies (as float)
    county_dummies = pd.get_dummies(df_clean['county_id'], prefix='county', drop_first=True).astype(float)

    if trend_type == 'none':
        # Just county and state-year FE
        X_controls = pd.concat([county_dummies, state_year_dummies], axis=1)

    elif trend_type == 'linear':
        # County FE + state-year FE + county-specific linear trends
        year_vals = df_clean['year'].values.reshape(-1, 1)
        county_trends = county_dummies.values * year_vals
        county_trends_df = pd.DataFrame(county_trends,
                                        columns=[f'trend_{c}' for c in county_dummies.columns],
                                        index=county_dummies.index)
        X_controls = pd.concat([county_dummies, state_year_dummies, county_trends_df], axis=1)

    elif trend_type == 'quadratic':
        # County FE + state-year FE + county-specific linear + quadratic trends
        year_vals = df_clean['year'].values.reshape(-1, 1)
        year2_vals = df_clean['year2'].values.reshape(-1, 1)

        county_trends_lin = county_dummies.values * year_vals
        county_trends_lin_df = pd.DataFrame(county_trends_lin,
                                            columns=[f'trendL_{c}' for c in county_dummies.columns],
                                            index=county_dummies.index)

        county_trends_quad = county_dummies.values * year2_vals
        county_trends_quad_df = pd.DataFrame(county_trends_quad,
                                             columns=[f'trendQ_{c}' for c in county_dummies.columns],
                                             index=county_dummies.index)

        X_controls = pd.concat([county_dummies, state_year_dummies,
                               county_trends_lin_df, county_trends_quad_df], axis=1)

    # Get y and treat as numpy arrays
    y = df_clean[y_var].values.astype(float)
    treat = df_clean[treat_var].values.astype(float)

    # Convert controls to numpy and ensure float type
    X_controls_np = X_controls.values.astype(float)

    # Add constant
    X_controls_const = np.column_stack([np.ones(len(y)), X_controls_np])

    # Use numpy least squares for numerical stability
    # Residualize y
    try:
        beta_y, _, _, _ = np.linalg.lstsq(X_controls_const, y, rcond=None)
        y_resid = y - X_controls_const @ beta_y
    except np.linalg.LinAlgError:
        # Fallback: use pseudo-inverse
        beta_y = np.linalg.pinv(X_controls_const) @ y
        y_resid = y - X_controls_const @ beta_y

    # Residualize treat
    try:
        beta_treat, _, _, _ = np.linalg.lstsq(X_controls_const, treat, rcond=None)
        treat_resid = treat - X_controls_const @ beta_treat
    except np.linalg.LinAlgError:
        beta_treat = np.linalg.pinv(X_controls_const) @ treat
        treat_resid = treat - X_controls_const @ beta_treat

    # Final regression with clustered SEs using statsmodels
    # Get cluster values before any index changes
    cluster_vals = df_clean[cluster_var].values.flatten()

    df_final = pd.DataFrame({
        'y_resid': y_resid.flatten(),
        'treat_resid': treat_resid.flatten(),
        'cluster': cluster_vals
    })

    model_final = sm.OLS(df_final['y_resid'], df_final['treat_resid'])
    results = model_final.fit(cov_type='cluster', cov_kwds={'groups': df_final['cluster']})

    return {
        'coef': results.params[0],
        'se': results.bse[0],
        'n_obs': n_obs,
        'n_clusters': n_clusters
    }


def replicate_table2_col1to3(df):
    """
    Replicate Table 2, Columns 1-3: Democratic Turnout Share
    Sample: CA and UT only (counties with voter file data)
    """
    print("\n" + "="*60)
    print("TABLE 2, COLUMNS 1-3: Democratic Turnout Share")
    print("="*60)

    # Filter to non-missing share_votes_dem (this excludes WA)
    df_sample = df[df['share_votes_dem'].notna()].copy()

    # Create state_year identifier
    df_sample['state_year'] = df_sample['state'] + '_' + df_sample['year'].astype(str)

    print(f"\nSample: {len(df_sample)} obs, {df_sample['county_id'].nunique()} counties")
    print(f"States: {df_sample['state'].unique()}")

    results = []

    # Column 1: Basic (county FE + state-year FE)
    print("\nColumn 1: Basic specification...")
    res1 = reghdfe_with_trends(df_sample, 'share_votes_dem', 'treat', 'none', 'county_id')
    results.append(('Basic', res1))
    print(f"  Coef: {res1['coef']:.4f}, SE: {res1['se']:.4f}, N: {res1['n_obs']}, Clusters: {res1['n_clusters']}")

    # Column 2: Linear trends
    print("\nColumn 2: With linear county trends...")
    res2 = reghdfe_with_trends(df_sample, 'share_votes_dem', 'treat', 'linear', 'county_id')
    results.append(('Linear', res2))
    print(f"  Coef: {res2['coef']:.4f}, SE: {res2['se']:.4f}, N: {res2['n_obs']}, Clusters: {res2['n_clusters']}")

    # Column 3: Quadratic trends
    print("\nColumn 3: With quadratic county trends...")
    res3 = reghdfe_with_trends(df_sample, 'share_votes_dem', 'treat', 'quadratic', 'county_id')
    results.append(('Quadratic', res3))
    print(f"  Coef: {res3['coef']:.4f}, SE: {res3['se']:.4f}, N: {res3['n_obs']}, Clusters: {res3['n_clusters']}")

    return results


def replicate_table2_col4to6(df):
    """
    Replicate Table 2, Columns 4-6: Democratic Vote Share
    Sample: All states, reshaped to county-year-office level
    """
    print("\n" + "="*60)
    print("TABLE 2, COLUMNS 4-6: Democratic Vote Share")
    print("="*60)

    # Reshape data to long format (county-year-office)
    df_vote = df[['state', 'county', 'county_id', 'year', 'treat', 'year2', 'year3',
                  'dem_share_gov', 'dem_share_pres', 'dem_share_sen']].copy()

    df_long = pd.melt(df_vote,
                      id_vars=['state', 'county', 'county_id', 'year', 'treat', 'year2', 'year3'],
                      value_vars=['dem_share_gov', 'dem_share_pres', 'dem_share_sen'],
                      var_name='office', value_name='dem_share')

    df_long = df_long[df_long['dem_share'].notna()].copy()

    # Create state_year
    df_long['state_year'] = df_long['state'] + '_' + df_long['year'].astype(str)

    print(f"\nSample: {len(df_long)} obs, {df_long['county_id'].nunique()} counties")
    print(f"States: {df_long['state'].unique()}")

    results = []

    # Column 4: Basic
    print("\nColumn 4: Basic specification...")
    res4 = reghdfe_with_trends(df_long, 'dem_share', 'treat', 'none', 'county_id')
    results.append(('Basic', res4))
    print(f"  Coef: {res4['coef']:.4f}, SE: {res4['se']:.4f}, N: {res4['n_obs']}, Clusters: {res4['n_clusters']}")

    # Column 5: Linear trends
    print("\nColumn 5: With linear county trends...")
    res5 = reghdfe_with_trends(df_long, 'dem_share', 'treat', 'linear', 'county_id')
    results.append(('Linear', res5))
    print(f"  Coef: {res5['coef']:.4f}, SE: {res5['se']:.4f}, N: {res5['n_obs']}, Clusters: {res5['n_clusters']}")

    # Column 6: Quadratic trends
    print("\nColumn 6: With quadratic county trends...")
    res6 = reghdfe_with_trends(df_long, 'dem_share', 'treat', 'quadratic', 'county_id')
    results.append(('Quadratic', res6))
    print(f"  Coef: {res6['coef']:.4f}, SE: {res6['se']:.4f}, N: {res6['n_obs']}, Clusters: {res6['n_clusters']}")

    return results


def replicate_table3_col1to3(df):
    """
    Replicate Table 3, Columns 1-3: Turnout Share
    Sample: All states
    """
    print("\n" + "="*60)
    print("TABLE 3, COLUMNS 1-3: Turnout Share")
    print("="*60)

    # Filter to non-missing turnout_share
    df_sample = df[df['turnout_share'].notna()].copy()

    # Create state_year
    df_sample['state_year'] = df_sample['state'] + '_' + df_sample['year'].astype(str)

    print(f"\nSample: {len(df_sample)} obs, {df_sample['county_id'].nunique()} counties")
    print(f"States: {df_sample['state'].unique()}")

    results = []

    # Column 1: Basic
    print("\nColumn 1: Basic specification...")
    res1 = reghdfe_with_trends(df_sample, 'turnout_share', 'treat', 'none', 'county_id')
    results.append(('Basic', res1))
    print(f"  Coef: {res1['coef']:.4f}, SE: {res1['se']:.4f}, N: {res1['n_obs']}, Clusters: {res1['n_clusters']}")

    # Column 2: Linear trends
    print("\nColumn 2: With linear county trends...")
    res2 = reghdfe_with_trends(df_sample, 'turnout_share', 'treat', 'linear', 'county_id')
    results.append(('Linear', res2))
    print(f"  Coef: {res2['coef']:.4f}, SE: {res2['se']:.4f}, N: {res2['n_obs']}, Clusters: {res2['n_clusters']}")

    # Column 3: Quadratic trends
    print("\nColumn 3: With quadratic county trends...")
    res3 = reghdfe_with_trends(df_sample, 'turnout_share', 'treat', 'quadratic', 'county_id')
    results.append(('Quadratic', res3))
    print(f"  Coef: {res3['coef']:.4f}, SE: {res3['se']:.4f}, N: {res3['n_obs']}, Clusters: {res3['n_clusters']}")

    return results


def replicate_table3_col4to6(df):
    """
    Replicate Table 3, Columns 4-6: VBM Share
    Sample: California only
    """
    print("\n" + "="*60)
    print("TABLE 3, COLUMNS 4-6: VBM Share (CA only)")
    print("="*60)

    # Filter to CA and non-missing vbm_share
    df_sample = df[(df['state'] == 'CA') & (df['vbm_share'].notna())].copy()

    # Create state_year
    df_sample['state_year'] = df_sample['state'] + '_' + df_sample['year'].astype(str)

    print(f"\nSample: {len(df_sample)} obs, {df_sample['county_id'].nunique()} counties")

    results = []

    # Column 4: Basic
    print("\nColumn 4: Basic specification...")
    res4 = reghdfe_with_trends(df_sample, 'vbm_share', 'treat', 'none', 'county_id')
    results.append(('Basic', res4))
    print(f"  Coef: {res4['coef']:.4f}, SE: {res4['se']:.4f}, N: {res4['n_obs']}, Clusters: {res4['n_clusters']}")

    # Column 5: Linear trends
    print("\nColumn 5: With linear county trends...")
    res5 = reghdfe_with_trends(df_sample, 'vbm_share', 'treat', 'linear', 'county_id')
    results.append(('Linear', res5))
    print(f"  Coef: {res5['coef']:.4f}, SE: {res5['se']:.4f}, N: {res5['n_obs']}, Clusters: {res5['n_clusters']}")

    # Column 6: Quadratic trends
    print("\nColumn 6: With quadratic county trends...")
    res6 = reghdfe_with_trends(df_sample, 'vbm_share', 'treat', 'quadratic', 'county_id')
    results.append(('Quadratic', res6))
    print(f"  Coef: {res6['coef']:.4f}, SE: {res6['se']:.4f}, N: {res6['n_obs']}, Clusters: {res6['n_clusters']}")

    return results


def create_table2_replication(cols1to3, cols4to6):
    """Create formatted Table 2 replication"""
    print("\n" + "="*70)
    print("TABLE 2 REPLICATION: Partisan Outcomes")
    print("="*70)

    print("\n{:<20} {:>12} {:>12} {:>12} {:>12} {:>12} {:>12}".format(
        '', '(1)', '(2)', '(3)', '(4)', '(5)', '(6)'))
    print("{:<20} {:>12} {:>12} {:>12} {:>12} {:>12} {:>12}".format(
        '', 'Dem Turn', 'Dem Turn', 'Dem Turn', 'Dem Vote', 'Dem Vote', 'Dem Vote'))
    print("-" * 92)

    # Coefficients
    coefs = [cols1to3[0][1]['coef'], cols1to3[1][1]['coef'], cols1to3[2][1]['coef'],
             cols4to6[0][1]['coef'], cols4to6[1][1]['coef'], cols4to6[2][1]['coef']]
    print("{:<20} {:>12.3f} {:>12.3f} {:>12.3f} {:>12.3f} {:>12.3f} {:>12.3f}".format(
        'VBM', *coefs))

    # Standard errors
    ses = [cols1to3[0][1]['se'], cols1to3[1][1]['se'], cols1to3[2][1]['se'],
           cols4to6[0][1]['se'], cols4to6[1][1]['se'], cols4to6[2][1]['se']]
    print("{:<20} {:>12} {:>12} {:>12} {:>12} {:>12} {:>12}".format(
        '', *[f"({se:.3f})" for se in ses]))

    print("-" * 92)

    # N obs
    ns = [cols1to3[0][1]['n_obs'], cols1to3[1][1]['n_obs'], cols1to3[2][1]['n_obs'],
          cols4to6[0][1]['n_obs'], cols4to6[1][1]['n_obs'], cols4to6[2][1]['n_obs']]
    print("{:<20} {:>12} {:>12} {:>12} {:>12} {:>12} {:>12}".format(
        'N', *ns))

    # N clusters
    ncs = [cols1to3[0][1]['n_clusters'], cols1to3[1][1]['n_clusters'], cols1to3[2][1]['n_clusters'],
           cols4to6[0][1]['n_clusters'], cols4to6[1][1]['n_clusters'], cols4to6[2][1]['n_clusters']]
    print("{:<20} {:>12} {:>12} {:>12} {:>12} {:>12} {:>12}".format(
        'Counties', *ncs))

    print("{:<20} {:>12} {:>12} {:>12} {:>12} {:>12} {:>12}".format(
        'County FE', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'))
    print("{:<20} {:>12} {:>12} {:>12} {:>12} {:>12} {:>12}".format(
        'State×Year FE', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'))
    print("{:<20} {:>12} {:>12} {:>12} {:>12} {:>12} {:>12}".format(
        'County Trends', 'No', 'Linear', 'Quad', 'No', 'Linear', 'Quad'))

    # Save to CSV
    table2_data = {
        'Specification': ['Basic', 'Linear Trends', 'Quadratic Trends'],
        'Dem_Turnout_Coef': [cols1to3[i][1]['coef'] for i in range(3)],
        'Dem_Turnout_SE': [cols1to3[i][1]['se'] for i in range(3)],
        'Dem_Turnout_N': [cols1to3[i][1]['n_obs'] for i in range(3)],
        'Dem_Vote_Coef': [cols4to6[i][1]['coef'] for i in range(3)],
        'Dem_Vote_SE': [cols4to6[i][1]['se'] for i in range(3)],
        'Dem_Vote_N': [cols4to6[i][1]['n_obs'] for i in range(3)]
    }
    pd.DataFrame(table2_data).to_csv('output/tables/table2_replication.csv', index=False)


def create_table3_replication(cols1to3, cols4to6):
    """Create formatted Table 3 replication"""
    print("\n" + "="*70)
    print("TABLE 3 REPLICATION: Participation Outcomes")
    print("="*70)

    print("\n{:<20} {:>12} {:>12} {:>12} {:>12} {:>12} {:>12}".format(
        '', '(1)', '(2)', '(3)', '(4)', '(5)', '(6)'))
    print("{:<20} {:>12} {:>12} {:>12} {:>12} {:>12} {:>12}".format(
        '', 'Turnout', 'Turnout', 'Turnout', 'VBM Share', 'VBM Share', 'VBM Share'))
    print("-" * 92)

    # Coefficients
    coefs = [cols1to3[0][1]['coef'], cols1to3[1][1]['coef'], cols1to3[2][1]['coef'],
             cols4to6[0][1]['coef'], cols4to6[1][1]['coef'], cols4to6[2][1]['coef']]
    print("{:<20} {:>12.3f} {:>12.3f} {:>12.3f} {:>12.3f} {:>12.3f} {:>12.3f}".format(
        'VBM', *coefs))

    # Standard errors
    ses = [cols1to3[0][1]['se'], cols1to3[1][1]['se'], cols1to3[2][1]['se'],
           cols4to6[0][1]['se'], cols4to6[1][1]['se'], cols4to6[2][1]['se']]
    print("{:<20} {:>12} {:>12} {:>12} {:>12} {:>12} {:>12}".format(
        '', *[f"({se:.3f})" for se in ses]))

    print("-" * 92)

    # N obs
    ns = [cols1to3[0][1]['n_obs'], cols1to3[1][1]['n_obs'], cols1to3[2][1]['n_obs'],
          cols4to6[0][1]['n_obs'], cols4to6[1][1]['n_obs'], cols4to6[2][1]['n_obs']]
    print("{:<20} {:>12} {:>12} {:>12} {:>12} {:>12} {:>12}".format(
        'N', *ns))

    # N clusters
    ncs = [cols1to3[0][1]['n_clusters'], cols1to3[1][1]['n_clusters'], cols1to3[2][1]['n_clusters'],
           cols4to6[0][1]['n_clusters'], cols4to6[1][1]['n_clusters'], cols4to6[2][1]['n_clusters']]
    print("{:<20} {:>12} {:>12} {:>12} {:>12} {:>12} {:>12}".format(
        'Counties', *ncs))

    print("{:<20} {:>12} {:>12} {:>12} {:>12} {:>12} {:>12}".format(
        'County FE', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'))
    print("{:<20} {:>12} {:>12} {:>12} {:>12} {:>12} {:>12}".format(
        'State×Year FE', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'))
    print("{:<20} {:>12} {:>12} {:>12} {:>12} {:>12} {:>12}".format(
        'County Trends', 'No', 'Linear', 'Quad', 'No', 'Linear', 'Quad'))

    # Save to CSV
    table3_data = {
        'Specification': ['Basic', 'Linear Trends', 'Quadratic Trends'],
        'Turnout_Coef': [cols1to3[i][1]['coef'] for i in range(3)],
        'Turnout_SE': [cols1to3[i][1]['se'] for i in range(3)],
        'Turnout_N': [cols1to3[i][1]['n_obs'] for i in range(3)],
        'VBM_Share_Coef': [cols4to6[i][1]['coef'] for i in range(3)],
        'VBM_Share_SE': [cols4to6[i][1]['se'] for i in range(3)],
        'VBM_Share_N': [cols4to6[i][1]['n_obs'] for i in range(3)]
    }
    pd.DataFrame(table3_data).to_csv('output/tables/table3_replication.csv', index=False)


def main():
    """Main replication function"""

    print("\n" + "="*70)
    print("REPLICATION OF THOMPSON ET AL. (2020)")
    print("Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share")
    print("="*70)

    # Load data
    print("\nLoading data...")
    df = pd.read_stata('original/data/modified/analysis.dta')
    print(f"Loaded {len(df)} observations")

    # Run replications
    t2_cols1to3 = replicate_table2_col1to3(df)
    t2_cols4to6 = replicate_table2_col4to6(df)
    t3_cols1to3 = replicate_table3_col1to3(df)
    t3_cols4to6 = replicate_table3_col4to6(df)

    # Create summary comparison table
    print("\n\n" + "="*70)
    print("REPLICATION COMPARISON")
    print("="*70)

    # Original values from paper
    original = {
        'Table 2 - Dem Turnout Share': {
            'Basic': (0.007, 0.003),
            'Linear': (0.001, 0.001),
            'Quadratic': (0.001, 0.001)
        },
        'Table 2 - Dem Vote Share': {
            'Basic': (0.028, 0.011),
            'Linear': (0.011, 0.004),
            'Quadratic': (0.007, 0.003)
        },
        'Table 3 - Turnout': {
            'Basic': (0.021, 0.009),
            'Linear': (0.022, 0.007),
            'Quadratic': (0.021, 0.008)
        },
        'Table 3 - VBM Share': {
            'Basic': (0.186, 0.027),
            'Linear': (0.157, 0.035),
            'Quadratic': (0.136, 0.085)
        }
    }

    replicated = {
        'Table 2 - Dem Turnout Share': t2_cols1to3,
        'Table 2 - Dem Vote Share': t2_cols4to6,
        'Table 3 - Turnout': t3_cols1to3,
        'Table 3 - VBM Share': t3_cols4to6
    }

    print("\n{:<30} {:<12} {:<18} {:<18} {:<12}".format(
        'Outcome', 'Spec', 'Original', 'Replicated', 'Diff'))
    print("-" * 90)

    comparison_data = []

    for outcome in original.keys():
        for i, (spec, res) in enumerate(replicated[outcome]):
            orig_coef, orig_se = original[outcome][spec]
            repl_coef = res['coef']
            repl_se = res['se']
            diff = repl_coef - orig_coef
            pct_diff = (diff / orig_coef * 100) if orig_coef != 0 else np.nan

            print("{:<30} {:<12} {:<18} {:<18} {:<12}".format(
                outcome if i == 0 else '',
                spec,
                f"{orig_coef:.3f} ({orig_se:.3f})",
                f"{repl_coef:.3f} ({repl_se:.3f})",
                f"{diff:+.4f}"
            ))

            comparison_data.append({
                'Outcome': outcome,
                'Specification': spec,
                'Original_Coef': orig_coef,
                'Original_SE': orig_se,
                'Replicated_Coef': repl_coef,
                'Replicated_SE': repl_se,
                'Difference': diff,
                'Pct_Difference': pct_diff,
                'N': res['n_obs'],
                'N_Clusters': res['n_clusters']
            })

    # Save results
    comparison_df = pd.DataFrame(comparison_data)
    comparison_df.to_csv('output/tables/replication_comparison.csv', index=False)
    print(f"\nResults saved to output/tables/replication_comparison.csv")

    # Create formatted tables
    create_table2_replication(t2_cols1to3, t2_cols4to6)
    create_table3_replication(t3_cols1to3, t3_cols4to6)

    return comparison_df


if __name__ == '__main__':
    comparison = main()
