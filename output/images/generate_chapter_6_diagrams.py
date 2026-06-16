from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent

NAVY = "#0B1D3A"
NAVY2 = "#162B52"
TEAL = "#0B7285"
GOLD = "#C9962A"
GREEN = "#166534"
GRAY = "#6B7280"
LINE = "#D4D0C8"
CREAM = "#F7F4EF"
WARM = "#F0EDE8"


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
    <marker id="arrow_teal" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{TEAL}"/></marker>
    <marker id="arrow_gold" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{GOLD}"/></marker>
    <marker id="arrow_green" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{GREEN}"/></marker>
  </defs>"""


def save_svg(name, viewbox, body):
    (BASE / f"{name}.svg").write_text(
        f'<svg viewBox="{viewbox}" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto;">\n{defs()}\n{body}\n</svg>\n',
        encoding="utf-8",
    )


def sp(point, scale):
    return int(round(point[0] * scale)), int(round(point[1] * scale))


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


def draw_box(d, box, title, lines, scale, header=NAVY2, stroke=NAVY):
    x, y, w, h = box
    d.rounded_rectangle((*sp((x, y), scale), *sp((x + w, y + h), scale)), radius=2 * scale, fill=CREAM, outline=stroke, width=max(1, int(1.4 * scale)))
    d.rounded_rectangle((*sp((x, y), scale), *sp((x + w, y + 22), scale)), radius=2 * scale, fill=header, outline=header)
    tb = d.textbbox((0, 0), title, font=F_HEAD)
    d.text((int((x + w / 2) * scale - (tb[2] - tb[0]) / 2), int((y + 4) * scale)), title, fill="white", font=F_HEAD)
    ty = int((y + 31) * scale)
    for text, color, weight in lines:
        d.text((int((x + 7) * scale), ty), text, fill=color, font=F_HEAD if weight == "600" else F_BODY)
        ty += int(12 * scale)


def arrow(d, p1, p2, color, scale):
    x1, y1 = sp(p1, scale)
    x2, y2 = sp(p2, scale)
    d.line((x1, y1, x2, y2), fill=color, width=max(1, int(1.4 * scale)))
    dx, dy = x2 - x1, y2 - y1
    if abs(dx) >= abs(dy):
        sign = 1 if dx >= 0 else -1
        pts = [(x2, y2), (x2 - sign * int(7 * scale), y2 - int(4 * scale)), (x2 - sign * int(7 * scale), y2 + int(4 * scale))]
    else:
        sign = 1 if dy >= 0 else -1
        pts = [(x2, y2), (x2 - int(4 * scale), y2 - sign * int(7 * scale)), (x2 + int(4 * scale), y2 - sign * int(7 * scale))]
    d.polygon(pts, fill=color)


def path_arrow(d, points, color, scale):
    d.line([sp(point, scale) for point in points], fill=color, width=max(1, int(1.4 * scale)))
    arrow(d, points[-2], points[-1], color, scale)


def save_png(name, size, draw_fn):
    scale = 2
    img = Image.new("RGB", (size[0] * scale, size[1] * scale), "white")
    draw_fn(ImageDraw.Draw(img), scale)
    img.save(BASE / f"{name}.png")


def contribution_streams():
    body = f"""
  <text x="25" y="28" font-family="JetBrains Mono, monospace" font-size="14" fill="{NAVY}" font-weight="700">Internship Contribution Streams</text>
  <rect x="30" y="62" width="700" height="118" rx="2" fill="{WARM}" stroke="{LINE}" stroke-width="1"/>
  <rect x="30" y="218" width="700" height="118" rx="2" fill="{CREAM}" stroke="{LINE}" stroke-width="1"/>
  <text x="48" y="88" font-family="JetBrains Mono, monospace" font-size="9" fill="{NAVY}" font-weight="700">PLATFORM DELIVERY</text>
  <text x="48" y="244" font-family="JetBrains Mono, monospace" font-size="9" fill="{TEAL}" font-weight="700">PFE MODULE PREPARATION</text>
{svg_box(190, 88, 110, 64, "JIRA", [("ticket scope", GRAY, "400"), ("sprint work", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(345, 88, 110, 64, "BITBUCKET", [("branch + PR", GRAY, "400"), ("review", GOLD, "600")], header=GOLD, stroke=GOLD)}
{svg_box(500, 88, 110, 64, "TESTER", [("validation", GRAY, "400"), ("feedback", GREEN, "600")], header=GREEN, stroke=GREEN)}
{svg_box(190, 244, 110, 64, "REFINEMENT", [("PO concepts", GRAY, "400"), ("rules", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(345, 244, 110, 64, "DIAGRAMS", [("flows", GRAY, "400"), ("corrections", GOLD, "600")], header=GOLD, stroke=GOLD)}
{svg_box(500, 244, 110, 64, "TARGET_DESIGN", [("module shape", GRAY, "400"), ("future merge", GREEN, "600")], header=GREEN, stroke=GREEN)}
  <line x1="300" y1="120" x2="344" y2="120" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <line x1="455" y1="120" x2="499" y2="120" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <line x1="300" y1="276" x2="344" y2="276" stroke="{TEAL}" stroke-width="1.4" marker-end="url(#arrow_teal)"/>
  <line x1="455" y1="276" x2="499" y2="276" stroke="{TEAL}" stroke-width="1.4" marker-end="url(#arrow_teal)"/>
  <path d="M 555,152 L 555,196 L 245,196 L 245,243" fill="none" stroke="{GOLD}" stroke-width="1.2" stroke-dasharray="5 3" marker-end="url(#arrow_gold)"/>
  <text x="375" y="191" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="7" fill="{GOLD}">platform exposure fed the PFE analysis</text>
"""
    save_svg("ch6_contribution_streams", "0 0 760 370", body)

    def draw_fn(d, s):
        d.text(sp((25, 13), s), "Internship Contribution Streams", font=F_TITLE, fill=NAVY)
        d.rounded_rectangle((*sp((30, 62), s), *sp((730, 180), s)), radius=2 * s, fill=WARM, outline=LINE, width=max(1, s))
        d.rounded_rectangle((*sp((30, 218), s), *sp((730, 336), s)), radius=2 * s, fill=CREAM, outline=LINE, width=max(1, s))
        d.text(sp((48, 77), s), "PLATFORM DELIVERY", font=F_HEAD, fill=NAVY)
        d.text(sp((48, 233), s), "PFE MODULE PREPARATION", font=F_HEAD, fill=TEAL)
        boxes = [
            ((190, 88, 110, 64), "JIRA", [("ticket scope", GRAY, "400"), ("sprint work", TEAL, "600")], TEAL, TEAL),
            ((345, 88, 110, 64), "BITBUCKET", [("branch + PR", GRAY, "400"), ("review", GOLD, "600")], GOLD, GOLD),
            ((500, 88, 110, 64), "TESTER", [("validation", GRAY, "400"), ("feedback", GREEN, "600")], GREEN, GREEN),
            ((190, 244, 110, 64), "REFINEMENT", [("PO concepts", GRAY, "400"), ("rules", TEAL, "600")], TEAL, TEAL),
            ((345, 244, 110, 64), "DIAGRAMS", [("flows", GRAY, "400"), ("corrections", GOLD, "600")], GOLD, GOLD),
            ((500, 244, 110, 64), "TARGET_DESIGN", [("module shape", GRAY, "400"), ("future merge", GREEN, "600")], GREEN, GREEN),
        ]
        for box, title, lines, header, stroke in boxes:
            draw_box(d, box, title, lines, s, header, stroke)
        for p1, p2, color in [((300, 120), (344, 120), NAVY), ((455, 120), (499, 120), NAVY), ((300, 276), (344, 276), TEAL), ((455, 276), (499, 276), TEAL)]:
            arrow(d, p1, p2, color, s)
        path_arrow(d, [(555, 152), (555, 196), (245, 196), (245, 243)], GOLD, s)
        d.text(sp((292, 181), s), "platform exposure fed the PFE analysis", font=F_SMALL if "F_SMALL" in globals() else F_BODY, fill=GOLD)

    save_png("ch6_contribution_streams", (760, 370), draw_fn)


def skills_map():
    body = f"""
  <text x="25" y="28" font-family="JetBrains Mono, monospace" font-size="14" fill="{NAVY}" font-weight="700">Skills Acquired During the Internship</text>
{svg_box(300, 170, 150, 80, "INTERNSHIP_GROWTH", [("technical practice", GRAY, "400"), ("banking context", TEAL, "600"), ("team rhythm", GOLD, "600")], header=NAVY2, stroke=NAVY)}
{svg_box(40, 72, 130, 74, "BACKEND", [("Spring Boot", GRAY, "400"), ("JPA + OAuth2", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(300, 72, 130, 74, "FRONTEND", [("React + TS", GRAY, "400"), ("forms + services", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(580, 72, 130, 74, "DEVOPS", [("Docker stack", GRAY, "400"), ("Git + PRs", GOLD, "600")], header=GOLD, stroke=GOLD)}
{svg_box(40, 278, 130, 74, "DOMAIN", [("SCF products", GRAY, "400"), ("program logic", GREEN, "600")], header=GREEN, stroke=GREEN)}
{svg_box(300, 278, 130, 74, "COLLAB", [("Scrum", GRAY, "400"), ("PO refinement", GOLD, "600")], header=GOLD, stroke=GOLD)}
{svg_box(580, 278, 130, 74, "QUALITY", [("review comments", GRAY, "400"), ("tester feedback", GREEN, "600")], header=GREEN, stroke=GREEN)}
  <line x1="170" y1="109" x2="299" y2="194" stroke="{TEAL}" stroke-width="1.4" marker-end="url(#arrow_teal)"/>
  <line x1="365" y1="146" x2="374" y2="169" stroke="{TEAL}" stroke-width="1.4" marker-end="url(#arrow_teal)"/>
  <line x1="580" y1="109" x2="451" y2="194" stroke="{GOLD}" stroke-width="1.4" marker-end="url(#arrow_gold)"/>
  <line x1="170" y1="315" x2="299" y2="226" stroke="{GREEN}" stroke-width="1.4" marker-end="url(#arrow_green)"/>
  <line x1="365" y1="278" x2="374" y2="251" stroke="{GOLD}" stroke-width="1.4" marker-end="url(#arrow_gold)"/>
  <line x1="580" y1="315" x2="451" y2="226" stroke="{GREEN}" stroke-width="1.4" marker-end="url(#arrow_green)"/>
"""
    save_svg("ch6_skills_map", "0 0 750 390", body)

    def draw_fn(d, s):
        d.text(sp((25, 13), s), "Skills Acquired During the Internship", font=F_TITLE, fill=NAVY)
        boxes = [
            ((300, 170, 150, 80), "INTERNSHIP_GROWTH", [("technical practice", GRAY, "400"), ("banking context", TEAL, "600"), ("team rhythm", GOLD, "600")], NAVY2, NAVY),
            ((40, 72, 130, 74), "BACKEND", [("Spring Boot", GRAY, "400"), ("JPA + OAuth2", TEAL, "600")], TEAL, TEAL),
            ((300, 72, 130, 74), "FRONTEND", [("React + TS", GRAY, "400"), ("forms + services", TEAL, "600")], TEAL, TEAL),
            ((580, 72, 130, 74), "DEVOPS", [("Docker stack", GRAY, "400"), ("Git + PRs", GOLD, "600")], GOLD, GOLD),
            ((40, 278, 130, 74), "DOMAIN", [("SCF products", GRAY, "400"), ("program logic", GREEN, "600")], GREEN, GREEN),
            ((300, 278, 130, 74), "COLLAB", [("Scrum", GRAY, "400"), ("PO refinement", GOLD, "600")], GOLD, GOLD),
            ((580, 278, 130, 74), "QUALITY", [("review comments", GRAY, "400"), ("tester feedback", GREEN, "600")], GREEN, GREEN),
        ]
        for box, title, lines, header, stroke in boxes:
            draw_box(d, box, title, lines, s, header, stroke)
        for p1, p2, color in [
            ((170, 109), (299, 194), TEAL),
            ((365, 146), (374, 169), TEAL),
            ((580, 109), (451, 194), GOLD),
            ((170, 315), (299, 226), GREEN),
            ((365, 278), (374, 251), GOLD),
            ((580, 315), (451, 226), GREEN),
        ]:
            arrow(d, p1, p2, color, s)

    save_png("ch6_skills_map", (750, 390), draw_fn)


def future_roadmap():
    body = f"""
  <text x="25" y="28" font-family="JetBrains Mono, monospace" font-size="14" fill="{NAVY}" font-weight="700">Recommendations for Future Development</text>
{svg_box(40, 125, 125, 82, "DISBURSEMENT", [("native module", GRAY, "400"), ("final API", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(220, 125, 125, 82, "ASYNC_FLOWS", [("events", GRAY, "400"), ("Kafka/RabbitMQ", GOLD, "600")], header=GOLD, stroke=GOLD)}
{svg_box(400, 125, 125, 82, "MOBILE", [("CP access", GRAY, "400"), ("status tracking", GREEN, "600")], header=GREEN, stroke=GREEN)}
{svg_box(580, 125, 125, 82, "ANALYTICS", [("dashboards", GRAY, "400"), ("portfolio view", TEAL, "600")], header=NAVY2, stroke=NAVY)}
  <line x1="165" y1="166" x2="219" y2="166" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <line x1="345" y1="166" x2="399" y2="166" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <line x1="525" y1="166" x2="579" y2="166" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#arrow_navy)"/>
  <rect x="85" y="255" width="580" height="54" rx="2" fill="{WARM}" stroke="{LINE}" stroke-width="1"/>
  <text x="375" y="276" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8" fill="{NAVY}" font-weight="600">common principle</text>
  <text x="126" y="294" font-family="JetBrains Mono, monospace" font-size="7.2" fill="{GRAY}">Keep the platform configurable, governed, traceable, and useful for bank operations.</text>
"""
    save_svg("ch6_future_roadmap", "0 0 750 340", body)

    def draw_fn(d, s):
        d.text(sp((25, 13), s), "Recommendations for Future Development", font=F_TITLE, fill=NAVY)
        boxes = [
            ((40, 125, 125, 82), "DISBURSEMENT", [("native module", GRAY, "400"), ("final API", TEAL, "600")], TEAL, TEAL),
            ((220, 125, 125, 82), "ASYNC_FLOWS", [("events", GRAY, "400"), ("Kafka/RabbitMQ", GOLD, "600")], GOLD, GOLD),
            ((400, 125, 125, 82), "MOBILE", [("CP access", GRAY, "400"), ("status tracking", GREEN, "600")], GREEN, GREEN),
            ((580, 125, 125, 82), "ANALYTICS", [("dashboards", GRAY, "400"), ("portfolio view", TEAL, "600")], NAVY2, NAVY),
        ]
        for box, title, lines, header, stroke in boxes:
            draw_box(d, box, title, lines, s, header, stroke)
        for p1, p2 in [((165, 166), (219, 166)), ((345, 166), (399, 166)), ((525, 166), (579, 166))]:
            arrow(d, p1, p2, NAVY, s)
        d.rounded_rectangle((*sp((85, 255), s), *sp((665, 309), s)), radius=2 * s, fill=WARM, outline=LINE, width=max(1, s))
        d.text(sp((307, 264), s), "common principle", font=F_HEAD, fill=NAVY)
        d.text(sp((126, 287), s), "Keep the platform configurable, governed, traceable, and useful for bank operations.", font=F_BODY, fill=GRAY)

    save_png("ch6_future_roadmap", (750, 340), draw_fn)


if __name__ == "__main__":
    contribution_streams()
    skills_map()
    future_roadmap()
    print("Generated Chapter VI diagrams in", BASE)
