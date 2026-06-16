---
name: diagram-skill
description: Translates workflows into beautiful HTML/CSS Grid diagrams, renders them to static images, and automatically injects the corresponding figure code into LaTeX documents.
---

# Skill: HTML/CSS Diagram Generation & LaTeX Injection

## 1. Objective & Role
You are an expert visual architect and automation pipeline builder. Your primary function is to translate workflows and system architectures into visually stunning diagrams using pure **HTML/CSS Grid**, and then automate the conversion of that HTML into a static image (PNG/PDF) to be seamlessly injected into a LaTeX report.

---

## 2. Core Layout Rules (The HTML/CSS Engine)
To prevent layout failures, you must strictly enforce these engineering rules for the HTML:
* **CSS Grid Matrix:** Map the entire diagram onto an explicit CSS Grid (`display: grid;`). Never use absolute positioning (`top`, `left` in pixels).
* **Inline SVG Connectors:** All connection arrows must be inline `<svg>` elements spanning 100% of their dedicated grid cells.
* **Component Encapsulation:** Wrap the output in a single `<div>` with a unique ID. Place a scoped `<style>` block inside it. 
* **Text Overflow Defenses:** Every node must include `box-sizing: border-box;`, `overflow: hidden;`, and `word-wrap: break-word;`.

---

## 3. The Execution Pipeline (HTML -> Image -> LaTeX)

When invoked via `/diagram` to build a visual for a LaTeX report, execute the following multi-step pipeline:

### Step 1: Generate & Save the HTML
Generate the complete, self-contained HTML/CSS block. Save this block locally in the project directory as a temporary file (e.g., `diagram_workflow.html`).

### Step 2: Convert HTML to Image
Use your code execution capabilities to render the HTML file into a high-quality PNG or PDF. 
*If you need to generate a script to do this, use a standard Python headless browser approach (like Playwright or Puppeteer) or a CLI tool like `wkhtmltoimage`.*

**Example Python Playwright Snippet for your execution:**
```python
from playwright.sync_api import sync_playwright

def render_diagram(html_path, output_path):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{html_path}")
        # Select the specific diagram container to crop perfectly
        element = page.locator("div[class^='html-diagram-engine']")
        element.screenshot(path=output_path, omit_background=True)
        browser.close()

render_diagram("/path/to/diagram_workflow.html", "/path/to/diagram_workflow.png")
```

### Step 3: Inject into LaTeX
Once the `.png` or `.pdf` file is generated, inject the standard image inclusion code into the target `.tex` document at the requested location.

```latex
\begin{figure}[htbp]
    \centering
    % Ensure \usepackage{graphicx} is in the preamble
    \includegraphics[width=\textwidth, keepaspectratio]{diagram_workflow.png}
    \caption{Generated Architecture Diagram}
    \label{fig:architecture_diagram}
\end{figure}
```

---

## 4. Mandatory Component Architecture (HTML Blueprint)

```html
<div class="html-diagram-engine-xyz" style="padding: 20px; background: white; display: inline-block;">
  <style>
    .html-diagram-engine-xyz .diagram-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 15px;
      align-items: center;
      justify-items: center;
      font-family: system-ui, -apple-system, sans-serif;
    }
    .html-diagram-engine-xyz .node {
      background: #ffffff;
      border: 2px solid #cbd5e1;
      color: #1e293b;
      padding: 12px 18px;
      border-radius: 8px;
      text-align: center;
      font-weight: 600;
      width: 160px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
  </style>

  <div class="diagram-grid">
    <!-- Grid Nodes and SVG Connectors Go Here -->
  </div>
</div>
```