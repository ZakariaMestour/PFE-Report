---
name: diagram-skill
description: Use this skill whenever you need to generate a **technical diagram** as an SVG — including state machines, class diagrams, sequence diagrams, flow charts, architecture diagrams, entity relationship diagrams, or trigger chains. This skill enforces the spatial discipline that prevents the three most common failures in AI-generated SVGs: arrows that miss their targets, text that overflows its box, and elements that collide or misalign. Do NOT use this skill for data charts or graphs (bar, line, pie) — use a charting library for those. This skill is for structural/relational diagrams only.
---
## Core Philosophy
 
**Every coordinate is a deliberate calculation, not a guess.**
 
AI agents fail at SVG diagrams because they place elements by intuition and draw arrows by approximation. This skill eliminates both. You will:
1. Plan a coordinate grid on paper (mentally) before writing any SVG
2. Place every element at an exact `(x, y)` with an exact `width` and `height`
3. Derive every arrow start/end point arithmetically from those box coordinates
4. Verify text fits inside its box before committing
---
 
## Step 1 — Choose Your ViewBox
 
Always start with a `viewBox`. This is your coordinate space. Choose dimensions that give you comfortable working room:
 
```svg
<svg viewBox="0 0 700 400" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto;">
```
 
**Rules:**
- Use `width:100%; height:auto` on the `style` attribute so the diagram scales responsively
- Keep viewBox width between 400–800 for most diagrams
- Keep viewBox height between 250–500 for most diagrams
- Never use `width` and `height` attributes directly on `<svg>` — use the style instead
---
 
## Step 2 — Define Arrow Markers in `<defs>`
 
Always define your arrow markers before drawing anything. Every arrow type you need gets its own named marker.
 
```svg
<defs>
  <!-- Standard solid arrow -->
  <marker id="arrow_navy" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0 L7,3.5 L0,7 Z" fill="#0B1D3A"/>
  </marker>
 
  <!-- Dashed/secondary arrow -->
  <marker id="arrow_gray" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0 L7,3.5 L0,7 Z" fill="#6B7280"/>
  </marker>
 
  <!-- Success/green arrow -->
  <marker id="arrow_green" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0 L7,3.5 L0,7 Z" fill="#166534"/>
  </marker>
 
  <!-- Error/red arrow -->
  <marker id="arrow_red" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0 L7,3.5 L0,7 Z" fill="#B91C1C"/>
  </marker>
</defs>
```
 
**Critical rule on `refX`:** Set `refX` to `markerWidth - 1` (here: 6). This places the arrow tip exactly at the line endpoint. If you use `refX="3.5"`, the arrow body overlaps the target box — a very common bug.
 
---
 
## Step 3 — Build a Coordinate Table Before Drawing
 
Before writing any SVG elements, write out a mental (or commented) table:
 
```
BOX NAME         x    y    w    h    center_x   center_y   right_edge   bottom_edge
Program          10   60   120  100  70         110        130          160
Invoice          200  20   140  110  270        75         340          130
Disbursement     380  70   150  120  455        130        530          190
```
 
- `center_x = x + w/2`
- `center_y = y + h/2`
- `right_edge = x + w`
- `bottom_edge = y + h`
You will use these values directly for arrows. Do not eyeball them.
 
---
 
## Step 4 — Draw Boxes
 
### Simple box with header bar
 
```svg
<!-- Outer box -->
<rect x="10" y="60" width="120" height="100" rx="2" fill="#F7F4EF" stroke="#0B1D3A" stroke-width="1.5"/>
<!-- Header bar (same rx, covers the top corners) -->
<rect x="10" y="60" width="120" height="22" rx="2" fill="#0B1D3A"/>
<!-- Header text — centered horizontally in the box -->
<text x="70" y="75" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9" fill="white" font-weight="600">BoxName</text>
```
 
**Header text y-position rule:** `header_y + 15` (positions text vertically centered in a 22px tall header).
 
**Body text rule:** Start at `y + 36`, increment by 13px per line. Never let text go below `y + height - 5`.
 
```svg
<!-- Body text lines — x is box_x + 8 for left padding -->
<text x="18" y="96" font-family="JetBrains Mono, monospace" font-size="7.5" fill="#6B7280">attribute1</text>
<text x="18" y="109" font-family="JetBrains Mono, monospace" font-size="7.5" fill="#6B7280">attribute2</text>
<text x="18" y="122" font-family="JetBrains Mono, monospace" font-size="7.5" fill="#0B7285" font-weight="600">keyAttribute</text>
```
 
### Text overflow check
Before committing: `last_text_y ≤ box_y + box_height - 5`. If it exceeds, either increase the box height or reduce the font size to 7px.
 
---
 
## Step 5 — Draw Arrows
 
### Straight horizontal arrow (left → right)
 
From `right_edge` of Box A to `left_edge` of Box B, both at the same `center_y`:
 
```svg
<line
  x1="130" y1="110"
  x2="198" y2="110"
  stroke="#0B1D3A" stroke-width="1.5"
  marker-end="url(#arrow_navy)"/>
```
 
**Rule:** `x2` = `target_box_x - 1`. Subtract 1 pixel so the line doesn't visually overlap the target border.
 
### Straight vertical arrow (top → bottom)
 
```svg
<line
  x1="270" y1="130"
  x2="270" y2="168"
  stroke="#0B1D3A" stroke-width="1.5"
  marker-end="url(#arrow_navy)"/>
```
 
`x1 = x2 = source_center_x`. `y1 = source_bottom_edge`. `y2 = target_y - 1`.
 
### Diagonal arrow
 
```svg
<line
  x1="130" y1="85"
  x2="198" y2="110"
  stroke="#166534" stroke-width="1.5"
  marker-end="url(#arrow_green)"/>
```
 
Calculate the exact corner or edge point you're leaving from, and the exact edge point you're arriving at.
 
### L-shaped route (avoiding collisions)
 
When a direct line would cross other elements, use a `<path>` with explicit waypoints:
 
```svg
<path
  d="M 130,145 L 160,145 L 160,210 L 378,210 L 378,150"
  fill="none"
  stroke="#0B1D3A" stroke-width="1.5"
  marker-end="url(#arrow_navy)"/>
```
 
**Rule:** Every waypoint coordinate must be verified to not pass through another box. Check each segment against your coordinate table.
 
### Dashed arrow (secondary relationship)
 
```svg
<line
  x1="270" y1="130"
  x2="270" y2="185"
  stroke="#6B7280" stroke-width="1"
  stroke-dasharray="5 2"
  marker-end="url(#arrow_gray)"/>
```
 
### Arrow with label
 
Place the label at the midpoint of the arrow, offset by a few pixels perpendicular to the line:
 
```svg
<!-- Horizontal arrow with label above it -->
<line x1="130" y1="110" x2="198" y2="110" stroke="#0B1D3A" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
<text x="164" y="106" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="7" fill="#0B1D3A">1..*</text>
```
 
Midpoint x = `(x1 + x2) / 2`. Label y = `arrow_y - 4` (above) or `arrow_y + 10` (below).
 
---
 
## Step 6 — Color System
 
Use this palette consistently. Never use random hex values.
 
```
--navy:   #0B1D3A   Primary boxes, main arrows, headers
--navy2:  #162B52   Header bars for primary entities
--teal:   #0B7285   Author's module, secondary entities, highlighted fields
--teal2:  #0E9CB5   Accents, active states
--gold:   #C9962A   Warning, junction tables, auto-mode elements
--gold2:  #E8B84B   Kafka topics, event labels
--green:  #166534   Success states, REPAID, positive flows
--red:    #B91C1C   Error states, FAILED, NPA
--orange: #C2410C   OVERDUE, warning states
--gray:   #6B7280   Secondary text, muted attributes
--line:   #D4D0C8   Box borders, dividers
--cream:  #F7F4EF   Box fill (light entities)
--warm:   #F0EDE8   Alternate row background
--dark:   #1A1A1A   Kafka/event bus background
```
 
**Font rule:** Always use `font-family="JetBrains Mono, monospace"` for technical content (entity names, attributes, state names, code). Use `font-family="Georgia, serif"` only for narrative labels.
 
---
 
## Step 7 — State Machine Specific Rules
 
States are rounded rectangles (`rx="12"` for pill shape, `rx="2"` for slight rounding).
 
```svg
<!-- Pill-shaped state -->
<rect x="50" y="40" width="140" height="26" rx="13" fill="#0B7285"/>
<text x="120" y="57" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9" fill="white" font-weight="600">STATE_NAME</text>
```
 
**Initial state:** Filled black circle, radius 8.
```svg
<circle cx="120" cy="14" r="8" fill="#0B1D3A"/>
```
 
**Terminal state:** Filled circle in the state's color.
```svg
<circle cx="120" cy="250" r="6" fill="#166534"/>
```
 
**Transition arrow from pill bottom:** `x1 = state_x + state_width/2`, `y1 = state_y + state_height`.
**Transition arrow to pill top:** `x2 = state_x + state_width/2 - 1`, `y2 = state_y`.
 
**Branch arrows from same state:** Offset the departure x-coordinate slightly left and right of center to make branching visually clear:
- Left branch departs at `center_x - 25`
- Right branch departs at `center_x + 25`
---
 
## Step 8 — Sequence Diagram Specific Rules
 
```svg
<!-- Actor box -->
<rect x="2" y="18" width="80" height="15" rx="2" fill="#F0EDE8" stroke="#0B1D3A" stroke-width="1"/>
<text x="42" y="29" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="7" fill="#0B1D3A" font-weight="600">ActorName</text>
 
<!-- Lifeline — starts at actor_bottom, runs to diagram_bottom -->
<line x1="42" y1="33" x2="42" y2="280" stroke="#D4D0C8" stroke-width="0.8" stroke-dasharray="4 3"/>
 
<!-- Synchronous message (solid arrow) -->
<line x1="42" y1="55" x2="118" y2="55" stroke="#0B7285" stroke-width="1.5" marker-end="url(#arrow_navy)"/>
<text x="80" y="51" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="6.5" fill="#0B7285">methodName()</text>
 
<!-- Return message (dashed arrow, reversed direction) -->
<line x1="118" y1="70" x2="46" y2="70" stroke="#C9962A" stroke-width="1" stroke-dasharray="3 2" marker-end="url(#arrow_gold)"/>
<text x="80" y="66" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="6.5" fill="#C9962A">return value</text>
```
 
**Lifeline x-coordinate rule:** All messages on a lifeline use exactly the same `x` value — the actor's `center_x`. Never approximate.
 
**Vertical spacing rule:** Each message pair (call + return) occupies 18–22px of vertical space. Plan your total height before drawing.
 
---
 
## Step 9 — Annotation Boxes
 
For notes, legends, or callout boxes:
 
```svg
<rect x="5" y="200" width="190" height="55" rx="2" fill="rgba(201,150,42,0.07)" stroke="#C9962A" stroke-width="0.8"/>
<text x="100" y="215" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="7.5" fill="#C9962A" font-weight="600">Box Title</text>
<text x="13" y="229" font-family="JetBrains Mono, monospace" font-size="7.5" fill="#0B1D3A">Line one content</text>
<text x="13" y="242" font-family="JetBrains Mono, monospace" font-size="7.5" fill="#0B1D3A">Line two content</text>
```
 
**Height check:** `last_text_y (242) ≤ box_y + box_height - 5 (250)`. ✓
 
---
 
## Step 10 — Final Checklist Before Outputting
 
Run through this list mentally for every diagram:
 
- [ ] Every box: does `last_text_y ≤ box_y + box_height - 5`?
- [ ] Every arrow: does `x1, y1` sit exactly on the source box edge (not inside, not floating)?
- [ ] Every arrow: does `x2, y2` stop 1px before the target box border?
- [ ] Every `marker-end`: does the referenced `id` exist in `<defs>`?
- [ ] Every L-shaped path: does each waypoint avoid crossing another box?
- [ ] All lifelines in sequence diagrams: same `x` value used consistently?
- [ ] Branch arrows departing from the same state: offset by ±20–30px from center?
- [ ] No text element uses `x` less than `box_x + 6` (left padding)?
- [ ] viewBox height is sufficient for all content (nothing drawn below viewBox bottom)?
---
 
## Common Bugs Reference
 
| Bug | Cause | Fix |
|-----|-------|-----|
| Arrow floats before target box | `refX` too small in marker | Set `refX = markerWidth - 1` |
| Arrow overshoots into target box | `x2/y2` not offset by -1 | Subtract 1px from endpoint |
| Text overflows box bottom | Too many lines, box too short | Increase box `height` or reduce `font-size` to 7px |
| Arrow departs from wrong edge | Using center instead of edge point | Use `right_edge = x + width` for right departure |
| L-route crosses a box | Waypoints not checked against coordinate table | Re-route; add an extra waypoint to go around |
| Diagonal arrow misses target | Endpoint approximated | Recalculate target edge point from exact coordinates |
| Dashed arrow has solid arrowhead | Missing `stroke-dasharray` on marker path | `stroke-dasharray` applies to the `<line>`, not the marker |
 
---
 
## Minimal Working Example
 
A two-entity diagram with one relationship arrow:
 
```svg
<svg viewBox="0 0 400 150" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto;">
  <defs>
    <marker id="arr" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
      <path d="M0,0 L7,3.5 L0,7 Z" fill="#0B1D3A"/>
    </marker>
  </defs>
 
  <!-- Box A: x=10, y=40, w=120, h=70, center_x=70, center_y=75, right_edge=130 -->
  <rect x="10" y="40" width="120" height="70" rx="2" fill="#F7F4EF" stroke="#0B1D3A" stroke-width="1.5"/>
  <rect x="10" y="40" width="120" height="22" rx="2" fill="#0B1D3A"/>
  <text x="70" y="55" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9" fill="white" font-weight="600">EntityA</text>
  <text x="18" y="78" font-family="JetBrains Mono, monospace" font-size="7.5" fill="#6B7280">attribute1</text>
  <text x="18" y="91" font-family="JetBrains Mono, monospace" font-size="7.5" fill="#6B7280">attribute2</text>
  <!-- last text y=91, box bottom=110-5=105 ✓ -->
 
  <!-- Arrow from right edge of A (130, 75) to left edge of B (270-1=269, 75) -->
  <line x1="130" y1="75" x2="269" y2="75" stroke="#0B1D3A" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Cardinality label at midpoint x=(130+269)/2=199, above arrow -->
  <text x="199" y="71" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="7.5" fill="#0B1D3A">1..*</text>
 
  <!-- Box B: x=270, y=40, w=120, h=70, center_x=330, center_y=75 -->
  <rect x="270" y="40" width="120" height="70" rx="2" fill="#F7F4EF" stroke="#0B7285" stroke-width="1.5"/>
  <rect x="270" y="40" width="120" height="22" rx="2" fill="#0B7285"/>
  <text x="330" y="55" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9" fill="white" font-weight="600">EntityB</text>
  <text x="278" y="78" font-family="JetBrains Mono, monospace" font-size="7.5" fill="#6B7280">attribute1</text>
  <text x="278" y="91" font-family="JetBrains Mono, monospace" font-size="7.5" fill="#6B7280">attribute2</text>
</svg>
```