from __future__ import annotations

import math
from pathlib import Path
from xml.sax.saxutils import escape

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
WHITE = "#FFFFFF"
DARK = "#1A1A1A"


def font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/seguisb.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


class Diagram:
    def __init__(self, name: str, width: int, height: int, title: str | None = None):
        self.name = name
        self.width = width
        self.height = height
        self.svg: list[str] = []
        self.scale = 3
        self.image = Image.new("RGB", (width * self.scale, height * self.scale), WHITE)
        self.draw = ImageDraw.Draw(self.image)
        self.fonts = {
            "title": font(24 * self.scale, True),
            "head": font(12 * self.scale, True),
            "body": font(10 * self.scale),
            "small": font(8 * self.scale),
            "tiny": font(7 * self.scale),
        }
        if title:
            self.text(26, 28, title, size=14, color=NAVY, weight="700")

    def _p(self, x: float, y: float):
        return int(round(x * self.scale)), int(round(y * self.scale))

    def _font(self, size: float, weight: str = "400"):
        return font(max(7, int(size * self.scale)), weight in {"600", "700"})

    def text(
        self,
        x: float,
        y: float,
        value: str,
        size: float = 8,
        color: str = GRAY,
        weight: str = "400",
        anchor: str = "start",
    ):
        value_svg = escape(value)
        self.svg.append(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
            f'font-family="JetBrains Mono, monospace" font-size="{size}" '
            f'fill="{color}" font-weight="{weight}">{value_svg}</text>'
        )
        f = self._font(size, weight)
        bbox = self.draw.textbbox((0, 0), value, font=f)
        tx = x * self.scale
        if anchor == "middle":
            tx -= (bbox[2] - bbox[0]) / 2
        elif anchor == "end":
            tx -= bbox[2] - bbox[0]
        self.draw.text((int(tx), int((y - size + 1) * self.scale)), value, fill=color, font=f)

    def rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        fill: str = CREAM,
        stroke: str = NAVY,
        sw: float = 1.2,
        rx: float = 2,
        dash: str | None = None,
    ):
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        self.svg.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash_attr}/>'
        )
        box = (*self._p(x, y), *self._p(x + w, y + h))
        width = max(1, int(sw * self.scale))
        self.draw.rounded_rectangle(
            box, radius=int(rx * self.scale), fill=fill, outline=stroke, width=width
        )

    def line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: str = NAVY,
        sw: float = 1.2,
        arrow: bool = False,
        dash: str | None = None,
    ):
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        marker = f' marker-end="url(#arrow_{self._marker_color(color)})"' if arrow else ""
        self.svg.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="{sw}"{dash_attr}{marker}/>'
        )
        p1 = self._p(x1, y1)
        p2 = self._p(x2, y2)
        width = max(1, int(sw * self.scale))
        if dash:
            self._draw_dashed(p1, p2, color, width)
        else:
            self.draw.line((*p1, *p2), fill=color, width=width)
        if arrow:
            self._arrow_head(x1, y1, x2, y2, color)

    def path(self, points: list[tuple[float, float]], color: str = NAVY, sw: float = 1.2, arrow: bool = False, dash: str | None = None):
        d = "M " + " L ".join(f"{x},{y}" for x, y in points)
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        marker = f' marker-end="url(#arrow_{self._marker_color(color)})"' if arrow else ""
        self.svg.append(
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}"{dash_attr}{marker}/>'
        )
        scaled = [self._p(x, y) for x, y in points]
        width = max(1, int(sw * self.scale))
        if dash:
            for start, end in zip(scaled, scaled[1:]):
                self._draw_dashed(start, end, color, width)
        else:
            self.draw.line(scaled, fill=color, width=width)
        if arrow and len(points) >= 2:
            x1, y1 = points[-2]
            x2, y2 = points[-1]
            self._arrow_head(x1, y1, x2, y2, color)

    def ellipse(self, x: float, y: float, w: float, h: float, fill: str = WHITE, stroke: str = NAVY, sw: float = 1.2):
        self.svg.append(
            f'<ellipse cx="{x + w / 2}" cy="{y + h / 2}" rx="{w / 2}" ry="{h / 2}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        )
        self.draw.ellipse((*self._p(x, y), *self._p(x + w, y + h)), fill=fill, outline=stroke, width=max(1, int(sw * self.scale)))

    def circle(self, cx: float, cy: float, r: float, fill: str, stroke: str | None = None, sw: float = 1.0):
        stroke_attr = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{stroke_attr}/>')
        box = (*self._p(cx - r, cy - r), *self._p(cx + r, cy + r))
        self.draw.ellipse(box, fill=fill, outline=stroke, width=max(1, int(sw * self.scale)) if stroke else 1)

    def polygon(self, points: list[tuple[float, float]], fill: str, stroke: str = NAVY, sw: float = 1.2):
        pts = " ".join(f"{x},{y}" for x, y in points)
        self.svg.append(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        self.draw.polygon([self._p(x, y) for x, y in points], fill=fill, outline=stroke)

    def box(self, x: float, y: float, w: float, h: float, title: str, lines: list[str], header: str = NAVY2, stroke: str = NAVY, fill: str = CREAM):
        self.rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.2, rx=2)
        self.rect(x, y, w, 22, fill=header, stroke=header, sw=1.0, rx=2)
        self.text(x + w / 2, y + 15, title, size=8.2, color=WHITE, weight="700", anchor="middle")
        ty = y + 38
        for line in lines:
            color = TEAL if line.startswith("*") else GRAY
            value = line[1:] if line.startswith("*") else line
            self.text(x + 8, ty, value, size=7.2, color=color, weight="600" if line.startswith("*") else "400")
            ty += 12

    def uml_class(self, x: float, y: float, w: float, name: str, attrs: list[str], methods: list[str] | None = None, fill: str = CREAM, stroke: str = NAVY):
        methods = methods or []
        line_h = 12
        h = 28 + line_h * (len(attrs) + len(methods)) + (10 if methods else 0) + 8
        self.rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.2, rx=2)
        self.rect(x, y, w, 24, fill=stroke, stroke=stroke, sw=1.0, rx=2)
        self.text(x + w / 2, y + 16, name, size=8.2, color=WHITE, weight="700", anchor="middle")
        self.line(x, y + 24, x + w, y + 24, stroke, sw=0.8)
        ty = y + 39
        for attr in attrs:
            self.text(x + 8, ty, attr, size=6.7, color=DARK)
            ty += line_h
        if methods:
            self.line(x, ty - 5, x + w, ty - 5, LINE, sw=0.8)
            for method in methods:
                self.text(x + 8, ty + 4, method, size=6.7, color=GRAY)
                ty += line_h
        return h

    def state(self, x: float, y: float, w: float, label: str, fill: str = TEAL):
        self.rect(x, y, w, 28, fill=fill, stroke=fill, sw=1.0, rx=14)
        self.text(x + w / 2, y + 18, label, size=8.0, color=WHITE, weight="700", anchor="middle")

    def usecase(self, cx: float, cy: float, w: float, h: float, label: str, stroke: str = NAVY):
        self.ellipse(cx - w / 2, cy - h / 2, w, h, fill=WHITE, stroke=stroke, sw=1.2)
        parts = label.split("\n")
        start = cy - (len(parts) - 1) * 5
        for i, part in enumerate(parts):
            self.text(cx, start + i * 11, part, size=7.2, color=DARK, weight="600", anchor="middle")

    def actor(self, x: float, y: float, label: str, color: str = NAVY):
        self.circle(x, y, 8, WHITE, stroke=color, sw=1.2)
        self.line(x, y + 8, x, y + 38, color, sw=1.2)
        self.line(x - 18, y + 20, x + 18, y + 20, color, sw=1.2)
        self.line(x, y + 38, x - 16, y + 60, color, sw=1.2)
        self.line(x, y + 38, x + 16, y + 60, color, sw=1.2)
        for i, part in enumerate(label.split("\n")):
            self.text(x, y + 78 + i * 11, part, size=7, color=color, weight="700", anchor="middle")

    def lifeline(self, x: float, y: float, h: float, name: str, w: float = 92):
        self.rect(x - w / 2, y, w, 22, fill=WARM, stroke=NAVY, sw=1.0, rx=2)
        self.text(x, y + 15, name, size=6.8, color=NAVY, weight="700", anchor="middle")
        self.line(x, y + 22, x, y + h, color=LINE, sw=0.8, dash="4 3")

    def activation(self, x: float, y: float, h: float):
        self.rect(x - 3, y, 6, h, fill=WHITE, stroke=GRAY, sw=0.8, rx=0)

    def save(self):
        defs = f"""
<defs>
  <marker id="arrow_navy" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{NAVY}"/></marker>
  <marker id="arrow_teal" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{TEAL}"/></marker>
  <marker id="arrow_gold" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{GOLD}"/></marker>
  <marker id="arrow_green" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{GREEN}"/></marker>
  <marker id="arrow_red" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{RED}"/></marker>
  <marker id="arrow_gray" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{GRAY}"/></marker>
</defs>"""
        svg = (
            f'<svg viewBox="0 0 {self.width} {self.height}" xmlns="http://www.w3.org/2000/svg" '
            f'style="width:100%; height:auto;">\n{defs}\n' + "\n".join(self.svg) + "\n</svg>\n"
        )
        (BASE / f"{self.name}.svg").write_text(svg, encoding="utf-8")
        self.image.save(BASE / f"{self.name}.png")

    @staticmethod
    def _marker_color(color: str) -> str:
        return {
            NAVY: "navy",
            TEAL: "teal",
            GOLD: "gold",
            GREEN: "green",
            RED: "red",
            GRAY: "gray",
        }.get(color, "navy")

    def _draw_dashed(self, p1, p2, color, width):
        x1, y1 = p1
        x2, y2 = p2
        length = math.hypot(x2 - x1, y2 - y1)
        if length <= 0:
            return
        dash = 12
        gap = 8
        ux = (x2 - x1) / length
        uy = (y2 - y1) / length
        dist = 0
        while dist < length:
            end = min(dist + dash, length)
            self.draw.line(
                (x1 + ux * dist, y1 + uy * dist, x1 + ux * end, y1 + uy * end),
                fill=color,
                width=width,
            )
            dist += dash + gap

    def _arrow_head(self, x1: float, y1: float, x2: float, y2: float, color: str):
        sx1, sy1 = self._p(x1, y1)
        sx2, sy2 = self._p(x2, y2)
        dx = sx2 - sx1
        dy = sy2 - sy1
        angle = math.atan2(dy, dx)
        length = 8 * self.scale
        spread = math.radians(28)
        p1 = (
            sx2 - length * math.cos(angle - spread),
            sy2 - length * math.sin(angle - spread),
        )
        p2 = (
            sx2 - length * math.cos(angle + spread),
            sy2 - length * math.sin(angle + spread),
        )
        self.draw.polygon([(sx2, sy2), p1, p2], fill=color)


def ch1_scf_ecosystem():
    d = Diagram("ch1_scf_ecosystem", 780, 430, "Supply Chain Finance Ecosystem")
    d.box(300, 165, 180, 90, "SCF PROGRAM", ["product rules", "eligibility", "*finance limits"], TEAL, TEAL)
    d.box(50, 175, 150, 76, "ANCHOR", ["large buyer/seller", "*risk reference"], NAVY2, NAVY)
    d.box(580, 175, 150, 76, "COUNTERPARTY", ["supplier / buyer", "*SME participant"], NAVY2, NAVY)
    d.box(310, 45, 160, 74, "BANK", ["program owner", "*financing control"], GREEN, GREEN)
    d.box(310, 320, 160, 74, "INVOICE POOL", ["cashflows", "*trade documents"], GOLD, GOLD)
    d.line(200, 213, 299, 213, NAVY, arrow=True)
    d.text(250, 205, "program relationship", 6.7, NAVY, anchor="middle")
    d.line(480, 213, 579, 213, NAVY, arrow=True)
    d.text(530, 205, "eligible operations", 6.7, NAVY, anchor="middle")
    d.line(390, 119, 390, 164, GREEN, arrow=True)
    d.text(428, 144, "governance", 6.7, GREEN, anchor="middle")
    d.line(390, 320, 390, 256, GOLD, arrow=True)
    d.text(440, 296, "invoice evidence", 6.7, GOLD, anchor="middle")
    d.path([(580, 251), (580, 285), (200, 285), (200, 252)], GRAY, sw=1.2, arrow=True)
    d.text(390, 278, "goods / services and invoice exchange", 6.7, GRAY, anchor="middle")
    d.save()


def ch1_workflow():
    d = Diagram("ch1_internship_workflow", 780, 360, "Daily Development and Validation Workflow")
    lanes = [("Developer", 60, 92), ("Tech Lead", 60, 176), ("Tester", 60, 260)]
    for label, x, y in lanes:
        d.rect(30, y - 34, 710, 68, WARM if y != 176 else CREAM, LINE, 1, 2)
        d.text(x, y + 4, label, 8, NAVY if y != 260 else GREEN, "700", "middle")
    d.box(150, 70, 110, 46, "JIRA", ["ticket"], TEAL, TEAL)
    d.box(310, 70, 130, 46, "IMPLEMENT", ["backend + UI"], TEAL, TEAL)
    d.box(500, 70, 110, 46, "PUSH", ["Bitbucket"], NAVY2, NAVY)
    d.box(310, 154, 130, 46, "PR REVIEW", ["comments"], GOLD, GOLD)
    d.box(500, 154, 110, 46, "MERGE", ["approved"], GREEN, GREEN)
    d.box(500, 238, 110, 46, "VERIFY", ["QA result"], GREEN, GREEN)
    d.line(260, 93, 309, 93, NAVY, arrow=True)
    d.line(440, 93, 499, 93, NAVY, arrow=True)
    d.path([(555, 116), (555, 154)], GOLD, arrow=True)
    d.line(440, 177, 499, 177, GREEN, arrow=True)
    d.path([(365, 154), (365, 128), (365, 117)], GOLD, arrow=True)
    d.path([(555, 200), (555, 238)], GREEN, arrow=True)
    d.path([(500, 262), (450, 262), (450, 177), (441, 177)], RED, sw=1.0, arrow=True, dash="5 3")
    d.text(420, 252, "fix if rejected", 6.5, RED, anchor="middle")
    d.save()


def ch1_timeline():
    d = Diagram("ch1_internship_timeline", 780, 330, "Internship Timeline")
    d.line(70, 165, 710, 165, NAVY, sw=2.0)
    events = [
        (90, "FEB", "Remote training", ["business logic", "Java / Spring Boot"], TEAL, 218),
        (240, "W3", "On-site work", ["team integration", "SCF codebase"], GREEN, 60),
        (390, "S2-S8", "Sprint delivery", ["Jira tickets", "PR + testing"], TEAL, 218),
        (540, "MON", "PO refinement", ["module rules", "diagram reviews"], GOLD, 60),
        (690, "JUL", "Report closure", ["synthesis", "final polish"], GREEN, 218),
    ]
    for x, code, title, lines, color, by in events:
        d.circle(x, 165, 7, color, NAVY)
        d.line(x, 172 if by > 165 else 158, x, by - 1 if by > 165 else by + 82, GRAY)
        d.box(x - 65, by, 130, 82, code, [title, *lines], color, color)
    d.save()


def ch2_architecture():
    d = Diagram("ch2_global_architecture", 820, 440, "Global Architecture of the SCF Platform")
    d.rect(40, 72, 740, 78, WARM, LINE)
    d.rect(40, 178, 740, 102, CREAM, LINE)
    d.rect(40, 310, 740, 78, WARM, LINE)
    d.text(65, 98, "Channel Layer", 8, NAVY, "700")
    d.text(65, 205, "Business and Edge Layer", 8, NAVY, "700")
    d.text(65, 337, "Infrastructure Layer", 8, NAVY, "700")
    d.box(210, 90, 120, 46, "React SPA", ["role views"], TEAL, TEAL)
    d.box(390, 90, 130, 46, "Axios Client", ["gateway paths"], NAVY2, NAVY)
    d.box(140, 205, 135, 58, "adria-gateway", ["JWT, filters", "*routing"], NAVY2, NAVY)
    d.box(330, 205, 145, 58, "scf-service", ["modular monolith", "*SCF modules"], TEAL, TEAL)
    d.box(530, 205, 130, 58, "FDL / Props", ["reference data", "runtime values"], TEAL, TEAL)
    d.box(105, 330, 120, 42, "Keycloak", ["OIDC"], GREEN, GREEN)
    d.box(260, 330, 120, 42, "PostgreSQL", ["business data"], NAVY2, NAVY)
    d.box(415, 330, 120, 42, "MinIO", ["documents"], GOLD, GOLD)
    d.box(570, 330, 120, 42, "Kafka", ["events"], DARK, DARK)
    d.line(330, 113, 389, 113, NAVY, arrow=True)
    d.path([(455, 136), (455, 175), (208, 175), (208, 204)], NAVY, arrow=True)
    d.line(275, 234, 329, 234, NAVY, arrow=True)
    d.line(475, 234, 529, 234, NAVY, arrow=True)
    d.path([(208, 205), (208, 170), (165, 170), (165, 329)], GREEN, arrow=True, dash="5 3")
    d.path([(402, 263), (402, 309), (320, 309), (320, 329)], NAVY, arrow=True)
    d.path([(420, 263), (420, 329)], GOLD, arrow=True)
    d.path([(448, 263), (448, 298), (630, 298), (630, 329)], DARK, arrow=True)
    d.save()


def ch2_gateway():
    d = Diagram("ch2_gateway_filter_chain", 820, 340, "Gateway Routing and Filter Chain")
    nodes = [
        (45, "Request", "browser/API", NAVY2, NAVY),
        (175, "Auth", "JWT / public", GREEN, GREEN),
        (305, "Security", "ClamAV, limits", GOLD, GOLD),
        (450, "Routing", "/scf /fdl", TEAL, TEAL),
        (590, "Discovery", "lb:// service", NAVY2, NAVY),
        (710, "Fallback", "resilience", RED, RED),
    ]
    for x, title, line, header, stroke in nodes:
        d.box(x, 135, 95, 58, title.upper(), [line], header, stroke)
    for i in range(len(nodes) - 1):
        x1 = nodes[i][0] + 95
        x2 = nodes[i + 1][0] - 1
        d.line(x1, 164, x2, 164, NAVY if i < 4 else RED, arrow=True)
    d.box(450, 48, 95, 50, "HMAC", ["webhooks"], GREEN, GREEN)
    d.path([(497, 98), (497, 134)], GREEN, arrow=True, dash="5 3")
    d.box(450, 230, 95, 50, "Logging", ["correlation"], GOLD, GOLD)
    d.path([(497, 193), (497, 229)], GOLD, arrow=True, dash="5 3")
    d.save()


def ch2_auth():
    d = Diagram("ch2_auth_role_flow", 820, 360, "Authentication and Role Resolution")
    xs = [70, 210, 360, 520, 675]
    labels = ["Browser", "Keycloak", "React Auth", "Business View", "Backend"]
    for x, label in zip(xs, labels):
        d.lifeline(x, 55, 315, label, 96)
    messages = [
        (70, 210, 100, "authorize + PKCE", NAVY),
        (210, 70, 130, "authorization code", GOLD),
        (70, 210, 160, "token exchange", NAVY),
        (210, 360, 190, "access + refresh token", GREEN),
        (360, 520, 220, "decode roles", TEAL),
        (520, 675, 250, "Bearer API call", NAVY),
        (675, 520, 280, "authorized response", GOLD),
    ]
    for x1, x2, y, text, color in messages:
        end = x2 - 1 if x2 > x1 else x2 + 1
        d.line(x1, y, end, y, color, arrow=True, dash="4 3" if color == GOLD else None)
        d.text((x1 + x2) / 2, y - 6, text, 6.2, color, anchor="middle")
    d.save()


def ch2_storage():
    d = Diagram("ch2_storage_document_flow", 820, 360, "Document Storage and Conversion Flow")
    d.box(55, 150, 115, 62, "Upload UI", ["multipart file"], TEAL, TEAL)
    d.box(220, 150, 125, 62, "Gateway", ["ClamAV scan"], GREEN, GREEN)
    d.box(395, 150, 130, 62, "SCF Service", ["metadata + ports"], TEAL, TEAL)
    d.box(610, 65, 120, 62, "MinIO", ["object bytes"], NAVY2, NAVY)
    d.box(610, 150, 120, 62, "PostgreSQL", ["document row"], NAVY2, NAVY)
    d.box(610, 235, 120, 62, "Gotenberg", ["PDF conversion"], GOLD, GOLD)
    d.line(170, 181, 219, 181, NAVY, arrow=True)
    d.line(345, 181, 394, 181, GREEN, arrow=True)
    d.line(525, 170, 609, 96, NAVY, arrow=True)
    d.line(525, 181, 609, 181, NAVY, arrow=True)
    d.line(525, 194, 609, 266, GOLD, arrow=True)
    d.save()


def ch3_class():
    d = Diagram("ch3_core_data_model", 860, 520, "Main SCF Class Diagram")
    d.uml_class(330, 40, 170, "ScfProgramConfiguration", ["+id: UUID", "+reference: String", "+currency: Currency", "+financePercent: BigDecimal", "+status: ProgramStatus"], [], CREAM, TEAL)
    d.uml_class(65, 62, 150, "ScfProductDefinition", ["+code: String", "+type: ProductType", "+instrument: Instrument", "+status: ApprovalStatus"], [], CREAM, NAVY)
    d.uml_class(640, 62, 150, "ScfAnchor", ["+anchorCode: String", "+name: String", "+role: AnchorRole"], [], CREAM, NAVY)
    d.uml_class(65, 245, 160, "ScfCounterParty", ["+legalName: String", "+role: CounterpartyRole", "+status: CounterPartyStatus", "+taxIdentifier: String"], [], CREAM, TEAL)
    d.uml_class(345, 245, 150, "ScfProgramCounterParty", ["+roleInProgram: String", "+limitAmount: BigDecimal", "+active: Boolean"], [], CREAM, GOLD)
    d.uml_class(640, 245, 145, "Country", ["+code: String", "+name: String"], [], CREAM, NAVY)
    d.uml_class(640, 380, 145, "City", ["+code: String", "+name: String", "+postalCode: String"], [], CREAM, NAVY)
    d.uml_class(65, 390, 160, "ScfBankAccount", ["+iban: String", "+swiftCode: String", "+currency: Currency", "+primaryAccount: Boolean"], [], CREAM, NAVY)
    d.uml_class(330, 390, 170, "ScfProgramCashflow", ["+invoiceNumber: String", "+amount: BigDecimal", "+dueDate: LocalDate", "+validationStatus: String"], [], CREAM, GOLD)
    d.line(215, 100, 329, 100, NAVY)
    d.text(235, 94, "1", 7, NAVY)
    d.text(310, 94, "0..*", 7, NAVY)
    d.line(500, 100, 639, 100, NAVY)
    d.text(515, 94, "1", 7, NAVY)
    d.text(610, 94, "1..*", 7, NAVY)
    d.line(407, 151, 407, 244, GOLD)
    d.text(414, 170, "1", 7, NAVY)
    d.text(414, 235, "0..*", 7, NAVY)
    d.line(225, 310, 344, 310, GOLD)
    d.text(242, 304, "1", 7, NAVY)
    d.text(314, 304, "0..*", 7, NAVY)
    d.path([(145, 344), (145, 389)], NAVY)
    d.text(152, 356, "1", 7, NAVY)
    d.text(152, 383, "0..*", 7, NAVY)
    d.path([(495, 310), (565, 310), (565, 180), (500, 180)], GOLD)
    d.text(520, 304, "program link", 6.5, GOLD)
    d.line(712, 336, 712, 379, NAVY)
    d.text(718, 355, "1", 7, NAVY)
    d.text(718, 374, "0..*", 7, NAVY)
    d.path([(640, 285), (595, 285), (595, 130), (500, 130)], NAVY)
    d.text(600, 278, "country", 6.5, NAVY)
    d.path([(407, 151), (407, 205), (555, 205), (555, 452), (500, 452)], GOLD, dash="5 3")
    d.text(570, 318, "1 to 0..*", 6.5, GOLD)
    d.save()


def ch3_maker_checker():
    d = Diagram("ch3_maker_checker_state", 780, 310, "UML State Machine - Maker/Checker Governance")
    d.circle(70, 152, 8, NAVY)
    d.state(125, 138, 105, "DRAFT", TEAL)
    d.state(295, 138, 155, "PENDING_APPROVAL", GOLD)
    d.state(535, 74, 110, "APPROVED", GREEN)
    d.state(535, 202, 110, "REJECTED", RED)
    d.circle(705, 88, 8, WHITE, NAVY, 1.4)
    d.circle(705, 88, 4, NAVY)
    d.line(78, 152, 124, 152, NAVY, arrow=True)
    d.line(230, 152, 294, 152, NAVY, arrow=True)
    d.text(262, 146, "submit()", 6.7, NAVY, anchor="middle")
    d.line(450, 145, 534, 88, GREEN, arrow=True)
    d.text(492, 108, "approve()", 6.7, GREEN, anchor="middle")
    d.line(450, 160, 534, 216, RED, arrow=True)
    d.text(492, 199, "reject(comment)", 6.7, RED, anchor="middle")
    d.line(645, 88, 696, 88, GREEN, arrow=True)
    d.path([(535, 216), (240, 216), (240, 166), (230, 166)], GRAY, arrow=True, dash="5 3")
    d.text(380, 209, "restore originalData when update is rejected", 6.5, GRAY, anchor="middle")
    d.save()


def ch3_program_activity():
    d = Diagram("ch3_program_configuration_flow", 760, 470, "UML Activity - Program Configuration")
    d.circle(380, 58, 8, NAVY)
    y = 95
    actions = [
        ("Select product definition", TEAL),
        ("Enter general program data", TEAL),
        ("Assign anchor and counterparties", TEAL),
        ("Configure fees and flat charges", GOLD),
        ("Configure cashflow and disbursement rules", GOLD),
    ]
    for label, color in actions:
        d.rect(260, y, 240, 32, CREAM, color, 1.2, 16)
        d.text(380, y + 20, label, 7.4, color, "700", "middle")
        d.line(380, y - 18, 380, y - 1, color, arrow=True)
        y += 58
    d.polygon([(380, 382), (450, 414), (380, 446), (310, 414)], WARM, NAVY)
    d.text(380, 411, "Complete?", 7.4, NAVY, "700", "middle")
    d.line(380, 359, 380, 381, GOLD, arrow=True)
    d.path([(310, 414), (210, 414), (210, 153), (259, 153)], RED, arrow=True, dash="5 3")
    d.text(238, 405, "[no]", 7, RED, anchor="middle")
    d.line(450, 414, 600, 414, GREEN, arrow=True)
    d.text(515, 406, "[yes] submit for approval", 7, GREEN, anchor="middle")
    d.circle(630, 414, 8, WHITE, NAVY, 1.4)
    d.circle(630, 414, 4, NAVY)
    d.save()


def use_case_back_office():
    d = Diagram("ch4_use_case_back_office", 920, 560, "UML Use Case Diagram - Back Office")
    d.actor(85, 150, "Bank\nMaker", TEAL)
    d.actor(85, 365, "Bank\nChecker", GREEN)
    d.rect(210, 70, 650, 440, WHITE, NAVY, 1.2, 2)
    d.text(535, 94, "SCF Back Office Boundary", 8, NAVY, "700", "middle")
    cases = [
        (390, 125, "Create / edit\nproduct", TEAL),
        (390, 225, "Configure\nprogram", TEAL),
        (390, 325, "Onboard\ncounterparty", TEAL),
        (655, 225, "Submit\npending change", GOLD),
        (390, 445, "Review pending\noperation", GREEN),
        (655, 445, "Approve or\nreject", GREEN),
    ]
    for cx, cy, label, color in cases:
        d.usecase(cx, cy, 150, 48, label, color)
    d.line(112, 190, 315, 125, GRAY)
    d.line(112, 190, 315, 225, GRAY)
    d.line(112, 190, 315, 325, GRAY)
    d.line(112, 405, 315, 445, GRAY)
    d.line(465, 125, 580, 207, GOLD, dash="5 3", arrow=True)
    d.text(520, 158, "<<include>>", 6.4, GOLD, anchor="middle")
    d.line(465, 225, 580, 225, GOLD, dash="5 3", arrow=True)
    d.text(522, 216, "<<include>>", 6.4, GOLD, anchor="middle")
    d.line(465, 325, 580, 243, GOLD, dash="5 3", arrow=True)
    d.text(520, 286, "<<include>>", 6.4, GOLD, anchor="middle")
    d.line(465, 445, 580, 445, GREEN, dash="5 3", arrow=True)
    d.text(522, 436, "<<include>>", 6.4, GREEN, anchor="middle")
    d.save()


def use_case_middle_office():
    d = Diagram("ch4_use_case_middle_office", 920, 670, "UML Use Case Diagram - Middle Office")
    d.actor(85, 170, "Middle Office\nAnalyst", TEAL)
    d.actor(85, 500, "Compliance /\nAudit", NAVY)
    d.rect(210, 70, 650, 550, WHITE, NAVY, 1.2, 2)
    d.text(535, 94, "SCF Middle Office Boundary", 8, NAVY, "700", "middle")
    cases = [
        (390, 125, "Monitor\ntransactions", TEAL),
        (655, 125, "Filter inquiry\nresults", TEAL),
        (390, 245, "Follow failed\npayments", RED),
        (390, 365, "Export operational\nreport", GOLD),
        (655, 535, "Consult audit\ntrail", NAVY),
        (390, 485, "Analyze portfolio\nexposure", GREEN),
    ]
    for cx, cy, label, color in cases:
        d.usecase(cx, cy, 155, 48, label, color)
    d.line(112, 210, 312, 125, GRAY)
    d.line(112, 210, 312, 245, GRAY)
    d.line(112, 210, 312, 365, GRAY)
    d.line(112, 210, 312, 485, GRAY)
    d.line(112, 540, 577, 535, GRAY)
    d.line(468, 125, 577, 125, TEAL, dash="5 3", arrow=True)
    d.text(522, 116, "<<include>>", 6.4, TEAL, anchor="middle")
    d.save()


def use_case_front_office():
    d = Diagram("ch4_use_case_front_office", 900, 520, "UML Use Case Diagram - Front Office")
    d.rect(190, 60, 545, 410, WHITE, NAVY, 1.2, 2)
    d.text(462, 84, "SCF Front Office Boundary", 8, NAVY, "700", "middle")
    d.actor(80, 105, "Buyer", TEAL)
    d.actor(80, 305, "Supplier", GREEN)
    d.actor(820, 205, "Bank", NAVY)
    cases = [
        (600, 105, "Request\npayment", GREEN),
        (360, 170, "Track invoice\nstatus", TEAL),
        (520, 230, "Consult\ntransactions", NAVY),
        (360, 285, "Upload or create\ninvoice", TEAL),
        (600, 330, "Request\nfinance", GOLD),
        (520, 415, "Request early\npayment", GREEN),
    ]
    for cx, cy, label, color in cases:
        d.usecase(cx, cy, 150, 48, label, color)
    # Primary actors are on the left. The bank is the only secondary/supporting actor.
    d.line(108, 145, 525, 105, GRAY)
    d.line(108, 145, 285, 170, GRAY)
    d.line(108, 145, 445, 230, GRAY)
    d.line(108, 345, 285, 285, GRAY)
    d.line(108, 345, 525, 330, GRAY)
    d.line(108, 345, 445, 415, GRAY)
    d.line(792, 245, 675, 105, GRAY)
    d.line(792, 245, 675, 330, GRAY)
    d.line(792, 245, 595, 415, GRAY)
    d.save()


def ch4_navigation():
    d = Diagram("ch4_navigation_role_flow", 760, 360, "Frontend Routing and Role-Based Navigation")
    d.box(55, 150, 120, 58, "App.tsx", ["providers", "routes"], TEAL, TEAL)
    d.box(230, 75, 135, 58, "KeycloakAuth", ["PKCE callback", "tokens"], GREEN, GREEN)
    d.box(230, 230, 135, 58, "AuthGuard", ["protected route", "redirect"], NAVY2, NAVY)
    d.box(420, 150, 120, 58, "Index.tsx", ["sidebar", "selectedModule"], TEAL, TEAL)
    d.box(595, 75, 120, 58, "BusinessView", ["BANK", "ANCHOR / CP"], GOLD, GOLD)
    d.box(595, 230, 120, 58, "Modules", ["dashboard", "SCF flows"], NAVY2, NAVY)
    d.line(175, 165, 229, 104, GREEN, arrow=True)
    d.line(175, 193, 229, 259, NAVY, arrow=True)
    d.line(365, 259, 419, 193, NAVY, arrow=True)
    d.line(540, 165, 594, 104, GOLD, arrow=True)
    d.line(540, 193, 594, 259, NAVY, arrow=True)
    d.save()


def ch4_invoice_upload():
    d = Diagram("ch4_invoice_upload_flow", 760, 350, "Invoice Upload Component Interaction")
    d.box(45, 145, 125, 68, "InvoiceUploadForm", ["state owner", "program context"], TEAL, TEAL)
    d.box(230, 60, 130, 58, "ExcelUploader", ["spreadsheet rows"], NAVY2, NAVY)
    d.box(230, 232, 130, 58, "ScannedUploader", ["PDF / image path"], GOLD, GOLD)
    d.box(420, 145, 130, 68, "UploadTable", ["row validation", "issue details"], TEAL, TEAL)
    d.box(610, 60, 115, 58, "Summary", ["counts"], NAVY2, NAVY)
    d.box(610, 232, 115, 58, "Reports", ["rejection file"], GOLD, GOLD)
    d.line(170, 165, 229, 89, NAVY, arrow=True)
    d.line(170, 193, 229, 261, GOLD, arrow=True)
    d.line(360, 89, 419, 165, NAVY, arrow=True)
    d.line(360, 261, 419, 193, GOLD, arrow=True)
    d.line(550, 165, 609, 89, NAVY, arrow=True)
    d.line(550, 193, 609, 261, GOLD, arrow=True)
    d.save()


def ch4_disbursement_wizard():
    d = Diagram("ch4_finance_disbursement_wizard", 820, 285, "Finance Disbursement Wizard - Corrected Step Order")
    steps = [
        ("1", "Program /\nProduct", TEAL),
        ("2", "Invoice\nSelection", TEAL),
        ("3", "Finance\nDetails", TEAL),
        ("4", "Repayment\nDetails", GREEN),
        ("5", "Accounting\nEntries", GOLD),
        ("6", "Review /\nSubmit", NAVY),
    ]
    xs = [80, 210, 340, 470, 600, 730]
    for x, (num, label, color) in zip(xs, steps):
        d.circle(x, 100, 20, color, NAVY)
        d.text(x, 106, num, 10, WHITE, "700", "middle")
        d.rect(x - 55, 145, 110, 60, WHITE, color, 1.2, 2)
        for i, part in enumerate(label.split("\n")):
            d.text(x, 168 + i * 13, part, 7.4, color, "700", "middle")
    for a, b in zip(xs, xs[1:]):
        d.line(a + 20, 100, b - 21, 100, NAVY, arrow=True)
    d.text(410, 238, "The repayment schedule is prepared before accounting entries and final submission.", 7.2, NAVY, "700", "middle")
    d.save()


def ch4_services():
    d = Diagram("ch4_services_layer", 760, 340, "Frontend Services Layer")
    d.box(65, 145, 125, 66, "Components", ["forms", "tables/wizards"], TEAL, TEAL)
    d.box(240, 145, 125, 66, "Hooks", ["useProgramForm", "useInvoiceForm"], NAVY2, NAVY)
    d.box(415, 145, 130, 66, "Feature Services", ["typed functions", "endpoint mapping"], TEAL, TEAL)
    d.box(610, 70, 115, 58, "Axios Client", ["Bearer token"], GREEN, GREEN)
    d.box(610, 230, 115, 58, "Types", ["DTO models"], GOLD, GOLD)
    d.line(190, 178, 239, 178, NAVY, arrow=True)
    d.line(365, 178, 414, 178, NAVY, arrow=True)
    d.line(545, 165, 609, 99, GREEN, arrow=True)
    d.line(545, 191, 609, 259, GOLD, arrow=True)
    d.save()


def disbursement_use_case():
    d = Diagram("ch5_disbursement_use_case", 860, 520, "UML Use Case Diagram - Disbursement Module")
    d.rect(210, 50, 600, 420, WHITE, NAVY, 1.2, 2)
    d.text(510, 74, "Disbursement Module Boundary", 8, NAVY, "700", "middle")
    d.actor(85, 220, "Buyer or\nSupplier", TEAL)
    cases = [
        (365, 130, "Request\nfinance", GOLD),
        (365, 230, "Choose mode\nINDIVIDUAL/CLUBBED", TEAL),
        (365, 350, "Automatic\ndisbursement", GOLD),
        (610, 180, "Run eligibility\nchecks", TEAL),
        (610, 295, "Submit payment\ninstruction", NAVY),
        (610, 405, "Process async\ncallback", GREEN),
    ]
    for cx, cy, label, color in cases:
        d.usecase(cx, cy, 160, 50, label, color)
    d.line(112, 260, 285, 130, GRAY)
    d.line(112, 260, 285, 230, GRAY)
    d.line(365, 155, 365, 204, TEAL, dash="5 3", arrow=True)
    d.text(405, 184, "<<include>>", 6.4, TEAL, anchor="middle")
    d.line(445, 230, 530, 180, TEAL, dash="5 3", arrow=True)
    d.text(490, 197, "<<include>>", 6.4, TEAL, anchor="middle")
    d.line(445, 350, 530, 180, TEAL, dash="5 3", arrow=True)
    d.text(488, 278, "<<include>>", 6.4, TEAL, anchor="middle")
    d.line(610, 205, 610, 269, NAVY, dash="5 3", arrow=True)
    d.text(648, 243, "<<include>>", 6.4, NAVY, anchor="middle")
    d.line(610, 320, 610, 379, GREEN, dash="5 3", arrow=True)
    d.text(650, 357, "<<include>>", 6.4, GREEN, anchor="middle")
    d.text(510, 452, "Only the primary front-office actor is shown; payment and scheduling are internal collaborators.", 6.8, NAVY, "700", "middle")
    d.save()


def disbursement_class():
    d = Diagram("ch5_disbursement_class_diagram", 940, 570, "UML Class Diagram - Disbursement Domain")
    d.uml_class(40, 60, 165, "Program", ["+type: ProgramType", "+financePercent: Decimal", "+maxDisbursement: int", "+maxTenorDays: int", "+autoDisbursement: bool"], [], CREAM, NAVY)
    d.uml_class(285, 60, 165, "Invoice", ["+status: InvoiceStatus", "+amountState: AmountState", "+amount: Decimal", "+issueDate: Date", "+dueDate: Date", "+tenorDays: int"], [], CREAM, TEAL)
    d.uml_class(560, 60, 175, "Disbursement", ["+mode: INDIVIDUAL|CLUBBED", "+source: MANUAL|AUTO", "+state: DisbState", "+amount: Decimal", "+paymentRef: String", "+failureReason: String"], [], CREAM, GOLD)
    d.uml_class(285, 350, 165, "FinanceRecord", ["+status: FinanceStatus", "+scope: INDIVIDUAL|CLUBBED", "+principalAmount: Decimal", "+maturityDate: Date", "+totalDue: Decimal"], [], CREAM, GREEN)
    d.uml_class(560, 350, 175, "FinanceRecordInvoice", ["+allocatedAmount: Decimal", "+settledAmount: Decimal", "+allocationState: String"], [], CREAM, GOLD)
    d.uml_class(765, 350, 135, "Transaction", ["+type: TransactionType", "+amount: Decimal", "+reference: String", "+createdAt: Instant"], [], CREAM, NAVY)
    d.line(205, 120, 284, 120, NAVY)
    d.text(214, 113, "1", 7, NAVY)
    d.text(258, 113, "1..*", 7, NAVY)
    d.line(450, 120, 559, 120, TEAL)
    d.text(462, 113, "1..*", 7, NAVY)
    d.text(535, 113, "1", 7, NAVY)
    d.path([(125, 160), (125, 255), (648, 255), (648, 170)], GOLD)
    d.text(136, 190, "1", 7, NAVY)
    d.text(600, 247, "0..*", 7, NAVY)
    d.path([(648, 170), (648, 295), (368, 295), (368, 349)], GREEN)
    d.text(505, 286, "creates if SUCCESS", 6.5, GREEN, anchor="middle")
    d.text(378, 340, "0..1", 7, NAVY)
    d.line(450, 415, 559, 415, GOLD)
    d.text(462, 408, "1", 7, NAVY)
    d.text(530, 408, "1..*", 7, NAVY)
    d.path([(648, 170), (648, 349)], GOLD)
    d.text(656, 255, "1 to 0..1", 7, NAVY)
    d.path([(368, 170), (368, 235), (648, 235), (648, 349)], TEAL, dash="5 3")
    d.text(505, 226, "covered invoices", 6.5, TEAL, anchor="middle")
    d.path([(450, 430), (515, 430), (515, 520), (835, 520), (835, 438)], NAVY, dash="5 3")
    d.path([(735, 150), (750, 150), (750, 300), (835, 300), (835, 349)], NAVY, dash="5 3")
    d.path([(450, 150), (520, 150), (520, 300), (835, 300)], NAVY, dash="5 3")
    d.text(715, 535, "generated ledger entries", 6.5, NAVY, anchor="middle")
    d.rect(40, 455, 390, 62, WARM, GOLD, 1.0, 2)
    d.text(58, 476, "Constraint", 7.4, GOLD, "700")
    d.text(58, 495, "No separate finance-request class; Disbursement carries mode and source.", 7.0, NAVY)
    d.save()


def disbursement_state_machine():
    d = Diagram("ch5_disbursement_state_machine", 840, 400, "UML State Machine - Disbursement Lifecycle")
    d.circle(70, 185, 8, NAVY)
    d.state(140, 171, 115, "INITIATED", TEAL)
    d.state(340, 171, 205, "PENDING_CONFIRMATION", GOLD)
    d.state(660, 95, 105, "SUCCESS", GREEN)
    d.state(660, 245, 105, "FAILED", RED)
    d.circle(795, 109, 8, WHITE, NAVY, 1.4)
    d.circle(795, 109, 4, NAVY)
    d.circle(795, 259, 8, WHITE, NAVY, 1.4)
    d.circle(795, 259, 4, NAVY)
    d.line(78, 185, 139, 185, NAVY, arrow=True)
    d.line(255, 185, 339, 185, NAVY, arrow=True)
    d.text(297, 177, "POST /payments", 6.6, NAVY, anchor="middle")
    d.line(545, 178, 659, 109, GREEN, arrow=True)
    d.text(607, 132, "async callback SUCCESS", 6.5, GREEN, anchor="middle")
    d.line(545, 193, 659, 259, RED, arrow=True)
    d.text(610, 244, "async callback FAILED", 6.5, RED, anchor="middle")
    d.path([(198, 199), (198, 259), (659, 259)], RED, arrow=True)
    d.text(395, 251, "sync 422 rejection", 6.5, RED, anchor="middle")
    d.line(765, 109, 786, 109, GREEN, arrow=True)
    d.line(765, 259, 786, 259, RED, arrow=True)
    d.rect(90, 305, 520, 54, WARM, LINE, 1.0, 2)
    d.text(106, 326, "Success effects", 7.2, GREEN, "700")
    d.text(106, 345, "Create FinanceRecord, create FINANCE_DISBURSEMENT transaction, publish disbursement.success, set invoice FINANCED.", 6.7, NAVY)
    d.save()


def disbursement_sequence():
    d = Diagram("ch5_disbursement_sequence_uml", 1120, 690, "UML Sequence Diagram - Manual Disbursement with Async Payment Callback")
    xs = [60, 190, 330, 470, 610, 760, 900, 1040]
    names = ["Buyer/Supplier", "React Wizard", "Disb. Service", "Program/Invoice", "Payment GW", "adria-gateway", "Kafka", "EventConsumer"]
    for x, name in zip(xs, names):
        d.lifeline(x, 55, 650, name, 112)
    for x, y, h in [(190, 95, 470), (330, 125, 465), (470, 155, 110), (610, 285, 185), (760, 420, 120), (900, 455, 90), (1040, 490, 120)]:
        d.activation(x, y, h)
    messages = [
        (60, 190, 100, "select lodged invoices + mode", NAVY, False),
        (190, 330, 130, "requestFinance(payload)", TEAL, False),
        (330, 470, 160, "load program rules + invoice state", NAVY, False),
        (470, 330, 190, "rules, tenor, remaining amount", GOLD, True),
        (330, 330, 220, "run C1-C4 eligibility checks", TEAL, False),
        (330, 610, 290, "POST /payments", NAVY, False),
        (610, 330, 320, "202 Accepted + paymentRef", GOLD, True),
        (330, 190, 350, "state=PENDING_CONFIRMATION", GOLD, True),
        (610, 760, 425, "POST /callbacks/payment", NAVY, False),
        (760, 760, 455, "validate HMAC signature", GREEN, False),
        (760, 610, 485, "HTTP 200 fast ack", GOLD, True),
        (760, 900, 515, "publish payment.callback", TEAL, False),
        (900, 1040, 545, "consume callback event", TEAL, False),
        (1040, 330, 575, "update disbursement SUCCESS/FAILED", GREEN, False),
        (330, 330, 605, "create FinanceRecord + Transaction; update Invoice", GREEN, False),
    ]
    for x1, x2, y, label, color, dashed in messages:
        end = x2 - 1 if x2 > x1 else x2 + 1
        d.line(x1, y, end, y, color, arrow=True, dash="4 3" if dashed else None)
        d.text((x1 + x2) / 2, y - 6, label, 6.1, color, anchor="middle")
    d.rect(300, 235, 360, 38, WHITE, GOLD, 1.0, 2, dash="5 3")
    d.text(315, 258, "alt: any eligibility check fails -> no Disbursement is submitted to Payment Gateway", 6.6, GOLD)
    d.rect(590, 333, 180, 52, WHITE, RED, 1.0, 2, dash="5 3")
    d.text(604, 354, "alt: sync 422", 6.5, RED, "700")
    d.text(604, 371, "state=FAILED; invoice remains LODGED", 6.2, RED)
    d.save()


def ch6_streams():
    d = Diagram("ch6_contribution_streams", 780, 390, "Internship Contribution Streams")
    d.rect(35, 65, 710, 130, WARM, LINE)
    d.rect(35, 225, 710, 130, CREAM, LINE)
    d.text(70, 92, "Platform Delivery", 9, NAVY, "700")
    d.text(70, 252, "PFE Module Preparation", 9, TEAL, "700")
    for x, title, lines, color in [
        (210, "Jira", ["tickets"], TEAL),
        (380, "Bitbucket", ["PR review"], GOLD),
        (550, "Tester", ["validation"], GREEN),
    ]:
        d.box(x, 105, 120, 54, title, lines, color, color)
    for x, title, lines, color in [
        (210, "PO Sessions", ["business rules"], TEAL),
        (380, "Diagrams", ["flow review"], GOLD),
        (550, "Target Design", ["future merge"], GREEN),
    ]:
        d.box(x, 265, 120, 54, title, lines, color, color)
    d.line(330, 132, 379, 132, NAVY, arrow=True)
    d.line(500, 132, 549, 132, NAVY, arrow=True)
    d.line(330, 292, 379, 292, TEAL, arrow=True)
    d.line(500, 292, 549, 292, TEAL, arrow=True)
    d.path([(610, 159), (610, 208), (270, 208), (270, 264)], GOLD, arrow=True, dash="5 3")
    d.text(440, 202, "delivery context feeds module analysis", 6.7, GOLD, anchor="middle")
    d.save()


def ch6_skills():
    d = Diagram("ch6_skills_map", 780, 360, "Skills Acquired During the Internship")
    d.box(285, 72, 210, 56, "Internship Growth", ["technical, domain, and process learning"], NAVY2, NAVY)
    nodes = [
        (75, "Backend", ["Spring Boot", "JPA/OAuth2"], TEAL),
        (201, "Frontend", ["React", "TypeScript"], TEAL),
        (327, "DevOps", ["Docker", "Git / PR"], GOLD),
        (453, "Banking", ["SCF domain", "program logic"], GREEN),
        (579, "Collaboration", ["Scrum", "PO refinement"], GOLD),
        (705, "Quality", ["review", "testing feedback"], GREEN),
    ]
    bus_y = 176
    d.line(390, 128, 390, bus_y, NAVY, sw=1.2)
    d.line(75, bus_y, 705, bus_y, NAVY, sw=1.2)
    for x, title, lines, color in nodes:
        d.box(x - 56, 220, 112, 76, title, lines, color, color)
        d.line(x, bus_y, x, 219, color, arrow=True)
    d.save()


def ch6_roadmap():
    d = Diagram("ch6_future_roadmap", 780, 340, "Recommendations for Future Development")
    nodes = [
        (85, "Disbursement", ["native module"], TEAL),
        (260, "Async Flows", ["Kafka/RabbitMQ"], GOLD),
        (435, "Mobile", ["counterparty access"], GREEN),
        (610, "Analytics", ["portfolio view"], NAVY),
    ]
    for x, title, lines, color in nodes:
        d.box(x, 125, 125, 72, title, lines, color, color)
    for (x1, _, _, _), (x2, _, _, _) in zip(nodes, nodes[1:]):
        d.line(x1 + 125, 161, x2 - 1, 161, NAVY, arrow=True)
    d.rect(120, 250, 540, 50, WARM, LINE)
    d.text(390, 272, "Common direction", 8, NAVY, "700", "middle")
    d.text(390, 290, "Keep the platform governed, traceable, configurable, and useful for bank operations.", 6.8, GRAY, anchor="middle")
    d.save()


def run_all():
    ch1_scf_ecosystem()
    ch1_workflow()
    ch1_timeline()
    ch2_architecture()
    ch2_gateway()
    ch2_auth()
    ch2_storage()
    ch3_class()
    ch3_maker_checker()
    ch3_program_activity()
    use_case_back_office()
    use_case_middle_office()
    use_case_front_office()
    ch4_navigation()
    ch4_invoice_upload()
    ch4_disbursement_wizard()
    ch4_services()
    disbursement_use_case()
    disbursement_class()
    disbursement_state_machine()
    disbursement_sequence()
    ch6_streams()
    ch6_skills()
    ch6_roadmap()


if __name__ == "__main__":
    run_all()
    print(f"Generated professional diagrams in {BASE}")
