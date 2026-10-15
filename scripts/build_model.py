import datetime
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter

wb = Workbook()
FONT = "Arial"
BLUE = Font(name=FONT, color="0000FF", size=10)
BLACK = Font(name=FONT, color="000000", size=10)
GREEN = Font(name=FONT, color="008000", size=10)
BOLD = Font(name=FONT, bold=True, size=10)
BOLDW = Font(name=FONT, bold=True, size=10, color="FFFFFF")
TITLE = Font(name=FONT, bold=True, size=14)
ITAL = Font(name=FONT, italic=True, size=9, color="666666")
YELLOW = PatternFill("solid", fgColor="FFFF00")
HEADFILL = PatternFill("solid", fgColor="1F3864")
SECFILL = PatternFill("solid", fgColor="D9E1F2")
FCFILL = PatternFill("solid", fgColor="F2F2F2")
THIN = Side(style="thin", color="000000")

NUM = '#,##0;(#,##0);"-"'
NUM1 = '#,##0.0;(#,##0.0);"-"'
PCT = '0.0%;(0.0%);"-"'
MULT = '0.00"x"'
MULT1 = '0.0"x"'
USD = '$#,##0.00;($#,##0.00);"-"'
DATEF = 'mmm d, yyyy'

COLS = list("BCDEFGHIJ")
HIST = list("BCDE")
FC = list("FGHIJ")
YEARS = ["FY2023A", "FY2024A", "FY2025A", "FY2026A", "FY2027E", "FY2028E", "FY2029E", "FY2030E", "FY2031E"]


def prev(c):
    return chr(ord(c) - 1)


def ws_setup(ws, title, subtitle=None, years=True, hdr_row=4):
    ws.sheet_view.showGridLines = False
    ws["A1"] = title
    ws["A1"].font = TITLE
    if subtitle:
        ws["A2"] = subtitle
        ws["A2"].font = ITAL
    ws.column_dimensions["A"].width = 52
    for c in COLS:
        ws.column_dimensions[c].width = 12.5
    if years:
        ws[f"A{hdr_row}"] = "($ in millions, FY ends Jan 31)"
        ws[f"A{hdr_row}"].font = BOLDW
        ws[f"A{hdr_row}"].fill = HEADFILL
        for c, y in zip(COLS, YEARS):
            cell = ws[f"{c}{hdr_row}"]
            cell.value = y
            cell.font = BOLDW
            cell.fill = HEADFILL
            cell.alignment = Alignment(horizontal="right")
        ws.freeze_panes = f"B{hdr_row + 1}"


def put(ws, ref, val, font=BLACK, fmt=None, fill=None, bold=False, comment=None):
    cell = ws[ref]
    cell.value = val
    f = font
    if bold:
        f = Font(name=FONT, color=font.color, bold=True, size=10)
    cell.font = f
    if fmt:
        cell.number_format = fmt
    if fill:
        cell.fill = fill
    if comment:
        cell.comment = Comment(comment, "Model")
    return cell


def label(ws, row, text, bold=False, indent=0, section=False):
    cell = ws[f"A{row}"]
    cell.value = ("   " * indent) + text
    cell.font = BOLD if (bold or section) else BLACK
    if section:
        for c in ["A"] + COLS:
            ws[f"{c}{row}"].fill = SECFILL


def row_hist(ws, row, vals, fmt=NUM, cols=HIST, comment=None):
    for c, v in zip(cols, vals):
        if v is None:
            continue
        put(ws, f"{c}{row}", v, BLUE, fmt)
    if comment:
        ws[f"{cols[0]}{row}"].comment = Comment(comment, "Model")


def row_f(ws, row, fn, cols=FC, fmt=NUM, font=BLACK, bold=False):
    for c in cols:
        put(ws, f"{c}{row}", fn(c, prev(c)), font, fmt, bold=bold)


def total_border(ws, row, cols=COLS):
    for c in cols:
        ws[f"{c}{row}"].border = Border(top=THIN)
        ws[f"{c}{row}"].font = Font(name=FONT, bold=True, size=10, color=ws[f"{c}{row}"].font.color)


# =====================================================================
# COVER
# =====================================================================
cv = wb.active
cv.title = "Cover"

# =====================================================================
# ASSUMPTIONS
# =====================================================================
A = wb.create_sheet("Assumptions")
ws_setup(A, "Salesforce (CRM) - Forecast Assumptions",
         "Blue = hardcoded input. Yellow = key lever. Live rows (black) pick the active scenario with CHOOSE.", hdr_row=6)
A["A4"] = "Scenario selector (1 = Downside, 2 = Base, 3 = Upside)"
A["A4"].font = BOLD
put(A, "B4", 2, BLUE, "0", YELLOW)
put(A, "C4", '=CHOOSE($B$4,"Downside","Base","Upside")', BLACK, bold=True)
for c in HIST:
    A[f"{c}6"].value = None
    A[f"{c}6"].fill = HEADFILL
A.column_dimensions["K"].width = 70
put(A, "K6", "Rationale / source", BOLDW, fill=HEADFILL)


def arow(r, text, vals, fmt=PCT, note=None, key=False, indent=1):
    label(A, r, text, indent=indent)
    for c, v in zip(FC, vals):
        put(A, f"{c}{r}", v, BLUE, fmt, YELLOW if key else None)
    if note:
        put(A, f"K{r}", note, ITAL)


def live(r, text, r_down, fmt=PCT, note=None):
    label(A, r, text, bold=True, indent=1)
    for c in FC:
        put(A, f"{c}{r}", f"=CHOOSE($B$4,{c}{r_down},{c}{r_down+1},{c}{r_down+2})", BLACK, fmt, bold=True)
    if note:
        put(A, f"K{r}", note, ITAL)


label(A, 9, "Revenue drivers", section=True)
arow(10, "Current RPO growth - Downside", [0.09, 0.07, 0.06, 0.05, 0.045], key=True)
arow(11, "Current RPO growth - Base", [0.12, 0.105, 0.10, 0.09, 0.08], key=True,
     note="Q2 FY27 cRPO +14% Y/Y (incl. Informatica); Q3 guide ~14%. Base fades as acquisition lap ends; FY30 ~ mgmt $63B target")
arow(12, "Current RPO growth - Upside", [0.14, 0.13, 0.12, 0.11, 0.10], key=True)
live(13, "Current RPO growth - LIVE", 10)
arow(14, "Next-year sub. revenue / prior-year-end cRPO (x)", [1.257, 1.255, 1.25, 1.25, 1.25], MULT,
     note="Historical: FY24 1.32x, FY25 1.29x, FY26 1.30x. FY27 1.257x reproduces guidance (sub growth slightly >12%)")
arow(15, "cRPO as % of total RPO", [0.485] * 5,
     note="Historical: 50.6% / 48.5% / 47.6% / 48.5% (Jan-23 to Jan-26). Memo only - drives total RPO KPI")
arow(16, "Professional services growth - Downside", [-0.06] * 5)
arow(17, "Professional services growth - Base", [-0.02] * 5, note="PS revenue fell 4.5% FY25 and 3.6% FY26; low strategic priority")
arow(18, "Professional services growth - Upside", [0.02] * 5)
live(19, "Professional services growth - LIVE", 16)

label(A, 21, "Cost structure (GAAP, SBC embedded in each line)", section=True)
arow(22, "Cost of sub & support (% of sub rev) - Downside", [0.185] * 5,
     note="Downside: AI inference/compute costs pressure gross margin")
arow(23, "Cost of sub & support (% of sub rev) - Base", [0.175] * 5, note="Historical: 20.1% / 19.0% / 17.4% / 17.3%")
arow(24, "Cost of sub & support (% of sub rev) - Upside", [0.170] * 5)
live(25, "Cost of sub & support (% of sub rev) - LIVE", 22)
arow(26, "Cost of prof. services (% of PS rev)", [1.15] * 5, note="Historical: 109% / 102% / 110% / 116% - PS runs at a loss")
arow(27, "R&D (% of revenue)", [0.148] * 5, note="Historical: 16.1% / 14.1% / 14.5% / 14.4%; FY27 adds Informatica R&D")
arow(28, "Sales & marketing (% of revenue) - Downside", [0.348, 0.348, 0.346, 0.344, 0.342], key=True)
arow(29, "Sales & marketing (% of revenue) - Base", [0.345, 0.340, 0.335, 0.330, 0.325], key=True,
     note="Historical: 43.1% / 36.9% / 35.0% / 34.5%. Base = ~50bp/yr efficiency")
arow(30, "Sales & marketing (% of revenue) - Upside", [0.343, 0.335, 0.327, 0.319, 0.311], key=True)
live(31, "Sales & marketing (% of revenue) - LIVE", 28)
arow(32, "G&A (% of revenue)", [0.074, 0.073, 0.072, 0.071, 0.070], note="Historical: 8.1% / 7.3% / 7.5% / 7.2%")
arow(33, "Restructuring (% of revenue)", [0.010, 0.005, 0.005, 0.005, 0.005], note="FY26 1.4%; assume tapering")
arow(34, "Stock-based comp (% of revenue) - memo, already in opex", [0.083] * 5,
     note="Historical: 10.5% / 8.0% / 8.4% / 8.5%")
arow(35, "Amortization of acquired intangibles ($mm)", [1900, 1700, 1500, 1200, 900], NUM,
     note="FY26 $1,687mm; Informatica adds a full year in FY27, then roll-off. Capped at remaining balance")
arow(36, "Depreciation (% of beginning PP&E)", [0.20] * 5,
     note="Owned PP&E only. Finance-lease depreciation and lease principal payments are excluded (roughly offset)")
arow(37, "Capex (% of revenue)", [0.015] * 5, note="FY27 guidance: ~1.5% of revenue")
arow(38, "Effective tax rate", [0.223, 0.215, 0.215, 0.215, 0.215], note="FY27 GAAP guidance ~22.3%")
arow(39, "Interest rate on average debt", [0.045] * 5, note="Blend of legacy low-coupon notes and 2026 issuance")
arow(40, "Yield on beginning cash & marketable securities", [0.0375] * 5)

label(A, 42, "Working capital", section=True)
arow(43, "Accounts receivable (days of revenue, DSO)", [126] * 5, NUM,
     note="FY26: 126 days (Jan year-end is peak billing season)")
arow(44, "Capitalized contract costs (% of revenue)", [0.122] * 5, note="FY26: 12.2% (current + noncurrent)")
arow(45, "Prepaid & other current assets (% of revenue)", [0.054] * 5, note="FY26: 5.4%")
arow(46, "AP, accrued & other liabilities (% of revenue)", [0.199] * 5, note="FY26: 19.9%")
arow(47, "Unearned revenue (% of revenue)", [0.585] * 5, key=True,
     note="Historical: 55.4% / 54.5% / 54.7% / 58.6%. Key SaaS cash driver - flows to CFO")

label(A, 49, "Capital allocation", section=True)
arow(50, "Acquisitions ($mm)", [1504, 0, 0, 0, 0], NUM,
     note="FY27 = H1 actual. Contentful & Fin deals pending, prices undisclosed - not included")
arow(51, "Debt issuance ($mm)", [24842, 0, 0, 0, 0], NUM, note="FY27 = H1 actual (funded the $25B ASR)")
arow(52, "Debt repayment ($mm)", [0, 0, 0, 0, 0], NUM, note="Assumes maturities are refinanced")
arow(53, "Share repurchases ($mm)", [28000, None, None, None, None], NUM,
     note="FY27: H1 actual $27.3B incl. $25B ASR + small H2")
arow(54, "Share repurchases (% of free cash flow)", [None, 0.5, 0.5, 0.5, 0.5],
     note="FY28+: half of FCF; remainder builds cash / deleverages")
arow(55, "Dividends ($mm)", [1480, None, None, None, None], NUM, note="Q2 FY27 dividend $364mm x 4")
arow(56, "Dividend growth", [None, 0.05, 0.05, 0.05, 0.05])
arow(57, "Proceeds from employee stock plans ($mm)", [1000] * 5, NUM, note="FY25 $1,540mm; FY26 $1,039mm")
arow(58, "Diluted shares (mm)", [838, None, None, None, None], NUM, note="FY27 guidance: 838mm weighted average")
arow(59, "Annual change in diluted shares", [None, -0.015, -0.015, -0.015, -0.015],
     note="Net of SBC dilution and buybacks")

# =====================================================================
# REVENUE BUILD
# =====================================================================
R = wb.create_sheet("Revenue Build")
ws_setup(R, "Salesforce - RPO-Driven Revenue Build",
         "Subscription revenue = prior year-end current RPO x conversion ratio. cRPO is the bookings engine.")

label(R, 6, "Remaining performance obligation", section=True)
label(R, 7, "Current RPO (cRPO), year-end", indent=1)
row_hist(R, 7, [24600, 27600, 30200, 35100],
         comment="Source: Q4 FY24 and Q4 FY26 earnings releases (8-K Ex. 99.1). Jan-26 includes ~$2.2B Informatica")
row_f(R, 7, lambda c, p: f"={p}7*(1+Assumptions!{c}13)")
label(R, 8, "cRPO growth", indent=2)
row_f(R, 8, lambda c, p: f"={c}7/{p}7-1", cols=COLS[1:], fmt=PCT)
label(R, 9, "Total RPO, year-end", indent=1)
row_hist(R, 9, [48600, 56900, 63400, 72400])
row_f(R, 9, lambda c, p: f"={c}7/Assumptions!{c}15")
label(R, 10, "cRPO as % of total RPO", indent=2)
row_f(R, 10, lambda c, p: f"={c}7/{c}9", cols=COLS, fmt=PCT)

label(R, 12, "Revenue", section=True)
label(R, 13, "Subscription & support revenue", indent=1)
row_hist(R, 13, [29021, 32537, 35679, 39388])
row_f(R, 13, lambda c, p: f"={p}7*Assumptions!{c}14")
label(R, 14, "growth", indent=2)
row_f(R, 14, lambda c, p: f"={c}13/{p}13-1", cols=COLS[1:], fmt=PCT)
label(R, 15, "Conversion: sub revenue / prior-year-end cRPO", indent=2)
row_f(R, 15, lambda c, p: f"={c}13/{p}7", cols=COLS[1:], fmt=MULT)
label(R, 16, "Professional services & other revenue", indent=1)
row_hist(R, 16, [2331, 2320, 2216, 2137])
row_f(R, 16, lambda c, p: f"={p}16*(1+Assumptions!{c}19)")
label(R, 17, "growth", indent=2)
row_f(R, 17, lambda c, p: f"={c}16/{p}16-1", cols=COLS[1:], fmt=PCT)
label(R, 18, "Total revenue", bold=True)
row_f(R, 18, lambda c, p: f"={c}13+{c}16", cols=COLS)
total_border(R, 18)
label(R, 19, "growth", indent=2)
row_f(R, 19, lambda c, p: f"={c}18/{p}18-1", cols=COLS[1:], fmt=PCT)
label(R, 20, "Subscription mix", indent=2)
row_f(R, 20, lambda c, p: f"={c}13/{c}18", cols=COLS, fmt=PCT)

label(R, 22, "Billings (cash view of the top line)", section=True)
label(R, 23, "Unearned revenue, year-end", indent=1)
row_hist(R, 23, [17376, 19003, 20743, 24317])
row_f(R, 23, lambda c, p: f"=BS!{c}19", font=GREEN)
label(R, 24, "Calculated billings = revenue + change in unearned revenue", indent=1)
row_f(R, 24, lambda c, p: f"={c}18+{c}23-{p}23", cols=COLS[1:])
label(R, 25, "billings growth", indent=2)
row_f(R, 25, lambda c, p: f"={c}24/{p}24-1", cols=COLS[2:], fmt=PCT)

label(R, 27, "Guidance check (FY2027)", section=True)
label(R, 28, "FY27 revenue guidance - low / high ($mm)", indent=1)
put(R, "B28", 46100, BLUE, NUM, comment="Q2 FY27 earnings release (Aug 26, 2026): raised to $46.1B-$46.4B")
put(R, "C28", 46400, BLUE, NUM)
label(R, 29, "Model FY27E revenue within guidance?", indent=1)
put(R, "B29", '=IF(AND(F18>=B28,F18<=C28),"YES","OUTSIDE")', BLACK, bold=True)

# =====================================================================
# INCOME STATEMENT
# =====================================================================
I = wb.create_sheet("IS")
ws_setup(I, "Salesforce - Income Statement (GAAP)",
         "Historicals from 8-K earnings releases (Ex. 99.1). Forecast driven by Assumptions and Revenue Build.")

label(I, 5, "Subscription & support revenue", indent=1)
row_f(I, 5, lambda c, p: f"='Revenue Build'!{c}13", cols=COLS, font=GREEN)
label(I, 6, "Professional services & other revenue", indent=1)
row_f(I, 6, lambda c, p: f"='Revenue Build'!{c}16", cols=COLS, font=GREEN)
label(I, 7, "Total revenue", bold=True)
row_f(I, 7, lambda c, p: f"={c}5+{c}6", cols=COLS)
total_border(I, 7)
label(I, 8, "growth", indent=2)
row_f(I, 8, lambda c, p: f"={c}7/{p}7-1", cols=COLS[1:], fmt=PCT)

label(I, 10, "Cost of revenue - subscription & support", indent=1)
row_hist(I, 10, [5821, 6177, 6198, 6796])
row_f(I, 10, lambda c, p: f"={c}5*Assumptions!{c}25")
label(I, 11, "Cost of revenue - professional services", indent=1)
row_hist(I, 11, [2539, 2364, 2445, 2474])
row_f(I, 11, lambda c, p: f"={c}6*Assumptions!{c}26")
label(I, 12, "Total cost of revenue", indent=1)
row_f(I, 12, lambda c, p: f"={c}10+{c}11", cols=COLS)
label(I, 13, "Gross profit", bold=True)
row_f(I, 13, lambda c, p: f"={c}7-{c}12", cols=COLS)
total_border(I, 13)
label(I, 14, "Gross margin", indent=2)
row_f(I, 14, lambda c, p: f"={c}13/{c}7", cols=COLS, fmt=PCT)

label(I, 16, "Research & development", indent=1)
row_hist(I, 16, [5055, 4906, 5493, 5993])
row_f(I, 16, lambda c, p: f"={c}7*Assumptions!{c}27")
label(I, 17, "Sales & marketing", indent=1)
row_hist(I, 17, [13526, 12877, 13257, 14345])
row_f(I, 17, lambda c, p: f"={c}7*Assumptions!{c}31")
label(I, 18, "General & administrative", indent=1)
row_hist(I, 18, [2553, 2534, 2836, 3000])
row_f(I, 18, lambda c, p: f"={c}7*Assumptions!{c}32")
label(I, 19, "Restructuring", indent=1)
row_hist(I, 19, [828, 988, 461, 586])
row_f(I, 19, lambda c, p: f"={c}7*Assumptions!{c}33")
label(I, 20, "Total operating expenses", indent=1)
row_f(I, 20, lambda c, p: f"=SUM({c}16:{c}19)", cols=COLS)
label(I, 21, "Operating income (GAAP EBIT)", bold=True)
row_f(I, 21, lambda c, p: f"={c}13-{c}20", cols=COLS)
total_border(I, 21)
label(I, 22, "GAAP operating margin", indent=2)
row_f(I, 22, lambda c, p: f"={c}21/{c}7", cols=COLS, fmt=PCT)

label(I, 24, "Gains (losses) on strategic investments", indent=1)
row_hist(I, 24, [-239, -277, -121, 1017])
row_f(I, 24, lambda c, p: "=0")
put(I, "K24", "Not forecast - volatile mark-to-market", ITAL)
label(I, 25, "Interest income (on beginning cash + marketable securities)", indent=1)
row_f(I, 25, lambda c, p: f"=Assumptions!{c}40*(BS!{p}5+BS!{p}6)")
label(I, 26, "Interest expense (on average debt)", indent=1)
row_f(I, 26, lambda c, p: f"=-Assumptions!{c}39*AVERAGE(BS!{p}21,BS!{c}21)")
label(I, 27, "Other income (expense), net", indent=1)
row_hist(I, 27, [-131, 216, 354, 172])
row_f(I, 27, lambda c, p: f"={c}25+{c}26")
label(I, 28, "Pre-tax income", bold=True)
row_f(I, 28, lambda c, p: f"={c}21+{c}24+{c}27", cols=COLS)
total_border(I, 28)
label(I, 29, "Provision for income taxes", indent=1)
row_hist(I, 29, [-452, -814, -1241, -2063])
row_f(I, 29, lambda c, p: f"=-{c}28*Assumptions!{c}38")
label(I, 30, "Net income", bold=True)
row_f(I, 30, lambda c, p: f"={c}28+{c}29", cols=COLS)
total_border(I, 30)
label(I, 31, "Net margin", indent=2)
row_f(I, 31, lambda c, p: f"={c}30/{c}7", cols=COLS, fmt=PCT)
label(I, 32, "Effective tax rate", indent=2)
row_f(I, 32, lambda c, p: f"=-{c}29/{c}28", cols=COLS, fmt=PCT)

label(I, 34, "Diluted shares (mm)", indent=1)
row_hist(I, 34, [997, 984, 974, 956])
put(I, "F34", "=Assumptions!F58", GREEN, NUM)
row_f(I, 34, lambda c, p: f"={p}34*(1+Assumptions!{c}59)", cols=FC[1:])
label(I, 35, "Diluted EPS (GAAP, $)", bold=True)
row_f(I, 35, lambda c, p: f"={c}30/{c}34", cols=COLS, fmt=USD)

label(I, 37, "Memo items", section=True)
label(I, 38, "Stock-based compensation (in opex above)", indent=1)
row_hist(I, 38, [3279, 2787, 3183, 3509])
row_f(I, 38, lambda c, p: f"={c}7*Assumptions!{c}34")
label(I, 39, "Amortization of acquired intangibles", indent=1)
row_hist(I, 39, [None, None, 1651, 1687])
row_f(I, 39, lambda c, p: f"=MIN(Assumptions!{c}35,BS!{p}14)")
label(I, 40, "Depreciation (forecast: owned PP&E only; excl. lease ROU amortization)", indent=1)
row_f(I, 40, lambda c, p: f"={c}41-{c}39", cols=["D", "E"])
row_f(I, 40, lambda c, p: f"=Assumptions!{c}36*BS!{p}10")
label(I, 41, "Total D&A", indent=1)
row_hist(I, 41, [3786, 3959, 3477, 3631])
row_f(I, 41, lambda c, p: f"={c}39+{c}40")
label(I, 42, "EBITDA (GAAP EBIT + D&A; SBC treated as expense)", bold=True)
row_f(I, 42, lambda c, p: f"={c}21+{c}41", cols=COLS)
label(I, 43, "Non-GAAP operating income (EBIT + SBC + amortization + restructuring)", indent=1)
row_f(I, 43, lambda c, p: f"={c}21+{c}38+{c}39+{c}19", cols=COLS[2:])
label(I, 44, "Non-GAAP operating margin", indent=2)
row_f(I, 44, lambda c, p: f"={c}43/{c}7", cols=COLS[2:], fmt=PCT)
I.column_dimensions["K"].width = 40

# =====================================================================
# BALANCE SHEET
# =====================================================================
B = wb.create_sheet("BS")
ws_setup(B, "Salesforce - Balance Sheet",
         "FY25A/FY26A from Q4 FY26 release. Some lines combined (current + noncurrent). FY23A/FY24A not shown.")

label(B, 5, "Cash & cash equivalents", indent=1)
row_hist(B, 5, [8848, 7327], cols=["D", "E"])
row_f(B, 5, lambda c, p: f"=CF!{c}30", font=GREEN)
label(B, 6, "Marketable securities", indent=1)
row_hist(B, 6, [5184, 2238], cols=["D", "E"])
row_f(B, 6, lambda c, p: f"={p}6")
label(B, 7, "Accounts receivable, net", indent=1)
row_hist(B, 7, [11945, 14339], cols=["D", "E"])
row_f(B, 7, lambda c, p: f"=IS!{c}7*Assumptions!{c}43/365")
label(B, 8, "Prepaid expenses & other current assets", indent=1)
row_hist(B, 8, [1779, 2243], cols=["D", "E"])
row_f(B, 8, lambda c, p: f"=IS!{c}7*Assumptions!{c}45")
label(B, 9, "Capitalized contract costs (current + noncurrent)", indent=1)
row_hist(B, 9, [4446, 5060], cols=["D", "E"])
row_f(B, 9, lambda c, p: f"=IS!{c}7*Assumptions!{c}44")
label(B, 10, "Property & equipment, net", indent=1)
row_hist(B, 10, [3236, 3120], cols=["D", "E"])
row_f(B, 10, lambda c, p: f"={p}10-CF!{c}16-IS!{c}40")
label(B, 11, "Operating lease right-of-use assets", indent=1)
row_hist(B, 11, [2157, 2003], cols=["D", "E"])
row_f(B, 11, lambda c, p: f"={p}11")
label(B, 12, "Strategic investments", indent=1)
row_hist(B, 12, [4852, 7591], cols=["D", "E"])
row_f(B, 12, lambda c, p: f"={p}12")
label(B, 13, "Goodwill", indent=1)
row_hist(B, 13, [51283, 57941], cols=["D", "E"])
row_f(B, 13, lambda c, p: f"={p}13-CF!{c}17")
label(B, 14, "Intangible assets acquired, net", indent=1)
row_hist(B, 14, [4428, 6815], cols=["D", "E"])
row_f(B, 14, lambda c, p: f"={p}14-IS!{c}39")
label(B, 15, "Deferred tax & other assets", indent=1)
row_hist(B, 15, [4770, 3628], cols=["D", "E"])
row_f(B, 15, lambda c, p: f"={p}15")
label(B, 16, "Total assets", bold=True)
row_f(B, 16, lambda c, p: f"=SUM({c}5:{c}15)", cols=COLS[2:])
total_border(B, 16, COLS[2:])

label(B, 18, "AP, accrued expenses & other liabilities", indent=1)
row_hist(B, 18, [6658, 8253], cols=["D", "E"])
row_f(B, 18, lambda c, p: f"=IS!{c}7*Assumptions!{c}46")
label(B, 19, "Unearned revenue", indent=1)
row_hist(B, 19, [20743, 24317], cols=["D", "E"])
row_f(B, 19, lambda c, p: f"=IS!{c}7*Assumptions!{c}47")
label(B, 20, "Operating lease liabilities (current + noncurrent)", indent=1)
row_hist(B, 20, [2959, 2737], cols=["D", "E"])
row_f(B, 20, lambda c, p: f"={p}20")
label(B, 21, "Total debt (current + noncurrent)", indent=1)
row_hist(B, 21, [8433, 14439], cols=["D", "E"])
row_f(B, 21, lambda c, p: f"={p}21+CF!{c}21+CF!{c}22")
label(B, 22, "Other noncurrent liabilities", indent=1)
row_hist(B, 22, [2962, 3417], cols=["D", "E"])
row_f(B, 22, lambda c, p: f"={p}22")
label(B, 23, "Total liabilities", bold=True)
row_f(B, 23, lambda c, p: f"=SUM({c}18:{c}22)", cols=COLS[2:])
total_border(B, 23, COLS[2:])

label(B, 25, "Paid-in capital, common stock & AOCI", indent=1)
row_hist(B, 25, [64311, 69149], cols=["D", "E"])
row_f(B, 25, lambda c, p: f"={p}25+IS!{c}38+CF!{c}25")
label(B, 26, "Treasury stock", indent=1)
row_hist(B, 26, [-19507, -32228], cols=["D", "E"])
row_f(B, 26, lambda c, p: f"={p}26+CF!{c}23")
label(B, 27, "Retained earnings", indent=1)
row_hist(B, 27, [16369, 22221], cols=["D", "E"])
row_f(B, 27, lambda c, p: f"={p}27+IS!{c}30+CF!{c}24")
label(B, 28, "Total stockholders' equity", bold=True)
row_f(B, 28, lambda c, p: f"=SUM({c}25:{c}27)", cols=COLS[2:])
total_border(B, 28, COLS[2:])
label(B, 29, "Total liabilities & equity", bold=True)
row_f(B, 29, lambda c, p: f"={c}23+{c}28", cols=COLS[2:])

label(B, 31, "BALANCE CHECK (assets - liabilities - equity; must be 0)", bold=True)
row_f(B, 31, lambda c, p: f"=ROUND({c}16-{c}29,3)", cols=COLS[2:], fmt='#,##0.000;(#,##0.000);"OK"', bold=True)
label(B, 33, "Memo: net cash / (net debt) incl. marketable securities", indent=1)
row_f(B, 33, lambda c, p: f"={c}5+{c}6-{c}21", cols=COLS[2:])
label(B, 34, "Memo: total debt / EBITDA", indent=1)
row_f(B, 34, lambda c, p: f"={c}21/IS!{c}42", cols=COLS[2:], fmt=MULT1)

# =====================================================================
# CASH FLOW
# =====================================================================
C = wb.create_sheet("CF")
ws_setup(C, "Salesforce - Cash Flow Statement",
         "Historicals show key lines only; 'other operating' is the reconciling item to reported CFO.")

label(C, 5, "Net income", indent=1)
row_f(C, 5, lambda c, p: f"=IS!{c}30", cols=COLS, font=GREEN)
label(C, 6, "Depreciation & amortization", indent=1)
row_f(C, 6, lambda c, p: f"=IS!{c}41", cols=COLS, font=GREEN)
label(C, 7, "Stock-based compensation (non-cash add-back)", indent=1)
row_f(C, 7, lambda c, p: f"=IS!{c}38", cols=COLS, font=GREEN)
label(C, 8, "(Increase) / decrease in accounts receivable", indent=1)
row_f(C, 8, lambda c, p: f"=BS!{p}7-BS!{c}7")
label(C, 9, "(Increase) / decrease in prepaid & other", indent=1)
row_f(C, 9, lambda c, p: f"=BS!{p}8-BS!{c}8")
label(C, 10, "(Increase) / decrease in capitalized contract costs", indent=1)
row_f(C, 10, lambda c, p: f"=BS!{p}9-BS!{c}9")
label(C, 11, "Increase / (decrease) in AP & accrued", indent=1)
row_f(C, 11, lambda c, p: f"=BS!{c}18-BS!{p}18")
label(C, 12, "Increase / (decrease) in unearned revenue", indent=1)
row_hist(C, 12, [1744, 1623, 1584, 2924])
row_f(C, 12, lambda c, p: f"=BS!{c}19-BS!{p}19")
label(C, 13, "Other operating items, net (historical reconciling item)", indent=1)
row_f(C, 13, lambda c, p: f"={c}15-SUM({c}5:{c}12)", cols=HIST)
row_f(C, 13, lambda c, p: "=0")
label(C, 14, "Cash from operations (CFO)", bold=True)
row_f(C, 14, lambda c, p: f"=SUM({c}5:{c}13)", cols=COLS)
total_border(C, 14)
label(C, 15, "Memo: reported CFO", indent=2)
row_hist(C, 15, [7111, 10234, 13092, 14996])
C["A15"].font = ITAL

label(C, 16, "Capital expenditures", indent=1)
row_hist(C, 16, [-798, -736, -658, -594])
row_f(C, 16, lambda c, p: f"=-IS!{c}7*Assumptions!{c}37")
label(C, 17, "Acquisitions, net of cash", indent=1)
row_hist(C, 17, [None, None, -2734, -9268])
row_f(C, 17, lambda c, p: f"=-Assumptions!{c}50")
label(C, 18, "Net (purchases) / sales of investments", indent=1)
row_f(C, 18, lambda c, p: f"=(BS!{p}6-BS!{c}6)+(BS!{p}12-BS!{c}12)")
label(C, 19, "Cash from investing (CFI)", bold=True)
row_f(C, 19, lambda c, p: f"=SUM({c}16:{c}18)")
total_border(C, 19, FC)

label(C, 21, "Debt issuance", indent=1)
row_hist(C, 21, [None, None, 0, 6000])
row_f(C, 21, lambda c, p: f"=Assumptions!{c}51")
label(C, 22, "Debt repayment", indent=1)
row_hist(C, 22, [None, None, -1000, 0])
row_f(C, 22, lambda c, p: f"=-Assumptions!{c}52")
label(C, 23, "Share repurchases", indent=1)
row_hist(C, 23, [-4000, -7620, -7829, -12596])
put(C, "F23", "=-Assumptions!F53", BLACK, NUM)
row_f(C, 23, lambda c, p: f"=-Assumptions!{c}54*MAX({c}32,0)", cols=FC[1:])
label(C, 24, "Dividends", indent=1)
row_hist(C, 24, [0, 0, -1537, -1587])
put(C, "F24", "=-Assumptions!F55", BLACK, NUM)
row_f(C, 24, lambda c, p: f"={p}24*(1+Assumptions!{c}56)", cols=FC[1:])
label(C, 25, "Proceeds from employee stock plans", indent=1)
row_hist(C, 25, [None, None, 1540, 1039])
row_f(C, 25, lambda c, p: f"=Assumptions!{c}57")
label(C, 26, "Cash from financing (CFF)", bold=True)
row_f(C, 26, lambda c, p: f"=SUM({c}21:{c}25)")
total_border(C, 26, FC)

label(C, 28, "Net change in cash", bold=True)
row_f(C, 28, lambda c, p: f"={c}14+{c}19+{c}26")
label(C, 29, "Beginning cash", indent=1)
row_f(C, 29, lambda c, p: f"=BS!{p}5", font=GREEN)
label(C, 30, "Ending cash", bold=True)
row_f(C, 30, lambda c, p: f"={c}29+{c}28")
total_border(C, 30, FC)

label(C, 32, "Free cash flow (CFO - capex)", bold=True)
row_f(C, 32, lambda c, p: f"={c}14+{c}16", cols=COLS)
label(C, 33, "FCF margin", indent=2)
row_f(C, 33, lambda c, p: f"={c}32/IS!{c}7", cols=COLS, fmt=PCT)
label(C, 34, "FCF growth", indent=2)
row_f(C, 34, lambda c, p: f"={c}32/{p}32-1", cols=COLS[1:], fmt=PCT)
label(C, 35, "FCF after SBC (treating SBC as a cash cost)", indent=1)
row_f(C, 35, lambda c, p: f"={c}32-{c}7", cols=COLS)

# =====================================================================
# DCF
# =====================================================================
D = wb.create_sheet("DCF")
ws_setup(D, "Salesforce - Unlevered DCF Valuation",
         "Mid-year convention. FY27 includes only the cash flow after the Jul-31-2026 balance sheet date.", years=False)
D.column_dimensions["A"].width = 58
D.column_dimensions["K"].width = 60


def dput(r, text, val, fmt=NUM, inp=False, note=None, bold=False, key=False):
    label(D, r, text, bold=bold, indent=0 if bold else 1)
    put(D, f"B{r}", val, BLUE if inp else BLACK, fmt, YELLOW if key else None, bold=bold)
    if note:
        put(D, f"K{r}", note, ITAL)


label(D, 4, "Market & balance sheet inputs", section=True)
dput(5, "Valuation date", datetime.date(2026, 10, 14), DATEF, True)
dput(6, "Share price ($)", 235.95, USD, True, "NYSE close Oct 14, 2026 (stockanalysis.com)")
dput(7, "Basic shares outstanding (mm)", 823, NUM, True, "Post-ASR; stockanalysis.com Oct 2026")
dput(8, "Dilutive securities (mm)", 7, NUM, True, "Estimate for RSUs/options (treasury method)")
dput(9, "Diluted shares (mm)", "=B7+B8", NUM, bold=True)
dput(10, "Balance sheet date for net debt", datetime.date(2026, 7, 31), DATEF, True, "Latest 10-Q: Q2 FY27")
dput(11, "Cash & cash equivalents", 8310, NUM, True, "Q2 FY27 balance sheet")
dput(12, "Marketable securities", 3093, NUM, True, "Q2 FY27 balance sheet")
dput(13, "Strategic investments (book)", 11324, NUM, True, "Q2 FY27 balance sheet; mostly private stakes")
dput(14, "Haircut on strategic investments", 0.20, PCT, True, "Illiquid private holdings - conservative haircut", key=True)
dput(15, "Total debt", 39288, NUM, True, "Q2 FY27: $0 current + $39,288mm noncurrent (post-ASR)")
dput(16, "Treat SBC as a real cost? (1 = yes, 0 = add back)", 1, "0", True,
     "1 = do NOT add SBC back to FCF (conservative, dilution is real). 0 = sell-side style add-back", key=True)

label(D, 18, "Discount rate (WACC)", section=True)
dput(19, "Risk-free rate (10Y UST)", 0.052, PCT, True, "10Y Treasury ~5.19-5.24%, Oct 9-13, 2026")
dput(20, "Equity risk premium", 0.05, PCT, True, "Damodaran-style implied ERP range 4.5-5.5%")
dput(21, "Levered beta", 1.26, '0.00', True, "5Y monthly beta, stockanalysis.com")
dput(22, "Cost of equity (CAPM)", "=B19+B21*B20", PCT, bold=True)
dput(23, "Pre-tax cost of debt", 0.055, PCT, True, "~Rf + 30bp spread for A-rated issuer")
dput(24, "Tax rate", 0.21, PCT, True, "US federal statutory")
dput(25, "After-tax cost of debt", "=B23*(1-B24)", PCT)
dput(26, "Market value of equity", "=B6*B9", NUM)
dput(27, "Debt", "=B15", NUM)
dput(28, "Equity weight", "=B26/(B26+B27)", PCT)
dput(29, "Debt weight", "=B27/(B26+B27)", PCT)
dput(30, "WACC", "=B28*B22+B29*B25", PCT, bold=True, key=True)

label(D, 32, "Terminal value inputs", section=True)
dput(33, "Perpetuity growth rate", 0.03, PCT, True, key=True, note="Nominal; below long-run nominal GDP")
dput(34, "Exit EV / EBITDA multiple (on FY31 GAAP EBITDA)", 16.0, MULT1, True, key=True,
     note="CRM trades ~17-18x FY27E GAAP EBITDA today; assume some compression by FY31")
dput(35, "Weight on perpetuity method in blended value", 0.5, PCT, True)

# FCF build
hdr = 37
put(D, f"A{hdr}", "Unlevered free cash flow ($mm)", BOLDW, fill=HEADFILL)
for c, y in zip(FC, YEARS[4:]):
    put(D, f"{c}{hdr}", y, BOLDW, fill=HEADFILL)
    D[f"{c}{hdr}"].alignment = Alignment(horizontal="right")
for c in "BCDE":
    D[f"{c}{hdr}"].fill = HEADFILL

label(D, 38, "Fiscal year-end date", indent=1)
for i, c in enumerate(FC):
    put(D, f"{c}38", f"=DATE({2027 + i},1,31)", BLACK, DATEF)
label(D, 39, "Revenue", indent=1)
row_f(D, 39, lambda c, p: f"=IS!{c}7", font=GREEN)
label(D, 40, "EBIT (GAAP, after SBC expense)", indent=1)
row_f(D, 40, lambda c, p: f"=IS!{c}21", font=GREEN)
label(D, 41, "Less: taxes on EBIT", indent=1)
row_f(D, 41, lambda c, p: f"=-{c}40*Assumptions!{c}38")
label(D, 42, "NOPAT", bold=True)
row_f(D, 42, lambda c, p: f"={c}40+{c}41")
label(D, 43, "Plus: D&A", indent=1)
row_f(D, 43, lambda c, p: f"=IS!{c}41", font=GREEN)
label(D, 44, "Plus: SBC add-back (only if B16 = 0)", indent=1)
row_f(D, 44, lambda c, p: f"=IS!{c}38*(1-$B$16)")
label(D, 45, "Less: capex", indent=1)
row_f(D, 45, lambda c, p: f"=CF!{c}16", font=GREEN)
label(D, 46, "Less: increase in net working capital", indent=1)
row_f(D, 46, lambda c, p: f"=SUM(CF!{c}8:{c}12)", font=GREEN)
label(D, 47, "Unlevered free cash flow", bold=True)
row_f(D, 47, lambda c, p: f"=SUM({c}42:{c}46)", bold=True)
total_border(D, 47, FC)
label(D, 48, "UFCF margin", indent=2)
row_f(D, 48, lambda c, p: f"={c}47/{c}39", fmt=PCT)
label(D, 49, "Fraction of year included", indent=1)
put(D, "F49", "=(F38-$B$10)/365", BLACK, '0.000')
row_f(D, 49, lambda c, p: "=1", cols=FC[1:], fmt='0.000')
label(D, 50, "UFCF included", indent=1)
row_f(D, 50, lambda c, p: f"={c}47*{c}49")
label(D, 51, "Discount period (mid-period, years from valuation date)", indent=1)
row_f(D, 51, lambda c, p: f"=MAX(({c}38-$B$5)/365-{c}49/2,0)", fmt='0.000')
label(D, 52, "Discount factor", indent=1)
row_f(D, 52, lambda c, p: f"=1/(1+$B$30)^{c}51", fmt='0.0000')
label(D, 53, "PV of UFCF", bold=True)
row_f(D, 53, lambda c, p: f"={c}50*{c}52")

label(D, 55, "Terminal value", section=True)
dput(56, "Sum of PV of UFCF", "=SUM(F53:J53)")
dput(57, "Years from valuation date to end of FY31", "=(J38-B5)/365", '0.000')
dput(58, "Terminal UFCF (FY31 x (1 + g))", "=J47*(1+B33)")
dput(59, "Terminal value - perpetuity growth", "=B58/(B30-B33)")
dput(60, "Terminal value - exit multiple", "=IS!J42*B34")
dput(61, "PV of terminal value - perpetuity", "=B59/(1+B30)^B57")
dput(62, "PV of terminal value - exit multiple", "=B60/(1+B30)^B57")
dput(63, "Implied exit EV/EBITDA from perpetuity method", "=B59/IS!J42", MULT1)
dput(64, "Implied perpetuity growth from exit multiple", "=(B60*B30-J47)/(B60+J47)", PCT)

# Bridge
put(D, "A66", "Enterprise value to equity value bridge", BOLDW, fill=HEADFILL)
for c, t in zip("BCD", ["Perpetuity", "Exit multiple", "Blended"]):
    put(D, f"{c}66", t, BOLDW, fill=HEADFILL)
    D[f"{c}66"].alignment = Alignment(horizontal="right")
rows = [
    (67, "Enterprise value", ["=$B$56+$B$61", "=$B$56+$B$62", "=$B$35*B67+(1-$B$35)*C67"], NUM),
    (68, "Plus: cash & equivalents", ["=$B$11"] * 3, NUM),
    (69, "Plus: marketable securities", ["=$B$12"] * 3, NUM),
    (70, "Plus: strategic investments (after haircut)", ["=$B$13*(1-$B$14)"] * 3, NUM),
    (71, "Less: total debt", ["=-$B$15"] * 3, NUM),
    (72, "Equity value", ["=SUM(B67:B71)", "=SUM(C67:C71)", "=SUM(D67:D71)"], NUM),
    (73, "Diluted shares (mm)", ["=$B$9"] * 3, NUM),
    (74, "Implied value per share ($)", ["=B72/B73", "=C72/C73", "=D72/D73"], USD),
    (75, "Current share price ($)", ["=$B$6"] * 3, USD),
    (76, "Upside / (downside)", ["=B74/B75-1", "=C74/C75-1", "=D74/D75-1"], PCT),
    (77, "Terminal value as % of EV", ["=$B$61/B67", "=$B$62/C67", "=($B$35*$B$61+(1-$B$35)*$B$62)/D67"], PCT),
]
for r, t, fs, fmt in rows:
    label(D, r, t, bold=r in (67, 72, 74), indent=0 if r in (67, 72, 74) else 1)
    for c, f in zip("BCD", fs):
        put(D, f"{c}{r}", f, BLACK, fmt, bold=r in (72, 74))
for c in "BCD":
    D[f"{c}72"].border = Border(top=THIN)
    D[f"{c}74"].fill = YELLOW

NETCASH = "($B$11+$B$12+$B$13*(1-$B$14)-$B$15)"


def sens(top, title, colvals, colfmt, tv_expr):
    put(D, f"A{top}", title, BOLDW, fill=HEADFILL)
    for c in "BCDEF":
        D[f"{c}{top}"].fill = HEADFILL
    put(D, f"A{top+1}", "WACC (down) / " + ("growth" if "growth" in title else "exit multiple") + " (across)", ITAL)
    for c, v in zip("BCDEF", colvals):
        put(D, f"{c}{top+1}", v, BOLD, colfmt)
    for i, dw in enumerate([-0.01, -0.005, 0, 0.005, 0.01]):
        r = top + 2 + i
        put(D, f"A{r}", f"=$B$30+({dw})", BOLD, PCT)
        D[f"A{r}"].alignment = Alignment(horizontal="right")
        for c in "BCDEF":
            w = f"$A{r}"
            x = f"{c}${top+1}"
            f = (f"=(SUMPRODUCT($F$50:$J$50,1/(1+{w})^$F$51:$J$51)"
                 f"+{tv_expr.format(w=w, x=x)}/(1+{w})^$B$57+{NETCASH})/$B$9")
            put(D, f"{c}{r}", f, BLACK, USD)
            if dw == 0 and c == "D":
                D[f"{c}{r}"].fill = YELLOW


sens(80, "Sensitivity: value per share - perpetuity growth method",
     ["=$B$33-0.01", "=$B$33-0.005", "=$B$33", "=$B$33+0.005", "=$B$33+0.01"], PCT,
     "$J$47*(1+{x})/({w}-{x})")
sens(89, "Sensitivity: value per share - exit multiple method",
     ["=$B$34-4", "=$B$34-2", "=$B$34", "=$B$34+2", "=$B$34+4"], MULT1,
     "IS!$J$42*{x}")

# =====================================================================
# SOURCES
# =====================================================================
S = wb.create_sheet("Sources")
S.sheet_view.showGridLines = False
S.column_dimensions["A"].width = 46
S.column_dimensions["B"].width = 110
put(S, "A1", "Sources", TITLE)
src = [
    ("FY2026 & FY2025 financial statements, RPO, FY27 initial guidance",
     "Salesforce Q4 FY26 earnings release, 8-K Ex. 99.1 (Feb 25, 2026): https://www.sec.gov/Archives/edgar/data/1108524/000110852426000056/crm-q4fy26xexhibit991.htm"),
    ("FY2024 & FY2023 financial statements, RPO",
     "Salesforce Q4 FY24 earnings release, 8-K Ex. 99.1 (Feb 28, 2024): https://www.sec.gov/Archives/edgar/data/1108524/000110852424000002/crm-q4fy24xexhibit991.htm"),
    ("Q2 FY27 balance sheet (Jul 31, 2026), ASR, debt, raised FY27 guidance",
     "Salesforce Q2 FY27 earnings release (Aug 26, 2026): https://investor.salesforce.com/files/doc_financials/2027/q2/CRM-Q2-FY27-Earnings-Press-Release.pdf"),
    ("Share price, shares outstanding, beta", "stockanalysis.com/stocks/crm (close Oct 14, 2026)"),
    ("10-year Treasury yield", "themortgagereports.com (Oct 13, 2026: 5.19%); etfdb.com (Oct 9, 2026: 5.24%)"),
    ("", ""),
    ("Combined balance sheet lines", "Capitalized contract costs, operating lease liabilities and debt combine current + noncurrent. "
     "'Paid-in capital, common stock & AOCI' = common stock + APIC + AOCI."),
    ("Not verified from primary source", "Strategic-investment haircut, ERP, cost of debt, dilutive securities and all forecast "
     "drivers are analyst judgment - change them on Assumptions / DCF."),
]
for i, (a, b) in enumerate(src, start=3):
    put(S, f"A{i}", a, BOLD)
    put(S, f"B{i}", b, BLACK)
    S[f"B{i}"].alignment = Alignment(wrap_text=True, vertical="top")
    S[f"A{i}"].alignment = Alignment(wrap_text=True, vertical="top")

# =====================================================================
# COVER content
# =====================================================================
cv.sheet_view.showGridLines = False
cv.column_dimensions["A"].width = 50
for c in "BCDE":
    cv.column_dimensions[c].width = 16
put(cv, "A1", "Salesforce, Inc. (NYSE: CRM) - 3-Statement Model & DCF", TITLE)
put(cv, "A2", "Built Oct 14, 2026. Base year FY2026A (Jan 31, 2026); forecast FY2027E-FY2031E. $ in millions.", ITAL)

put(cv, "A4", "Key outputs (live scenario)", BOLDW, fill=HEADFILL)
for c in "BCD":
    cv[f"{c}4"].fill = HEADFILL
outs = [
    ("Active scenario", "=Assumptions!C4", None),
    ("Implied value per share - blended ($)", "=DCF!D74", USD),
    ("Implied value per share - perpetuity ($)", "=DCF!B74", USD),
    ("Implied value per share - exit multiple ($)", "=DCF!C74", USD),
    ("Current share price ($)", "=DCF!B6", USD),
    ("Upside / (downside) - blended", "=DCF!D76", PCT),
    ("WACC", "=DCF!B30", PCT),
    ("FY27E revenue / within guidance?", "=IS!F7", NUM),
    ("FY31E revenue", "=IS!J7", NUM),
    ("FY26A-FY31E revenue CAGR", "=(IS!J7/IS!E7)^(1/5)-1", PCT),
    ("FY31E GAAP operating margin", "=IS!J22", PCT),
    ("FY31E non-GAAP operating margin", "=IS!J44", PCT),
    ("FY31E free cash flow (CFO - capex)", "=CF!J32", NUM),
]
for i, (t, f, fmt) in enumerate(outs, start=5):
    put(cv, f"A{i}", t, BLACK)
    put(cv, f"B{i}", f, GREEN, fmt, bold=True)
put(cv, "C12", "='Revenue Build'!B29", GREEN, bold=True)

put(cv, "A19", "Model integrity checks", BOLDW, fill=HEADFILL)
for c in "BCD":
    cv[f"{c}19"].fill = HEADFILL
put(cv, "A20", "Balance sheet balances in every year?")
put(cv, "B20", '=IF(SUMPRODUCT(ABS(BS!D31:J31))<0.01,"OK","ERROR")', BLACK, bold=True)
put(cv, "A21", "Forecast cash stays positive?")
put(cv, "B21", '=IF(MIN(BS!F5:J5)>0,"OK","NEGATIVE CASH")', BLACK, bold=True)
put(cv, "A22", "Historical CF ties to reported CFO?")
put(cv, "B22", '=IF(SUMPRODUCT(ABS(CF!B14:E14-CF!B15:E15))<0.01,"OK","ERROR")', BLACK, bold=True)
put(cv, "A23", "WACC > terminal growth?")
put(cv, "B23", '=IF(DCF!B30>DCF!B33,"OK","ERROR")', BLACK, bold=True)

put(cv, "A25", "Scenario snapshot (values pasted at build; re-run by changing Assumptions!B4)", BOLDW, fill=HEADFILL)
for c in "BCD":
    cv[f"{c}25"].fill = HEADFILL
for c, t in zip("BCD", ["Downside", "Base", "Upside"]):
    put(cv, f"{c}26", t, BOLD)
    cv[f"{c}26"].alignment = Alignment(horizontal="right")
snap_rows = ["Value per share - blended ($)", "Upside / (downside)", "FY31E revenue ($mm)",
             "FY31E GAAP operating margin", "FY31E free cash flow ($mm)"]
for i, t in enumerate(snap_rows, start=27):
    put(cv, f"A{i}", t)

put(cv, "A34", "How to use", BOLDW, fill=HEADFILL)
for c in "BCD":
    cv[f"{c}34"].fill = HEADFILL
howto = [
    "1. Flip the scenario on Assumptions!B4 (1 Downside, 2 Base, 3 Upside). Everything recalculates.",
    "2. Revenue engine: Revenue Build. Subscription revenue = prior year-end cRPO x conversion ratio; cRPO growth is the main lever.",
    "3. Costs and working capital are % of revenue on Assumptions; historical ratios are listed next to each input.",
    "4. Statements: IS -> BS -> CF. Ending cash on CF feeds BS cash; BS!31 must be 0 in every year.",
    "5. DCF: B16 toggles whether SBC is treated as a real cost (default 1 = yes). Sensitivity tables at DCF!A80 and A89.",
    "Colour code: blue = hardcoded input, black = formula, green = link to another sheet, yellow = key lever.",
]
for i, t in enumerate(howto, start=35):
    put(cv, f"A{i}", t)

for ws in wb.worksheets:
    for row in ws.iter_rows():
        for cell in row:
            if cell.font and cell.font.name != FONT:
                cell.font = Font(name=FONT, size=cell.font.size or 10, bold=cell.font.bold,
                                 italic=cell.font.italic, color=cell.font.color)


# Scenario snapshot: values from recalculating the workbook with Assumptions!B4 = 1, 2, 3
SNAPSHOT = {  # scenario: (value per share, upside, FY31 revenue, FY31 GAAP op margin, FY31 FCF)
    "1": (179.9113, -0.2375, 58522.1, 0.2241, 15916.5),
    "2": (230.3644, -0.0237, 67037.0, 0.2489, 20151.8),
    "3": (265.0172, 0.1232, 72624.8, 0.2642, 23023.8),
}
for col, s in zip("BCD", ("1", "2", "3")):
    for r, (v, f) in enumerate(zip(SNAPSHOT[s], ["$#,##0.00", "0.0%;(0.0%)", "#,##0", "0.0%", "#,##0"]), start=27):
        c = cv[f"{col}{r}"]
        c.value = v
        c.number_format = f
        c.font = Font(name="Arial", size=10, italic=True)
cv["A32"] = "Snapshot uses base valuation inputs (WACC, terminal growth, exit multiple) in all three scenarios."
cv["A32"].font = ITAL

OUT = Path(__file__).resolve().parent.parent / "model" / "Salesforce_CRM_Model.xlsx"
wb.save(OUT)
print(f"saved {OUT}")
