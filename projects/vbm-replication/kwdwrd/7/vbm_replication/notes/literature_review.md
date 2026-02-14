# Literature Review: Vote-by-Mail Effects on Turnout and Partisan Outcomes

## Summary Table

| Authors | Year | Journal | Topic | Key Finding | Verified? |
|---------|------|---------|-------|-------------|-----------|
| Thompson, Wu, Yoder, Hall | 2020 | PNAS | VBM partisan effects | No partisan effects; ~2pp turnout increase | Yes |
| Gerber, Huber, Hill | 2013 | Political Science Research and Methods | WA all-mail turnout | 2-4pp turnout increase; reduces turnout gaps | Yes |
| Kousser, Mullin | 2007 | Political Analysis | CA VBM participation | Mixed effects; increases turnout in special elections | Yes |
| Southwell, Burchett | 2000 | American Politics Quarterly | OR all-mail turnout | ~10pp turnout increase (later disputed) | Yes |
| Gronke, Galanes-Rosenbaum, Miller, Toffey | 2008 | Annual Review of Political Science | Convenience voting review | Reviews early voting, VBM, absentee voting | Yes |
| Berinsky, Burns, Traugott | 2001 | Public Opinion Quarterly | Who votes by mail | VBM doesn't diversify electorate; habitual voters | Yes |
| Barber, Holbein | 2020 | Science Advances | WA/UT mandatory VBM | 1.8-2.9pp turnout increase; no partisan effect | Yes |
| Amlani, Collitt | 2022 | Election Law Journal | 2020 VBM policy effects | 2.6% turnout increase; no partisan advantage | Yes |
| Goodman-Bacon | 2021 | Journal of Econometrics | Staggered DiD methods | TWFE can be biased with staggered treatment | Yes |
| Callaway, Sant'Anna | 2021 | Journal of Econometrics | DiD with multiple periods | New estimator for heterogeneous treatment effects | Yes |
| Sun, Abraham | 2021 | Journal of Econometrics | Event study heterogeneity | TWFE event studies can have "forbidden comparisons" | Yes |

---

## 1. Foundational VBM Studies

### 1.1 Gerber, Huber, and Hill (2013)

**Citation**: Gerber, Alan S., Gregory A. Huber, and Seth J. Hill. 2013. "Identifying the Effect of All-Mail Elections on Turnout: Staggered Reform in the Evergreen State." *Political Science Research and Methods* 1(1): 91-116.

**Verified**: Yes - Available via [Cambridge Core](https://www.cambridge.org/core/journals/political-science-research-and-methods/article/abs/identifying-the-effect-of-allmail-elections-on-turnout-staggered-reform-in-the-evergreen-state/3725E51B9B7F331D77DC9B49130D7F7D)

**Summary**: This paper exploits Washington State's county-by-county rollout of all-mail elections from 2005-2011 to estimate causal effects on turnout. Using both county-level data and individual voter file records, the authors find:

- All-mail elections increase aggregate participation by 2-4 percentage points
- The reform increased turnout more for lower-participating registrants than for frequent voters
- This suggests VBM reduces turnout disparities between habitual and infrequent voters

**Methodology**: Difference-in-differences with county fixed effects and year fixed effects, exploiting staggered adoption timing. This is the same identification strategy used by Thompson et al. (2020).

**Relevance**: Provides the Washington data and empirical framework that Thompson et al. (2020) build upon.

---

### 1.2 Kousser and Mullin (2007)

**Citation**: Kousser, Thad, and Megan Mullin. 2007. "Does Voting by Mail Increase Participation? Using Matching to Analyze a Natural Experiment." *Political Analysis* 15(4): 428-445.

**Verified**: Yes - Available via [Cambridge Core](https://www.cambridge.org/core/journals/political-analysis/article/abs/does-voting-by-mail-increase-participation-using-matching-to-analyze-a-natural-experiment/D502CA1057D8EC73091E5ACE9E575994)

**Summary**: Uses nearest-neighbor matching on California precinct data to estimate VBM effects. Key findings:

- In general elections, VBM precincts had *lower* turnout than matched traditional precincts
- In special elections, VBM substantially increased turnout
- Results suggest selection effects in prior VBM studies may overstate positive effects

**Methodology**: Matching estimator pairing VBM precincts with similar traditional precincts within the same county.

**Relevance**: Provides early evidence from California and highlights importance of election type heterogeneity.

---

### 1.3 Southwell and Burchett (2000)

**Citation**: Southwell, Priscilla L., and Justin I. Burchett. 2000. "The Effect of All-Mail Elections on Voter Turnout." *American Politics Quarterly* 28(1): 72-79.

**Verified**: Yes - Available via [SAGE Journals](https://journals.sagepub.com/doi/10.1177/1532673X00028001004)

**Summary**: Analyzes Oregon's adoption of all-mail elections, finding approximately 10 percentage point increase in turnout. This was one of the most widely cited early studies on VBM effects.

**Important caveat**: Later research (Gronke and Miller 2012) attempted to replicate these findings and found evidence of a "novelty effect" - the large turnout gains appeared only in the first few VBM elections and diminished thereafter.

**Relevance**: Foundational study, though findings have been revised by subsequent research.

---

### 1.4 Gronke et al. (2008)

**Citation**: Gronke, Paul, Eva Galanes-Rosenbaum, Peter A. Miller, and Daniel Toffey. 2008. "Convenience Voting." *Annual Review of Political Science* 11: 437-455.

**Verified**: Yes - Available via [Annual Reviews](https://www.annualreviews.org/doi/abs/10.1146/annurev.polisci.11.053006.190912)

**Summary**: Comprehensive review article covering multiple forms of convenience voting: early in-person voting, voting by mail, absentee voting, and electronic voting. Key observations:

- By 2008, >30% of Americans used some form of convenience voting
- Research on VBM was unevenly distributed across voting methods
- Called for more rigorous research designs to identify causal effects

**Relevance**: Provides theoretical framework and literature context for VBM research.

---

### 1.5 Berinsky, Burns, and Traugott (2001)

**Citation**: Berinsky, Adam J., Nancy Burns, and Michael W. Traugott. 2001. "Who Votes by Mail?: A Dynamic Model of the Individual-Level Consequences of Voting-by-Mail Systems." *Public Opinion Quarterly* 65(2): 178-197.

**Verified**: Yes - Available via [Oxford Academic](https://academic.oup.com/poq/article-abstract/65/2/178/1877024)

**Summary**: Examines who uses VBM when it becomes available. Key findings:

- VBM adoption is concentrated among habitual voters
- VBM does not substantially change the demographic composition of the electorate
- VBM may not achieve goals of diversifying voter participation

**Relevance**: Provides theoretical expectations for why VBM might have limited partisan effects - if it primarily affects already-engaged voters who would vote anyway, compositional changes would be small.

---

## 2. Post-2020 Studies

### 2.1 Barber and Holbein (2020)

**Citation**: Barber, Michael, and John B. Holbein. 2020. "The Participatory and Partisan Impacts of Mandatory Vote-by-Mail." *Science Advances* 6(35): eabc7685.

**Verified**: Yes - Available via [Science Advances](https://www.science.org/doi/10.1126/sciadv.abc7685)

**Summary**: Uses 40+ million voting records from Washington and Utah to estimate VBM effects with multiple causal inference methods. Findings:

- Mandatory VBM increases turnout by 1.8-2.9 percentage points
- No effect on election outcomes at various levels of government
- Confirms Thompson et al. (2020) findings with larger sample

**Relevance**: Published simultaneously with Thompson et al., provides independent confirmation of null partisan effects.

---

### 2.2 Amlani and Collitt (2022)

**Citation**: Amlani, Sharif, and Samuel Collitt. 2022. "The Impact of Vote-By-Mail Policy on Turnout and Vote Share in the 2020 Election." *Election Law Journal* 21(2): 135-149.

**Verified**: Yes - Available via [Liebert Pub](https://www.liebertpub.com/doi/full/10.1089/elj.2021.0015)

**Summary**: Uses difference-in-differences to examine how 2020 pandemic-era VBM policy changes affected turnout and vote share. Key findings:

- Counties sending mail ballots to all voters saw 2.6% higher turnout
- No evidence that easier VBM conferred partisan advantage
- Lesser reforms (no-excuse absentee) may have actually reduced turnout by ~1.4%

**Relevance**: Extends VBM research to the 2020 pandemic context; tests whether null partisan findings hold under extraordinary circumstances.

---

### 2.3 COVID-19 and Partisan Polarization of VBM

**Citation**: Stewart III, Charles. 2020. "America's Electorate is Increasingly Polarized Along Partisan Lines About Voting by Mail During the COVID-19 Crisis." *PNAS* 117(40): 24640-24642.

**Verified**: Yes - Available via [PNAS](https://www.pnas.org/doi/10.1073/pnas.2008023117)

**Summary**: Documents how VBM became a partisan issue during the pandemic:

- ~10 percentage point partisan gap in VBM preferences in April 2020
- Gap doubled to ~20 percentage points by June 2020
- Party leader statements (especially President Trump's) influenced these attitudes

**Relevance**: Explains why the extension period (2020-2024) may show different dynamics than the original study period (1996-2018).

---

## 3. Methodological Literature on Staggered Difference-in-Differences

### 3.1 Goodman-Bacon (2021)

**Citation**: Goodman-Bacon, Andrew. 2021. "Difference-in-Differences with Variation in Treatment Timing." *Journal of Econometrics* 225(2): 254-277.

**Verified**: Yes - Available via [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0304407621001445)

**Summary**: Proves that two-way fixed effects (TWFE) difference-in-differences estimators with staggered treatment timing are weighted averages of many 2×2 DD comparisons. Key insights:

- With heterogeneous treatment effects over time, TWFE can produce biased estimates
- Some comparisons use already-treated units as controls ("forbidden comparisons")
- Weights can even be negative in some cases

**Relevance**: Thompson et al. (2020) use TWFE with staggered timing. Understanding Goodman-Bacon decomposition helps interpret their estimates.

---

### 3.2 Callaway and Sant'Anna (2021)

**Citation**: Callaway, Brantly, and Pedro H.C. Sant'Anna. 2021. "Difference-in-Differences with Multiple Time Periods." *Journal of Econometrics* 225(2): 200-230.

**Verified**: Yes - Available via [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0304407620303948)

**Summary**: Proposes estimators for settings with multiple time periods and variation in treatment timing that avoid the problems identified by Goodman-Bacon. Key features:

- Uses only not-yet-treated or never-treated units as controls
- Allows for heterogeneous effects across cohorts and time
- Provides aggregation schemes to summarize overall effects

**Relevance**: Provides modern alternative to TWFE that could be used as robustness check for the extension analysis.

---

### 3.3 Sun and Abraham (2021)

**Citation**: Sun, Liyang, and Sarah Abraham. 2021. "Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects." *Journal of Econometrics* 225(2): 175-199.

**Verified**: Yes - Available via [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S030440762030378X)

**Summary**: Shows that event study specifications (with leads and lags) using TWFE can be contaminated when treatment effects are heterogeneous. Key points:

- Coefficient on a given lead/lag can include effects from other periods
- Apparent pre-trends can arise solely from treatment effect heterogeneity
- Propose "interaction-weighted" estimator free of contamination

**Relevance**: If we estimate event studies for the extension analysis, Sun-Abraham methods may provide cleaner estimates than standard TWFE event studies.

---

## 4. Synthesis and Implications for Extension

### Consensus Findings from Literature

1. **Turnout effects**: VBM increases turnout by approximately 2-4 percentage points (Gerber et al. 2013; Thompson et al. 2020; Barber & Holbein 2020)

2. **Partisan effects**: No consistent evidence that VBM advantages either party in "normal times" (Thompson et al. 2020; Barber & Holbein 2020; Amlani & Collitt 2022)

3. **Compositional effects**: VBM primarily affects already-engaged voters; limited effect on diversifying electorate (Berinsky et al. 2001)

### Open Questions for Extension

1. **Post-COVID dynamics**: Did partisan polarization around VBM in 2020 change the causal effects?

2. **Methodological robustness**: Do modern staggered DiD estimators (Callaway-Sant'Anna, Sun-Abraham) produce different conclusions than TWFE?

3. **California continued rollout**: Do effects of continued VCA adoption (2020-2024) differ from early adoption (2018)?

### Limitations of Existing Literature

1. Most studies focus on pre-2020 period
2. Limited research on interaction between VBM and pandemic conditions
3. Modern DiD methods not yet widely applied to VBM research
