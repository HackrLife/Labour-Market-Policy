# Registry verification — 24 October 2026

## Method and limits

Each dataset was checked against official documentation or a live response through WebFetch and WebSearch. The sandbox shell could not reach any of the data hosts. Most live API URLs were not on the fetch allowlist. The exceptions were `sdmx.oecd.org` (structure queries), one `sdmx.ilo.org` structure URL, `download.bls.gov` and a git clone of GitHub. As a result, `verified: true` means an official page or a live response confirmed the identifier and its meaning. It does not mean that a full data pull through the connector succeeded. The web search budget ran out before the last two World Bank codes could be checked. Those entries are marked unverified and the reason is given.

The registry now holds 45 datasets: the original 44 plus `eurostat/jvs_q_r21`. 27 are verified and 18 are not.

## What the SDMX connector needs for CSV

`fetch_sdmx` sends `Accept: p["accept"]` (default `application/vnd.sdmx.data+csv; charset=utf-8`) and passes `p["query"]` as URL parameters.

| Publisher | What returns CSV | Evidence | Registry setting now |
|---|---|---|---|
| Eurostat (SDMX 2.1) | Query parameter `format=SDMX-CSV`, which returns SDMX-CSV 1.0 flat. `compressed=true` returns `.gz`. Content negotiation through the Accept header is not documented. The dataset code goes in the path bare, e.g. `/data/une_rt_m`. | Eurostat API detailed guidelines › SDMX 2.1 › data query | `format: SDMX-CSV, compressed: "false"`. The undocumented `accept: text/csv` override was removed. |
| OECD (.Stat Suite) | Query parameter `format=csvfile` (codes) or `format=csvfilewithlabels` (codes and labels). The version segment may be omitted. The service is rate-limited. | OECD data explainer "API" (oecd.org/en/data/insights/data-explainers/2024/09/api.html) | `format: csvfile` kept. The Accept header was changed to `application/vnd.sdmx.data+csv;file=true`, which the .Stat Suite maps to `csvfile` (mapping documented by ABS for the same software). |
| ABS (.Stat Suite) | Accept header only: `application/vnd.sdmx.data+csv`, `text/csv`, `application/vnd.sdmx.data+csv;labels=both` or `…;file=true;labels=both`. No `format=` parameter is documented. If the version is omitted, it defaults to `latest`. The `all` key can time out on large flows. | ABS Data API user guide › Using the API, Worked examples | The connector default already works. Hard-coded `1.0.0` versions were removed. |
| ILOSTAT SDMX (alternative) | `https://sdmx.ilo.org/rest/data/ILO,DF_<INDICATOR without _A>,1.0/<key>?format=csv` or `Accept: application/vnd.sdmx.data+csv;version=1.0.0`. The guide says `format` overrides Accept. Dataflows are named `DF_<DSD_ID>`, with frequency as a key dimension. | ILOSTAT SDMX API Reference Guide (webapps.ilo.org/ilostat-files/Documents/SDMX_User_Guide.pdf) | Not used yet. See the ILOSTAT section. |

**One normaliser caveat:** `norm_sdmx` lower-cases column names and strips `:label` suffixes, so `csvfilewithlabels` and `labels=both` output also parses.

## ILOSTAT endpoint

- `https://rplumber.ilo.org/data/indicator/?id=<ID>` is still in use in 2026. The World Bank WDR 2026 reproducibility package cites `…/data/indicator?id=EMP_2EMP_SEX_STE_NB_A`, and an ERF working paper (Mar 2026) cites `…/data/indicator/?id=UNE_DEAP_SEX_AGE_RT_A&…&type=label`.
- `type=code` is consistent with the API. The connector's `format=.csv.gz` value was not confirmed. A public tutorial documents `format=.csv`. A third-party project fixed a broken `.csv.gz` URL on 20 Oct 2026.
- Rilostat 2.5.1 (16 Oct 2026), the official R client, downloads whole tables from `https://rplumber.ilo.org/files/indicator/<ID>.rds`. The `ilostat-files/WEB_bulk_download/indicator/<ID>.csv.gz` path is not documented as current on the bulk page, which uses placeholders only.
- **Recommendation:** before setting any ILOSTAT entry to verified, run one live pull with `format=.csv.gz`. If it fails, change `fetch_ilostat` to `format=.csv` (and drop the gzip expectation, which `norm_ilostat` already tolerates), or switch to the SDMX endpoint above with `format=csv`.

## Dataset table

| Key | Verified | Evidence | Change made |
|---|---|---|---|
| abs/labour_force | false | abs.gov.au Data API user guide (pattern, Accept); dataflow id LF only from a third-party client | Removed `,1.0.0` (latest); notes |
| abs/job_vacancies | false | as above; JV only from a third-party client | Removed `,1.0.0`; notes |
| abs/wage_price_index | false | as above; `ABS,WPI/all` in readabs docs | Removed `,1.0.0`; notes |
| bls/headline_monthly | true | bls.gov CPS errata page (LNS ids); bls.gov/web/empsit/cesseriespub.htm; FRED CES6562000001, CEU9000000001 | Notes only |
| bls/jolts | false | download.bls.gov/pub/time.series/jt/jt.txt (layout); jt.data.2.JobOpenings (JOL, JOR live); industry codes from a jt.industry mirror | Notes; industry ids unconfirmed live |
| bls/productivity_labour_share | true | fred.stlouisfed.org/series/PRS85006092, PRS85006173, PRS85006112 | Set verified; notes |
| bls/oews_national | true | bls.gov/oes/current/oes37.htm lists oesm25nat.zip | Set verified |
| bls/employment_projections | true | bls.gov/emp/tables.htm lists ind-occ-matrix/occupation.xlsx; 2025–35 release 27 Aug 2026 | Set verified |
| eurostat/une_rt_m | true | ec.europa.eu/eurostat/cache/metadata/en/une_rt_m_esms.htm | Removed `accept: text/csv` |
| eurostat/jvs_q_nace2 | false | Eurostat data browser title "(2001-2025)"; Statistics Explained uses jvs_q_r21 | Title marks it closed; notes; kept for history |
| eurostat/jvs_q_r21 | true | Eurostat Statistics Explained "Job vacancy statistics" (Sep 2026) | **New** NACE Rev. 2.1 successor |
| eurostat/lfsa_ergan | false | Mirrors only (DBnomics, EIGE) | Removed accept; notes |
| eurostat/migr_pop1ctz | true | ec.europa.eu/eurostat/cache/metadata/en/migr_ind_esmsip2.htm | Removed accept |
| eurostat/lc_lci_r2_q | true | Statistics Explained "Labour cost index – recent trends" (Jun 2026) | Removed accept; title "nominal value" |
| fred/distribution_and_profits | false | FRED pages for WFRBST01134, WFRBSN09161, CP, GDP, GDICOMP; ALFRED for WFRBSB50215 | **A4102C1Q027SBEA (wages and salaries only) → GDICOMP (compensation of employees)**; fredgraph endpoint not reached |
| fred/labour_market_extras | false | FRED pages for LNS12300060, LES1252881600Q | Frequency → mixed (LES… is quarterly); endpoint not reached |
| ilostat/unemployment_rate_modelled | false | DBnomics ILO/UNE_2EAP_SEX_AGE_RT; tutorial using the `_A` id | Notes (endpoint) |
| ilostat/employment_by_activity_modelled | false | DBnomics ILO/EMP_2EMP_SEX_ECO_NB | Notes |
| ilostat/employment_by_occupation_modelled | false | DBnomics ILO/EMP_2EMP_SEX_OCU_NB | Notes |
| ilostat/neet_youth_modelled | false | DBnomics ILO/EIP_2EET_SEX_RT | Notes |
| ilostat/labour_income_share | false | DBnomics ILO/LAP_2GDP_NOC_RT | Notes |
| ilostat/output_per_worker | false | DBnomics GDP_205U = 2015 US$; GDP_211P = PPP; ILOSTAT labour-productivity page (Nov 2025, 2021 PPP) | **GDP_205U_NOC_NB_A → GDP_211P_NOC_NB_A** |
| ilostat/mean_monthly_earnings | false | DBnomics ILO/EAR_4MTH_SEX_ECO_CUR_NB | Notes |
| ilostat/informality_rate | false | DBnomics ILO/EMP_NIFL_SEX_RT | Notes |
| ilostat/migrant_workers_by_citizenship | false | DBnomics ILO/MST_TEMP_SEX_AGE_CCT_NB; ILOSTAT labour-migration topic page | **EMP_TEMP_SEX_CCT_NB_A (not found) → MST_TEMP_SEX_AGE_CCT_NB_A**; title adds age |
| oecd/unemployment_monthly | false | DBnomics provider link only (OECD.SDD.TPS, v1.0) | Accept header → `…+csv;file=true` |
| oecd/house_prices | true | OECD Data Explorer URL (df[ag]=OECD.ECO.MPD) | Accept header |
| oecd/average_annual_wages | true | Live: sdmx.oecd.org/public/rest/dataflow/OECD.ELS.SAE/DSD_EARNINGS@AV_AN_WAGE/1.0 | Accept header |
| oecd/migration_flows | true | OECD Data Explorer "(DSD_MIG@DF_MIG) International migration database" | Version dropped (latest); title widened; measure filter needed for inflows |
| research/gpts_occ_exposure | true | Live git clone of openai/gpts-are-gpts (main; MIT; header checked) | Notes corrected (column names; analysis/ path) |
| research/onet_database | true | onetcenter.org What's New (31.0, Aug 2026); /dictionary/31.0/csv/ | **db_30_0_text.zip → db_31_0_csv.zip** (no text zip listed for 31.0) |
| undesa/migrant_stock_2024 | true | un.org/development/desa/pd/node/3315 | **URL corrected** (removed `files/documents/2025/Jan/`); licence caveat |
| undesa/wpp_2024_indicators | false | Third-party quote of the URL and the CC BY 3.0 IGO terms; official page script-rendered | Notes |
| worldbank/unemployment_total | true | data.worldbank.org/indicator/SL.UEM.TOTL.ZS | Notes |
| worldbank/unemployment_youth | true | WDI glossary SL.UEM.1524.ZS | Notes |
| worldbank/lfpr_total | true | WDI glossary SL.TLF.CACT.ZS | Notes |
| worldbank/emp_agriculture_share | true | data.worldbank.org/indicator/SL.AGR.EMPL.ZS | Title adds "modelled ILO estimate" |
| worldbank/emp_industry_share | true | WDI glossary SL.IND.EMPL.ZS | Title |
| worldbank/emp_services_share | true | WDI glossary SL.SRV.EMPL.ZS | Title |
| worldbank/migrant_stock | true | WDI glossary SM.POP.TOTL | Notes on periodicity |
| worldbank/remittances_received | true | data.worldbank.org/indicator/BX.TRF.PWKR.CD.DT | Notes |
| worldbank/gdp_per_person_employed | true | data.worldbank.org/indicator/SL.GDP.PCAP.EM.KD; OWID WDI metadata | false → true |
| worldbank/fertility_rate | false | Not retrieved (fetch failed; search budget exhausted) | true → false |
| worldbank/age_dependency_old | false | Not retrieved | true → false |
| worldbank/urban_population_share | true | data.worldbank.org/indicator/SP.URB.TOTL.IN.ZS | Notes |

## Licence and redistribution fields

- World Bank (CC BY 4.0), O*NET (CC BY 4.0), BLS (public domain) and the GPTs-are-GPTs repository (MIT) are confirmed.
- FRED series carry FRED's own tag "Public Domain: Citation Requested", so `attribution` is appropriate.
- WPP 2024 is CC BY 3.0 IGO, quoted from the producer's terms through a third party.
- The International Migrant Stock page states no licence. Check the UN terms of use before redistributing that file.
- ILOSTAT (CC BY 4.0), OECD (CC BY 4.0 since July 2024), Eurostat (CC BY 4.0 under Decision 2011/833/EU) and ABS (CC BY 4.0) were not re-confirmed this session. They are left as recorded.

## Not done

- BLS API v2 limits were not re-confirmed. The connector assumes 25 series and 10 years per query without a key, and 50 series and 20 years with a key.
- No full data pull was run for any connector.
