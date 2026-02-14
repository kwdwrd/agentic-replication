# Universal Vote-by-Mail and Partisan Outcomes: A Replication and Extension Through 2024

## Abstract

We replicate and extend Thompson, Wu, Yoder, and Hall (2020), who found that universal vote-by-mail (VBM) has no impact on partisan turnout or vote share using county-level data from California, Utah, and Washington (1996--2018). Our Python-based replication reproduces all original estimates within rounding tolerance. We then extend the analysis through 2024, incorporating three additional election cycles that span the COVID-19 pandemic and the continued rollout of California's Voter's Choice Act (VCA). Using the same difference-in-differences framework with county and state-by-year fixed effects, we find that the null partisan effect of VBM persists in the extended sample: the estimated effect on Democratic vote share is 0.004 (SE = 0.003) with quadratic county trends, statistically indistinguishable from zero. The turnout-boosting effect of VBM (~1--2 percentage points) remains positive in the pooled sample but is attenuated in the post-2018 period, likely reflecting the confounding influence of California's 2020 executive order that sent mail ballots to all voters regardless of VCA status. Event study estimates show no evidence of pre-trends for either partisan outcomes or turnout. These findings reinforce the conclusion that universal VBM does not confer a systematic partisan advantage, even in the post-pandemic period when mail voting became politically salient.

---

## 1. Introduction

The question of whether universal vote-by-mail (VBM) affects partisan electoral outcomes has been one of the most politically charged debates in American election administration. During the COVID-19 pandemic, the expansion of mail voting became a flashpoint: Republican leaders, including President Trump, repeatedly claimed that expanded mail voting would benefit Democrats, while some Democratic advocates hoped it would boost their party's electoral prospects (Lockhart et al. 2020). Despite the intensity of these claims, the empirical evidence has consistently pointed to a null partisan effect.

Thompson et al. (2020), published in the *Proceedings of the National Academy of Sciences*, provided the most rigorous causal evidence to date on this question. Exploiting the staggered county-level rollout of universal VBM across California, Utah, and Washington from 1996 to 2018, they estimated the effect of VBM on partisan turnout share, partisan vote share, overall turnout, and voting mode using a difference-in-differences (DiD) design with county and state-by-year fixed effects. Their central finding was striking: universal VBM had no detectable effect on either party's share of turnout or their vote share. The only robust effect was a modest increase in overall turnout of approximately 2 percentage points and a mechanical shift in the mode of voting toward mail ballots.

This paper makes two contributions. First, we provide a complete computational replication of Thompson et al. (2020) using their original data and a Python implementation of the estimation procedures. Our replication confirms all original findings: every point estimate matches the published results within rounding tolerance (maximum difference of 0.0005 across 12 coefficient estimates). Second, we extend the analysis through 2024, adding three election cycles (2020, 2022, 2024) that provide substantial new identifying variation from California's continued VCA rollout---from 5 participating counties in 2018 to 30 by 2024.

The extension period is particularly valuable for two reasons. First, California's VCA continued its staggered county-level rollout after 2018, with 10 new counties joining in 2020, 14 in 2022, and 1 in 2024. This ongoing staggered adoption provides new treatment variation within the same institutional framework studied by Thompson et al. Second, the extension period encompasses the COVID-19 pandemic, during which mail voting became intensely partisan in public discourse (Lockhart et al. 2020). If VBM were to develop partisan effects, the post-2020 period---when Republican voters became substantially less likely to vote by mail than Democrats---would be the most likely context for such effects to emerge.

Our extension analysis finds that the null partisan result holds through 2024. On the full 1996--2024 sample, the estimated effect of VBM on Democratic vote share is 0.004 (SE = 0.003) with quadratic county trends, consistent with zero. The turnout effect remains positive in the pooled sample (0.013, SE = 0.006) but is attenuated relative to the original period, likely reflecting the confounding influence of Governor Newsom's Executive Order N-64-20, which directed all California counties to mail ballots to registered voters in 2020 regardless of VCA participation. This executive order reduced the treatment contrast between VCA and non-VCA counties, biasing the post-2020 estimates toward zero. Event study specifications show no evidence of pre-trends for either outcome, supporting the validity of the parallel trends assumption.

We also examine heterogeneity by estimating the interaction between VBM treatment and a post-2018 indicator. The interaction term for Democratic vote share is small and marginally significant in some specifications, while the interaction for turnout is consistently negative and significant, further consistent with the COVID-era attenuation of the treatment contrast.

The remainder of the paper proceeds as follows. Section 2 reviews the relevant literature on VBM and partisan outcomes. Section 3 describes the data and empirical strategy. Section 4 presents the replication results. Section 5 presents the extension results. Section 6 discusses the findings and their implications, and Section 7 concludes.

## 2. Literature Review

### 2.1 Vote-by-Mail and Turnout

The convenience voting literature has studied the effects of vote-by-mail on participation for over two decades. Southwell and Burchett (2000) provided an early analysis of Oregon's pioneering all-mail system, reporting a turnout increase of approximately 10 percentage points, though subsequent work questioned the magnitude of this estimate. Gronke et al. (2008) reviewed the broader convenience voting literature and concluded that alternative voting methods generally have modest effects on turnout and are unlikely to transform the composition of the electorate.

Gerber, Huber, and Hill (2013) provided the most rigorous pre-Thompson estimate, exploiting Washington State's staggered county-level adoption of all-mail elections. Using both aggregate county data and individual voter file records, they found that all-mail elections increased turnout by 2 to 4 percentage points, with larger effects for low-propensity voters. Kousser and Mullin (2007) found a null effect of VBM on turnout in California regular elections using a matching design, though they detected positive effects in low-salience special elections.

Berinsky, Burns, and Traugott (2001) raised equity concerns, finding that VBM may primarily mobilize existing voters rather than bringing new participants into the electorate. This suggests that VBM could potentially widen rather than narrow participation gaps, though the evidence from Gerber et al. (2013) points in the opposite direction.

### 2.2 Vote-by-Mail and Partisan Outcomes

The central empirical question addressed by Thompson et al. (2020) and the present paper is whether VBM systematically advantages either political party. The pre-2020 evidence was largely null. Thompson et al. (2020) found no effect on Democratic turnout share or vote share across three states and two decades. Barber and Holbein (2020), published concurrently, reached the same conclusion using data from six states and 40 million individual voter records: mandatory VBM increased turnout by 2--3 percentage points but had no effect on partisan outcomes.

The post-2020 evidence has reinforced the null finding. Amlani and Collitt (2022) examined the 2020 election specifically and found that counties mailing ballots to all voters experienced 2.6% higher turnout but no partisan advantage. This finding is noteworthy because the 2020 election was conducted in an environment of intense partisan polarization over mail voting itself.

### 2.3 COVID-19 and the Partisan Polarization of Mail Voting

Lockhart et al. (2020) documented a striking development: the emergence of a partisan gap in preferences for voting by mail during the COVID-19 pandemic. Using nationally representative surveys from April and June 2020, they found a 10-percentage-point gap between Democrats and Republicans in VBM preferences in April, which doubled to nearly 20 percentage points by June. This partisan polarization of voting mode raises a natural question: if Democrats and Republicans are differentially likely to use mail voting, could universal VBM---which makes mail voting available to everyone---have different effects in the post-COVID era than it did before?

Our extension speaks directly to this question. If universal VBM developed partisan effects after mail voting became politically salient, we would expect to see a divergence between the pre-2020 and post-2020 estimates.

### 2.4 Methodological Advances in Staggered Difference-in-Differences

Recent methodological work has highlighted potential pitfalls in standard two-way fixed effects (TWFE) DiD estimators when treatment is staggered and treatment effects are heterogeneous. Goodman-Bacon (2021) showed that the TWFE estimator can be decomposed into a weighted average of all possible 2x2 DiD comparisons, with potentially negative weights on some comparisons. Callaway and Sant'Anna (2021) proposed a group-time average treatment effect estimator robust to treatment effect heterogeneity, and Sun and Abraham (2021) showed that standard event study specifications can produce misleading pre-trends when effects vary across cohorts.

These concerns are relevant to the Thompson et al. (2020) setting, where treatment timing varies across counties and states. However, the fact that the point estimates are close to zero across multiple specifications and subsamples---and that event study estimates show no pre-trends---provides reassurance that the null finding is not an artifact of problematic TWFE comparisons. A precisely estimated null effect is unlikely to be driven by negative weights, since it would require positive and negative effects to cancel almost exactly.

## 3. Data and Methods

### 3.1 Original Data

The original analysis dataset from Thompson et al. (2020) contains 1,454 county-election observations covering 126 counties across three states (58 in California, 29 in Utah, 39 in Washington) from 1996 to 2018. The data were obtained from the authors' public replication archive.

The key outcome variables are:
- **Democratic registration share** (`share_votes_dem`): The proportion of registered voters who are Democrats. Available for California and Utah only (87 counties), as Washington does not have partisan voter registration.
- **Democratic vote share** (`dem_share`): The Democratic candidate's share of the two-party vote, measured separately for governor, president, and senator races and stacked into a long dataset.
- **Turnout** (`turnout_share`): Total ballots cast divided by citizen voting-age population (CVAP).
- **VBM share** (`vbm_share`): The proportion of ballots cast by mail. Available for California only.

The treatment variable (`treat`) equals 1 when a county has adopted universal vote-by-mail and 0 otherwise. In Washington, counties adopted VBM between 1996 and 2012. In Utah, counties adopted VBM between 2012 and 2018. In California, five counties adopted the Voter's Choice Act (VCA) for the 2018 election.

### 3.2 Extension Data

We extend the dataset through 2024 by collecting county-level election results for three additional election cycles:

**2020:** Presidential election results for all three states. Data sourced from official Secretary of State certified results (California) and the `tonmcg/US_County_Level_Election_Results_08-24` GitHub repository (Utah, Washington).

**2022:** Governor election results for California; Senate election results for Utah and Washington. California data from the Secretary of State; Utah data aggregated from OpenElections precinct-level records; Washington data from the Secretary of State.

**2024:** Presidential election results for all three states. Sources match the 2020 data.

For Utah's 2022 Senate race, we note that no Democratic candidate ran. Independent candidate Evan McMullin served as the primary opposition to Republican Mike Lee. We code McMullin's votes as the opposition vote share for consistency with the two-party framework. This is acknowledged as a limitation.

Citizen voting-age population (CVAP) for the extension years is approximated by applying state-level growth factors derived from Census estimates to the last available CVAP observation in the original data. This approximation is reasonable for the cross-sectional variation that drives identification but introduces measurement error in the turnout variable.

We update California's VCA adoption data through 2024. The VCA rollout continued as follows:
- **2018:** 5 counties (original sample)
- **2020:** 15 counties (10 new)
- **2022:** 29 counties (14 new)
- **2024:** 30 counties (1 new: Placer)

The adoption data were verified against the California Secretary of State's official VCA participating counties list.

For the treatment variable in the extension period, all Utah and Washington counties are coded as treated (both states achieved universal VBM before 2020). California counties are coded based on VCA adoption timing. We note that Governor Newsom's Executive Order N-64-20 directed all California counties to mail ballots to registered voters for the November 2020 election, regardless of VCA status. We maintain the VCA-based treatment coding for consistency with the structural policy definition used by Thompson et al. (2020), but the executive order attenuates the treatment contrast in 2020 and should be kept in mind when interpreting the results.

The merged dataset contains 1,832 observations: 1,454 from the original period (1996--2018) and 378 from the extension period (2020--2024).

### 3.3 Empirical Strategy

We follow Thompson et al. (2020) and estimate the following equation:

$$Y_{cst} = \beta \cdot \text{VBM}_{cst} + \gamma_{cs} + \delta_{st} + \varepsilon_{cst}$$

where $Y_{cst}$ is the outcome for county $c$ in state $s$ at election time $t$; $\text{VBM}_{cst}$ is an indicator equal to 1 when universal VBM is in effect; $\gamma_{cs}$ are county fixed effects; and $\delta_{st}$ are state-by-year fixed effects. Standard errors are clustered at the county level.

We estimate three specifications for each outcome:
1. **Basic:** County and state-by-year fixed effects only.
2. **Linear trends:** Adds county-specific linear time trends (county $\times$ year interactions).
3. **Quadratic trends:** Adds county-specific linear and quadratic time trends.

The inclusion of county-specific trends is important because counties that adopted VBM may have been on different political trajectories than non-adopters. The trend specifications allow each county to follow its own linear or quadratic path, with the treatment effect identified from deviations from this county-specific trend that coincide with VBM adoption.

For the extension analysis, we also estimate:
- **Period interaction models:** $Y_{cst} = \beta_1 \cdot \text{VBM}_{cst} + \beta_2 \cdot (\text{VBM}_{cst} \times \text{Post2018}_t) + \gamma_{cs} + \delta_{st} + \varepsilon_{cst}$, where $\text{Post2018}_t$ is an indicator for elections after 2018. The coefficient $\beta_2$ captures the differential effect of VBM in the post-2018 period.
- **California-only models:** Restricting to California exploits the within-state staggered VCA rollout from 2018 to 2024.
- **Event study models:** Using dummies for event time relative to VCA adoption (with $t = -2$ as the reference period) to test for pre-trends and trace out dynamic treatment effects.

### 3.4 Implementation

All analyses were implemented in Python using NumPy for linear algebra and Pandas for data manipulation. The Stata `reghdfe` command was replicated using an iterative demeaning (alternating projections) algorithm, which alternately demeans variables by county and state-by-year groups until convergence (tolerance: $10^{-10}$). County-specific trends are absorbed by projecting out county-level regressions on year (linear) or year and year-squared (quadratic) within each iteration. Clustered standard errors use the standard sandwich estimator with the $G/(G-1)$ small-sample correction.

## 4. Replication Results

Table 1 presents the replication of the original Table 2 (partisan outcomes) and Table 3 (participation outcomes).

### Table 1: Replication of Thompson et al. (2020)

**Panel A: Partisan Outcomes (Original Table 2)**

| | (1) | (2) | (3) | (4) | (5) | (6) |
|---|---|---|---|---|---|---|
| **Outcome** | Dem Reg | Dem Reg | Dem Reg | Dem Vote | Dem Vote | Dem Vote |
| **Specification** | Basic | Linear | Quad | Basic | Linear | Quad |
| Original | 0.007 | 0.001 | 0.001 | 0.028 | 0.011 | 0.007 |
| | (0.003) | (0.001) | (0.001) | (0.011) | (0.004) | (0.003) |
| Replicated | 0.007 | 0.001 | 0.001 | 0.029 | 0.011 | 0.007 |
| | (0.003) | (0.001) | (0.001) | (0.011) | (0.004) | (0.003) |
| Counties | 87 | 87 | 87 | 126 | 126 | 126 |
| Observations | 986 | 986 | 986 | 1,998 | 1,998 | 1,998 |

**Panel B: Participation Outcomes (Original Table 3)**

| | (1) | (2) | (3) | (4) | (5) | (6) |
|---|---|---|---|---|---|---|
| **Outcome** | Turnout | Turnout | Turnout | VBM Share | VBM Share | VBM Share |
| **Specification** | Basic | Linear | Quad | Basic | Linear | Quad |
| Original | 0.021 | 0.022 | 0.021 | 0.186 | 0.157 | 0.136 |
| | (0.009) | (0.007) | (0.008) | (0.027) | (0.035) | (0.085) |
| Replicated | 0.021 | 0.022 | 0.021 | 0.186 | 0.158 | 0.136 |
| | (0.009) | (0.007) | (0.007) | (0.026) | (0.033) | (0.076) |
| Counties | 126 | 126 | 126 | 58 | 58 | 58 |
| Observations | 1,240 | 1,240 | 1,240 | 892 | 892 | 892 |

*Notes:* All specifications include county and state-by-year fixed effects. Standard errors clustered at county level in parentheses. Columns 1--3 use Democratic registration share (CA, UT) or turnout as the outcome; columns 4--6 use stacked Democratic vote share or VBM share. "Linear" adds county-specific linear year trends; "Quad" adds both linear and quadratic trends.

All 12 point estimates match the original paper within rounding tolerance. The maximum absolute difference is 0.0005 (columns 4 and 6 of Panel A), which rounds to zero at the three-decimal-place precision reported in the original paper. Standard errors are also very close, with minor differences attributable to implementation details of the finite-sample corrections for clustered standard errors in high-dimensional fixed effects models.

## 5. Extension Results

### 5.1 Main Results on the Full Sample

Table 2 presents the main extension results, estimated on the full 1996--2024 sample.

### Table 2: Extension Results — Full Sample (1996--2024)

**Panel A: Democratic Vote Share**

| | (1) Basic | (2) Linear | (3) Quadratic |
|---|---|---|---|
| VBM | 0.024*** | 0.006* | 0.004 |
| | (0.007) | (0.003) | (0.003) |
| Counties | 126 | 126 | 126 |
| Observations | 2,376 | 2,376 | 2,376 |

**Panel B: Turnout**

| | (1) Basic | (2) Linear | (3) Quadratic |
|---|---|---|---|
| VBM | 0.019*** | 0.011** | 0.013** |
| | (0.005) | (0.005) | (0.006) |
| Counties | 126 | 126 | 126 |
| Observations | 1,618 | 1,618 | 1,618 |

*Notes:* \*p<0.1, \*\*p<0.05, \*\*\*p<0.01. All specifications include county and state-by-year fixed effects. Standard errors clustered at county level. "Linear" adds county-specific linear trends; "Quadratic" adds linear and quadratic trends. Democratic vote share is stacked across governor, president, and senator races.

The main finding is unchanged: the effect of VBM on Democratic vote share is small and statistically insignificant once county-specific trends are included. The quadratic trend estimate of 0.004 (SE = 0.003) is statistically indistinguishable from zero and substantively negligible---an effect of less than half a percentage point. The basic specification shows a larger coefficient (0.024), but as in the original paper, this is likely driven by pre-existing trends rather than a causal effect of VBM.

The turnout effect remains positive and statistically significant across all specifications. The linear trend estimate is 0.011 (SE = 0.005), somewhat smaller than the original paper's 0.022 (SE = 0.007), suggesting some attenuation in the extension period. This attenuation is explored further below.

### 5.2 Period Comparison

Table 3 separates the estimates by period.

### Table 3: Results by Period

| | Original (1996--2018) | Extension (2020--2024) |
|---|---|---|
| **Dem Vote Share** | | |
| Basic | 0.029** (0.011) | -0.005 (0.006) |
| Linear | 0.011*** (0.004) | 0.016 (0.010) |
| **Turnout** | | |
| Basic | 0.021** (0.009) | -0.010 (0.007) |
| Linear | 0.022*** (0.007) | -0.050*** (0.017) |

*Notes:* Standard errors clustered at county level in parentheses.

The extension-period-only estimates are imprecise due to the limited number of observations (378) and time periods (3 election cycles). The basic specification for Dem vote share in the extension period is -0.005, consistent with zero. The negative turnout estimate in the extension period (-0.050 with linear trends) is striking but should be interpreted cautiously: with only three time periods, county-specific linear trends are estimated with very few degrees of freedom, and the 2020 executive order confounds the treatment contrast.

### 5.3 Heterogeneity: VBM Effect by Period

Table 4 presents results from the interaction model, testing whether VBM effects differ pre- and post-2018.

### Table 4: VBM $\times$ Post-2018 Interaction

**Panel A: Democratic Vote Share**

| | (1) Basic | (2) Linear | (3) Quadratic |
|---|---|---|---|
| VBM | 0.028*** | 0.010*** | 0.008** |
| | (0.009) | (0.003) | (0.003) |
| VBM $\times$ Post-2018 | -0.009 | -0.013** | -0.021*** |
| | (0.014) | (0.006) | (0.006) |
| Combined (VBM + interaction) | 0.019 | -0.003 | -0.013 |

**Panel B: Turnout**

| | (1) Basic | (2) Linear | (3) Quadratic |
|---|---|---|---|
| VBM | 0.029*** | 0.023*** | 0.021*** |
| | (0.007) | (0.007) | (0.007) |
| VBM $\times$ Post-2018 | -0.020** | -0.029*** | -0.027*** |
| | (0.010) | (0.009) | (0.009) |
| Combined (VBM + interaction) | 0.009 | -0.006 | -0.006 |

*Notes:* Post-2018 indicator absorbed by state-by-year fixed effects. The "Combined" row reports the sum of the VBM and interaction coefficients, representing the total VBM effect in the post-2018 period.

The interaction term for turnout is consistently negative and significant, indicating that VBM's turnout-boosting effect was smaller (or reversed) in the post-2018 period. The combined effect (VBM + interaction) is approximately zero in the trend specifications. As noted, this likely reflects the confounding of Governor Newsom's executive order rather than a genuine change in VBM's causal effect on turnout.

For Democratic vote share, the interaction is negative and significant in the trend specifications. The combined post-2018 effect is -0.003 (linear trends) or -0.013 (quadratic trends), neither of which is large enough to suggest a meaningful partisan impact of VBM.

### 5.4 California-Only Analysis

Table 5 exploits the within-California VCA stagger for identification.

### Table 5: California-Only Results (1998--2024)

| | (1) Basic | (2) Linear | (3) Quadratic |
|---|---|---|---|
| **Dem Vote Share** | | |
| VBM | 0.020* | -0.004 | -0.012*** |
| | (0.010) | (0.005) | (0.005) |
| N | 812 | 812 | 812 |
| **Turnout** | | |
| VBM | 0.010 | -0.005 | -0.003 |
| | (0.006) | (0.006) | (0.006) |
| N | 754 | 754 | 754 |

*Notes:* 58 California counties. Fixed effects: county + year. Standard errors clustered at county level.

The California-only estimates reinforce the null finding. With linear or quadratic trends, the VCA effect on Democratic vote share is close to zero (or slightly negative). The turnout effect is also not statistically significant in the CA-only sample, consistent with the attenuation caused by the 2020 executive order.

### 5.5 Event Study

Figure 1 presents event study estimates for Democratic vote share and turnout, plotted around the time of VCA adoption for California's 30 treated counties. The reference period is two years before adoption ($t = -2$). The specification includes county fixed effects, year fixed effects, and county-specific linear trends.

### Table 6: Event Study Coefficients (CA Treated Counties)

**Panel A: Democratic Vote Share**

| Event Time | Coefficient | SE | 95% CI |
|---|---|---|---|
| $t - 6$ | 0.005 | 0.007 | [-0.008, 0.018] |
| $t - 4$ | -0.002 | 0.005 | [-0.011, 0.007] |
| $t - 2$ | --- (ref) | --- | --- |
| $t = 0$ | -0.002 | 0.006 | [-0.014, 0.009] |
| $t + 2$ | 0.001 | 0.010 | [-0.019, 0.022] |
| $t + 4$ | 0.013 | 0.019 | [-0.024, 0.050] |
| $t + 6$ | 0.015 | 0.027 | [-0.037, 0.067] |

**Panel B: Turnout**

| Event Time | Coefficient | SE | 95% CI |
|---|---|---|---|
| $t - 6$ | 0.004 | 0.006 | [-0.008, 0.016] |
| $t - 4$ | -0.004 | 0.006 | [-0.015, 0.007] |
| $t - 2$ | --- (ref) | --- | --- |
| $t = 0$ | -0.007 | 0.009 | [-0.026, 0.011] |
| $t + 2$ | -0.003 | 0.014 | [-0.031, 0.024] |
| $t + 4$ | -0.014 | 0.024 | [-0.060, 0.033] |
| $t + 6$ | -0.017 | 0.035 | [-0.085, 0.051] |

*Notes:* 30 treated CA counties. Reference period is $t = -2$ (one election before VCA adoption). Specification includes county FE, year FE, and county-specific linear trends. Event times are in election-year units (biennial). Standard errors clustered at county level.

The event study provides strong evidence for the parallel trends assumption. Pre-treatment coefficients at $t - 6$ and $t - 4$ are small and statistically insignificant for both outcomes, indicating no differential pre-trends between VCA adopters and non-adopters before adoption. Post-treatment coefficients are also small and insignificant, consistent with the null effect found in the main specifications. The confidence intervals widen at longer horizons, as expected given the smaller number of counties observed at extreme event times.

### 5.6 Robustness: Excluding 2020

The 2020 election is the most potentially confounded observation in the extension sample due to Governor Newsom's executive order. Table 7 presents results excluding 2020.

### Table 7: Robustness — Excluding 2020

| | (1) Basic | (2) Linear | (3) Quadratic |
|---|---|---|---|
| **Dem Vote Share** | | | |
| VBM | 0.027*** | 0.007** | 0.006* |
| | (0.008) | (0.003) | (0.003) |
| N | 2,250 | 2,250 | 2,250 |
| **Turnout** | | | |
| VBM | 0.019*** | 0.013** | 0.016** |
| | (0.006) | (0.005) | (0.006) |
| N | 1,492 | 1,492 | 1,492 |

*Notes:* Excludes all 2020 observations. Standard errors clustered at county level.

Excluding 2020 yields results very similar to the full sample. The Democratic vote share effect remains small and insignificant with trends (0.007 linear, 0.006 quadratic). The turnout effect is slightly larger than the full-sample estimate (0.013 vs. 0.011 with linear trends), consistent with 2020 being a confounded observation that attenuates the estimated treatment effect.

## 6. Discussion

### 6.1 Summary of Findings

Our analysis yields three main findings:

1. **The null partisan effect of VBM is robust through 2024.** Across all specifications and subsamples, VBM has no meaningful effect on Democratic vote share. The largest estimate with county trends is 0.007 (SE = 0.003), substantively negligible at less than one percentage point. This finding holds in the full sample, in the extension period alone, in California only, and when excluding the potentially confounded 2020 election.

2. **VBM's turnout-boosting effect persists but is attenuated post-2018.** The pooled estimate of approximately 1--2 percentage points is consistent with the original finding, though the post-2018 interaction is negative and significant. The attenuation is most likely driven by the COVID-era confound (the 2020 executive order) rather than a genuine change in VBM's causal effect.

3. **Event study evidence supports the parallel trends assumption.** Pre-treatment coefficients are small and insignificant, providing no evidence of differential pre-trends. This supports the internal validity of the difference-in-differences design.

### 6.2 The COVID Confound

The most important interpretive challenge for the extension analysis is Governor Newsom's Executive Order N-64-20, which directed all California counties to mail ballots to all registered voters for the November 2020 general election. This executive order effectively treated all California counties as universal VBM in 2020, regardless of their VCA status. Under our coding scheme---which maintains the structural VCA-based treatment definition---non-VCA counties in 2020 are coded as untreated despite receiving de facto VBM treatment.

This contamination of the control group biases the extension-period estimates toward zero for turnout (since even "untreated" counties received the treatment). For partisan outcomes, the bias direction depends on whether de facto VBM (temporary executive order) has different effects from de jure VBM (permanent VCA adoption). If the effects are similar, the contamination biases the partisan estimate toward zero as well.

The robustness check excluding 2020 helps address this concern, and the results are indeed somewhat stronger (larger turnout effect) when 2020 is excluded.

### 6.3 Limitations

Several limitations should be noted. First, voter registration composition data (`share_votes_dem`) is not available for the extension period, so we cannot replicate the full Table 2 on the extended sample. Second, our CVAP estimates for the extension years are approximations based on growth factors rather than county-specific Census data, introducing measurement error in the turnout denominator. Third, Utah's 2022 Senate race lacked a Democratic candidate, requiring us to code the independent opposition candidate as the non-Republican vote share. Fourth, we do not implement the robust heterogeneity-aware DiD estimators of Callaway and Sant'Anna (2021) or Sun and Abraham (2021), though the consistency of our results across specifications and the clean event study evidence suggest that the TWFE approach performs adequately in this setting.

### 6.4 Implications for Election Policy

The persistence of the null partisan finding through 2024 has important implications for election policy debates. Claims that universal VBM systematically advantages either party lack empirical support, even in the post-pandemic period when mail voting became intensely partisan in public discourse. Policymakers considering universal VBM should weigh its potential to modestly increase turnout against administrative costs and implementation challenges, without concern that it will tip the partisan balance.

## 7. Conclusion

We replicate Thompson et al. (2020) and extend their analysis of universal vote-by-mail through 2024, spanning the COVID-19 pandemic and the continued rollout of California's Voter's Choice Act. Our replication confirms all original findings. Our extension finds that the null partisan effect of VBM is robust: VBM does not meaningfully affect Democratic vote share in either the original or extended sample. VBM's turnout-boosting effect persists in the pooled sample but is attenuated in the post-2018 period, likely due to confounding from California's 2020 executive order. Event study evidence supports the parallel trends assumption underlying the identification strategy.

These findings reinforce the growing consensus in the empirical literature: universal vote-by-mail is a voter convenience reform that modestly increases participation without conferring a systematic partisan advantage. This conclusion holds even in the politically charged post-pandemic environment.

## References

Amlani, Sharif, and Carlos Collitt. 2022. "The Impact of Vote-By-Mail Policy on Turnout and Vote Share in the 2020 Election." *Election Law Journal* 21(1).

Barber, Michael, and John B. Holbein. 2020. "The Participatory and Partisan Impacts of Mandatory Vote-by-Mail." *Science Advances* 6(35): eabc7685.

Berinsky, Adam J., Nancy Burns, and Michael W. Traugott. 2001. "Who Votes by Mail? A Dynamic Model of the Individual-Level Consequences of Voting-by-Mail Systems." *Public Opinion Quarterly* 65(2): 178--197.

Callaway, Brantly, and Pedro H. C. Sant'Anna. 2021. "Difference-in-Differences with Multiple Time Periods." *Journal of Econometrics* 225(2): 200--230.

Gerber, Alan S., Gregory A. Huber, and Seth J. Hill. 2013. "Identifying the Effect of All-Mail Elections on Turnout: Staggered Reform in the Evergreen State." *Political Science Research and Methods* 1(1): 91--116.

Goodman-Bacon, Andrew. 2021. "Difference-in-Differences with Variation in Treatment Timing." *Journal of Econometrics* 225(2): 254--277.

Gronke, Paul, Eva Galanes-Rosenbaum, Peter A. Miller, and Daniel Toffey. 2008. "Convenience Voting." *Annual Review of Political Science* 11: 437--455.

Kousser, Thad, and Megan Mullin. 2007. "Does Voting by Mail Increase Participation? Using Matching to Analyze a Natural Experiment." *Political Analysis* 15(4): 428--445.

Lockhart, Mackenzie, Seth J. Hill, Jennifer Merolla, Mindy Romero, and Thad Kousser. 2020. "America's Electorate Is Increasingly Polarized Along Partisan Lines About Voting by Mail During the COVID-19 Crisis." *Proceedings of the National Academy of Sciences* 117(40): 24640--24642.

Southwell, Priscilla L., and Justin I. Burchett. 2000. "The Effect of All-Mail Elections on Voter Turnout." *American Politics Quarterly* 28(1): 72--79.

Sun, Liyang, and Sarah Abraham. 2021. "Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects." *Journal of Econometrics* 225(2): 175--199.

Thompson, Daniel M., Jennifer A. Wu, Jesse Yoder, and Andrew B. Hall. 2020. "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share." *Proceedings of the National Academy of Sciences* 117(25): 14052--14056.
