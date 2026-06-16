from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent

NAVY = "#0B1D3A"
NAVY2 = "#162B52"
TEAL = "#0B7285"
TEAL2 = "#0E9CB5"
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
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


F_TITLE = font(28, True)
F_HEAD = font(16, True)
F_BODY = font(13)
F_SMALL = font(11)


def svg_defs():
    return f"""
  <defs>
    <marker id="arrow_navy" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
      <path d="M0,0 L7,3.5 L0,7 Z" fill="{NAVY}"/>
    </marker>
    <marker id="arrow_gray" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
      <path d="M0,0 L7,3.5 L0,7 Z" fill="{GRAY}"/>
    </marker>
    <marker id="arrow_green" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
      <path d="M0,0 L7,3.5 L0,7 Z" fill="{GREEN}"/>
    </marker>
    <marker id="arrow_gold" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
      <path d="M0,0 L7,3.5 L0,7 Z" fill="{GOLD}"/>
    </marker>
  </defs>"""


def svg_box(x, y, w, h, title, lines, header=NAVY2, stroke=NAVY, fill=CREAM):
    cx = x + w / 2
    out = [
        f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>',
        f'  <rect x="{x}" y="{y}" width="{w}" height="22" rx="2" fill="{header}"/>',
        f'  <text x="{cx}" y="{y + 15}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9" fill="white" font-weight="600">{title}</text>',
    ]
    ty = y + 38
    for text, color, weight in lines:
        out.append(f'  <text x="{x + 8}" y="{ty}" font-family="JetBrains Mono, monospace" font-size="7.5" fill="{color}" font-weight="{weight}">{text}</text>')
        ty += 13
    return "\n".join(out)


def svg_label(x, y, text, color=NAVY, size=7):
    return f'  <text x="{x}" y="{y}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="{size}" fill="{color}">{text}</text>'


def save_svg(name, viewbox, body):
    svg = f'<svg viewBox="{viewbox}" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto;">\n{svg_defs()}\n{body}\n</svg>\n'
    (BASE / f"{name}.svg").write_text(svg, encoding="utf-8")


def scale_point(p, s):
    return int(round(p[0] * s)), int(round(p[1] * s))


def draw_rect(draw, box, fill, outline, s, header=None, title=None, body=None):
    x, y, w, h = box
    rect = [int(x * s), int(y * s), int((x + w) * s), int((y + h) * s)]
    draw.rounded_rectangle(rect, radius=int(2 * s), fill=fill, outline=outline, width=max(1, int(1.5 * s)))
    if header:
        hbox = [int(x * s), int(y * s), int((x + w) * s), int((y + 22) * s)]
        draw.rounded_rectangle(hbox, radius=int(2 * s), fill=header, outline=header)
    if title:
        bbox = draw.textbbox((0, 0), title, font=F_HEAD)
        tx = int((x + w / 2) * s - (bbox[2] - bbox[0]) / 2)
        draw.text((tx, int((y + 5) * s)), title, fill="white", font=F_HEAD)
    if body:
        ty = int((y + 31) * s)
        for text, color, weight in body:
            draw.text((int((x + 8) * s), ty), text, fill=color, font=F_BODY if weight == "400" else F_HEAD)
            ty += int(14 * s)


def draw_arrow(draw, p1, p2, color, s, width=1.5):
    x1, y1 = scale_point(p1, s)
    x2, y2 = scale_point(p2, s)
    draw.line((x1, y1, x2, y2), fill=color, width=max(1, int(width * s)))
    dx, dy = x2 - x1, y2 - y1
    if abs(dx) >= abs(dy):
        sign = 1 if dx >= 0 else -1
        pts = [(x2, y2), (x2 - sign * int(7 * s), y2 - int(4 * s)), (x2 - sign * int(7 * s), y2 + int(4 * s))]
    else:
        sign = 1 if dy >= 0 else -1
        pts = [(x2, y2), (x2 - int(4 * s), y2 - sign * int(7 * s)), (x2 + int(4 * s), y2 - sign * int(7 * s))]
    draw.polygon(pts, fill=color)


def draw_path(draw, pts, color, s):
    scaled = [scale_point(p, s) for p in pts]
    draw.line(scaled, fill=color, width=max(1, int(1.5 * s)))
    draw_arrow(draw, pts[-2], pts[-1], color, s)


def save_png(name, size, draw_fn):
    s = 2
    img = Image.new("RGB", (size[0] * s, size[1] * s), "white")
    draw = ImageDraw.Draw(img)
    draw_fn(draw, s)
    img.save(BASE / f"{name}.png")


def ecosystem():
    # Coordinate table:
    # NAME           x    y    w    h    cx   cy   right  bottom
    # Anchor         45   175  150  78   120  214  195    253
    # Program        275  165  160  98   355  214  435    263
    # Counterparty   555  175  150  78   630  214  705    253
    # Bank           275  45   160  78   355  84   435    123
    # Instrument     275  330  160  78   355  369  435    408
    body = f"""
  <!-- Coordinate table embedded in generator source. Last body text y values stay within each box. -->
  <text x="30" y="28" font-family="JetBrains Mono, monospace" font-size="14" fill="{NAVY}" font-weight="700">Supply Chain Finance Ecosystem</text>
{svg_box(45, 175, 150, 78, "ANCHOR", [("large buyer/seller", GRAY, "400"), ("commercial reference", GRAY, "400")], header=NAVY2, stroke=NAVY)}
{svg_box(275, 165, 160, 98, "SCF_PROGRAM", [("product + limits", GRAY, "400"), ("fees + eligibility", GRAY, "400"), ("disbursement rules", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(555, 175, 150, 78, "COUNTERPARTY", [("supplier / SME", GRAY, "400"), ("distributor / buyer", GRAY, "400")], header=NAVY2, stroke=NAVY)}
{svg_box(275, 45, 160, 78, "BANK", [("program governance", GRAY, "400"), ("financing control", GRAY, "400")], header=NAVY2, stroke=NAVY)}
{svg_box(275, 330, 160, 78, "INSTRUMENTS", [("invoices", GRAY, "400"), ("purchase orders", GRAY, "400"), ("trade documents", TEAL, "600")], header=GOLD, stroke=GOLD)}
  <line x1="195" y1="214" x2="274" y2="214" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
{svg_label(235, 207, "program setup", NAVY)}
  <line x1="435" y1="214" x2="554" y2="214" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
{svg_label(495, 207, "eligibility", NAVY)}
  <line x1="355" y1="123" x2="355" y2="164" stroke="{TEAL}" stroke-width="1.5" marker-end="url(#arrow_green)"/>
{svg_label(385, 146, "validation", TEAL)}
  <line x1="355" y1="330" x2="355" y2="264" stroke="{GOLD}" stroke-width="1.5" marker-end="url(#arrow_gold)"/>
{svg_label(406, 302, "cashflow input", GOLD)}
  <path d="M 555,253 L 555,292 L 195,292 L 195,254" fill="none" stroke="{GRAY}" stroke-width="1.5" marker-end="url(#arrow_gray)"/>
{svg_label(375, 286, "goods / services + invoice", GRAY)}
  <line x1="435" y1="84" x2="554" y2="175" stroke="{GREEN}" stroke-width="1.5" marker-end="url(#arrow_green)"/>
{svg_label(502, 124, "financing", GREEN)}
  <line x1="275" y1="84" x2="196" y2="175" stroke="{GREEN}" stroke-width="1.5" marker-end="url(#arrow_green)"/>
{svg_label(226, 124, "payment flow", GREEN)}
"""
    save_svg("ch1_scf_ecosystem", "0 0 750 430", body)

    def draw_fn(d, s):
        d.text(scale_point((30, 13), s), "Supply Chain Finance Ecosystem", font=F_TITLE, fill=NAVY)
        boxes = [
            ((45, 175, 150, 78), NAVY, NAVY2, "ANCHOR", [("large buyer/seller", GRAY, "400"), ("commercial reference", GRAY, "400")]),
            ((275, 165, 160, 98), TEAL, TEAL, "SCF_PROGRAM", [("product + limits", GRAY, "400"), ("fees + eligibility", GRAY, "400"), ("disbursement rules", TEAL, "600")]),
            ((555, 175, 150, 78), NAVY, NAVY2, "COUNTERPARTY", [("supplier / SME", GRAY, "400"), ("distributor / buyer", GRAY, "400")]),
            ((275, 45, 160, 78), NAVY, NAVY2, "BANK", [("program governance", GRAY, "400"), ("financing control", GRAY, "400")]),
            ((275, 330, 160, 78), GOLD, GOLD, "INSTRUMENTS", [("invoices", GRAY, "400"), ("purchase orders", GRAY, "400"), ("trade documents", TEAL, "600")]),
        ]
        for box, stroke, header, title, lines in boxes:
            draw_rect(d, box, CREAM, stroke, s, header, title, lines)
        for p1, p2, color in [((195, 214), (274, 214), NAVY), ((435, 214), (554, 214), NAVY), ((355, 123), (355, 164), TEAL), ((355, 330), (355, 264), GOLD), ((435, 84), (554, 175), GREEN), ((275, 84), (196, 175), GREEN)]:
            draw_arrow(d, p1, p2, color, s)
        draw_path(d, [(555, 253), (555, 292), (195, 292), (195, 254)], GRAY, s)

    save_png("ch1_scf_ecosystem", (750, 430), draw_fn)


def workflow():
    # Coordinate table:
    # Ticket x=25 y=120 w=120 h=74 cx=85 cy=157 right=145 bottom=194
    # Dev x=175 y=120 w=120 h=74 cx=235 cy=157 right=295 bottom=194
    # Push x=325 y=120 w=120 h=74 cx=385 cy=157 right=445 bottom=194
    # PR x=475 y=120 w=120 h=74 cx=535 cy=157 right=595 bottom=194
    # Test x=625 y=120 w=120 h=74 cx=685 cy=157 right=745 bottom=194
    body = f"""
  <text x="25" y="30" font-family="JetBrains Mono, monospace" font-size="14" fill="{NAVY}" font-weight="700">Daily Development and Validation Workflow</text>
{svg_box(25, 120, 120, 74, "JIRA", [("ticket assigned", GRAY, "400"), ("sprint scope", GRAY, "400")], header=NAVY2, stroke=NAVY)}
{svg_box(175, 120, 120, 74, "DEV", [("backend/frontend", GRAY, "400"), ("implementation", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(325, 120, 120, 74, "BITBUCKET", [("branch push", GRAY, "400"), ("PR opened", GRAY, "400")], header=TEAL, stroke=TEAL)}
{svg_box(475, 120, 120, 74, "PR_REVIEW", [("tech lead", GRAY, "400"), ("approve/request", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(625, 120, 120, 74, "TESTER", [("verification", GRAY, "400"), ("ticket closure", GREEN, "600")], header=NAVY2, stroke=NAVY)}
  <line x1="145" y1="157" x2="174" y2="157" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
  <line x1="295" y1="157" x2="324" y2="157" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
  <line x1="445" y1="157" x2="474" y2="157" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
  <line x1="595" y1="157" x2="624" y2="157" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
  <rect x="475" y="245" width="120" height="48" rx="2" fill="{WARM}" stroke="{GOLD}" stroke-width="1.5"/>
  <text x="535" y="265" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8" fill="{GOLD}" font-weight="600">MODIFICATION</text>
  <text x="483" y="281" font-family="JetBrains Mono, monospace" font-size="7.5" fill="{GRAY}">comments returned</text>
  <path d="M 535,245 L 535,195" fill="none" stroke="{GOLD}" stroke-width="1.5" marker-end="url(#arrow_gold)"/>
  <path d="M 475,269 L 235,269 L 235,195" fill="none" stroke="{GOLD}" stroke-width="1.5" marker-end="url(#arrow_gold)"/>
{svg_label(355, 263, "review loop", GOLD)}
"""
    save_svg("ch1_internship_workflow", "0 0 770 325", body)

    def draw_fn(d, s):
        d.text(scale_point((25, 15), s), "Daily Development and Validation Workflow", font=F_TITLE, fill=NAVY)
        for box, stroke, header, title, lines in [
            ((25, 120, 120, 74), NAVY, NAVY2, "JIRA", [("ticket assigned", GRAY, "400"), ("sprint scope", GRAY, "400")]),
            ((175, 120, 120, 74), TEAL, TEAL, "DEV", [("backend/frontend", GRAY, "400"), ("implementation", TEAL, "600")]),
            ((325, 120, 120, 74), TEAL, TEAL, "BITBUCKET", [("branch push", GRAY, "400"), ("PR opened", GRAY, "400")]),
            ((475, 120, 120, 74), TEAL, TEAL, "PR_REVIEW", [("tech lead", GRAY, "400"), ("approve/request", TEAL, "600")]),
            ((625, 120, 120, 74), NAVY, NAVY2, "TESTER", [("verification", GRAY, "400"), ("ticket closure", GREEN, "600")]),
        ]:
            draw_rect(d, box, CREAM, stroke, s, header, title, lines)
        for p1, p2 in [((145, 157), (174, 157)), ((295, 157), (324, 157)), ((445, 157), (474, 157)), ((595, 157), (624, 157))]:
            draw_arrow(d, p1, p2, NAVY, s)
        draw_rect(d, (475, 245, 120, 48), WARM, GOLD, s)
        d.text(scale_point((490, 257), s), "MODIFICATION", font=F_SMALL, fill=GOLD)
        d.text(scale_point((483, 272), s), "comments returned", font=F_SMALL, fill=GRAY)
        draw_path(d, [(535, 245), (535, 195)], GOLD, s)
        draw_path(d, [(475, 269), (235, 269), (235, 195)], GOLD, s)

    save_png("ch1_internship_workflow", (770, 325), draw_fn)


def timeline():
    body = f"""
  <text x="25" y="30" font-family="JetBrains Mono, monospace" font-size="14" fill="{NAVY}" font-weight="700">Internship Timeline</text>
  <line x1="50" y1="165" x2="720" y2="165" stroke="{NAVY}" stroke-width="2"/>
  <circle cx="90" cy="165" r="7" fill="{TEAL}" stroke="{NAVY}" stroke-width="1"/>
  <circle cx="235" cy="165" r="7" fill="{TEAL}" stroke="{NAVY}" stroke-width="1"/>
  <circle cx="385" cy="165" r="7" fill="{TEAL}" stroke="{NAVY}" stroke-width="1"/>
  <circle cx="535" cy="165" r="7" fill="{TEAL}" stroke="{NAVY}" stroke-width="1"/>
  <circle cx="685" cy="165" r="7" fill="{GREEN}" stroke="{NAVY}" stroke-width="1"/>
{svg_box(30, 218, 120, 82, "FEB_2026", [("remote training", DARK, "400"), ("business layer", GRAY, "400"), ("Java/Spring Boot", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(175, 55, 120, 82, "WEEK_3", [("on-site work", GRAY, "400"), ("team integration", GRAY, "400"), ("delivery rhythm", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(325, 218, 120, 82, "SPRINTS", [("Sprint 2 to 8", GRAY, "400"), ("Jira + PRs", GRAY, "400"), ("tester loop", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(475, 55, 120, 82, "MONDAYS", [("PO refinement", GRAY, "400"), ("functional", GRAY, "400"), ("diagrams", TEAL, "600")], header=GOLD, stroke=GOLD)}
{svg_box(625, 218, 120, 82, "JUL_01", [("internship end", GRAY, "400"), ("report synthesis", GREEN, "600")], header=GREEN, stroke=GREEN)}
  <line x1="90" y1="172" x2="90" y2="217" stroke="{GRAY}" stroke-width="1"/>
  <line x1="235" y1="164" x2="235" y2="138" stroke="{GRAY}" stroke-width="1"/>
  <line x1="385" y1="172" x2="385" y2="217" stroke="{GRAY}" stroke-width="1"/>
  <line x1="535" y1="164" x2="535" y2="138" stroke="{GRAY}" stroke-width="1"/>
  <line x1="685" y1="172" x2="685" y2="217" stroke="{GRAY}" stroke-width="1"/>
"""
    save_svg("ch1_internship_timeline", "0 0 775 325", body)

    def draw_fn(d, s):
        d.text(scale_point((25, 15), s), "Internship Timeline", font=F_TITLE, fill=NAVY)
        d.line((*scale_point((50, 165), s), *scale_point((720, 165), s)), fill=NAVY, width=max(1, int(2 * s)))
        for x, color in [(90, TEAL), (235, TEAL), (385, TEAL), (535, TEAL), (685, GREEN)]:
            cx, cy = scale_point((x, 165), s)
            d.ellipse((cx - 7 * s, cy - 7 * s, cx + 7 * s, cy + 7 * s), fill=color, outline=NAVY, width=max(1, int(s)))
        for box, stroke, header, title, lines in [
            ((30, 218, 120, 82), TEAL, TEAL, "FEB_2026", [("remote training", GRAY, "400"), ("business layer", GRAY, "400"), ("Java/Spring Boot", TEAL, "600")]),
            ((175, 55, 120, 82), TEAL, TEAL, "WEEK_3", [("on-site work", GRAY, "400"), ("team integration", GRAY, "400"), ("delivery rhythm", TEAL, "600")]),
            ((325, 218, 120, 82), TEAL, TEAL, "SPRINTS", [("Sprint 2 to 8", GRAY, "400"), ("Jira + PRs", GRAY, "400"), ("tester loop", TEAL, "600")]),
            ((475, 55, 120, 82), GOLD, GOLD, "MONDAYS", [("PO refinement", GRAY, "400"), ("functional", GRAY, "400"), ("diagrams", TEAL, "600")]),
            ((625, 218, 120, 82), GREEN, GREEN, "JUL_01", [("internship end", GRAY, "400"), ("report synthesis", GREEN, "600")]),
        ]:
            draw_rect(d, box, CREAM, stroke, s, header, title, lines)

    save_png("ch1_internship_timeline", (775, 325), draw_fn)


if __name__ == "__main__":
    ecosystem()
    workflow()
    timeline()
    print("Generated SVG-first Chapter I diagrams in", BASE)
