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


F_TITLE = font(26, True)
F_HEAD = font(15, True)
F_BODY = font(12)
F_SMALL = font(10)


def defs():
    return f"""
  <defs>
    <marker id="arrow_navy" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{NAVY}"/></marker>
    <marker id="arrow_gray" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{GRAY}"/></marker>
    <marker id="arrow_green" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{GREEN}"/></marker>
    <marker id="arrow_gold" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{GOLD}"/></marker>
  </defs>"""


def svg_box(x, y, w, h, title, lines, header=NAVY2, stroke=NAVY, fill=CREAM):
    cx = x + w / 2
    out = [
        f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>',
        f'  <rect x="{x}" y="{y}" width="{w}" height="22" rx="2" fill="{header}"/>',
        f'  <text x="{cx}" y="{y + 15}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8.5" fill="white" font-weight="600">{title}</text>',
    ]
    ty = y + 38
    for text, color, weight in lines:
        out.append(f'  <text x="{x + 8}" y="{ty}" font-family="JetBrains Mono, monospace" font-size="7.2" fill="{color}" font-weight="{weight}">{text}</text>')
        ty += 13
    return "\n".join(out)


def label(x, y, text, color=NAVY, size=7):
    return f'  <text x="{x}" y="{y}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="{size}" fill="{color}">{text}</text>'


def save_svg(name, viewbox, body):
    (BASE / f"{name}.svg").write_text(
        f'<svg viewBox="{viewbox}" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto;">\n{defs()}\n{body}\n</svg>\n',
        encoding="utf-8",
    )


def sp(p, s):
    return int(round(p[0] * s)), int(round(p[1] * s))


def draw_box(d, box, title, lines, s, header=NAVY2, stroke=NAVY, fill=CREAM):
    x, y, w, h = box
    d.rounded_rectangle((*sp((x, y), s), *sp((x + w, y + h), s)), radius=2 * s, fill=fill, outline=stroke, width=max(1, int(1.5 * s)))
    d.rounded_rectangle((*sp((x, y), s), *sp((x + w, y + 22), s)), radius=2 * s, fill=header, outline=header)
    tb = d.textbbox((0, 0), title, font=F_HEAD)
    d.text((int((x + w / 2) * s - (tb[2] - tb[0]) / 2), int((y + 4) * s)), title, fill="white", font=F_HEAD)
    ty = int((y + 32) * s)
    for text, color, weight in lines:
        d.text((int((x + 8) * s), ty), text, fill=color, font=F_HEAD if weight == "600" else F_BODY)
        ty += int(13 * s)


def arrow(d, p1, p2, color, s, width=1.5):
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
    d.line([sp(p, s) for p in pts], fill=color, width=max(1, int(1.5 * s)))
    arrow(d, pts[-2], pts[-1], color, s)


def save_png(name, size, draw_fn):
    s = 2
    img = Image.new("RGB", (size[0] * s, size[1] * s), "white")
    draw_fn(ImageDraw.Draw(img), s)
    img.save(BASE / f"{name}.png")


def global_architecture():
    # Coordinate table:
    # UI x=25 y=175 w=110 h=82 cx=80 cy=216 right=135 bottom=257
    # Gateway x=185 y=165 w=125 h=100 cx=247.5 cy=215 right=310 bottom=265
    # SCF x=370 y=55 w=125 h=82 cx=432.5 cy=96 right=495 bottom=137
    # FDL x=370 y=170 w=125 h=82 cx=432.5 cy=211 right=495 bottom=252
    # Props x=370 y=285 w=125 h=82 cx=432.5 cy=326 right=495 bottom=367
    # Infra x=585 y=55/170/285 w=140 h=82
    body = f"""
  <text x="25" y="30" font-family="JetBrains Mono, monospace" font-size="14" fill="{NAVY}" font-weight="700">Global Microservices Architecture</text>
{svg_box(25, 175, 110, 82, "REACT_UI", [("Vite + TypeScript", GRAY, "400"), ("role-based views", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(185, 165, 125, 100, "GATEWAY", [("JWT validation", GRAY, "400"), ("filters + routing", GRAY, "400"), ("circuit breakers", TEAL, "600")], header=NAVY2, stroke=NAVY)}
{svg_box(370, 55, 125, 82, "SCF_SERVICE", [("programs", GRAY, "400"), ("counterparties", GRAY, "400"), ("cashflows/docs", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(370, 170, 125, 82, "FDL_SERVICE", [("countries/cities", GRAY, "400"), ("currencies", GRAY, "400"), ("references", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(370, 285, 125, 82, "PROPERTIES", [("runtime values", GRAY, "400"), ("feature toggles", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(585, 55, 140, 82, "PLATFORM_STD", [("Eureka registry", GRAY, "400"), ("Config server", GRAY, "400")], header=GOLD, stroke=GOLD)}
{svg_box(585, 170, 140, 82, "SECURITY", [("Keycloak realm", GRAY, "400"), ("JWT + roles", GREEN, "600")], header=GREEN, stroke=GREEN)}
{svg_box(585, 285, 140, 82, "STORAGE", [("PostgreSQL", GRAY, "400"), ("MinIO + Gotenberg", TEAL, "600")], header=NAVY2, stroke=NAVY)}
  <line x1="135" y1="216" x2="184" y2="216" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
  <line x1="310" y1="196" x2="369" y2="96" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
  <line x1="310" y1="216" x2="369" y2="216" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
  <line x1="310" y1="236" x2="369" y2="326" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
  <path d="M 495,66 L 540,66 L 540,96 L 584,96" fill="none" stroke="{GOLD}" stroke-width="1.5" marker-end="url(#arrow_gold)"/>
  <path d="M 247,165 L 247,42 L 584,42 L 584,90" fill="none" stroke="{GREEN}" stroke-width="1.2" stroke-dasharray="5 2" marker-end="url(#arrow_green)"/>
  <path d="M 495,211 L 535,211 L 535,211 L 584,211" fill="none" stroke="{GREEN}" stroke-width="1.5" marker-end="url(#arrow_green)"/>
  <path d="M 495,326 L 535,326 L 535,326 L 584,326" fill="none" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
"""
    save_svg("ch2_global_architecture", "0 0 760 395", body)

    def draw_fn(d, s):
        d.text(sp((25, 14), s), "Global Microservices Architecture", font=F_TITLE, fill=NAVY)
        for box, title, lines, header, stroke in [
            ((25, 175, 110, 82), "REACT_UI", [("Vite + TypeScript", GRAY, "400"), ("role-based views", TEAL, "600")], TEAL, TEAL),
            ((185, 165, 125, 100), "GATEWAY", [("JWT validation", GRAY, "400"), ("filters + routing", GRAY, "400"), ("circuit breakers", TEAL, "600")], NAVY2, NAVY),
            ((370, 55, 125, 82), "SCF_SERVICE", [("programs", GRAY, "400"), ("counterparties", GRAY, "400"), ("cashflows/docs", TEAL, "600")], TEAL, TEAL),
            ((370, 170, 125, 82), "FDL_SERVICE", [("countries/cities", GRAY, "400"), ("currencies", GRAY, "400"), ("references", TEAL, "600")], TEAL, TEAL),
            ((370, 285, 125, 82), "PROPERTIES", [("runtime values", GRAY, "400"), ("feature toggles", TEAL, "600")], TEAL, TEAL),
            ((585, 55, 140, 82), "PLATFORM_STD", [("Eureka registry", GRAY, "400"), ("Config server", GRAY, "400")], GOLD, GOLD),
            ((585, 170, 140, 82), "SECURITY", [("Keycloak realm", GRAY, "400"), ("JWT + roles", GREEN, "600")], GREEN, GREEN),
            ((585, 285, 140, 82), "STORAGE", [("PostgreSQL", GRAY, "400"), ("MinIO + Gotenberg", TEAL, "600")], NAVY2, NAVY),
        ]:
            draw_box(d, box, title, lines, s, header, stroke)
        for p1, p2, c in [((135, 216), (184, 216), NAVY), ((310, 196), (369, 96), NAVY), ((310, 216), (369, 216), NAVY), ((310, 236), (369, 326), NAVY), ((495, 66), (584, 96), GOLD), ((495, 211), (584, 211), GREEN), ((495, 326), (584, 326), NAVY)]:
            arrow(d, p1, p2, c, s)
        path_arrow(d, [(247, 165), (247, 42), (584, 42), (584, 90)], GREEN, s)

    save_png("ch2_global_architecture", (760, 395), draw_fn)


def gateway_flow():
    body = f"""
  <text x="25" y="30" font-family="JetBrains Mono, monospace" font-size="14" fill="{NAVY}" font-weight="700">Gateway Routing and Filter Chain</text>
{svg_box(25, 150, 105, 74, "REQUEST", [("HTTP/API call", GRAY, "400"), ("multipart/JWT", TEAL, "600")], header=NAVY2, stroke=NAVY)}
{svg_box(165, 150, 115, 74, "SECURITY", [("public paths", GRAY, "400"), ("JWT validation", GREEN, "600")], header=GREEN, stroke=GREEN)}
{svg_box(315, 65, 115, 74, "FILTERS", [("ClamAV scan", GRAY, "400"), ("bruteforce", GRAY, "400")], header=GOLD, stroke=GOLD)}
{svg_box(315, 205, 115, 74, "OBSERVE", [("maintenance", GRAY, "400"), ("request id", TEAL, "600")], header=GOLD, stroke=GOLD)}
{svg_box(485, 60, 105, 70, "/SCF", [("business API", GRAY, "400"), ("port 8082", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(485, 155, 105, 70, "/FDL", [("reference API", GRAY, "400"), ("port 8083", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(485, 250, 105, 70, "/PROPERTIES", [("runtime config", GRAY, "400"), ("port 8084", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(635, 155, 105, 70, "EUREKA", [("lb:// routing", GRAY, "400"), ("fallbacks", GREEN, "600")], header=NAVY2, stroke=NAVY)}
  <line x1="130" y1="187" x2="164" y2="187" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
  <line x1="280" y1="187" x2="314" y2="102" stroke="{GOLD}" stroke-width="1.5" marker-end="url(#arrow_gold)"/>
  <line x1="280" y1="187" x2="314" y2="242" stroke="{GOLD}" stroke-width="1.5" marker-end="url(#arrow_gold)"/>
  <path d="M 430,102 L 460,102 L 460,95 L 484,95" fill="none" stroke="{TEAL}" stroke-width="1.5" marker-end="url(#arrow_green)"/>
  <line x1="430" y1="242" x2="484" y2="285" stroke="{TEAL}" stroke-width="1.5" marker-end="url(#arrow_green)"/>
  <line x1="430" y1="187" x2="484" y2="190" stroke="{TEAL}" stroke-width="1.5" marker-end="url(#arrow_green)"/>
  <line x1="590" y1="190" x2="634" y2="190" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
"""
    save_svg("ch2_gateway_filter_chain", "0 0 765 345", body)

    def draw_fn(d, s):
        d.text(sp((25, 14), s), "Gateway Routing and Filter Chain", font=F_TITLE, fill=NAVY)
        # Preview intentionally simplified but coordinate-equivalent to SVG.
        for box, title, lines, header, stroke in [
            ((25, 150, 105, 74), "REQUEST", [("HTTP/API call", GRAY, "400"), ("multipart/JWT", TEAL, "600")], NAVY2, NAVY),
            ((165, 150, 115, 74), "SECURITY", [("public paths", GRAY, "400"), ("JWT validation", GREEN, "600")], GREEN, GREEN),
            ((315, 65, 115, 74), "FILTERS", [("ClamAV scan", GRAY, "400"), ("bruteforce", GRAY, "400")], GOLD, GOLD),
            ((315, 205, 115, 74), "OBSERVE", [("maintenance", GRAY, "400"), ("request id", TEAL, "600")], GOLD, GOLD),
            ((485, 60, 105, 70), "/SCF", [("business API", GRAY, "400"), ("port 8082", TEAL, "600")], TEAL, TEAL),
            ((485, 155, 105, 70), "/FDL", [("reference API", GRAY, "400"), ("port 8083", TEAL, "600")], TEAL, TEAL),
            ((485, 250, 105, 70), "/PROPERTIES", [("runtime config", GRAY, "400"), ("port 8084", TEAL, "600")], TEAL, TEAL),
            ((635, 155, 105, 70), "EUREKA", [("lb:// routing", GRAY, "400"), ("fallbacks", GREEN, "600")], NAVY2, NAVY),
        ]:
            draw_box(d, box, title, lines, s, header, stroke)
        for p1, p2, c in [((130,187),(164,187),NAVY),((280,187),(314,102),GOLD),((280,187),(314,242),GOLD),((430,102),(484,95),TEAL),((430,242),(484,285),TEAL),((430,187),(484,190),TEAL),((590,190),(634,190),NAVY)]:
            arrow(d, p1, p2, c, s)

    save_png("ch2_gateway_filter_chain", (765, 345), draw_fn)


def auth_flow():
    body = f"""
  <text x="25" y="30" font-family="JetBrains Mono, monospace" font-size="14" fill="{NAVY}" font-weight="700">Authentication and Role Resolution Flow</text>
{svg_box(25, 150, 110, 78, "BROWSER", [("opens /auth", GRAY, "400"), ("PKCE challenge", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(175, 150, 110, 78, "KEYCLOAK", [("login", GRAY, "400"), ("code + tokens", GREEN, "600")], header=GREEN, stroke=GREEN)}
{svg_box(325, 150, 115, 78, "FRONTEND", [("sessionStorage", GRAY, "400"), ("decode JWT", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(480, 70, 115, 78, "BUSINESS_VIEW", [("BANK", GRAY, "400"), ("ANCHOR", GRAY, "400"), ("COUNTERPARTY", TEAL, "600")], header=GOLD, stroke=GOLD)}
{svg_box(480, 230, 115, 78, "AXIOS", [("Bearer token", GRAY, "400"), ("refresh on 401", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(635, 150, 105, 78, "BACKEND", [("resource server", GRAY, "400"), ("ROLE_* auth", GREEN, "600")], header=NAVY2, stroke=NAVY)}
  <line x1="135" y1="189" x2="174" y2="189" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
{label(155, 184, "redirect", NAVY)}
  <line x1="285" y1="189" x2="324" y2="189" stroke="{GREEN}" stroke-width="1.5" marker-end="url(#arrow_green)"/>
{label(305, 184, "tokens", GREEN)}
  <line x1="440" y1="170" x2="479" y2="109" stroke="{GOLD}" stroke-width="1.5" marker-end="url(#arrow_gold)"/>
  <line x1="440" y1="208" x2="479" y2="269" stroke="{TEAL}" stroke-width="1.5" marker-end="url(#arrow_green)"/>
  <line x1="595" y1="269" x2="634" y2="189" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
"""
    save_svg("ch2_auth_role_flow", "0 0 765 330", body)

    def draw_fn(d, s):
        d.text(sp((25, 14), s), "Authentication and Role Resolution Flow", font=F_TITLE, fill=NAVY)
        for box, title, lines, header, stroke in [
            ((25,150,110,78),"BROWSER",[("opens /auth",GRAY,"400"),("PKCE challenge",TEAL,"600")],TEAL,TEAL),
            ((175,150,110,78),"KEYCLOAK",[("login",GRAY,"400"),("code + tokens",GREEN,"600")],GREEN,GREEN),
            ((325,150,115,78),"FRONTEND",[("sessionStorage",GRAY,"400"),("decode JWT",TEAL,"600")],TEAL,TEAL),
            ((480,70,115,78),"BUSINESS_VIEW",[("BANK",GRAY,"400"),("ANCHOR",GRAY,"400"),("COUNTERPARTY",TEAL,"600")],GOLD,GOLD),
            ((480,230,115,78),"AXIOS",[("Bearer token",GRAY,"400"),("refresh on 401",TEAL,"600")],TEAL,TEAL),
            ((635,150,105,78),"BACKEND",[("resource server",GRAY,"400"),("ROLE_* auth",GREEN,"600")],NAVY2,NAVY),
        ]:
            draw_box(d, box, title, lines, s, header, stroke)
        for p1,p2,c in [((135,189),(174,189),NAVY),((285,189),(324,189),GREEN),((440,170),(479,109),GOLD),((440,208),(479,269),TEAL),((595,269),(634,189),NAVY)]:
            arrow(d,p1,p2,c,s)

    save_png("ch2_auth_role_flow", (765, 330), draw_fn)


def storage_flow():
    body = f"""
  <text x="25" y="30" font-family="JetBrains Mono, monospace" font-size="14" fill="{NAVY}" font-weight="700">Document Storage and Conversion Flow</text>
{svg_box(25, 155, 110, 78, "USER_UPLOAD", [("document file", GRAY, "400"), ("metadata", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(170, 155, 115, 78, "GATEWAY", [("multipart", GRAY, "400"), ("ClamAV scan", GREEN, "600")], header=GREEN, stroke=GREEN)}
{svg_box(325, 155, 125, 78, "SCF_SERVICE", [("validate file", GRAY, "400"), ("save metadata", TEAL, "600")], header=TEAL, stroke=TEAL)}
{svg_box(500, 75, 115, 78, "MINIO", [("object bytes", GRAY, "400"), ("presigned URL", TEAL, "600")], header=NAVY2, stroke=NAVY)}
{svg_box(500, 235, 115, 78, "GOTENBERG", [("DOCX/XLSX", GRAY, "400"), ("PDF output", GOLD, "600")], header=GOLD, stroke=GOLD)}
{svg_box(650, 155, 95, 78, "POSTGRES", [("document row", GRAY, "400"), ("file path", TEAL, "600")], header=NAVY2, stroke=NAVY)}
  <line x1="135" y1="194" x2="169" y2="194" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
  <line x1="285" y1="194" x2="324" y2="194" stroke="{GREEN}" stroke-width="1.5" marker-end="url(#arrow_green)"/>
  <line x1="450" y1="175" x2="499" y2="114" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
  <line x1="450" y1="213" x2="499" y2="274" stroke="{GOLD}" stroke-width="1.5" marker-end="url(#arrow_gold)"/>
  <line x1="450" y1="194" x2="649" y2="194" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
{label(548, 188, "metadata", NAVY)}
"""
    save_svg("ch2_storage_document_flow", "0 0 770 340", body)

    def draw_fn(d, s):
        d.text(sp((25,14),s), "Document Storage and Conversion Flow", font=F_TITLE, fill=NAVY)
        for box,title,lines,header,stroke in [
            ((25,155,110,78),"USER_UPLOAD",[("document file",GRAY,"400"),("metadata",TEAL,"600")],TEAL,TEAL),
            ((170,155,115,78),"GATEWAY",[("multipart",GRAY,"400"),("ClamAV scan",GREEN,"600")],GREEN,GREEN),
            ((325,155,125,78),"SCF_SERVICE",[("validate file",GRAY,"400"),("save metadata",TEAL,"600")],TEAL,TEAL),
            ((500,75,115,78),"MINIO",[("object bytes",GRAY,"400"),("presigned URL",TEAL,"600")],NAVY2,NAVY),
            ((500,235,115,78),"GOTENBERG",[("DOCX/XLSX",GRAY,"400"),("PDF output",GOLD,"600")],GOLD,GOLD),
            ((650,155,95,78),"POSTGRES",[("document row",GRAY,"400"),("file path",TEAL,"600")],NAVY2,NAVY),
        ]:
            draw_box(d,box,title,lines,s,header,stroke)
        for p1,p2,c in [((135,194),(169,194),NAVY),((285,194),(324,194),GREEN),((450,175),(499,114),NAVY),((450,213),(499,274),GOLD),((450,194),(649,194),NAVY)]:
            arrow(d,p1,p2,c,s)

    save_png("ch2_storage_document_flow", (770, 340), draw_fn)


if __name__ == "__main__":
    global_architecture()
    gateway_flow()
    auth_flow()
    storage_flow()
    print("Generated Chapter II diagrams in", BASE)
