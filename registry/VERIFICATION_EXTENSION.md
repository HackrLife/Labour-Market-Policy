# Registry extension: verification log (2026-10-24)

This log covers the new source files added to `registry/sources/`. The files that were already there (abs, bls, eurostat, fred, ilostat, oecd, research, undesa, worldbank) were not changed.

**What `verified: true` means here.** The identifier or URL was confirmed against the publisher's own page or documentation, for example a download href copied from the release page. No file had been downloaded at registration; the first ingest run confirms each entry. When a pull fails, set the entry back to `verified: false`.

## Datasets

| Key | Verified | Redistribution | Evidence | Connector change needed |
|---|---|---|---|---|
| ggdc/pwt_110 | true | open (CC BY 4.0) | https://www.rug.nl/ggdc/productivity/pwt/pwt-releases/pwt110 (xlsx = dataverse datafile/554105, DOI 10.34894/FABVLR) | The sheet name is not known yet, so `parse: none`. After opening the file, set `parse: xlsx` and `sheet`. |
| ggdc/pwt_110_na | true | open | Same release page (datafile/554022) | None |
| ggdc/maddison_2023 | true | open (CC BY 4.0) | https://rug.nl/ggdc/historicaldevelopment/maddison/releases/maddison-project-database-2023 (datafile/421302, DOI 10.34894/INZBF2). The sheet name `Full data` comes from the CRAN MaddisonData vignette. | None |
| ggdc/etd | true | open (CC BY 4.0) | https://www.rug.nl/ggdc/structuralchange/etd/ (datafile/382704, DOI 10.34894/LCH4CA). Covers 1990–2018 only. | The sheet layout is unconfirmed, so `parse: none`. |
| ggdc_10sd/ten_sector_2014 | false | restricted | https://www.rug.nl/ggdc/structuralchange/previous-sector-database/10-sector-2014 still lists `10sd_jan15_2014.xlsx`, but the page names no licence. | None. The GGDC copyright page needs a review before any redistribution. |
| owid/annual_working_hours | true | attribution | https://ourworldindata.org/grapher/annual-working-hours-per-worker?tab=table. Sources are Huberman & Minns (1870–1938) and PWT 11.0. | Rename the columns Entity/Code/Year in a notebook. |
| fred_longrun/ces_longrun | true | attribution | https://fred.stlouisfed.org/data/PAYEMS and /data/MANEMP (both start 1939-01) | None (existing `fred` connector) |
| fred_longrun/ces_information | false | attribution | The 1939 start date comes from the GHDx catalogue (FRED/USINFO); the FRED page itself was not reached. | None |
| ons/lfs_unemployment_rate | true | open (OGL v3) | The CSV href on https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/unemployment/timeseries/mgsx/lms | **Add parse kind `ons_ts`** (described below). |
| ons/vacancies_total | true | open | The CSV href on .../timeseries/ap2y/unem | `ons_ts` |
| ons/awe_total_pay | true | open | The CSV href on .../timeseries/kab9/emp | `ons_ts` |
| statcan/lfs_characteristics_monthly | true | attribution (StatCan Open Licence) | The URL pattern comes from https://www.statcan.gc.ca/en/developers/tips, which uses this exact table as its example. The zip members are named in the CSV user guide. The title was checked in The Daily (2026-02-06). | None (`zip_csv`) |
| statcan/job_vacancies_monthly_nsa | true | attribution | Table 14-10-0371-01 appears in The Daily (2024-12-19). It is monthly, not quarterly. | None |
| statcan/job_vacancies_monthly_sa | true | attribution | open.canada.ca dataset 1862cd2e-… (table 14-10-0432-01) | None |
| statsnz/hlfs_headline | false | attribution | https://portal.apis.stats.govt.nz/how-to-subscribe says a key is required in the `Ocp-Apim-Subscription-Key` header. The base URL and the dataflow are not published on any page that could be reached. | **sdmx `headers_env`**: read the key from env `STATSNZ_API_KEY`. The URL is still TBD. |
| estat_japan/lfs_long_series | false | attribution (Japan Gov Standard Terms v2.0, compatible with CC BY 4.0) | Endpoint pattern from https://www.e-stat.go.jp/api/en/node/166. The appId is issued on registration (https://www.e-stat.go.jp/api/terms-of-use). The statsDataId is TBD. | **http `query` + env injection** for `appId` (env `ESTAT_APP_ID`). The API also requires a credit line. |
| kosis/eaps_unemployment | false | restricted | Endpoint and parameters from the kosis R package manual and https://kosis.kr/serviceInfo/openAPIGuide.do. The tblId is TBD and the terms page was unreachable. | **http `query` + env injection** for `apiKey` (env `KOSIS_API_KEY`), plus a JSON normaliser. |
| mospi/plfs | false | restricted | PLFS is listed in MoSPI's official MCP server (nso-india/esankhyiki-mcp). The data host is api.mospi.gov.in and needs no key. The REST paths sit in that repo's `swagger/` folder, which could not be read from at compilation (24 October 2026). | URL TBD, plus a JSON normaliser. |
| nbs_china/urban_surveyed_unemployment | false | restricted | NBS documents no API. Community packages scrape an undocumented endpoint. | Not recommended. Use ILOSTAT or IMF WEO for China instead. |
| ibge/pnadc_unemployment_quarterly | false | attribution | The base URL and path grammar come from the sidrar CRAN docs. Table 4099 is described as the quarterly unemployment rate. The variable code inside 4099 was not confirmed, and table 6381 could not be confirmed at all, so it is omitted. | A SIDRA JSON normaliser: the first record is the header, and fields are D*C/V. |
| statssa/qlfs | false | restricted | The portal (isibaloweb.statssa.gov.za …/qlfs2025.php) offers CSV/SPSS/Stata downloads, but only through links the page builds itself, with no stable URL or API. | URL TBD. Use ILOSTAT for headline series. |
| imf/weo_unemployment | false | attribution (IMF terms; bulk automated download needs permission) | The base URL comes from https://browser.sdmx.io/agencies/IMF. The path, key order, `LUR` code and `Accept: text/csv` come from third-party worked examples (bd-econ.com, rogermariolopez.com). The IMF's own pages mention registering on the portal. | Probably none (existing `sdmx`). If the IMF requires a key, add a `headers_env` subscription key. |
| oecd_alfs/alfs_summary | false | open | DBnomics lists the flow DSD_ALFS@DF_SUMTAB v1.0. The agency OECD.SDD.TPS is inferred, not confirmed. | None |
| oecd_alfs/alfs_employment_activity | false | open | Agency and version 1.1 come from a third-party mirror. | None |

## Connector extensions needed (Python not edited)

1. **`http` query parameters.** `fetch_http` calls `_get(p["url"], headers=…)` but does not pass `params`. Change it to `_get(url, headers=…, params=p.get("query"))`.
2. **Secrets from the environment.** Add a helper that turns any `*_env` key into a real value. For example, `query.appId_env: ESTAT_APP_ID` becomes `appId=os.environ["ESTAT_APP_ID"]`, and `headers_env: {Ocp-Apim-Subscription-Key: STATSNZ_API_KEY}` becomes a request header with that value. Apply it in both `fetch_http` and `fetch_sdmx`. Keys must never appear in `Fetched.url` or in the logs; `r.url` currently contains the query string, so redact it. The environment variables are `ESTAT_APP_ID`, `KOSIS_API_KEY` and `STATSNZ_API_KEY`, plus an optional `IMF_API_KEY`.
3. **Parse kind `ons_ts`.** ONS generator CSVs begin with about 7 quoted metadata rows (Title, CDID, Source dataset ID, …). Annual, quarterly and monthly rows then share one pair of columns, with periods written as `1971`, `1971 Q1` and `1971 JAN`. The parser should skip rows until the first one that matches `^\d{4}`, convert each label to `YYYY`, `YYYY-Qn` or `YYYY-MM`, and keep a `frequency` column.
4. **JSON normalisers** for SIDRA (array whose first element is the header record), KOSIS (`PRD_DE`, `DT`, `ITM_ID`, `C1`) and the MoSPI eSankhyiki API.
5. **Placeholder URLs.** Entries with `url: TBD` load correctly but fail on pull. You could make `labobs pull` skip any entry whose URL is `TBD` and log a warning.
