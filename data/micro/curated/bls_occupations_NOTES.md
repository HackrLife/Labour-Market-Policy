# B: BLS occupation and JOLTS data — notes

Collected 24 Oct 2026 from bls.gov pages. Each value below was read from the BLS page cited.

## Vintages (all newer than the brief assumed)
- **OEWS: May 2025** (released 2026; "Occupational Employment and Wages -- May 2025"). This is not May 2024. The `/oes/current/` profile pages now point to May 2025.
- **Employment Projections: 2025–35** (released 27 Aug 2026). The 2024–34 set has been replaced. OOH pages also use 2025 base data and 2025–35 projections.
- **JOLTS: August 2026, preliminary** (released 29 Sep 2026). This is the latest month available.

## Sources and column definitions (B_bls_occupations.csv)
- `employment`: OEWS May 2025 national wage-and-salary employment, from News Release Table 1 (https://www.bls.gov/news.release/ocwage.t01.htm). It excludes the self-employed. The CSV keeps this URL in `oews_source_url`.
- `mean_wage`: OEWS May 2025 annual mean wage, from the same Table 1.
- `median_wage`: median annual wage for May 2025, from OEWS, as printed in EP Table 1.2 or the occupation's OOH page. OEWS Table 1 gives only the median *hourly* wage. The hourly figures in Table 1 match the OOH figures (for example, RN $46.90/hr and $97,550/yr).
- `p90_wage`: the OOH Pay section sentence "the highest 10 percent earned more than $X" (May 2025 OEWS). Blank where OOH gives only a combined group or an hourly figure (see the gaps below).
- `proj_change_pct`: EP 2025–35. Where `proj_pct_precision` = `1dp`, the value is from EP Table 1.2 or Table 1.5 to one decimal place. Where it is `int`, the value is the OOH rounded integer, because Table 1.2 for that occupation could not be read: web retrieval truncated that part of the 178k-character page.
- `annual_openings`: EP 2025–35 annual average occupational openings, converted to persons. The source is Table 1.2 (thousands, one decimal place) or the OOH sentence "About N openings … each year".
- `ep_employment_2025_thous` / `ep_employment_2035_thous`: the EP National Employment Matrix totals, in thousands. These include the self-employed, so they are higher than OEWS employment. Example: construction managers are 609.1k in EP and 380,360 in OEWS, because many are self-employed.
- `source_url`: the OOH page or EP table used for the projections, median and p90 values.

### All-occupations benchmarks
- OEWS May 2025: employment 155,495,730; **mean annual wage $69,770**; median hourly wage $24.51. The **median annual wage is $50,980**, from EP Tables 1.2 and 1.5, which use OEWS May 2025 wages.
- EP 2025–35 total employment: 170,280.8k in 2025 to 176,198.5k in 2035. That is +5,917.6k, or **+3.5%**. Annual average openings are 17,461.8k. The release says this is "slower than the 10.9 percent growth recorded over the 2015-25 decade" (https://www.bls.gov/news.release/ecopro.nr0.htm).

## Classification caveats
- **Special education teachers**: BLS uses **SOC 25-2052** (kindergarten and elementary), not 25-2056. The CSV uses 25-2052. The group 25-2050 is 584,100 jobs in 2025, 583,800 in 2035 and 0%, with about 37,100 openings a year for all special education teachers.
- **Clinical lab**: 29-2010 is the combined group. OEWS employment of 332,940 and EP employment of 343.0k are for the group.
- **Occupational health and safety specialists (19-5011)**: the OEWS row is specialists only (140,610; mean $93,860). OOH median is $90,150. The OOH openings figure of 20,900 covers specialists *and* technicians, so the CSV leaves it blank.
- **Customer service reps, bookkeeping clerks, data entry keyers and medical transcriptionists** are grouped as "digital" following the brief. Their wages are below the all-occupations median, so they are routine-information jobs, not well-paid digital ones. Consider labelling them "routine information" in the paper.

## Gaps (not verifiable at compilation (24 October 2026))
- **Power plant operators (51-8013)**: the OEWS Table 1 row could not be read because the page was truncated, so OEWS employment and mean wage are blank. The OOH page gives a median of $102,040, EP employment of 29.8k → 28.3k (−5%), and p90 and openings only for the combined group of operators, distributors and dispatchers ($136,550 and about 3,400 openings a year).
- **Nurse practitioners**: OOH gives p90 ($224,490) and openings (32,200) only for the combined nurse anesthetists, midwives and NPs group, so the CSV leaves both blank. EP 2025–35: 336.3k → 474.1k (+41.0%), the fastest-growing detailed occupation.
- **Compliance officers (13-1041)**: the p90 value was not fetched. The OOH page was not opened.
- **Data entry keyers**: the OOH page was blocked, so p90 and openings are blank. The EP values come from Table 1.5.
- **Customer service reps**: OOH gives p10 and p90 only as hourly figures (highest 10% above $30.57/hr), so `p90_wage` is blank.
- **Special education K–elementary and K–12 education administrators**: OEWS Table 1 suppresses hourly wages for these, which is normal for teachers. Annual means are given. The education administrators p90 ($167,770) comes from the principals OOH page.
- The **JOLTS 2025 annual average** was not obtained. The BLS series tool (pdq SurveyOutputServlet) is blocked by robots.txt, and the api.bls.gov endpoint is not allowed. B_jolts.csv instead carries Aug 2025 and May–Aug 2026 (seasonally adjusted) from the JOLTS news release PDF. Aug 2025 serves as a year-earlier comparison.
- JOLTS has **no separate "educational services" total** in Table 1. It reports *private* educational services and *state and local government education* separately, and the CSV includes both.

## Fastest-declining occupations (EP Table 1.5, 2025–35)
The top five are word processors and typists (−34.4%), telephone operators (−27.6%), switchboard operators (−26.0%), **data entry keyers (−25.5%)** and foundry mold and coremakers (−23.0%). **Table 1.5 itself does not name AI**, and it has no notes about AI.

The 2025–35 projections release does attribute declines to AI:
- "the continued integration of automation tools, including those powered by AI, into workflows ... is likely to reduce demand for several office and administrative support occupations." Office and administrative support is the fastest-declining major group at −4.0%, or −752,100 jobs.
- "incorporation of AI tools into the sales process" is cited for sales and related occupations (−1.4%).
- "The use of generative AI software ... may limit demand for some jobs in the arts, design, entertainment, sports, and media occupational group."
- AI power demand and data centres are named as the driver of utilities growth: "Nearly all the job growth is expected from electric power generation, transmission, and distribution ... including artificial intelligence (AI) power demands."
- BLS is introducing a new data product comparing occupations on "theoretical and observed exposure to artificial intelligence (AI)." This would be worth fetching in a follow-up.

### OOH statements that cite AI (2025–35 Job Outlook sections)
- Computer programmers (−7.3%): "many companies are expected to leverage technologies, including artificial intelligence (AI)" to automate programming tasks.
- Writers and authors (0%): "Increasing use of artificial intelligence (AI) for writing is projected to dampen demand for these workers."
- Technical writers (+1%): growth "may be slowed by artificial intelligence (AI) tools".
- Graphic designers (−2%): "Automated design tools, such as artificial intelligence (AI), are projected to ... reduce the need for these workers."
- Paralegals (0%): demand "limited by advances in technology, including artificial intelligence (AI)."
- Public relations specialists (+2%): "AI is increasingly making inroads into data-rich social media, which may soften demand".
- Editors, market research analysts and advertising sales agents: these pages do not mention AI. Advertising sales cites automated ad placement.
- Customer service reps and bookkeeping clerks: these pages cite automation, not AI by name.
- Medical transcriptionists: the page cites speech recognition and NLP, not AI by name.

## JOLTS (B_jolts.csv)
Source: https://www.bls.gov/news.release/pdf/jolts.pdf (Table 1, seasonally adjusted; levels in thousands, rates in percent). The latest month is August 2026 (preliminary): total nonfarm openings 7,079k at a 4.3% rate. Rates for August 2026: health care and social assistance 5.4%, professional and business services 5.0%, manufacturing 4.0%, information 4.3% (up from 2.5–3.1% in May–July 2026), construction 2.9%. The release says: "Job openings changed little in all industries."

## CompTIA "State of the Tech Workforce"
**Not collected.** The comptia.org report pages could not be retrieved. No CompTIA figures are reported, and none should be cited from this file until the report is obtained.
