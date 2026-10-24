"""Generate the analysis notebooks from one specification.

Run:  python notebooks/_build.py
Every notebook gets the same header (purpose, datasets, vintage check) and
footer (curator notes). Edit the specs here, not the .ipynb files, so the
notebooks stay consistent; executed outputs are written by the analysis
workflow.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

SETUP = """import pandas as pd
import matplotlib.pyplot as plt
from labobs.load import load, vintage, curated, raw_payload
from labobs.nb import select, pivot, latest, plot_lines, plot_bars, to_annual, FOCUS, FOCUS_NAMES
pd.set_option("display.max_rows", 80)
pd.set_option("display.float_format", "{:,.2f}".format)"""


def vintage_cell(keys):
    return ("DATASETS = " + json.dumps(keys) + "\n"
            "for k in DATASETS:\n"
            "    v = vintage(k)\n"
            "    print(f\"{k:50} vintage {v.get('vintage', 'not yet ingested'):12} sha {v.get('sha256', '')[:12]}\")")


FOOTER = """## Curator notes

_Written by the curator agent after each new vintage: what changed, which revisions matter, and what to watch. See `DATA_CHANGELOG.md` for the full log._"""


def nb(title, purpose, datasets, cells, curated_inputs=()):
    src = [("md", f"# {title}\n\n{purpose}\n\n"
                  f"**Datasets:** {', '.join('`'+d+'`' for d in datasets) or '—'}"
                  + (f"  \n**Curated inputs:** {', '.join('`'+c+'`' for c in curated_inputs)}" if curated_inputs else "")
                  + "\n\nThis notebook reads the latest vintage each time it runs; re-run after a new release to update every table and chart."),
           ("code", SETUP)]
    if datasets:
        src.append(("code", vintage_cell(datasets)))
    src += cells
    src.append(("md", FOOTER))
    out = []
    for kind, text in src:
        lines = text.strip("\n").splitlines(keepends=True)
        if kind == "md":
            out.append({"cell_type": "markdown", "metadata": {}, "source": lines})
        else:
            out.append({"cell_type": "code", "metadata": {}, "execution_count": None,
                        "outputs": [], "source": lines})
    return {"cells": out, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python",
                                                       "name": "python3"},
                                       "language_info": {"name": "python"}},
            "nbformat": 4, "nbformat_minor": 5}


M, C = "md", "code"

SPECS = {
# ------------------------------------------------------------------ employment
"employment/01_global_unemployment.ipynb": nb(
    "Global unemployment",
    "Unemployment rates across economies since 1991 (ILO modelled estimates via the World Bank), with the latest reading, the change on the prior year, and the gap between each economy and the world rate.",
    ["worldbank/unemployment_total", "ilostat/unemployment_rate_modelled"],
    [(M, "## Latest reading by economy"),
     (C, 'u = load("worldbank/unemployment_total")\nlatest(select(u, ref_area=FOCUS))'),
     (C, 'p = pivot(select(u, ref_area=FOCUS))\nplot_lines(p, "Unemployment rate, % of labour force", "%", "ILO modelled estimates via World Bank WDI (SL.UEM.TOTL.ZS)");'),
     (M, "## Distance from the world rate"),
     (C, 'gap = p.sub(p["WLD"], axis=0).drop(columns="WLD")\ngap.tail(5).T.sort_values(gap.index[-1])'),
     (M, "## By sex (ILO modelled estimates)\nRows are filtered to total age 15+; `sex` takes SEX_T, SEX_M, SEX_F."),
     (C, 'ilo = load("ilostat/unemployment_rate_modelled")\nprint(ilo.columns.tolist())\nprint(ilo["classif1"].drop_duplicates().head(20).tolist())'),
     (C, 'f = select(ilo, ref_area=FOCUS, classif1="AGE_YTHADULT_YGE15")\nsexgap = pivot(f, columns="sex").assign(gap=lambda d: d["SEX_F"] - d["SEX_M"])\nsexgap.tail(10)')]),

"employment/02_youth_unemployment_neet.ipynb": nb(
    "Youth unemployment and NEET",
    "How far young people trail the overall labour market: youth (15–24) unemployment, the youth-to-total ratio, and the share of youth not in employment, education or training.",
    ["worldbank/unemployment_youth", "worldbank/unemployment_total", "ilostat/neet_youth_modelled"],
    [(C, 'y = pivot(select(load("worldbank/unemployment_youth"), ref_area=FOCUS))\nt = pivot(select(load("worldbank/unemployment_total"), ref_area=FOCUS))\nplot_lines(y, "Youth unemployment rate (15–24), %", "%", "ILO modelled estimates via World Bank WDI (SL.UEM.1524.ZS)");'),
     (M, "## Youth-to-total unemployment ratio\nA ratio above 2 means a young person is more than twice as likely to be unemployed as the average worker."),
     (C, 'ratio = (y / t).dropna(how="all")\nplot_bars(ratio.ffill().iloc[-1], f"Youth / total unemployment ratio, {ratio.index[-1]}", "ratio", "World Bank WDI");'),
     (M, "## NEET share"),
     (C, 'neet = load("ilostat/neet_youth_modelled")\nlatest(select(neet, ref_area=FOCUS, sex="SEX_T"))'),
     (M, "## Latest national releases (curated)\nNational definitions differ in age band (15–24, 16–24, 15–29); compare levels within rows, not across them."),
     (C, 'curated("employment", "youth_labour_markets")[["region", "series", "value", "unit", "period", "source"]]')],
    ["employment/youth_labour_markets"]),

"employment/03_us_labour_market.ipynb": nb(
    "United States: labour market and sector employment",
    "Headline CPS and CES series since 1990, and the reallocation of payroll employment across manufacturing, construction, information and health care.",
    ["bls/headline_monthly"],
    [(C, 'h = load("bls/headline_monthly")\nur = pivot(select(h, indicator=["LNS14000000", "LNS14000012"]), columns="indicator_label")\nplot_lines(ur, "US unemployment rate", "%", "BLS CPS", names={});'),
     (M, "## Sector employment, index 1995 = 100"),
     (C, 'sec = ["CES3000000001", "CES2000000001", "CES5000000001", "CES6562000001", "CES0000000001"]\ns = pivot(select(h, indicator=sec), columns="indicator_label")\nbase = s.loc[s.index.str.startswith("1995")].mean()\nplot_lines(s / base * 100, "Payroll employment by sector, 1995 = 100", "index", "BLS CES", names={});'),
     (M, "## Share of nonfarm employment"),
     (C, 'tot = pivot(select(h, indicator="CES0000000001"), columns="indicator")["CES0000000001"]\nshare = s.drop(columns=[c for c in s.columns if "Total" in c]).div(tot, axis=0) * 100\nshare.iloc[[0, -1]].T.rename(columns=lambda c: f"share {c}")')]),

"employment/04_australia_labour_force.ipynb": nb(
    "Australia: Labour Force",
    "ABS Labour Force headline estimates. The first cells list the dimensions and codes in the latest vintage so the series selection below can be checked against the ABS data structure.",
    ["abs/labour_force"],
    [(C, 'lf = load("abs/labour_force")\ndims = [c for c in lf.columns if c not in ("source", "dataset", "value", "period", "ref_area", "indicator")]\n{d: lf[d].drop_duplicates().head(12).tolist() for d in dims}'),
     (M, "## Unemployment and participation\nSet the codes below from the dimension listing (ABS LF: MEASURE M13 = unemployment rate, M12 = participation rate; TSEST 20 = seasonally adjusted; SEX 3 = persons; AGE 1599 = 15+, 1524 = 15–24). Confirm against the listing above if ABS revises its codelists."),
     (C, 'SEL = dict(measure="M13", tsest=20, sex=3, region="AUS")\nsel = {k: v for k, v in SEL.items() if k in lf.columns}\nu = select(lf, **sel)\nage_col = "age" if "age" in u.columns else None\np = pivot(u, columns=age_col) if age_col else pivot(u, columns="indicator")\nplot_lines(p.tail(240), "Australia: unemployment rate (seasonally adjusted)", "%", "ABS Labour Force, Australia", names={});')]),

"employment/05_europe_unemployment.ipynb": nb(
    "Europe: unemployment, total and under-25",
    "Eurostat monthly unemployment (seasonally adjusted, % of labour force) for total and under-25 populations.",
    ["eurostat/une_rt_m"],
    [(C, 'e = load("eurostat/une_rt_m")\ne = select(e, s_adj="SA", sex="T", unit="PC_ACT")\nareas = ["EA20", "EU27_2020", "DE", "FR", "IT", "ES", "SE", "PL", "NL"]\nlatest(select(e, age="Y_LT25", ref_area=areas))'),
     (C, 'plot_lines(pivot(select(e, age="Y_LT25", ref_area=areas)).loc["2005":], "Under-25 unemployment rate (SA)", "%", "Eurostat une_rt_m", names={});'),
     (C, 'plot_lines(pivot(select(e, age="TOTAL", ref_area=areas)).loc["2005":], "Unemployment rate, total (SA)", "%", "Eurostat une_rt_m", names={});')]),

# ------------------------------------------------------------------ vacancies
"vacancies/01_us_beveridge_curve.ipynb": nb(
    "United States: Beveridge curve",
    "Job openings rate against the unemployment rate since December 2000. Outward shifts indicate lower matching efficiency; movements along the curve reflect the cycle.",
    ["bls/jolts", "bls/headline_monthly"],
    [(C, 'jo = pivot(select(load("bls/jolts"), indicator="JTS000000000000000JOR"), columns="indicator")\nur = pivot(select(load("bls/headline_monthly"), indicator="LNS14000000"), columns="indicator")\nbc = jo.join(ur, how="inner").dropna()\nbc.columns = ["openings_rate", "unemployment_rate"]\nbc.tail()'),
     (C, 'fig, ax = plt.subplots(figsize=(8, 6))\nyears = bc.index.str[:4].astype(int)\nsc = ax.scatter(bc.unemployment_rate, bc.openings_rate, c=years, cmap="viridis", s=14)\nax.plot(bc.unemployment_rate, bc.openings_rate, color="#999", linewidth=0.4)\nax.annotate(bc.index[-1], (bc.unemployment_rate.iloc[-1], bc.openings_rate.iloc[-1]))\nax.set_xlabel("Unemployment rate, %"); ax.set_ylabel("Job openings rate, %")\nax.set_title("US Beveridge curve", loc="left", fontweight="bold")\nfig.colorbar(sc, label="year"); fig.text(0.01, -0.02, "Source: BLS JOLTS and CPS", fontsize=8);'),
     (M, "## Vacancies per unemployed person"),
     (C, 'h = load("bls/headline_monthly")\nopen_lvl = pivot(select(load("bls/jolts"), indicator="JTS000000000000000JOL"), columns="indicator").iloc[:, 0]\nunemp = None  # unemployment level (LNS13000000) can be added to bls/headline_monthly to compute V/U directly\nopen_lvl.tail(12)')]),

"vacancies/02_us_openings_by_industry.ipynb": nb(
    "United States: job openings by industry",
    "Openings rates by industry from JOLTS: where unmet labour demand sits relative to the economy-wide rate.",
    ["bls/jolts"],
    [(C, 'j = load("bls/jolts")\nrates = pivot(select(j, indicator=[c for c in j.indicator.unique() if c.endswith("JOR")]), columns="indicator_label")\nplot_lines(rates.loc["2015":], "Job openings rate by industry", "%", "BLS JOLTS", names={});'),
     (C, 'rates.iloc[-1].sort_values(ascending=False).to_frame(rates.index[-1])'),
     (M, "## Curated snapshot (with private and public education)"),
     (C, 'curated("vacancies", "jolts_by_industry_2025_2026").pivot_table(index="industry", columns="period", values="openings_rate")')],
    ["vacancies/jolts_by_industry_2025_2026"]),

"vacancies/03_eu_job_vacancy_rates.ipynb": nb(
    "Europe: job vacancy rates by activity",
    "Eurostat quarterly job vacancy rate (vacancies as a share of occupied plus vacant posts) by activity, splicing the closed NACE Rev. 2 table (to 2025) with the NACE Rev. 2.1 table; where both report a quarter, Rev. 2.1 is kept.",
    ["eurostat/jvs_q_r21", "eurostat/jvs_q_nace2"],
    [(C, 'v = pd.concat([load("eurostat/jvs_q_nace2").assign(nace_rev="2"), load("eurostat/jvs_q_r21").assign(nace_rev="2.1")])\nv = v.sort_values("nace_rev").drop_duplicates([c for c in v.columns if c not in ("value", "nace_rev", "dataset", "obs_flag")], keep="last")\nprint({c: v[c].drop_duplicates().head(15).tolist() for c in ["indic_em", "nace_r2", "sizeclas"] if c in v.columns})'),
     (C, 'sel = dict(indic_em="JOBRATE")\nif "sizeclas" in v.columns: sel["sizeclas"] = "TOTAL"\nr = select(v, **sel)\nact = {"B-S": "Industry, construction & services", "F": "Construction", "Q": "Health & social work", "J": "Information & communication", "C": "Manufacturing", "P": "Education", "D": "Energy"}\nea = select(r, ref_area="EU27_2020", nace_r2=list(act))\nplot_lines(pivot(ea, columns="nace_r2").rename(columns=act).loc["2015":], "EU27 job vacancy rate by activity", "%", "Eurostat jvs_q_nace2", names={});')]),

"vacancies/04_labour_shortage_estimates.ipynb": nb(
    "Labour shortage estimates: health, energy, manufacturing, construction, education",
    "Curated projections and survey measures of unmet labour demand from WHO, IEA, US DOE, Deloitte/Manufacturing Institute, ABC, UNESCO, Jobs and Skills Australia and EURES. Each row carries its source URL.",
    [],
    [(C, 'sh = curated("vacancies", "labour_shortage_estimates")\nsh[["region", "sector", "series", "value", "unit", "period", "source"]].sort_values(["sector", "region"])'),
     (M, "These are projections and survey measures with different definitions and horizons; they establish order of magnitude and direction, not a common unit.")],
    ["vacancies/labour_shortage_estimates"]),

# ------------------------------------------------------------------ wages
"wages/01_labour_income_share.ipynb": nb(
    "Labour income share",
    "Labour's share of GDP (ILO modelled estimates, including an imputation for the self-employed) and its change since 2004.",
    ["ilostat/labour_income_share"],
    [(C, 'ls = select(load("ilostat/labour_income_share"), ref_area=FOCUS)\nplot_lines(pivot(ls), "Labour income share, % of GDP", "%", "ILO modelled estimates (LAP_2GDP_NOC_RT_A)");'),
     (C, 'p = pivot(ls)\n(p.iloc[-1] - p.loc[p.index.astype(str) == "2004"].iloc[0]).sort_values().to_frame(f"change 2004–{p.index[-1]} (pp)")')]),

"wages/02_oecd_average_wages.ipynb": nb(
    "OECD average annual wages",
    "Average annual wages per full-time-equivalent employee, constant prices and PPP; real growth since 2000.",
    ["oecd/average_annual_wages"],
    [(C, 'w = load("oecd/average_annual_wages")\nprint({c: w[c].drop_duplicates().head(10).tolist() for c in w.columns if c not in ("value", "period", "ref_area")})'),
     (C, 'cols = [c for c in ("unit_measure", "price_base", "unit_mult") if c in w.columns]\nprint("Filter on these to pick constant-price PPP USD:", cols)\nsel = {}\nif "price_base" in w.columns: sel["price_base"] = "Q"\nreal = select(w, **sel) if sel else w\np = pivot(select(real, ref_area=[a for a in FOCUS if a in set(real.ref_area)]))\nplot_lines(p / p.loc[p.index.astype(str) == "2000"].iloc[0] * 100, "Real average wages, 2000 = 100", "index", "OECD Average annual wages");')]),

"wages/03_earnings_by_activity.ipynb": nb(
    "Earnings by economic activity",
    "Average monthly earnings of employees by activity (ILO national series): how pay in health, education, construction, utilities and information compares with the economy-wide mean in each country.",
    ["ilostat/mean_monthly_earnings"],
    [(C, 'e = load("ilostat/mean_monthly_earnings")\nprint(e["classif1"].drop_duplicates().tolist()[:40])'),
     (C, 'e = select(e, sex="SEX_T")\nacts = [c for c in e.classif1.unique() if c.startswith("ECO_ISIC4_")]\nrel = e[e.classif1.isin(acts + ["ECO_ISIC4_TOTAL"])]\nlast = rel.sort_values("period").groupby(["ref_area", "classif1"]).tail(1)\ntab = last.pivot_table(index="ref_area", columns="classif1", values="value")\n(tab.div(tab["ECO_ISIC4_TOTAL"], axis=0)).loc[[a for a in FOCUS if a in tab.index]].round(2)')]),

"wages/04_eu_labour_costs.ipynb": nb(
    "Europe: labour cost index",
    "Eurostat quarterly labour cost index by activity: wage and non-wage cost growth across sectors.",
    ["eurostat/lc_lci_r2_q"],
    [(C, 'l = load("eurostat/lc_lci_r2_q")\nprint({c: l[c].drop_duplicates().head(12).tolist() for c in l.columns if c not in ("value", "period", "ref_area", "source", "dataset")})'),
     (C, 'sel = {k: v for k, v in dict(unit="PCH_SM", s_adj="SCA", lcstruct="D1_D4_MD5").items() if k in l.columns}\nx = select(l, ref_area="EU27_2020", **sel)\nplot_lines(pivot(x, columns="nace_r2").loc["2015":], "EU27 labour cost growth, % y/y", "%", "Eurostat lc_lci_r2_q", names={});')]),

# ------------------------------------------------------------------ migration
"migration/01_international_migrant_stock.ipynb": nb(
    "International migrant stock",
    "Migrant stock by destination over time (UN DESA via the World Bank), and the full origin–destination matrix from the UN DESA 2024 release.",
    ["worldbank/migrant_stock", "undesa/migrant_stock_2024"],
    [(C, 'm = load("worldbank/migrant_stock")\nlatest(select(m, ref_area=FOCUS))'),
     (C, 'p = pivot(select(m, ref_area=[a for a in FOCUS if a != "WLD"]))\nplot_lines(p / 1e6, "International migrant stock", "millions", "UN DESA via World Bank (SM.POP.TOTL)");'),
     (M, "## Origin–destination matrix (UN DESA 2024)"),
     (C, 'x = pd.ExcelFile(raw_payload("undesa/migrant_stock_2024"))\nprint(x.sheet_names)'),
     (C, 'df = pd.read_excel(x, sheet_name="Table 1", header=10)\ndf.head()')]),

"migration/02_remittances.ipynb": nb(
    "Remittances",
    "Personal remittances received: the largest recipients and long-run growth. Remittances are the income channel through which labour migration reaches origin economies.",
    ["worldbank/remittances_received"],
    [(C, 'r = load("worldbank/remittances_received")\nr = r[r.ref_area.str.len() == 3]\nlast = r.dropna(subset=["value"]).sort_values("period").groupby("ref_area").tail(1)\ntop = last.nlargest(15, "value").set_index("area_name")\n(top["value"] / 1e9).round(1).to_frame("US$ bn")'),
     (C, 'p = pivot(select(r, ref_area=["IND", "MEX", "PHL", "CHN", "EGY", "PAK", "BGD", "NGA"]))\nplot_lines(p.loc["1990":] / 1e9, "Remittances received", "US$ bn", "World Bank (BX.TRF.PWKR.CD.DT)", names={});')]),

"migration/03_eu_employment_by_citizenship.ipynb": nb(
    "Europe: employment rates by citizenship",
    "Employment rates of nationals, EU citizens and non-EU citizens (age 20–64): the labour-market integration gap.",
    ["eurostat/lfsa_ergan"],
    [(C, 'g = load("eurostat/lfsa_ergan")\nprint({c: g[c].drop_duplicates().head(12).tolist() for c in ("citizen", "age", "sex", "unit") if c in g.columns})'),
     (C, 'x = select(g, sex="T", age="Y20-64", citizen=["NAT", "EU27_2020_FOR", "NEU27_2020_FOR"])\nareas = ["EU27_2020", "DE", "FR", "ES", "IT", "SE", "NL"]\nlast = x[x.ref_area.isin(areas)].sort_values("period").groupby(["ref_area", "citizen"]).tail(1)\nlast.pivot_table(index="ref_area", columns="citizen", values="value").assign(gap_non_eu=lambda d: d["NEU27_2020_FOR"] - d["NAT"])')]),

"migration/04_oecd_migration_inflows.ipynb": nb(
    "OECD: inflows of foreign population",
    "Annual inflows of foreign nationals into OECD countries (International Migration Database).",
    ["oecd/migration_flows"],
    [(C, 'f = load("oecd/migration_flows")\nprint({c: f[c].drop_duplicates().head(12).tolist() for c in f.columns if c not in ("value", "period", "ref_area", "source", "dataset")})'),
     (C, '# Select total inflows of foreign population (measure code from the listing above)\nf.groupby(["ref_area", "period"])["value"].sum().unstack().iloc[:, -6:].sort_values(f.period.max(), ascending=False).head(20)')]),

"migration/05_migrant_workers_ilo.ipynb": nb(
    "Migrant workers (ILO labour migration statistics)",
    "Employment of migrant workers by citizenship from ILOSTAT's labour migration series.",
    ["ilostat/migrant_workers_by_citizenship"],
    [(C, 'w = load("ilostat/migrant_workers_by_citizenship")\nprint(w.columns.tolist()); print(w.classif1.drop_duplicates().tolist()[:20])'),
     (C, 'latest(select(w, sex="SEX_T"), by=["ref_area", "classif1"]).head(40)')]),

# ------------------------------------------------------------------ adjustment
"adjustment/01_global_sectoral_reallocation.ipynb": nb(
    "Sectoral reallocation: agriculture, industry, services",
    "Employment shares by broad sector since 1991 (ILO modelled estimates), and the long-run US series from 1900 for historical context.",
    ["worldbank/emp_agriculture_share", "worldbank/emp_industry_share", "worldbank/emp_services_share"],
    [(C, 'sec = {"Agriculture": "worldbank/emp_agriculture_share", "Industry": "worldbank/emp_industry_share", "Services": "worldbank/emp_services_share"}\nframes = {k: pivot(select(load(v), ref_area=FOCUS)) for k, v in sec.items()}\nfig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=True)\nfor ax, (k, p) in zip(axes, frames.items()):\n    plot_lines(p[["WLD", "IND", "CHN", "IDN", "USA", "AUS"]], f"{k}, % of employment", "%", "ILO modelled via World Bank", ax=ax)'),
     (C, 'chg = pd.DataFrame({k: p.iloc[-1] - p.iloc[0] for k, p in frames.items()})\nchg.rename(index=FOCUS_NAMES).round(1)'),
     (M, "## United States, 1900 to today (curated)"),
     (C, 'h = curated("adjustment", "long_run_sectoral_employment")\nh[h.region.isin(["US", "United States"])][["series", "period", "value", "unit", "source"]]')],
    ["adjustment/long_run_sectoral_employment"]),

"adjustment/02_us_sector_employment_since_1990.ipynb": nb(
    "United States: sector employment since 1990",
    "Levels and net change of payroll employment in health care, construction, manufacturing and information.",
    ["bls/headline_monthly"],
    [(C, 'h = load("bls/headline_monthly")\nsec = ["CES6562000001", "CES2000000001", "CES3000000001", "CES5000000001"]\ns = pivot(select(h, indicator=sec), columns="indicator_label")\nplot_lines(s / 1000, "Payroll employment", "millions", "BLS CES", names={});'),
     (C, 'jan95 = s.loc["1995-01"]\nlast = s.iloc[-1]\npd.DataFrame({"Jan 1995": jan95, s.index[-1]: last, "net change": last - jan95, "% change": (last / jan95 - 1) * 100}).round(1)')]),

"adjustment/03_us_labour_flows.ipynb": nb(
    "United States: hires, quits and layoffs",
    "Gross labour flows from JOLTS. Annual hires of about 60 million set the scale against which any displacement estimate should be read; the quits rate tracks workers' confidence in moving between jobs.",
    ["bls/jolts"],
    [(C, 'j = load("bls/jolts")\nf = pivot(select(j, indicator=["JTS000000000000000HIL", "JTS000000000000000QUL", "JTS000000000000000LDL"]), columns="indicator_label")\nplot_lines(f / 1000, "Monthly hires, quits and layoffs", "millions", "BLS JOLTS", names={});'),
     (C, 'annual = to_annual(select(j, indicator=["JTS000000000000000HIL", "JTS000000000000000QUL", "JTS000000000000000LDL"]))\nannual["value"] = annual["value"] * 12 / 1000\nannual.pivot_table(index="period", columns="indicator_label", values="value").tail(10).round(1)')]),

"adjustment/04_employment_by_occupation_global.ipynb": nb(
    "Employment by occupation (ISCO major groups)",
    "How the occupational mix differs across economies: professionals, technicians and clerical workers (the information-intensive groups) against craft, plant and elementary occupations.",
    ["ilostat/employment_by_occupation_modelled"],
    [(C, 'o = select(load("ilostat/employment_by_occupation_modelled"), sex="SEX_T")\nprint(o.classif1.drop_duplicates().tolist())'),
     (C, 'skill = o[o.classif1.str.startswith("OCU_ISCO08_") & ~o.classif1.str.endswith("TOTAL")]\nlast = skill[skill.period == skill.period.max()]\nshares = last.pivot_table(index="ref_area", columns="classif1", values="value")\nshares = shares.div(shares.sum(axis=1), axis=0) * 100\nshares.loc[[a for a in FOCUS if a in shares.index]].round(1)')]),

# ------------------------------------------------------------------ macro
"macro/01_us_labour_share_productivity.ipynb": nb(
    "United States: labour share and productivity",
    "Nonfarm business labour share and productivity growth, with the curated 1990–2026 series used in the research.",
    ["bls/productivity_labour_share"],
    [(C, 'p = pivot(select(load("bls/productivity_labour_share"), indicator="PRS85006173"), columns="indicator_label")\nplot_lines(p, "Labour share, nonfarm business (2017 = 100)", "index", "BLS Productivity and Costs (PRS85006173)", names={});'),
     (C, 'q = pivot(select(load("bls/productivity_labour_share"), indicator="PRS85006092"), columns="indicator_label")\nto_annual(q.stack().rename("value").reset_index().rename(columns={"level_1": "indicator"})).pivot_table(index="period", values="value").tail(15)'),
     (C, 'curated("macro", "labour_share_wealth_concentration").query("series.str.contains(\'share of GDI\')", engine="python").tail(12)')],
    ["macro/labour_share_wealth_concentration"]),

"macro/02_wealth_profits_concentration.ipynb": nb(
    "United States: wealth concentration and corporate profits",
    "Distributional Financial Accounts (top 1% and bottom 50% shares of net worth) and after-tax corporate profits relative to GDP.",
    ["fred/distribution_and_profits"],
    [(C, 'd = load("fred/distribution_and_profits")\nw = pivot(select(d, indicator=["WFRBST01134", "WFRBSB50215"]), columns="indicator").rename(columns={"WFRBST01134": "Top 1%", "WFRBSB50215": "Bottom 50%"})\nplot_lines(w, "Share of US household net worth", "%", "Federal Reserve DFA via FRED", names={});'),
     (C, 'g = pivot(select(d, indicator=["CP", "GDP"]), columns="indicator")\nprof = (g["CP"] / g["GDP"] * 100).dropna().to_frame("after-tax profits, % of GDP")\nplot_lines(prof, "Corporate profits after tax, % of GDP", "%", "BEA via FRED (CP, GDP)", names={});')]),

"macro/03_okun_phillips.ipynb": nb(
    "United States: Okun's law and the wage Phillips curve",
    "Quarterly change in unemployment against real GDP growth (Okun), and nominal wage growth against unemployment (Phillips).",
    ["bls/headline_monthly", "fred/distribution_and_profits", "fred/labour_market_extras"],
    [(C, 'import numpy as np\nur = to_annual(select(load("bls/headline_monthly"), indicator="LNS14000000"))\ngdp = select(load("fred/distribution_and_profits"), indicator="GDP").copy()\ngdp["period"] = gdp["period"].astype(str).str[:4]\ng = gdp.groupby("period")["value"].mean().pct_change() * 100\nu = ur.set_index("period")["value"].diff()\nok = pd.concat({"gdp_growth_nominal": g, "d_unemployment": u}, axis=1).dropna()\nb = np.polyfit(ok.gdp_growth_nominal, ok.d_unemployment, 1)\nprint(f"Okun slope (nominal GDP, annual): {b[0]:.2f}  — replace GDP with real GDP (GDPC1) for the textbook coefficient")\nok.tail()'),
     (C, 'wage = select(load("fred/labour_market_extras"), indicator="LES1252881600Q").copy()\nwage["period"] = wage["period"].astype(str).str[:4]\nwg = wage.groupby("period")["value"].mean().pct_change() * 100\nph = pd.concat({"real_median_weekly_earnings_growth": wg, "unemployment": ur.set_index("period")["value"]}, axis=1).dropna()\nax = ph.plot.scatter(x="unemployment", y="real_median_weekly_earnings_growth", figsize=(7, 5))\nax.set_title("Real earnings growth vs unemployment", loc="left");')]),

"macro/04_output_per_worker_global.ipynb": nb(
    "Output per worker",
    "Labour productivity levels (GDP per worker, PPP) and growth since 2000 across economies.",
    ["ilostat/output_per_worker"],
    [(C, 'o = select(load("ilostat/output_per_worker"), ref_area=FOCUS)\np = pivot(o)\nplot_bars(p.iloc[-1] / 1000, f"Output per worker, {p.index[-1]}", "thousand 2021 PPP $", "ILO modelled estimates");'),
     (C, 'growth = ((p.iloc[-1] / p.loc[p.index.astype(str) == "2000"].iloc[0]) ** (1 / (int(str(p.index[-1])) - 2000)) - 1) * 100\ngrowth.sort_values().rename(index=FOCUS_NAMES).to_frame("annual growth since 2000, %").round(2)')]),

"macro/05_talent_capital_allocation.ipynb": nb(
    "Talent and capital allocation",
    "Curated evidence on where venture capital, R&D and elite graduates have gone since 1995, set against productivity in construction and research productivity.",
    [],
    [(C, 'a = curated("macro", "talent_capital_allocation")\na["value"] = pd.to_numeric(a["value"], errors="coerce")\nvc = a[a.series.str.startswith("VC deal value")]\nvc.pivot_table(index="period", columns="series", values="value")'),
     (C, 'a[a.series.str.contains("MIT|Construction|Research productivity")][["series", "period", "value", "unit", "source"]]')],
    ["macro/talent_capital_allocation"]),

# ------------------------------------------------------------------ micro
"micro/01_ai_exposure_by_occupation.ipynb": nb(
    "Generative-AI task exposure by occupation group",
    "Employment-weighted LLM task exposure (Eloundou, Manning, Mishkin & Rock 2024) for internet-era digital occupations, pre-1995 physical-economy occupations, and pre-1995 office and professional occupations, using OEWS May 2025 employment. Method and sensitivity: `analysis/ai_exposure/METHOD.md`.",
    [],
    [(C, 'from labobs import REPO_ROOT\nA = REPO_ROOT / "analysis" / "ai_exposure" / "outputs"\ng = pd.read_csv(A / "G_exposure_by_group.csv")\ng'),
     (C, 'col = [c for c in g.columns if "human_beta" in c and "mean" in c] or [c for c in g.columns if "human_beta" in c]\nax = g.set_index(g.columns[0])[col[0]].plot.barh(figsize=(8, 3), color="#1a73e8")\nax.set_title("Mean share of tasks exposed (human β), employment-weighted", loc="left");'),
     (C, 'mg = pd.read_csv(A / "G_exposure_by_major_group.csv")\nmg.sort_values(mg.columns[-1], ascending=False).head(25)'),
     (C, 'pd.read_csv(A / "G_sensitivity.csv")'),
     (M, "To refresh after a new OEWS release: update `analysis/ai_exposure/inputs/` and run `python analysis/ai_exposure/exposure.py`.")]),

"micro/02_occupations_physical_vs_digital.ipynb": nb(
    "Occupations: wages and projected growth, physical economy vs digital",
    "BLS OEWS May 2025 wages and Employment Projections 2025–35 for physical-economy white-collar occupations, blue-collar comparators and AI-exposed digital occupations.",
    [],
    [(C, 'o = curated("micro", "bls_occupations_physical_vs_digital_2025")\no = o[o.group != "total"]\nfor c in ("median_wage", "proj_change_pct", "annual_openings", "employment"):\n    o[c] = pd.to_numeric(o[c], errors="coerce")\nfig, ax = plt.subplots(figsize=(10, 7))\ncol = {"physical": "#1e8e3e", "digital": "#d93025", "bluecollar": "#f9ab00"}\nfor gname, d in o.groupby("group"):\n    ax.scatter(d.proj_change_pct, d.median_wage / 1000, s=(d.annual_openings.fillna(2000) / 400), alpha=0.6, label=gname, color=col.get(gname))\nfor _, r in o.iterrows():\n    ax.annotate(r.title[:28], (r.proj_change_pct, r.median_wage / 1000), fontsize=6)\nax.axvline(3.5, color="#999", ls="--", lw=0.8); ax.axhline(50.98, color="#999", ls="--", lw=0.8)\nax.set_xlabel("Projected employment change 2025–35, %"); ax.set_ylabel("Median annual wage, $000")\nax.set_title("Wage vs projected growth (bubble = annual openings)", loc="left", fontweight="bold"); ax.legend(frameon=False);'),
     (C, 'o.groupby("group")[["employment", "annual_openings"]].sum()')],
    ["micro/bls_occupations_physical_vs_digital_2025"]),

"micro/03_oews_full_distribution.ipynb": nb(
    "OEWS: the full occupational wage distribution",
    "Parses the latest national OEWS release (all ~830 detailed occupations) from the raw vintage: employment, median and percentile wages.",
    ["bls/oews_national"],
    [(C, 'import zipfile\nz = zipfile.ZipFile(raw_payload("bls/oews_national"))\nprint(z.namelist())'),
     (C, 'name = next(n for n in z.namelist() if n.lower().endswith((".xlsx", ".xls")))\noews = pd.read_excel(z.open(name))\noews.columns = [c.lower() for c in oews.columns]\ndet = oews[oews.o_group == "detailed"].copy()\nfor c in ("tot_emp", "a_median", "a_pct90"):\n    det[c] = pd.to_numeric(det[c], errors="coerce")\ndet[["occ_code", "occ_title", "tot_emp", "a_median", "a_pct90"]].sort_values("tot_emp", ascending=False).head(25)')]),

"micro/04_onet_tasks.ipynb": nb(
    "O*NET: task and work-context content",
    "Explores the O*NET database release: task statements per occupation and work-context measures of physical presence (e.g. 'Physical Proximity', 'Spend Time Using Your Hands'), which proxy the physical-accountability boundary of automation.",
    ["research/onet_database"],
    [(C, 'import zipfile\nz = zipfile.ZipFile(raw_payload("research/onet_database"))\n[n for n in z.namelist() if n.endswith(".txt")][:40]'),
     (C, 'wc = pd.read_csv(z.open(next(n for n in z.namelist() if n.endswith("Work Context.txt"))), sep="\\t")\nphys = wc[wc["Element Name"].isin(["Physical Proximity", "Spend Time Using Your Hands to Handle, Control, or Feel Objects, Tools, or Controls", "Face-to-Face Discussions"]) & (wc["Scale ID"] == "CX")]\nphys.pivot_table(index="O*NET-SOC Code", columns="Element Name", values="Data Value").describe()')]),

# ------------------------------------------------------------------ demography
"demography/01_fertility_and_ageing.ipynb": nb(
    "Fertility and ageing",
    "Total fertility rates against the 2.1 replacement level, and old-age dependency ratios: the labour-supply backdrop for every other notebook.",
    ["worldbank/fertility_rate", "worldbank/age_dependency_old"],
    [(C, 'f = pivot(select(load("worldbank/fertility_rate"), ref_area=FOCUS))\nax = plot_lines(f.loc["1970":], "Total fertility rate", "births per woman", "UN WPP via World Bank (SP.DYN.TFRT.IN)")\nax.axhline(2.1, color="k", ls="--", lw=0.8);'),
     (C, 'd = pivot(select(load("worldbank/age_dependency_old"), ref_area=FOCUS))\nplot_bars(d.iloc[-1], f"Old-age dependency ratio, {d.index[-1]}", "65+ per 100 aged 15–64", "World Bank (SP.POP.DPND.OL)");'),
     (C, 'curated("demography", "fertility_ageing_urbanisation")[["region", "series", "value", "unit", "period", "source"]]')],
    ["demography/fertility_ageing_urbanisation"]),

"demography/02_urbanisation.ipynb": nb(
    "Urbanisation",
    "Urban share of population over time; read with the housing notebooks, since labour demand and housing cost concentrate in the same metropolitan areas.",
    ["worldbank/urban_population_share"],
    [(C, 'u = pivot(select(load("worldbank/urban_population_share"), ref_area=FOCUS))\nplot_lines(u.loc["1960":], "Urban population, % of total", "%", "World Bank (SP.URB.TOTL.IN.ZS)");')]),

"demography/03_population_projections.ipynb": nb(
    "World Population Prospects 2024: projections",
    "Medium-variant projections of population, fertility and working-age population to 2100 from the UN DESA release file.",
    ["undesa/wpp_2024_indicators"],
    [(C, 'w = pd.read_csv(raw_payload("undesa/wpp_2024_indicators"), low_memory=False)\nprint(w.columns.tolist()[:40])'),
     (C, 'iso = ["WLD"] if "ISO3_code" not in w.columns else None\nsel = w[w["ISO3_code"].isin(["AUS", "USA", "JPN", "KOR", "CHN", "IND", "IDN", "DEU", "ITA"])] if "ISO3_code" in w.columns else w\np = sel.pivot_table(index="Time", columns="ISO3_code", values="TPopulation1July")\nplot_lines(p / 1000, "Population (medium variant)", "millions", "UN DESA WPP 2024", names={});')]),

# ------------------------------------------------------------------ housing
"housing/01_house_price_to_income.ipynb": nb(
    "House prices relative to income",
    "OECD price-to-income ratios (index) and the curated Demographia median multiples for major cities.",
    ["oecd/house_prices"],
    [(C, 'h = load("oecd/house_prices")\nprint({c: h[c].drop_duplicates().head(12).tolist() for c in h.columns if c not in ("value", "period", "ref_area", "source", "dataset")})'),
     (C, 'm = [c for c in h.columns if c in ("measure", "indicator")]\nsel = {m[0]: "HPI_YDH"} if m and "HPI_YDH" in set(h[m[0]]) else {}\nx = select(h, ref_area=[a for a in FOCUS if a in set(h.ref_area)], **sel)\nplot_lines(pivot(to_annual(x)), "House price-to-income ratio (index)", "index", "OECD Analytical house price indicators");'),
     (M, "## Median multiples by city (curated, Demographia 2026)"),
     (C, 'c = curated("housing", "housing_affordability_policy")\nc[c.series.str.contains("median multiple", case=False)][["region", "value", "period", "source"]].sort_values("value", ascending=False)')],
    ["housing/housing_affordability_policy"]),

"housing/02_australia_housing_and_policy.ipynb": nb(
    "Australia: housing affordability and policy",
    "Price-to-income ratios, deposit-saving time, home ownership by age, and the 2025–26 policy record (Housing Accord progress; the 2026 negative gearing and CGT legislation).",
    [],
    [(C, 'c = curated("housing", "housing_affordability_policy")\nc[c.region.astype(str).str.contains("Australia|Sydney|Melbourne", case=False)][["region", "series", "value", "unit", "period", "source"]]')],
    ["housing/housing_affordability_policy"]),
}


def main():
    for rel, content in SPECS.items():
        p = HERE / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(content, indent=1) + "\n")
    print(f"wrote {len(SPECS)} notebooks")


if __name__ == "__main__":
    main()
