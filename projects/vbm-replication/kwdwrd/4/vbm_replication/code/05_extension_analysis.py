"""
05_extension_analysis.py

Extension analysis for Thompson et al. (2020) replication.
Tests whether null partisan effects hold in the post-COVID era (2020-2024).

Analyses:
1. Main results with extended data (1996-2024)
2. Heterogeneous effects by period (pre vs post 2018)
3. Separate estimates by period
4. California-specific analysis
5. Event study specification
6. Robustness checks
"""

import pandas as pd
import numpy as np
from pathlib import Path
import statsmodels.api as sm
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Set paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "output" / "tables"
FIGURE_DIR = PROJECT_ROOT / "output" / "figures"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    """Load the combined analysis dataset."""
    df = pd.read_csv(DATA_DIR / "full_analysis_data.csv")
    print(f"Loaded {len(df)} observations")
    return df


def run_twfe_regression(df, y_var, treat_var='treat', county_var='county_id',
                        state_year_var='state_year', cluster_var='county_id',
                        trend_type='none', additional_controls=None):
    """
    Run two-way fixed effects regression with optional county trends.
    Same implementation as replication script.
    """
    # Select relevant columns and drop missing
    cols_needed = list(set([y_var, treat_var, county_var, state_year_var, cluster_var, 'year']))
    if additional_controls:
        cols_needed.extend(additional_controls)
    cols_needed = list(set(cols_needed))

    sample = df[cols_needed].dropna().copy().reset_index(drop=True)

    if len(sample) < 10:
        return None

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
        year_centered = sample['year'] - sample['year'].mean()

        if trend_type == 'linear':
            sample['y_dm2'] = y_dm2
            sample['treat_dm2'] = treat_dm2
            sample['year_c'] = year_centered

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

                try:
                    model_y = sm.OLS(county_data['y_dm2'], X).fit()
                    y_resid.extend(model_y.resid.tolist())
                except:
                    y_resid.extend(county_data['y_dm2'].tolist())

                try:
                    model_t = sm.OLS(county_data['treat_dm2'], X).fit()
                    treat_resid.extend(model_t.resid.tolist())
                except:
                    treat_resid.extend(county_data['treat_dm2'].tolist())

            y_final = pd.Series(y_resid, index=sample.index)
            x_final = pd.Series(treat_resid, index=sample.index)

        elif trend_type == 'quadratic':
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

                try:
                    model_y = sm.OLS(county_data['y_dm2'], X).fit()
                    y_resid.extend(model_y.resid.tolist())
                except:
                    y_resid.extend(county_data['y_dm2'].tolist())

                try:
                    model_t = sm.OLS(county_data['treat_dm2'], X).fit()
                    treat_resid.extend(model_t.resid.tolist())
                except:
                    treat_resid.extend(county_data['treat_dm2'].tolist())

            y_final = pd.Series(y_resid, index=sample.index)
            x_final = pd.Series(treat_resid, index=sample.index)

    # Final regression
    X = sm.add_constant(x_final)
    model = sm.OLS(y_final, X, missing='drop')

    clusters = sample[cluster_var]
    results = model.fit(cov_type='cluster', cov_kwds={'groups': clusters})

    coef = results.params.iloc[1]
    se = results.bse.iloc[1]
    pval = results.pvalues.iloc[1]

    return {
        'coef': coef,
        'se': se,
        'pval': pval,
        'n_obs': int(results.nobs),
        'n_clusters': clusters.nunique(),
        'ci_low': coef - 1.96 * se,
        'ci_high': coef + 1.96 * se
    }


def run_interaction_regression(df, y_var, treat_var='treat', interact_var='post_2018',
                               county_var='county_id', state_year_var='state_year',
                               cluster_var='county_id'):
    """
    Run regression with interaction term to test for heterogeneous effects.
    Y = β1*treat + β2*treat*post_2018 + β3*post_2018 + county_FE + state_year_FE
    """
    cols_needed = list(set([y_var, treat_var, interact_var, county_var, state_year_var, cluster_var, 'year']))
    sample = df[cols_needed].dropna().copy().reset_index(drop=True)

    if len(sample) < 10:
        return None

    # Create interaction term
    sample['treat_x_post'] = sample[treat_var] * sample[interact_var]

    # Demean all variables by county and state-year
    for var in [y_var, treat_var, interact_var, 'treat_x_post']:
        sample[f'{var}_county_dm'] = sample[var] - sample.groupby(county_var)[var].transform('mean')
        sample[f'{var}_dm'] = sample[f'{var}_county_dm'] - sample.groupby(state_year_var)[f'{var}_county_dm'].transform('mean')

    # Regression
    y = sample[f'{y_var}_dm']
    X = sample[[f'{treat_var}_dm', 'treat_x_post_dm']]
    X = sm.add_constant(X)

    model = sm.OLS(y, X, missing='drop')
    clusters = sample[cluster_var]
    results = model.fit(cov_type='cluster', cov_kwds={'groups': clusters})

    return {
        'treat_coef': results.params[f'{treat_var}_dm'],
        'treat_se': results.bse[f'{treat_var}_dm'],
        'treat_pval': results.pvalues[f'{treat_var}_dm'],
        'interact_coef': results.params['treat_x_post_dm'],
        'interact_se': results.bse['treat_x_post_dm'],
        'interact_pval': results.pvalues['treat_x_post_dm'],
        'n_obs': int(results.nobs),
        'n_clusters': clusters.nunique()
    }


def reshape_to_vote_share_panel(df):
    """Reshape data to have one row per county-year-office for vote share analysis."""
    rows = []
    for idx, row in df.iterrows():
        for office, var in [('pres', 'dem_share_pres'), ('gov', 'dem_share_gov'), ('sen', 'dem_share_sen')]:
            if pd.notna(row.get(var)):
                rows.append({
                    'state': row['state'],
                    'county': row['county'],
                    'year': row['year'],
                    'county_id': row['county_id'],
                    'state_year': row['state_year'],
                    'treat': row['treat'],
                    'post_2018': row['post_2018'],
                    'office': office,
                    'dem_share': row[var]
                })
    return pd.DataFrame(rows)


def main_results_extended(df):
    """
    Task 5.1: Main results with extended data (1996-2024).
    Replicate Table 2 and Table 3 specifications with full sample.
    """
    print("\n" + "=" * 60)
    print("TASK 5.1: MAIN RESULTS WITH EXTENDED DATA (1996-2024)")
    print("=" * 60)

    results = []

    # Democratic Vote Share (equivalent to Table 2, Cols 4-6)
    print("\nDemocratic Vote Share (all states, office-level)")
    print("-" * 50)

    vote_share_df = reshape_to_vote_share_panel(df)
    print(f"Sample: {len(vote_share_df)} obs, {vote_share_df['county_id'].nunique()} counties")

    for spec, trend in [('Basic', 'none'), ('Linear', 'linear'), ('Quadratic', 'quadratic')]:
        result = run_twfe_regression(
            vote_share_df,
            y_var='dem_share',
            trend_type=trend
        )
        if result:
            results.append({
                'Outcome': 'Dem Vote Share',
                'Sample': 'Full (1996-2024)',
                'Specification': spec,
                'Coef': result['coef'],
                'SE': result['se'],
                'CI_Low': result['ci_low'],
                'CI_High': result['ci_high'],
                'N_Obs': result['n_obs'],
                'N_Counties': result['n_clusters']
            })
            print(f"  {spec:10s}: coef = {result['coef']:.4f} ({result['se']:.4f}), n = {result['n_obs']}")

    # Turnout (equivalent to Table 3, Cols 1-3)
    print("\nTurnout (all states)")
    print("-" * 50)

    turnout_df = df[df['turnout_share'].notna()].copy()
    print(f"Sample: {len(turnout_df)} obs, {turnout_df['county_id'].nunique()} counties")

    for spec, trend in [('Basic', 'none'), ('Linear', 'linear'), ('Quadratic', 'quadratic')]:
        result = run_twfe_regression(
            turnout_df,
            y_var='turnout_share',
            trend_type=trend
        )
        if result:
            results.append({
                'Outcome': 'Turnout',
                'Sample': 'Full (1996-2024)',
                'Specification': spec,
                'Coef': result['coef'],
                'SE': result['se'],
                'CI_Low': result['ci_low'],
                'CI_High': result['ci_high'],
                'N_Obs': result['n_obs'],
                'N_Counties': result['n_clusters']
            })
            print(f"  {spec:10s}: coef = {result['coef']:.4f} ({result['se']:.4f}), n = {result['n_obs']}")

    return pd.DataFrame(results)


def heterogeneity_by_period(df):
    """
    Task 5.2: Test for heterogeneous effects by period.
    Estimate: Y = β1*treat + β2*treat×post_2018 + FE
    """
    print("\n" + "=" * 60)
    print("TASK 5.2: HETEROGENEOUS EFFECTS BY PERIOD")
    print("=" * 60)

    results = []

    # Democratic Vote Share
    print("\nDemocratic Vote Share - Interaction Model")
    print("-" * 50)

    vote_share_df = reshape_to_vote_share_panel(df)
    result = run_interaction_regression(vote_share_df, y_var='dem_share')

    if result:
        results.append({
            'Outcome': 'Dem Vote Share',
            'Treat_Coef': result['treat_coef'],
            'Treat_SE': result['treat_se'],
            'Interact_Coef': result['interact_coef'],
            'Interact_SE': result['interact_se'],
            'Interact_Pval': result['interact_pval'],
            'N_Obs': result['n_obs']
        })
        print(f"  Main effect (treat):      {result['treat_coef']:.4f} ({result['treat_se']:.4f})")
        print(f"  Interaction (treat×post): {result['interact_coef']:.4f} ({result['interact_se']:.4f}), p={result['interact_pval']:.3f}")

    # Turnout
    print("\nTurnout - Interaction Model")
    print("-" * 50)

    turnout_df = df[df['turnout_share'].notna()].copy()
    result = run_interaction_regression(turnout_df, y_var='turnout_share')

    if result:
        results.append({
            'Outcome': 'Turnout',
            'Treat_Coef': result['treat_coef'],
            'Treat_SE': result['treat_se'],
            'Interact_Coef': result['interact_coef'],
            'Interact_SE': result['interact_se'],
            'Interact_Pval': result['interact_pval'],
            'N_Obs': result['n_obs']
        })
        print(f"  Main effect (treat):      {result['treat_coef']:.4f} ({result['treat_se']:.4f})")
        print(f"  Interaction (treat×post): {result['interact_coef']:.4f} ({result['interact_se']:.4f}), p={result['interact_pval']:.3f}")

    return pd.DataFrame(results)


def separate_by_period(df):
    """
    Task 5.3: Separate estimates by period.
    """
    print("\n" + "=" * 60)
    print("TASK 5.3: SEPARATE ESTIMATES BY PERIOD")
    print("=" * 60)

    results = []

    for period_name, period_val in [('Original (1996-2018)', 0), ('Extension (2020-2024)', 1)]:
        print(f"\n{period_name}")
        print("-" * 50)

        period_df = df[df['post_2018'] == period_val].copy()

        # Democratic Vote Share
        vote_share_df = reshape_to_vote_share_panel(period_df)
        if len(vote_share_df) > 0:
            result = run_twfe_regression(vote_share_df, y_var='dem_share', trend_type='linear')
            if result:
                results.append({
                    'Outcome': 'Dem Vote Share',
                    'Period': period_name,
                    'Coef': result['coef'],
                    'SE': result['se'],
                    'CI_Low': result['ci_low'],
                    'CI_High': result['ci_high'],
                    'N_Obs': result['n_obs']
                })
                print(f"  Dem Vote Share: {result['coef']:.4f} ({result['se']:.4f}), n={result['n_obs']}")

        # Turnout
        turnout_df = period_df[period_df['turnout_share'].notna()].copy()
        if len(turnout_df) > 0:
            result = run_twfe_regression(turnout_df, y_var='turnout_share', trend_type='linear')
            if result:
                results.append({
                    'Outcome': 'Turnout',
                    'Period': period_name,
                    'Coef': result['coef'],
                    'SE': result['se'],
                    'CI_Low': result['ci_low'],
                    'CI_High': result['ci_high'],
                    'N_Obs': result['n_obs']
                })
                print(f"  Turnout:        {result['coef']:.4f} ({result['se']:.4f}), n={result['n_obs']}")

    return pd.DataFrame(results)


def california_analysis(df):
    """
    Task 5.4: California-specific analysis.
    Focus on California where most new variation exists.
    """
    print("\n" + "=" * 60)
    print("TASK 5.4: CALIFORNIA-SPECIFIC ANALYSIS")
    print("=" * 60)

    ca_df = df[df['state'] == 'CA'].copy()
    print(f"California sample: {len(ca_df)} observations")

    results = []

    # Full CA sample
    print("\nCalifornia Full Sample (1998-2024)")
    print("-" * 50)

    for outcome, y_var in [('Dem Vote Share (Pres)', 'dem_share_pres'),
                           ('Dem Vote Share (Gov)', 'dem_share_gov'),
                           ('Turnout', 'turnout_share')]:
        sample = ca_df[ca_df[y_var].notna()].copy()
        if len(sample) > 10:
            result = run_twfe_regression(sample, y_var=y_var, trend_type='linear')
            if result:
                results.append({
                    'Analysis': 'CA Full',
                    'Outcome': outcome,
                    'Coef': result['coef'],
                    'SE': result['se'],
                    'N_Obs': result['n_obs']
                })
                print(f"  {outcome:25s}: {result['coef']:.4f} ({result['se']:.4f}), n={result['n_obs']}")

    # CA 2018-2024 only (VCA period)
    print("\nCalifornia VCA Period (2018-2024)")
    print("-" * 50)

    ca_vca = ca_df[ca_df['year'] >= 2018].copy()
    print(f"VCA period sample: {len(ca_vca)} observations")

    for outcome, y_var in [('Dem Vote Share (Pres)', 'dem_share_pres'),
                           ('Dem Vote Share (Gov)', 'dem_share_gov'),
                           ('Turnout', 'turnout_share')]:
        sample = ca_vca[ca_vca[y_var].notna()].copy()
        if len(sample) > 10:
            result = run_twfe_regression(sample, y_var=y_var, trend_type='none')
            if result:
                results.append({
                    'Analysis': 'CA VCA Period',
                    'Outcome': outcome,
                    'Coef': result['coef'],
                    'SE': result['se'],
                    'N_Obs': result['n_obs']
                })
                print(f"  {outcome:25s}: {result['coef']:.4f} ({result['se']:.4f}), n={result['n_obs']}")

    return pd.DataFrame(results)


def event_study(df):
    """
    Task 5.5: Event study specification for California.
    Estimate effects by year relative to VCA adoption.
    """
    print("\n" + "=" * 60)
    print("TASK 5.5: EVENT STUDY (CALIFORNIA)")
    print("=" * 60)

    # Load VCA adoption data
    vca = pd.read_csv(PROJECT_ROOT / "data" / "extension" / "california_vbm_adoption.csv")

    # Merge adoption year with CA data
    ca_df = df[df['state'] == 'CA'].copy()
    ca_df = ca_df.merge(vca[['county', 'vca_first_year']], on='county', how='left')

    # Create relative time variable
    ca_df['rel_time'] = ca_df['year'] - ca_df['vca_first_year']

    # Only include counties that adopted VCA during study period
    ca_df = ca_df[ca_df['vca_first_year'] < 9999].copy()
    print(f"Sample: {ca_df['county'].nunique()} VCA counties")

    # Bin relative time
    ca_df['rel_time_binned'] = ca_df['rel_time'].clip(-10, 6)

    # Create event time dummies (omit -2 as reference)
    event_times = sorted(ca_df['rel_time_binned'].unique())
    event_times = [t for t in event_times if t != -2]  # Omit reference period

    results = []

    for outcome, y_var in [('Dem Vote Share (Pres)', 'dem_share_pres'), ('Turnout', 'turnout_share')]:
        sample = ca_df[ca_df[y_var].notna()].copy()

        if len(sample) < 20:
            continue

        # Create event time dummies
        for t in event_times:
            sample[f'event_{t}'] = (sample['rel_time_binned'] == t).astype(int)

        # Demean outcome by county and state-year
        sample['y_county_dm'] = sample[y_var] - sample.groupby('county_id')[y_var].transform('mean')
        sample['y_dm'] = sample['y_county_dm'] - sample.groupby('state_year')['y_county_dm'].transform('mean')

        # Demean event dummies
        for t in event_times:
            sample[f'event_{t}_county_dm'] = sample[f'event_{t}'] - sample.groupby('county_id')[f'event_{t}'].transform('mean')
            sample[f'event_{t}_dm'] = sample[f'event_{t}_county_dm'] - sample.groupby('state_year')[f'event_{t}_county_dm'].transform('mean')

        # Regression
        event_cols = [f'event_{t}_dm' for t in event_times]
        X = sample[event_cols]
        X = sm.add_constant(X)
        y = sample['y_dm']

        try:
            model = sm.OLS(y, X, missing='drop').fit(cov_type='cluster', cov_kwds={'groups': sample['county_id']})

            for t in event_times:
                col = f'event_{t}_dm'
                if col in model.params.index:
                    results.append({
                        'Outcome': outcome,
                        'Rel_Time': t,
                        'Coef': model.params[col],
                        'SE': model.bse[col],
                        'CI_Low': model.params[col] - 1.96 * model.bse[col],
                        'CI_High': model.params[col] + 1.96 * model.bse[col]
                    })
        except Exception as e:
            print(f"  Error estimating event study for {outcome}: {e}")

    results_df = pd.DataFrame(results)

    # Print results
    if len(results_df) > 0:
        print("\nEvent Study Coefficients:")
        print("-" * 50)
        for outcome in results_df['Outcome'].unique():
            print(f"\n{outcome}:")
            outcome_df = results_df[results_df['Outcome'] == outcome].sort_values('Rel_Time')
            for _, row in outcome_df.iterrows():
                marker = "*" if row['Rel_Time'] >= 0 else " "
                print(f"  t={int(row['Rel_Time']):+3d}: {row['Coef']:+.4f} ({row['SE']:.4f}) {marker}")

        # Create event study plot
        create_event_study_plot(results_df)

    return results_df


def create_event_study_plot(results_df):
    """Create event study figure."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for i, outcome in enumerate(['Dem Vote Share (Pres)', 'Turnout']):
        ax = axes[i]
        outcome_df = results_df[results_df['Outcome'] == outcome].sort_values('Rel_Time')

        if len(outcome_df) == 0:
            continue

        # Plot coefficients with confidence intervals
        ax.errorbar(outcome_df['Rel_Time'], outcome_df['Coef'],
                    yerr=1.96 * outcome_df['SE'],
                    fmt='o', capsize=3, capthick=1, color='navy')

        # Reference lines
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax.axvline(x=-0.5, color='red', linestyle='--', linewidth=1, alpha=0.7)

        ax.set_xlabel('Years Relative to VCA Adoption')
        ax.set_ylabel('Effect on ' + outcome)
        ax.set_title(f'Event Study: {outcome}')

        # Shade pre-treatment period
        ax.axvspan(ax.get_xlim()[0], -0.5, alpha=0.1, color='gray')

    plt.tight_layout()
    plt.savefig(FIGURE_DIR / 'event_study.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\nSaved event study figure to {FIGURE_DIR / 'event_study.png'}")


def robustness_checks(df):
    """
    Task 5.6: Robustness checks.
    """
    print("\n" + "=" * 60)
    print("TASK 5.6: ROBUSTNESS CHECKS")
    print("=" * 60)

    results = []

    # 1. Dropping 2020 (COVID year)
    print("\n1. Dropping 2020 (COVID election year)")
    print("-" * 50)

    df_no2020 = df[df['year'] != 2020].copy()
    vote_share_df = reshape_to_vote_share_panel(df_no2020)

    result = run_twfe_regression(vote_share_df, y_var='dem_share', trend_type='linear')
    if result:
        results.append({
            'Check': 'Dropping 2020',
            'Outcome': 'Dem Vote Share',
            'Coef': result['coef'],
            'SE': result['se'],
            'N_Obs': result['n_obs']
        })
        print(f"  Dem Vote Share: {result['coef']:.4f} ({result['se']:.4f})")

    turnout_df = df_no2020[df_no2020['turnout_share'].notna()].copy()
    result = run_twfe_regression(turnout_df, y_var='turnout_share', trend_type='linear')
    if result:
        results.append({
            'Check': 'Dropping 2020',
            'Outcome': 'Turnout',
            'Coef': result['coef'],
            'SE': result['se'],
            'N_Obs': result['n_obs']
        })
        print(f"  Turnout:        {result['coef']:.4f} ({result['se']:.4f})")

    # 2. Presidential elections only
    print("\n2. Presidential elections only")
    print("-" * 50)

    pres_df = df[df['dem_share_pres'].notna()].copy()
    result = run_twfe_regression(pres_df, y_var='dem_share_pres', trend_type='linear')
    if result:
        results.append({
            'Check': 'Presidential Only',
            'Outcome': 'Dem Vote Share (Pres)',
            'Coef': result['coef'],
            'SE': result['se'],
            'N_Obs': result['n_obs']
        })
        print(f"  Dem Vote Share (Pres): {result['coef']:.4f} ({result['se']:.4f})")

    # 3. California only (where variation exists)
    print("\n3. California only")
    print("-" * 50)

    ca_df = df[df['state'] == 'CA'].copy()
    ca_pres = ca_df[ca_df['dem_share_pres'].notna()].copy()
    result = run_twfe_regression(ca_pres, y_var='dem_share_pres', trend_type='linear')
    if result:
        results.append({
            'Check': 'California Only',
            'Outcome': 'Dem Vote Share (Pres)',
            'Coef': result['coef'],
            'SE': result['se'],
            'N_Obs': result['n_obs']
        })
        print(f"  Dem Vote Share (Pres): {result['coef']:.4f} ({result['se']:.4f})")

    ca_turnout = ca_df[ca_df['turnout_share'].notna()].copy()
    result = run_twfe_regression(ca_turnout, y_var='turnout_share', trend_type='linear')
    if result:
        results.append({
            'Check': 'California Only',
            'Outcome': 'Turnout',
            'Coef': result['coef'],
            'SE': result['se'],
            'N_Obs': result['n_obs']
        })
        print(f"  Turnout:               {result['coef']:.4f} ({result['se']:.4f})")

    return pd.DataFrame(results)


def main():
    print("=" * 60)
    print("EXTENSION ANALYSIS: THOMPSON ET AL. (2020)")
    print("Testing VBM Effects in Post-COVID Era (2020-2024)")
    print("=" * 60)

    # Load data
    df = load_data()

    # Run all analyses
    main_results = main_results_extended(df)
    heterogeneity = heterogeneity_by_period(df)
    period_results = separate_by_period(df)
    ca_results = california_analysis(df)
    event_results = event_study(df)
    robustness = robustness_checks(df)

    # Save all results
    print("\n" + "=" * 60)
    print("SAVING RESULTS")
    print("=" * 60)

    main_results.to_csv(OUTPUT_DIR / 'extension_main_results.csv', index=False)
    heterogeneity.to_csv(OUTPUT_DIR / 'extension_heterogeneity.csv', index=False)
    period_results.to_csv(OUTPUT_DIR / 'extension_by_period.csv', index=False)
    ca_results.to_csv(OUTPUT_DIR / 'extension_california.csv', index=False)
    if len(event_results) > 0:
        event_results.to_csv(OUTPUT_DIR / 'extension_event_study.csv', index=False)
    robustness.to_csv(OUTPUT_DIR / 'extension_robustness.csv', index=False)

    print("\nResults saved to output/tables/:")
    print("  - extension_main_results.csv")
    print("  - extension_heterogeneity.csv")
    print("  - extension_by_period.csv")
    print("  - extension_california.csv")
    print("  - extension_event_study.csv")
    print("  - extension_robustness.csv")

    print("\nFigures saved to output/figures/:")
    print("  - event_study.png")

    # Summary
    print("\n" + "=" * 60)
    print("KEY FINDINGS SUMMARY")
    print("=" * 60)

    print("\n1. MAIN RESULTS (Full Sample 1996-2024):")
    for _, row in main_results[main_results['Specification'] == 'Linear'].iterrows():
        sig = "*" if abs(row['Coef']) > 1.96 * row['SE'] else ""
        print(f"   {row['Outcome']}: {row['Coef']:.4f} ({row['SE']:.4f}){sig}")

    print("\n2. PERIOD HETEROGENEITY:")
    for _, row in heterogeneity.iterrows():
        sig = "*" if row['Interact_Pval'] < 0.05 else ""
        print(f"   {row['Outcome']}: interaction = {row['Interact_Coef']:.4f} ({row['Interact_SE']:.4f}){sig}")

    print("\n3. SEPARATE BY PERIOD:")
    for _, row in period_results.iterrows():
        sig = "*" if abs(row['Coef']) > 1.96 * row['SE'] else ""
        print(f"   {row['Period']}, {row['Outcome']}: {row['Coef']:.4f} ({row['SE']:.4f}){sig}")


if __name__ == "__main__":
    main()
