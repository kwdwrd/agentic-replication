# Utah 2022 Senate Election: Special Case

## Background

The 2022 Utah U.S. Senate race between incumbent Mike Lee (R) and Evan McMullin (Independent) was unique:

1. **No Democratic Candidate**: For the first time in Utah history, the Democratic Party did not nominate a Senate candidate
2. **Independent Coalition**: McMullin ran as an Independent with endorsement from the Utah Democratic Party
3. **Historical Margin**: Lee's 53.2% to McMullin's 42.7% was the closest Senate race in Utah since 1974

## Implications for Extension Analysis

### For Partisan Outcome Variables (`dem_share_sen`)
- Utah 2022 **should be excluded** from the `dem_share_sen` analysis because there was no Democratic candidate
- Alternatively, McMullin could be treated as a proxy for "opposition to Republican" but this changes the interpretation

### For Turnout Analysis (`turnout_share`)
- Utah 2022 **can still be used** for turnout analysis
- Total ballots cast and registered voters are unaffected by candidate identity

### For VBM Share Analysis
- Utah does not provide VBM statistics at the county level in the same format as CA/WA
- Utah has universal mail voting statewide since 2019, so all 29 counties are "treated"

## Data Collected

Only partial county-level data was available from news sources. Full official results would require accessing PDF canvass reports from individual county clerks or purchasing from Dave Leip's Election Atlas.

## Statewide Totals
- Mike Lee (R): 571,974 votes (53.2%)
- Evan McMullin (I): 459,958 votes (42.7%)
- Other candidates: ~4.1%

## Sources
- NBC News 2022 Election Results
- Salt Lake Tribune
- Utah Secretary of State / vote.utah.gov
