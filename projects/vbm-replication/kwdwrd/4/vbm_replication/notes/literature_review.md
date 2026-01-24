# Literature Review: Vote-by-Mail and Electoral Outcomes

This document summarizes the relevant academic literature on vote-by-mail (VBM) effects on turnout and partisan outcomes. All citations have been verified through web searches.

---

## Summary Table

| Authors | Year | Journal | Topic | Key Finding | Verified? |
|---------|------|---------|-------|-------------|-----------|
| Thompson, Wu, Yoder, & Hall | 2020 | PNAS | VBM partisan effects & turnout | Null partisan effects; +2 pp turnout | Yes |
| Gerber, Huber, & Hill | 2013 | Political Science Research & Methods | WA all-mail turnout effects | +2-4 pp turnout; benefits low-propensity voters | Yes |
| Kousser & Mullin | 2007 | Political Analysis | CA VBM participation | -2.6 pp in general elections; +7 pp in local elections | Yes |
| Southwell & Burchett | 2000 | American Politics Quarterly | Oregon all-mail turnout | +10 pp turnout (later questioned) | Yes |
| Gronke et al. | 2008 | Annual Review of Political Science | Convenience voting review | Mixed effects; does not mobilize new voters | Yes |
| Berinsky, Burns, & Traugott | 2001 | Public Opinion Quarterly | Who votes by mail | VBM voters are older, more educated, more Republican | Yes |
| Goodman-Bacon | 2021 | Journal of Econometrics | Staggered DiD methodology | TWFE can be biased with treatment timing variation | Yes |
| Callaway & Sant'Anna | 2021 | Journal of Econometrics | DiD with multiple periods | Alternative estimators for staggered adoption | Yes |
| Sun & Abraham | 2021 | Journal of Econometrics | Event studies with heterogeneous effects | Standard event studies can be contaminated | Yes |
| Amlani & Collitt | 2022 | Election Law Journal | 2020 VBM effects | +2.6 pp turnout; no partisan advantage | Yes |
| McGhee, Paluch, & Romero | 2022 | Research & Politics | 2020 VBM policy effects | +5.6 pp turnout in VBM states; no robust partisan effects | Yes |

---

## Foundational VBM Studies

### Gerber, Huber, and Hill (2013)
**Citation**: Gerber, Alan S., Gregory A. Huber, and Seth J. Hill. 2013. "Identifying the Effect of All-Mail Elections on Turnout: Staggered Reform in the Evergreen State." *Political Science Research and Methods* 1(1): 91-116.

**Summary**: This study exploits Washington State's county-by-county adoption of all-mail elections from 2005-2011. Using both aggregate county-level data and individual-level voter file data, the authors find that all-mail elections increased turnout by 2-4 percentage points. Importantly, they find that the reform benefited low-propensity voters more than frequent voters, suggesting VBM can reduce participation disparities. This paper provides the methodological template for Thompson et al. (2020), which extends the analysis to include California and Utah and examines partisan outcomes.

**Verified**: Yes - Cambridge Core, Yale ISPS

---

### Kousser and Mullin (2007)
**Citation**: Kousser, Thad, and Megan Mullin. 2007. "Does Voting by Mail Increase Participation? Using Matching to Analyze a Natural Experiment." *Political Analysis* 15(4): 428-445.

**Summary**: Using a natural experiment in California where some precincts are randomly assigned to vote by mail, this study finds that VBM *decreases* turnout by 2.6-2.9 percentage points in general elections. However, it *increases* turnout by about 7 percentage points in local special elections. The authors argue that comparing absentee voters to in-person voters (as some prior studies did) is misleading because absentee voters self-select and differ systematically from other voters. This paper highlights the importance of identification strategy in VBM research.

**Verified**: Yes - MIT, SSRN, Political Analysis

---

### Southwell and Burchett (2000)
**Citation**: Southwell, Priscilla L., and Justin I. Burchett. 2000. "The Effect of All-Mail Elections on Voter Turnout." *American Politics Quarterly* 28(1): 72-79.

**Summary**: Analyzing 48 statewide elections in Oregon, this influential early study found that all-mail elections increased turnout by approximately 10 percentage points. This became the most widely cited result on VBM turnout effects. However, subsequent replication attempts (Gronke and Miller 2012) could not reproduce these findings when extending the time series, suggesting the original effect may have been a novelty effect from the first few VBM elections.

**Verified**: Yes - SAGE Journals

---

### Gronke et al. (2008)
**Citation**: Gronke, Paul, Eva Galanes-Rosenbaum, Peter A. Miller, and Daniel Toffey. 2008. "Convenience Voting." *Annual Review of Political Science* 11: 437-455.

**Summary**: This comprehensive review of convenience voting (including early voting, VBM, and absentee voting) finds that over 30% of Americans used some form of convenience voting by 2008. Despite theoretical expectations from rational choice theory that convenience voting should increase turnout, the empirical literature finds mixed results. The authors note that convenience voting does not appear to mobilize new voters or reach disempowered populations—it mainly provides an alternative method for existing voters. This review established the conventional wisdom that VBM effects on turnout are modest at best.

**Verified**: Yes - Annual Reviews

---

### Berinsky, Burns, and Traugott (2001)
**Citation**: Berinsky, Adam J., Nancy Burns, and Michael W. Traugott. 2001. "Who Votes by Mail? A Dynamic Model of the Individual-Level Consequences of Voting-by-Mail Systems." *Public Opinion Quarterly* 65(2): 178-197.

**Summary**: This study examines the individual-level characteristics of VBM users in Oregon. The authors find that VBM voters tend to be older, more educated, and more Republican than in-person voters. They develop a dynamic model showing how the composition of VBM users changes over time as the policy matures. This paper raises important questions about whether VBM expands the electorate or simply changes how existing voters cast ballots.

**Verified**: Yes - Oxford Academic

---

## Post-2020 Studies

### Amlani and Collitt (2022)
**Citation**: Amlani, Sharif, and Samuel Collitt. 2022. "The Impact of Vote-By-Mail Policy on Turnout and Vote Share in the 2020 Election." *Election Law Journal* 21(2): 135-149.

**Summary**: Using a two-period difference-in-differences design, this study examines how COVID-19-related VBM expansions affected turnout and presidential vote share in 2020. Counties that mailed ballots to all registered voters saw 2.6 percentage points higher turnout compared to counties with no policy change. Importantly, the authors find no evidence that VBM expansions conferred a partisan advantage to either party. This is one of the first rigorous studies of VBM effects during the pandemic.

**Verified**: Yes - SAGE Journals, Harvard Dataverse (replication data)

---

### McGhee, Paluch, and Romero (2022)
**Citation**: McGhee, Eric, Jennifer Paluch, and Mindy Romero. 2022. "Vote-by-Mail Policy and the 2020 Presidential Election." *Research & Politics* 9(2): 1-15.

**Summary**: This study examines VBM policy effects both before and during the 2020 pandemic election using county-level data. States that mailed ballots to all registered voters saw turnout increase by an average of 5.6 percentage points, with even larger effects among infrequent voters. However, the authors find no robust partisan effects—in many specifications, VBM slightly benefits Republicans. This suggests that even during the politically charged 2020 election, VBM did not fundamentally advantage either party.

**Verified**: Yes - SAGE Journals, SSRN

---

## Methodological Papers on Staggered Difference-in-Differences

### Goodman-Bacon (2021)
**Citation**: Goodman-Bacon, Andrew. 2021. "Difference-in-Differences with Variation in Treatment Timing." *Journal of Econometrics* 225(2): 254-277.

**Summary**: This seminal paper shows that the standard two-way fixed effects (TWFE) difference-in-differences estimator is a weighted average of all possible two-group/two-period comparisons in the data. Critically, some of these comparisons use already-treated units as controls, which can lead to bias when treatment effects are heterogeneous over time. The "Goodman-Bacon decomposition" allows researchers to see how much weight each comparison receives. This paper has major implications for studies like Thompson et al. (2020) that use staggered adoption designs.

**Verified**: Yes - ScienceDirect, NBER Working Paper 25018

---

### Callaway and Sant'Anna (2021)
**Citation**: Callaway, Brantly, and Pedro H.C. Sant'Anna. 2021. "Difference-in-Differences with Multiple Time Periods." *Journal of Econometrics* 225(2): 200-230.

**Summary**: This paper proposes alternative difference-in-differences estimators that are robust to heterogeneous treatment effects in settings with multiple time periods and staggered treatment adoption. The key innovation is using only "not-yet-treated" units as controls, avoiding the bias that can arise from using already-treated units. The authors provide group-time average treatment effects that can be aggregated in various ways. The accompanying R package `did` implements these methods.

**Verified**: Yes - ScienceDirect, arXiv, CRAN

---

### Sun and Abraham (2021)
**Citation**: Sun, Liyang, and Sarah Abraham. 2021. "Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects." *Journal of Econometrics* 225(2): 175-199.

**Summary**: This paper addresses problems with standard event study specifications (leads and lags of treatment) in the presence of heterogeneous treatment effects. The authors show that coefficients on specific leads or lags can be "contaminated" by effects from other periods, and apparent pre-trends can arise purely from treatment effect heterogeneity rather than violations of parallel trends. They propose an interaction-weighted estimator that avoids these problems. The Stata commands `eventstudyweights` and `eventstudyinteract` implement their methods.

**Verified**: Yes - ScienceDirect, arXiv, Zenodo (replication materials)

---

## Relevance for This Replication and Extension

### For Replication
The methodological papers (Goodman-Bacon, Callaway & Sant'Anna, Sun & Abraham) raise important questions about whether the Thompson et al. (2020) estimates could be affected by heterogeneous treatment effects across cohorts. A thorough replication might apply these newer methods as a robustness check.

### For Extension
The post-2020 studies (Amlani & Collitt, McGhee et al.) provide evidence that VBM effects during the pandemic were similar to pre-pandemic effects: modest turnout increases with no partisan advantage. This suggests the extension through 2024 may find similar patterns, though the unique context of post-COVID elections warrants investigation.

### Key Themes Across Literature
1. **Turnout effects are modest**: Most credible studies find 2-4 percentage point increases
2. **Partisan effects are null**: No consistent evidence that VBM advantages either party
3. **Selection matters**: Studies comparing VBM users to non-users suffer from selection bias
4. **Mobilization is limited**: VBM mainly changes how existing voters vote, not who votes
5. **Context matters**: Effects may differ between general and local elections, and across states
