======================================================================
ORIGINAL DATA EXAMINATION
======================================================================

1. DIMENSIONS
----------------------------------------
Rows: 1,454
Columns: 134

2. KEY VARIABLE NAMES
----------------------------------------
  state: present
  county: present
  year: present
  prim_or_gen: present
  treat: present
  share_votes_dem: present
  dem_share_gov: present
  dem_share_pres: present
  turnout_share: present
  vbm_share: present
  cvap: present
  county_id: present
  state_year_id: present
  year2: present

3. GEOGRAPHIC COVERAGE
----------------------------------------
CA: 58 counties, 638 observations
UT: 29 counties, 348 observations
WA: 39 counties, 468 observations
Total: 124 counties, 1454 observations

4. TIME COVERAGE
----------------------------------------
Years: 1996 - 2018
Election years: [1996, 1998, 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018]
Number of elections: 12

5. ELECTION TYPES
----------------------------------------
prim_or_gen
general    1454
Name: count, dtype: int64

6. TREATMENT VARIABLE (treat)
----------------------------------------
Overall: 0.233 treated
CA: 5 treated obs (0.8%)
UT: 59 treated obs (17.0%)
WA: 275 treated obs (58.8%)

7. KEY OUTCOME VARIABLES - SUMMARY STATISTICS
----------------------------------------

share_votes_dem - Dem Turnout Share (CA, UT only)
  N: 986
  Mean: 0.2844
  Std: 0.1762
  Min: 0.0163
  Max: 0.6582

dem_share_gov - Dem Vote Share (Governor)
  N: 756
  Mean: 0.4281
  Std: 0.1559
  Min: 0.0789
  Max: 0.8815

dem_share_pres - Dem Vote Share (President)
  N: 698
  Mean: 0.4295
  Std: 0.1681
  Min: 0.0698
  Max: 0.9015

turnout_share - Turnout (ballots/CVAP)
  N: 1240
  Mean: 0.5416
  Std: 0.1209
  Min: 0.2250
  Max: 0.9347

vbm_share - VBM Share (CA only)
  N: 892
  Mean: 0.5831
  Std: 0.2460
  Min: 0.0080
  Max: 1.0001

8. MISSING VALUES FOR KEY VARIABLES
----------------------------------------
share_votes_dem: 468 missing (32.2%)
dem_share_gov: 698 missing (48.0%)
dem_share_pres: 756 missing (52.0%)
turnout_share: 214 missing (14.7%)
vbm_share: 562 missing (38.7%)

9. FIXED EFFECTS STRUCTURE
----------------------------------------
Unique county_id: 126
Unique state_year_id: 35

10. SAMPLE SIZES FOR REPLICATION
----------------------------------------

Table 2, Cols 1-3 (Dem Turnout Share):
  Sample: CA and UT with share_votes_dem
  N: 986
  Counties: 87

Note: dem_share not directly available, need to construct

Table 3, Cols 1-3 (Turnout):
  N: 1240
  Counties: 126

Table 3, Cols 4-6 (VBM Share, CA only):
  N: 580
  Counties: 58