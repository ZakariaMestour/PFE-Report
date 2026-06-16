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
LINE = "#D4D0C8"
CREAM = "#F7F4EF"
WARM = "#F0EDE8"
DARK = "#1A1A1A"


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
F_SMALL = font(10)


def defs():
    return f"""
  <defs>
    <marker id="arrow_navy" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{NAVY}"/></marker>
    <marker id="arrow_gray" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{GRAY}"/></marker>
    <marker id="arrow_teal" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{TEAL}"/></marker>
    <marker id="arrow_gold" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{GOLD}"/></marker>
    <marker id="arrow_green" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{GREEN}"/></marker>
    <marker id="arrow_red" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{RED}"/></marker>
  </defs>"""


def save_svg(name, viewbox, body):
    (BASE / f"{name}.svg").write_text(
        f'<svg viewBox="{viewbox}" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto;">\n{defs()}\n{body}\n</svg>\n',
        encoding="utf-8",
    )


def sp(point, scale):
    return int(round(point[0] * scale)), int(round(point[1] * scale))


def svg_text(x, y, text, size=7.5, color=GRAY, weight="400", anchor="start"):
    return (
        f'  <text x="{x}" y="{y}" text-anchor="{anchor}" '
        f'font-family="JetBrains Mono, monospace" font-size="{size}" '
        f'fill="{color}" font-weight="{weight}">{text}</text>'
    )


def svg_box(x, y, w, h, title, lines, header=NAVY2, stroke=NAVY):
    cx = x + w / 2
    out = [
        f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{CREAM}" stroke="{stroke}" stroke-width="1.4"/>',
        f'  <rect x="{x}" y="{y}" width="{w}" height="22" rx="2" fill="{header}"/>',
        f'  <text x="{cx}" y="{y + 15}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8" fill="white" font-weight="600">{title}</text>',
    ]
    ty = y + 37
    for text, color, weight in lines:
        out.append(svg_text(x + 7, ty, text, 6.8, color, weight))
        ty += 12
    return "\n".join(out)


def draw_box(d, box, title, lines, scale, header=NAVY2, stroke=NAVY):
    x, y, w, h = box
    d.rounded_rectangle(
        (*sp((x, y), scale), *sp((x + w, y + h), scale)),
        radius=2 * scale,
        fill=CREAM,
        outline=stroke,
        width=max(1, int(1.4 * scale)),
    )
    d.rounded_rectangle(
        (*sp((x, y), scale), *sp((x + w, y + 22), scale)),
        radius=2 * scale,
        fill=header,
        outline=header,
    )
    tb = d.textbbox((0, 0), title, font=F_HEAD)
    d.text((int((x + w / 2) * scale - (tb[2] - tb[0]) / 2), int((y + 4) * scale)), title, fill="white", font=F_HEAD)
    ty = int((y + 31) * scale)
    for text, color, weight in lines:
        d.text((int((x + 7) * scale), ty), text, fill=color, font=F_HEAD if weight == "600" else F_BODY)
        ty += int(12 * scale)


def arrow(d, p1, p2, color, scale, dashed=False):
    x1, y1 = sp(p1, scale)
    x2, y2 = sp(p2, scale)
    if dashed:
        draw_dashed_line(d, (x1, y1), (x2, y2), color, max(1, int(1.2 * scale)))
    else:
        d.line((x1, y1, x2, y2), fill=color, width=max(1, int(1.4 * scale)))
    dx, dy = x2 - x1, y2 - y1
    if abs(dx) >= abs(dy):
        sign = 1 if dx >= 0 else -1
        pts = [(x2, y2), (x2 - sign * int(7 * scale), y2 - int(4 * scale)), (x2 - sign * int(7 * scale), y2 + int(4 * scale))]
    else:
        sign = 1 if dy >= 0 else -1
        pts = [(x2, y2), (x2 - int(4 * scale), y2 - sign * int(7 * scale)), (x2 + int(4 * scale), y2 - sign * int(7 * scale))]
    d.polygon(pts, fill=color)


def draw_dashed_line(d, start, end, color, width):
    x1, y1 = start
    x2, y2 = end
    length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    if length == 0:
        return
    dash, gap = 10, 6
    ux, uy = (x2 - x1) / length, (y2 - y1) / length
    dist = 0
    while dist < length:
        seg_end = min(dist + dash, length)
        d.line((x1 + ux * dist, y1 + uy * dist, x1 + ux * seg_end, y1 + uy * seg_end), fill=color, width=width)
        dist += dash + gap


def path_arrow(d, points, color, scale):
    scaled = [sp(point, scale) for point in points]
    d.line(scaled, fill=color, width=max(1, int(1.4 * scale)))
    arrow(d, points[-2], points[-1], color, scale)


def save_png(name, size, draw_fn):
    scale = 2
    img = Image.new("RGB", (size[0] * scale, size[1] * scale), "white")
    draw_fn(ImageDraw.Draw(img), scale)
    img.save(BASE / f"{name}.png")


def value_chain_map():
    body = f"""
  <text x="25" y="28" font-family="JetBrains Mono, monospace" font-size="14" fill="{NAVY}" font-weight="700">Disbursement Module in the SCF Value Chain</text>
{svg_box(35, 92, 125, 82, "PROGRAM", [("anchor + CP", GRAY, "400"), ("limits/rules", TEAL, "600")], header=NAVY2, stroke=NAVY)}
{svg_box(35, 218, 125, 82, "INVOICES", [("validated rows", GRAY, "400"), ("eligible amount", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(235, 62, 130, 82, "FEE_CATALOGUE", [("rates + flats", GRAY, "400"), ("charge basis", GOLD, "600")], header=GOLD, stroke=GOLD)}
{svg_box(235, 248, 130, 82, "PRODUCT", [("SCF family", GRAY, "400"), ("instrument", TEAL, "600")], header=NAVY2, stroke=NAVY)}
{svg_box(435, 155, 145, 95, "DISBURSEMENT", [("select finance", GRAY, "400"), ("calculate terms", TEAL, "600"), ("prepare request", GOLD, "600")], header=TEAL, stroke=TEAL)}
{svg_box(640, 60, 125, 82, "ACCOUNTING", [("debit/credit", GRAY, "400"), ("read-only lines", TEAL, "600")], header=NAVY2, stroke=NAVY)}
{svg_box(640, 180, 125, 82, "REPAYMENT", [("schedule", GRAY, "400"), ("due dates", GREEN, "600")], header=GREEN, stroke=GREEN)}
{svg_box(640, 300, 125, 82, "APPROVAL", [("maker/checker", GRAY, "400"), ("DRAFT -> PENDING", GOLD, "600")], header=GOLD, stroke=GOLD)}
  <line x1="160" y1="133" x2="434" y2="178" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <line x1="160" y1="259" x2="434" y2="203" stroke="{TEAL}" stroke-width="1.4" marker-end="url(#arrow_teal)"/>
  <line x1="365" y1="103" x2="434" y2="180" stroke="{GOLD}" stroke-width="1.4" marker-end="url(#arrow_gold)"/>
  <line x1="365" y1="289" x2="434" y2="225" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <line x1="580" y1="178" x2="639" y2="101" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <line x1="580" y1="203" x2="639" y2="221" stroke="{GREEN}" stroke-width="1.4" marker-end="url(#arrow_green)"/>
  <line x1="580" y1="225" x2="639" y2="341" stroke="{GOLD}" stroke-width="1.4" marker-end="url(#arrow_gold)"/>
"""
    save_svg("ch5_value_chain_map", "0 0 800 420", body)

    def draw_fn(d, s):
        d.text(sp((25, 13), s), "Disbursement Module in the SCF Value Chain", font=F_TITLE, fill=NAVY)
        boxes = [
            ((35, 92, 125, 82), "PROGRAM", [("anchor + CP", GRAY, "400"), ("limits/rules", TEAL, "600")], NAVY2, NAVY),
            ((35, 218, 125, 82), "INVOICES", [("validated rows", GRAY, "400"), ("eligible amount", TEAL, "600")], TEAL, TEAL),
            ((235, 62, 130, 82), "FEE_CATALOGUE", [("rates + flats", GRAY, "400"), ("charge basis", GOLD, "600")], GOLD, GOLD),
            ((235, 248, 130, 82), "PRODUCT", [("SCF family", GRAY, "400"), ("instrument", TEAL, "600")], NAVY2, NAVY),
            ((435, 155, 145, 95), "DISBURSEMENT", [("select finance", GRAY, "400"), ("calculate terms", TEAL, "600"), ("prepare request", GOLD, "600")], TEAL, TEAL),
            ((640, 60, 125, 82), "ACCOUNTING", [("debit/credit", GRAY, "400"), ("read-only lines", TEAL, "600")], NAVY2, NAVY),
            ((640, 180, 125, 82), "REPAYMENT", [("schedule", GRAY, "400"), ("due dates", GREEN, "600")], GREEN, GREEN),
            ((640, 300, 125, 82), "APPROVAL", [("maker/checker", GRAY, "400"), ("DRAFT -> PENDING", GOLD, "600")], GOLD, GOLD),
        ]
        for box, title, lines, header, stroke in boxes:
            draw_box(d, box, title, lines, s, header, stroke)
        for p1, p2, color in [
            ((160, 133), (434, 178), NAVY),
            ((160, 259), (434, 203), TEAL),
            ((365, 103), (434, 180), GOLD),
            ((365, 289), (434, 225), NAVY),
            ((580, 178), (639, 101), NAVY),
            ((580, 203), (639, 221), GREEN),
            ((580, 225), (639, 341), GOLD),
        ]:
            arrow(d, p1, p2, color, s)

    save_png("ch5_value_chain_map", (800, 420), draw_fn)


def activity_uml():
    body = f"""
  <text x="25" y="28" font-family="JetBrains Mono, monospace" font-size="14" fill="{NAVY}" font-weight="700">UML Activity Diagram - Disbursement Request</text>
  <circle cx="385" cy="55" r="8" fill="{NAVY}"/>
  <rect x="295" y="83" width="180" height="34" rx="17" fill="{CREAM}" stroke="{TEAL}" stroke-width="1.4"/>
  <text x="385" y="104" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8" fill="{TEAL}" font-weight="600">Select program and product</text>
  <rect x="295" y="145" width="180" height="34" rx="17" fill="{CREAM}" stroke="{TEAL}" stroke-width="1.4"/>
  <text x="385" y="166" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8" fill="{TEAL}" font-weight="600">Load eligible invoices</text>
  <rect x="295" y="207" width="180" height="34" rx="17" fill="{CREAM}" stroke="{TEAL}" stroke-width="1.4"/>
  <text x="385" y="228" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8" fill="{TEAL}" font-weight="600">Enter finance terms</text>
  <polygon points="385,270 455,305 385,340 315,305" fill="{WARM}" stroke="{GOLD}" stroke-width="1.4"/>
  <text x="385" y="302" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="7.5" fill="{NAVY}" font-weight="600">Valid</text>
  <text x="385" y="314" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="7.5" fill="{NAVY}" font-weight="600">request?</text>
  <rect x="520" y="288" width="165" height="34" rx="17" fill="{CREAM}" stroke="{RED}" stroke-width="1.4"/>
  <text x="602.5" y="309" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8" fill="{RED}" font-weight="600">Show validation errors</text>
  <rect x="295" y="368" width="180" height="34" rx="17" fill="{CREAM}" stroke="{NAVY}" stroke-width="1.4"/>
  <text x="385" y="389" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8" fill="{NAVY}" font-weight="600">Generate accounting entries</text>
  <rect x="295" y="430" width="180" height="34" rx="17" fill="{CREAM}" stroke="{GREEN}" stroke-width="1.4"/>
  <text x="385" y="451" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8" fill="{GREEN}" font-weight="600">Build repayment schedule</text>
  <rect x="295" y="492" width="180" height="34" rx="17" fill="{CREAM}" stroke="{GOLD}" stroke-width="1.4"/>
  <text x="385" y="513" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8" fill="{GOLD}" font-weight="600">Submit for approval</text>
  <circle cx="385" cy="562" r="9" fill="white" stroke="{NAVY}" stroke-width="1.8"/>
  <circle cx="385" cy="562" r="5" fill="{NAVY}"/>
  <line x1="385" y1="63" x2="385" y2="82" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <line x1="385" y1="117" x2="385" y2="144" stroke="{TEAL}" stroke-width="1.4" marker-end="url(#arrow_teal)"/>
  <line x1="385" y1="179" x2="385" y2="206" stroke="{TEAL}" stroke-width="1.4" marker-end="url(#arrow_teal)"/>
  <line x1="385" y1="241" x2="385" y2="269" stroke="{TEAL}" stroke-width="1.4" marker-end="url(#arrow_teal)"/>
  <line x1="455" y1="305" x2="519" y2="305" stroke="{RED}" stroke-width="1.4" marker-end="url(#arrow_red)"/>
  <text x="487" y="300" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="7" fill="{RED}">[no]</text>
  <path d="M 602,288 L 602,252 L 480,252 L 480,224 L 476,224" fill="none" stroke="{RED}" stroke-width="1.2" stroke-dasharray="5 3" marker-end="url(#arrow_red)"/>
  <line x1="385" y1="340" x2="385" y2="367" stroke="{GREEN}" stroke-width="1.4" marker-end="url(#arrow_green)"/>
  <text x="406" y="356" font-family="JetBrains Mono, monospace" font-size="7" fill="{GREEN}">[yes]</text>
  <line x1="385" y1="402" x2="385" y2="429" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <line x1="385" y1="464" x2="385" y2="491" stroke="{GREEN}" stroke-width="1.4" marker-end="url(#arrow_green)"/>
  <line x1="385" y1="526" x2="385" y2="552" stroke="{GOLD}" stroke-width="1.4" marker-end="url(#arrow_gold)"/>
"""
    save_svg("ch5_disbursement_activity_uml", "0 0 760 590", body)

    def draw_pill(d, box, text, outline, scale):
        x, y, w, h = box
        d.rounded_rectangle((*sp((x, y), scale), *sp((x + w, y + h), scale)), radius=int(h / 2 * scale), fill=CREAM, outline=outline, width=max(1, int(1.4 * scale)))
        tb = d.textbbox((0, 0), text, font=F_HEAD)
        d.text((int((x + w / 2) * scale - (tb[2] - tb[0]) / 2), int((y + 9) * scale)), text, fill=outline, font=F_HEAD)

    def draw_fn(d, s):
        d.text(sp((25, 13), s), "UML Activity Diagram - Disbursement Request", font=F_TITLE, fill=NAVY)
        d.ellipse((*sp((377, 47), s), *sp((393, 63), s)), fill=NAVY)
        for box, text, color in [
            ((295, 83, 180, 34), "Select program and product", TEAL),
            ((295, 145, 180, 34), "Load eligible invoices", TEAL),
            ((295, 207, 180, 34), "Enter finance terms", TEAL),
            ((520, 288, 165, 34), "Show validation errors", RED),
            ((295, 368, 180, 34), "Generate accounting entries", NAVY),
            ((295, 430, 180, 34), "Build repayment schedule", GREEN),
            ((295, 492, 180, 34), "Submit for approval", GOLD),
        ]:
            draw_pill(d, box, text, color, s)
        d.polygon([sp((385, 270), s), sp((455, 305), s), sp((385, 340), s), sp((315, 305), s)], fill=WARM, outline=GOLD)
        d.text(sp((357, 291), s), "Valid", fill=NAVY, font=F_HEAD)
        d.text(sp((347, 304), s), "request?", fill=NAVY, font=F_HEAD)
        d.ellipse((*sp((376, 553), s), *sp((394, 571), s)), fill="white", outline=NAVY, width=max(1, int(1.8 * s)))
        d.ellipse((*sp((380, 557), s), *sp((390, 567), s)), fill=NAVY)
        for p1, p2, color in [
            ((385, 63), (385, 82), NAVY),
            ((385, 117), (385, 144), TEAL),
            ((385, 179), (385, 206), TEAL),
            ((385, 241), (385, 269), TEAL),
            ((455, 305), (519, 305), RED),
            ((385, 340), (385, 367), GREEN),
            ((385, 402), (385, 429), NAVY),
            ((385, 464), (385, 491), GREEN),
            ((385, 526), (385, 552), GOLD),
        ]:
            arrow(d, p1, p2, color, s)
        path_arrow(d, [(602, 288), (602, 252), (480, 252), (480, 224), (476, 224)], RED, s)
        d.text(sp((480, 286), s), "[no]", fill=RED, font=F_SMALL)
        d.text(sp((406, 344), s), "[yes]", fill=GREEN, font=F_SMALL)

    save_png("ch5_disbursement_activity_uml", (760, 590), draw_fn)


def sequence_uml():
    xs = [45, 175, 305, 435, 565, 695]
    names = ["BankOfficer", "DisbModal", "FinanceSvc", "Gateway", "SCFService", "Database"]
    body = f"""
  <text x="25" y="28" font-family="JetBrains Mono, monospace" font-size="14" fill="{NAVY}" font-weight="700">UML Sequence Diagram - Target Disbursement Submission</text>
"""
    for x, name in zip(xs, names):
        body += f'  <rect x="{x - 42}" y="48" width="84" height="20" rx="2" fill="{WARM}" stroke="{NAVY}" stroke-width="1"/>\n'
        body += f'  <text x="{x}" y="62" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="7" fill="{NAVY}" font-weight="600">{name}</text>\n'
        body += f'  <line x1="{x}" y1="68" x2="{x}" y2="505" stroke="{LINE}" stroke-width="0.8" stroke-dasharray="4 3"/>\n'
    for x, y, h in [(175, 90, 390), (305, 117, 360), (435, 142, 335), (565, 167, 285), (695, 192, 230)]:
        body += f'  <rect x="{x - 3}" y="{y}" width="6" height="{h}" fill="{CREAM}" stroke="{GRAY}" stroke-width="0.8"/>\n'
    messages = [
        (45, 175, 93, "open wizard", TEAL, False),
        (175, 305, 118, "load eligible invoices", TEAL, False),
        (305, 435, 143, "GET /finance context", NAVY, False),
        (435, 565, 168, "route /scf", NAVY, False),
        (565, 695, 193, "read program + invoices", NAVY, False),
        (695, 565, 218, "eligibility data", GOLD, True),
        (565, 435, 243, "context response", GOLD, True),
        (435, 305, 268, "typed response", GOLD, True),
        (305, 175, 293, "invoice list", GOLD, True),
        (175, 305, 323, "createDisbursement()", TEAL, False),
        (305, 435, 348, "POST /finance/disbursements", NAVY, False),
        (435, 565, 373, "submit request", NAVY, False),
        (565, 695, 398, "persist draft", NAVY, False),
        (695, 565, 423, "draft id", GOLD, True),
        (565, 435, 448, "201 DRAFT", GOLD, True),
        (435, 305, 473, "created response", GOLD, True),
        (305, 175, 498, "display success", GOLD, True),
    ]
    for x1, x2, y, label, color, dashed in messages:
        dash = ' stroke-dasharray="4 3"' if dashed else ""
        marker = "arrow_gold" if dashed else ("arrow_teal" if color == TEAL else "arrow_navy")
        body += f'  <line x1="{x1}" y1="{y}" x2="{x2 - 1 if x2 > x1 else x2 + 1}" y2="{y}" stroke="{color}" stroke-width="1.2"{dash} marker-end="url(#{marker})"/>\n'
        body += f'  <text x="{(x1 + x2) / 2}" y="{y - 5}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="6.3" fill="{color}">{label}</text>\n'
    body += f"""
  <rect x="252" y="362" width="106" height="20" rx="2" fill="{CREAM}" stroke="{TEAL}" stroke-width="1"/>
  <text x="305" y="376" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="6.5" fill="{TEAL}" font-weight="600">typed payload</text>
"""
    save_svg("ch5_disbursement_sequence_uml", "0 0 740 535", body)

    def draw_fn(d, s):
        d.text(sp((25, 13), s), "UML Sequence Diagram - Target Disbursement Submission", font=F_TITLE, fill=NAVY)
        for x, name in zip(xs, names):
            d.rounded_rectangle((*sp((x - 42, 48), s), *sp((x + 42, 68), s)), radius=2 * s, fill=WARM, outline=NAVY, width=max(1, s))
            tb = d.textbbox((0, 0), name, font=F_SMALL)
            d.text((int(x * s - (tb[2] - tb[0]) / 2), int(53 * s)), name, fill=NAVY, font=F_SMALL)
            draw_dashed_line(d, sp((x, 68), s), sp((x, 505), s), LINE, max(1, int(0.8 * s)))
        for x, y, h in [(175, 90, 390), (305, 117, 360), (435, 142, 335), (565, 167, 285), (695, 192, 230)]:
            d.rectangle((*sp((x - 3, y), s), *sp((x + 3, y + h), s)), fill=CREAM, outline=GRAY, width=max(1, int(0.8 * s)))
        for x1, x2, y, label, color, dashed in messages:
            arrow(d, (x1, y), (x2 - 1 if x2 > x1 else x2 + 1, y), color, s, dashed)
            tb = d.textbbox((0, 0), label, font=F_SMALL)
            d.text((int(((x1 + x2) / 2) * s - (tb[2] - tb[0]) / 2), int((y - 15) * s)), label, fill=color, font=F_SMALL)
        d.rounded_rectangle((*sp((252, 362), s), *sp((358, 382), s)), radius=2 * s, fill=CREAM, outline=TEAL, width=max(1, s))
        tb = d.textbbox((0, 0), "typed payload", font=F_SMALL)
        d.text((int(305 * s - (tb[2] - tb[0]) / 2), int(367 * s)), "typed payload", fill=TEAL, font=F_SMALL)

    save_png("ch5_disbursement_sequence_uml", (740, 535), draw_fn)


def integration_roadmap():
    body = f"""
  <text x="25" y="28" font-family="JetBrains Mono, monospace" font-size="14" fill="{NAVY}" font-weight="700">Disbursement Module Integration Roadmap</text>
{svg_box(35, 135, 130, 88, "REFINEMENT", [("PO sessions", GRAY, "400"), ("business rules", TEAL, "600"), ("diagram review", GOLD, "600")], header=TEAL, stroke=TEAL)}
{svg_box(215, 135, 130, 88, "ISOLATED_DESIGN", [("target module", GRAY, "400"), ("flow + model", TEAL, "600"), ("no native merge yet", GOLD, "600")], header=GOLD, stroke=GOLD)}
{svg_box(395, 135, 130, 88, "PROTOTYPE", [("wizard panes", GRAY, "400"), ("typed service", TEAL, "600"), ("screenshots later", GOLD, "600")], header=TEAL, stroke=TEAL)}
{svg_box(575, 135, 130, 88, "NATIVE_INJECTION", [("future sprint", GRAY, "400"), ("backend contract", TEAL, "600"), ("approval lifecycle", GREEN, "600")], header=GREEN, stroke=GREEN)}
  <line x1="165" y1="179" x2="214" y2="179" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <line x1="345" y1="179" x2="394" y2="179" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <line x1="525" y1="179" x2="574" y2="179" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <rect x="215" y="260" width="310" height="52" rx="2" fill="{WARM}" stroke="{GOLD}" stroke-width="1"/>
  <text x="370" y="278" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8" fill="{GOLD}" font-weight="600">current report boundary</text>
  <text x="230" y="296" font-family="JetBrains Mono, monospace" font-size="7.2" fill="{NAVY}">The chapter documents design, intended contracts, and visible UI flow.</text>
"""
    save_svg("ch5_integration_roadmap", "0 0 740 345", body)

    def draw_fn(d, s):
        d.text(sp((25, 13), s), "Disbursement Module Integration Roadmap", font=F_TITLE, fill=NAVY)
        boxes = [
            ((35, 135, 130, 88), "REFINEMENT", [("PO sessions", GRAY, "400"), ("business rules", TEAL, "600"), ("diagram review", GOLD, "600")], TEAL, TEAL),
            ((215, 135, 130, 88), "ISOLATED_DESIGN", [("target module", GRAY, "400"), ("flow + model", TEAL, "600"), ("no native merge yet", GOLD, "600")], GOLD, GOLD),
            ((395, 135, 130, 88), "PROTOTYPE", [("wizard panes", GRAY, "400"), ("typed service", TEAL, "600"), ("screenshots later", GOLD, "600")], TEAL, TEAL),
            ((575, 135, 130, 88), "NATIVE_INJECTION", [("future sprint", GRAY, "400"), ("backend contract", TEAL, "600"), ("approval lifecycle", GREEN, "600")], GREEN, GREEN),
        ]
        for box, title, lines, header, stroke in boxes:
            draw_box(d, box, title, lines, s, header, stroke)
        for p1, p2 in [((165, 179), (214, 179)), ((345, 179), (394, 179)), ((525, 179), (574, 179))]:
            arrow(d, p1, p2, NAVY, s)
        d.rounded_rectangle((*sp((215, 260), s), *sp((525, 312), s)), radius=2 * s, fill=WARM, outline=GOLD, width=max(1, s))
        d.text(sp((282, 266), s), "current report boundary", fill=GOLD, font=F_HEAD)
        d.text(sp((230, 288), s), "The chapter documents design, intended contracts, and visible UI flow.", fill=NAVY, font=F_SMALL)

    save_png("ch5_integration_roadmap", (740, 345), draw_fn)


if __name__ == "__main__":
    value_chain_map()
    activity_uml()
    sequence_uml()
    integration_roadmap()
    print("Generated Chapter V diagrams in", BASE)
