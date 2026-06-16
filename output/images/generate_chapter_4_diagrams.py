from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
NAVY = "#0B1D3A"
NAVY2 = "#162B52"
TEAL = "#0B7285"
GOLD = "#C9962A"
GREEN = "#166534"
GRAY = "#6B7280"
CREAM = "#F7F4EF"


def font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/seguisb.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


F_TITLE = font(25, True)
F_HEAD = font(14, True)
F_BODY = font(11)


def defs():
    return f"""
  <defs>
    <marker id="arrow_navy" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{NAVY}"/></marker>
    <marker id="arrow_green" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{GREEN}"/></marker>
    <marker id="arrow_gold" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{GOLD}"/></marker>
  </defs>"""


def svg_box(x, y, w, h, title, lines, header=NAVY2, stroke=NAVY):
    cx = x + w / 2
    out = [
        f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{CREAM}" stroke="{stroke}" stroke-width="1.4"/>',
        f'  <rect x="{x}" y="{y}" width="{w}" height="22" rx="2" fill="{header}"/>',
        f'  <text x="{cx}" y="{y + 15}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8" fill="white" font-weight="600">{title}</text>',
    ]
    ty = y + 37
    for text, color, weight in lines:
        out.append(f'  <text x="{x + 7}" y="{ty}" font-family="JetBrains Mono, monospace" font-size="6.8" fill="{color}" font-weight="{weight}">{text}</text>')
        ty += 12
    return "\n".join(out)


def save_svg(name, viewbox, body):
    (BASE / f"{name}.svg").write_text(
        f'<svg viewBox="{viewbox}" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto;">\n{defs()}\n{body}\n</svg>\n',
        encoding="utf-8",
    )


def sp(p, s):
    return int(round(p[0] * s)), int(round(p[1] * s))


def draw_box(d, box, title, lines, s, header=NAVY2, stroke=NAVY):
    x, y, w, h = box
    d.rounded_rectangle((*sp((x, y), s), *sp((x + w, y + h), s)), radius=2 * s, fill=CREAM, outline=stroke, width=max(1, int(1.4 * s)))
    d.rounded_rectangle((*sp((x, y), s), *sp((x + w, y + 22), s)), radius=2 * s, fill=header, outline=header)
    tb = d.textbbox((0, 0), title, font=F_HEAD)
    d.text((int((x + w / 2) * s - (tb[2] - tb[0]) / 2), int((y + 4) * s)), title, fill="white", font=F_HEAD)
    ty = int((y + 31) * s)
    for text, color, weight in lines:
        d.text((int((x + 7) * s), ty), text, fill=color, font=F_HEAD if weight == "600" else F_BODY)
        ty += int(12 * s)


def arrow(d, p1, p2, color, s):
    x1, y1 = sp(p1, s)
    x2, y2 = sp(p2, s)
    d.line((x1, y1, x2, y2), fill=color, width=max(1, int(1.4 * s)))
    dx, dy = x2 - x1, y2 - y1
    if abs(dx) >= abs(dy):
        sign = 1 if dx >= 0 else -1
        pts = [(x2, y2), (x2 - sign * int(7 * s), y2 - int(4 * s)), (x2 - sign * int(7 * s), y2 + int(4 * s))]
    else:
        sign = 1 if dy >= 0 else -1
        pts = [(x2, y2), (x2 - int(4 * s), y2 - sign * int(7 * s)), (x2 + int(4 * s), y2 - sign * int(7 * s))]
    d.polygon(pts, fill=color)


def path_arrow(d, pts, color, s):
    d.line([sp(p, s) for p in pts], fill=color, width=max(1, int(1.4 * s)))
    arrow(d, pts[-2], pts[-1], color, s)


def save_png(name, size, draw_fn):
    s = 2
    img = Image.new("RGB", (size[0] * s, size[1] * s), "white")
    draw_fn(ImageDraw.Draw(img), s)
    img.save(BASE / f"{name}.png")


def navigation():
    body = f"""
  <text x="25" y="28" font-family="JetBrains Mono, monospace" font-size="14" fill="{NAVY}" font-weight="700">Frontend Routing and Role-Based Navigation</text>
{svg_box(35, 145, 110, 78, "APP_TSX", [("providers", GRAY, "400"), ("routes", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(185, 70, 115, 78, "AUTH", [("PKCE callback", GRAY, "400"), ("token storage", GREEN, "600")], header=GREEN, stroke=GREEN)}
{svg_box(185, 220, 115, 78, "AUTH_GUARD", [("isAuthenticated", GRAY, "400"), ("redirect /auth", TEAL, "600")], header=NAVY2, stroke=NAVY)}
{svg_box(345, 145, 115, 78, "INDEX", [("AppSidebar", GRAY, "400"), ("selectedModule", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(505, 70, 115, 78, "BUSINESS_VIEW", [("BANK", GRAY, "400"), ("ANCHOR/CP", TEAL, "600")], header=GOLD, stroke=GOLD)}
{svg_box(505, 220, 145, 78, "FEATURE_MODULES", [("dashboard/master", GRAY, "400"), ("invoice/disburse", TEAL, "600")], header=NAVY2, stroke=NAVY)}
  <line x1="145" y1="164" x2="184" y2="109" stroke="{GREEN}" stroke-width="1.4" marker-end="url(#arrow_green)"/>
  <line x1="145" y1="204" x2="184" y2="259" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <line x1="300" y1="259" x2="344" y2="184" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <line x1="460" y1="164" x2="504" y2="109" stroke="{GOLD}" stroke-width="1.4" marker-end="url(#arrow_gold)"/>
  <line x1="460" y1="204" x2="504" y2="259" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
"""
    save_svg("ch4_navigation_role_flow", "0 0 690 330", body)

    def draw_fn(d, s):
        d.text(sp((25, 13), s), "Frontend Routing and Role-Based Navigation", font=F_TITLE, fill=NAVY)
        boxes = [
            ((35,145,110,78),"APP_TSX",[("providers",GRAY,"400"),("routes",TEAL,"600")],TEAL,TEAL),
            ((185,70,115,78),"AUTH",[("PKCE callback",GRAY,"400"),("token storage",GREEN,"600")],GREEN,GREEN),
            ((185,220,115,78),"AUTH_GUARD",[("isAuthenticated",GRAY,"400"),("redirect /auth",TEAL,"600")],NAVY2,NAVY),
            ((345,145,115,78),"INDEX",[("AppSidebar",GRAY,"400"),("selectedModule",TEAL,"600")],TEAL,TEAL),
            ((505,70,115,78),"BUSINESS_VIEW",[("BANK",GRAY,"400"),("ANCHOR/CP",TEAL,"600")],GOLD,GOLD),
            ((505,220,145,78),"FEATURE_MODULES",[("dashboard/master",GRAY,"400"),("invoice/disburse",TEAL,"600")],NAVY2,NAVY),
        ]
        for b,t,l,h,st in boxes:
            draw_box(d,b,t,l,s,h,st)
        for p1,p2,c in [((145,164),(184,109),GREEN),((145,204),(184,259),NAVY),((300,259),(344,184),NAVY),((460,164),(504,109),GOLD),((460,204),(504,259),NAVY)]:
            arrow(d,p1,p2,c,s)

    save_png("ch4_navigation_role_flow", (690, 330), draw_fn)


def invoice_upload():
    body = f"""
  <text x="25" y="28" font-family="JetBrains Mono, monospace" font-size="14" fill="{NAVY}" font-weight="700">Invoice Upload Component Flow</text>
{svg_box(35, 145, 130, 82, "UPLOAD_FORM", [("orchestrator", GRAY, "400"), ("program context", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(215, 55, 125, 78, "EXCEL_UPLOADER", [(".xlsx/.xls", GRAY, "400"), ("drag-drop", TEAL, "600")], header=NAVY2, stroke=NAVY)}
{svg_box(215, 235, 125, 78, "SCANNED_UPLOAD", [("PDF/images", GRAY, "400"), ("OCR path", GOLD, "600")], header=GOLD, stroke=GOLD)}
{svg_box(390, 145, 125, 82, "UPLOAD_TABLE", [("row validation", GRAY, "400"), ("errors/warnings", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(565, 55, 125, 78, "SUMMARY_CARD", [("valid/warning", GRAY, "400"), ("error totals", TEAL, "600")], header=NAVY2, stroke=NAVY)}
{svg_box(565, 235, 125, 78, "REPORTS", [("eligibility", GRAY, "400"), ("rejection file", GOLD, "600")], header=GOLD, stroke=GOLD)}
  <line x1="165" y1="166" x2="214" y2="94" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <line x1="165" y1="206" x2="214" y2="274" stroke="{GOLD}" stroke-width="1.4" marker-end="url(#arrow_gold)"/>
  <line x1="340" y1="94" x2="389" y2="166" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <line x1="340" y1="274" x2="389" y2="206" stroke="{GOLD}" stroke-width="1.4" marker-end="url(#arrow_gold)"/>
  <line x1="515" y1="166" x2="564" y2="94" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <line x1="515" y1="206" x2="564" y2="274" stroke="{GOLD}" stroke-width="1.4" marker-end="url(#arrow_gold)"/>
"""
    save_svg("ch4_invoice_upload_flow", "0 0 720 340", body)

    def draw_fn(d, s):
        d.text(sp((25,13),s), "Invoice Upload Component Flow", font=F_TITLE, fill=NAVY)
        boxes = [
            ((35,145,130,82),"UPLOAD_FORM",[("orchestrator",GRAY,"400"),("program context",TEAL,"600")],TEAL,TEAL),
            ((215,55,125,78),"EXCEL_UPLOADER",[(".xlsx/.xls",GRAY,"400"),("drag-drop",TEAL,"600")],NAVY2,NAVY),
            ((215,235,125,78),"SCANNED_UPLOAD",[("PDF/images",GRAY,"400"),("OCR path",GOLD,"600")],GOLD,GOLD),
            ((390,145,125,82),"UPLOAD_TABLE",[("row validation",GRAY,"400"),("errors/warnings",TEAL,"600")],TEAL,TEAL),
            ((565,55,125,78),"SUMMARY_CARD",[("valid/warning",GRAY,"400"),("error totals",TEAL,"600")],NAVY2,NAVY),
            ((565,235,125,78),"REPORTS",[("eligibility",GRAY,"400"),("rejection file",GOLD,"600")],GOLD,GOLD),
        ]
        for b,t,l,h,st in boxes:
            draw_box(d,b,t,l,s,h,st)
        for p1,p2,c in [((165,166),(214,94),NAVY),((165,206),(214,274),GOLD),((340,94),(389,166),NAVY),((340,274),(389,206),GOLD),((515,166),(564,94),NAVY),((515,206),(564,274),GOLD)]:
            arrow(d,p1,p2,c,s)

    save_png("ch4_invoice_upload_flow", (720, 340), draw_fn)


def disbursement_wizard():
    steps = [
        ("PROGRAM", "select program", 35),
        ("INVOICES", "eligible invoices", 145),
        ("FINANCE", "terms + fees", 255),
        ("ACCOUNTING", "debit/credit", 365),
        ("REPAYMENT", "schedule", 475),
        ("REVIEW", "submit", 585),
    ]
    body = f'  <text x="25" y="28" font-family="JetBrains Mono, monospace" font-size="14" fill="{NAVY}" font-weight="700">Finance Disbursement Six-Step Wizard</text>\n'
    for title, line, x in steps:
        header = TEAL if title not in ("ACCOUNTING", "REVIEW") else GOLD
        stroke = TEAL if title not in ("ACCOUNTING", "REVIEW") else GOLD
        body += svg_box(x, 135, 90, 78, title, [(line, GRAY, "400"), ("wizard pane", TEAL if header == TEAL else GOLD, "600")], header=header, stroke=stroke) + "\n"
    for i in range(len(steps) - 1):
        x1 = steps[i][2] + 90
        x2 = steps[i + 1][2] - 1
        body += f'  <line x1="{x1}" y1="174" x2="{x2}" y2="174" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>\n'
    save_svg("ch4_finance_disbursement_wizard", "0 0 700 260", body)

    def draw_fn(d, s):
        d.text(sp((25,13),s), "Finance Disbursement Six-Step Wizard", font=F_TITLE, fill=NAVY)
        for title,line,x in steps:
            h = TEAL if title not in ("ACCOUNTING","REVIEW") else GOLD
            draw_box(d,(x,135,90,78),title,[(line,GRAY,"400"),("wizard pane",TEAL if h==TEAL else GOLD,"600")],s,h,h)
        for i in range(len(steps)-1):
            arrow(d,(steps[i][2]+90,174),(steps[i+1][2]-1,174),NAVY,s)

    save_png("ch4_finance_disbursement_wizard", (700, 260), draw_fn)


def services_layer():
    body = f"""
  <text x="25" y="28" font-family="JetBrains Mono, monospace" font-size="14" fill="{NAVY}" font-weight="700">Frontend Services Layer</text>
{svg_box(35, 140, 120, 82, "COMPONENTS", [("forms/tables", GRAY, "400"), ("modals/wizards", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(205, 140, 120, 82, "HOOKS", [("useProgramForm", GRAY, "400"), ("useInvoiceForm", TEAL, "600")], header=NAVY2, stroke=NAVY)}
{svg_box(375, 140, 125, 82, "SERVICES", [("typed functions", GRAY, "400"), ("endpoint mapping", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(550, 60, 120, 78, "API_CLIENT", [("Axios", GRAY, "400"), ("Bearer token", GREEN, "600")], header=GREEN, stroke=GREEN)}
{svg_box(550, 230, 120, 78, "TYPES", [("invoiceUpload.ts", GRAY, "400"), ("scfTransaction.ts", TEAL, "600")], header=GOLD, stroke=GOLD)}
  <line x1="155" y1="181" x2="204" y2="181" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <line x1="325" y1="181" x2="374" y2="181" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <line x1="500" y1="161" x2="549" y2="99" stroke="{GREEN}" stroke-width="1.4" marker-end="url(#arrow_green)"/>
  <line x1="500" y1="201" x2="549" y2="269" stroke="{GOLD}" stroke-width="1.4" marker-end="url(#arrow_gold)"/>
"""
    save_svg("ch4_services_layer", "0 0 700 335", body)

    def draw_fn(d, s):
        d.text(sp((25,13),s), "Frontend Services Layer", font=F_TITLE, fill=NAVY)
        boxes = [
            ((35,140,120,82),"COMPONENTS",[("forms/tables",GRAY,"400"),("modals/wizards",TEAL,"600")],TEAL,TEAL),
            ((205,140,120,82),"HOOKS",[("useProgramForm",GRAY,"400"),("useInvoiceForm",TEAL,"600")],NAVY2,NAVY),
            ((375,140,125,82),"SERVICES",[("typed functions",GRAY,"400"),("endpoint mapping",TEAL,"600")],TEAL,TEAL),
            ((550,60,120,78),"API_CLIENT",[("Axios",GRAY,"400"),("Bearer token",GREEN,"600")],GREEN,GREEN),
            ((550,230,120,78),"TYPES",[("invoiceUpload.ts",GRAY,"400"),("scfTransaction.ts",TEAL,"600")],GOLD,GOLD),
        ]
        for b,t,l,h,st in boxes:
            draw_box(d,b,t,l,s,h,st)
        for p1,p2,c in [((155,181),(204,181),NAVY),((325,181),(374,181),NAVY),((500,161),(549,99),GREEN),((500,201),(549,269),GOLD)]:
            arrow(d,p1,p2,c,s)

    save_png("ch4_services_layer", (700, 335), draw_fn)


if __name__ == "__main__":
    navigation()
    invoice_upload()
    disbursement_wizard()
    services_layer()
    print("Generated Chapter IV diagrams in", BASE)
