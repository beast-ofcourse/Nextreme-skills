# Document Types — Budgets, Blocks, and Taste Per Genre

Pick the type that matches the user’s intent. If no type fits, compose a new one from the block palette — do not force a report template onto a resume.

| Type | Page Budget | Cover | Blocks (in order) | Taste Note |
|---|---|---|---|---|
| **Report** (7–12p) | 550–650 w/p | `report` fullbleed (dark dot grid, Playfair) | cover → TOC (optional, not for 4p) → h1 (accent rule) → body (justified, hyphens) → figure (image+Figure N) → table (three-line) → chart (vector) → callout → divider → back cover | Dark trust, zinc backbone, ink vs terracotta per warmth |
| **Proposal** (6–10p) | 550 w/p | `split` (Syne, left panel) | cover → h1 Problem → h1 Solution → table (pricing, accent header) → timeline → signature | Before/after, split cover signals duality |
| **Resume** (1–2p strict) | 350 (auto-fit) | `typographic` (oversized word, DM Serif) | header (name, contact) → section (h2) → bullets (achievements, not duties) → table (skills) → bar (language) | Auto-fit: scales up until sheet full, no hole on p1 |
| **Portfolio** (6–10p) | 500 | `atmospheric` (near-black, radial glow, Fraunces) | cover → TOC → h1 project → figure grid (meander) → table (specs) → callout (principle) | Meander diagonal photos + threading text (page-as-canvas) |
| **Magazine / Journal** (6p) | 500 | `magazine` (cream `Lora+Cormorant`, meander) | cover → pull quote → body (2-col, `column-count: 2`) → figure (side-wrap) | Editorial, `line-height 1.5–1.55`, drop caps optional |
| **Letter** (1p) | 400 | None or `frame` inset | letterhead (running header) → date → recipient → h1 subject → body → signature | Parchment optional, running header position `top-center` |
| **Minimal** (1–3p) | 550 | `minimal` (white + 8px bar, Cormorant) | h1 → body → divider → table → callout | Single accent moment |
| **Academic** (GOST) | 300 (A4, 14pt) | `academic` (PT Serif) | sections on fresh pages, figures *after* first mention, tables full-width caption-above, bibliography | `Typst` engine preferred, strict `before:`/`after:` anchors |

## Block Palette (Copy-Paste HTML)

```html
<div class="h-1 w-12 bg-[#1B365D] mb-4"></div>
<h1 class="text-[22pt] font-medium" style="letter-spacing:-0.06em">Section Title</h1>
<p class="text-[10.5pt] leading-[1.55] text-justify" style="hyphens:auto; text-wrap:pretty">
  Body with <strong>bold</strong> and <em>italic</em>.
</p>
<blockquote class="border-l-4 border-[#1B365D] bg-zinc-50 p-4 pl-6 my-6">Insight — callout</blockquote>

<table class="w-full text-sm" style="border-collapse:collapse; border-top:1px solid #18181b; border-bottom:1px solid #18181b">
  <thead><tr class="border-b border-zinc-900"><th class="text-xs uppercase tracking-[-0.01em] py-2">Metric</th></tr></thead>
  <tbody><tr class="border-b border-zinc-100"><td class="py-2">Value</td></tr></tbody>
</table>

<figure class="my-6">
  <img src="figure.png" style="max-width:100%" alt="Description">
  <figcaption class="text-xs text-zinc-500 tracking-[-0.01em] mt-2 text-center">Figure 1 — Caption</figcaption>
</figure>

<!-- Chart via Recharts SVG (vector) -->
<div id="chart" class="w-full h-64"></div>

<hr class="border-zinc-200 my-8">
<p class="text-xs text-zinc-500">Caption — muted, 8pt</p>
<div style="break-after: page"></div> <!-- explicit page break only when story demands -->
```

## Cover Extras (Inject via tokens)

- `--accent "#HEX"` (and `accent_lt` auto-derived toward white)
- `--cover-bg "#HEX"`
- `--cover-image` (URL or `assets/cover.jpg` — full-bleed via `background-size: cover`)
- `--abstract` (short deck/abstract on cover, below title)

## Budget Heuristics (When Not Using Typst `estimate_page_budget`)

- Report dense (1.45): 600 words = 1 page. Sparse editorial (1.55 + figures): 400 words = 1 page.
- Resume: 1 page hard. If content is 0.6 page, scale type up (auto-fit) until fill 92%+.
- Portfolio: 1 project ≈ 1.2 pages (images cost lines — budget via Typst `query` if available).

## Anti-Patterns

- TOC on <5 pages = waste.
- Table without banding/header rule = taste fail.
- Chart as PNG screenshot (raster) when SVG vector exists = fail.
- Cover without dot grid / geometric but with stock photo stretched = generic.
