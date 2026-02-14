"""
Create figures for VBM extension paper
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 13

# Load data
california = pd.read_csv('../data/california_analysis.csv')
combined = pd.read_csv('../data/combined_analysis.csv')

# Create output directory
import os
os.makedirs('../paper/figures', exist_ok=True)

# ============================================================
# FIGURE 1: VCA Adoption Timeline
# ============================================================

fig, ax = plt.subplots(figsize=(8, 5))

years = [2018, 2020, 2022, 2024]
cumulative = [5, 15, 27, 29]
pct = [c/58*100 for c in cumulative]

bars = ax.bar(years, cumulative, color='steelblue', edgecolor='black', linewidth=0.5)

# Add percentage labels
for bar, p in zip(bars, pct):
    ax.annotate(f'{p:.1f}%',
                xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                xytext=(0, 5),
                textcoords='offset points',
                ha='center', va='bottom',
                fontsize=10)

ax.set_xlabel('Year')
ax.set_ylabel('Number of VCA Counties')
ax.set_title('California Voter\'s Choice Act Adoption')
ax.set_xticks(years)
ax.set_ylim(0, 35)
ax.axhline(y=58, color='red', linestyle='--', alpha=0.5, label='Total CA Counties (58)')
ax.legend(loc='upper left')

plt.tight_layout()
plt.savefig('../paper/figures/fig1_vca_adoption.png', dpi=300, bbox_inches='tight')
plt.savefig('../paper/figures/fig1_vca_adoption.pdf', bbox_inches='tight')
plt.close()

print("Created Figure 1: VCA Adoption Timeline")

# ============================================================
# FIGURE 2: Treatment Status Over Time
# ============================================================

fig, ax = plt.subplots(figsize=(10, 6))

# Calculate treatment rate by state and year
treat_by_state_year = combined.groupby(['state', 'year'])['treat'].mean().unstack(level=0)

# Plot
colors = {'CA': 'steelblue', 'UT': 'forestgreen', 'WA': 'darkorange'}
for state in ['CA', 'UT', 'WA']:
    if state in treat_by_state_year.columns:
        data = treat_by_state_year[state].dropna()
        ax.plot(data.index, data.values * 100, 'o-', label=state,
                color=colors[state], linewidth=2, markersize=6)

ax.set_xlabel('Year')
ax.set_ylabel('Percent of Counties with Universal VBM')
ax.set_title('Universal Vote-by-Mail Adoption Over Time')
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.legend(title='State')
ax.set_ylim(-5, 105)

plt.tight_layout()
plt.savefig('../paper/figures/fig2_treatment_over_time.png', dpi=300, bbox_inches='tight')
plt.savefig('../paper/figures/fig2_treatment_over_time.pdf', bbox_inches='tight')
plt.close()

print("Created Figure 2: Treatment Status Over Time")

# ============================================================
# FIGURE 3: Turnout by VCA Status (California 2020-2024)
# ============================================================

fig, ax = plt.subplots(figsize=(8, 5))

ca_ext = california[california['year'] >= 2020].copy()

# Calculate mean turnout by year and treatment
turnout_by_year_treat = ca_ext.groupby(['year', 'treat'])['turnout_share'].mean().unstack()

x = np.arange(len([2020, 2022, 2024]))
width = 0.35

bars1 = ax.bar(x - width/2, turnout_by_year_treat[0] * 100, width,
               label='Non-VCA Counties', color='lightcoral', edgecolor='black', linewidth=0.5)
bars2 = ax.bar(x + width/2, turnout_by_year_treat[1] * 100, width,
               label='VCA Counties', color='steelblue', edgecolor='black', linewidth=0.5)

ax.set_xlabel('Year')
ax.set_ylabel('Turnout (%)')
ax.set_title('Voter Turnout by VCA Status (California)')
ax.set_xticks(x)
ax.set_xticklabels([2020, 2022, 2024])
ax.legend()
ax.set_ylim(0, 80)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())

# Add difference annotations
for i, year in enumerate([2020, 2022, 2024]):
    diff = (turnout_by_year_treat[1].loc[year] - turnout_by_year_treat[0].loc[year]) * 100
    ax.annotate(f'+{diff:.1f}pp',
                xy=(i, max(turnout_by_year_treat[0].loc[year], turnout_by_year_treat[1].loc[year]) * 100 + 2),
                ha='center', fontsize=9, color='darkgreen')

plt.tight_layout()
plt.savefig('../paper/figures/fig3_turnout_by_vca.png', dpi=300, bbox_inches='tight')
plt.savefig('../paper/figures/fig3_turnout_by_vca.pdf', bbox_inches='tight')
plt.close()

print("Created Figure 3: Turnout by VCA Status")

# ============================================================
# FIGURE 4: Coefficient Comparison (Original vs Extension)
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Panel A: Partisan Effects
ax = axes[0]
outcomes = ['Dem Share\n(Pres)', 'Dem Share\n(Gov)', 'Dem Share\n(Sen)']
original = [0.0012, 0.0039, 0.0067]
original_se = [0.0023, 0.0039, 0.0055]
extension = [0.0192, 0.0316, 0.0343]
extension_se = [0.0067, 0.0084, 0.0126]

x = np.arange(len(outcomes))
width = 0.35

ax.bar(x - width/2, [o*100 for o in original], width, yerr=[s*100*1.96 for s in original_se],
       label='Original (1996-2018)', color='steelblue', capsize=3)
ax.bar(x + width/2, [e*100 for e in extension], width, yerr=[s*100*1.96 for s in extension_se],
       label='Extension (1996-2024)', color='darkorange', capsize=3)

ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax.set_ylabel('Effect on Democratic Vote Share (pp)')
ax.set_title('Panel A: Partisan Effects')
ax.set_xticks(x)
ax.set_xticklabels(outcomes)
ax.legend()
ax.set_ylim(-1, 6)

# Panel B: Turnout Effects
ax = axes[1]
outcomes = ['Turnout']
original = [0.0201]
original_se = [0.0046]
extension = [0.0197]
extension_se = [0.0060]

x = np.arange(len(outcomes))
width = 0.35

ax.bar(x - width/2, [o*100 for o in original], width, yerr=[s*100*1.96 for s in original_se],
       label='Original (1996-2018)', color='steelblue', capsize=3)
ax.bar(x + width/2, [e*100 for e in extension], width, yerr=[s*100*1.96 for s in extension_se],
       label='Extension (1996-2024)', color='darkorange', capsize=3)

ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax.set_ylabel('Effect on Turnout (pp)')
ax.set_title('Panel B: Turnout Effects')
ax.set_xticks(x)
ax.set_xticklabels(outcomes)
ax.legend()
ax.set_ylim(0, 4)

plt.tight_layout()
plt.savefig('../paper/figures/fig4_coefficient_comparison.png', dpi=300, bbox_inches='tight')
plt.savefig('../paper/figures/fig4_coefficient_comparison.pdf', bbox_inches='tight')
plt.close()

print("Created Figure 4: Coefficient Comparison")

# ============================================================
# FIGURE 5: Turnout Trends by State
# ============================================================

fig, ax = plt.subplots(figsize=(10, 6))

# Calculate mean turnout by state and year (presidential years only)
pres_years = combined[combined['pres'] == 1].copy()
turnout_by_state_year = pres_years.groupby(['state', 'year'])['turnout_share'].mean().unstack(level=0)

colors = {'CA': 'steelblue', 'UT': 'forestgreen', 'WA': 'darkorange'}
for state in ['CA', 'UT', 'WA']:
    if state in turnout_by_state_year.columns:
        data = turnout_by_state_year[state].dropna()
        ax.plot(data.index, data.values * 100, 'o-', label=state,
                color=colors[state], linewidth=2, markersize=6)

ax.set_xlabel('Year')
ax.set_ylabel('Average Turnout (%)')
ax.set_title('Voter Turnout in Presidential Elections by State')
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.legend(title='State')
ax.set_ylim(40, 80)

# Add vertical lines for key events
ax.axvline(x=2011, color='darkorange', linestyle=':', alpha=0.5)
ax.text(2011.2, 75, 'WA universal\nVBM', fontsize=8, color='darkorange')

ax.axvline(x=2018, color='steelblue', linestyle=':', alpha=0.5)
ax.text(2018.2, 75, 'CA VCA\nbegins', fontsize=8, color='steelblue')

plt.tight_layout()
plt.savefig('../paper/figures/fig5_turnout_trends.png', dpi=300, bbox_inches='tight')
plt.savefig('../paper/figures/fig5_turnout_trends.pdf', bbox_inches='tight')
plt.close()

print("Created Figure 5: Turnout Trends by State")

print("\nAll figures saved to paper/figures/")
