# Salesforce (CRM) — Three-Statement Model & DCF

**Is Salesforce worth its share price?** This project answers that from the viewpoint of a long-term shareholder, using a fully linked three-statement financial model and a discounted cash flow (DCF) valuation built from Salesforce's own SEC filings.

| | Downside | **Base** | Upside |
|---|---:|---:|---:|
| Value per share | $179.91 | **$230.36** | $265.02 |
| vs. share price ($235.95, Oct 14, 2026) | −23.8% | **−2.4%** | +12.3% |
| FY2031 revenue | $58.5B | **$67.0B** | $72.6B |
| FY2031 GAAP operating margin | 22.4% | **24.9%** | 26.4% |
| FY2031 free cash flow | $15.9B | **$20.2B** | $23.0B |

**Conclusion:** in the base case Salesforce is roughly fairly valued. The stock only looks cheap if you believe its AI products (Agentforce) lift bookings above management's current trajectory.

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
3. **Costs** are modeled as a share of revenue on a GAAP basis (stock compensation stays inside each cost line).
4. **Balance sheet and cash flow** are fully linked. Unearned revenue, the cash customers prepay, is the key working-capital inflow. The balance sheet balances to zero in every year.
5. **DCF**: unlevered free cash flow discounted at a 10.3% WACC (mid-year convention), with terminal value from both perpetuity growth (3.0%) and an exit multiple (16x EBITDA), blended 50/50. Net debt and share count come from the Jul 31, 2026 balance sheet.

## Key judgment calls

| Choice | Why | Effect |
|---|---|---|
| Stock comp treated as a real cost | The dilution to shareholders is real | Adding it back raises base value to ~$282 |
| WACC built from a 5.2% 10-year Treasury | Reflects current rates, not an old 8% template | At 8% WACC the base value would be much higher |
| Lease-adjusted free cash flow | Lease payments are real cash costs | Modeled FCF runs ~$1B below company-reported FCF |
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
| **Cover** | Key outputs, integrity checks, scenario snapshot, how-to |
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
- Share price, shares outstanding and beta: stockanalysis.com, close Oct 14, 2026
- 10-year Treasury yield: 5.19–5.24%, Oct 9–13, 2026

## Roadmap

- [ ] Interactive website with live sliders (built, not yet published)
- [ ] Weekly refresh of share price and Treasury yield
- [ ] Earnings-update workflow that proposes changes for review
