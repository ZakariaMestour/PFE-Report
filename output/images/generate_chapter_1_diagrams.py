from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

BASE = Path(__file__).resolve().parent


def font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


TITLE = font(34, True)
SUBTITLE = font(20)
NODE = font(19, True)
SMALL = font(16)
TINY = font(14)


def rounded(draw, box, fill, outline, radius=18, width=3):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def centered_text(draw, box, text, fnt, fill="#183044", spacing=5):
    x1, y1, x2, y2 = box
    max_width = x2 - x1 - 28
    words_per_line = max(8, max_width // 11)
    lines = []
    for part in text.split("\n"):
        lines.extend(textwrap.wrap(part, width=words_per_line) or [""])
    line_height = int(getattr(fnt, "size", 16) * 1.35)
    heights = [line_height for _ in lines]
    total = sum(heights) + spacing * (len(lines) - 1)
    y = y1 + ((y2 - y1) - total) / 2
    for line, h in zip(lines, heights):
        bbox = draw.textbbox((0, 0), line, font=fnt)
        w = bbox[2] - bbox[0]
        draw.text((x1 + ((x2 - x1) - w) / 2, y - bbox[1]), line, font=fnt, fill=fill)
        y += h + spacing


def arrow(draw, start, end, color="#4b6478", width=4):
    draw.line([start, end], fill=color, width=width)
    sx, sy = start
    ex, ey = end
    if abs(ex - sx) >= abs(ey - sy):
        sign = 1 if ex >= sx else -1
        pts = [(ex, ey), (ex - sign * 16, ey - 9), (ex - sign * 16, ey + 9)]
    else:
        sign = 1 if ey >= sy else -1
        pts = [(ex, ey), (ex - 9, ey - sign * 16), (ex + 9, ey - sign * 16)]
    draw.polygon(pts, fill=color)


def save_html(name, title, body):
    html = f"""<!doctype html>
<html>
<head><meta charset=\"utf-8\"><title>{title}</title></head>
<body>
<div class=\"html-diagram-engine-{name}\" style=\"padding:24px;background:white;display:inline-block;\">
  <style>
    .html-diagram-engine-{name} .diagram-grid {{
      display:grid;
      grid-template-columns:repeat(5, 180px);
      gap:18px;
      align-items:center;
      justify-items:center;
      font-family:system-ui,-apple-system,Segoe UI,sans-serif;
    }}
    .html-diagram-engine-{name} .node {{
      box-sizing:border-box;
      overflow:hidden;
      word-wrap:break-word;
      background:#ffffff;
      border:2px solid #b7c6d6;
      color:#183044;
      padding:14px 16px;
      border-radius:8px;
      text-align:center;
      font-weight:650;
      width:180px;
      min-height:76px;
      box-shadow:0 6px 14px rgba(24,48,68,.08);
    }}
    .html-diagram-engine-{name} .accent {{ background:#edf7f1;border-color:#73a884; }}
    .html-diagram-engine-{name} .bank {{ background:#eef3fb;border-color:#6f93c6; }}
    .html-diagram-engine-{name} svg {{ width:100%; height:60px; }}
  </style>
  <div class=\"diagram-grid\">
{body}
  </div>
</div>
</body>
</html>
"""
    (BASE / f"{name}.html").write_text(html, encoding="utf-8")


def ecosystem():
    img = Image.new("RGB", (1500, 760), "#ffffff")
    d = ImageDraw.Draw(img)
    d.text((60, 44), "Supply Chain Finance Ecosystem", font=TITLE, fill="#172b3a")
    d.text((62, 88), "Commercial exchange, financing decision, and controlled payment movement", font=SUBTITLE, fill="#557086")

    bank = (590, 150, 910, 270)
    anchor = (170, 360, 490, 480)
    counterparty = (1010, 360, 1330, 480)
    program = (590, 360, 910, 500)
    invoice = (590, 585, 910, 690)

    for box, text, fill, outline in [
        (bank, "Bank\nProgram governance\nFinancing control", "#eef3fb", "#6f93c6"),
        (anchor, "Anchor\nLarge buyer or seller\nCommercial reference", "#f7fbef", "#95a96a"),
        (counterparty, "Counterparty\nSupplier, distributor,\nSME or buyer", "#fff5ec", "#c89158"),
        (program, "SCF Program\nProducts, limits, fees,\ndisbursement rules", "#eef8f2", "#73a884"),
        (invoice, "Underlying Instruments\nInvoices, purchase orders,\ntrade documents", "#f5f0fb", "#9a79bf"),
    ]:
        rounded(d, box, fill, outline)
        centered_text(d, box, text, NODE)

    arrow(d, (490, 405), (590, 405))
    d.text((498, 372), "Program setup", font=TINY, fill="#4b6478")
    arrow(d, (910, 405), (1010, 405))
    d.text((918, 372), "Eligibility rules", font=TINY, fill="#4b6478")
    arrow(d, (750, 270), (750, 360))
    d.text((768, 304), "Validation", font=TINY, fill="#4b6478")
    arrow(d, (750, 585), (750, 500))
    d.text((812, 515), "Cashflow input", font=TINY, fill="#4b6478")
    d.line([(1010, 480), (1010, 540), (490, 540), (490, 480)], fill="#6d7f8b", width=4)
    d.polygon([(490, 480), (481, 496), (499, 496)], fill="#6d7f8b")
    d.text((556, 552), "Goods / services and invoice exchange", font=TINY, fill="#53636f")
    arrow(d, (910, 215), (1010, 360), "#6f93c6")
    d.text((940, 270), "Financing", font=TINY, fill="#53636f")
    arrow(d, (590, 215), (490, 360), "#6f93c6")
    d.text((476, 270), "Payment flow", font=TINY, fill="#53636f")

    img.save(BASE / "ch1_scf_ecosystem.png")
    save_html("ch1_scf_ecosystem", "Supply Chain Finance Ecosystem", """
    <div class=\"node accent\">Anchor<br>Commercial reference</div>
    <svg><line x1=\"5\" y1=\"30\" x2=\"175\" y2=\"30\" stroke=\"#4b6478\" stroke-width=\"4\" marker-end=\"url(#arrow)\"/></svg>
    <div class=\"node bank\">SCF Program<br>Rules and fees</div>
    <svg><line x1=\"5\" y1=\"30\" x2=\"175\" y2=\"30\" stroke=\"#4b6478\" stroke-width=\"4\"/></svg>
    <div class=\"node accent\">Counterparty<br>Supplier or distributor</div>
    """)


def workflow():
    img = Image.new("RGB", (1500, 620), "#ffffff")
    d = ImageDraw.Draw(img)
    d.text((60, 44), "Daily Development and Validation Workflow", font=TITLE, fill="#172b3a")
    d.text((62, 88), "From sprint task assignment to tester verification", font=SUBTITLE, fill="#557086")
    boxes = [
        ((70, 220, 285, 340), "Jira Ticket\nAssigned in sprint"),
        ((330, 210, 545, 355), "Development\nBackend and frontend\nimplementation"),
        ((590, 220, 805, 340), "Bitbucket Push\nBranch publication"),
        ((850, 220, 1065, 340), "Pull Request\nTech Lead review"),
        ((1110, 220, 1325, 340), "Tester Validation\nVerification after merge"),
    ]
    for i, (box, text) in enumerate(boxes):
        rounded(d, box, "#eef3fb" if i in (0, 4) else "#eef8f2", "#6f93c6" if i in (0, 4) else "#73a884")
        centered_text(d, box, text, NODE)
        if i < len(boxes) - 1:
            arrow(d, (box[2], 280), (boxes[i + 1][0][0], 280))

    d.rounded_rectangle((850, 390, 1065, 480), radius=14, fill="#fff5ec", outline="#c89158", width=3)
    centered_text(d, (850, 390, 1065, 480), "Modification\nrequested", SMALL)
    arrow(d, (955, 390), (955, 340), "#c89158")
    arrow(d, (850, 435), (545, 340), "#c89158")
    d.text((630, 410), "Review comments return to development", font=TINY, fill="#6e5b46")
    img.save(BASE / "ch1_internship_workflow.png")
    save_html("ch1_internship_workflow", "Internship Workflow", """
    <div class=\"node\">Jira Ticket</div>
    <svg></svg>
    <div class=\"node accent\">Development</div>
    <svg></svg>
    <div class=\"node\">Bitbucket PR</div>
    """)


def timeline():
    img = Image.new("RGB", (1500, 620), "#ffffff")
    d = ImageDraw.Draw(img)
    d.text((60, 44), "Internship Timeline", font=TITLE, fill="#172b3a")
    d.text((62, 88), "Five-month PFE period with parallel Disbursement Module refinement", font=SUBTITLE, fill="#557086")
    y = 300
    d.line((120, y, 1380, y), fill="#4b6478", width=5)
    stages = [
        (170, "February 2026\nRemote training\nBusiness and stack"),
        (420, "After week 2\nOn-site integration\nTeam delivery"),
        (690, "Sprint 2 to Sprint 8\nJira tasks, PRs,\ntesting loop"),
        (980, "Weekly Mondays\nPO refinement\nFunctional diagrams"),
        (1240, "July 1st, 2026\nInternship closure\nReport synthesis"),
    ]
    for i, (x, text) in enumerate(stages):
        d.ellipse((x - 16, y - 16, x + 16, y + 16), fill="#73a884", outline="#315c43", width=3)
        box = (x - 110, y + 48 if i % 2 == 0 else y - 150, x + 110, y + 150 if i % 2 == 0 else y - 48)
        rounded(d, box, "#eef8f2" if i != 4 else "#eef3fb", "#73a884" if i != 4 else "#6f93c6", radius=14)
        centered_text(d, box, text, SMALL)
        d.line((x, y + 16 if i % 2 == 0 else y - 16, x, box[1] if i % 2 == 0 else box[3]), fill="#8aa0b3", width=2)
    img.save(BASE / "ch1_internship_timeline.png")
    save_html("ch1_internship_timeline", "Internship Timeline", """
    <div class=\"node\">Remote Training</div>
    <svg></svg>
    <div class=\"node accent\">On-site Work</div>
    <svg></svg>
    <div class=\"node bank\">Sprint 2 to Sprint 8</div>
    """)


if __name__ == "__main__":
    ecosystem()
    workflow()
    timeline()
    print("Generated Chapter I diagrams in", BASE)
