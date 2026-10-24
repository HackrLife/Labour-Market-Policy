# H. Concentration, market power and the one-sided economy: evidence file

Compiled 24 October 2026. Every figure below was retrieved during this session from the URL given; nothing is taken from memory. FRED CSV download endpoints were blocked by the session proxy, so FRED values were read from the FRED "Table Data" pages (fred.stlouisfed.org/data/<ID>) or series pages. Chartable values are in `/home/claude/research/H_series.csv` (352 rows), built by `/home/claude/research/scripts/build_H_series.py`.

## 0. Claim under test and verdict

**Claim.** The pre-1995 physical economy is structurally largely unchanged in what it employs and does, while value, profits, market power and wealth have concentrated in a small digital/financial core and the labour share has fallen.

**Verdict.** The distributional half of the claim is well supported by the official series. The US labour share is at or near its lowest level in the 1990–2026 record, corporate profits are at a post-1947 high as a share of GDP, the top 1% wealth share is at a series high, and equity value is more concentrated in ten firms than at any point since the 1960s. The structural half is supported for employment: construction, health care and manufacturing still account for a large share of jobs, and health care employment has roughly doubled since 1995, whereas the information sector employs fewer people in September 2026 than in January 1995. Three qualifications are needed. (i) The mechanism is contested. Several measurement studies attribute most of the labour-share decline to the capitalisation of intellectual property, to housing, or to heavy reallocation toward productive firms, and the markup evidence is under active challenge (Benkard, Miller and Yurukoglu 2025). (ii) "Digital/financial core" is a combination of two distinct phenomena. Rising concentration in Autor et al. (2020) is economy-wide, including retail and wholesale; it is not confined to technology. (iii) "Structurally unchanged" overstates the case. Manufacturing employment has fallen by about 4.6 million since 1995, and physical-sector productivity has diverged sharply, from strong gains in retail and computer manufacturing to stagnation in construction.

---

## 1. Autor, Dorn, Katz, Patterson and Van Reenen (2020)

**Citation.** Autor, David, David Dorn, Lawrence F. Katz, Christina Patterson, and John Van Reenen. 2020. "The Fall of the Labor Share and the Rise of Superstar Firms." *Quarterly Journal of Economics* 135(2): 645–709. DOI: 10.1093/qje/qjaa004. Sources: https://eprints.lse.ac.uk/104480 ; https://lkatz.scholars.harvard.edu/publications/fall-labor-share-and-rise-superstar-firms ; author PDF https://shapingwork.mit.edu/wp-content/uploads/2023/10/THE-FALL-OF-THE-LABOR-SHARE-AND-THE-RISE-OF-SUPERSTAR-FIRMSast.pdf ; NBER WP 23396.

**Data and argument.** The paper uses the US Economic Census from 1982. Its hypothesis is that globalisation or technology shifts sales toward the most productive firms in each industry. These "superstar" firms have high markups and low labour shares, so the reallocation lowers the aggregate labour share. The authors test seven predictions and report support for all seven.

**Key numbers (author PDF).**
- The share of US employment in firms with more than 5,000 employees rose from 28% (1987) to 34% (2016) (Section I).
- Sales concentration (CR4, CR20) rose in all six sectors from 1982 to 2012, and rose faster for sales than for employment ("scale without mass").
- Manufacturing payroll/value added fell 16.07 points from 1982 to 2012 (Table IV, Panel A). Reallocation among surviving firms accounts for −13.15 points and the unweighted within-firm change for −2.93. For compensation/value added the total is −18.48, with reallocation −18.67 and within-survivor −0.24.
- The survivor reallocation term is negative in every sector for payroll/sales: retail −5.44, wholesale −4.59, services −0.76, utilities/transport −3.25 (1992–2012), finance −0.75 (1992–2012).
- Concentration–labour share regressions in manufacturing (five-year changes, payroll/value added): CR4 −0.148, CR20 −0.228, both significant at 5%. The relationship is stronger in high-tech industries (interaction −0.067, SE 0.031).

**Relevance.** The paper supports the claim that value has concentrated in a small set of firms that employ relatively few workers per unit of sales. It does not support a purely digital reading. The decline appears in retail, wholesale, utilities and transport, and the authors' interpretation is that superstar firms are *more productive*, which is the efficiency reading listed under Contradicting evidence.

## 2. De Loecker, Eeckhout and Unger (2020)

**Citation.** De Loecker, Jan, Jan Eeckhout, and Gabriel Unger. 2020. "The Rise of Market Power and the Macroeconomic Implications." *Quarterly Journal of Economics* 135(2): 561–644. DOI: 10.1093/qje/qjz041. Sources: https://www.nber.org/papers/23687 (NBER WP 23687, August 2017, DOI 10.3386/w23687) ; https://academicnewsletter.sufe.edu.cn/info/344950.

**Key numbers.**
- The aggregate (sales-weighted) markup rose from 21% above marginal cost in 1980 (1.21) to 61% (1.61) in 2016. The rise comes from the upper tail of the distribution, and the median markup is roughly unchanged. Endpoint years 1980/2016 are from the secondary summary at https://www.progress.org/wiki/de-loecker-eeckhout-unger-markups/; the abstract gives "from 21% … to 61%".
- The average profit rate rose from about 1% to about 8% of sales.
- The 2017 working paper reported 18% to 67% (through 2014). Cite the published figures, not the WP figures.
- Data: Compustat publicly listed firms, 1955–2016. Production-function approach with cost of goods sold as the variable input.

**Relevance.** This is the main source for rising market power, and it links that rise to the falling labour share. For the challenges, see Section 11.

## 3. Philippon (2019); Gutiérrez and Philippon

**Philippon, Thomas. 2019.** *The Great Reversal: How America Gave Up on Free Markets.* Cambridge, MA: Belknap Press of Harvard University Press. xii + 343 pp. ISBN 9780674237544 (from the Cambridge *Business History Review* listing). Argument (NYU Stern summary, https://www.stern.nyu.edu/experience-stern/faculty-research/great-reversal-how-america-gave-free-markets.md): US industries are more concentrated than twenty years earlier, incumbents lobby to protect rents, and the result is higher prices, lower investment, productivity and wages, and greater inequality, while Europe has become more competitive. The single figure confirmed second-hand is that US broadband prices are about twice European levels, whereas they were lower in 1999 (Barron's excerpt via Stern news; https://potsandpansbyccg.com/2020/02/28/why-are-us-broadband-prices-so-high/ gives about $70 in the US versus $31–35 in France, Germany, Japan, South Korea and the UK). The book's household-cost estimates were not verified.

**Gutiérrez, Germán, and Thomas Philippon. 2017.** "Investmentless Growth: An Empirical Investigation." *Brookings Papers on Economic Activity* 48(2, Fall): 89–190. RePEc: https://ideas.repec.org/p/cpr/ceprdp/11673.html ; PDF https://www.brookings.edu/wp-content/uploads/2017/09/2_gutierrezphilippon.pdf. Findings: US private investment has been weak relative to profitability and Tobin's Q since the early 2000s. There is little support for explanations based on financial constraints, risk premia or safe-asset scarcity, limited support for intangibles and globalisation, and fairly strong support for declining competition and for short-termism/governance. The investment gap is concentrated in firms owned by quasi-indexers in less competitive industries, and these firms spend a large share of free cash flow on buybacks.

**Gutiérrez, Germán, and Thomas Philippon. 2017.** "Declining Competition and Investment in the U.S." NBER WP 23583. DOI: 10.3386/w23583. https://www.nber.org/papers/w23583. US business has under-invested relative to Q since the early 2000s, partly because of declining competition. Leaders in manufacturing raised investment after exogenous increases in Chinese competition. Excess entry in the late 1990s predicts higher investment relative to Q.

**Relevance.** These papers support "profits without commensurate investment," a pattern consistent with rents. Note that Section 9 now shows the opposite pattern among the hyperscalers in 2025–26: very large capital spending. Gutiérrez–Philippon's underinvestment finding describes the 2000–2017 period and should not be extended to 2026 without qualification.

## 4. US labour share

**BLS nonfarm business labour share, all workers (FRED PRS85006173).** Index 2017=100, quarterly, last updated 2026-09-03. https://fred.stlouisfed.org/data/PRS85006173

| Period | Index |
|---|---|
| 1990Q1 | 110.182 |
| 1995Q1 / 1995 average | 107.167 / 107.24 |
| 2000Q1 / 2001Q1 (local peak) | 112.828 / 113.626 |
| 2019Q4 | 99.588 |
| 2020Q2 (pandemic composition spike) | 104.195 |
| 2025Q4 | 95.727 |
| 2026Q1 | 94.843 |
| **2026Q2 (latest)** | **93.446** |

The index for 2026Q2 is 12.8% below 1995Q1 and 6.2% below 2019Q4. It is the lowest value from 1990 onward (only post-1990 values were retrieved). The decline is not monotonic. The share rose between 1997 and 2001, and the 2020 spike reflects job losses concentrated among low-wage workers.

**BEA, compensation of employees as a share of GDI (FRED A4002E1A156NBEA),** annual, percent. https://fred.stlouisfed.org/data/A4002E1A156NBEA
1970 58.4 · 1980 57.7 · 1990 57.0 · **1995 55.7** · 2000 56.6 · 2005 54.0 · 2010 53.0 · 2015 52.8 · 2019 53.3 · 2020 54.6 · 2021 53.0 · 2022 51.7 · 2023 51.5 · 2024 51.4 · **2025 50.9**.

**BEA, wage and salary disbursements as a share of GDI (FRED W270RE1A156NBEA):** 1995 45.3, 2000 46.6, 2013 42.0, 2020 44.5, 2025 42.0 (full annual series in CSV). https://fred.stlouisfed.org/data/W270RE1A156NBEA

Both BEA measures are at their lowest values in the retrieved record in 2025.

## 5. US wealth concentration (Federal Reserve Distributional Financial Accounts)

**Top 1% share of household net worth (FRED WFRBST01134),** percent of aggregate, vintage of 18 September 2026. https://fred.stlouisfed.org/data/WFRBST01134
1989Q3 22.8 · 1990Q1 22.8 · 1990Q3 22.4 (series low) · 1995Q1 26.4 · 1995Q4 27.4 · 2000Q1 27.9 · 2010Q1 28.2 · 2019Q4 30.4 · 2020Q1 29.0 · 2024Q4 30.9 · 2025Q4 31.8 · 2026Q1 31.7 · **2026Q2 32.5 (series high)**.
Trading Tools (https://www.thetrading.tools/chart-of-the-day/2026-09-20-top-1-percent-wealth-share-record) reports the 0.8-point rise in 2026Q2 as the largest of 147 quarterly changes, coinciding with a 14.8% SPY gain in the quarter.

**Bottom 50% share of household net worth (FRED WFRBSB50215).** Table page blocked. Values from the FRED series page (https://fred.stlouisfed.org/series/WFRBSB50215): 2025Q2 2.4, 2025Q3 2.4, 2025Q4 2.4, 2026Q1 2.4, **2026Q2 2.3**. The FRED release table (https://fred.stlouisfed.org/release/tables?rid=453&eid=813804) confirms 2.3 for 2026Q2. Historical points from American Default Research, citing WFRBSB50215 (https://americandefault.org/indicators/the-bottom-half/): 1989Q3 3.5, series high 4.1 in 1992Q3, series low 0.4 in 2010Q4.

**Full distribution, 2026Q2 (FRED release table):** top 0.1% 15.0; 99–99.9th 17.5; top 1% 32.5; 90–99th 36.4; 50–90th 28.8; bottom 50% 2.3.
**Levels, 2026Q2 (millions USD):** top 1% 60,313,023; bottom 50% 4,278,038 (https://fred.stlouisfed.org/release/tables?rid=453&eid=813668). The top 1% holds about 14 times the net worth of the bottom 50%.
**Corporate equities and mutual fund shares, 2026Q2:** top 1% 50.9%, bottom 50% 0.6%. This explains why equity-led value concentration (Section 7) passes directly into wealth concentration.
**Bottom 50% share of total assets (WFRBSB50189):** 1990Q1 7.3, 1995Q1 8.3, 2026Q2 5.0. https://fred.stlouisfed.org/data/WFRBSB50189

Vintage caution: a 2020 summary of the DFA (UWSP, https://blog.uwsp.edu/cps/2020/07/13/the-economic-recovery-2010-19-what-changed-and-what-didnt-part-2-wealth-distribution/) gave top 1% shares of 23.3 (1990), 28.3 (1995) and 32.9 (2019), and bottom 50% shares of 3.9 (1990), 4.0 (1995) and 1.5 (2019). These differ from the current vintage (for example, 2019Q4 top 1% is now 30.4). The Fed restates the full history at each release. Cite the 2026 vintage only.

## 6. Corporate profits as a share of GDP

Computed from FRED table pages (billions USD, SAAR): CP (after tax, without IVA/CCAdj) https://fred.stlouisfed.org/data/CP ; A053RC1Q027SBEA (national income, before tax, without IVA/CCAdj) https://fred.stlouisfed.org/data/A053RC1Q027SBEA ; GDP https://fred.stlouisfed.org/data/gdp. Annual ratios use the sum of the four quarters.

| Period | After-tax CP / GDP | Pre-tax / GDP |
|---|---|---|
| 1995 | 6.56% | 9.11% |
| 2000Q1 | 5.65% | 8.08% |
| 2019Q4 | 9.67% | 11.11% |
| 2025 | 11.43% | 13.50% |
| 2026Q1 | 12.37% | 14.65% |
| **2026Q2** | **13.14%** | **15.70%** |

Inputs for 2026Q2: CP 4,279.937; pre-tax 5,111.956; GDP 32,563.030. The after-tax ratio has doubled since 1995. Payden & Rygel (28 Aug 2026, https://www.payden.com/insights/wir-2026-08-28-profits-boom) report pre-tax profits with IVA/CCAdj of $4.83 trillion in 2026Q2, up 22.8% year on year, equal to 14.9% of nominal GDP, "the highest share in data dating back to 1947." First Trust (https://www.ftportfolios.com/blogs/EconBlog/2026/8/26/real-gdp-growth-in-q2-was-unrevised-at-a-1.5percent-annual-rate) reports that domestic non-financial profits rose 10.4% in Q2, which it attributes to technology and energy, and notes that a SpaceX IPO and tariff refunds may have temporarily raised measured profits.

Domestic-industry profits after tax with IVA/CCAdj (W273RC1Q027SBEA): 1995Q1 394.194, 2026Q2 3,339.666 (https://fred.stlouisfed.org/data/W273RC1Q027SBEA).

## 7. Market concentration of large technology firms

**Top 10 share of the S&P 500.**
- 2000 (dot-com peak): 27% (Goldman Sachs Insights, 21 Mar 2024, https://www.goldmansachs.com/insights/articles/is-the-sp-too-concentrated).
- 31 May 2024: 34.07%; the prior record was 32.87% in 1963 (Global Financial Data, https://globalfinancialdata.com/s-p-market-concentration-hits-an-all-time-high).
- Mid-2025: "almost 40%," a level "not seen since the mid-1960s" (S&P Dow Jones Indices, Edwards and Didio, *In the Shadows of Giants*, April 2026, https://www.spglobal.com/spdji/en/documents/research/research-in-the-shadows-of-giants.pdf).
- 1 Oct 2025: 38.7% (Seeking Alpha News).
- 14 Mar 2026: "almost 40%" (Apollo, Bloomberg data, https://www.apolloacademy.com/sp-500-concentration-approaching-50/).
- ChartRow (from SEC N-PORT filings, https://chartrow.com/sp500/concentration): 22.8% (Sep 2019), 40.7% peak (Dec 2025), 37.9% (Jun 2026).
- S&P DJI data via Firstrade (18 Aug 2026): about 40%, compared with about 19% ten years earlier. At end-2025 the top 10 held about 32% of index earnings, so their share of value exceeds their share of earnings.

**Magnificent 7.** About 34% of the S&P 500 (Charles Schwab, August 2026), with a combined value of about $24.6 trillion in early October 2026 (ChartRow, both via Political.org, 7 Oct 2026). These are secondary figures.

**Headcount against value (latest 10-K, exact wording verified on sec.gov):**

| Firm | Employees | Date | 10-K |
|---|---|---|---|
| Apple | ~166,000 FTE | 27 Sep 2025 | https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm |
| Microsoft | ~223,000 full-time (121k US, 102k intl) | 30 Jun 2026 | https://www.sec.gov/Archives/edgar/data/0000789019/000119312526323660/msft-20260630.htm |
| Alphabet | 190,820 | 31 Dec 2025 | https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm |
| Amazon | ~1,576,000 full- and part-time | 31 Dec 2025 | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm |
| Meta | 78,865 (75,472 at 30 Jun 2026 per Q2 release) | 31 Dec 2025 | https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm |
| Nvidia | ~42,000 (31k R&D) in 38 countries | FY-end Jan 2026 | https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm |
| Tesla | 134,785 | 31 Dec 2025 | https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm |

The total is about 2.41 million worldwide, or about 0.84 million excluding Amazon. Against US nonfarm payrolls of 159.0 million (Sep 2026), that is 1.5% (0.5% excluding Amazon). Because the headcounts are global, these ratios overstate the US employment share. The group holds about a third of S&P 500 value. Amazon's 1.58 million is dominated by fulfilment, logistics and store operations. The 10-K does not break headcount down by function, so the "largely warehouse/logistics" characterisation is an inference from Amazon's business mix, not a reported figure. Tesla is a manufacturing firm. Two of the seven therefore employ mainly physical-economy labour, which weakens the strict "digital core employs few" framing. Nvidia, with about 42,000 staff and the largest index weight (about 6% per ChartRow), is the cleanest example of "scale without mass."

## 8. Productivity in physical sectors

**Goolsbee, Austan, and Chad Syverson. 2023.** "The Strange and Awful Path of Productivity in the U.S. Construction Sector." NBER WP 30845 (January 2023). DOI: 10.3386/w30845. https://www.nber.org/papers/w30845. Published as chapter 4 in Basu, Eldridge, Haltiwanger and Strassner (eds.), *Technology, Productivity, and Economic Growth*, NBER CRIW vol. 83, University of Chicago Press (2025 per the NBER page; ISBN 9780226839080), https://www.nber.org/books-and-chapters/technology-productivity-and-economic-growth/strange-and-awful-path-productivity-us-construction-sector.
- Abstract: aggregate data show a "large and decades-long decline" in construction productivity. Physical-output measures for housing show productivity falling or stagnant. Firms have become less efficient at turning materials into output. States with more productive construction sectors do not gain share, which the authors take as evidence of market frictions. Measurement error is unlikely to be the whole explanation.
- Numbers from Chicago Booth Review (secondary, https://chicagobooth.edu/review/us-construction-has-productivity-problem): construction labour productivity fell about 1% a year from 1970 to 2020, and by 2020 was below its 1950 level. Over the same period construction capital rose nearly eightfold and manufacturing labour productivity rose about ninefold.

**BEA–BLS integrated industry labour productivity, 1995→2020 (index 2012=100).** From a local copy of `BEA_BLS_industry_lp.csv` in the *GPTs are GPTs* replication repository, /home/claude/research/raw/gpts/GPTs-are-GPTs/data/. Upstream vintage not independently verified.
- Construction 109.92 → 106.20 (×0.97)
- Data processing / internet publishing 29.29 → 144.72 (×4.94)
- Broadcasting and telecom ×4.44
- Computer and electronic products ×6.32
- Retail trade ×1.92
- Ambulatory health care 91.55 → 102.69 (×1.12)
- Hospitals and nursing ×1.39
- Educational services ×1.10
- Legal services ×1.02
- Food services ×1.16

**BLS TFP, average annual growth 2019–24** (TED, 6 Jan 2026, https://www.bls.gov/opub/ted/2026/total-factor-productivity-increased-in-12-out-of-21-major-industries-from-2019-to-2024.htm): construction −0.7; information 1.8; health care and social assistance 0.7; manufacturing −0.1; professional and technical services 2.5; transportation and warehousing −0.4. BLS release USDL-25-1588 (19 Dec 2025, https://www.bls.gov/news.release/pdf/prod5.pdf), labour productivity in 2024: construction 1.9, information 5.3, health care 3.3, manufacturing −0.9.
**BLS detailed construction measures** (updated 28 Sep 2026, https://www.bls.gov/productivity/highlights/construction-labor-productivity.htm): in 2025, productivity fell 4.5% in single-family residential, 7.4% in multifamily, 12.1% in industrial building, and 1.8% in highway, street and bridge construction. Highway productivity declined every year from 2021 to 2025. Construction was 5.2% of nonfarm payroll employment and 4.4% of GDP in 2025.
**Information-sector TFP** (BLS TED 2024, https://www.bls.gov/opub/ted/2024/information-about-the-information-industry-productivity-and-growth.htm): 1990–2000 −0.8; 2000–07 3.4; 2007–19 1.0; 2019–22 2.3.

**Employment (BLS CES via FRED, thousands, SA), Jan 1995 → Sep 2026:**
- Construction (USCONS): 5,234 → 8,364
- Health care and social assistance (CES6562000001): 11,195.9 → 23,958.6
- Manufacturing (MANEMP): 17,262 → 12,652
- Information (USINFO): 2,785 → 2,739 (peak 3,552 in Jan 2000)
- Total nonfarm (PAYEMS): 116,505 → 159,044

Reading: low-productivity-growth physical and care sectors have absorbed a large share of employment growth, while the high-productivity information sector employs the same number of people as in 1995. This is the clearest support in this file for the claim that the physical economy remains where the jobs are.

## 9. Investment flows

**Hyperscaler 2026 capital expenditure guidance (latest, Q2 2026 reporting season):**
- Alphabet: $195–205 billion, raised from $180–190 billion. CFO Anat Ashkenazi, Q2 call, 23 Jul 2026 (w.media, https://w.media/ai-infrastructure-demand-pushes-alphabets-2026-capex-guidance-to-us-205-billion/). Q2 2026 capex was $44.9 billion.
- Meta: $130–145 billion including principal payments on finance leases, narrowed from $125–145 billion. Q2 2026 capex was $31.08 billion. Meta press release, 29 Jul 2026 (primary): https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-Second-Quarter-2026-Results/
- Amazon: about $220 billion, up from $200 billion. Andy Jassy, Q2 call, 30 Jul 2026 (Fortune, https://fortune.com/2026/07/30/andy-jassy-amazon-capex-demand-aws-pga-tour/).
- Microsoft: FY26 Q4 capex was $41 billion, about two-thirds on short-lived assets (CPUs/GPUs). Hood: "calendar year 2026 CapEx investment expectations remain unchanged," but the shift from finance to operating leases "adjust[s] our expectation to approximately $175 billion" (previously about $190 billion). FY27 Q1 is expected at over $50 billion. Sources: Motley Fool transcript https://www.fool.com/earnings/call-transcripts/2026/08/07/microsoft-msft-q4-2026-earnings-call-transcript/ ; CFO Dive https://www.cfodive.com/news/microsoft-holds-line-ai-spending-plans/.
- Sum of the four, using range midpoints and Microsoft's $175 billion: about $733 billion. On the low and high ends: $720–745 billion.

**Comparison with US physical infrastructure (Census C30, August 2026, SAAR; via InvestingLive, 1 Oct 2026, https://investinglive.com/news/us-construction-spending-for-the-month-of-august-0-9-versus-0-0-expected/):** total construction $2,203.1 billion (−1.7% y/y); public construction $547.8 billion; public highway and street $150.6 billion. Private data-centre construction was $84.95 billion SAAR in August 2026, compared with $49.05 billion a year earlier (NeoTeo analysis of Census tables, https://www.neoteo.com/en/us-data-center-construction-hit-a-reported-record-annual-pace-in-august). ABC (via Metal Construction News, 12 Aug 2026): private nonresidential construction excluding data centres fell 7.9% y/y in June 2026, and manufacturing construction fell 21.4% y/y.
Reading: four firms' planned 2026 capex (about $0.73 trillion, global) exceeds all US public construction ($0.55 trillion SAAR) and is about 4.9 times public highway spending. The comparison is not like for like. Hyperscaler capex is global, mostly equipment, and includes leases, whereas C30 is US structures only. Note also that much of this capex is physical: buildings, power and construction labour. It is a channel through which digital-core profits flow into the physical economy, which complicates a strict two-sector reading.

**Venture capital.**
- US 2025: $339.4 billion deal value, with AI/ML 65.4% of deal value and 39.4% of deal count (PitchBook-NVCA Venture Monitor Q4 2025, https://nvca.org/wp-content/uploads/2026/01/q4-2025-pitchbook-nvca-venture-monitor.pdf).
- US H1 2026: $412.7 billion, with AI about 86% ($355.9 billion) (PitchBook-NVCA Q2 2026 via SiliconANGLE, 9 Jul 2026, https://siliconangle.com/2026/07/09/pitchbook-us-venture-funding-hits-412-7b).
- Global 2025: $512 billion, with AI over half of value and nearly one-third of deals (PitchBook via SiliconANGLE, 7 Jan 2026).
- Global Q3 2026: $159 billion, with AI $102 billion (64%), 27 rounds of $1 billion or more, and $679 billion year to date (Crunchbase, via AI Weekly 5 Oct 2026; original https://news.crunchbase.com/venture/q3-2026-global-startup-funding-ai-billion-dollar-rounds-exits-data/ could not be fetched). For comparison, Q3 2025 was $97 billion with AI $45 billion (about 46%) (Crunchbase News, https://news.crunchbase.com/?p=92450).

## 10. Theory and background

**Acemoglu, Daron, and Simon Johnson. 2023.** *Power and Progress: Our Thousand-Year Struggle Over Technology and Prosperity.* New York: PublicAffairs. vii + 546 pp. ISBN 9781541702530 (library catalogue, https://catalog.chattlibrary.org/Record/1968926). Argument (MIT Sloan Management Review summary, https://sloanreview.mit.edu/?p=108664):
- The authors reject the "productivity bandwagon," the view that productivity gains automatically raise wages.
- The direction of technology reflects the "vision" of powerful actors.
- Gains have been shared only when countervailing power existed: democracy, unions and antitrust.
- Cheap labour-replacing "so-so automation" raises neither productivity nor wages much.
- The shift to shareholder-value maximisation reduced labour's share of gains.
- Their prescription for AI is "machine usefulness rather than machine intelligence."

Relevance: this is the mechanism the paper's claim needs. Who captures the gains is an institutional outcome, not a technological one.

**Piketty, Thomas. 2014.** *Capital in the Twenty-First Century.* Trans. Arthur Goldhammer. Cambridge, MA: Belknap Press of Harvard University Press. 696 pp. ISBN 978-0-674-43000-6. French original: Éditions du Seuil, 2013. When r > g persistently, wealth concentrates. Piketty later stated that r > g does not explain rising inequality in labour income (Wikipedia summary, https://en.wikipedia.org/wiki/Capital_in_the_Twenty-First_Century). Relevance: this is background for Section 5. Rising top-1% wealth with flat-to-falling labour share is consistent with returns on concentrated equity outpacing wage growth.

## 11. Contradicting evidence

1. **The labour-share decline as a measurement artefact (IPP capitalisation).** Koh, Dongya, Raül Santaeulàlia-Llopis, and Yu Zheng. 2020. "Labor Share Decline and Intellectual Property Products Capital." *Econometrica* 88(6): 2609–2628. DOI: 10.3982/ECTA17477. https://econometricsociety.org/publications/econometrica/2020/11/01/labor-share-decline-and-intellectual-property-products-capital. They find that the long-run decline in the US labour share is "entirely explained by the capitalization of intellectual property products." Implication: part of the "falling labour share" reflects the 1999/2013 NIPA treatment of software and R&D as investment. This cuts directly against using the labour share as evidence of one-sidedness without qualification. It is partly offset by the BEA compensation/GDI series (Section 4), which also falls, but which is likewise affected by IPP capitalisation through the GDI denominator.

2. **Housing and self-employment.** Rognlie, Matthew. 2015. "Deciphering the Fall and Rise in the Net Capital Share." *Brookings Papers on Economic Activity*, Spring 2015 (https://www.brookings.edu/articles/deciphering-the-fall-and-rise-in-the-net-capital-share). Net of depreciation, housing is the only source of a long-run rise in the capital share across the G7. Gutiérrez, Germán, and Sophie Piton. 2020. "Revisiting the Global Decline of the (Non-housing) Labor Share." *AER: Insights* 2(3): 321–38. DOI: 10.1257/aeri.20190285. Once housing and self-employment are harmonised, the labour share is stable or rising in all major advanced economies except the US and Canada. Implication: the decline is a North American phenomenon, not a general feature of digital capitalism.

3. **Efficient ("good") concentration.** Autor et al. (2020) interpret superstar firms as more productive, with concentrating industries showing faster productivity growth. Covarrubias, Matias, Germán Gutiérrez, and Thomas Philippon. 2020. "From Good to Bad Concentration? U.S. Industries over the Past 30 Years." *NBER Macroeconomics Annual 2019*, vol. 34 (NBER WP 25983, DOI 10.3386/w25983, https://nber.org/papers/w25983). Concentration in the 1990s was efficient: tougher price competition, intangible investment and rising leader productivity. After 2000 it became inefficient: entrenchment, entry barriers, lower investment and higher prices. Implication: the welfare reading depends on the period, and the 1995–2000 window, which is the claim's own baseline, was the benign phase.

4. **Within-establishment dynamics.** Kehrig, Matthias, and Nicolas Vincent. 2021. "The Micro-Level Anatomy of the Labor Share Decline." *QJE* 136(2): 1031–1087 (NBER WP 25275, https://www.nber.org/papers/w25275). Manufacturing labour share fell from 62 to 41 points (1967–2012) while the typical establishment's share rose by more than 3 points. Reallocation is toward high-productivity, high-price units whose low labour shares are temporary, rebounding after 5–8 years. The authors find that the reallocation is not driven by superstar firms. Implication: the evidence points to demand-side forces and transitory rents, not durable market power.

5. **Markup estimates are contested.**
   - Traina, James. 2018. "Is Aggregate Market Power Increasing? Production Trends Using Financial Statements." Stigler Center WP 272 (https://ideas.repec.org/p/zbw/cbscwp/272.html). Including SG&A largely removes the markup rise; this content summary is via the progress.org page, since RePEc shows no abstract.
   - Basu, Susanto. 2019. "Are Price-Cost Markups Rising in the United States? A Discussion of the Evidence." *JEP* 33(3): 3–22. DOI: 10.1257/jep.33.3.3. Dramatic markup increases are hard to reconcile with aggregate data, and current methods cannot distinguish flat from modestly rising markups.
   - Hall, Robert E. 2018. "New Evidence on the Markup of Prices over Marginal Costs and the Role of Mega-Firms in the US Economy." NBER WP 24574. DOI: 10.3386/w24574. Typical markup about 1.3, rising between 1988 and 2015. Sectors with more mega-firms do not have higher markups, though there is some evidence that markups grew where mega-firm intensity rose.
   - Benkard, C. Lanier, Nathan H. Miller, and Ali Yurukoglu. 2025. "The Rise of Market Power and the Macroeconomic Implications: Comment." NBER WP 34513 (Nov 2025). DOI: 10.3386/w34513. https://www.nber.org/papers/w34513. The De Loecker–Eeckhout–Unger result depends on unreported sample restrictions that drop 27% of observations. On the full sample, the increase is almost entirely driven by Finance and Insurance, and is modest otherwise (about 1.30 to 1.35 by 2016, per progress.org summary). The authors reply (2025, per the same summary) that this reflects outliers in NAICS 3254 (pharmaceuticals). Implication: this is the strongest recent challenge. Interestingly, if it holds, it relocates rising markups to the *financial* core, which is partly consistent with the claim's "digital/financial" wording.

6. **Post-2020 labour-share recovery: not supported by the data.** The BLS index rose in 2020 (to 104.195 in Q2) but this was a composition effect, and it has since fallen to 93.446. BEA compensation/GDI fell from 54.6 (2020) to 50.9 (2025). No recovery is visible in the official series through mid-2026. The brief 2020–21 rise should be reported, not omitted.

7. **The physical economy has changed.** Manufacturing employment fell by about 4.6 million (17.26m to 12.65m), and industry productivity growth varied widely (retail ×1.92, computers ×6.3, construction ×0.97, 1995–2020). Two Magnificent 7 firms (Amazon, Tesla) are large physical employers. Hyperscaler capex now supports a construction sub-sector (data centres, $85 billion SAAR). "Largely unchanged" should be restricted to occupational and sectoral employment composition in construction, care, transport and trades, and should not be applied to manufacturing.

8. **Concentration has precedent.** Top 10 S&P concentration of about 32–33% occurred in 1955 and 1963 (Global Financial Data). The current level is a post-1960s record, not unprecedented, and should not be described as "the highest ever" without that qualifier.

## 12. Could not verify

- **Bottom 50% share in 1990Q1 and 1995 (current vintage).** The FRED table for WFRBSB50215 and the Fed DFA site were blocked. Only 1989Q3 3.5, the 1992Q3 high of 4.1 and the 2010Q4 low of 0.4 are available, via American Default Research. The 2020-vintage UWSP values (3.9 in 1990, 4.0 in 1995) are not comparable with the 2026 vintage. To fill the gap, download WFRBSB50215 directly.
- **The 1980 and 2016 endpoints of the De Loecker–Eeckhout–Unger markup.** The abstract gives 21% and 61%. The years 1980 and 2016 come from secondary summaries (progress.org and the abstract's "after 1980"), not from the published figure.
- **Philippon (2019) quantitative claims** beyond the broadband price ratio, including household cost estimates. The book was not accessed directly.
- **Goolsbee–Syverson numerical results** (−1% a year, eightfold capital, ninefold manufacturing). These come from Chicago Booth Review, not the paper's tables.
- **BLS official labour productivity by sector, 1995–2025.** These were not retrieved. The 1995–2020 figures are BEA–BLS integrated-account indices from a local replication file whose vintage was not verified upstream.
- **Microsoft FY2027 capex.** One aggregator (Sentisense) reports FY26 capex of about $190 billion and an FY27 guide of $255–260 billion. This conflicts with the transcript language, which gives about $175 billion for calendar 2026 after lease reclassification. Treat the Sentisense figure as unverified.
- **Alphabet and Amazon capex** come from press reports of earnings calls, not company releases. Actual 2025 capex for each hyperscaler was not retrieved.
- **The Crunchbase Q3 2026 figures** come from a secondary site. The Crunchbase page itself was blocked.
- **The Magnificent 7 share (about 34%) and value ($24.6 trillion)** are secondary (Schwab and ChartRow via Political.org).
- **Amazon headcount by function.** The 10-K reports no split, so the warehouse/logistics share is an inference.
- **The total US infrastructure spending comparison.** Only Census public construction and highway SAAR figures were obtained. Federal IIJA outlays were not retrieved.
- **Stiglitz and Zuboff** were not covered (both optional).
- **The DFA top 1% value before 1989** does not exist, since the series begins in 1989Q3. No pre-1989 comparison is possible from the DFA.
