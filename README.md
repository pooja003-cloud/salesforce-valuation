# Salesforce (CRM) — Three-Statement Model & DCF

**Is Salesforce worth its share price?** This project answers that from the viewpoint of a long-term shareholder, using a fully linked three-statement financial model and a discounted cash flow (DCF) valuation built from Salesforce's own SEC filings.

| | Downside | **Base** | Upside |
|---|---:|---:|---:|
| **Value per share (perpetuity growth, headline)** | $171.48 | **$221.76** | $255.81 |
| vs. share price ($235.95, Oct 14, 2026) | −27.3% | **−6.0%** | +8.4% |
| Cross-check: value per share at 13x exit EV/EBITDA | $195.58 | $245.31 | $279.56 |
| FY2031 revenue | $58.5B | **$67.0B** | $72.6B |
| FY2031 GAAP operating margin | 25.6% | **28.2%** | 29.8% |
| FY2031 unlevered FCF, valued in the DCF¹ | $12.8B | **$16.5B** | $19.0B |
| FY2031 free cash flow, CFO − capex² | $17.4B | **$21.9B** | $25.0B |

¹ Before interest, with stock-based compensation treated as a cost. This is the cash flow the DCF discounts.
² After interest, with stock-based compensation added back, the way companies usually report FCF. Shown for comparison only.

**Conclusion:** in the base case Salesforce looks fairly to slightly fully valued: the headline value is about 6% below the share price, and the exit-multiple cross-check is about 4% above it. The stock only looks cheap if you believe its AI products (Agentforce) lift bookings above management's current trajectory.

> Educational project, not investment advice.

---

## Why Salesforce

- **Subscription business with contracted backlog.** Customers sign multi-year contracts and often pay upfront. Salesforce reports $72.4B of remaining performance obligations (RPO), with $35.1B due within 12 months. That backlog makes revenue unusually forecastable.
- **A live debate on stock-based compensation.** Salesforce pays about 8% of revenue in stock. Whether to treat that as a real cost changes the valuation by about $50 per share.
- **An eventful 2026.** The Informatica acquisition, a $25B accelerated share repurchase funded with ~$24.8B of new debt, and a large bet on agentic AI.
- **Clean, well-covered public filings,** so every historical input is verifiable.

## How the model works

```
SEC filings ──► RPO revenue build ──► Income statement ──► Balance sheet ◄──► Cash flow ──► DCF ──► Value per share
```

1. **Current RPO** (revenue under contract, due within 12 months) grows at a scenario-specific rate.
2. **Subscription revenue** = prior year-end current RPO × a conversion ratio (1.29–1.32x historically; 1.257x in FY27 reproduces management's $46.1–46.4B guidance).
3. **Costs** are modeled as a share of revenue on a GAAP basis (stock compensation stays inside each cost line). Amortization of acquired intangibles is excluded from those percentages and follows its own schedule, so as acquisitions age the roll-off lifts GAAP operating income instead of turning into a hidden cash cost.
4. **Balance sheet and cash flow** are fully linked. Unearned revenue, the cash customers prepay, is the key working-capital inflow. The balance sheet balances to zero in every year.
5. **DCF**: unlevered free cash flow discounted at a 10.3% WACC (mid-year convention). The headline terminal value uses perpetuity growth of 3.0%. A 13x exit EV/EBITDA multiple is a cross-check: it implies 3.8% growth forever, so the two methods agree within a point. Net debt and share count come from the Jul 31, 2026 balance sheet.

## Key judgment calls

| Choice | Why | Effect |
|---|---|---|
| Stock comp treated as a real cost | The dilution to shareholders is real | Adding it back raises base value to ~$305 |
| Perpetuity growth as the headline method | It values the same cash flow the model forecasts | Exit multiple at 13x gives $245 as a cross-check; at 16x it would give $293 but imply 4.9% growth forever |
| WACC built from a 5.21% 10-year Treasury | Reflects current rates, not an old 8% template | At 8% WACC the base value would be ~$335 |
| Finance-lease costs kept inside operating costs | Simpler than splitting into depreciation plus financing-line principal; treats them as if paid in cash | Slightly conservative versus the company's own FCF definition |
| Undisclosed acquisitions excluded | Contentful and Fin prices not yet public | Will be added when disclosed |
| Debt assumed to refinance | Keeps the model simple | Cash builds to ~$48B by FY31 |

## Repository contents

```
model/Salesforce_CRM_Model.xlsx   The model (open in Excel)
scripts/build_model.py            Rebuilds the workbook from scratch with openpyxl
docs/project-explained.md         Plain-English explanation for non-finance readers
```

### Workbook tabs

| Tab | What it holds |
|---|---|
| **Cover** | Key outputs, integrity checks (balance sheet, positive cash, WACC > growth, exit multiple vs perpetuity consistency), size of the historical cash-flow plug, scenario snapshot, how-to |
| **Assumptions** | All forecast drivers. Scenario switch in cell `B4` (1 Downside, 2 Base, 3 Upside) |
| **Revenue Build** | RPO-driven revenue engine, billings, FY27 guidance check |
| **IS / BS / CF** | Income statement, balance sheet (with balance check), cash flow statement |
| **DCF** | WACC, unlevered FCF, terminal value, equity bridge, two sensitivity tables |
| **Sources** | Where every historical number comes from |

Colour code: **blue** = hardcoded input · **black** = formula · **green** = link to another sheet · **yellow** = key lever.

### Rebuilding the workbook

```bash
pip install -r requirements.txt
python scripts/build_model.py
```

The script writes formulas, not values. Open the file in Excel and it calculates automatically.

## Updating the model

- **After each earnings release:** update the latest balance sheet inputs on the `DCF` tab (cash, investments, debt, basic shares in `B7`).
- **Market data:** share price (`DCF!B6`) and risk-free rate (`DCF!B19`).
- **Your own view:** change base-case current RPO growth for FY28–FY31 on `Assumptions` row 11. FY27 is anchored to guidance.

## Sources

- [Salesforce Q4 FY26 earnings release, 8-K Ex. 99.1 (Feb 25, 2026)](https://www.sec.gov/Archives/edgar/data/1108524/000110852426000056/crm-q4fy26xexhibit991.htm)
- [Salesforce Q4 FY24 earnings release, 8-K Ex. 99.1 (Feb 28, 2024)](https://www.sec.gov/Archives/edgar/data/1108524/000110852424000002/crm-q4fy24xexhibit991.htm)
- [Salesforce Q2 FY27 earnings release (Aug 26, 2026)](https://investor.salesforce.com/files/doc_financials/2027/q2/CRM-Q2-FY27-Earnings-Press-Release.pdf)
- Share price and shares outstanding: stockanalysis.com, close Oct 14, 2026
- Beta 1.26: Yahoo Finance "Beta (5Y monthly)", monthly returns vs the S&P 500; cross-checked with stockanalysis.com "Beta (5Y)"
- [10-year Treasury yield: FRED series DGS10](https://fred.stlouisfed.org/series/DGS10), 5.21% on Oct 13, 2026

## Changelog

- **Model review (Oct 15, 2026).** Amortization of acquired intangibles moved out of the cost percentages so its roll-off raises operating income; headline switched to perpetuity growth with a 13x exit multiple as a consistency-checked cross-check (was a 50/50 blend with 16x, which implied 4.9% growth forever); both FCF definitions labeled; lease wording corrected; the cash-flow tie-out check (which could not fail) replaced by a plug-size disclosure; 10-year yield re-sourced to FRED and beta to a named 5-year monthly window. Base value moved from $230.36 to $221.76; the conclusion (roughly fairly valued) is unchanged.

## Roadmap

- [ ] Interactive website with live sliders (built, not yet published)
- [ ] Weekly refresh of share price and Treasury yield
- [ ] Earnings-update workflow that proposes changes for review
