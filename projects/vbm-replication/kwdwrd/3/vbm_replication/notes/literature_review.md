# Literature Review: Vote-by-Mail Effects on Turnout and Partisan Outcomes

## Summary Table

| Authors | Year | Journal | Topic | Key Finding | Verified? |
|---------|------|---------|-------|-------------|-----------|
| Gerber, Huber, Hill | 2013 | Political Science Research and Methods | VBM turnout effects (Washington) | VBM increases turnout 2-4pp; reduces turnout disparities | Yes |
| Kousser, Mullin | 2007 | Political Analysis | VBM turnout effects (California) | No turnout increase in general elections; increases in special elections | Yes |
| Southwell, Burchett | 2000 | American Politics Quarterly | VBM turnout effects (Oregon) | VBM increases turnout ~10pp | Yes |
| Gronke et al. | 2008 | Annual Review of Political Science | Convenience voting review | Mixed evidence; convenience voting does not draw new voters | Yes |
| Berinsky, Burns, Traugott | 2001 | Public Opinion Quarterly | Who votes by mail | VBM spread without empirical evaluation of impact | Yes |
| Goodman-Bacon | 2021 | Journal of Econometrics | Staggered DiD methodology | TWFE can be biased with treatment timing variation | Yes |
| Callaway, Sant'Anna | 2021 | Journal of Econometrics | Staggered DiD methodology | Proposes alternative estimator for multiple time periods | Yes |
| Sun, Abraham | 2021 | Journal of Econometrics | Event study methodology | Lead/lag coefficients contaminated with heterogeneous effects | Yes |
| Lockhart et al. | 2020 | PNAS | Partisan polarization on VBM during COVID | 10-20pp partisan gap in VBM preferences emerged | Yes |
| Amlani, Collitt | 2022 | Election Law Journal | VBM effects in 2020 | 2.6pp turnout increase; no partisan advantage | Yes |

---

## Foundational VBM Studies

### Gerber, Huber, and Hill (2013)
**Citation**: Gerber, Alan S., Gregory A. Huber, and Seth J. Hill. 2013. "Identifying the Effect of All-Mail Elections on Turnout: Staggered Reform in the Evergreen State." *Political Science Research and Methods* 1(1): 91-116.

**Design**: Exploits staggered county-level adoption of all-mail elections in Washington State.

**Findings**:
- All-mail elections increase aggregate turnout by 2-4 percentage points
- Reform increased turnout more for lower-participating registrants than frequent voters
- VBM reduces turnout disparities between habitual and occasional voters

**Relevance**: Closest methodological precursor to Thompson et al. (2020). Uses similar staggered DiD design in one of the same states.

---

### Kousser and Mullin (2007)
**Citation**: Kousser, Thad, and Megan Mullin. 2007. "Does Voting by Mail Increase Participation? Using Matching to Analyze a Natural Experiment." *Political Analysis* 15(4): 428-445.

**Design**: Uses matching methods with California data where voters are quasi-randomly assigned to vote-by-mail in some precincts.

**Findings**:
- VBM does **not** increase turnout in general elections
- Voters assigned to vote by mail turn out at **lower** rates than polling-place voters
- VBM can increase turnout in low-salience special elections

**Relevance**: Provides cautionary evidence that VBM effects may depend on election type. Challenges assumption that VBM always increases turnout.

---

### Southwell and Burchett (2000)
**Citation**: Southwell, Priscilla L., and Justin I. Burchett. 2000. "The Effect of All-Mail Elections on Voter Turnout." *American Politics Quarterly* 28(1): 72-79.

**Design**: Analyzes 48 statewide elections in Oregon before and after VBM adoption.

**Findings**:
- Oregon's all-mail system increased turnout by approximately 10 percentage points
- Early influential study that supported VBM expansion

**Note**: Later work by Gronke and Miller (2012) could not replicate this finding; suggested the effect may have been a novelty effect that faded over time.

---

### Gronke et al. (2008)
**Citation**: Gronke, Paul, Eva Galanes-Rosenbaum, Peter A. Miller, and Daniel Toffey. 2008. "Convenience Voting." *Annual Review of Political Science* 11: 437-455.

**Design**: Comprehensive review of convenience voting research (early voting, VBM, absentee voting).

**Findings**:
- More than 30% of Americans used convenience voting by 2008
- Earlier studies found no increase in turnout from postal voting
- VBM does not appear to draw in new voters or appeal to disempowered populations
- Voters using early/absentee voting tend to be more partisan and ideologically extreme

**Relevance**: Provides theoretical framework for understanding why VBM might not dramatically change the electorate.

---

### Berinsky, Burns, and Traugott (2001)
**Citation**: Berinsky, Adam J., Nancy Burns, and Michael W. Traugott. 2001. "Who Votes by Mail? A Dynamic Model of the Individual-Level Consequences of Voting-by-Mail Systems." *Public Opinion Quarterly* 65(2): 178-197.

**Design**: Individual-level analysis of VBM adoption patterns.

**Findings**:
- VBM spread across the U.S. largely without empirical evaluation
- Individual-level factors matter most for turnout
- Need to control for individual characteristics when evaluating VBM effects

**Relevance**: Early warning that selection effects complicate VBM evaluation.

---

## Post-2020 / COVID-Era Studies

### Lockhart et al. (2020)
**Citation**: Lockhart, Mackenzie, Seth J. Hill, Jennifer Merolla, Mindy Romero, and Thad Kousser. 2020. "America's Electorate Is Increasingly Polarized Along Partisan Lines About Voting by Mail During the COVID-19 Crisis." *Proceedings of the National Academy of Sciences* 117(40): 24640-24642.

**Design**: Two nationally representative surveys in April and June 2020 (N = 5,612 and 5,818).

**Findings**:
- Nearly 10pp partisan gap in VBM preferences in April 2020
- Gap doubled to nearly 20pp by June 2020
- Democrats much more likely to prefer mail voting than Republicans
- Support for national VBM legislation became increasingly polarized

**Relevance**: Documents that VBM became a partisan issue during COVID-19, which may affect the extension analysis. The original Thompson et al. findings came from "normal times" - the post-2020 context is fundamentally different.

---

### Amlani and Collitt (2022)
**Citation**: Amlani, Sharif, and Samuel Collitt. 2022. "The Impact of Vote-By-Mail Policy on Turnout and Vote Share in the 2020 Election." *Election Law Journal* 21(2): 135-149.

**Design**: Two-period difference-in-differences comparing counties that changed VBM policy for 2020 vs. those that did not.

**Findings**:
- Counties that mailed ballots to all voters saw 2.6% higher turnout
- **No evidence of partisan advantage** from VBM expansion
- Lesser reforms (no-excuse absentee, mailing applications) may have reduced turnout

**Relevance**: Most directly relevant to the extension. Confirms null partisan effects held during COVID-19 election, though uses different research design than Thompson et al.

---

## Methodological Papers on Staggered Difference-in-Differences

### Goodman-Bacon (2021)
**Citation**: Goodman-Bacon, Andrew. 2021. "Difference-in-Differences with Variation in Treatment Timing." *Journal of Econometrics* 225(2): 254-277.

**Key Insight**: Shows that two-way fixed effects (TWFE) DiD estimators are weighted averages of many "2×2 DiD" comparisons. With staggered adoption:
- Some comparisons use already-treated units as controls
- Weights depend on group sizes and timing
- Can produce biased estimates if treatment effects are heterogeneous over time

**Relevance**: Thompson et al. use standard TWFE. The extension should consider whether Goodman-Bacon decomposition reveals problematic comparisons.

---

### Callaway and Sant'Anna (2021)
**Citation**: Callaway, Brantly, and Pedro H.C. Sant'Anna. 2021. "Difference-in-Differences with Multiple Time Periods." *Journal of Econometrics* 225(2): 200-230.

**Key Insight**: Proposes group-time average treatment effects (ATT(g,t)) that avoid problematic comparisons. Only compares:
- Treated units to never-treated units, OR
- Treated units to not-yet-treated units

Provides methods for aggregating to summary parameters.

**Relevance**: Could use Callaway-Sant'Anna estimator as robustness check in extension.

---

### Sun and Abraham (2021)
**Citation**: Sun, Liyang, and Sarah Abraham. 2021. "Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects." *Journal of Econometrics* 225(2): 175-199.

**Key Insight**: Event study coefficients from TWFE can be contaminated by effects from other periods when treatment effects are heterogeneous. Proposes interaction-weighted estimator that avoids contamination.

**Relevance**: Event study figures in VBM replication should consider whether standard TWFE event study is appropriate or if Sun-Abraham correction needed.

---

## Key Themes from Literature

### 1. Modest Turnout Effects
Most rigorous studies find VBM increases turnout by 2-4 percentage points at most. Larger effects (like Southwell & Burchett's 10pp) may reflect novelty or methodological issues.

### 2. Null or Minimal Partisan Effects
No rigorous study finds substantial partisan advantages from VBM. This includes both pre-COVID (Thompson et al.) and COVID-era (Amlani & Collitt) research.

### 3. Selection into VBM
Voters who use VBM tend to be those who would have voted anyway. VBM changes **how** people vote more than **whether** they vote.

### 4. Context Matters
- VBM effects may differ for general vs. special elections
- Effects may differ in "normal times" vs. during a pandemic
- State-specific contexts (registration systems, political culture) may matter

### 5. Methodological Concerns
Recent econometric literature raises concerns about TWFE with staggered adoption. The extension should:
- Consider Goodman-Bacon decomposition
- Potentially use Callaway-Sant'Anna or Sun-Abraham estimators
- Test robustness to alternative specifications

---

## Implications for Extension

1. **Expect null partisan effects** based on prior literature, but test formally
2. **Expect modest turnout effects** (~2pp) if any new VBM adoption occurs
3. **COVID-19 changed the context** - VBM became a partisan issue
4. **Limited new variation** - Most states fully adopted VBM by 2020
5. **Consider modern DiD methods** as robustness checks
