"""Trading comps for Salesforce: NTM multiples from consensus estimates.

Reads data/comps_inputs.csv (consensus from MarketScreener, Oct 28, 2026 closing prices)
and writes data/comps.csv. Prints the CRM value implied by the peer median multiples.

NTM (next twelve months) = calendar-weighted blend of fiscal years:
    NTM = (m / 12) * current FY + (1 - m / 12) * next FY,  m = months left in the current FY
    LTM = (m / 12) * previous FY + (1 - m / 12) * current FY
Revenue growth = NTM revenue / LTM revenue - 1.
"""
import csv
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rows = list(csv.DictReader(open(ROOT / "data" / "comps_inputs.csv")))

# Same equity bridge as the DCF (DCF tab, Jul 31, 2026 balance sheet), so comps and DCF differ only in EV
BRIDGE = 8310 + 3093 + 11324 * (1 - 0.20) - 39288  # cash + securities + 80% of strategic investments - debt
DILUTED_SHARES = 830

out = []
for r in rows:
    f = {k: float(v) for k, v in r.items() if k not in
         ("ticker", "company", "role", "currency", "fy_end", "price_source", "cur_fy_label", "consensus_snapshot")}
    w = f["months_left_in_current_fy"] / 12
    ntm = lambda a, b: w * f[a] + (1 - w) * f[b]
    rev_ntm = ntm("rev_cur_fy", "rev_next_fy")
    rev_ltm = w * f["rev_prev_fy"] + (1 - w) * f["rev_cur_fy"]
    ebitda_ntm = ntm("ebitda_cur_fy", "ebitda_next_fy")
    # EPS is GAAP for every company (MarketScreener; matches reported FY figures). Strip known one-offs from the
    # current FY so both years reflect ongoing earnings: CRM FY27 includes $2.43/share of Q2 strategic-investment gains.
    f["eps_cur_fy"] -= f["eps_cur_fy_one_offs"]
    eps_ntm = ntm("eps_cur_fy", "eps_next_fy")
    mcap = f["price_oct28"] * f["shares_mm"]
    ev = mcap + f["net_debt_mm"]
    out.append({
        "ticker": r["ticker"], "company": r["company"], "role": r["role"], "currency": r["currency"],
        "price_oct28": f["price_oct28"], "market_cap_mm": round(mcap), "ev_mm": round(ev),
        "ntm_revenue_mm": round(rev_ntm), "ntm_ebitda_mm": round(ebitda_ntm), "ntm_eps": round(eps_ntm, 3),
        "ev_ntm_revenue": round(ev / rev_ntm, 2), "ev_ntm_ebitda": round(ev / ebitda_ntm, 1),
        "ntm_pe": round(f["price_oct28"] / eps_ntm, 1), "ntm_revenue_growth": round(rev_ntm / rev_ltm - 1, 3),
        "ntm_ebitda_margin": round(ebitda_ntm / rev_ntm, 3),
    })

with open(ROOT / "data" / "comps.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
    w.writeheader()
    w.writerows(out)

peers = [o for o in out if o["role"] == "peer"]
crm = next(o for o in out if o["ticker"] == "CRM")
med = {k: statistics.median(p[k] for p in peers)
       for k in ("ev_ntm_revenue", "ev_ntm_ebitda", "ntm_pe", "ntm_revenue_growth", "ntm_ebitda_margin")}

print(f"{'':6}{'EV/Rev':>8}{'EV/EBITDA':>11}{'P/E':>7}{'Growth':>8}{'Margin':>8}")
for o in out:
    tag = " (ref)" if o["role"] == "reference" else ""
    print(f"{o['ticker']:6}{o['ev_ntm_revenue']:>7.1f}x{o['ev_ntm_ebitda']:>10.1f}x{o['ntm_pe']:>6.1f}x"
          f"{o['ntm_revenue_growth']:>8.1%}{o['ntm_ebitda_margin']:>8.1%}{tag}")
print(f"{'Median':6}{med['ev_ntm_revenue']:>7.1f}x{med['ev_ntm_ebitda']:>10.1f}x{med['ntm_pe']:>6.1f}x"
      f"{med['ntm_revenue_growth']:>8.1%}{med['ntm_ebitda_margin']:>8.1%}   (5 peers, excl. MSFT)")

implied = {
    "EV / NTM revenue": (med["ev_ntm_revenue"] * crm["ntm_revenue_mm"] + BRIDGE) / DILUTED_SHARES,
    "EV / NTM EBITDA": (med["ev_ntm_ebitda"] * crm["ntm_ebitda_mm"] + BRIDGE) / DILUTED_SHARES,
    "NTM P/E": med["ntm_pe"] * crm["ntm_eps"],
}
print("\nCRM value implied by peer median multiples (DCF equity bridge, 830mm diluted shares):")
for k, v in implied.items():
    print(f"  {k:18} ${v:,.2f}")
print(f"  {'Median of three':18} ${statistics.median(implied.values()):,.2f}")

# Growth-matched check: peers growing within 2 points of CRM's NTM revenue growth
near = [p for p in peers if abs(p["ntm_revenue_growth"] - crm["ntm_revenue_growth"]) <= 0.02]
if near:
    gm = {k: statistics.mean(p[k] for p in near) for k in ("ev_ntm_revenue", "ev_ntm_ebitda", "ntm_pe")}
    gi = {
        "EV / NTM revenue": (gm["ev_ntm_revenue"] * crm["ntm_revenue_mm"] + BRIDGE) / DILUTED_SHARES,
        "EV / NTM EBITDA": (gm["ev_ntm_ebitda"] * crm["ntm_ebitda_mm"] + BRIDGE) / DILUTED_SHARES,
        "NTM P/E": gm["ntm_pe"] * crm["ntm_eps"],
    }
    print(f"\nGrowth-matched peers ({', '.join(p['ticker'] for p in near)}; NTM growth within 2 pts of CRM):")
    for k, v in gi.items():
        print(f"  {k:18} ${v:,.2f}")
