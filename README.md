# Salesforce (CRM) — Three-Statement Model & DCF

> **Rating: Hold · Price target $228 · Price $242.11 on Oct 28, 2026 (NYSE close)**
>
> Base-case value is 5.8% below the share price. Rating rule: upside above +15% is a Buy, −10% to +15% a Hold, below −10% a Sell. On Oct 29 software stocks sold off after ServiceNow's results and CRM traded near $231 intraday; at that price the gap is about −1%, still a Hold.

**Is Salesforce worth its share price?** This project answers that from the viewpoint of a long-term shareholder, using a fully linked three-statement financial model and a discounted cash flow (DCF) valuation built from Salesforce's own SEC filings, checked against trading comparables.

| | Downside | **Base** | Upside |
|---|---:|---:|---:|
| **Value per share (perpetuity growth, headline)** | $176.43 | **$228.11** | $263.10 |
| vs. share price ($242.11, Oct 28, 2026) | −27.1% | **−5.8%** | +8.7% |
| Cross-check: value per share at 13x exit EV/EBITDA | $197.58 | $247.78 | $282.35 |
| FY2031 revenue | $58.5B | **$67.0B** | $72.6B |
| FY2031 GAAP operating margin | 25.6% | **28.2%** | 29.8% |
| FY2031 unlevered FCF, valued in the DCF¹ | $12.8B | **$16.5B** | $19.0B |
| FY2031 free cash flow, CFO − capex² | $17.4B | **$21.9B** | $25.0B |

¹ Before interest, with stock-based compensation treated as a cost. This is the cash flow the DCF discounts.
² After interest, with stock-based compensation added back, the way companies usually report FCF. Shown for comparison only.

Even the upside case only reaches +8.7%, short of the +15% a Buy needs. Peers trade at multiples that imply more ($238–$286, see [Trading comps](#trading-comps)), mostly because the market does not charge for stock-based compensation the way this model does.

> Educational project, not investment advice.

![Cover tab: key outputs, call, integrity checks and scenario snapshot](docs/images/cover.png)

---

## Investment thesis

1. **Most of next year's revenue is already signed.** Salesforce ended FY26 with $72.4B of remaining performance obligations, $35.1B of it due within twelve months. That backlog is why the model can build revenue from contracts rather than from a growth guess, and why FY27 lands inside management's guidance.
2. **Reported profits rise as old deals finish amortizing.** About $1.9B a year of acquired-intangible amortization falls to roughly $0.5B by FY31. That is a non-cash charge, so as it runs off, GAAP operating margin climbs from 20% to 28% without the business having to do anything new.
3. **Agentforce is not in the base case.** The base case has bookings growth fading from 12% to 8%. If agentic AI reaccelerates growth, that is upside the price target does not count on; the upside scenario ($263) shows roughly what it would take.

## The key debate: is stock-based compensation a real cost?

Salesforce pays about 8% of revenue (~$3.8B in FY27) in stock. Most sell-side models add it back to free cash flow because no cash leaves the company. This model does not: every share issued to employees is a smaller slice for existing owners, and Salesforce spends cash on buybacks partly to offset that dilution.

The choice is worth about **$85 a share**: $228 with stock comp as a cost, about **$313** if it is added back. It is also the main reason the comps (below) imply more than the DCF, since peer multiples are built on adjusted earnings that exclude it.

## Risks

1. **Debt-funded buyback.** Salesforce borrowed about $24.8B in 2026 to buy back $25B of stock, taking total debt from $14.4B to $39.3B. Buying shares near today's price creates little value if the stock is worth about $228, and the debt now costs interest the company did not pay before.
2. **Integrating Informatica.** The acquisition closed in late 2025 and adds roughly 3 points to FY27 growth. If customers churn or the data-management product loses ground, that growth fades and the amortization charges stay without the revenue behind them.
3. **The multiple shrinks as growth slows.** Revenue growth slows from about 11% in FY27 to about 9% by FY31. Slower-growing software companies trade on lower multiples, and the model already assumes CRM's EV/EBITDA falls from 18.4x today to 13x. A faster de-rating would pull the cross-check value down by roughly $30 per 2x of multiple.

---

## Trading comps

A market-based check next to the DCF: what CRM would be worth if it traded at its peers' multiples. All prices are Oct 28, 2026 closes; estimates are analyst consensus from MarketScreener; NTM (next twelve months) blends each company's fiscal years by the months remaining.

| Company | EV / NTM revenue | EV / NTM EBITDA | NTM P/E | NTM revenue growth |
|---|---:|---:|---:|---:|
| ServiceNow (NOW) | 8.2x | 21.6x | 68.5x | 19.3% |
| Oracle (ORCL) | 5.2x | 9.0x | 18.8x | 39.9% |
| Adobe (ADBE) | 3.4x | 7.1x | 11.8x | 9.3% |
| Workday (WDAY) | 4.2x | 12.1x | 33.7x | 10.7% |
| SAP (SAP) | 5.5x | 16.8x | 26.5x | 11.4% |
| **Peer median** | **5.2x** | **12.1x** | **26.5x** | **11.4%** |
| **Salesforce (CRM)** | **4.5x** | **11.3x** | **24.4x** | **10.1%** |
| *Microsoft (MSFT), reference only* | *9.3x* | *15.1x* | *25.3x* | *18.5%* |

Microsoft is shown for reference and left out of the median: its size and Azure/AI mix make it a different business, not a peer.

**CRM value implied by peer multiples** (same equity bridge as the DCF: cash, securities, 80% of strategic investments, less debt, over 830M diluted shares):

| Multiple | Peer median | Growth-matched peers (ADBE, WDAY, SAP) |
|---|---:|---:|
| EV / NTM revenue | $285.51 | $237.64 |
| EV / NTM EBITDA | $268.77 | $266.36 |
| NTM P/E | $263.46 | $238.61 |

**DCF $228 vs comps $238–$286: why they differ**

- **Stock comp.** Consensus EBITDA and most peer valuations exclude stock-based compensation; the DCF counts it as a cost. With stock comp added back the DCF gives about $313, above the comps range. The comps sit between the two treatments.
- **Faster growers lift the median.** ServiceNow (19% growth) and Oracle (40%, driven by AI infrastructure contracts) pull the median up. Peers growing at CRM's pace (Adobe, Workday, SAP) imply $238–$266, close to today's price.
- **Comps measure relative value, the DCF intrinsic value.** Comps say what the market pays today for similar companies; the DCF asks what the cash flows are worth at a 10.2% required return. If the whole sector is richly priced, comps inherit that. The two disagreeing by $10–60 is normal and is the reason to show both.

**Caveats.** Consensus snapshots range from Sep 22 to Oct 28, 2026; prices are all Oct 28. ServiceNow reported after the Oct 28 close and fell about 19–27% on Oct 29, which would cut its multiples sharply and lower the peer median. EPS bases differ by company as reported by MarketScreener, so P/E is the least reliable of the three. The inputs, sources and calculation are in `data/comps_inputs.csv` and `scripts/comps.py`.

---

## Why Salesforce

- **Subscription business with contracted backlog.** Customers sign multi-year contracts and often pay upfront. That backlog makes revenue unusually forecastable.
- **A live debate on stock-based compensation,** worth about $85 a share (see above).
- **An eventful 2026.** The Informatica acquisition, a $25B accelerated share repurchase funded with new debt, and a large bet on agentic AI.
- **Clean, well-covered public filings,** so every historical input is verifiable.

## How the model works

```
SEC filings ──► RPO revenue build ──► Income statement ──► Balance sheet ◄──► Cash flow ──► DCF ──► Value per share
                                                                                              ▲
                                                                     Trading comps ───────────┘ (cross-check)
```

1. **Current RPO** (revenue under contract, due within 12 months) grows at a scenario-specific rate.
2. **Subscription revenue** = prior year-end current RPO × a conversion ratio (1.29–1.32x historically; 1.257x in FY27 reproduces management's $46.1–46.4B guidance).
3. **Costs** are modeled as a share of revenue on a GAAP basis (stock compensation stays inside each cost line). Amortization of acquired intangibles is excluded from those percentages and follows its own schedule, so as acquisitions age the roll-off lifts GAAP operating income instead of turning into a hidden cash cost.
4. **Balance sheet and cash flow** are fully linked. Unearned revenue, the cash customers prepay, is the key working-capital inflow. The balance sheet balances to zero in every year.
5. **DCF**: unlevered free cash flow discounted at a 10.2% WACC (mid-year convention). The headline terminal value uses perpetuity growth of 3.0%. A 13x exit EV/EBITDA multiple is shown as a cross-check. It is **calibrated, not independent**: it was set so its implied perpetual growth (3.6%) stays close to the 3% assumption, so the two methods agreeing is by construction. What it does tell you is that holding today's 18.4x FY27E GAAP EBITDA multiple into FY31 would require far more growth than the model assumes; the cross-check therefore assumes a de-rating from 18x to 13x as revenue growth slows from ~11% to ~9%. (On GAAP EBITDA, which counts stock comp as a cost; 13x is ~10x on adjusted EBITDA.) Net debt and share count come from the Jul 31, 2026 balance sheet.
6. **Call**: the Cover tab turns the headline upside into a rating with the rule above, and shows the price target and the date it was priced.

## Key judgment calls

| Choice | Why | Effect |
|---|---|---|
| Stock comp treated as a real cost | The dilution to shareholders is real | Adding it back raises base value to ~$313 |
| Perpetuity growth as the headline method | It values the same cash flow the model forecasts | Exit multiple at 13x gives $248 as a cross-check; at 16x it would give $296 but imply 4.8% growth forever |
| 13x exit multiple, calibrated | Chosen to keep implied growth near 3%, i.e. a de-rating from today's 18.4x as growth slows; not taken from peers | Each 2x turn moves the cross-check by roughly $30 a share (see DCF sensitivity table) |
| Margins expand in the base case | Sales & marketing efficiency (~50 bp a year) plus amortization roll-off | Non-GAAP operating margin 34.0% (FY26) → 37.8% (FY31), about 4 points; GAAP 20.1% → 28.2% |
| WACC built from a 4.99% 10-year Treasury | Reflects current rates, not an old 8% template | At 8% WACC the base value would be ~$336 |
| Finance-lease costs kept inside operating costs | Simpler than splitting into depreciation plus financing-line principal; treats them as if paid in cash | Slightly conservative versus the company's own FCF definition |
| Undisclosed acquisitions excluded | Contentful and Fin prices not yet public | Will be added when disclosed |
| ASR final settlement not yet reflected | Not reported as of Oct 28; 823M basic shares after the initial delivery | Any extra shares delivered at settlement would lift value per share slightly |
| Debt assumed to refinance | Keeps the model simple | Cash builds to ~$48B by FY31 |

## Margin path vs management's targets

The base case assumes about **4 points of non-GAAP operating margin expansion** (34.0% in FY26 to 37.8% in FY31). GAAP margin rises faster (20.1% to 28.2%) because amortization of acquired intangibles rolls off from $1.9B to $0.5B.

Management's own yardstick is its "50 by FY30" framework: subscription & support growth (constant currency) plus non-GAAP operating margin should total 50 by the end of FY30 ([Oct 2025 investor day](https://investor.salesforce.com/news/news-details/2025/Salesforce-Announces-New-FY30-Revenue-Target-of-60B-10-Organic-FY26-FY30-CAGR/)). The model's FY30 score is **46.9** (10.0% growth + 36.9% margin; reported rather than constant-currency growth), so the base case is more conservative than management's target. FY30 revenue in the model is $61.7B including Informatica, against management's $60B+ target excluding it.

![DCF tab: terminal value, equity bridge and sensitivity tables](docs/images/dcf-valuation.png)

## Repository contents

```
model/Salesforce_CRM_Model.xlsx   The model (open in Excel)
scripts/build_model.py            Rebuilds the workbook from scratch with openpyxl
scripts/comps.py                  Computes the trading comps and implied values
data/comps_inputs.csv             Comps inputs: Oct 28 prices, consensus estimates, sources
data/comps.csv                    Comps output: multiples, growth, margins
docs/project-explained.md         Plain-English explanation for non-finance readers
docs/images/                      Screenshots of the Cover and DCF tabs
```

### Workbook tabs

| Tab | What it holds |
|---|---|
| **Cover** | Key outputs, the call (rating, price target, pricing date), integrity checks (balance sheet, positive cash, WACC > growth, exit-multiple calibration), today's market multiple, FY30 "growth + margin" score, the historical cash-flow plug, scenario snapshot, how-to |
| **Assumptions** | All forecast drivers. Scenario switch in cell `B4` (1 Downside, 2 Base, 3 Upside) |
| **Revenue Build** | RPO-driven revenue engine, billings, FY27 guidance check |
| **IS / BS / CF** | Income statement, balance sheet (with balance check), cash flow statement |
| **DCF** | WACC, unlevered FCF, terminal value, equity bridge, two sensitivity tables |
| **Sources** | Where every historical number comes from |

Colour code: **blue** = hardcoded input · **black** = formula · **green** = link to another sheet · **yellow** = key lever.

### Rebuilding

```bash
pip install -r requirements.txt
python scripts/build_model.py   # workbook
python scripts/comps.py         # comps table and implied values
```

The build script writes formulas, not values. Open the file in Excel and it calculates automatically.

## Updating the model

- **Before publishing a call:** refresh the share price (`DCF!B6`), the valuation date (`DCF!B5`) and the risk-free rate (`DCF!B19`), then re-check the rating on the Cover tab. Refresh `price_oct28` in `data/comps_inputs.csv` to the same date.
- **After each earnings release:** update the latest balance sheet inputs on the `DCF` tab (cash, investments, debt, basic shares in `B7`). The next release (Q3 FY27) is expected around Dec 2, 2026.
- **Your own view:** change base-case current RPO growth for FY28–FY31 on `Assumptions` row 11. FY27 is anchored to guidance.

## Sources

- [Salesforce Q4 FY26 earnings release, 8-K Ex. 99.1 (Feb 25, 2026)](https://www.sec.gov/Archives/edgar/data/1108524/000110852426000056/crm-q4fy26xexhibit991.htm)
- [Salesforce Q4 FY24 earnings release, 8-K Ex. 99.1 (Feb 28, 2024)](https://www.sec.gov/Archives/edgar/data/1108524/000110852424000002/crm-q4fy24xexhibit991.htm)
- [Salesforce Q2 FY27 earnings release (Aug 26, 2026)](https://investor.salesforce.com/files/doc_financials/2027/q2/CRM-Q2-FY27-Earnings-Press-Release.pdf)
- Share price: $242.11 NYSE close, Oct 28, 2026 ([Motley Fool quote](https://www.fool.com/quote/nyse/crm/); [Trefis, Oct 29](https://www.trefis.com/stock/crm/articles/621321/can-you-still-buy-salesforce-stock-today/2026-10-29))
- Beta 1.26: Yahoo Finance "Beta (5Y monthly)", monthly returns vs the S&P 500; cross-checked with stockanalysis.com "Beta (5Y)"
- [10-year Treasury yield: FRED series DGS10](https://fred.stlouisfed.org/series/dgs10), 4.99% on Oct 27, 2026
- Comps consensus estimates: MarketScreener valuation pages for each company (snapshot dates in `data/comps_inputs.csv`); Oct 28 closes from Motley Fool, boerse.de (SAP, Xetra) and stockanalysis.com (MSFT)
- [Oct 29 software selloff after ServiceNow results (24/7 Wall St.)](https://247wallst.com/investing/2026/10/29/servicenow-tumbles-19-as-slower-contract-growth-overshadows-raised-ai-target-salesforce-slides-6-workday-drops-5)

## Changelog

- **Model review (Oct 15, 2026).** Amortization of acquired intangibles moved out of the cost percentages so its roll-off raises operating income; headline switched to perpetuity growth with a 13x exit multiple as a cross-check (was a 50/50 blend with 16x, which implied 4.9% growth forever); both FCF definitions labeled; lease wording corrected; the cash-flow tie-out check (which could not fail) replaced by a plug-size disclosure; 10-year yield re-sourced to FRED and beta to a named 5-year monthly window. Base value moved from $230.36 to $221.76.
- **Second review (Oct 15, 2026).** 13x exit multiple disclosed as calibrated, with today's market multiple shown for context; margin path compared with management's "50 by FY30" target; historical working-capital lines filled from the reported cash flow statements (FY25–FY26 plug now max 10.6% of CFO, was 26.8%); screenshots added.
- **Call and comps (Oct 29, 2026).** Repriced at the Oct 28 close ($242.11) with the 10-year at 4.99%; base value $228.11 (was $221.76, mainly the lower risk-free rate). Added the rating rule and call (Hold, price target $228), trading comps against five peers with Microsoft as reference, and the thesis, key debate and risks.

## Roadmap

- [ ] Interactive website with live sliders (built, not yet published)
- [ ] Weekly refresh of share price and Treasury yield
- [ ] Earnings-update workflow that proposes changes for review
