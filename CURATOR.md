# Curator

The curator keeps this repository current and interprets what changes. Ingestion itself runs in GitHub Actions (`ingest.yml`, daily); the curator works on top of each run. These are its standing instructions.

## Each run

1. **Read the run.** Open the newest `logs/runs/<date>.json` and the latest `DATA_CHANGELOG.md` entry. List datasets that were published, unchanged, failed or rejected.
2. **Triage failures.**
   - `failed` with HTTP 404/400: the publisher moved or renamed the dataset. Find the current identifier from the publisher's documentation, fix `registry/sources/<source>.yaml`, and note the evidence URL in `registry/VERIFICATION.md`.
   - `failed` with 403/429/timeouts: transient or rate-limited. Leave it for the next run; escalate if it fails three runs in a row (`registry/status.json`).
   - `rejected`: validation caught a truncated pull (row count fell >20%) or a schema change. Inspect the raw vintage; never overwrite `latest.csv` by hand.
3. **Read the revisions.** For each new vintage, check `added`, `revised` and the latest period. More than 25% of observations revised usually means a benchmark revision; record it, because it changes every derived chart.
4. **Update the notebooks' curator notes.** After the analysis workflow re-renders the notebooks, write two to five sentences in the "Curator notes" cell of each notebook whose data changed: the new reading, the change on the prior period and year, and anything the revision altered. Every number cites the dataset key and vintage date.
5. **Write the monitor entry.** Add `monitor/<YYYY-MM-DD>.md` (template below) when any of the AI-labour indicators changed.

## Curating new sources

A new dataset enters `registry/sources/` only when:
- the publisher is an official statistical body, an international organisation, or a peer-reviewed replication archive;
- the licence permits redistribution (`open` or `attribution`); otherwise it is registered as `restricted` and only derived aggregates are published;
- the identifier has been confirmed against the publisher's documentation or a live response (`verified: true`).

Historical series that no API serves (pre-1990 sector shares, published research tables) go to `data/<domain>/curated/` as CSV with `series, region, period, value, unit, source, url` and are never edited silently: corrections are new rows or new files, noted in `DATA_CHANGELOG.md`.

## AI-labour monitor: indicators tracked

| Indicator | Dataset |
|---|---|
| Unemployment and youth unemployment by economy | `worldbank/unemployment_*`, `eurostat/une_rt_m`, `abs/labour_force`, `bls/headline_monthly` |
| Openings rates: health, construction, manufacturing vs information | `bls/jolts`, `eurostat/jvs_q_nace2`, `abs/job_vacancies` |
| Employment in information vs health care vs construction | `bls/headline_monthly` |
| Labour share and productivity | `bls/productivity_labour_share`, `ilostat/labour_income_share` |
| Wealth concentration and profits | `fred/distribution_and_profits` |
| Task exposure by occupation group | `analysis/ai_exposure` (re-run on each OEWS release) |
| Hires, quits, layoffs | `bls/jolts` |

## Monitor entry template

```markdown
# AI-labour monitor — YYYY-MM-DD

**New releases this period:** dataset keys and vintages.

## What moved
- One line per indicator that changed, with the number, the prior value and the source key.

## Reading
Three to six sentences: whether the information layer (exposed occupations, information-sector employment and openings) is diverging further from the physical economy (health, construction, energy), and what the revision record changes in that reading.

## Watch
Releases due before the next entry.
```

## Rules

- Never fabricate or estimate a figure that a dataset does not contain. If a number is not in the data, say so.
- Never edit raw vintages.
- Keep analytical choices (filters, base years, deflators) in notebooks, where they are visible, not in connectors.
