# Literature Review

## Summary Table

| Authors | Year | Journal | Topic | Key Finding | Verified? |
|---------|------|---------|-------|-------------|-----------|
| Southwell and Burchett | 2000 | *American Politics Quarterly* 28(1): 72–79 | Oregon all-mail election turnout | All-mail elections increased turnout by ~10 pp in Oregon statewide elections; subsequent work attributed much of this to novelty effects | Yes |
| Berinsky, Burns, and Traugott | 2001 | *Public Opinion Quarterly* 65(2): 178–197 | Who votes by mail in Oregon | VBM increases turnout by retaining current voters rather than mobilizing nonvoters; does not change partisan composition but reinforces resource stratification of electorate | Yes |
| Kousser and Mullin | 2007 | *Political Analysis* 15(4): 428–445 | VBM and participation via natural experiment | Voters quasi-randomly assigned to VBM turned out at *lower* rates in regular elections; VBM increased turnout in special/low-salience elections | Yes |
| Gronke, Galanes-Rosenbaum, Miller, and Toffey | 2008 | *Annual Review of Political Science* 11: 437–455 | Convenience voting review | Comprehensive review finding convenience voting (early, absentee, VBM) used by 30%+ of voters; most evidence shows little to no effect on overall turnout despite theoretical expectations | Yes |
| Gerber, Huber, and Hill | 2013 | *Political Science Research and Methods* 1(1): 91–116 | Washington State VBM staggered adoption | All-mail voting increased turnout by 2–4 pp using cross-sectional and temporal variation in WA county adoption; larger gains for infrequent voters | Yes |
| Barber and Holbein | 2020 | *Science Advances* 6(35): eabc7685 | Mandatory VBM participatory and partisan impacts | Mandatory VBM increases turnout by 2–3 pp but does not advantage either party; uses nationwide county data (1992–2018) and 40M+ individual voter records from WA and UT | Yes |
| Thompson, Wu, Yoder, and Hall | 2020 | *PNAS* 117(25): 14052–14056 | Universal VBM partisan effects (CA, UT, WA) | Null partisan effects on turnout composition and vote share; modest ~2 pp turnout increase; staggered county-level DiD design | Yes |
| Lockhart, Hill, Merolla, Romero, and Kousser | 2020 | *PNAS* 117(40): 24640–24642 | Partisan polarization over VBM during COVID | ~10 pp partisan gap in VBM preference in April 2020 doubled to ~20 pp by June 2020; exposure to COVID projections widened gap | Yes |
| Hopkins, Meredith, Chainani, Olin, and Tse | 2021 | *PNAS* 118(4): e2021022118 | Field experiment encouraging VBM in Philadelphia 2020 | Postcards encouraging VBM increased mail ballot use by 0.4 pp (~3%); many additional mail ballots only counted due to last-minute policy intervention | Yes |
| Yoder, Handan-Nader, Myers, Nowacki, Thompson, Wu, Yorgason, and Hall | 2021 | *Science Advances* 7(52): eabk1755 | Absentee voting effects in 2020 election | No-excuse absentee voting did not meaningfully increase turnout in 2020; voter interest, not voting mode, drove record turnout; natural experiment in TX/IN at age-65 threshold | Yes |
| Goodman-Bacon | 2021 | *Journal of Econometrics* 225(2): 254–277 | DiD with variation in treatment timing | TWFE DiD estimator is weighted average of all 2×2 DiDs; biased when treatment effects change over time because already-treated units serve as controls | Yes |
| Callaway and Sant'Anna | 2021 | *Journal of Econometrics* 225(2): 200–230 | DiD with multiple time periods | Group-time ATT estimators for staggered DiD; outcome regression, IPW, and doubly-robust approaches; avoids TWFE pitfalls by using not-yet-treated units as controls | Yes |
| Sun and Abraham | 2021 | *Journal of Econometrics* 225(2): 175–199 | Event study with heterogeneous treatment effects | TWFE event studies can produce contaminated estimates and spurious pre-trends; propose interaction-weighted estimator with non-negative weights | Yes |
| McGhee, Paluch, and Romero | 2022 | *Research & Politics* 9(2) | VBM policy and 2020 presidential election | States mailing all voters ballots saw turnout increase of ~5.6 pp; expanding VBM has no robust partisan effects; uses county-level data from 2020 | Yes |
| McDonald, Mucci, Shino, and Smith | 2023 | *Election Law Journal* 23(1): 1–18 | Mail voting and voter turnout 2012–2020 | States with greater mail voting usage consistently have higher turnout across all general elections 2012–2020; challenges "substitution effect" hypothesis | Yes |

## Detailed Summaries

### Foundational VBM Studies

**Southwell and Burchett (2000)** conducted one of the earliest systematic analyses of all-mail elections, examining 48 statewide elections in Oregon. They reported a ~10 pp turnout increase from all-mail elections, claiming mail voting was "a major stimulus to voter participation, second only to the impact of a presidential contest." However, subsequent work by Gronke and Miller (2012) attributed much of this estimated effect to novelty, as the boost diminished over time.

**Berinsky, Burns, and Traugott (2001)** used individual-level Oregon voter data across multiple elections to study *who* votes by mail. They found VBM increases turnout primarily by retaining current voters (reducing dropout) rather than mobilizing nonvoters. Critically, VBM does not affect partisan composition, but it increases rather than diminishes the resource stratification of the electorate—resource-rich voters are kept in while resource-poor voters' behavior changes little.

**Kousser and Mullin (2007)** exploited a natural experiment in which California voters were quasi-randomly assigned to vote by mail. Using matching methods, they found VBM actually *decreased* turnout in regular elections, though it increased turnout in special/low-salience elections where baseline participation is low. This highlighted that the turnout effects of VBM depend on electoral context.

**Gronke et al. (2008)** provided a comprehensive review of the convenience voting literature (early voting, no-excuse absentee, VBM). They documented that over 30% of American voters used some form of convenience voting, but the most common empirical finding was that adoption had little to no effect on overall turnout—a paradox given the theoretical expectation that reducing voting costs should increase participation.

**Gerber, Huber, and Hill (2013)** produced the most rigorous pre-Thompson et al. study of VBM, exploiting the staggered county-level adoption of all-mail elections in Washington State. They estimated a 2–4 pp turnout increase, with larger gains for infrequent voters. This paper's design directly inspired Thompson et al.'s (2020) approach, extending it to three states and adding partisan outcomes.

### The Original Paper and Contemporaneous Studies

**Thompson, Wu, Yoder, and Hall (2020)** extended the Gerber et al. approach to three states (CA, UT, WA) and shifted focus to partisan outcomes. Their null finding on partisan effects, combined with the ~2 pp turnout increase, became the central empirical reference in the 2020 VBM debate.

**Barber and Holbein (2020)**, published simultaneously in *Science Advances*, reached similar conclusions using nationwide county-level data (1992–2018) and 40M+ individual voter records from WA and UT. Mandatory VBM increased turnout 2–3 pp without advantaging either party.

**Lockhart et al. (2020)** provided important context by documenting rapid partisan polarization *about* VBM during COVID-19. Using nationally representative surveys, they found a ~10 pp partisan gap in VBM preferences in April 2020 that doubled to ~20 pp by June 2020, with Democrats strongly preferring mail voting and Republicans preferring in-person voting. This behavioral divergence in *how* people vote did not, however, translate into partisan electoral advantages.

### Post-2020 Election Studies

**Hopkins et al. (2021)** conducted a field experiment during COVID-19 in Philadelphia, randomly sending postcards encouraging VBM to ~47,000 registrants. The intervention increased mail ballot usage by ~0.4 pp. Notably, many additional mail ballots only counted because of a last-minute policy intervention extending the receipt deadline, highlighting the administrative challenges of VBM expansion.

**Yoder et al. (2021)** directly examined the 2020 election using microdata on millions of voters and a natural experiment comparing 64- vs. 65-year-olds in TX and IN (where only those 65+ can vote absentee without excuse). They found no-excuse absentee voting did not meaningfully increase 2020 turnout or affect partisan composition. Voter interest, not voting mode, drove the record turnout.

**McGhee, Paluch, and Romero (2022)** used county-level 2020 data and found states mailing all voters ballots saw turnout increase by ~5.6 pp—larger than pre-COVID estimates—while expanding VBM had no robust partisan effects.

**McDonald et al. (2023)** analyzed CPS and CES data from 2012–2020, finding that states with greater mail voting usage consistently experienced higher turnout, challenging the "substitution effect" hypothesis that mail voting merely replaces in-person voting.

### Methodological Papers on Staggered DiD

**Goodman-Bacon (2021)** provided the foundational decomposition showing that the TWFE DiD estimator in staggered settings is a weighted average of all possible 2×2 DiDs. The weights can be negative when treatment effects vary over time, because already-treated units effectively serve as "controls." This paper raised important concerns about the Thompson et al. design, though the null findings are less susceptible to these biases than non-null findings would be.

**Callaway and Sant'Anna (2021)** developed group-time average treatment effect estimators that avoid TWFE pitfalls by using only not-yet-treated units as controls. Their approach permits estimation of heterogeneous treatment effects across cohorts and time periods.

**Sun and Abraham (2021)** showed that TWFE event study specifications can produce contaminated coefficient estimates and spurious pre-trends when treatment effects are heterogeneous across cohorts. They proposed an interaction-weighted estimator that avoids these problems. This is directly relevant to interpreting Thompson et al.'s event study robustness checks.
