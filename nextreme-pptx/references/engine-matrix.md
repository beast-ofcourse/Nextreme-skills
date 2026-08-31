# Engine Matrix — 3 Engines, You Decide Per Slide

No single engine is honest for every deck. You pick per slide, per audience — not per user request.

## 1. Decision Flow — Content Drives Engine

```
Slide needs to exist
├─ User handed you a branded .pptx with masters?
│  └─ YES → Engine B (slide-master layouts) — fill placeholders, preserve schemeClr
├─ Is the story data-heavy report or KPI board with native charts?
│  └─ YES → Engine C (native dict) — native chart, native table, Python dict source
├─ Is this a sparse pitch / editorial / Bento narrative where typography is the value?
│  └─ YES → Engine A (HTML→SVG→PPTX agency vector) — Bento Grid via SVG → shapes
└─ Default → Engine C (native dict) — editable, testable, diffable
```

You must justify the pick in one line per slide (“bar_chart → native chart for editable data; matrix_2x2 → vector shapes for precise placement”). If you cannot, you didn’t triage.

---

## 2. Engine A — HTML → SVG → PPTX (Agency Polish Path)

**Borrowed from Akxan/ppt-agent-skill + CerealAxis/Powerpoint-Generator — the only path that nails editorial typography.**

**How:** Write each slide as standalone HTML/CSS (no JS runtime) using Bento Grid tokens, render to SVG via `dom-to-svg` (or headless Puppeteer `dom-to-svg`/`html2svg.py`), then `svg2pptx.py` (or `svg2pptx` npm / `svg2pptx` python) → native vector shapes in `.pptx` (`right-click → Convert to Shape` works in PPT 365). Do **not** use `html2canvas` raster path for text — text must stay selectable.

**When:** Founder pitch, editorial spread, public docket — any deck where 7-level typography + tracking + OpenType matters more than native chart data.

**Guarantee:** `gallery.py`-style smoke: HTML → SVG → PPTX produces editable vectors, not a full-slide PNG. If you fell back to `html2png → png2pptx`, mark the deck “PNG PPTX (pixel-perfect fidelity, not vector)” in the deliver note — don’t claim vector.

**Scripts (skills.sh):**
```bash
# HTML→SVG (one file per slide: slide-01.html → slide-01.svg)
python ${CLAUDE_SKILL_DIR}/scripts/html2svg.py slide-01.html slide-01.svg
# SVG→PPTX (collect)
python ${CLAUDE_SKILL_DIR}/scripts/svg2pptx.py svg/ deck.pptx --size 13.33x7.5
npm alternative:
npx svg2pptx slide-01.svg slide-01.pptx
```

**Constraint:** Keep HTML to CSS variables that `svg2pptx` understands — flex/grid, Bento spacing, SVG text with `tabular-nums`. No JS-driven charts here; use Engine C for data.

---

## 3. Engine B — Slide-Master Layouts (Template Fidelity Path)

**Borrowed from tristan-mcinnis/pptx-from-layouts-skill — the only honest way to survive enterprise templates.**

**Why overlay fails:** Most skills `inventory → replace` by stamping text on top of placeholder rects. Professional masters use `ph` placeholders with `idx`/`type` + `cNvPr` names + `schemeClr` theme refs. Overlay breaks theme, margins, and layout contracts. Raw placeholder fill preserves all three.

**3-Step Contract (keep it):**

**B1 — Profile.** Given branded `template.pptx`:
- Unzip `.pptx` (ZIP). List `ppt/slideLayouts/*.xml` + `ppt/slideMasters/*.xml`. For each layout, extract `p:cNvPr/@name`, `p:ph/@type`, `p:ph/@idx`, and `a:schemeClr` vs `a:srgbClr` refs. Emit `layout-catalog.md` (the `[HINT:]` menu) + `config.json` (`{layouts: [{name, file, placeholders: [{name,type,idx,bounds}]}]}`).
- Reuse `pptx-profile` logic: `python ${CLAUDE_SKILL_DIR}/scripts/profile_template.py template.pptx --out ./catalog` → writes `catalog/layout-catalog.md` + `catalog/config.json`.

**B2 — Author.** Given `catalog` + content, emit `slides.md` linted to those hints:
```md
# Slide 3 — Why Now
[HINT: comparison-2col]
## Left: Before
- 3 weeks to close report
## Right: After
- 4 hours with pipeline
```
Linter checks: every `[HINT: layout]` exists in `config.json`; each placeholder named in content has a `ph` in that layout; no slide exceeds `MARGIN` bounds.

**B3 — Render.** Fill real placeholders via `python-pptx` `_element` (not textbox overlay):
```python
from pptx import Presentation
prs = Presentation("template.pptx")
layout = prs.slide_layouts[get_layout_index("comparison-2col")]  # from config.json
slide = prs.slides.add_slide(layout)
# Fill by placeholder idx/type, not by shape index
ph = slide.placeholders[placeholder_id]  # e.g. ph for title
ph.text = "Why Now"  # run-level preserve if needed
# For typed rich text, clear then add_run to keep schemeClr
tf = ph.text_frame; tf.clear(); p=tf.paragraphs[0]; p.add_run().text="..."
prs.save("deck.pptx")
```
Validate: `validate_pptx.py --check-theme` scans `a:schemeClr` retained vs `a:srgbClr` hard-coded.

---

## 4. Engine C — Native Dict (Programmatic Editability Path)

**Borrowed from PHY041/slide-kit — the only path where code owns every pixel and every pixel stays editable.**

**Mental model (python-pptx docs v1.0.0):** `Presentation → Slides → Shapes → (TextFrame → Paragraphs → Runs | Table → Cells | Chart → Series | Picture)`. A `.pptx` is a ZIP; `python-pptx` mutates `ppt/slides/*.xml` directly.

**Install + version check:**
```bash
pip install -r ${CLAUDE_SKILL_DIR}/requirements.txt  # python-pptx>=0.8.11, pyyaml>=6.0, lxml, Pillow
python -c "import pptx; print(pptx.__version__)"
```

**Canonical contract (verified against installed 1.0.2):**
```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION

prs = Presentation()
prs.slide_width = Inches(13.33); prs.slide_height = Inches(7.5)  # 16:9
blank = prs.slide_layouts[6]  # Blank (index 6 in default 11-layout template)
slide = prs.slides.add_slide(blank)

# Text — bounds explicit, autoFit off, wordWrap on
left, top, width, height = Inches(0.6), Inches(0.6), Inches(4.0), Inches(0.8)
txBox = slide.shapes.add_textbox(left, top, width, height)
tf = txBox.text_frame; tf.word_wrap = True; tf.auto_size = None
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
run = p.add_run(); run.text = "Why Now"; run.font.size = Pt(28); run.font.bold = True
# Prefer schemeClr via theme override; hard RGB only when tokens demand:
run.font.color.rgb = RGBColor.from_string("1B4F72")

# Shape — native, not image
shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(2.0), Inches(3.8), Inches(1.2))
shape.fill.solid(); shape.fill.fore_color.rgb = RGBColor.from_string("EFF1F5")
shape.line.color.rgb = RGBColor.from_string("BDC3C7")

# Table — native, not screenshot
rows, cols = 4, 3
tbl = slide.shapes.add_table(rows, cols, Inches(0.6), Inches(4.0), Inches(6.0), Inches(1.8)).table
tbl.cell(0,0).text = "Metric"
for r in range(rows):
    for c in range(cols):
        cell = tbl.cell(r,c); cell.vertical_anchor = MSO_ANCHOR.MIDDLE

# Chart — native, data editable in PowerPoint
chart = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.6), Inches(2.0), Inches(5.0), Inches(3.0),
    chart_data).chart  # chart_data = ChartData() with categories/series
chart.has_legend = True; chart.legend.position = XL_LEGEND_POSITION.BOTTOM
# Override per-series brand color (don’t trust default palette):
for idx, series in enumerate(chart.series):
    series.format.fill.solid(); series.format.fill.fore_color.rgb = RGBColor.from_string(["1B4F72","2E86AB","A8DADC"][idx])
```
**Shape model escape hatch (when python-pptx lacks helper):**
```python
# Example: preserve a:schemeClr instead of a:srgbClr — drop to lxml
from lxml import etree
# find a:solidFill/a:schemeClr in slide._element, set @val = "accent1" instead of writing srgbClr
```

**What python-pptx cannot do — don’t pretend (per SlideForge 2026, Aspose pinned):**
- Animations / transitions (ECMA-376 §19.5, issue #1106 open since 2018) → author in template master; they survive round-trip.
- Render to PDF/PNG → `LibreOffice soffice --headless --convert-to pdf` or sandbox API; `prs.save("deck.pdf")` writes ZIP wearing pdf extension.
- `.ppt` (OLE2) or `.odp` open → `KeyError` in OPC reader; convert via Aspose/LibreOffice first.
- Autofit solver → `normAutofit` stores PowerPoint’s own computed `fontScale`/`lnSpcReduction`; you must cap text or guard with `--check-overflow`.

---

## 5. PptxGenJS Fallback (JS Lane)

When Node is available and pitch speed matters:

```bash
npm install pptxgenjs  # + canvas for images if needed
node ${CLAUDE_SKILL_DIR}/scripts/render_pptx.mjs --spec spec.json --out deck.pptx --theme vc_clean
```

Same tokens (WIDTH, HEIGHT, MARGIN, GRID_COLS, palette) shared via `style-system.md` — the JS renderer is recoloring-consistent with Python. Pick PptxGenJS when you need rapid Bento cards + timeline widgets without Python startup.

---

## 6. How the AI Picks — One-Line Justification Is Mandatory

For each slide you output a justification that names the engine and why layout/style fit. Examples (good vs bad):

- ✅ Good: “Slide 4 (stats_grid, native dict) — 4 KPIs need editable numbers and per-series brand colors → native chart engine; vc_clean navy for investor trust.”
- ❌ Bad: “Used python-pptx because it’s default” (no reason) or “Used HTML→SVG because it looks nice” (not content-driven).

If two engines tie, default to Engine C (native dict) — most editable, most testable, diffable YAML source.

---

## 7. Common Pitfalls (All Engines)

| Symptom | Cause | Fix |
| Phrase overlaps card border | Box width < content + GUTTER | Enforce `left+width+GUTTER ≤ COL_BOUND`; `--check-overflow` |
| Brand recolor fails | Wrote `a:srgbClr` over `a:schemeClr` | Preserve `schemeClr` via `_element` hatch; `--check-theme` |
| Placeholder left “Click to add” | Unfilled `ph` idx | Profile → fill that `ph` id, don’t overlay textbox |
| Chart colors drift | Left PowerPoint default palette | Per-series `solidFill` override |
| Deck bloat / OOM on 200 slides | python-pptx object model holds all | `lxml`-only extractor for read; generate 1 slide/call + `merge_presentations` for scale |
