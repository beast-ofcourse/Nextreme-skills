---
name: high-quality-flowcharts
description: "Design and produce polished, publication-grade flowcharts, roadmaps, process diagrams, decision trees, and taxonomy maps using HTML/CSS shells with inline SVG geometry and PDF export. Trigger this skill whenever the user asks for a \"flowchart\", \"roadmap\", \"process diagram\", \"decision tree\", \"org chart\", \"curriculum guide\", \"skill tree\", \"workflow\", \"yes/no flow\", \"classification map\", or any kind of visual diagram that belongs in a clean printable PDF — even if they don't explicitly say \"PDF\" or \"flowchart\". Also trigger when they want to visualize steps, logic, hierarchies, branching decisions, or learning paths. Do NOT trigger for simple code flow comments, quick sketches, or things better done as Mermaid diagrams in a markdown file — this skill is specifically for producing a standalone, print-ready PDF artifact."
license: MIT
---

# High-Quality Flowcharts — Build Print-Ready PDF Diagrams

This skill produces **publication-grade PDF diagrams** from user descriptions. Every output is a standalone, printable PDF with crisp vector geometry, clean typography, and intentional layout. The user gets three deliverables: the **PDF**, the **HTML+SVG source**, and a **verification preview**.

---

## CRITICAL: You Must Match the Template Style

The skill ships with example PDF templates in `templates/`. Your output MUST look like them — same design language, same visual quality. Before writing any code:

1. **Open every template PDF** in `templates/` (full-stack.pdf, ux-design.pdf, computer-science.pdf, cpp.pdf, c.pdf). Study each one.
2. **Extract their design language**: note the exact colors, font sizes, node shapes, border radii, connector styles, spacing rhythm, header treatment, and how branches attach to the spine.
3. **List what you see** — write down the specific visual properties you observe. If the templates use thin 1px borders with subtle drop shadows, so must you. If they use rounded rects with `rx="8"` and bold 14px labels, match that exactly.
4. **Only then** start coding. Your output must pass a visual consistency check against the templates.

Do NOT invent a new visual style. Replicate the template look. The templates are the ground truth for what "polished" means.

---

## Why This Approach Matters

Raw auto-generated diagrams usually look bad — inconsistent spacing, clipped text, wrong paper size, no visual hierarchy. This skill works differently:

- **HTML/CSS** handles the document frame (pages, margins, typography, print rules)
- **Inline SVG** renders the diagram itself (nodes, connectors, labels) — text is searchable, lines are crisp at any zoom
- **PDF export** via a headless browser or library preserves everything faithfully

The user is asking for something they can print, present, or share. Treat this as a design artifact, not a code exercise.

---

## Core Workflow

Do these steps in order. Each has a specific purpose — don't skip or reorder.

### 1. Study the Templates (Mandatory)

Read every PDF in `templates/`. These are your style reference. Note:
- **Color palette**: exact hex codes used for node fills, borders, text, connectors, headers
- **Typography**: font family, title size, section header size, body/node text size
- **Node styling**: border radius `rx` values, stroke widths, fill colors, shadow effects
- **Connector styling**: stroke width, color, dash patterns, arrowhead shape
- **Layout rhythm**: spacing between nodes, margins from page edge, spine width
- **Header area**: title placement, subtitle style, any logo or decorative element

After studying them, write down the design tokens you extracted. This is your style guide for the diagram.

### 2. Understand the Content Structure

Before writing any code, figure out what kind of diagram you're building and what the hierarchy looks like.

- **What's the top-level concept?** (the central topic or starting point)
- **What are the major sections or steps?** (the spine or main flow)
- **What are the sub-items or branches?** (details branching off each major section)
- **Are there decisions or conditional paths?** (yes/no branches, alternate routes)

Write this out as a structured outline before touching HTML. This prevents mid-construction rewrites.

### 3. Choose the Right Layout Pattern

Match the content to the best visual structure. Picking the wrong layout produces a confusing diagram.

| Pattern | When to Use | Visual Structure |
|---|---|---|
| **Roadmap** (Vertical Spine) | Learning paths, skill trees, curriculum guides, timelines | Central vertical spine, subtopics branch left/right |
| **Process Flow** (Horizontal) | Business workflows, algorithms, step-by-step guides, pipelines | Left-to-right linear chain with solid arrows |
| **Decision Tree** (Top-Down) | Troubleshooting guides, logic branching, yes/no diagnostics | Diamond decision nodes at top, rectangular actions below, labeled branches |
| **Taxonomy Map** (Clusters) | Topic classifications, org charts, category hierarchies, mind maps | Central hub with grouped clusters radiating outward |

**Example**: If the user says "show me a learning path for Python", that's a **Roadmap**. If they say "walk me through deploying a web app", that's a **Process Flow**. Get this right before you write any SVG.

### 4. Build the HTML/CSS Shell (The Document Frame)

This creates the printable page. The `@page` CSS rule is critical — without it the PDF export won't respect paper size.

Apply the design tokens you extracted from the templates. Use the template's exact colors, font sizes, and spacing. The HTML shell below is a starting point — customize it to match the template style.

```html
<!DOCTYPE html>
<html>
<head>
<style>
  @page { size: A4 landscape; margin: 0.4in; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { /* Use font family from templates */ }
  .page { /* Use padding/spacing from templates */ }
  .title { /* Use font size, weight, color from templates */ }
  .subtitle { /* Use font size, color from templates */ }
  svg.diagram { width: 100%; height: auto; display: block; }
  /* Add the template's exact node, connector, and header styles */
</style>
</head>
<body>
<div class="page">
  <div class="title">Diagram Title</div>
  <div class="subtitle">Optional subtitle or description</div>
  <svg class="diagram" viewBox="0 0 WIDTH HEIGHT" xmlns="http://www.w3.org/2000/svg">
    <!-- Diagram elements go here -->
  </svg>
</div>
</body>
</html>
```

**Key decisions to make:**
- **Paper size**: A4 (default, most common for printing) or Letter. Prefer landscape for wide diagrams.
- **Margins**: 0.4in minimum on all sides. Less than that risks content being clipped by printers.
- **SVG viewBox**: Set this to the logical coordinate space of your diagram. Use a coordinate system where X grows right and Y grows down.

### 5. Render the Diagram as Inline SVG

This is the core of the output. Every element in the diagram is a named SVG `<g>` group with clear coordinates.

**Coordinate system conventions:**
- Work in a unified coordinate space (e.g., `viewBox="0 0 1200 800"` for a full-page diagram)
- Place elements at explicit (x, y) positions — don't rely on auto-layout
- Use a 20px or 40px grid alignment to keep things visually consistent

**Node types (match template styling exactly):**
- **Section headers (spine nodes)**: `<rect>` with rounded corners (`rx="8"`), bold centered text, colored fill as seen in templates
- **Subtopic nodes**: Smaller `<rect>` with lighter fill, regular weight text, matching template border radius
- **Decision diamonds**: `<polygon>` with four points, question text centered inside, using template color scheme
- **End nodes / terminals**: `<rect>` with `rx="20"` (pill shape) using template's terminal styling

**Connectors:**
- **Spine lines**: Solid or dashed vertical/horizontal `<line>` using template's stroke color and width
- **Branch connectors**: Curved `<path>` using cubic bezier (`C` commands) for smooth curves
- **Process arrows**: `<path>` with marker-end arrowhead, or a separate `<polygon>` for the arrowhead
- **Decision branches**: Straight lines from diamond corners with "Yes"/"No" labels

**Typography within SVG (match template sizes exactly):**
- Section names inside SVG: as seen in templates (typically `font-size="14"` to `font-size="16"`, bold)
- Subtopic labels inside SVG: as seen in templates (typically `font-size="12"` to `font-size="13"`)
- Connector labels: as seen in templates (typically `font-size="10"` to `font-size="11"`)
- Use the template's font family throughout. Keep to sans-serif that renders reliably.

### 6. Generate the PDF

Use the bundled script — it tries multiple backends automatically:

```bash
python scripts/generate_pdf.py output.html output.pdf [--landscape] [--paper-size A4]
```

The script tries Playwright first (best quality), then WeasyPrint, then pdfkit.

### 7. Verify the Output

Run the verification script to produce a preview image:

```bash
python scripts/verify_pdf.py output.pdf
```

Open the preview and visually check for:
- **Does it match the template style?** Compare side by side
- **Clipped text** — text that overflows its box or reaches the page edge
- **Overlapping elements** — nodes sitting on top of each other
- **Broken connectors** — lines that don't connect properly or miss their target
- **Missing labels** — empty connectors, blank nodes
- **Wrong paper orientation** — content doesn't fit or looks squished

If you see problems, go back to step 4/5 and fix.

### 8. Deliver Everything

When the user's request is complete, always deliver these three files:

1. **The PDF** — polished, ready to print or share
2. **The HTML source** — so they can edit it later
3. **The verification image** — proves it rendered correctly

---

## Common Patterns & Sizing Reference

These are defaults. Adjust to match template dimensions if they differ.

### Node Sizing
| Element | Width (px) | Height (px) | Notes |
|---|---|---|---|
| Spine/section header | 220 | 44 | Center column, larger |
| Subtopic branch | 180 | 34 | Side columns |
| Decision diamond | 180 | 180 | Points at top/bottom/left/right |
| Terminal/end node | 180 | 40 | Rounded pill shape |

### Spacing
- Between spine nodes: 80–100px vertically
- Between branches and spine: 120–150px horizontally
- Between sibling subtopics: 30–40px vertically
- Page margins: 0.4in minimum

### Layout Dimensions (A4 Landscape, 1200x800 coordinate space)
- Center spine runs at X=600
- Left branches: X=150 to X=400
- Right branches: X=800 to X=1050
- Y starts at ~120 (below title) and ends at ~750 (before bottom margin)

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| PDF has no content (blank) | The viewBox or SVG dimensions are wrong | Set explicit viewBox="0 0 W H" and ensure elements are within bounds |
| Text is clipped | Node too small for text, or margins too tight | Increase node width by 20-40px first, then font size |
| Connectors don't reach their target | Source/target coordinates don't match actual element positions | Use element centers, not edges, for connector endpoints |
| PDF generation hangs or fails | Missing backend tool | Install playwright: `npx playwright install chromium` |
| Colors look wrong in PDF | CSS custom properties not resolving in SVG | Use inline `fill="#xxxxxx"` directly in SVG instead of CSS var() |
| Landscape doesn't work | @page orientation missing | Add `size: A4 landscape` to @page rule |
| Diagram feels cramped | Too much content for one page | Increase paper size, use larger viewBox, or split into multiple pages |
| Output doesn't match template style | You didn't study the templates first | Go back to step 1 and extract exact design tokens from templates/ |

---

## Reference Files

- `templates/` — **STUDY THESE FIRST.** They define the visual style your output must match.
- `references/layout-patterns.md` — Visual structure details for each pattern
- `references/visual-style.md` — Color palette and typography tokens (verify against templates)
- `scripts/generate_pdf.py` — HTML→PDF conversion (tries multiple backends)
- `scripts/verify_pdf.py` — Creates preview image for manual verification
