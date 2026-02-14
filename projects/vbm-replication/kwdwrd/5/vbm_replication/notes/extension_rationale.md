# Extension Rationale

## 1. What Changed After 2018?

### COVID-19 Pandemic and Emergency VBM Expansion
The 2020 election was held during the COVID-19 pandemic, which fundamentally altered the voting landscape in the United States. Many states and counties expanded mail voting options to reduce public health risks. This created a massive shift in how Americans voted: in 2020, approximately 46% of voters cast ballots by mail, compared to about 24% in 2016. The pandemic thus provides a natural test of whether the null partisan effects found by Thompson et al. (2020) hold under dramatically different conditions.

### VBM Becoming a Partisan Issue
Before 2020, voting by mail was not a strongly partisan issue. After President Trump repeatedly criticized mail voting as fraudulent, preferences for mail voting became sharply polarized along party lines. Lockhart et al. (2020) documented a nearly 20 percentage point gap between Democrats and Republicans in their preference for voting by mail by June 2020. In the actual 2020 election, approximately 59% of Biden voters used mail ballots compared to only 30% of Trump voters. This partisan divergence in VBM usage raises the question of whether universal VBM adoption could have partisan effects in this new environment, even if it did not before 2020.

### Continued California Voter's Choice Act Rollout
California's Voter's Choice Act (VCA) continued its staggered rollout after the original paper's sample period:
- **2018:** 5 counties (Madera, Napa, Nevada, Sacramento, San Mateo) --- original paper captured this
- **2020:** 10 additional counties joined (Amador, Butte, Calaveras, El Dorado, Fresno, Los Angeles, Mariposa, Orange, Santa Clara, Tuolumne), for 15 total
- **2022:** 14 additional counties joined (Alameda, Humboldt, Imperial, Kings, Marin, Merced, Riverside, San Benito, San Diego, Santa Cruz, Sonoma, Stanislaus, Ventura, Yolo), for 29 total
- **2024:** 1 additional county joined (Placer), for 30 total

This continued rollout provides new variation in treatment timing within California that can be exploited in the difference-in-differences framework.

## 2. What New Variation Exists?

### California: Primary Source of New Variation
California is the key state for the extension analysis. The VCA rollout from 2020 to 2024 provides substantial new treatment variation:
- 10 newly treated counties in 2020 (including large counties: Los Angeles, Orange, Santa Clara)
- 14 newly treated counties in 2022
- 1 newly treated county in 2024
- 28 of 58 counties never adopted VCA through 2024 (potential control group)

This staggered adoption within California allows continued application of the difference-in-differences design.

### Utah: Limited New Variation
Utah had already achieved near-universal VBM by 2018 (27 of 29 counties). By 2019, all Utah counties conducted elections by mail. Therefore, there is essentially no new VBM adoption variation in Utah for the extension period. Utah still contributes to the analysis through the state-by-year fixed effects and as a comparison point, but it does not generate new treatment variation.

### Washington: No New Variation
Washington has been 100% vote-by-mail since 2011 (all 39 counties). There is no new VBM variation in Washington for the extension period. Like Utah, Washington contributes to the fixed effects structure but provides no new identifying variation.

### Summary of New Variation

| State | Pre-2020 Treated Counties | New Treatment 2020-2024 | Never Treated (through 2024) |
|-------|--------------------------|------------------------|------------------------------|
| California | 5 (2018 VCA) | 25 new VCA counties (2020-2024) | 28 counties |
| Utah | 27-29 | 0-2 (all by 2019) | 0 |
| Washington | 39 (all since 2012) | 0 | 0 |

## 3. Research Questions for the Extension

### Primary Questions

1. **Do the null partisan effects hold in the post-COVID period?**
   The original paper found that universal VBM does not affect Democratic turnout share or vote share. Does this finding extend to 2020-2024, when VBM became a partisan issue? If the null result holds even in this polarized environment, it would further strengthen confidence in the finding.

2. **Is there evidence of heterogeneous effects by time period?**
   We can test this by interacting the VBM treatment indicator with a post-2018 dummy. A significant interaction would suggest that VBM effects changed after the pandemic politicized mail voting. The key coefficient is:
   ```
   Y_cst = beta1(VBM_cst) + beta2(VBM_cst x Post2018_t) + gamma_cs + delta_st + epsilon_cst
   ```
   If beta2 is large and significant, the VBM effect differs post-2018.

3. **Do event study patterns look similar pre- and post-2018?**
   California's continued VCA rollout allows estimation of event studies centered on treatment adoption. We can examine whether the pattern of leads and lags around VCA adoption in 2020-2024 mirrors the pattern around 2018 adoption.

### Secondary Questions

4. **Does California's VCA expansion show similar effects to the initial 2018 pilot?**
   The original paper captured only the initial 5-county VCA pilot. The 2020-2024 expansion includes much larger counties (Los Angeles, Orange, San Diego) and may reveal effects that were not apparent in the small initial rollout.

5. **What is the effect on turnout in the extended sample?**
   The original paper found a robust ~2pp increase in turnout. Does this finding hold when adding 2020-2024 data?

## 4. Limitations to Acknowledge

### Limited New Variation Outside California
Since Utah and Washington are fully treated by 2019, the extension analysis relies almost entirely on California's VCA rollout for new identifying variation. This reduces the cross-state generalizability that was a strength of the original paper.

### Cannot Separate VBM Effects from COVID Effects in 2020
The 2020 election was exceptional in many ways beyond VBM expansion: record turnout, pandemic conditions, highly mobilized electorate, unique candidates. Counties that adopted VCA in 2020 did so partly in response to the pandemic, introducing potential selection effects. It is difficult to isolate the causal effect of VBM from the broader COVID-19 disruption.

### Confounding of VCA with Other COVID-Era Voting Changes
California's VCA involves more than just mailing ballots to voters---it also replaces traditional polling places with fewer vote centers open for multiple days. During COVID, even non-VCA counties expanded mail voting options. In 2020, Governor Newsom issued Executive Order N-64-20 requiring all counties to mail ballots to all registered voters for the November general election. This means the distinction between VCA and non-VCA counties may have been attenuated in 2020, potentially biasing the treatment effect toward zero.

### Post-2020 Period May Have Different Dynamics
After 2020, the political dynamics around mail voting continued to evolve. Republican suspicion of mail voting persisted, and some states moved to restrict mail voting while others expanded it. The effects of VBM adoption in 2022 and 2024 may differ from those in 2018 or 2020 simply because the political context changed.

### Smaller Effective Sample for New Variation
While California has 58 counties, the identifying variation in the extension comes from comparing counties that newly adopted VCA to those that did not. With 30 of 58 counties having adopted VCA by 2024 and 28 remaining without VCA, the comparison group is adequate but smaller than the full cross-state design in the original paper.

### Data Availability Concerns
Extension data must be collected from state election offices, which may have different reporting formats, variable definitions, or data quality. CVAP estimates for 2020-2024 must be derived from the 2020 Census and American Community Survey, which may differ methodologically from the estimates used in the original study period.
