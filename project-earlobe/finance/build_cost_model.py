#!/usr/bin/env python3
"""Build finance/cost-model.xlsx: the Earlobe cost-out workbook and ROI model.

Every number lives in the ASSUMPTIONS blocks below and lands on the
'Assumptions' tab in blue (inputs). Every other tab is formulas only, so the
workbook recalculates when Joshua edits an input in Excel/Sheets.

    python finance/build_cost_model.py            # writes finance/cost-model.xlsx
    python <xlsx skill>/scripts/recalc.py finance/cost-model.xlsx

Prices are list prices as of Oct 2026 and cite docs/research/facts-and-figures.md
IDs (F-...). Anything we estimated rather than read is marked "(inference)".
"""
from __future__ import annotations

import os

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cost-model.xlsx")

SCEN = ["Test markets", "Wave 1", "Scale", "Dominate"]
CASES = ["Conservative", "Base", "Optimistic"]

# ----------------------------------------------------------------- assumptions
GLOBAL = [
    # key, label, value, unit, note
    ("chars_per_min", "Spoken characters per audio minute", 1000, "chars/min", "ElevenLabs guidance ~1,000 chars ≈ 1 min (F-TTS)"),
    ("credits_per_char", "ElevenLabs credits per character", 1.0, "credits", "1.0 full-quality voices; Flash/Turbo ~0.5 (F-TTS-09) — verify per model"),
    ("rerender", "Re-render / QA overhead on voice", 1.25, "x", "(inference) F-TTS-16: retakes, pronunciation fixes, QA listens"),
    ("secondary_rate", "Secondary voice engine, $ per audio minute", 0.03, "$", "Google Chirp 3 HD-class, $30 per 1M chars (F-TTS-23)"),
    ("weekdays", "Weekdays per month", 21.7, "days", "365×5/7/12"),
    ("days", "Days per month", 30.4, "days", ""),
    ("cache_savings", "Prompt-caching savings on LLM input", 0.15, "%", "(inference) system prompts + rubrics cached; cache reads bill at 0.1× input"),
    ("rewrite_rate", "Share of episodes that need a REWRITE loop", 0.30, "%", "(inference) tune from gate logs after launch"),
    ("rewrite_share", "Cost of one rewrite loop vs a first pass", 0.60, "x", "(inference) writer + re-check of changed claims"),
    ("batch_discount", "Batch API discount (evergreen only)", 0.50, "%", "Anthropic Message Batches: 50% off (F-LLM)"),
]

TIERS = [("opus", 4.00, 20.00), ("sonnet", 2.00, 10.00), ("haiku", 0.10, 0.50)]
SEARCH_PER_1K = 10.0

# Per-episode agent steps for a baseline ~7-minute verified news brief.
STEPS = [
    # agent, tier, input tokens, output tokens (incl. thinking), web searches
    ("Story triage (Story Desk)", "haiku", 60000, 4000, 0),
    ("Producer / scriptwriter", "opus", 40000, 10000, 0),
    ("Claim extractor", "opus", 8000, 4000, 0),
    ("Source verifier (blind, web search)", "opus", 150000, 12000, 20),
    ("Fact checker", "opus", 40000, 6000, 0),
    ("Bias checker", "sonnet", 10000, 3000, 0),
    ("Legal / defamation screener", "opus", 10000, 3000, 0),
    ("Copywriter (title, notes, social)", "sonnet", 8000, 3000, 0),
    ("Disclosure + QA listener", "haiku", 6000, 1500, 0),
]

SHOW_TYPES = [
    # key, label, minutes/ep, eps/month/show, LLM scale vs baseline, batch(0/1), ads/ep, downloads/ep base (inference)
    ("local", "Local daily brief", 7, 21.7, 1.0, 0, 2, 120),          # F-AUD-03 base
    ("breaking", "Breaking Desk feed", 3, 30, 0.8, 0, 1, 500),         # F-AUD-04 base
    ("courts", "Courts roundup", 10, 21.7, 1.3, 0, 2, 120),            # (inference)
    ("tracker", "Case Tracker (weekly + flashes)", 20, 8.3, 1.8, 0, 3, 300),   # (inference)
    ("coldcase", "Cold Case Files", 22, 8.7, 2.2, 1, 3, 400),          # F-AUD-04 base
    ("archive", "Archive series (History of Hollywood, hometown)", 18, 13, 1.8, 1, 3, 400),  # (inference)
    ("niche", "Hyper-specific always-on feed", 5, 12, 0.6, 0, 1, 60),
]

# Shows per type per scenario: Test, Wave 1, Scale, Dominate
SHOW_COUNTS = {
    "local": [2, 6, 25, 100],
    "breaking": [1, 2, 3, 5],
    "courts": [1, 3, 10, 30],
    "tracker": [1, 1, 2, 4],
    "coldcase": [1, 1, 2, 4],
    "archive": [1, 4, 15, 50],
    "niche": [0, 10, 100, 500],
}
DOWNLOAD_MULT = [1.0, 1.5, 2.25, 3.0]   # audience maturity (inference); keeps local <= 400/ep (F-AUD-03 optimistic)

ELEVEN_PLANS = [
    # name, $/month, credits/month (F-TTS, as of Oct 2026)
    ("Creator", 22, 121000),
    ("Pro", 99, 600000),
    ("Scale", 299, 1800000),
    ("Business", 990, 6000000),
    ("Enterprise (negotiated)", 3000, 30000000),
]
PLAN_BY_SCEN = ["Scale", "Business", "Enterprise (negotiated)", "Enterprise (negotiated)"]   # F-TTS-35/36
OVERAGE_PER_1K = [0.24, 0.24, 0.12, 0.10]  # $ per 1k extra credits (F-TTS-11 Pro ~$0.24; later stages negotiated, inference)
SECONDARY_SHARE = [0, 0, 0, 0]   # share of minutes on the secondary engine; all-ElevenLabs by founder choice (hybrid: F-TTS-36..38)
GRANT_CREDITS = [0, 0, 0, 0]     # ElevenLabs Startup Grant credits/month if awarded (~2,750,000 for 12 months, F-TTS-22)

# Revenue assumptions by case (Conservative, Base, Optimistic) — all (inference) until benchmarked (F-ADS)
REV = [
    ("cpm", "Programmatic CPM (gross, per 1,000 ad impressions)", [8, 13, 20], "$"),       # F-ADS-07
    ("fill", "Ad fill rate", [0.30, 0.55, 0.75], "%"),                                       # F-ADS-08
    ("share", "Our share after host/marketplace", [0.50, 0.60, 0.70], "%"),
    ("sponsor_cpm", "Local direct sponsor, effective CPM per slot", [20, 35, 60], "$"),      # F-ADS-10
    ("sponsor_sold", "Local sponsor slots sold (sell-through)", [0.25, 0.50, 0.75], "%"),     # F-ADS-10
    ("pkg_rate", "Flat community package, $ per month", [50, 100, 150], "$"),                # F-ADS-10
    ("b2b_rate", "B2B white-label brief, $ per client per month", [1000, 2000, 3500], "$"),
    ("api_rate", "Trust Stack API, $ per client per month", [500, 1500, 3000], "$"),
    ("services_rate", "Studio Services project, $ each", [1500, 3000, 5000], "$"),
    ("premium_price", "Premium/ad-free subscription, $ per month", [3, 5, 7], "$"),
]
# Volume drivers by scenario (Test, Wave 1, Scale, Dominate) — (inference)
REV_VOLUME = [
    ("pkgs_per_local", "Community packages sold per local/courts show", [1, 2, 3, 4], "packages"),
    ("b2b_clients", "B2B white-label clients", [0, 1, 5, 20], "clients"),
    ("api_clients", "Trust Stack API clients", [0, 0, 3, 15], "clients"),
    ("services_projects", "Studio Services projects per month", [1, 2, 3, 4], "projects"),
    ("premium_subs", "Premium subscribers", [0, 50, 500, 3000], "subs"),
]
PREMIUM_NET = 0.70  # share kept after platform fees (inference; Apple/Patreon vary)

FIXED = [
    # category, item, vendor/plan, $/month, qty by scenario, note
    ("Hosting", "Podcast hosting + dynamic ad insertion", "Multi-show host (see cost-out-and-roi.md)", 49, [1, 2, 5, 20], "F-HOST-10 — verify current plans"),
    ("Insurance", "Media liability / E&O", "Specialist media insurer", 500, [1, 1, 2, 3], "F-LEGAL-01 placeholder; automated courts/crime may be declined — get quotes"),
    ("Infrastructure", "GitHub (Actions minutes, private repos)", "GitHub Free → Team", 0, [1, 1, 1, 1], "Public repo Actions are free; Team $4/user if needed"),
    ("Infrastructure", "Database (Supabase)", "Free → Pro", 25, [0, 1, 1, 1], "Free tier pauses when idle; Pro from Wave 1 (F-INFRA-03)"),
    ("Infrastructure", "Compute for always-on agents / runners", "VPS or managed runners", 0, [0, 20, 150, 800], "(inference) GitHub Actions covers early stages"),
    ("Data", "Court + news data (PACER, paid APIs)", "PACER, CourtListener, news API", 1, [150, 250, 500, 2000], "F-DATA-02 PACER ~$150-300/mo; CourtListener/GDELT free first"),
    ("Voice", "Google AI Pro (NotebookLM, optional prototyping)", "Google AI Pro", 19.99, [1, 0, 0, 0], "Not a production engine (F-TTS-32)"),
    ("Legal", "California LLC annual tax (if CA-registered)", "Franchise Tax Board", 66.67, [1, 1, 1, 1], "$800/yr (F-LEGAL-05)"),
    ("Music", "Music / sonic library license", "Library subscription", 30, [1, 1, 1, 2], "F-LEGAL-06"),
    ("Admin", "Domain + email", "Registrar + mailbox", 8, [1, 1, 1, 1], "(inference)"),
    ("Admin", "Bookkeeping software", "e.g. QuickBooks/Wave", 30, [1, 1, 1, 1], "(inference)"),
    ("Admin", "Design tools (cover art, clips)", "Canva Pro or similar", 15, [1, 1, 1, 2], "(inference)"),
    ("People", "Contract help (sales, legal on retainer)", "Freelance", 0, [0, 0, 2000, 8000], "(inference) first hires come from revenue"),
]
ONE_TIME = [
    ("Legal", "Media-lawyer setup review (standards, courts/crime lanes)", 5000, "F-LEGAL-02 mid ($2,500-$7,500)"),
    ("Legal", "Trademark filing: 2 classes (41, then 9)", 700, "USPTO $350/class (F-LEGAL-03)"),
    ("Legal", "Trademark clearance search (attorney)", 1000, "F-LEGAL-02 ($500-$2,000 per mark)"),
    ("Legal", "DBA / assumed-name filing", 120, "F-LEGAL-04 (~$56-$176)"),
    ("Brand", "Network + show cover art and sonic logo", 500, "(inference)"),
    ("Admin", "Domain registration (year 1)", 20, "(inference)"),
    ("Voice", "Voice design / pronunciation dictionaries setup", 0, "Included in ElevenLabs plan"),
]

STAGE_BY_MONTH = [1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3]           # 1=Test 2=Wave1 3=Scale 4=Dominate
AUDIENCE_RAMP = [0.10, 0.20, 0.30, 0.35, 0.45, 0.55, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]

# ----------------------------------------------------------------- styling
ARIAL = "Arial"
F_IN = Font(name=ARIAL, color="0000FF")
F_CALC = Font(name=ARIAL, color="000000")
F_LINK = Font(name=ARIAL, color="008000")
F_BOLD = Font(name=ARIAL, bold=True)
F_H1 = Font(name=ARIAL, bold=True, size=14)
F_H2 = Font(name=ARIAL, bold=True, size=11, color="FFFFFF")
FILL_H = PatternFill("solid", fgColor="1F3A5F")
FILL_KEY = PatternFill("solid", fgColor="FFFF00")
FILL_SUB = PatternFill("solid", fgColor="E8EEF5")
THIN = Side(style="thin", color="B7C3D0")
BOX = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)
USD = '$#,##0;($#,##0);"-"'
USD2 = '$#,##0.00;($#,##0.00);"-"'
PCT = '0.0%;(0.0%);"-"'
NUM = '#,##0;(#,##0);"-"'
NUM1 = '#,##0.0;(#,##0.0);"-"'


def style_all(ws):
    for row in ws.iter_rows():
        for c in row:
            if c.font is None or c.font.name != ARIAL:
                c.font = Font(name=ARIAL, bold=c.font.bold if c.font else False,
                              color=c.font.color if c.font else None,
                              size=c.font.size if c.font else 11)


def header(ws, row, labels, col=1):
    for i, lab in enumerate(labels):
        c = ws.cell(row=row, column=col + i, value=lab)
        c.font, c.fill = F_H2, FILL_H
        c.alignment = Alignment(wrap_text=True, vertical="center")


def title(ws, text, sub=None):
    ws["A1"] = text
    ws["A1"].font = F_H1
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(name=ARIAL, italic=True, color="555555")


def inp(ws, ref, value, fmt=None, key=False):
    c = ws[ref]
    c.value = value
    c.font = F_IN
    if fmt:
        c.number_format = fmt
    if key:
        c.fill = FILL_KEY
    return c


def calc(ws, ref, formula, fmt=None, bold=False, link=False):
    c = ws[ref]
    c.value = formula
    c.font = Font(name=ARIAL, bold=bold, color="008000" if link else "000000")
    if fmt:
        c.number_format = fmt
    return c


def widths(ws, spec):
    for col, w in spec.items():
        ws.column_dimensions[col].width = w


# ----------------------------------------------------------------- build
def build():
    wb = Workbook()
    A = {}            # name -> absolute ref on Assumptions
    SC = "'Scenarios'"
    AS = "'Assumptions'"

    # ============================================================ Assumptions
    ws = wb.active
    ws.title = "Assumptions"
    title(ws, "Assumptions — every input lives here (blue = editable)",
          "Prices as of Oct 2026 — verify before buying. (inference) = our estimate, not a quoted price.")
    r = 4
    ws.cell(row=r, column=1, value="Model selectors").font = F_BOLD
    r += 1
    ws.cell(row=r, column=1, value="Revenue case (1 = Conservative, 2 = Base, 3 = Optimistic)")
    inp(ws, f"B{r}", 2, key=True)
    A["case"] = f"{AS}!$B${r}"
    r += 1
    ws.cell(row=r, column=1, value="Scenario used for unit economics (1 = Test … 4 = Dominate)")
    inp(ws, f"B{r}", 2, key=True)
    A["ue_scen"] = f"{AS}!$B${r}"

    r += 2
    ws.cell(row=r, column=1, value="Global").font = F_BOLD
    r += 1
    header(ws, r, ["Input", "Value", "Unit", "Source / note"])
    for key, label, val, unit, note in GLOBAL:
        r += 1
        ws.cell(row=r, column=1, value=label)
        inp(ws, f"B{r}", val, PCT if unit == "%" else ("0.00" if isinstance(val, float) else NUM))
        ws.cell(row=r, column=3, value=unit)
        ws.cell(row=r, column=4, value=note)
        A[key] = f"{AS}!$B${r}"

    r += 2
    ws.cell(row=r, column=1, value="Claude API list prices (per million tokens)").font = F_BOLD
    r += 1
    header(ws, r, ["Tier", "Input $/M", "Output $/M", "Source / note"])
    for tier, pin, pout in TIERS:
        r += 1
        ws.cell(row=r, column=1, value=tier)
        inp(ws, f"B{r}", pin, USD2)
        inp(ws, f"C{r}", pout, USD2)
        ws.cell(row=r, column=4, value="Anthropic list price, Oct 2026 (F-LLM)")
        A[f"in_{tier}"] = f"{AS}!$B${r}"
        A[f"out_{tier}"] = f"{AS}!$C${r}"
    r += 1
    ws.cell(row=r, column=1, value="Web search, $ per 1,000 searches")
    inp(ws, f"B{r}", SEARCH_PER_1K, USD2)
    ws.cell(row=r, column=4, value="Anthropic web search tool (F-LLM)")
    A["search"] = f"{AS}!$B${r}"

    r += 2
    ws.cell(row=r, column=1, value="Per-episode agent work — baseline 7-minute verified news brief").font = F_BOLD
    r += 1
    header(ws, r, ["Agent step", "Tier", "Input tokens", "Output tokens", "Web searches", "Cost / episode"])
    step_first = r + 1
    for name, tier, tin, tout, srch in STEPS:
        r += 1
        ws.cell(row=r, column=1, value=name)
        inp(ws, f"B{r}", tier)
        inp(ws, f"C{r}", tin, NUM)
        inp(ws, f"D{r}", tout, NUM)
        inp(ws, f"E{r}", srch, NUM)
        price_in = (f'IF(B{r}="opus",{A["in_opus"]},IF(B{r}="sonnet",{A["in_sonnet"]},{A["in_haiku"]}))')
        price_out = (f'IF(B{r}="opus",{A["out_opus"]},IF(B{r}="sonnet",{A["out_sonnet"]},{A["out_haiku"]}))')
        calc(ws, f"F{r}", f"=C{r}/1000000*{price_in}+D{r}/1000000*{price_out}+E{r}/1000*{A['search']}", USD2)
    step_last = r
    r += 1
    ws.cell(row=r, column=1, value="Baseline LLM + search cost per episode (before caching/rewrites)").font = F_BOLD
    calc(ws, f"F{r}", f"=SUM(F{step_first}:F{step_last})", USD2, bold=True)
    A["llm_base"] = f"{AS}!$F${r}"

    r += 2
    ws.cell(row=r, column=1, value="Show types").font = F_BOLD
    r += 1
    header(ws, r, ["Show type", "Minutes / episode", "Episodes / month / show", "LLM work vs baseline",
                   "Batch-eligible (1/0)", "Ad slots / episode", "Downloads / episode (base, test stage)"])
    A["types"] = {}
    for key, label, mins, eps, scale, batch, ads, dl in SHOW_TYPES:
        r += 1
        ws.cell(row=r, column=1, value=label)
        inp(ws, f"B{r}", mins, NUM)
        inp(ws, f"C{r}", eps, NUM1)
        inp(ws, f"D{r}", scale, "0.0x")
        inp(ws, f"E{r}", batch, NUM)
        inp(ws, f"F{r}", ads, NUM)
        inp(ws, f"G{r}", dl, NUM)
        ws.cell(row=r, column=8, value="(inference) — replace with real analytics after launch")
        A["types"][key] = r
    ws_types = (min(A["types"].values()), max(A["types"].values()))

    r += 2
    ws.cell(row=r, column=1, value="Number of shows by scenario").font = F_BOLD
    r += 1
    header(ws, r, ["Show type"] + SCEN)
    A["counts"] = {}
    for key, label, *_ in SHOW_TYPES:
        r += 1
        ws.cell(row=r, column=1, value=label)
        for j, v in enumerate(SHOW_COUNTS[key]):
            inp(ws, f"{get_column_letter(2 + j)}{r}", v, NUM, key=True)
        A["counts"][key] = r
    r += 1
    ws.cell(row=r, column=1, value="Audience maturity multiplier on downloads")
    for j, v in enumerate(DOWNLOAD_MULT):
        inp(ws, f"{get_column_letter(2 + j)}{r}", v, "0.0x")
    A["dl_mult_row"] = r

    r += 2
    ws.cell(row=r, column=1, value="ElevenLabs plans (voice engine)").font = F_BOLD
    r += 1
    header(ws, r, ["Plan", "$ / month", "Credits / month", "$ per 1k credits", "Source / note"])
    plan_first = r + 1
    for name, price, credits in ELEVEN_PLANS:
        r += 1
        ws.cell(row=r, column=1, value=name)
        inp(ws, f"B{r}", price, USD)
        inp(ws, f"C{r}", credits, NUM)
        calc(ws, f"D{r}", f"=IF(C{r}=0,0,B{r}/C{r}*1000)", USD2)
        ws.cell(row=r, column=5, value="elevenlabs.io/pricing, Oct 2026 (F-TTS)" if "Enterprise" not in name
                else "(inference) negotiated volume deal")
    plan_last = r
    A["plan_names"] = f"{AS}!$A${plan_first}:$A${plan_last}"
    A["plan_prices"] = f"{AS}!$B${plan_first}:$B${plan_last}"
    A["plan_credits"] = f"{AS}!$C${plan_first}:$C${plan_last}"
    r += 1
    header(ws, r, ["Plan used by scenario"] + SCEN)
    r += 1
    ws.cell(row=r, column=1, value="Plan name (must match a plan above)")
    for j, v in enumerate(PLAN_BY_SCEN):
        inp(ws, f"{get_column_letter(2 + j)}{r}", v, key=True)
    A["plan_row"] = r
    r += 1
    ws.cell(row=r, column=1, value="Overage, $ per 1k extra credits")
    for j, v in enumerate(OVERAGE_PER_1K):
        inp(ws, f"{get_column_letter(2 + j)}{r}", v, USD2)
    A["overage_row"] = r
    r += 1
    ws.cell(row=r, column=1, value="Share of minutes on secondary engine (hybrid)")
    for j, v in enumerate(SECONDARY_SHARE):
        inp(ws, f"{get_column_letter(2 + j)}{r}", v, PCT)
    A["secondary_row"] = r
    r += 1
    ws.cell(row=r, column=1, value="ElevenLabs Startup Grant credits / month (0 unless awarded)")
    for j, v in enumerate(GRANT_CREDITS):
        inp(ws, f"{get_column_letter(2 + j)}{r}", v, NUM)
    A["grant_row"] = r

    r += 2
    ws.cell(row=r, column=1, value="Revenue rates by case").font = F_BOLD
    r += 1
    header(ws, r, ["Rate"] + CASES + ["Unit"])
    A["rev"] = {}
    for key, label, vals, unit in REV:
        r += 1
        ws.cell(row=r, column=1, value=label)
        for j, v in enumerate(vals):
            inp(ws, f"{get_column_letter(2 + j)}{r}", v, PCT if unit == "%" else USD)
        ws.cell(row=r, column=5, value=unit)
        A["rev"][key] = f"INDEX({AS}!$B${r}:$D${r},{A['case']})"
    r += 1
    ws.cell(row=r, column=1, value="Premium: share kept after platform fees")
    inp(ws, f"B{r}", PREMIUM_NET, PCT)
    A["premium_net"] = f"{AS}!$B${r}"

    r += 2
    ws.cell(row=r, column=1, value="Revenue volume by scenario").font = F_BOLD
    r += 1
    header(ws, r, ["Driver"] + SCEN)
    A["vol"] = {}
    for key, label, vals, unit in REV_VOLUME:
        r += 1
        ws.cell(row=r, column=1, value=label)
        for j, v in enumerate(vals):
            inp(ws, f"{get_column_letter(2 + j)}{r}", v, NUM1 if isinstance(v, float) else NUM)
        A["vol"][key] = r

    r += 2
    ws.cell(row=r, column=1, value="12-month plan inputs").font = F_BOLD
    r += 1
    header(ws, r, ["Month"] + [str(m) for m in range(1, 13)])
    r += 1
    ws.cell(row=r, column=1, value="Stage (1 Test, 2 Wave 1, 3 Scale, 4 Dominate)")
    for m, v in enumerate(STAGE_BY_MONTH):
        inp(ws, f"{get_column_letter(2 + m)}{r}", v, NUM, key=True)
    A["stage_row"] = r
    r += 1
    ws.cell(row=r, column=1, value="Audience ramp (share of steady-state downloads)")
    for m, v in enumerate(AUDIENCE_RAMP):
        inp(ws, f"{get_column_letter(2 + m)}{r}", v, PCT)
    A["ramp_row"] = r
    widths(ws, {"A": 58, "B": 14, "C": 16, "D": 16, "E": 16, "F": 16, "G": 18, "H": 50})
    for col in "IJKLM":
        ws.column_dimensions[col].width = 12
    ws.freeze_panes = "B4"

    # ============================================================ Unit Economics
    ue = wb.create_sheet("Unit Economics")
    title(ue, "Unit economics — cost and break-even per episode",
          "Voice cost uses the effective $/credit of the scenario chosen on Assumptions (unit-economics scenario).")
    header(ue, 4, ["Show type", "Minutes", "LLM + search $ / ep", "Voice $ / ep", "Variable cost $ / ep",
                   "Revenue $ per download", "Break-even downloads / ep", "Base downloads / ep (scenario)",
                   "Margin $ / ep at base downloads"])
    ue_rows = {}
    r = 4
    for key, label, *_ in SHOW_TYPES:
        r += 1
        t = A["types"][key]
        ue.cell(row=r, column=1, value=label)
        calc(ue, f"B{r}", f"={AS}!B{t}", NUM, link=True)
        llm = (f"={A['llm_base']}*{AS}!D{t}*(1-{A['cache_savings']})*(1-{AS}!E{t}*{A['batch_discount']})"
               f"*(1+{A['rewrite_rate']}*{A['rewrite_share']})")
        calc(ue, f"C{r}", llm, USD2)
        eff = f"INDEX({SC}!$C$30:$F$30,{A['ue_scen']})"   # effective voice $ per audio minute (Scenarios row 30)
        calc(ue, f"D{r}", f"=B{r}*{eff}", USD2)
        calc(ue, f"E{r}", f"=C{r}+D{r}", USD2, bold=True)
        rev_dl = f"={AS}!F{t}*{A['rev']['cpm']}/1000*{A['rev']['fill']}*{A['rev']['share']}"
        calc(ue, f"F{r}", rev_dl, '$#,##0.0000')
        calc(ue, f"G{r}", f"=IF(F{r}=0,0,E{r}/F{r})", NUM, bold=True)
        calc(ue, f"H{r}", f"={AS}!G{t}*INDEX({AS}!$B${A['dl_mult_row']}:$E${A['dl_mult_row']},{A['ue_scen']})", NUM)
        calc(ue, f"I{r}", f"=H{r}*F{r}-E{r}", USD2)
        ue_rows[key] = r
    widths(ue, {"A": 44, "B": 10, "C": 18, "D": 14, "E": 18, "F": 18, "G": 20, "H": 22, "I": 24})
    r += 2
    ue.cell(row=r, column=1, value="Read this as: an episode pays for itself once it reaches the break-even downloads "
                                   "from ads alone. Sponsors, B2B, API and services revenue sit on top (Scenarios tab).")

    # ============================================================ Scenarios
    sc = wb.create_sheet("Scenarios")
    title(sc, "Scenarios — monthly steady state", "Revenue case set on Assumptions. All values per month.")
    header(sc, 3, ["Line", ""] + SCEN)
    cols = ["C", "D", "E", "F"]

    def put_row(row, label, fn, fmt=USD, bold=False):
        sc.cell(row=row, column=1, value=label).font = F_BOLD if bold else Font(name=ARIAL)
        for j, col in enumerate(cols):
            calc(sc, f"{col}{row}", fn(j, col), fmt, bold=bold)

    row = 4
    sc.cell(row=row, column=1, value="Shows").font = F_BOLD
    shows_rows = {}
    for key, label, *_ in SHOW_TYPES:
        row += 1
        cr = A["counts"][key]
        put_row(row, f"  {label}", lambda j, col, cr=cr: f"={AS}!{get_column_letter(2 + j)}{cr}", NUM)
        shows_rows[key] = row
    row += 1                                     # 12
    put_row(row, "Total shows", lambda j, col: f"=SUM({col}5:{col}{row - 1})", NUM, bold=True)
    total_shows_row = row
    row += 1
    sc.cell(row=row, column=1, value="Episodes per month").font = F_BOLD
    eps_rows = {}
    for key, label, *_ in SHOW_TYPES:
        row += 1
        t, s = A["types"][key], shows_rows[key]
        put_row(row, f"  {label}", lambda j, col, t=t, s=s: f"={col}{s}*{AS}!$C${t}", NUM)
        eps_rows[key] = row
    first_eps, last_eps = min(eps_rows.values()), max(eps_rows.values())
    row += 1
    put_row(row, "Total episodes / month", lambda j, col: f"=SUM({col}{first_eps}:{col}{last_eps})", NUM, bold=True)
    total_eps_row = row
    row += 1
    mins = "+".join(f"{{col}}{eps_rows[k]}*{AS}!$B${A['types'][k]}" for k in eps_rows)
    put_row(row, "Audio minutes / month", lambda j, col: "=" + mins.format(col=col), NUM)
    minutes_row = row
    row += 1
    put_row(row, "ElevenLabs credits needed / month (after hybrid share, overhead, grant)",
            lambda j, col: f"=MAX(0,{col}{minutes_row}*(1-{AS}!{get_column_letter(2 + j)}${A['secondary_row']})"
                           f"*{A['chars_per_min']}*{A['credits_per_char']}*{A['rerender']}"
                           f"-{AS}!{get_column_letter(2 + j)}${A['grant_row']})", NUM)
    credits_row = row
    # row 26..30 voice cost block — keep effective-rate row at 30 (Unit Economics references it)
    row = 26
    put_row(row, "ElevenLabs plan price", lambda j, col:
            f"=INDEX({A['plan_prices']},MATCH({AS}!{get_column_letter(2 + j)}${A['plan_row']},{A['plan_names']},0))", USD)
    price_row = row
    row = 27
    put_row(row, "Plan credits included", lambda j, col:
            f"=INDEX({A['plan_credits']},MATCH({AS}!{get_column_letter(2 + j)}${A['plan_row']},{A['plan_names']},0))", NUM)
    incl_row = row
    row = 28
    put_row(row, "Overage credits", lambda j, col: f"=MAX(0,{col}{credits_row}-{col}{incl_row})", NUM)
    over_row = row
    row = 29
    put_row(row, "Voice (ElevenLabs) cost / month", lambda j, col:
            f"={col}{price_row}+{col}{over_row}/1000*{AS}!{get_column_letter(2 + j)}${A['overage_row']}"
            f"+{col}{minutes_row}*{AS}!{get_column_letter(2 + j)}${A['secondary_row']}*{A['secondary_rate']}", USD, bold=True)
    voice_row = row
    row = 30
    put_row(row, "Effective voice $ per audio minute", lambda j, col:
            f"=IF({col}{minutes_row}=0,0,{col}{voice_row}/{col}{minutes_row})", '$#,##0.0000')
    row = 31
    llm = "+".join(f"{{col}}{eps_rows[k]}*'Unit Economics'!$C${ue_rows[k]}" for k in eps_rows)
    put_row(row, "Claude API (agents + web search) / month", lambda j, col: "=" + llm.format(col=col), USD, bold=True)
    llm_row = row
    row = 32
    put_row(row, "Fixed operating costs / month (Cost Lines)", lambda j, col:
            f"='Cost Lines'!{get_column_letter(9 + j)}$FIXEDTOTAL", USD, bold=True)
    fixed_row = row
    row = 33
    put_row(row, "TOTAL MONTHLY COST", lambda j, col: f"={col}{voice_row}+{col}{llm_row}+{col}{fixed_row}", USD, bold=True)
    cost_row = row
    row = 34
    put_row(row, "Cost per episode (all-in)", lambda j, col: f"=IF({col}{total_eps_row}=0,0,{col}{cost_row}/{col}{total_eps_row})", USD2)
    row = 36
    sc.cell(row=row, column=1, value="Audience & revenue").font = F_BOLD
    row = 37
    dls = "+".join(f"{{col}}{eps_rows[k]}*{AS}!$G${A['types'][k]}" for k in eps_rows)
    put_row(row, "Downloads / month", lambda j, col:
            f"=({dls.format(col=col)})*{AS}!{get_column_letter(2 + j)}${A['dl_mult_row']}", NUM)
    dl_row = row
    row = 38
    imps = "+".join(f"{{col}}{eps_rows[k]}*{AS}!$G${A['types'][k]}*{AS}!$F${A['types'][k]}" for k in eps_rows)
    put_row(row, "Programmatic ad revenue", lambda j, col:
            f"=({imps.format(col=col)})*{AS}!{get_column_letter(2 + j)}${A['dl_mult_row']}"
            f"/1000*{A['rev']['cpm']}*{A['rev']['fill']}*{A['rev']['share']}", USD)
    ads_row = row
    row = 39
    local_dl = (f"({{col}}{eps_rows['local']}*{AS}!$G${A['types']['local']}*{AS}!$F${A['types']['local']}"
                f"+{{col}}{eps_rows['courts']}*{AS}!$G${A['types']['courts']}*{AS}!$F${A['types']['courts']})")
    put_row(row, "Local sponsors (impressions sold + community packages)", lambda j, col:
            f"={local_dl.format(col=col)}*{AS}!{get_column_letter(2 + j)}${A['dl_mult_row']}"
            f"/1000*{A['rev']['sponsor_cpm']}*{A['rev']['sponsor_sold']}"
            f"+({col}{shows_rows['local']}+{col}{shows_rows['courts']})"
            f"*{AS}!{get_column_letter(2 + j)}${A['vol']['pkgs_per_local']}*{A['rev']['pkg_rate']}", USD)
    row = 40
    put_row(row, "B2B white-label briefs", lambda j, col:
            f"={AS}!{get_column_letter(2 + j)}${A['vol']['b2b_clients']}*{A['rev']['b2b_rate']}", USD)
    row = 41
    put_row(row, "Trust Stack API", lambda j, col:
            f"={AS}!{get_column_letter(2 + j)}${A['vol']['api_clients']}*{A['rev']['api_rate']}", USD)
    row = 42
    put_row(row, "C&C Studio Services", lambda j, col:
            f"={AS}!{get_column_letter(2 + j)}${A['vol']['services_projects']}*{A['rev']['services_rate']}", USD)
    row = 43
    put_row(row, "Premium subscriptions", lambda j, col:
            f"={AS}!{get_column_letter(2 + j)}${A['vol']['premium_subs']}*{A['rev']['premium_price']}*{A['premium_net']}", USD)
    row = 44
    put_row(row, "TOTAL MONTHLY REVENUE", lambda j, col: f"=SUM({col}{ads_row}:{col}43)", USD, bold=True)
    rev_row = row
    row = 45
    put_row(row, "NET / MONTH", lambda j, col: f"={col}{rev_row}-{col}{cost_row}", USD, bold=True)
    net_row = row
    row = 46
    put_row(row, "Margin", lambda j, col: f"=IF({col}{rev_row}=0,0,{col}{net_row}/{col}{rev_row})", PCT)
    row = 47
    put_row(row, "Ads share of revenue", lambda j, col: f"=IF({col}{rev_row}=0,0,{col}{ads_row}/{col}{rev_row})", PCT)
    row = 48
    put_row(row, "Annualized net", lambda j, col: f"={col}{net_row}*12", USD, bold=True)
    row = 49
    put_row(row, "Network-only revenue (ads + sponsors + premium)", lambda j, col:
            f"={col}{ads_row}+{col}39+{col}43", USD)
    net_rev_row = row
    row = 50
    put_row(row, "Network-only net (excludes B2B, API, Studio Services)", lambda j, col:
            f"={col}{net_rev_row}-{col}{cost_row}", USD, bold=True)
    net_only_row = row
    for rr in (cost_row, rev_row, net_row, net_only_row):
        for col in ["A"] + cols:
            sc[f"{col}{rr}"].fill = FILL_SUB
    widths(sc, {"A": 46, "B": 2, "C": 16, "D": 16, "E": 18, "F": 18})
    sc.freeze_panes = "C4"
    SCROWS = dict(cost=cost_row, rev=rev_row, ads=ads_row, net=net_row, eps=total_eps_row,
                  voice=voice_row, llm=llm_row, fixed=fixed_row, dl=dl_row,
                  net_rev=net_rev_row, net_only=net_only_row)

    # ============================================================ Cost Lines
    cl = wb.create_sheet("Cost Lines")
    title(cl, "Cost-out — every cost line by scenario (monthly unless one-time)",
          "Variable lines link to Scenarios; fixed lines = unit cost × quantity. Edit blue cells.")
    header(cl, 4, ["Category", "Item", "Vendor / plan", "Type", "Unit cost $/mo",
                   "Qty: Test", "Qty: Wave 1", "Qty: Scale", "Qty: Dominate", "", "", "", "Note / source"])
    header(cl, 4, ["$/mo Test", "$/mo Wave 1", "$/mo Scale", "$/mo Dominate"], col=10)
    r = 5
    for item, srow in (("Claude API — agents + web search", SCROWS["llm"]), ("ElevenLabs voice", SCROWS["voice"])):
        cl.cell(row=r, column=1, value="Variable")
        cl.cell(row=r, column=2, value=item)
        cl.cell(row=r, column=3, value="usage-based")
        cl.cell(row=r, column=4, value="variable")
        for j, col in enumerate(cols):
            calc(cl, f"{get_column_letter(10 + j)}{r}", f"={SC}!{col}{srow}", USD, link=True)
        cl.cell(row=r, column=14, value="From Scenarios (episodes × per-episode cost)")
        r += 1
    var_last = r - 1
    fixed_first = r
    for cat, item, vendor, unit, qtys, note in FIXED:
        cl.cell(row=r, column=1, value=cat)
        cl.cell(row=r, column=2, value=item)
        cl.cell(row=r, column=3, value=vendor)
        cl.cell(row=r, column=4, value="monthly")
        inp(cl, f"E{r}", unit, USD2)
        for j, q in enumerate(qtys):
            inp(cl, f"{get_column_letter(6 + j)}{r}", q, NUM)
            calc(cl, f"{get_column_letter(10 + j)}{r}", f"=$E{r}*{get_column_letter(6 + j)}{r}", USD)
        cl.cell(row=r, column=14, value=note)
        r += 1
    fixed_last = r - 1
    cl.cell(row=r, column=2, value="Fixed operating subtotal").font = F_BOLD
    for j in range(4):
        L = get_column_letter(10 + j)
        calc(cl, f"{L}{r}", f"=SUM({L}{fixed_first}:{L}{fixed_last})", USD, bold=True)
    fixed_total = r
    r += 1
    cl.cell(row=r, column=2, value="TOTAL MONTHLY (variable + fixed)").font = F_BOLD
    for j in range(4):
        L = get_column_letter(10 + j)
        calc(cl, f"{L}{r}", f"=SUM({L}5:{L}{var_last})+{L}{fixed_total}", USD, bold=True)
        cl[f"{L}{r}"].fill = FILL_SUB
    r += 2
    cl.cell(row=r, column=1, value="One-time startup costs").font = F_BOLD
    r += 1
    header(cl, r, ["Category", "Item", "", "", "Cost $", "", "", "", "", "", "", "", "Note / source"])
    ot_first = r + 1
    for cat, item, cost, note in ONE_TIME:
        r += 1
        cl.cell(row=r, column=1, value=cat)
        cl.cell(row=r, column=2, value=item)
        inp(cl, f"E{r}", cost, USD)
        cl.cell(row=r, column=13, value=note)
    r += 1
    cl.cell(row=r, column=2, value="Total one-time").font = F_BOLD
    calc(cl, f"E{r}", f"=SUM(E{ot_first}:E{r - 1})", USD, bold=True)
    onetime_ref = f"'Cost Lines'!$E${r}"
    widths(cl, {"A": 14, "B": 46, "C": 30, "D": 10, "E": 14, "F": 9, "G": 9, "H": 9, "I": 11,
                "J": 13, "K": 13, "L": 13, "M": 15, "N": 54})
    # patch the Scenarios fixed-cost links now that the subtotal row is known
    for j, col in enumerate(cols):
        sc[f"{col}{SCROWS['fixed']}"] = f"='Cost Lines'!{get_column_letter(10 + j)}{fixed_total}"
        sc[f"{col}{SCROWS['fixed']}"].font = F_LINK
        sc[f"{col}{SCROWS['fixed']}"].number_format = USD

    # ============================================================ 12-Month Plan
    pl = wb.create_sheet("12-Month Plan")
    title(pl, "12-month cash curve and payback", "Stage and audience ramp per month are set on Assumptions.")
    header(pl, 4, ["Month", "Stage", "Audience ramp", "Operating cost", "One-time cost", "Ad revenue",
                   "Other revenue", "Total revenue", "Net", "Cumulative cash", "Payback flag",
                   "Network-only net", "Network-only cumulative"])
    for m in range(1, 13):
        r = 4 + m
        L = get_column_letter(1 + m)
        calc(pl, f"A{r}", m, NUM)
        calc(pl, f"B{r}", f"={AS}!{L}${A['stage_row']}", NUM, link=True)
        calc(pl, f"C{r}", f"={AS}!{L}${A['ramp_row']}", PCT, link=True)
        calc(pl, f"D{r}", f"=INDEX({SC}!$C${SCROWS['cost']}:$F${SCROWS['cost']},B{r})", USD)
        calc(pl, f"E{r}", f"={onetime_ref}" if m == 1 else "=0", USD)
        calc(pl, f"F{r}", f"=INDEX({SC}!$C${SCROWS['ads']}:$F${SCROWS['ads']},B{r})*C{r}", USD)
        calc(pl, f"G{r}", f"=(INDEX({SC}!$C${SCROWS['rev']}:$F${SCROWS['rev']},B{r})"
                          f"-INDEX({SC}!$C${SCROWS['ads']}:$F${SCROWS['ads']},B{r}))*C{r}", USD)
        calc(pl, f"H{r}", f"=F{r}+G{r}", USD)
        calc(pl, f"I{r}", f"=H{r}-D{r}-E{r}", USD, bold=True)
        calc(pl, f"J{r}", f"=I{r}" if m == 1 else f"=J{r - 1}+I{r}", USD, bold=True)
        calc(pl, f"K{r}", f"=IF(J{r}>=0,IF({'TRUE' if m == 1 else f'J{r - 1}<0'},A{r},\"\"),\"\")", NUM)
        calc(pl, f"L{r}", f"=INDEX({SC}!$C${SCROWS['net_rev']}:$F${SCROWS['net_rev']},B{r})*C{r}-D{r}-E{r}", USD)
        calc(pl, f"M{r}", f"=L{r}" if m == 1 else f"=M{r - 1}+L{r}", USD)
    note = ("Every show in a stage publishes from its first month, so operating cost is charged in full; "
            "only revenue follows the audience ramp (conservative on purpose).")
    pl["A18"] = note
    pl["A18"].font = Font(name=ARIAL, italic=True, color="555555")
    pl["A20"], pl["A21"], pl["A22"], pl["A23"], pl["A24"], pl["A25"], pl["A26"] = (
        "Payback month", "Lowest cash point (max investment needed)", "Year-1 revenue", "Year-1 total cost",
        "Year-1 ROI (net ÷ total cost)", "Network-only: lowest cash point", "Network-only: year-1 cumulative net")
    calc(pl, "D25", "=MIN(0,MIN(M5:M16))", USD, bold=True)
    calc(pl, "D26", "=M16", USD, bold=True)
    for a in ("A20", "A21", "A22", "A23", "A24", "A25", "A26"):
        pl[a].font = F_BOLD
    calc(pl, "D20", '=IF(COUNT(K5:K16)=0,"Not within 12 months",MIN(K5:K16))', NUM, bold=True)
    calc(pl, "D21", "=MIN(0,MIN(J5:J16))", USD, bold=True)
    calc(pl, "D22", "=SUM(H5:H16)", USD, bold=True)
    calc(pl, "D23", "=SUM(D5:D16)+SUM(E5:E16)", USD, bold=True)
    calc(pl, "D24", "=IF(D23=0,0,(D22-D23)/D23)", PCT, bold=True)
    for a in ("D20", "D21", "D22", "D23", "D24", "D25", "D26"):
        pl[a].fill = FILL_KEY
    widths(pl, {"A": 40, "B": 8, "C": 14, "D": 16, "E": 14, "F": 14, "G": 14, "H": 14, "I": 14, "J": 16, "K": 12, "L": 16, "M": 20})

    # ============================================================ Sensitivity
    se = wb.create_sheet("Sensitivity")
    title(se, "Sensitivity — monthly net at the Scale scenario",
          "Rows: gross programmatic CPM. Columns: average downloads per episode across the network. "
          "Other revenue and all costs held at the Scale scenario.")
    cpms = [5, 8, 10, 15, 20, 25, 30]
    dls = [25, 50, 100, 250, 500, 1000, 2500]
    se["A4"] = "CPM ↓  /  downloads per episode →"
    se["A4"].font = F_BOLD
    for j, d in enumerate(dls):
        inp(se, f"{get_column_letter(2 + j)}4", d, NUM)
    avg_ads = (f"(SUMPRODUCT({SC}!E{first_eps}:E{last_eps},{AS}!$F${ws_types[0]}:$F${ws_types[1]})"
               f"/MAX(1,{SC}!E{total_eps_row}))")
    other = f"({SC}!E{SCROWS['rev']}-{SC}!E{SCROWS['ads']})"
    for i, cpm in enumerate(cpms):
        r = 5 + i
        inp(se, f"A{r}", cpm, USD)
        for j in range(len(dls)):
            L = get_column_letter(2 + j)
            calc(se, f"{L}{r}", f"={SC}!$E${total_eps_row}*{L}$4*{avg_ads}/1000*$A{r}"
                                f"*{A['rev']['fill']}*{A['rev']['share']}+{other}-{SC}!$E${SCROWS['cost']}", USD)
    r = 5 + len(cpms) + 2
    se[f"A{r}"] = "Break-even downloads per episode (ads only), by CPM — Scale scenario costs"
    se[f"A{r}"].font = F_BOLD
    r += 1
    header(se, r, ["CPM", "Break-even downloads / episode (network average)"])
    for i, cpm in enumerate(cpms):
        rr = r + 1 + i
        inp(se, f"A{rr}", cpm, USD)
        calc(se, f"B{rr}", f"=IFERROR(({SC}!$E${SCROWS['cost']}-{other})/({SC}!$E${total_eps_row}*{avg_ads}/1000*A{rr}"
                           f"*{A['rev']['fill']}*{A['rev']['share']}),0)", NUM)
    widths(se, {"A": 34, **{get_column_letter(2 + j): 14 for j in range(len(dls))}})

    # ============================================================ Start Here (first tab)
    st = wb.create_sheet("Start Here", 0)
    title(st, "Project Earlobe — cost-out & ROI model (Curious & Creative Network)",
          "Prices as of Oct 2026 — verify before buying. Built by finance/build_cost_model.py.")
    lines = [
        ("How to use", ""),
        ("1.", "Change inputs only on the Assumptions tab (blue text; yellow = key levers)."),
        ("2.", "Pick the revenue case (Conservative / Base / Optimistic) at the top of Assumptions."),
        ("3.", "Read results on Scenarios (monthly steady state), 12-Month Plan (cash + payback) and Sensitivity."),
        ("Colors", "Blue = input · Black = formula · Green = link to another tab · Yellow fill = key lever"),
        ("Scenarios", "Test = Columbia + LA + national shows · Wave 1 = + NYC/Chicago/more, first niche feeds · "
                      "Scale = 25 markets, 150+ shows · Dominate = 100 markets, ~700 shows"),
        ("Honesty note", "Downloads, CPM fill and sponsor counts are estimates until real analytics arrive. "
                         "Replace them with actuals monthly; the Finance/Bookkeeping Reporter agent does this."),
    ]
    rr = 4
    for a, b in lines:
        st[f"A{rr}"], st[f"B{rr}"] = a, b
        st[f"A{rr}"].font = F_BOLD
        rr += 1
    rr += 1
    header(st, rr, ["Headline (current revenue case)", ""] + SCEN)
    for label, srow, fmt in (("Shows", total_shows_row, NUM), ("Episodes / month", SCROWS["eps"], NUM),
                             ("Downloads / month", SCROWS["dl"], NUM), ("Total monthly cost", SCROWS["cost"], USD),
                             ("Total monthly revenue", SCROWS["rev"], USD), ("Net / month", SCROWS["net"], USD),
                             ("Network-only net / month (no B2B/API/services)", SCROWS["net_only"], USD)):
        rr += 1
        st[f"A{rr}"] = label
        for j, col in enumerate(cols):
            calc(st, f"{col}{rr}", f"={SC}!{col}{srow}", fmt, link=True)
    rr += 2
    st[f"A{rr}"] = "Payback month (12-Month Plan)"
    calc(st, f"C{rr}", "='12-Month Plan'!D20", NUM, link=True)
    rr += 1
    st[f"A{rr}"] = "Max cash needed before payback"
    calc(st, f"C{rr}", "='12-Month Plan'!D21", USD, link=True)
    rr += 1
    st[f"A{rr}"] = "Year-1 ROI"
    calc(st, f"C{rr}", "='12-Month Plan'!D24", PCT, link=True)
    widths(st, {"A": 34, "B": 90, "C": 16, "D": 16, "E": 16, "F": 16})

    # ============================================================ Sources
    so = wb.create_sheet("Sources")
    title(so, "Sources", "Full citations with links: docs/research/facts-and-figures.md (IDs F-...).")
    src = [
        ("F-LLM", "Anthropic API list prices by tier, web search $10/1k, batch 50% off, cache reads 0.1× (Oct 2026)"),
        ("F-TTS", "ElevenLabs pricing page: Creator $22/121k, Pro $99/600k, Scale $299/1.8M, Business $990/6M credits"),
        ("F-HOST", "Podcast host plans with dynamic ad insertion and programmatic marketplaces"),
        ("F-ADS", "Podcast CPM benchmarks (programmatic ~$5–$25), fill and revenue share"),
        ("F-LEGAL", "Media liability insurance (~$78/mo avg, Insureon); USPTO $350/class; DBA fees"),
        ("F-DATA", "RSS, GDELT, CourtListener free tiers; paid news APIs"),
        ("inference", "Downloads per episode, sponsor counts, B2B/API/services volumes and rates are planning estimates"),
    ]
    header(so, 4, ["ID", "What"])
    for i, (a, b) in enumerate(src):
        so[f"A{5 + i}"], so[f"B{5 + i}"] = a, b
    widths(so, {"A": 14, "B": 120})

    for sheet in wb.worksheets:
        style_all(sheet)
    wb.save(OUT)
    return OUT


if __name__ == "__main__":
    print(build())
