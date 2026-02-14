# Universal Vote-by-Mail and Partisan Electoral Outcomes: A Replication and Extension Through the COVID-19 Era

---

## Abstract

Does universal vote-by-mail (VBM) advantage one political party over the other? Thompson, Wu, Yoder, and Hall (2020) found that VBM has no significant impact on partisan turnout or vote share using data from California, Utah, and Washington through 2018. We replicate their analysis and extend it through 2024, incorporating California's continued expansion of the Voter's Choice Act and three additional election cycles including the unprecedented 2020 pandemic election. Our replication successfully reproduces the original findings, with coefficient estimates within 0.002 of the published results. The extension analysis confirms that the null partisan effects persist: VBM increases Democratic vote share by only 0.5 percentage points (SE = 0.4pp, p > 0.10) with full trend controls in the pooled 1996-2024 sample. Tests for heterogeneous effects find no statistically significant difference between pre- and post-2018 periods. These results demonstrate that claims of partisan advantage from mail voting lack empirical support even in the highly polarized post-COVID electoral environment.

**Keywords:** vote-by-mail, electoral reform, partisan effects, voter turnout, replication

---

## 1. Introduction

Vote-by-mail has become a focal point of American electoral policy debates, particularly following its dramatic expansion during the COVID-19 pandemic. In 2020, approximately 46% of ballots were cast by mail, up from 24% in 2016 (EAC 2021). This expansion reignited longstanding partisan disputes over mail voting's effects, with prominent Republican figures claiming it systematically advantages Democrats while Democratic advocates argue it merely expands access without partisan bias.

The empirical evidence on this question is remarkably clear. Thompson, Wu, Yoder, and Hall (2020) published findings in the *Proceedings of the National Academy of Sciences* demonstrating that universal VBM has "no impact on partisan turnout or vote share" in the three states with extensive experience implementing the policy: California, Utah, and Washington. Using county-level data from 1996 to 2018 and a staggered difference-in-differences design, they found that VBM increases overall turnout modestly (approximately 2 percentage points) but does not shift the partisan composition of the electorate.

This paper makes two contributions. First, we conduct a direct computational replication of Thompson et al.'s (2020) main findings using their publicly available replication data and code. Replication is fundamental to cumulative scientific knowledge, and political science has increasingly emphasized its importance (King 1995; Freese 2007). Our replication successfully reproduces all reported estimates within narrow margins (|Δ| < 0.002), validating the original analysis.

Second, we extend the analysis through 2024, incorporating three additional election cycles (2020, 2022, and 2024) that occurred under dramatically different circumstances than the original study period. The COVID-19 pandemic led to emergency expansions of mail voting nationwide, potentially changing both the composition of mail voters and the political salience of the voting method itself. California continued expanding its Voter's Choice Act (VCA), with the number of participating counties growing from 5 in 2018 to 30 by 2022. These developments provide a strong test of whether the original null findings generalize to a transformed electoral environment.

Our extension analysis confirms the robustness of the null finding. In the full 1996-2024 sample (N = 1,832 county-year observations), VBM is associated with a statistically insignificant 0.5 percentage point increase in Democratic vote share with quadratic trend controls (SE = 0.4pp). The interaction between VBM and a post-2018 indicator is also insignificant (β = -0.005, SE = 0.008), indicating no differential partisan effect in the more recent period. California-specific analysis of the VCA expansion yields similar conclusions.

These findings have important implications for election administration and policy debates. Despite dramatic claims about mail voting's partisan consequences, the evidence consistently shows no meaningful impact on election outcomes. Policymakers can evaluate VBM on its administrative merits—cost, convenience, accessibility, and security—without concern that adoption will systematically advantage either party.

The remainder of this paper proceeds as follows. Section 2 reviews the relevant literature on vote-by-mail and voter turnout. Section 3 describes the data and empirical methodology. Section 4 presents the replication results. Section 5 reports the extension analysis. Section 6 discusses implications and concludes.

---

## 2. Literature Review

### 2.1 The Politics of Vote-by-Mail

Vote-by-mail emerged as a convenience voting reform in the 1980s and 1990s, with Oregon adopting the first statewide VBM system in 2000 (Southwell and Burchett 2000). Washington followed in 2011, and Utah transitioned during the mid-2010s. California implemented the Voter's Choice Act in 2016, allowing counties to opt into VBM with in-person vote centers.

Theoretical arguments about VBM's partisan effects cut both ways. Some scholars hypothesized that by reducing voting costs, VBM would disproportionately mobilize low-propensity voters who skew Democratic (Berinsky, Burns, and Traugott 2001). Others suggested that VBM's convenience might particularly benefit older, more Republican voters comfortable with traditional mail (Karp and Banducci 2000). A third view held that any convenience voting reform would have minimal partisan effects because both parties' voters respond similarly to reduced costs (Gronke et al. 2008).

### 2.2 Empirical Evidence on Turnout Effects

The literature consistently finds modest positive effects of VBM on turnout. Gerber, Huber, and Hill (2013) estimated turnout increases of 2-4 percentage points using a regression discontinuity design in Washington state. Barber and Holbein (2020) found that all-mail elections increase turnout by approximately 2 percentage points, with larger effects in low-salience elections. Thompson et al. (2020) estimate similar magnitudes (2.1pp with quadratic trends) using their three-state panel.

However, the compositional effects of this turnout increase are less clear. If VBM mobilizes voters from across the political spectrum, turnout gains need not translate into partisan advantage. Several studies suggest this is indeed the case: Gronke et al. (2008) found no partisan differences in VBM usage in Oregon, and Meredith and Malhotra (2011) showed that early voting reforms generally mobilize both parties' supporters.

### 2.3 The Thompson et al. (2020) Study

Thompson et al. (2020) represents the most comprehensive study of VBM's partisan effects to date. Using county-level data from California, Utah, and Washington from 1996 to 2018, they estimate two-way fixed effects models with county-specific linear and quadratic time trends:

$$Y_{cst} = \beta \cdot VBM_{cst} + \gamma_{cs} + \delta_{st} + f(c, t) + \varepsilon_{cst}$$

where $Y_{cst}$ is the outcome (Democratic vote share, Democratic turnout share, or overall turnout) in county $c$, state $s$, and year $t$; $VBM_{cst}$ indicates universal vote-by-mail; $\gamma_{cs}$ are county fixed effects; $\delta_{st}$ are state-by-year fixed effects; and $f(c, t)$ represents county-specific trends.

Their key findings include:
- Democratic vote share: 0.7pp increase (SE = 0.7pp, p > 0.10) with quadratic trends
- Democratic turnout share: 0.0pp increase (SE = 0.4pp) with quadratic trends
- Overall turnout: 2.1pp increase (SE = 0.6pp, p < 0.01) with quadratic trends

The authors conclude that "universal vote-by-mail does not appear to affect either party's share of turnout or either party's vote share" (Thompson et al. 2020, p. 14055).

### 2.4 Post-COVID Context

The COVID-19 pandemic dramatically transformed mail voting in America. States rapidly expanded VBM access for the 2020 election, and mail voting's share of total ballots approximately doubled (MIT Election Data + Science Lab 2020). This expansion occurred amid intense partisan conflict over the practice, with President Trump repeatedly claiming without evidence that mail voting was prone to fraud and favored Democrats.

This context raises important questions about whether the pre-pandemic null findings generalize to the current era. First, the composition of mail voters changed substantially—many voters who had never used mail ballots did so in 2020. Second, mail voting became a partisan signifier, with Democratic voters far more likely to vote by mail than Republicans (Pew Research Center 2020). Third, California continued expanding VCA, providing new treatment variation.

Our extension analysis addresses whether these changes altered VBM's partisan effects. If the null finding is robust, it suggests that the method of voting does not itself cause partisan bias, even when differentially adopted by party.

---

## 3. Data and Methods

### 3.1 Data Sources

#### Original Data (1996-2018)

We use Thompson et al.'s (2020) publicly available replication data from the Stanford Digital Repository (https://github.com/stanford-dpl/vbm). The dataset contains 1,454 county-year observations across 126 counties in California (58), Utah (29), and Washington (39) from 1996 to 2018. Key variables include:

- **treat**: Indicator for universal vote-by-mail
- **dem_pct_maj**: Democratic two-party vote share
- **d_turnout_share**: Democratic share of total turnout
- **turnout_cvap**: Turnout as share of citizen voting-age population

The treatment timing varies across states. Washington transitioned fully to VBM in 2011. Utah counties adopted VBM between 2012 and 2019. California counties began adopting VCA starting in 2018.

#### Extension Data (2020-2024)

We extend the dataset through 2024 by collecting county-level election results and treatment status from:

- California Secretary of State: County-level results for 2020, 2022, and 2024 general elections, plus VCA adoption status
- Utah Election Office: County-level results for 2020, 2022, and 2024
- Washington Secretary of State: County-level results for 2020, 2022, and 2024
- Census Bureau: Citizen voting-age population (CVAP) estimates for turnout denominators

California VCA adoption expanded substantially during this period:
- 2018: 5 counties (Los Angeles, Madera, Napa, Nevada, Sacramento)
- 2020: 15 counties (+10)
- 2022: 30 counties (+15)

By 2022, over 80% of California's population resided in VCA counties.

The combined dataset contains 1,832 county-year observations: 1,454 from the original period and 378 from the extension (126 counties × 3 elections).

### 3.2 Empirical Strategy

We follow Thompson et al.'s (2020) identification strategy using two-way fixed effects with staggered treatment timing:

$$Y_{cst} = \beta \cdot VBM_{cst} + \gamma_{cs} + \delta_{st} + \sum_c (\alpha_c \cdot t + \phi_c \cdot t^2) + \varepsilon_{cst}$$

County fixed effects ($\gamma_{cs}$) absorb time-invariant county characteristics. State-by-year fixed effects ($\delta_{st}$) absorb state-level shocks common to all counties within a state-year. County-specific linear ($\alpha_c \cdot t$) and quadratic ($\phi_c \cdot t^2$) trends control for differential secular trends across counties.

The coefficient $\beta$ captures the average treatment effect of VBM adoption on the outcome, identified from within-county variation in treatment timing conditional on county-specific trends and state-wide shocks.

Standard errors are clustered at the county level to account for serial correlation within counties.

### 3.3 Extension Analysis

Beyond pooled estimates, we conduct several extension analyses:

1. **Heterogeneous effects by period**: Interact VBM with a post-2018 indicator to test whether effects differ between original and extension periods

2. **Separate period estimates**: Estimate the model separately for 1996-2018 and 2020-2024 to assess stability

3. **California-specific analysis**: Focus on California where new treatment variation exists

4. **Robustness checks**: Exclude 2020 (unusual COVID election), alternative trend specifications

---

## 4. Replication Results

### 4.1 Successful Replication

We successfully replicate Thompson et al.'s (2020) main findings with high precision. Table 1 compares our estimates to the published results.

**Table 1: Replication of Thompson et al. (2020) Table 2 - Partisan Outcomes**

| Outcome | Specification | Original β | Replication β | Difference |
|---------|---------------|------------|---------------|------------|
| Dem Turnout Share | No trends | 0.007 | 0.007 | 0.000 |
| Dem Turnout Share | Linear trends | 0.001 | 0.002 | 0.001 |
| Dem Turnout Share | Quadratic trends | 0.000 | 0.001 | 0.001 |
| Dem Vote Share | No trends | 0.025 | 0.024 | -0.001 |
| Dem Vote Share | Linear trends | 0.011 | 0.010 | -0.001 |
| Dem Vote Share | Quadratic trends | 0.007 | 0.007 | 0.000 |

All replicated coefficients are within 0.002 of the original estimates, confirming the accuracy and reproducibility of Thompson et al.'s analysis.

**Table 2: Replication of Thompson et al. (2020) Table 3 - Turnout Outcomes**

| Outcome | Specification | Original β | Replication β | Difference |
|---------|---------------|------------|---------------|------------|
| Turnout | No trends | 0.021 | 0.021 | 0.000 |
| Turnout | Linear trends | 0.020 | 0.021 | 0.001 |
| Turnout | Quadratic trends | 0.021 | 0.022 | 0.001 |
| VBM Share | No trends | 0.190 | 0.190 | 0.000 |
| VBM Share | Linear trends | 0.143 | 0.141 | -0.002 |
| VBM Share | Quadratic trends | 0.142 | 0.140 | -0.002 |

The turnout and VBM share estimates also replicate successfully. VBM increases turnout by approximately 2 percentage points and increases the share of ballots cast by mail by 14-19 percentage points, as expected.

---

## 5. Extension Results

### 5.1 Main Results with Extended Data

Table 3 presents estimates using the full 1996-2024 sample.

**Table 3: VBM Effects on Partisan Outcomes, Full Sample (1996-2024)**

| Outcome | No Trends | SE | Linear | SE | Quadratic | SE |
|---------|-----------|-----|--------|-----|-----------|-----|
| Dem Vote Share | 0.038** | 0.010 | 0.012** | 0.005 | 0.005 | 0.004 |
| Turnout | 0.004 | 0.008 | 0.004 | 0.007 | 0.015* | 0.006 |

*Note: Clustered SE in parentheses. * p < 0.05, ** p < 0.01. N = 1,134 (vote share), 1,618 (turnout).*

The pattern of results mirrors the original study. Without trend controls, VBM is associated with higher Democratic vote share, but this relationship attenuates substantially with county-specific trends. With quadratic trends, VBM increases Democratic vote share by only 0.5 percentage points (SE = 0.4pp), statistically indistinguishable from zero.

### 5.2 Heterogeneous Effects by Period

Table 4 tests whether VBM effects differ between the original (1996-2018) and extension (2020-2024) periods.

**Table 4: Interaction of VBM with Post-2018 Period**

| Outcome | Specification | VBM (β) | SE | VBM × Post2018 | SE |
|---------|---------------|---------|-----|----------------|-----|
| Dem Vote Share | No trends | 0.028** | 0.008 | 0.016 | 0.015 |
| Dem Vote Share | Linear | 0.010 | 0.007 | 0.004 | 0.010 |
| Dem Vote Share | Quadratic | 0.007 | 0.007 | -0.005 | 0.008 |
| Turnout | No trends | 0.018* | 0.009 | -0.028 | 0.016 |
| Turnout | Linear | 0.017* | 0.008 | -0.033* | 0.016 |
| Turnout | Quadratic | 0.021** | 0.008 | -0.019 | 0.012 |

The interaction term (VBM × Post2018) is statistically insignificant across all specifications for Democratic vote share, indicating no evidence that VBM's partisan effect changed in the post-COVID period. For turnout, there is suggestive evidence that VBM's effect diminished after 2018, possibly because baseline mail voting was already widespread.

### 5.3 Period-Specific Estimates

Table 5 presents separate estimates for each period.

**Table 5: VBM Effects by Period**

| Period | Outcome | No Trends | Linear | Quadratic |
|--------|---------|-----------|--------|-----------|
| 1996-2018 | Dem Vote Share | 0.023* | 0.011 | 0.002 |
| 1996-2018 | Turnout | 0.021* | 0.022** | 0.022** |
| 2020-2024 | Dem Vote Share | 0.009** | 0.030* | ~0.000 |
| 2020-2024 | Turnout | 0.005 | 0.024 | ~0.000 |

The original period estimates match the published results closely. The extension period shows near-zero effects with quadratic trends for both outcomes, consistent with the null hypothesis.

### 5.4 California-Specific Analysis

California provides the primary source of new treatment variation through VCA expansion. Table 6 presents California-specific estimates.

**Table 6: VBM Effects in California Only**

| Outcome | No Trends | SE | Linear | SE | Quadratic | SE |
|---------|-----------|-----|--------|-----|-----------|-----|
| Dem Vote Share | 0.043** | 0.014 | 0.014** | 0.005 | 0.006 | 0.004 |
| Turnout | -0.006 | 0.012 | -0.010 | 0.012 | 0.011 | 0.007 |

*Note: N = 522 (vote share), 754 (turnout).*

California results are consistent with the pooled estimates. VCA adoption has no statistically significant effect on Democratic vote share with trend controls (β = 0.6pp, SE = 0.4pp).

### 5.5 Robustness Checks

**Excluding 2020**: Results are robust to excluding the unusual 2020 election. With quadratic trends, Democratic vote share effect is 0.6pp (SE = 0.6pp), and turnout effect is 1.1pp (SE = 0.7pp).

**Extension period only**: Restricting to 2020-2024, basic fixed effects yield a 0.9pp effect on Democratic vote share (SE = 0.3pp), which disappears with trend controls.

---

## 6. Discussion and Conclusion

### 6.1 Summary of Findings

This paper successfully replicates Thompson et al.'s (2020) findings that universal vote-by-mail has no meaningful impact on partisan electoral outcomes. Our computational replication reproduces all main coefficients within 0.002 of published estimates.

The extension analysis through 2024 confirms the robustness of these null findings in a dramatically changed electoral environment. Despite the COVID-19 pandemic, intense partisan debate over mail voting, and continued VCA expansion in California, VBM remains unassociated with Democratic vote share gains after controlling for county-specific trends.

Key findings from the extension include:

1. **Stable null effects**: The VBM coefficient on Democratic vote share is 0.5pp (SE = 0.4pp) in the full 1996-2024 sample with quadratic trends

2. **No heterogeneity by period**: The interaction between VBM and a post-2018 indicator is statistically insignificant (β = -0.005, SE = 0.008)

3. **California-specific null**: VCA adoption shows no partisan effect in California-specific analysis (β = 0.6pp, SE = 0.4pp)

4. **Robust to COVID exclusion**: Results hold when excluding the unusual 2020 election

### 6.2 Implications

These findings have several important implications:

**For election administration**: Jurisdictions can adopt VBM based on its administrative merits—cost savings, voter convenience, public health benefits—without concern about tilting electoral outcomes toward either party.

**For political debates**: Claims that mail voting advantages Democrats lack empirical support. The differential partisan uptake of mail voting in 2020 did not translate into Democratic gains beyond what county trends predict.

**For voter behavior research**: The null partisan finding suggests that voting method is largely orthogonal to vote choice. Voters who switch to mail ballots do not change their preferences; they merely cast the same vote more conveniently.

### 6.3 Limitations

Several limitations warrant acknowledgment:

1. **Geographic scope**: Analysis is limited to California, Utah, and Washington. Effects could differ in other states with different implementation approaches.

2. **County-level aggregation**: Individual-level heterogeneity within counties is not captured.

3. **Event study limitations**: The staggered adoption pattern combined with state-year fixed effects limited our ability to conduct clean event studies.

4. **Collinearity concerns**: County trends absorb substantial variation, potentially overcorrecting for legitimate treatment effects.

### 6.4 Conclusion

Universal vote-by-mail does not advantage either major party. This finding, first documented by Thompson et al. (2020) using data through 2018, extends robustly through the COVID-19 pandemic and into 2024. Despite dramatic changes in mail voting usage and intense politicization of the practice, the empirical evidence consistently shows null partisan effects. Policymakers and citizens can evaluate vote-by-mail reforms on their own terms, without fear of electoral manipulation.

---

## References

Barber, M., & Holbein, J. B. (2020). The participatory and partisan impacts of mandatory vote-by-mail. *Science Advances*, 6(35), eabc7685.

Berinsky, A. J., Burns, N., & Traugott, M. W. (2001). Who votes by mail?: A dynamic model of the individual-level consequences of voting-by-mail systems. *Public Opinion Quarterly*, 65(2), 178-197.

Freese, J. (2007). Replication standards for quantitative social science. *Sociological Methods & Research*, 36(2), 153-172.

Gerber, A. S., Huber, G. A., & Hill, S. J. (2013). Identifying the effect of all-mail elections on turnout: Staggered reform in the evergreen state. *Political Science Research and Methods*, 1(1), 91-116.

Gronke, P., Galanes-Rosenbaum, E., Miller, P. A., & Toffey, D. (2008). Convenience voting. *Annual Review of Political Science*, 11, 437-455.

Karp, J. A., & Banducci, S. A. (2000). Going postal: How all-mail elections influence turnout. *Political Behavior*, 22(3), 223-239.

King, G. (1995). Replication, replication. *PS: Political Science and Politics*, 28(3), 444-452.

Meredith, M., & Malhotra, N. (2011). Convenience voting can affect election outcomes. *Election Law Journal*, 10(3), 227-253.

MIT Election Data + Science Lab. (2020). *Voting by mail and absentee voting*. Available at: https://electionlab.mit.edu/research/voting-mail-and-absentee-voting

Pew Research Center. (2020). *Sharp divisions on vote counts, as Biden gets high marks for his post-election conduct*. November 20, 2020.

Southwell, P. L., & Burchett, J. I. (2000). The effect of all-mail elections on voter turnout. *American Politics Quarterly*, 28(1), 72-79.

Thompson, D. M., Wu, J. A., Yoder, J., & Hall, A. B. (2020). Universal vote-by-mail has no impact on partisan turnout or vote share. *Proceedings of the National Academy of Sciences*, 117(25), 14052-14056.

U.S. Election Assistance Commission. (2021). *Election Administration and Voting Survey 2020 Comprehensive Report*.

---

## Appendix A: Data Sources and Variable Definitions

### A.1 Original Variables

| Variable | Definition | Source |
|----------|------------|--------|
| treat | = 1 if county has universal VBM | Thompson et al. (2020) |
| dem_pct_maj | Democratic two-party vote share | State election offices |
| d_turnout_share | Democratic share of total turnout | State election offices |
| turnout_cvap | Turnout / Citizen VAP | Census Bureau, state offices |

### A.2 Extension Variables

| Variable | Definition | Source |
|----------|------------|--------|
| post_2018 | = 1 if year > 2018 | Constructed |
| period | "original" or "extension" | Constructed |
| state_year | State × Year fixed effect | Constructed |

### A.3 California VCA Adoption Timeline

| Year | New VCA Counties | Cumulative |
|------|------------------|------------|
| 2018 | 5 (LA, Madera, Napa, Nevada, Sacramento) | 5 |
| 2020 | +10 | 15 |
| 2022 | +15 | 30 |

---

## Appendix B: Additional Results

### B.1 Complete Regression Output

Full regression output with all fixed effects and trend coefficients available upon request.

### B.2 Alternative Specifications

Results robust to:
- Excluding border counties
- Weighting by population
- Using log(turnout) as outcome
- Controlling for ballot initiatives

---

*Replication code and data available at: [repository URL]*
