# Labour Market Policy

An open, continuously updated research base on global labour markets: official labour statistics curated from past to present, notebooks that analyse each data type, and an ongoing AI-labour monitor built on both.

Non-commercial research by [Dev Das](https://github.com/HackrLife). Code MIT; data under each publisher's licence ([DATA_LICENSES.md](DATA_LICENSES.md)).

## What is here

```
registry/sources/      one YAML file per publisher: datasets, endpoints, licence, release calendar
data/<data type>/      every dataset, filed by data type
   <source>/<dataset>/vintages/<date>/   each distinct release, untouched, with hash and URL
   <source>/<dataset>/latest.csv         tidy table from the latest release
   curated/                              historical series no API serves, with row-level sources
notebooks/<data type>/ analysis notebooks, re-executed against each new release
analysis/              scripted analyses (e.g. ai_exposure: task exposure by occupation group)
monitor/               dated AI-labour monitor entries written by the curator agent
docs/evidence/         verified literature and evidence notes with citations
src/labobs/            ingestion, validation, storage and notebook helpers
```

## Data types

| Folder | Covers |
|---|---|
| `employment` | employment, unemployment, participation, youth and NEET |
| `vacancies` | job openings, vacancy rates, shortage estimates |
| `wages` | earnings, labour income share, labour costs |
| `migration` | migrant stocks and flows, migrant employment, remittances |
| `adjustment` | sectoral reallocation, hires, quits, layoffs, occupational mix |
| `macro` | labour share, productivity, profits, wealth concentration, Okun and Phillips relations |
| `micro` | occupations, tasks, wages by occupation, AI task exposure |
| `demography` | fertility, ageing, urbanisation, population projections |
| `housing` | housing costs as a labour-market constraint |

The full dataset list, generated from the registry, is in [CATALOGUE.md](CATALOGUE.md).

## How it stays current

1. **Ingest** (`.github/workflows/ingest.yml`, daily 05:17 UTC) pulls every registered dataset with its full history. A new vintage is stored only when the publisher's file changes. Each vintage is validated (schema, truncation, revision share) before `latest.csv` is replaced, and the run is logged to `logs/runs/` and `DATA_CHANGELOG.md`.
2. **Analysis** (`.github/workflows/analysis.yml`) re-executes all notebooks after an ingest that brought new data, and weekly, then commits the rendered outputs. `notebooks/HEALTH.md` lists any notebook that failed.
3. **Curation** — the curator agent ([CURATOR.md](CURATOR.md)) reviews each run, repairs moved endpoints, writes the curator notes in each notebook, and adds monitor entries.

## Use

```bash
pip install -e ".[analysis]"
labobs list                        # every registered dataset
labobs list --domain migration     # one data type
labobs ingest --source worldbank   # pull one source locally
python -m unittest discover -s tests
```

In a notebook:

```python
from labobs.load import load, vintage, curated
youth = load("worldbank/unemployment_youth", ref_area=["AUS", "IND", "ZAF"])
vintage("worldbank/unemployment_youth")      # release date and hash in use
```

## Setup (one time)

- Repository secret `BLS_API_KEY` (free, https://data.bls.gov/registrationEngine/) raises BLS limits to 50 series and 20 years per request.
- Repository variable `LABOBS_CONTACT`: a contact address sent in the User-Agent, as several statistics offices request.
- Actions permissions: Settings → Actions → General → Workflow permissions → **Read and write**.
