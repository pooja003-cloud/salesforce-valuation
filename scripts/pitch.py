"""Two-page equity pitch for Salesforce (CRM), built from the model and the comps.

Reads the recalculated workbook (model/Salesforce_CRM_Model.xlsx, cached values) and data/comps.csv,
and writes docs/pitch.pdf. Run scripts/build_model.py and recalculate (open/save in Excel or LibreOffice)
and scripts/comps.py first.
"""
import csv
import statistics
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "pitch.pdf"
CHART = ROOT / "docs" / "images" / "valuation-range.png"

# ---------------------------------------------------------------- data from the model
wb = load_workbook(ROOT / "model" / "Salesforce_CRM_Model.xlsx", data_only=True)
dcf, cov, inc = wb["DCF"], wb["Cover"], wb["IS"]
price = dcf["B6"].value
priced_on = dcf["B5"].value.strftime("%b %-d, %Y")
target = dcf["D74"].value
upside = dcf["D76"].value
rating = cov["E6"].value.title()
wacc = dcf["B30"].value
snap = {c: [cov[f"{c}{r}"].value for r in range(31, 38)] for c in "BCD"}  # Downside, Base, Upside
down, base, up = snap["B"][0], snap["C"][0], snap["D"][0]
exit_lo, exit_hi = snap["B"][2], snap["D"][2]
rev27, rev26 = inc["F7"].value, inc["E7"].value
diluted = dcf["B9"].value
bridge = dcf["B11"].value + dcf["B12"].value + dcf["B13"].value * (1 - dcf["B14"].value) - dcf["B15"].value
mcap = price * dcf["B7"].value  # basic shares
ev = price * diluted - bridge
SBC_ADDBACK = 313.24     # base value with SBC added back (DCF!B16 = 0); from the scenario run in the build notes
buy_below, sell_above = target / 1.15, target / 0.90

# ---------------------------------------------------------------- comps
comps = list(csv.DictReader(open(ROOT / "data" / "comps.csv")))
num = lambda r, k: float(r[k])
peers = [r for r in comps if r["role"] == "peer"]
crm = next(r for r in comps if r["ticker"] == "CRM")
near = [p for p in peers if abs(num(p, "ntm_revenue_growth") - num(crm, "ntm_revenue_growth")) <= 0.02]


def implied(group, agg):
    m = {k: agg([num(p, k) for p in group]) for k in ("ev_ntm_revenue", "ev_ntm_ebitda", "ntm_pe")}
    return [(m["ev_ntm_revenue"] * num(crm, "ntm_revenue_mm") + bridge) / diluted,
            (m["ev_ntm_ebitda"] * num(crm, "ntm_ebitda_mm") + bridge) / diluted,
            m["ntm_pe"] * num(crm, "ntm_eps")]


med_vals = implied(peers, statistics.median)
gm_vals = implied(near, statistics.mean)

# ---------------------------------------------------------------- chart: valuation range
INK, MUTED, LINE = "#121821", "#5a6474", "#dde2e9"
BLUE, ORANGE = "#2a78d6", "#eb6834"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
bars = [
    ("DCF scenarios (down / base / up)", down, up, base, BLUE),
    ("13x exit-multiple cross-check", exit_lo, exit_hi, snap["C"][2], BLUE),
    ("Comps: peer median", min(med_vals), max(med_vals), statistics.median(med_vals), ORANGE),
    ("Comps: growth-matched peers", min(gm_vals), max(gm_vals), statistics.median(gm_vals), ORANGE),
]
fig, ax = plt.subplots(figsize=(7.2, 2.7), dpi=200)
for i, (lab, lo, hi, mid, col) in enumerate(bars):
    y = len(bars) - 1 - i
    ax.barh(y, hi - lo, left=lo, height=0.5, color=col, alpha=0.35, edgecolor="none")
    ax.plot([mid], [y], "o", color=col, markersize=6, markeredgecolor="white", markeredgewidth=1.2)
    box = dict(boxstyle="square,pad=0.15", fc="white", ec="none")
    ax.text(lo - 3, y, f"${lo:,.0f}", va="center", ha="right", fontsize=8, color=MUTED, bbox=box, zorder=5)
    ax.text(hi + 3, y, f"${hi:,.0f}", va="center", ha="left", fontsize=8, color=MUTED, bbox=box, zorder=5)
ax.set_yticks(range(len(bars)))
ax.set_yticklabels([b[0] for b in reversed(bars)], color=INK)
ax.axvline(price, color=INK, lw=1.5, ls="--")
ax.text(price, len(bars) - 0.45, f"Price ${price:,.2f}", ha="center", va="bottom", fontsize=8, color=INK,
        bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"), zorder=6)
ax.axvline(SBC_ADDBACK, color=MUTED, lw=1, ls=":")
ax.text(SBC_ADDBACK, len(bars) - 0.45, f"DCF, SBC added back ${SBC_ADDBACK:,.0f}", ha="center", va="bottom",
        fontsize=7.5, color=MUTED, bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"), zorder=6)
ax.set_xlim(140, 350)
ax.set_ylim(-0.6, len(bars) + 0.05)
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(LINE)
ax.tick_params(axis="y", length=0)
ax.tick_params(axis="x", colors=MUTED)
ax.grid(axis="x", color=LINE, lw=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
CHART.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(CHART, dpi=200)
plt.close(fig)

# ---------------------------------------------------------------- styles
NAVY = colors.HexColor("#1F3864")
BLUEC = colors.HexColor("#1d5fc2")
GREY = colors.HexColor("#5a6474")
RULE = colors.HexColor("#dde2e9")
SOFT = colors.HexColor("#f4f6f9")
base_style = ParagraphStyle("b", fontName="Helvetica", fontSize=9, leading=12.2, textColor=colors.HexColor("#121821"))
S = {
    "title": ParagraphStyle("t", parent=base_style, fontName="Helvetica-Bold", fontSize=17, leading=21),
    "call": ParagraphStyle("c", parent=base_style, fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=BLUEC),
    "sub": ParagraphStyle("s", parent=base_style, fontSize=8, textColor=GREY),
    "h": ParagraphStyle("h", parent=base_style, fontName="Helvetica-Bold", fontSize=10.5, leading=13,
                        spaceBefore=8, spaceAfter=3, textColor=NAVY),
    "body": base_style,
    "bullet": ParagraphStyle("bl", parent=base_style, leftIndent=11, bulletIndent=0, spaceAfter=2.5),
    "small": ParagraphStyle("sm", parent=base_style, fontSize=7.2, leading=9.2, textColor=GREY),
    "cell": ParagraphStyle("ce", parent=base_style, fontSize=8, leading=10),
}


def P(t, s="body"):
    return Paragraph(t, S[s])


def bullets(items):
    return [Paragraph(t, S["bullet"], bulletText="•") for t in items]


def table(data, widths, bold_rows=(), italic_rows=(), align_right_from=1, header=True):
    t = Table(data, colWidths=widths, hAlign="LEFT")
    st = [
        ("FONT", (0, 0), (-1, -1), "Helvetica", 8),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#121821")),
        ("ALIGN", (align_right_from, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]
    if header:
        st += [("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 7.6), ("TEXTCOLOR", (0, 0), (-1, 0), GREY),
               ("LINEBELOW", (0, 0), (-1, 0), 0.8, NAVY)]
    for r in bold_rows:
        st.append(("FONT", (0, r), (-1, r), "Helvetica-Bold", 8))
    for r in italic_rows:
        st += [("FONT", (0, r), (-1, r), "Helvetica-Oblique", 8), ("TEXTCOLOR", (0, r), (-1, r), GREY)]
    t.setStyle(TableStyle(st))
    return t


def m(v):
    return f"${v:,.2f}"


# ---------------------------------------------------------------- page 1
story = []
story.append(P("Salesforce (NYSE: CRM)", "title"))
story.append(P(f"{rating} &nbsp;·&nbsp; Price target ${target:,.0f} &nbsp;·&nbsp; Price {m(price)} on {priced_on} "
               f"&nbsp;·&nbsp; {upside:+.1%} to target", "call"))
story.append(P("Equity pitch from a three-statement model and DCF built on Salesforce's SEC filings. "
               "Educational project, not investment advice.", "sub"))
story.append(Spacer(1, 6))

stats = [["Market cap", "Enterprise value", "FY27E revenue", "Backlog (RPO)", "Net debt", "WACC"],
         [f"${mcap/1000:,.0f}B", f"${ev/1000:,.0f}B", f"${rev27/1000:,.1f}B (+{rev27/rev26-1:.0%})", "$72.4B (+14%)",
          f"${-bridge/1000:,.1f}B", f"{wacc:.1%}"]]
st = Table(stats, colWidths=[1.12 * inch] * 6, hAlign="LEFT")
st.setStyle(TableStyle([
    ("FONT", (0, 0), (-1, 0), "Helvetica", 7), ("TEXTCOLOR", (0, 0), (-1, 0), GREY),
    ("FONT", (0, 1), (-1, 1), "Helvetica-Bold", 10), ("BACKGROUND", (0, 0), (-1, -1), SOFT),
    ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("LINEAFTER", (0, 0), (-2, -1), 0.5, colors.white),
]))
story.append(st)

story.append(P("The call", "h"))
story.append(P(
    f"Salesforce is roughly fairly priced. My base-case DCF values it at <b>{m(target)}</b>, {abs(upside):.1%} below "
    f"the {m(price)} share price, and even the upside case ({m(up)}) falls short of the +15% a Buy needs. "
    "The business is high quality, with most of next year's revenue already under contract and reported margins set to "
    "rise, but at today's price the market is already paying for that. The upside depends on Agentforce "
    "reaccelerating growth, which my base case does not assume."))

story.append(P("Thesis", "h"))
story += bullets([
    "<b>Most of next year's revenue is already signed.</b> $72.4B of remaining performance obligations at FY26 "
    "year-end, $35.1B due within twelve months. The model builds revenue from that backlog and reproduces FY27 "
    "guidance ($46.1–46.4B).",
    "<b>Reported profits rise as old deals finish amortizing.</b> Acquired-intangible amortization falls from "
    "~$1.9B to ~$0.5B by FY31, lifting GAAP operating margin from 20% to 28% with no change in the business.",
    "<b>Agentforce is upside, not base case.</b> Bookings growth fades from 12% to 8% in the base case. A "
    f"reacceleration is what the upside case ({m(up)}) prices.",
])

story.append(P("Valuation range", "h"))
story.append(Image(str(CHART), width=7.0 * inch, height=7.0 * inch * 2.7 / 7.2))
story.append(P("Bars show low–high; dots the midpoint. Comps use Oct 28, 2026 closes and MarketScreener consensus; "
               "the DCF counts stock-based compensation as a cost, peer EBITDA multiples do not.", "small"))

story.append(P("What would change the rating", "h"))
story += bullets([
    f"<b>Price:</b> holding the {m(target)} target, the rating becomes Buy below ${buy_below:,.0f} and Sell above "
    f"${sell_above:,.0f}.",
    "<b>Fundamentals:</b> current RPO growth well above the ~14% guided for Q3 would point to the upside case; a "
    "slowdown like ServiceNow's would point to the downside case ($176).",
])

story.append(PageBreak())

# ---------------------------------------------------------------- page 2
story.append(P("The key debate: is stock-based compensation a real cost?", "h"))
story.append(P(
    f"Salesforce pays about 8% of revenue (~$3.8B in FY27) in stock. Most sell-side models add it back to free cash "
    f"flow because no cash leaves the company. I don't: every share issued to employees is a smaller slice for "
    f"existing owners, and buybacks partly exist to offset that dilution. The choice is worth about "
    f"<b>${SBC_ADDBACK - target:,.0f} a share</b>: {m(target)} with stock comp as a cost, {m(SBC_ADDBACK)} if it is "
    "added back. It is also the main reason peers' multiples imply more than my DCF."))

story.append(P("Risks", "h"))
story += bullets([
    "<b>Debt-funded buyback.</b> ~$24.8B borrowed to buy back $25B of stock took total debt from $14.4B to $39.3B. "
    "Buying near today's price creates little value if the stock is worth ~$228, and the debt now carries interest.",
    "<b>Integrating Informatica.</b> Adds roughly 3 points to FY27 growth. If customers churn, that growth fades while "
    "the amortization charges remain.",
    "<b>The multiple shrinks as growth slows.</b> Growth slows from ~11% to ~9%; the model already assumes EV/EBITDA "
    "falls from 18.4x today to 13x. A faster de-rating costs about $32 a share per 2x of multiple.",
])

story.append(P("Scenarios", "h"))
sc = [["", "Downside", "Base", "Upside"],
      ["Story", "Bookings stall; AI costs\nsqueeze margins", "Guidance holds; ~50 bp/yr\nsales efficiency",
       "Agentforce lifts bookings"],
      ["Value per share (DCF)", m(down), m(base), m(up)],
      ["vs. price", f"{snap['B'][1]:+.1%}", f"{snap['C'][1]:+.1%}", f"{snap['D'][1]:+.1%}"],
      ["FY31 revenue", f"${snap['B'][3]/1000:,.1f}B", f"${snap['C'][3]/1000:,.1f}B", f"${snap['D'][3]/1000:,.1f}B"],
      ["FY31 GAAP operating margin", f"{snap['B'][4]:.1%}", f"{snap['C'][4]:.1%}", f"{snap['D'][4]:.1%}"],
      ["FY31 unlevered FCF (in DCF)", f"${snap['B'][6]/1000:,.1f}B", f"${snap['C'][6]/1000:,.1f}B",
       f"${snap['D'][6]/1000:,.1f}B"]]
sc[1] = [sc[1][0]] + [Paragraph(x.replace("\n", " "), S["cell"]) for x in sc[1][1:]]
story.append(table(sc, [1.9 * inch, 1.75 * inch, 1.75 * inch, 1.75 * inch], bold_rows=(2,)))

story.append(P("Trading comps", "h"))
rows = [["Company", "EV / NTM revenue", "EV / NTM EBITDA", "NTM P/E", "NTM revenue growth"]]
order = ["NOW", "ORCL", "ADBE", "WDAY", "SAP"]
names = {r["ticker"]: f"{r['company']} ({r['ticker']})" for r in comps}
for t in order:
    r = next(x for x in comps if x["ticker"] == t)
    rows.append([names[t], f"{num(r,'ev_ntm_revenue'):.1f}x", f"{num(r,'ev_ntm_ebitda'):.1f}x",
                 f"{num(r,'ntm_pe'):.1f}x", f"{num(r,'ntm_revenue_growth'):.1%}"])
med = lambda k: statistics.median(num(p, k) for p in peers)
rows.append(["Peer median", f"{med('ev_ntm_revenue'):.1f}x", f"{med('ev_ntm_ebitda'):.1f}x", f"{med('ntm_pe'):.1f}x",
             f"{med('ntm_revenue_growth'):.1%}"])
rows.append([names["CRM"], f"{num(crm,'ev_ntm_revenue'):.1f}x", f"{num(crm,'ev_ntm_ebitda'):.1f}x",
             f"{num(crm,'ntm_pe'):.1f}x", f"{num(crm,'ntm_revenue_growth'):.1%}"])
ms = next(x for x in comps if x["ticker"] == "MSFT")
rows.append([names["MSFT"] + ", reference only", f"{num(ms,'ev_ntm_revenue'):.1f}x", f"{num(ms,'ev_ntm_ebitda'):.1f}x",
             f"{num(ms,'ntm_pe'):.1f}x", f"{num(ms,'ntm_revenue_growth'):.1%}"])
story.append(table(rows, [2.35 * inch, 1.2 * inch, 1.2 * inch, 1.0 * inch, 1.35 * inch],
                   bold_rows=(6, 7), italic_rows=(8,)))
story.append(Spacer(1, 3))
story.append(P(
    f"<b>Implied CRM value:</b> peer median {m(min(med_vals))}–{m(max(med_vals))}; growth-matched peers "
    f"({', '.join(p['ticker'] for p in near)}) {m(min(gm_vals))}–{m(max(gm_vals))}. Comps sit above the DCF mainly "
    "because peer EBITDA excludes stock comp, and because ServiceNow and Oracle grow much faster. ServiceNow fell "
    "19–27% on Oct 29 after its results, which would lower the peer median."))

story.append(P("Method", "h"))
story.append(P(
    "Three-statement model from Salesforce's 8-K earnings releases (FY23–Q2 FY27). Subscription revenue = prior "
    "year-end current RPO × conversion ratio; costs as a share of revenue (GAAP), with acquisition amortization on its "
    f"own schedule. Unlevered FCF discounted at {wacc:.1%} WACC (10-year Treasury 4.99%, beta 1.26, ERP 5%); "
    "perpetuity growth 3% is the headline, a calibrated 13x exit multiple the cross-check. The balance sheet balances "
    "in every year and scenario. Full model, comps and notes: github.com/pooja003-cloud (README and docs/model-notes.md)."))
story.append(Spacer(1, 4))
story.append(P(
    "Sources: Salesforce Q4 FY24, Q4 FY26 and Q2 FY27 earnings releases (SEC 8-K Ex. 99.1 / investor relations); "
    "share prices: Oct 28, 2026 closes (Motley Fool, boerse.de, stockanalysis.com); FRED DGS10; Yahoo Finance beta; "
    "MarketScreener consensus estimates. Not investment advice.", "small"))


def frame(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(GREY)
    canvas.drawString(0.6 * inch, 0.45 * inch, f"Salesforce (CRM) equity pitch · priced {priced_on}")
    canvas.drawRightString(letter[0] - 0.6 * inch, 0.45 * inch, f"Page {doc.page} of 2")
    canvas.setStrokeColor(NAVY)
    canvas.setLineWidth(2)
    canvas.line(0.6 * inch, letter[1] - 0.42 * inch, letter[0] - 0.6 * inch, letter[1] - 0.42 * inch)
    canvas.restoreState()


doc = SimpleDocTemplate(str(OUT), pagesize=letter, leftMargin=0.6 * inch, rightMargin=0.6 * inch,
                        topMargin=0.55 * inch, bottomMargin=0.65 * inch,
                        title="Salesforce (CRM) equity pitch", author="Pooja Master")
doc.build(story, onFirstPage=frame, onLaterPages=frame)
print(f"saved {OUT}")
