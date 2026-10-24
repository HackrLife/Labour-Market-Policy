# G: LLM task exposure by era-based occupation group: method and results

Prepared 24 Oct 2026. Script: `/home/claude/research/scripts/exposure.py`. The OEWS parser is `/home/claude/research/scripts/parse_t01.py`. Every downloaded file was read with `python3 -I`.

## 1. Hypothesis tested

H: generative-AI task exposure is concentrated in occupations created or scaled by the post-1995 internet economy, at roughly 50% of their task content. Pre-1995 physical-economy occupations have far lower exposure.

## 2. Data sources

### 2.1 Exposure: Eloundou, Manning, Mishkin and Rock, "GPTs are GPTs", *Science* 2024
- Repository: https://github.com/openai/GPTs-are-GPTs, cloned to `raw/gpts/GPTs-are-GPTs/`. Commit `0471612fef3cc22b74fb884d27bff9dbd3770582` (2025-10-03).
- File: `data/occ_level.csv`. It has 923 O*NET-SOC 2019 codes, which collapse to 798 six-digit SOC codes.
- Columns, per the repository README ("dv_rating is the GPT-4 rating and human is from the annotators; _alpha=E1, _beta=E1+.5*E2, _gamma=E1+E2"):

| This analysis | Source column | Definition |
|---|---|---|
| `human_alpha` / `gpt4_alpha` | `human_rating_alpha` / `dv_rating_alpha` | share of tasks rated E1 (direct exposure) |
| `human_beta` / `gpt4_beta` | `human_rating_beta` / `dv_rating_beta` | E1 + 0.5·E2 |
| `human_zeta` / `gpt4_zeta` | `human_rating_gamma` / `dv_rating_gamma` | E1 + E2. The repository calls this gamma and the published paper calls it ζ. |

- Validation against the paper. On this weighting, 82.1% of employment has human β ≥ 0.10 and 21.9% has human β ≥ 0.50. The paper reports about 80% and about 19%. The small difference comes from using May 2025 rather than 2022 employment weights.

### 2.2 Employment: BLS OEWS May 2025, national, wage and salary
- The bls.gov site and the `oesm25nat.zip` file could not be reached from the shell (proxy 403). WebFetch truncates the table at 100k characters.
- Instead, the full text of OEWS News Release Table 1 (https://www.bls.gov/news.release/ocwage.t01.htm, "May 2025", last modified 15 May 2026) was fetched verbatim with the `apify/web-fetch` actor. It is saved as `raw/oews_t01/ocwage_t01.txt` (124,744 characters; SHA-256 prefix `b3b62479c666c9a3`) together with the raw JSON. The parser joins titles that wrap across lines and extracts 1,121 rows (`raw/oews_t01/t01_parsed.csv`).
- Table 1 has titles but no SOC codes. Codes are attached by exact title match to the detailed 2018-SOC rows of `data/national_May2021_dl.csv` from the GPTs repository (831 detailed codes). OEWS May 2025 uses the same 2018 SOC structure.
- Coverage: 830 of 831 detailed occupations match, with 155,481,840 employees, or 99.991% of the Table 1 total of 155,495,730. The only miss is Legislators (11-1031), for which OEWS publishes no employment figure.
- Cross-check: the parsed values agree with the 45 hand-collected rows in `B_bls_occupations.csv`, for example nuclear engineers at 15,280 and industrial engineers at 365,740.
- OEWS excludes the self-employed, so it under-weights construction trades, farming, personal care and creative occupations.

### 2.3 Crosswalk from O*NET-SOC 2019 to OEWS 2018 SOC
- Several O*NET codes under one six-digit SOC (.00, .01 and so on): unweighted mean. In the sensitivity check, the `.00` code is used alone.
- OEWS aggregates that O*NET splits into detailed codes (13-1020, 13-2020, 21-1018, 25-2052, 25-9045, 29-2010, 31-1120, 39-7010, 47-4090, 51-2028, 51-2090, 53-1047): mean of the O*NET child codes. The mapping is listed in `AGG` in the script.
- Residual "all other" codes with no O*NET rating: 47 codes, with exposure imputed as the mean of rated codes in the same broad group (5-digit), or the minor group if the broad group has none. The `exposure_source` column of the classification CSV records the method for every row.

## 3. Classification rules

Rules are applied in order. Every code, its group, sub-group and rule text are listed in `G_soc_classification.csv`.

**(a) Internet-era digital/information.** 30 occupations, 10.1m employees, 6.5% of employment.
- a1 tech: all 15-12xx computer occupations, 11-3021 computer and information systems managers, 15-2051 data scientists and 17-2061 computer hardware engineers.
- a2 digital marketing and media: 13-1161 market research analysts and marketing specialists, 15-1255 web and digital interface designers (assigned to a1 by the 15-12 rule, which runs first), 27-1014 special effects artists and animators, 27-1024 graphic designers, 27-3042 technical writers and 27-4032 film and video editors.
- a3 clerical work tied to digital systems: 43-9021 data entry keyers, 43-9031 desktop publishers, 29-2072 medical records specialists, 29-9021 health information technologists, and 49-2011 computer, ATM and office machine repairers.
- a4 contact centres: 43-4051 customer service representatives and 41-9041 telemarketers.

**(b) Pre-1995 physical economy.** 508 occupations, 89.1m employees, 57.3% of employment.
- b1: all detailed codes in major groups 29, 31, 33, 35, 37, 39, 45, 47, 49, 51 and 53, apart from the a3 codes listed above.
- b2 physical-sector white-collar roles:
  - all of major group 17 except 17-2061
  - preschool, K-12 and special education teachers (25-2xxx) and K-12 teaching assistants (25-9045)
  - 11-9032 K-12 education administrators
  - 11-9021 construction managers
  - 11-9111 medical and health services managers
  - 13-1081 logisticians
  - 11-3051 industrial production managers
  - 11-3071 transportation, storage and distribution managers
  - 11-3013 facilities managers
  - 11-9013 farm and ranch managers
  - 11-9051 food service managers
  - 11-9081 lodging managers
  - 11-9041 architectural and engineering managers
  - 13-1051 cost estimators
  - 11-9131 postmasters

**(c) Pre-1995 office/professional.** 113 occupations, 33.5m employees, 21.5% of employment. This group holds all remaining codes in majors 11, 13, 23 and 43.

**(d) Other pre-1995 (residual, not in the brief).** 179 occupations, 22.7m employees, 14.6% of employment. This group holds majors 19, 21, 25 (excluding K-12), 27 (excluding a2) and 41 (excluding telemarketers), plus 15-20xx mathematical occupations other than data scientists. These occupations are not part of the A versus B contrast, so they are reported separately rather than forced into (b) or (c).

**Alternative classification (Autor, Chin, Salomons and Seegmiller, 2024 QJE: the share of each occupation's employment in titles new since about 1940/1980).** Skipped. The replication data are on openICPSR, which the shell cannot reach (HTTP 000). GitHub code search is blocked for this session, and no GitHub mirror could be found.

## 4. Results (May 2025 employment weights)

### 4.1 By group

| Group | Employment (m) | Human α | Human β | Human ζ | GPT-4 β | GPT-4 ζ | % emp human β ≥ 0.5 | % emp GPT-4 β ≥ 0.5 | % emp human ζ ≥ 0.5 |
|---|---|---|---|---|---|---|---|---|---|
| (a) Internet-era digital | 10.11 | 0.293 | **0.580** | 0.866 | **0.661** | 0.954 | 78.2 | 99.4 | 98.6 |
| a1 tech | 5.84 | 0.225 | 0.544 | 0.862 | 0.728 | 0.928 | 69.8 | 100.0 | 98.7 |
| a2 digital marketing and media | 1.19 | 0.110 | 0.521 | 0.933 | 0.527 | 0.996 | 79.5 | 100.0 | 100.0 |
| a3 digital clerical | 0.43 | 0.211 | 0.484 | 0.757 | 0.665 | 0.894 | 54.3 | 84.7 | 84.7 |
| a4 contact centre | 2.65 | 0.538 | 0.701 | 0.863 | 0.573 | 1.000 | 100.0 | 100.0 | 100.0 |
| (b) Pre-1995 physical | 89.14 | 0.081 | **0.181** | 0.282 | **0.207** | 0.326 | 1.5 | 4.0 | 16.3 |
| b1 physical major groups | 77.88 | 0.068 | 0.154 | 0.240 | 0.181 | 0.274 | 0.1 | 1.8 | 10.0 |
| b2 physical-sector white collar | 11.26 | 0.171 | 0.370 | 0.568 | 0.391 | 0.685 | 10.9 | 19.1 | 60.0 |
| (c) Pre-1995 office/professional | 33.49 | 0.225 | **0.485** | 0.745 | **0.551** | 0.894 | 53.6 | 63.9 | 93.7 |
| (d) Other pre-1995 | 22.74 | 0.264 | 0.427 | 0.590 | 0.413 | 0.674 | 30.0 | 30.1 | 52.1 |
| All matched occupations | 155.48 | 0.152 | 0.309 | 0.465 | 0.341 | 0.540 | 21.9 | 26.9 | 43.6 |

Bootstrap of the difference in employment-weighted mean human β (2,000 draws, resampling occupations within each group):
- A − B: 0.394, 95% CI [0.320, 0.466].
- A − C: 0.089, 95% CI [0.010, 0.165].
- A − C on GPT-4 β: 0.111, 95% CI [0.031, 0.208].

Distribution of exposure across groups:
- Share of exposure-weighted employment (Σ emp·β, human): A 12.2%, B 33.7%, C 33.9%, D 20.3%.
- Share of all workers with human β ≥ 0.5: A 23.2%, B 3.9%, C 52.8%, D 20.1%.

### 4.2 By SOC major group (employment-weighted human β, highest first)

The full table, including GPT-4 measures and threshold shares, is in `G_exposure_by_major_group.csv`.

| Major group | Human β | GPT-4 β | % emp human β ≥ 0.5 |
|---|---|---|---|
| 15 Computer and mathematical | 0.548 | 0.751 | 67.9 |
| 43 Office and administrative support | 0.526 | 0.602 | 71.7 |
| 13 Business and financial | 0.518 | 0.538 | 75.8 |
| 19 Life, physical and social science | 0.480 | 0.452 | 46.0 |
| 23 Legal | 0.466 | 0.468 | 7.3 |
| 17 Architecture and engineering | 0.448 | 0.518 | 37.5 |
| 41 Sales | 0.448 | 0.412 | 33.5 |
| 11 Management | 0.433 | 0.469 | 14.1 |
| 27 Arts, design and media | 0.424 | 0.478 | 30.0 |
| 21 Community and social service | 0.346 | 0.306 | 2.5 |
| 25 Education | 0.337 | 0.363 | 9.9 |
| 29 Healthcare practitioners | 0.302 | 0.348 | 3.0 |
| 39 Personal care | 0.249 | 0.181 | 1.5 |
| 33 Protective service | 0.239 | 0.239 | 0.0 |
| 31 Healthcare support | 0.161 | 0.177 | 0.0 |
| 53 Transportation and material moving | 0.144 | 0.184 | 0.0 |
| 35 Food preparation | 0.137 | 0.145 | 0.0 |
| 49 Installation and repair | 0.115 | 0.159 | 0.0 |
| 51 Production | 0.092 | 0.174 | 0.0 |
| 47 Construction | 0.086 | 0.123 | 0.0 |
| 45 Farming | 0.079 | 0.139 | 0.0 |
| 37 Building and grounds | 0.053 | 0.033 | 0.0 |

## 5. Sensitivity

Full results are in `G_sensitivity.csv`. Values are employment-weighted.

| Variant | A human β | A GPT-4 β | B human β | B GPT-4 β | A/B (human β) | A % emp β ≥ 0.5 |
|---|---|---|---|---|---|---|
| Baseline | 0.580 | 0.661 | 0.181 | 0.207 | 3.20 | 78.2 |
| A = a1 tech only | 0.544 | 0.728 | 0.181 | 0.207 | 3.00 | 69.8 |
| A = a1 + a2 | 0.540 | 0.694 | 0.181 | 0.207 | 2.98 | 71.4 |
| A without customer service reps | 0.536 | 0.694 | 0.181 | 0.207 | 2.96 | 70.7 |
| A without contact centres | 0.537 | 0.693 | 0.181 | 0.207 | 2.96 | 70.4 |
| A plus all of office/admin (43) | 0.529 | 0.628 | 0.181 | 0.207 | 2.92 | 71.7 |
| A plus office/admin (43) and sales (41) | 0.501 | 0.552 | 0.181 | 0.207 | 2.76 | 58.4 |
| B = physical majors only (b1) | 0.580 | 0.661 | 0.154 | 0.181 | 3.77 | 78.2 |
| B without healthcare practitioners | 0.580 | 0.661 | 0.167 | 0.191 | 3.46 | 78.2 |
| Imputed exposure rows dropped | 0.580 | 0.661 | 0.182 | 0.208 | 3.19 | 78.2 |
| `.00` O*NET code only | 0.579 | 0.669 | 0.180 | 0.203 | 3.21 | 73.1 |
| Unweighted (each occupation counts once) | 0.540 | 0.692 | 0.170 | 0.208 | 3.18 | 73.3 |

How α, β and ζ compare:
- The A/B ratio is largest on α: 0.293 / 0.081 = 3.6.
- On ζ the ratio is 0.866 / 0.282 = 3.1.
- On α, internet-era occupations reach only 0.29 (0.22 for tech alone). Direct exposure without complementary software therefore falls well short of half of their tasks. Only the contact centre sub-group exceeds 0.5 on α.

## 6. Findings relative to H

1. **Supported: the level of exposure.** Internet-era digital occupations have employment-weighted β of 0.58 on human ratings and 0.66 on GPT-4 ratings. Their β stays between 0.50 and 0.58 across all eleven reclassification and weighting variants. This is consistent with "roughly 50% of task content" on the β measure. On α the figure is about 0.29, and on ζ about 0.87, so the "about 50%" description depends on using the β definition.
2. **Supported: the physical-economy contrast.** Pre-1995 physical occupations have β of 0.18 on human ratings and 0.21 on GPT-4 ratings. Only 1.5% of their employment has β ≥ 0.5, against 78% in group A. The A/B ratio stays between 2.8 and 3.8 under every variant, and the bootstrap interval for the gap excludes zero by a wide margin. In the eleven core physical major groups (b1), only 0.1% of employment reaches β ≥ 0.5.
3. **Not supported: concentration in the internet era as such.** Pre-1995 office and professional occupations (group c) have β of 0.49 human and 0.55 GPT-4. That is about 0.09–0.11 below group A. The gap is statistically distinguishable from zero, but its 95% interval reaches down to 0.01. Office and administrative support (43) and business and financial operations (13) are almost as exposed as computer and mathematical occupations (15). On human β, office/admin has a larger share of employment above 50% than computer and mathematical occupations do (71.7% against 67.9%).
   - The data therefore separate information-processing work from physical work. They do not separate internet-era work from pre-1995 work.
   - Group A is small: 6.5% of employment. It holds 12% of exposure-weighted employment and 23% of the workers whose β is at least 0.5. Most highly exposed workers (53%) are in pre-1995 office and professional occupations.
4. **Rater difference.** GPT-4 rates tech occupations much higher than human annotators do: 0.73 against 0.54 on β, and 100% against 70% of employment at β ≥ 0.5. Software developers show the largest gap, at 0.87 against 0.45. The human and GPT-4 ratings agree closely for physical occupations. Under GPT-4 ratings the A versus C gap is a little larger than under human ratings.

## 7. Caveats

- **The classification is partly circular.** Group A was defined by information-processing content. The exposure rubric scores text and information tasks. A high score for A is therefore partly built in, and the clearer test is the comparison of A with C.
- **"Internet-era" is assigned by judgement, not measured.** The intended measure was the Autor, Chin, Salomons and Seegmiller (2024) share of employment in new work titles, and it could not be obtained (§3). Computer occupations, CIS managers and data scientists grew with the digital economy. Customer service representatives, data entry keyers, telemarketers, graphic designers and technical writers all existed before 1995, and some (data entry, telemarketing) are older routine-information occupations rather than products of the internet. Excluding a3 and a4 (tech plus digital marketing and media only) gives β = 0.54.
- **Exposure is a 2023 rubric measure of potential exposure.** It measures whether an LLM or LLM-powered software could cut task time by 50% or more. It does not measure adoption, displacement or wage effects. The occupation scores are unweighted means over O*NET tasks.
- **Imputation and missing data.** 47 residual codes, 2.0m employees (1.3% of employment), use imputed exposure. Dropping them changes no headline value by more than 0.005.
- **OEWS coverage.** OEWS covers wage and salary jobs only. Including the self-employed would add weight to group B and to arts and media occupations.
- **Possible title-matching error.** SOC codes were attached to May 2025 Table 1 rows by exact title match to the 2018-SOC list. One duplicated title (a broad group equal to its detailed occupation) carries the same employment number, so no figure is double counted.

## 8. Files
- `G_soc_classification.csv`: 831 detailed SOC codes with title, major group, group and sub-group, rule text, 2025 employment, exposure source and the six exposure measures.
- `G_exposure_by_group.csv`: groups, sub-groups and all occupations. Columns:
  - weighted means of the six measures
  - % of employment ≥ 0.5 on each measure
  - % of employment > 0.5 and ≥ 0.10 on β
  - unweighted means
- `G_exposure_by_major_group.csv`: the same statistics for the 22 SOC major groups.
- `G_sensitivity.csv`: the twelve variants in §5.
- `G_top_occupations_groupA.csv`: group A occupations ranked by employment.
- `raw/run_log.txt`: console output of the final run.
