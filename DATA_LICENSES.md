# Data licences

This repository is non-commercial research. Code is MIT-licensed (see `LICENSE`). Data keeps the licence of its publisher, recorded per source in `registry/sources/*.yaml`.

| Source | Licence | In this repo |
|---|---|---|
| ILOSTAT (ILO) | CC BY 4.0 | Raw and processed |
| World Bank WDI | CC BY 4.0 | Raw and processed |
| OECD Data Explorer | CC BY 4.0 | Raw and processed |
| Eurostat | CC BY 4.0 (Commission reuse policy, Decision 2011/833/EU) | Raw and processed |
| US BLS | Public domain (US federal work) | Raw and processed |
| FRED (US government series only) | Public domain at origin; FRED attribution requested | Raw and processed |
| ABS | CC BY 4.0 | Raw and processed |
| UN DESA Population Division | CC BY 3.0 IGO | Raw and processed |
| O*NET (US DOL/ETA) | CC BY 4.0 | Raw |
| Eloundou et al. (2024), GPTs-are-GPTs | MIT (repository licence) | Raw and derived |
| Curated series (`data/*/curated/`) | Figures from the publications cited row by row; reproduced as short factual extracts with source and URL | Curated CSV |

Sources whose terms restrict redistribution are registered with `redistribution: restricted`. For those, only fetch code, hashes and derived aggregates are committed. No microdata are stored.

Attribution for every figure: the source and URL columns in the data files, and the `source` printed under every chart.
