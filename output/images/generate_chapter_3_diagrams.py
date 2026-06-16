from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent

NAVY = "#0B1D3A"
NAVY2 = "#162B52"
TEAL = "#0B7285"
GOLD = "#C9962A"
GREEN = "#166534"
RED = "#B91C1C"
ORANGE = "#C2410C"
GRAY = "#6B7280"
CREAM = "#F7F4EF"
WARM = "#F0EDE8"


def font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/seguisb.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
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
    <marker id="arrow_gray" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{GRAY}"/></marker>
    <marker id="arrow_green" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{GREEN}"/></marker>
    <marker id="arrow_gold" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{GOLD}"/></marker>
    <marker id="arrow_red" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{RED}"/></marker>
  </defs>"""


def svg_box(x, y, w, h, title, lines, header=NAVY2, stroke=NAVY, fill=CREAM):
    cx = x + w / 2
    out = [
        f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>',
        f'  <rect x="{x}" y="{y}" width="{w}" height="22" rx="2" fill="{header}"/>',
        f'  <text x="{cx}" y="{y + 15}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8" fill="white" font-weight="600">{title}</text>',
    ]
    ty = y + 37
    for text, color, weight in lines:
        out.append(f'  <text x="{x + 7}" y="{ty}" font-family="JetBrains Mono, monospace" font-size="6.8" fill="{color}" font-weight="{weight}">{text}</text>')
        ty += 12
    return "\n".join(out)


def svg_state(x, y, w, text, fill):
    return f'  <rect x="{x}" y="{y}" width="{w}" height="28" rx="14" fill="{fill}"/>\n  <text x="{x + w / 2}" y="{y + 18}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8" fill="white" font-weight="600">{text}</text>'


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


def arrow(d, p1, p2, color, s, width=1.4):
    x1, y1 = sp(p1, s)
    x2, y2 = sp(p2, s)
    d.line((x1, y1, x2, y2), fill=color, width=max(1, int(width * s)))
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


def data_model():
    body = f"""
  <text x="25" y="28" font-family="JetBrains Mono, monospace" font-size="14" fill="{NAVY}" font-weight="700">SCF Core Data Model</text>
{svg_box(305, 45, 145, 86, "BASE_ENTITY", [("id / version", GRAY, "400"), ("createdBy / date", GRAY, "400"), ("approvalStatus", TEAL, "600"), ("pendingAction", TEAL, "600")], header=NAVY2)}
{svg_box(35, 175, 135, 86, "COUNTERPARTY", [("companyName", GRAY, "400"), ("taxId / regNo", GRAY, "400"), ("role + status", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(35, 300, 135, 74, "BANK_ACCOUNT", [("accountNumber", GRAY, "400"), ("IBAN / SWIFT", GRAY, "400")], header=NAVY2)}
{svg_box(205, 300, 135, 74, "DOCUMENT", [("filePath", GRAY, "400"), ("bucketName", TEAL, "600")], header=NAVY2)}
{svg_box(305, 175, 145, 86, "PROGRAM", [("reference", GRAY, "400"), ("productType", GRAY, "400"), ("limits + dates", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(585, 175, 135, 86, "ANCHOR", [("anchorName", GRAY, "400"), ("anchorCode", GRAY, "400"), ("anchorRole", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(475, 300, 135, 74, "FEE_CATALOGUE", [("feeItems JSON", GRAY, "400"), ("flatFeeConfig", TEAL, "600")], header=GOLD, stroke=GOLD)}
{svg_box(635, 300, 115, 74, "CASHFLOW", [("invoiceNumber", GRAY, "400"), ("validation", TEAL, "600")], header=GOLD, stroke=GOLD)}
{svg_box(475, 60, 135, 74, "PRODUCT_DEF", [("productCode", GRAY, "400"), ("instrument", TEAL, "600")], header=NAVY2)}
  <line x1="377" y1="131" x2="377" y2="174" stroke="{GRAY}" stroke-width="1.2" stroke-dasharray="5 2" marker-end="url(#arrow_gray)"/>
  <line x1="170" y1="218" x2="304" y2="218" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <line x1="450" y1="218" x2="584" y2="218" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <line x1="542" y1="134" x2="378" y2="174" stroke="{GRAY}" stroke-width="1.2" stroke-dasharray="5 2" marker-end="url(#arrow_gray)"/>
  <line x1="102" y1="261" x2="102" y2="299" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <line x1="150" y1="261" x2="240" y2="299" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <line x1="395" y1="261" x2="542" y2="299" stroke="{GOLD}" stroke-width="1.4" marker-end="url(#arrow_gold)"/>
  <line x1="430" y1="261" x2="692" y2="299" stroke="{GOLD}" stroke-width="1.4" marker-end="url(#arrow_gold)"/>
"""
    save_svg("ch3_core_data_model", "0 0 780 395", body)

    def draw_fn(d, s):
        d.text(sp((25, 13), s), "SCF Core Data Model", font=F_TITLE, fill=NAVY)
        for box, title, lines, header, stroke in [
            ((305,45,145,86),"BASE_ENTITY",[("id / version",GRAY,"400"),("createdBy / date",GRAY,"400"),("approvalStatus",TEAL,"600"),("pendingAction",TEAL,"600")],NAVY2,NAVY),
            ((35,175,135,86),"COUNTERPARTY",[("companyName",GRAY,"400"),("taxId / regNo",GRAY,"400"),("role + status",TEAL,"600")],TEAL,TEAL),
            ((35,300,135,74),"BANK_ACCOUNT",[("accountNumber",GRAY,"400"),("IBAN / SWIFT",GRAY,"400")],NAVY2,NAVY),
            ((205,300,135,74),"DOCUMENT",[("filePath",GRAY,"400"),("bucketName",TEAL,"600")],NAVY2,NAVY),
            ((305,175,145,86),"PROGRAM",[("reference",GRAY,"400"),("productType",GRAY,"400"),("limits + dates",TEAL,"600")],TEAL,TEAL),
            ((585,175,135,86),"ANCHOR",[("anchorName",GRAY,"400"),("anchorCode",GRAY,"400"),("anchorRole",TEAL,"600")],TEAL,TEAL),
            ((475,300,135,74),"FEE_CATALOGUE",[("feeItems JSON",GRAY,"400"),("flatFeeConfig",TEAL,"600")],GOLD,GOLD),
            ((635,300,115,74),"CASHFLOW",[("invoiceNumber",GRAY,"400"),("validation",TEAL,"600")],GOLD,GOLD),
            ((475,60,135,74),"PRODUCT_DEF",[("productCode",GRAY,"400"),("instrument",TEAL,"600")],NAVY2,NAVY),
        ]:
            draw_box(d, box, title, lines, s, header, stroke)
        for p1,p2,c in [((377,131),(377,174),GRAY),((170,218),(304,218),NAVY),((450,218),(584,218),NAVY),((542,134),(378,174),GRAY),((102,261),(102,299),NAVY),((150,261),(240,299),NAVY),((395,261),(542,299),GOLD),((430,261),(692,299),GOLD)]:
            arrow(d,p1,p2,c,s)

    save_png("ch3_core_data_model", (780, 395), draw_fn)


def governance_state():
    body = f"""
  <text x="25" y="30" font-family="JetBrains Mono, monospace" font-size="14" fill="{NAVY}" font-weight="700">Maker/Checker Governance Lifecycle</text>
  <circle cx="70" cy="155" r="8" fill="{NAVY}"/>
{svg_state(120, 141, 105, "DRAFT", TEAL)}
{svg_state(290, 141, 150, "PENDING_APPROVAL", GOLD)}
{svg_state(515, 80, 110, "APPROVED", GREEN)}
{svg_state(515, 205, 110, "REJECTED", RED)}
  <circle cx="700" cy="94" r="6" fill="{GREEN}"/>
  <line x1="78" y1="155" x2="119" y2="155" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
  <line x1="225" y1="155" x2="289" y2="155" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
  <text x="257" y="149" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="7" fill="{NAVY}">submit</text>
  <line x1="440" y1="149" x2="514" y2="94" stroke="{GREEN}" stroke-width="1.5" marker-end="url(#arrow_green)"/>
  <text x="475" y="113" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="7" fill="{GREEN}">checker approves</text>
  <line x1="440" y1="161" x2="514" y2="219" stroke="{RED}" stroke-width="1.5" marker-end="url(#arrow_red)"/>
  <text x="475" y="197" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="7" fill="{RED}">checker rejects</text>
  <line x1="625" y1="94" x2="693" y2="94" stroke="{GREEN}" stroke-width="1.5" marker-end="url(#arrow_green)"/>
  <path d="M 515,219 L 235,219 L 235,169" fill="none" stroke="{GRAY}" stroke-width="1.2" stroke-dasharray="5 2" marker-end="url(#arrow_gray)"/>
  <text x="365" y="213" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="7" fill="{GRAY}">restore originalData on update rejection</text>
"""
    save_svg("ch3_maker_checker_state", "0 0 750 280", body)

    def draw_fn(d, s):
        d.text(sp((25, 14), s), "Maker/Checker Governance Lifecycle", font=F_TITLE, fill=NAVY)
        # PNG preview uses simple boxes to mirror the SVG.
        for x,y,w,t,c in [(120,141,105,"DRAFT",TEAL),(290,141,150,"PENDING_APPROVAL",GOLD),(515,80,110,"APPROVED",GREEN),(515,205,110,"REJECTED",RED)]:
            d.rounded_rectangle((*sp((x,y),s),*sp((x+w,y+28),s)),radius=14*s,fill=c)
            tb=d.textbbox((0,0),t,font=F_HEAD)
            d.text((int((x+w/2)*s-(tb[2]-tb[0])/2),int((y+6)*s)),t,fill="white",font=F_HEAD)
        d.ellipse((*sp((62,147),s),*sp((78,163),s)),fill=NAVY)
        d.ellipse((*sp((694,88),s),*sp((706,100),s)),fill=GREEN)
        for p1,p2,c in [((78,155),(119,155),NAVY),((225,155),(289,155),NAVY),((440,149),(514,94),GREEN),((440,161),(514,219),RED),((625,94),(693,94),GREEN)]:
            arrow(d,p1,p2,c,s)
        path_arrow(d,[(515,219),(235,219),(235,169)],GRAY,s)

    save_png("ch3_maker_checker_state", (750, 280), draw_fn)


def module_flow():
    body = f"""
  <text x="25" y="30" font-family="JetBrains Mono, monospace" font-size="14" fill="{NAVY}" font-weight="700">Program Configuration Functional Flow</text>
{svg_box(35, 120, 115, 82, "PRODUCT_DEF", [("product type", GRAY, "400"), ("instrument", TEAL, "600")], header=NAVY2)}
{svg_box(190, 120, 125, 82, "GENERAL_STEP", [("program info", GRAY, "400"), ("anchor + parties", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(355, 120, 125, 82, "FEE_STEP", [("fee items", GRAY, "400"), ("flat fee JSON", GOLD, "600")], header=GOLD, stroke=GOLD)}
{svg_box(520, 120, 135, 82, "CASHFLOW_STEP", [("disbursement", GRAY, "400"), ("repayment rules", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(285, 260, 150, 82, "PROGRAM_DRAFT", [("mapped entities", GRAY, "400"), ("copy excludes flows", TEAL, "600")], header=NAVY2)}
  <line x1="150" y1="161" x2="189" y2="161" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
  <line x1="315" y1="161" x2="354" y2="161" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
  <line x1="480" y1="161" x2="519" y2="161" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
  <path d="M 252,202 L 252,240 L 360,240 L 360,259" fill="none" stroke="{TEAL}" stroke-width="1.5" marker-end="url(#arrow_green)"/>
  <path d="M 417,202 L 417,240 L 360,240" fill="none" stroke="{GOLD}" stroke-width="1.5" marker-end="url(#arrow_gold)"/>
  <path d="M 587,202 L 587,240 L 435,240 L 435,259" fill="none" stroke="{TEAL}" stroke-width="1.5" marker-end="url(#arrow_green)"/>
"""
    save_svg("ch3_program_configuration_flow", "0 0 700 370", body)

    def draw_fn(d, s):
        d.text(sp((25,14),s),"Program Configuration Functional Flow",font=F_TITLE,fill=NAVY)
        for box,title,lines,header,stroke in [
            ((35,120,115,82),"PRODUCT_DEF",[("product type",GRAY,"400"),("instrument",TEAL,"600")],NAVY2,NAVY),
            ((190,120,125,82),"GENERAL_STEP",[("program info",GRAY,"400"),("anchor + parties",TEAL,"600")],TEAL,TEAL),
            ((355,120,125,82),"FEE_STEP",[("fee items",GRAY,"400"),("flat fee JSON",GOLD,"600")],GOLD,GOLD),
            ((520,120,135,82),"CASHFLOW_STEP",[("disbursement",GRAY,"400"),("repayment rules",TEAL,"600")],TEAL,TEAL),
            ((285,260,150,82),"PROGRAM_DRAFT",[("mapped entities",GRAY,"400"),("copy excludes flows",TEAL,"600")],NAVY2,NAVY),
        ]:
            draw_box(d,box,title,lines,s,header,stroke)
        for p1,p2,c in [((150,161),(189,161),NAVY),((315,161),(354,161),NAVY),((480,161),(519,161),NAVY)]:
            arrow(d,p1,p2,c,s)
        for pts,c in [([(252,202),(252,240),(360,240),(360,259)],TEAL), ([(417,202),(417,240),(360,240)],GOLD), ([(587,202),(587,240),(435,240),(435,259)],TEAL)]:
            path_arrow(d,pts,c,s)

    save_png("ch3_program_configuration_flow", (700, 370), draw_fn)


if __name__ == "__main__":
    data_model()
    governance_state()
    module_flow()
    print("Generated Chapter III diagrams in", BASE)
