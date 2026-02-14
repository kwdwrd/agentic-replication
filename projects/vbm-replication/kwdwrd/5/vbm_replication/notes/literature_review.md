# Literature Review

## Summary Table

| Authors | Year | Journal | Topic | Key Finding | Verified? |
|---------|------|---------|-------|-------------|-----------|
| Thompson, Wu, Yoder, and Hall | 2020 | PNAS 117(25): 14052-14056 | Causal effects of universal VBM on partisan outcomes | VBM has no partisan effect; ~2pp turnout increase | Yes |
| Gerber, Huber, and Hill | 2013 | Political Science Research and Methods 1(1): 91-116 | Effect of all-mail elections on turnout in Washington | All-mail elections increase turnout 2-4pp; larger effects for low-propensity voters | Yes |
| Kousser and Mullin | 2007 | Political Analysis 15(4): 428-445 | VBM and participation using matching | VBM does not increase turnout in regular elections; may increase turnout in special elections | Yes |
| Southwell and Burchett | 2000 | American Politics Quarterly 28(1): 72-79 | Effect of all-mail elections in Oregon | Oregon's VBM increased turnout by ~10pp (later questioned by Gronke and Miller 2012) | Yes |
| Gronke, Galanes-Rosenbaum, Miller, and Toffey | 2008 | Annual Review of Political Science 11: 437-455 | Review of convenience voting research | Convenience voting used by >30% of Americans; research unequally distributed across methods | Yes |
| Berinsky, Burns, and Traugott | 2001 | Public Opinion Quarterly 65(2): 178-197 | Who votes by mail---individual-level analysis | VBM may mobilize existing voters more than new voters; raises equity concerns | Yes |
| Barber and Holbein | 2020 | Science Advances 6(35): eabc7685 | Participatory and partisan impacts of mandatory VBM | VBM increases turnout 2-3pp; no effect on election outcomes or partisan advantage | Yes |
| Amlani and Collitt | 2022 | Election Law Journal 21(1) | Impact of VBM policy on turnout/vote share in 2020 | Counties mailing ballots saw 2.6% higher turnout; no partisan advantage | Yes |
| Lockhart, Hill, Merolla, Romero, and Kousser | 2020 | PNAS 117(40): 24640-24642 | Partisan polarization in VBM preferences during COVID | 10pp Dem-Rep gap in VBM preference in April 2020, doubling to 20pp by June | Yes |
| Goodman-Bacon | 2021 | Journal of Econometrics 225(2): 254-277 | DiD with variation in treatment timing | TWFE DiD can be biased with staggered treatment and heterogeneous effects | Yes |
| Callaway and Sant'Anna | 2021 | Journal of Econometrics 225(2): 200-230 | DiD with multiple time periods | Propose group-time ATT estimator robust to heterogeneous treatment effects | Yes |
| Sun and Abraham | 2021 | Journal of Econometrics 225(2): 175-199 | Event studies with heterogeneous treatment effects | Standard TWFE event studies can show spurious pre-trends; propose robust alternative | Yes |

## Detailed Summaries

### Foundational VBM Studies

#### Gerber, Huber, and Hill (2013)
**"Identifying the Effect of All-Mail Elections on Turnout: Staggered Reform in the Evergreen State"**
*Political Science Research and Methods* 1(1): 91-116.

This paper is the most direct antecedent to Thompson et al. (2020). It exploits the staggered county-level rollout of all-mail elections in Washington State to estimate the causal effect on turnout. Using both county-level aggregate data and individual-level voter file records, the authors find that all-mail elections increased aggregate turnout by 2 to 4 percentage points. Using individual data, they find the reform disproportionately increased turnout among lower-propensity voters, suggesting VBM reduces the participation gap between habitual and occasional voters. Thompson et al. (2020) build directly on this design, extending it to three states and examining partisan outcomes in addition to turnout.

#### Kousser and Mullin (2007)
**"Does Voting by Mail Increase Participation? Using Matching to Analyze a Natural Experiment"**
*Political Analysis* 15(4): 428-445.

Kousser and Mullin use a matching design to analyze the effect of VBM on turnout in California. Using nearest-neighbor matching to pair VBM precincts with traditional precincts within the same county, they find that VBM does not increase turnout in regular elections. However, they find some evidence that VBM increases turnout in special elections, where the baseline turnout is lower. The null finding for regular elections challenges the optimistic claims of VBM proponents and suggests that reducing the cost of voting may not be sufficient to bring non-voters to participate.

#### Southwell and Burchett (2000)
**"The Effect of All-Mail Elections on Voter Turnout"**
*American Politics Quarterly* 28(1): 72-79.

This early study of Oregon's pioneering vote-by-mail system reported that all-mail elections increased turnout by approximately 10 percentage points. However, subsequent work by Gronke and Miller (2012) was unable to replicate this finding and suggested the large effect may have been due to a novelty effect in the first few VBM elections. Despite the replication concerns, this paper remains important as one of the first empirical analyses of universal VBM.

#### Gronke, Galanes-Rosenbaum, Miller, and Toffey (2008)
**"Convenience Voting"**
*Annual Review of Political Science* 11: 437-455.

This review article provides a comprehensive overview of the convenience voting literature, covering early in-person voting, voting by mail, absentee voting, and other alternative voting methods. The authors note that convenience voting had become the mode of choice for over 30% of Americans by the mid-2000s, yet academic research on these practices was unevenly distributed. The review concludes that convenience voting reforms generally have modest effects on turnout and are unlikely to transform the composition of the electorate.

#### Berinsky, Burns, and Traugott (2001)
**"Who Votes by Mail? A Dynamic Model of the Individual-Level Consequences of Voting-by-Mail Systems"**
*Public Opinion Quarterly* 65(2): 178-197.

This paper examines the individual-level consequences of VBM systems, asking whether VBM changes who participates in elections. Using a dynamic model of individual voting behavior, the authors find that VBM may primarily mobilize existing voters (those who would have voted anyway) rather than bringing new voters into the electorate. This raises concerns about whether VBM exacerbates rather than reduces existing inequalities in participation, as more-engaged, higher-SES voters may disproportionately take advantage of the convenience.

### Post-2020 / COVID-Era Studies

#### Barber and Holbein (2020)
**"The Participatory and Partisan Impacts of Mandatory Vote-by-Mail"**
*Science Advances* 6(35): eabc7685.

Published concurrently with Thompson et al., this paper examines the effects of mandatory VBM using county-level data from six states (Colorado, Oregon, Utah, Washington, Nebraska, and California) spanning three decades, plus 40 million individual voter records from Washington and Utah. Using multiple causal inference methods, the authors find that mandatory VBM increases turnout by 2-3 percentage points but has no effect on election outcomes or partisan advantage. This represents a converging finding with Thompson et al. using a somewhat different set of states and methods.

#### Amlani and Collitt (2022)
**"The Impact of Vote-By-Mail Policy on Turnout and Vote Share in the 2020 Election"**
*Election Law Journal* 21(1).

This paper is particularly relevant for our extension, as it examines VBM effects during the COVID-19 pandemic. Using a difference-in-difference design, the authors find that counties that sent mail-in ballots to all registered voters experienced 2.6% higher turnout compared to counties with no policy change. They find no evidence that making VBM easier conferred a partisan advantage, even during the highly polarized 2020 election. This is encouraging for the external validity of Thompson et al.'s pre-COVID findings.

#### Lockhart, Hill, Merolla, Romero, and Kousser (2020)
**"America's Electorate Is Increasingly Polarized Along Partisan Lines About Voting by Mail During the COVID-19 Crisis"**
*PNAS* 117(40): 24640-24642.

This paper documents the partisan polarization in preferences for VBM that emerged during COVID-19. Using two nationally representative surveys (April and June 2020), the authors find a nearly 10 percentage point gap between Democrats and Republicans in their preference for voting by mail in April, which doubled to nearly 20 percentage points by June 2020. This polarization was amplified by exposure to scientific projections about the pandemic. The finding is important for our extension because it suggests that even if VBM has no inherent partisan bias, the differential adoption of VBM as a voting mode became itself a partisan phenomenon after 2020.

### Methodological Papers on Staggered Diff-in-Diff

#### Goodman-Bacon (2021)
**"Difference-in-Differences with Variation in Treatment Timing"**
*Journal of Econometrics* 225(2): 254-277.

This foundational methodological paper shows that the standard two-way fixed effects (TWFE) difference-in-differences estimator can be decomposed into a weighted average of all possible 2x2 DiD comparisons between groups that adopt treatment at different times. Critically, the weights can be negative, and the estimator can be biased when treatment effects are heterogeneous over time. This is directly relevant to Thompson et al.'s setting, where VBM treatment is staggered across counties and years. The Goodman-Bacon decomposition provides a way to assess the sensitivity of the estimates to problematic comparisons (e.g., using already-treated units as controls).

#### Callaway and Sant'Anna (2021)
**"Difference-in-Differences with Multiple Time Periods"**
*Journal of Econometrics* 225(2): 200-230.

Callaway and Sant'Anna propose a group-time average treatment effect (ATT) estimator that is robust to treatment effect heterogeneity. Their approach identifies treatment effects for each cohort (defined by treatment timing) at each post-treatment period, then aggregates these effects using transparent weighting. The method allows researchers to incorporate covariates, use different comparison groups (never-treated, not-yet-treated), and test for pre-trends more rigorously. This approach could be applied to the Thompson et al. setting as a robustness check on the standard TWFE estimates.

#### Sun and Abraham (2021)
**"Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects"**
*Journal of Econometrics* 225(2): 175-199.

Sun and Abraham show that standard TWFE event study specifications---where researchers include leads and lags of treatment---can produce misleading results when treatment effects are heterogeneous across cohorts. The coefficient on a given lead or lag can be "contaminated" by effects from other periods, and apparent pre-trends can arise solely from treatment effect heterogeneity rather than violation of parallel trends. They propose an interaction-weighted estimator that is free of this contamination. This is directly relevant to interpreting the event study specifications in Thompson et al.

## Key Themes from the Literature

1. **Consistent null partisan effects:** Across multiple studies, time periods, and states, there is no evidence that VBM systematically advantages either party.

2. **Modest turnout effects:** The consensus estimate is that VBM increases turnout by 2-4 percentage points, primarily by converting some non-voters into voters.

3. **Composition concerns:** Some evidence suggests VBM disproportionately mobilizes higher-propensity voters, potentially widening participation gaps (Berinsky et al. 2001), while other evidence suggests it helps lower-propensity voters more (Gerber et al. 2013).

4. **COVID changed the dynamics:** The 2020 pandemic made VBM a partisan issue, with Democrats much more likely to prefer and use mail voting. Whether this changes the causal effect of universal VBM on outcomes is an open question.

5. **Methodological advances:** Recent work on staggered DiD (Goodman-Bacon 2021; Callaway and Sant'Anna 2021; Sun and Abraham 2021) raises important concerns about standard TWFE estimators in settings like Thompson et al.'s, where treatment timing varies across units.
