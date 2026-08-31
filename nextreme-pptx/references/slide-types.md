# Slide Types — 17+ Roles, Geometry Recipes

Each slide lives for one job. If you need “and” to describe a slide (“timeline and stats”), split it. Bento Grid decides the card span; this file decides what the cards carry and how the geometry resolves to `Inches()` without overlap.

## Canvas Defaults

```
SLIDE_WIDTH  = Inches(13.33)  # 16:9 default; 4:3 is Inches(10)
SLIDE_HEIGHT = Inches(7.5)
MARGIN = Inches(0.6)
CONTENT_WIDTH = SLIDE_WIDTH - 2*MARGIN  # 12.13″ on 16:9
GRID_COLS = 12
GUTTER = Inches(0.32)
```

Every recipe below honors `MARGIN` + `GUTTER` + `COL_WIDTH` math — never hard `left=Inches(2.37)` without derivation.

---

## Taxonomy (PHY041’s 17, Extended With Bento Roles)

| Group | Type | Slot | Geometry | When |
|---|---|---|---|---|
| **Structural** | `cover` | 12-col hero, centered | Title DISPLAY 44pt at `top = 2.2″`, subtitle BODY 11pt at `top+1.0″` | Deck open |
| | `section_header` | 8-col left, tall band | H1 28pt, eyebrow H3, accent left rule `0.08″` | New chapter |
| | `closing` | 12-col hero, echo cover palette | Same geometry as `cover`, 1 CTA line | Last slide |
| **Pitch** | `problem` | 7+5 (asymmetric) | Left: 3 bullets BODY; Right: quote card | Problem framing |
| | `why_now` | 6+6 (comparison left=Before, right=After) | Two cards, each H3 kicker + 3 bullets | Timing |
| | `bento_features` | 4+4+4 (or 6+3+3) | 3 Bento feature cards, each icon + H3 + 2-line body | Features |
| | `moat_columns` | 6+6 or 4+4+4 | Defensive moats; each card has bold H3 + body | Moat |
| | `matrix_2x2` | Absolute `2×2` matrix (not Bento cols) | Outer rect `8.0″×4.2″` centered, quadrants via lines | Positioning |
| | `stats_grid` | 4× `3-col` (or 3× `4-col`) | KPI: MONO 28pt tabular number + H3 label + Δ | Traction / KPI |
| | `timeline` | Horizontal | Milestone dots on line `top=3.4″`, labels below | Roadmap |
| | `team` | 3× `4-col` (or 4× `3-col`) | Photo (circle crop `1.4″`) + name 11pt + role CAP | Team |
| | `ask` | Single focus 12-col | H2 “We’re raising $X” + 3 use-of-funds bars | Ask |
| **Academic** | `method_diagram` | 8+4 (diagram + steps) | Left: vector boxes+arrows; Right: 3-step bullets | Method |
| | `results_table` | 12-col table | Native table `6 cols × 4 rows`, `MediumGrid`, banded, `schemeClr` header fill | Results |
| | `references` | 12-col list | HANG indent `0.4″`, 9pt BODY, 6 refs max | Bibliography |
| **Universal** | `bar_chart` | 8+4 (chart + insight) | Left: native `COLUMN_CLUSTERED` `8-col≈8.1″`; Right: 4-col insight card | Data |
| | `line_chart` | same as `bar_chart` | `LINE_MARKER` | Trend |
| | `quote` | 12-col centered, 8-col text | 20pt serif italic, attribution 10pt `right` | Social proof |
| | `comparison` | 6+6 | Left vs Right cards, dividers as `schemeClr` line | Before/after |
| | `process` | 3× equal via bento | 3 steps with arrows between (`MSO_SHAPE.RIGHT_ARROW` 0.24″) | Flow |
| | `image_text` | 6+6 | Left: image `6-col`, Right: text `6-col` — **image not generated for team/UI** | Product shot |

Add more only if no type above covers the idea without stretching it. A new type that is “timeline but vertical” is `timeline` with `orientation=vertical`, not a new taxonomy entry.

---

## Geometry Recipes — Copyable Python (Native Engine)

### Cover (12-col hero)

```python
left, top, width, height = Inches(0.6), Inches(2.0), Inches(12.13), Inches(1.2)
txBox = slide.shapes.add_textbox(left, top, width, height)
tf = txBox.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
run = p.add_run(); run.text = "The Deck Title"; run.font.size = Pt(44); run.font.bold = True
# subtitle below
txBox2 = slide.shapes.add_textbox(Inches(0.6), Inches(3.4), Inches(12.13), Inches(0.6))
p2 = txBox2.text_frame.paragraphs[0]; p2.alignment = PP_ALIGN.CENTER
run2 = p2.add_run(); run2.text = "One-line promise the deck keeps"; run2.font.size = Pt(11)
```

### Stats Grid (4 × 3-col — KPI)

```python
cols = 4; card_w = slot_width(3)  # 3 cols each: (COL_WIDTH*3 + GUTTER*2) ≈ 2.8″
for idx, (num, label, delta) in enumerate(stats):  # stats = [("84%","Activation","+12pp"),...]
  left = Inches(0.6) + idx*(card_w + GUTTER)
  card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.2), card_w, Inches(1.9))
  card.fill.fore_color.rgb = RGBColor.from_string("F3F4F6"); card.line.fill.background()
  # number — MONO tabular
  tb = slide.shapes.add_textbox(left+Inches(0.28), Inches(2.4), card_w-Inches(0.56), Inches(0.7))
  p = tb.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
  run = p.add_run(); run.text = num; run.font.size = Pt(28); run.font.name = "JetBrains Mono"
  # label
  tb2 = slide.shapes.add_textbox(left+Inches(0.28), Inches(3.2), card_w-Inches(0.56), Inches(0.4))
  p2 = tb2.text_frame.paragraphs[0]; run2 = p2.add_run(); run2.text = label.upper(); run2.font.size = Pt(9)
```

### Bar Chart (8+4 split)

```python
from pptx.chart.data import ChartData
chart_data = ChartData(); chart_data.categories = ["Q1","Q2","Q3"]
chart_data.add_series("Revenue", [1.2, 1.9, 2.4])
# 8-col slot: left 0.6, width ≈ 8.1″ (8 cols)
chart_shape = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.6), Inches(1.8), Inches(8.1), Inches(3.8), chart_data)
chart = chart_shape.chart; chart.has_legend = True; chart.legend.position = XL_LEGEND_POSITION.BOTTOM
chart.value_axis.has_major_gridlines = True
for ser in chart.series: ser.format.fill.solid(); ser.format.fill.fore_color.rgb = RGBColor.from_string("1B4F72")
# 4-col insight card at right
card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.1), Inches(1.8), Inches(3.6), Inches(3.8))
```

### Matrix 2×2 (Absolute — Not Bento cols)

```python
outer = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(2.66), Inches(1.6), Inches(8.0), Inches(4.2))
outer.fill.background(); outer.line.color.rgb = RGBColor.from_string("E5E7EB")
# quad lines
h = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.66), Inches(1.6), Inches(0.02), Inches(4.2))
v = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(2.66), Inches(3.7), Inches(8.0), Inches(0.02))
```

### Bento Features (4+4+4)

```python
for idx, (icon, title, body) in enumerate(features):  # 3 items
  left = Inches(0.6) + idx*(slot_width(4)+GUTTER)
  card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.0), slot_width(4), Inches(3.4))
  # inner paddings via textboxes at left+CARD_PAD
```

Every recipe honors:
- `word_wrap=True`, `auto_size=None` (so a long word wraps glitch-free instead of overflowing).
- `vertical_anchor = MSO_ANCHOR.TOP` for body (never `MIDDLE` for paragraph text — it re-centers on edits).
- Native chart/table — not image.

---

## Ghost-Deck Checklist (Before Drawing a Pixel)

- [ ] Titles-only reading tells a complete argument (PHY041).
- [ ] No slide repeats the previous slide’s card pattern without narrative contrast.
- [ ] Each slide maps to one `type` above — if you split it into “A and B”, it was two slides.
- [ ] For each slide: `type + Bento layout + engine` is locked and justified.

---

## Density Guards (Borrowed from Noi1r 29 Rules + Akxan Iron Law)

- `≤7` bullets per slide; `≤2` formulas or `≤5` symbols; `≥1` visual per 3 theory slides (method_diagram / chart / table where text alone fails).
- Max `3–4` consecutive theory slides before a visual break (timeline, Bento, chart).
- If a slide wants 8 bullets → it wants to be two slides (split at the 4th bullet’s natural hinge).
