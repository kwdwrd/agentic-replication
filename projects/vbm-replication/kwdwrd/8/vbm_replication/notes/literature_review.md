# Literature Review: Vote-by-Mail Effects

## Summary Table of Verified Citations

| Authors | Year | Journal | Topic | Key Finding | Verified |
|---------|------|---------|-------|-------------|----------|
| Gerber, Huber, and Hill | 2013 | Political Science Research and Methods | Washington State VBM and turnout | All-mail elections increase turnout by 2-4 pp; reduces turnout disparities | Yes |
| Kousser and Mullin | 2007 | Political Analysis | VBM and participation in California | VBM does not increase turnout in general elections; may increase turnout in low-salience elections | Yes |
| Southwell and Burchett | 2000 | American Politics Quarterly | Oregon all-mail elections | Reported 10 pp turnout increase (later questioned by replication studies) | Yes |
| Gronke et al. | 2008 | Annual Review of Political Science | Convenience voting review | Comprehensive review of early voting, VBM, and other convenience measures | Yes |
| Berinsky, Burns, and Traugott | 2001 | Public Opinion Quarterly | Who uses VBM | Dynamic model of individual-level VBM usage; examines stratification of electorate | Yes |
| Goodman-Bacon | 2021 | Journal of Econometrics | Staggered DiD methodology | TWFE equals weighted average of 2x2 DiDs; warns of potential bias with heterogeneous effects | Yes |
| Callaway and Sant'Anna | 2021 | Journal of Econometrics | DiD with multiple periods | Proposes estimators robust to heterogeneous treatment effects | Yes |
| Sun and Abraham | 2021 | Journal of Econometrics | Event study estimation | Shows standard event study coefficients can be contaminated; proposes alternative estimator | Yes |
| Amlani and Collitt | 2022 | Election Law Journal | 2020 election VBM effects | Counties sending mail ballots had 2.6% higher turnout; no partisan advantage | Yes |

---

## Foundational VBM Studies

### Gerber, Huber, and Hill (2013)

**Citation**: Gerber, Alan S., Gregory A. Huber, and Seth J. Hill. 2013. "Identifying the Effect of All-Mail Elections on Turnout: Staggered Reform in the Evergreen State." *Political Science Research and Methods* 1(1): 91-116.

**Summary**: This paper is foundational to the Thompson et al. (2020) replication. The authors exploit Washington State's county-by-county adoption of all-mail elections from 2005-2011 to estimate causal effects on turnout. Using both aggregate county-level data and individual-level voter file records, they find:

- **Aggregate turnout**: All-mail elections increase participation by 2-4 percentage points
- **Distributional effects**: Reform increases turnout more for lower-participating registrants than frequent voters
- **Implication**: All-mail voting reduces turnout disparities between habitual and occasional voters

**Methodology**: Difference-in-differences exploiting staggered county-level adoption within a single state.

**Relevance**: Provides the Washington data used in Thompson et al. (2020) and establishes the staggered DiD approach.

---

### Kousser and Mullin (2007)

**Citation**: Kousser, Thad, and Megan Mullin. 2007. "Does Voting by Mail Increase Participation? Using Matching to Analyze a Natural Experiment." *Political Analysis* 15(4): 428-445.

**Summary**: The authors challenge optimistic claims about VBM's turnout effects by analyzing a California natural experiment where voters were quasi-randomly assigned to mail vs. polling place voting within the same elections.

**Key Findings**:
- **General elections**: Voters assigned to vote by mail turn out at *lower* rates than those assigned to polling places
- **Special/local elections**: VBM can increase turnout in otherwise low-participation contests
- **Selection effects**: Previous studies showing positive VBM effects may reflect selection (who chooses absentee voting) rather than causal effects

**Methodology**: Matching methods to construct comparable treatment and control groups.

**Implication**: The effects of VBM may depend heavily on election context and voter characteristics.

---

### Southwell and Burchett (2000)

**Citation**: Southwell, Priscilla L., and Justin I. Burchett. 2000. "The Effect of All-Mail Elections on Voter Turnout." *American Politics Quarterly* 28(1): 72-79.

**Summary**: An early and widely cited study of Oregon's all-mail election system, analyzing 48 statewide elections.

**Key Finding**: Reported that Oregon's all-mail system increased turnout by approximately 10 percentage points.

**Important Caveat**: Subsequent replication by Gronke and Miller (2012, *American Politics Research*) was unable to reproduce this finding. They found evidence of a "novelty effect" in early VBM elections that dissipated over time, and consistent effects only in special elections.

**Relevance**: Illustrates the importance of replication and the potential for initial estimates to overstate effects.

---

### Gronke, Galanes-Rosenbaum, Miller, and Toffey (2008)

**Citation**: Gronke, Paul, Eva Galanes-Rosenbaum, Peter A. Miller, and Daniel Toffey. 2008. "Convenience Voting." *Annual Review of Political Science* 11: 437-455.

**Summary**: A comprehensive review article covering all forms of convenience voting (early in-person, VBM, absentee, electronic voting) used by over 30% of American voters.

**Key Points**:
- Convenience voting effects are modest and context-dependent
- VBM may mobilize some voters while demobilizing others
- The social aspects of polling places may matter for turnout
- Effects likely vary by voter type, election type, and implementation

**Relevance**: Provides theoretical framework for understanding heterogeneous VBM effects.

---

### Berinsky, Burns, and Traugott (2001)

**Citation**: Berinsky, Adam J., Nancy Burns, and Michael W. Traugott. 2001. "Who Votes by Mail?: A Dynamic Model of the Individual-Level Consequences of Voting-by-Mail Systems." *Public Opinion Quarterly* 65(2): 178-197.

**Summary**: Examines the individual-level determinants of VBM usage and its consequences for electorate composition.

**Key Findings**:
- VBM is disproportionately used by voters who were already likely to participate
- VBM may increase turnout inequality rather than reduce it
- The electorate may become more stratified by socioeconomic status under VBM

**Implication**: Even if VBM increases aggregate turnout, the compositional effects matter for representation.

---

## Post-2020 Studies

### Amlani and Collitt (2022)

**Citation**: Amlani, Sharif, and Samuel Collitt. 2022. "The Impact of Vote-By-Mail Policy on Turnout and Vote Share in the 2020 Election." *Election Law Journal: Rules, Politics, and Policy* 21(1): 68-82.

**Summary**: Examines how COVID-19-induced VBM policy changes affected turnout and presidential vote share in 2020.

**Methodology**: Two-period difference-in-differences comparing counties that expanded VBM access to those that did not.

**Key Findings**:
- Counties that sent all registered voters mail ballots experienced 2.6% higher turnout
- Lesser reforms (no-excuse absentee without automatic mailing) may have reduced turnout by 1.4%
- **No evidence that VBM expansion conferred partisan advantage**

**Relevance**: Extends the null partisan effects finding to the COVID-19 context.

**Replication materials**: Available on Harvard Dataverse.

---

## Methodological Papers on Staggered Difference-in-Differences

### Goodman-Bacon (2021)

**Citation**: Goodman-Bacon, Andrew. 2021. "Difference-in-Differences with Variation in Treatment Timing." *Journal of Econometrics* 225(2): 254-277.

**Summary**: A foundational methodological paper showing that the standard two-way fixed effects (TWFE) estimator in staggered DiD settings equals a weighted average of all possible 2×2 DiD comparisons.

**Key Insight**: When treatment effects are heterogeneous across cohorts or over time, TWFE can produce misleading estimates because:
- Early-treated units serve as controls for later-treated units
- Weights can be negative in some comparisons
- The estimand may not correspond to any meaningful average treatment effect

**Implication for VBM Studies**: Thompson et al. (2020) use standard TWFE. If VBM effects differ across states or adoption cohorts, Goodman-Bacon's concerns apply. However, the paper's null partisan findings make this less concerning (heterogeneous nulls still aggregate to null).

---

### Callaway and Sant'Anna (2021)

**Citation**: Callaway, Brantly, and Pedro H.C. Sant'Anna. 2021. "Difference-in-Differences with Multiple Time Periods." *Journal of Econometrics* 225(2): 200-230.

**Summary**: Proposes alternative estimators for staggered DiD that are robust to treatment effect heterogeneity.

**Key Contributions**:
- Identifies group-time average treatment effects
- Allows not-yet-treated units as controls (often more comparable)
- Provides aggregation schemes for summarizing heterogeneous effects
- Accompanying R package (`did`) for implementation

**Relevance**: Could be used to assess robustness of Thompson et al. findings to heterogeneity concerns.

---

### Sun and Abraham (2021)

**Citation**: Sun, Liyang, and Sarah Abraham. 2021. "Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects." *Journal of Econometrics* 225(2): 175-199.

**Summary**: Shows that standard event study specifications (leads and lags around treatment) can produce contaminated coefficients when treatment effects are heterogeneous.

**Key Problem**: A coefficient on a given lead or lag can be contaminated by effects from other periods. Apparent pre-trends can arise solely from treatment effect heterogeneity, not parallel trends violations.

**Solution**: Proposes an interaction-weighted estimator free of contamination.

**Relevance**: Important for interpreting event study plots in VBM research.

---

## Summary of Literature Findings

### Consensus Points

1. **Turnout effects**: VBM modestly increases overall turnout, typically by 2-4 percentage points, though effects are context-dependent.

2. **Partisan effects**: The weight of evidence suggests VBM does not systematically advantage either party. This holds across:
   - Normal times (Thompson et al. 2020)
   - COVID-19 context (Amlani and Collitt 2022)

3. **Compositional effects**: VBM may primarily mobilize voters who were already likely to participate, potentially not improving representativeness.

### Open Questions

1. **Long-run effects**: Do turnout gains persist or reflect novelty?

2. **Post-COVID dynamics**: Has the politicization of VBM changed its effects?

3. **Heterogeneity**: Do effects vary by voter demographics, election type, or implementation details?

4. **California VCA**: The continued rollout provides new variation for testing null partisan effects.

---

## References

Amlani, Sharif, and Samuel Collitt. 2022. "The Impact of Vote-By-Mail Policy on Turnout and Vote Share in the 2020 Election." *Election Law Journal* 21(1): 68-82.

Berinsky, Adam J., Nancy Burns, and Michael W. Traugott. 2001. "Who Votes by Mail?: A Dynamic Model of the Individual-Level Consequences of Voting-by-Mail Systems." *Public Opinion Quarterly* 65(2): 178-197.

Callaway, Brantly, and Pedro H.C. Sant'Anna. 2021. "Difference-in-Differences with Multiple Time Periods." *Journal of Econometrics* 225(2): 200-230.

Gerber, Alan S., Gregory A. Huber, and Seth J. Hill. 2013. "Identifying the Effect of All-Mail Elections on Turnout: Staggered Reform in the Evergreen State." *Political Science Research and Methods* 1(1): 91-116.

Goodman-Bacon, Andrew. 2021. "Difference-in-Differences with Variation in Treatment Timing." *Journal of Econometrics* 225(2): 254-277.

Gronke, Paul, Eva Galanes-Rosenbaum, Peter A. Miller, and Daniel Toffey. 2008. "Convenience Voting." *Annual Review of Political Science* 11: 437-455.

Kousser, Thad, and Megan Mullin. 2007. "Does Voting by Mail Increase Participation? Using Matching to Analyze a Natural Experiment." *Political Analysis* 15(4): 428-445.

Southwell, Priscilla L., and Justin I. Burchett. 2000. "The Effect of All-Mail Elections on Voter Turnout." *American Politics Quarterly* 28(1): 72-79.

Sun, Liyang, and Sarah Abraham. 2021. "Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects." *Journal of Econometrics* 225(2): 175-199.

Thompson, Daniel M., Jennifer A. Wu, Jesse Yoder, and Andrew B. Hall. 2020. "Universal Vote-by-Mail Has No Impact on Partisan Turnout or Vote Share." *Proceedings of the National Academy of Sciences* 117(25): 14052-14056.
