# Literature Review: Vote-by-Mail and Electoral Outcomes

## Summary Table of Verified Citations

| Authors | Year | Journal | Topic | Key Finding | Verified? |
|---------|------|---------|-------|-------------|-----------|
| Gerber, Huber, & Hill | 2013 | Political Science Research and Methods | WA VBM turnout effects | VBM increases turnout 2-4 pp; reduces disparities | Yes |
| Kousser & Mullin | 2007 | Political Analysis | VBM and participation | VBM increases turnout in mail ballot elections | Yes |
| Southwell & Burchett | 2000 | American Politics Quarterly | Oregon VBM turnout | VBM increased OR turnout ~10 pp (but see Gronke & Miller critique) | Yes |
| Gronke et al. | 2008 | Annual Review of Political Science | Convenience voting review | Comprehensive review of early/mail voting research | Yes |
| Berinsky, Burns, & Traugott | 2001 | Public Opinion Quarterly | Who votes by mail | Examines individual-level VBM adoption patterns | Yes |
| Thompson et al. | 2020 | PNAS | VBM partisan effects | Null partisan effects, +2pp turnout | Yes |
| Goodman-Bacon | 2021 | Journal of Econometrics | Staggered DiD methods | TWFE can be biased with treatment timing variation | Yes |
| Callaway & Sant'Anna | 2021 | Journal of Econometrics | DiD with multiple periods | Alternative estimators for staggered adoption | Yes |
| Sun & Abraham | 2021 | Journal of Econometrics | Event study heterogeneity | Event study coefficients can be contaminated | Yes |
| Amlani & Collitt | 2022 | Election Law Journal | 2020 VBM effects | +2.6% turnout from universal VBM; no partisan effect | Yes |
| McGhee, Paluch, & Romero | 2022 | Research & Politics | 2020 VBM policy | +5.6% turnout from mailing ballots; no partisan effect | Yes |

---

## Foundational VBM Studies

### Gerber, Huber, and Hill (2013)
**"Identifying the Effect of All-Mail Elections on Turnout: Staggered Reform in the Evergreen State"**
*Political Science Research and Methods*, 1(1): 91-116.

This study exploits Washington State's staggered county-level VBM adoption—the same variation used in Thompson et al. (2020). Using both aggregate county data and individual-level voter file records, Gerber et al. find:
- All-mail elections increase participation by 2-4 percentage points
- Effects are larger for lower-propensity voters, reducing turnout disparities
- The staggered rollout provides credible causal identification

**Relevance**: This is the primary methodological predecessor to Thompson et al., using the same Washington data and similar diff-in-diff approach. Thompson et al. extend this by adding California and Utah and examining partisan outcomes.

### Kousser and Mullin (2007)
**"Does Voting by Mail Increase Participation? Using Matching to Analyze a Natural Experiment"**
*Political Analysis*, 15(4): 428-445.

Kousser and Mullin use a matching design exploiting quasi-random assignment to mail ballot elections in California. They address selection bias concerns in earlier VBM research by comparing demographically similar voters assigned to different voting modes.

**Key findings**:
- VBM increases turnout, particularly in lower-salience elections
- Selection effects explain much of the apparent VBM advantage in observational studies
- Results support modest positive turnout effects

### Southwell and Burchett (2000)
**"The Effect of All-Mail Elections on Voter Turnout"**
*American Politics Quarterly*, 28(1): 72-79.

This early study of Oregon's VBM system reported a 10 percentage point increase in turnout. However, subsequent research has questioned these estimates:
- Gronke and Miller (2012) failed to replicate the finding with extended data
- The effect may reflect a "novelty" effect from initial adoption
- Consistent effects found only in special elections

**Relevance**: Illustrates early optimism about VBM turnout effects that later research has moderated.

### Gronke et al. (2008)
**"Convenience Voting"**
*Annual Review of Political Science*, 11: 437-455.

This comprehensive review examines all forms of convenience voting (early voting, VBM, no-excuse absentee). Key conclusions:
- Evidence on turnout effects is mixed
- VBM appears to have modest positive effects
- More research needed on partisan and compositional effects

**Relevance**: Establishes the theoretical framework for understanding convenience voting reforms.

### Berinsky, Burns, and Traugott (2001)
**"Who Votes by Mail?: A Dynamic Model of the Individual-Level Consequences of Voting-by-Mail Systems"**
*Public Opinion Quarterly*, 65(2): 178-197.

This individual-level analysis examines who adopts VBM when it becomes available:
- Higher-propensity voters more likely to use VBM initially
- Raises concerns about compositional effects
- Questions whether VBM reaches low-propensity voters

**Relevance**: Highlights the distinction between who *uses* VBM vs. how VBM affects *aggregate* outcomes.

---

## Post-2020 Studies

### Amlani and Collitt (2022)
**"The Impact of Vote-By-Mail Policy on Turnout and Vote Share in the 2020 Election"**
*Election Law Journal*, 21(2).

Using a two-period difference-in-differences design comparing 2016 to 2020, this study examines emergency VBM expansions during COVID-19:
- Counties mailing ballots to all voters saw 2.6% higher turnout
- No evidence of partisan advantage from VBM expansion
- Lesser reforms (no-excuse absentee) had smaller or negative effects

**Relevance**: Directly tests whether Thompson et al.'s null partisan findings hold during COVID-19.

### McGhee, Paluch, and Romero (2022)
**"Vote-by-mail policy and the 2020 presidential election"**
*Research & Politics*, 9(2): 1-15.

Examining county-level data across states with varying VBM policies:
- Universal VBM increased turnout by 5.6 percentage points on average
- Effects largest in counties with little prior mail voting experience
- Effects larger for infrequent voters (6-8 pp)
- No robust partisan effects

**Relevance**: Confirms turnout effects and null partisan effects in 2020 context.

### Partisan Polarization on VBM (Stewart et al., 2020)
**"America's electorate is increasingly polarized along partisan lines about voting by mail during the COVID-19 crisis"**
*PNAS*, 117(40): 24640-24642.

While not about VBM *effects*, this study documents partisan polarization in VBM *attitudes*:
- 10 pp Democrat-Republican gap in VBM preference in April 2020
- Gap doubled to 20 pp by June 2020
- COVID-19 risk perceptions drove partisan differences

**Relevance**: Explains why VBM became controversial despite null partisan effects on outcomes.

---

## Methodological Literature on Staggered Diff-in-Diff

### Goodman-Bacon (2021)
**"Difference-in-differences with variation in treatment timing"**
*Journal of Econometrics*, 225(2): 254-277.

This paper shows that two-way fixed effects (TWFE) estimators with staggered adoption:
- Are weighted averages of all possible 2×2 DiD comparisons
- Can include "bad" comparisons (already-treated as controls)
- May be biased with heterogeneous treatment effects

**Relevance**: Thompson et al. use TWFE. Goodman-Bacon decomposition could reveal whether estimates rely on problematic comparisons.

### Callaway and Sant'Anna (2021)
**"Difference-in-Differences with multiple time periods"**
*Journal of Econometrics*, 225(2): 200-230.

Proposes alternative estimators that:
- Avoid using already-treated units as controls
- Allow for heterogeneous effects across cohorts and time
- Provide group-time average treatment effects

**Relevance**: Could be applied to Thompson et al. data as robustness check.

### Sun and Abraham (2021)
**"Estimating dynamic treatment effects in event studies with heterogeneous treatment effects"**
*Journal of Econometrics*, 225(2): 175-199.

Shows that event study coefficients from TWFE regressions:
- Can be "contaminated" by effects from other periods
- May show spurious pre-trends from treatment effect heterogeneity
- Proposes interaction-weighted estimators

**Relevance**: Thompson et al. report event studies. Sun-Abraham estimator could provide robustness check.

---

## Summary of Evidence

### On Turnout Effects
The literature consistently finds **modest positive turnout effects** of VBM:
- Pre-2020 estimates: 2-4 pp (Gerber et al., Thompson et al.)
- 2020 estimates: 2.6-5.6 pp (Amlani & Collitt, McGhee et al.)
- Effects may be larger for low-propensity voters

### On Partisan Effects
Evidence strongly supports **null partisan effects**:
- Thompson et al. (2020): No effect on Dem turnout share or vote share
- Amlani & Collitt (2022): No partisan advantage in 2020
- McGhee et al. (2022): No robust partisan effects in 2020

### Key Methodological Considerations
1. Selection bias: Who chooses to use VBM vs. aggregate effects of availability
2. Staggered adoption: TWFE may be biased; newer estimators available
3. Context dependence: Effects may differ across states, elections, time periods
