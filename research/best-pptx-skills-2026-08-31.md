# Best PPTX Generation Skills — Deep Research (2026-08-31)

**Question:** Which GitHub skills are best-in-class for `.pptx` / PowerPoint generation in 2026, what engines do they use, and what should `nextreme-pptx` borrow to be #1?

**Method:** Live web search (2026-08-31) + doc fetch on high-trust primary sources: GitHub READMEs (stars, commits, architecture docs), `python-pptx` official docs (v1.0.0), SourceToDocs/Zylos technical analyses (2026-06/07), SlideForge engineering posts, and Anthropic official pptx skill design (as referenced by Zylos).

---

## 1. Executive Summary — Top 3 For Different Needs

| Rank | Skill | Stars | Engine | Core Thesis | When to Pick |
|---|---|---|---|---|---|
| **1** | **Akxan/ppt-agent-skill** | 140 | `HTML → SVG → PPTX` (dom-to-svg, svg2pptx) | 6-step pipeline (research→outline→HTML→SVG→PPTX), 26 benchmarked styles (Linear/Stripe/Apple/NYT), 18 charts, Bento Grid, strict typography (tabular-nums, OpenType) | General “one sentence → agency-quality deck” — best overall polish per websearch consensus |
| **2** | **tristan-mcinnis/pptx-from-layouts-skill** | — (new, benchmarked 95/100 vs 32 skills) | `python-pptx` **via slide-master layouts** (not inventory/replace) | Profile template → tag `slides.md` with `[HINT: layout]` → render into real placeholders | **Enterprise / brand-sensitive** — you own a designed `.pptx` template and must not break masters |
| **3** | **PHY041/claude-skill-slide-kit** | — | `python-pptx` native shapes (17 slide types, 4 themes) | Every element is editable shape/chart/table — no rasterized slides; Gemini image only for concept diagrams | Researchers / founders who need **fully editable native PPTX** from Python dict |

If you must pick **one to clone for an extreme skill**, merge **(1)’s pipeline + design rigor** with **(2)’s template fidelity** and **(3)’s editability guarantee**. No current skill does all three at once — that is the gap for `nextreme-pptx`.

---

## 2. Full Field — 10 Skills Scanned

### Tier 1 — World-Class Design System
**Akxan/ppt-agent-skill** — https://github.com/Akxan/ppt-agent-skill — 2026-03-20 — 140★ / 48 forks — MIT
- **Pipeline:** 6 steps: demand research → material collection → outline → planning draft → HTML design (per 26 styles) → `html_packager → html2svg → svg2pptx → gallery` (scripts: `html_packager.py`, `html2svg.py`, `svg2pptx.py`, `gallery.py`, `smoke_test.py`).
- **Design:** 26 styles in 5 blocks (dark-pro 7, light-premium 8, vibrant 4, oriental 3, natural-retro 4) — each mock 1280×720, real CSS reference (not screenshots). Typography tier: 7 font-size steps, tracking law, `tabular-nums`, `OpenType` features, serif-italic mix, 3-layer font-stack downgrade. Bento Grid 7 layouts (Single Focus, 50/50, Asymmetric, Three-col, Primary-Secondary, Hero+Subs, Mixed Grid).
- **Charts:** 18 — basic 8 (progress/mirror bar, donut, sparkline, dot-grid, KPI, metric row, rating) + advanced 6 (radar, timeline, funnel, gauge, multi-bar, geo) + ECharts-level 4 (choropleth, network, sankey, calendar heatmap) — all pure HTML/CSS/SVG (no JS runtime → svg2pptx safe).
- **QA:** Failure-mode catalog (8) + fix-order iron law + smoke_test (52 style + pipeline-compat checks, 6 end-to-end HTML→SVG→PPTX).
- **Why it leads:** Only skill benchmarking itself against Linear/Anthropic/Stripe/Apple editorial pages and enforcing typography as code, not vibes. HTML→SVG→PPTX preserves editability (`right-click → Convert to Shape` in PPT 365).

### Tier 1 — Template Fidelity King
**tristan-mcinnis/pptx-from-layouts-skill** — https://github.com/tristan-mcinnis/pptx-from-layouts-skill — MIT
- **Architecture:** 3 skills: `pptx-profile` (template → `layout-catalog.md` + `config.json` with real `[HINT:]` names) → `pptx-author` (catalog + content → `slides.md` linted) → `pptx-from-layouts` (slides.md + template + config → validated `deck.pptx`). Subagents: `pptx-outline-architect`, `pptx-template-onboarder`, `pptx-deck-qa`.
- **Insight:** Tested 32 skills; most use `inventory/replace` overlay (breaks many professional templates). This uses **slide-master layouts & placeholders** — semantically correct. Scored **95/100** vs `pptx-jjuidev 94`, `anthropics-pptx 90.6` (included in `alternatives/` for transparency). Bundled `Inner Chapter` template is demo only.
- **Typography markers:** `{blue}`, `{bold}`, `{question}` — rich formatting without breaking placeholder runs.

### Tier 2 — Editable Native Shapes
**PHY041/claude-skill-slide-kit** — https://github.laiyagushi.com/PHY041/claude-skill-slide-kit — 2026-04-21 — MIT
- **Model:** Content = Python dict → 17 slide types (`cover`, `section_header`, `problem`, `why_now`, `bento_features`, `moat_columns`, `matrix_2x2`, `stats_grid`, `timeline`, `team`, `ask`, `closing`, `method_diagram`, `results_table`, `references`, `bar_chart`, `quote`) × 4 themes (`vc_clean` navy, `academic_minimal` Georgia, `research_dark` navy/cyan-orange, `editorial` cream/red serif). Every shape/chart/table is native editable — no HTML/raster.
- **Charts:** Native `.pptx` Chart objects (editable data). Asset matrix: numbers→`bar_chart`, 2×2→`matrix_2x2`, process→`method_diagram` (boxes+arrows), concept→`method_diagram` + Gemini Nano Banana (SOTA text-in-image).
- **Principle:** “Ghost-deck test: titles alone must tell the argument.” Theme is recoloring layer — swap `theme_key` without touching content.

**CerealAxis/Powerpoint-Generator** — https://github.com/CerealAxis/Powerpoint-Generator — 2026-04-06 — MIT — fork of `Akxan/ppt-agent-skill` with 16 styles, 7 bento, 12 card types (`text/data/list/tag_cloud/process/timeline/comparison/quote/stat_block/feature_grid/image_text/data_highlight`), dual export `SVG PPTX` (editable vectors) + `PNG PPTX` (pixel-perfect), 6-step pipeline + `pipeline-compat.md`.

**Noi1r/powerpoint-skill** — PptxGenJS + **OMML math** (native PowerPoint math via pandoc, editable) + LaTeX PNG@600DPI fallback + 5-layer diagram pipeline (Graphviz→Mermaid→TikZ→Shapes→PDF extraction), 5 themes, 29 hard rules (density, layout diversity, overflow guards), 6-step QA loop with scoring. Caveat: OMML renders blank in LibreOffice PDF (PowerPoint/WPS only) — documented.

**timmonsyim/presentation-skill** + **siril9/presentation-skill** + **gnipbao/knowledge-cat-ppt-skill** — all **source-first** (`outline.json` is source of truth, scripts build `.pptx`, QA before delivery). Common converge:
- **Source-first:** `outline.json` + `design_brief.json` + `content_plan.json` + `evidence_plan.json` + `asset_plan.json` → `pptxgenjs` (JS) or `python-pptx` (Python) renderer.
- **Renderer:** `pptxgenjs` v4.0.1 (dominant JS, zero deps, browser+Node; Anthropic’s official skill chose it) vs `python-pptx` (mature Python, free/MIT, 28.3 MB vs Aspose 196.6 MB).
- **Presets/grammars:** 13–16 style families + 8 composition grammars (Answer Pyramid, Evidence Plate, etc.) + descriptor corpus (~2,200 deck-like records → 311 atoms) — style routing without copying assets.
- **QA is structural:** Geometric (overflow/overlap) + render (LibreOffice `soffice → pdftoppm` → visual subagent) + content (placeholder grep) — looped until 0 new issues. Anthropic’s skill explicitly unpacks `.pptx` to raw XML for edits (not object model) → repack, to preserve `schemeClr` theme indirection.

**Others scanned:** `0xZoharHuang/pptx-skill-cc-gemini-` (Gemini CLI HTML→PPTX, `html2pptx.cjs`, `inventory.py/replace.py/rearrange.py/thumbnail.py`), `VikrantSingh01/md2pptx` (markdown → leadership-grade `.pptx`, themeable), `powerpoint-igorwarzocha`, `elite-powerpoint-designer`, etc. (lower fidelity per `pptx-from-layouts` benchmark).

---

## 3. Engine Truth — What `python-pptx` Can and Cannot Do (2026)

**Source:** `python-pptx` docs v1.0.0 + SourceToDocs practical guide (2026-06-07) + Zylos research (2026-07-03) + SlideForge limitations post (2026-04-20) + Aspose comparison (2026-08-12, pinned: python-pptx 1.0.2 vs Aspose 26.7.0).

**Can do well (and why it’s the de facto Python choice — MIT, mature, 28.3 MB):**
- Round-trip any `.pptx` (ZIP of OOXML), add slides, populate text placeholders **by named placeholder** (not position/string-match), add images/tables/autoshapes, add column/bar/line/pie charts (native editable), core properties.
- Template fidelity IF you target placeholders by `Selection Pane` name and use run-level replacement (preserves single-run formatting; paragraph-level replace collapses runs and loses bold/highlight/link). Picture/text placeholders survive if touched minimally.

**Cannot do (and silent failure modes that must be QA’d):**
- **Brand fidelity:** Writes `srgbClr` (hard RGB) not `schemeClr` (theme reference) → breaks global recoloring; image cropping (`a:srcRect`) minimal API → round-trip can lose crops; theme color inheritance via slide master fragile if master edited mid-pipeline.
- **Geometry:** No bounds/overflow validation — `left=Inches(10)` on 13.33″×7.5″ silently clips; no autofit solver — PowerPoint’s `normAutofit` (`fontScale`/`lnSpcReduction`, e.g. `55000`=55%) is result of its own iterative solver (whole-number font steps + ≤20% line-spacing reduction); no library replicates it. Trade-off: fonttools (fast, shaping-unaware) vs HarfBuzz (correct `x_advance` but needs font file) vs LibreOffice/Aspose (ground truth, heavy).
- **No rendering:** No `slide.to_image()`, no PDF/HTML export, no animation/transition exposure (timing tree ECMA-376 §19.5, issue #1106 open since 2018). Put animations in the template (preserved round-trip) or transplant `timing` tree via `lxml` (brittle — `spid` must match).
- **Charts:** Stacked column with data labels, waterfall/combo → uneven; colors need explicit per-series override or PowerPoint theming muddies brand palette.
- **Scale:** Large decks OOM via python-pptx object model → use `lxml`-only XML extractor; `Presentation.save()` under `.pdf` name still writes ZIP (no PDF writer).

**Convergent fix (Anthropic + Zylos + PPTAgent):** *Generate ≠ trust*. Mandatory loop: `generate → LibreOffice headless → PDF → pdftoppm → images → adversarial visual review (subagent) + programmatic checks (overflow, placeholder grep) → fix source → re-render` until clean. Preserve `schemeClr` indirection; treat fixed slot widths as constraints to rephrase to, not geometry to mutate.

---

## 4. What Makes a Skill “World-Class” in 2026 — Extracted Pattern

1. **Pipeline, not prompt:** 5–6 explicit steps with JSON contracts between steps (research/outline/plan/HTML/SVG/PPTX), each step referencing its `references/` file.
2. **Style as code:** 13–26 named styles, each with CSS variables (palette, font stack, density, spacing), plus Bento Grid / composition grammar (7–12 card/role types) — not freeform layout.
3. **Editability guarantee:** Either native shapes (`python-pptx`/`PptxGenJS`) or `HTML→SVG→PPTX` with `Convert to Shape` — never full-slide raster.
4. **Template as contract:** Distill finished deck → placeholder contract (`layout-catalog.md` + `config.json` / `design_brief.json`) → enforce slot widths, `schemeClr` preservation, font stacks.
5. **QA as gate:** Geometric + render + content checks, iterative, with receipts (hash-bound approval, `smoke_test.py`, visual contact sheets).
6. **Failure catalog:** 8+ documented failure modes (underfill, decorative substitution, off-canvas, theme-break, autofit miss) with fix-order iron law.

---

## 5. Recommendation for `nextreme-pptx` (the extreme skill you want as #1)

**Positioning:** `nextreme-docs` did `python-docx` discipline → do the same for slides but beat the field by solving the half no one solves well: *layout safety + brand fidelity together*.

**Borrow:**
- From **Akxan** — 26-style rigor + Bento Grid + `smoke_test.py` + failure-mode catalog + `html_packager/html2svg/svg2pptx` **editable vector** path (best general polish).
- From **tristan-mcinnis** — 3-step `profile → author → render` with real `[HINT: layout]` tags and placeholder-name discipline (only way to survive enterprise templates).
- From **PHY041** — 17 slide-type taxonomy + 4-theme recoloring layer + ghost-deck test.
- From **Anthropic/Zylos** — `unpack → raw XML edit → repack` for template-preserving edits (preserve `schemeClr`), plus mandatory `soffice → pdftoppm → visual QA` loop (the honest differentiator).

**Must-have for #1:**
- `compatibility: python>=3.9` + `requirements.txt` (`python-pptx`, `pyyaml`, `lxml`, `Pillow`) — ship `scripts/` + `templates/` + `references/` via `skills.sh` (same fix we just did for `nextreme-docs`).
- Dual renderer: **PptxGenJS** (JS) for from-scratch agency decks, **python-pptx raw-XML** for template-preserving enterprise decks — chosen per task, not one-size.
- `references/style-system.md` with measured tokens (paper: 13.33″×7.5″ 16:9 vs 10″×7.5″ 4:3, margins, font scales, `tabular-nums`, OpenType, 3-layer font stacks like `Calibri→Arial→Aptos`).
- `scripts/validate_pptx.py` — OOXML validator (unzip, check `schemeClr` vs `srgbClr`, overflow/bounds, placeholder grep, `lxml`-only fast path for large decks) + `scripts/render_check.py` (LibreOffice headless where available).
- `templates/` — 9–12 role-based starters (cover, section, problem/why-now, bento-features, matrix_2x2, stats_grid, timeline, quote, bar_chart, method_diagram, references, ask) × 4 themes — each valid YAML/JSON with real content, not filler.

**Anti-patterns to reject (per Zylos/SlideForge):** inventory/replace overlay (breaks masters), hard-coded RGB instead of `schemeClr`, mutating slide geometry to fit overflow (rephrase instead), animation via code (use template timing), `save("deck.pdf")` via `python-pptx` (ZIP-wearing-PDF), and skipping the render QA step (overflow only observable in pixels).

---

## 6. Sources (High-Trust, 2026)

- Akxan/ppt-agent-skill — https://github.com/Akxan/ppt-agent-skill — README (2026-03-20, 140★, 26 styles, 18 charts, smoke_test)
- tristan-mcinnis/pptx-from-layouts-skill — https://github.com/tristan-mcinnis/pptx-from-layouts-skill — README (95/100 benchmark vs 32 skills, `[HINT:]` flow)
- PHY041/claude-skill-slide-kit — https://github.laiyagushi.com/PHY041/claude-skill-slide-kit — README (2026-04-21, 17 types, 4 themes)
- CerealAxis/Powerpoint-Generator — https://github.com/CerealAxis/Powerpoint-Generator — README (2026-04-06, 16 styles, dual PPTX export)
- SourceToDocs — python-pptx practical guide — https://sourcetodocs.com/blog/python-pptx-practical-guide/ — 2026-06-07
- SourceToDocs — PowerPoint Automation — https://sourcetodocs.com/powerpoint-automation/ — 2026-04-26
- Zylos Research — Template-Driven Document Generation — https://zylos.ai/research/2026-07-03-template-driven-document-generation-ooxml-brand-compliance/ — 2026-07-03 (Anthropic pptx skill architecture, `schemeClr` vs `srgbClr`, autofit solver)
- SlideForge — python-pptx vs API — https://slideforge.dev/blog/generate-powerpoint-python — 2026-04-03 / 2026-04-20 limitations post
- Aspose vs python-pptx — https://products.aspose.com/slides/python-net/python-pptx-comparison/ — pinned 2026-08-12 (python-pptx 1.0.2 vs Aspose 26.7.0, no rendering in python-pptx)
- python-pptx docs — https://python-pptx.readthedocs.io/en/latest/ — v1.0.0 (capabilities, placeholder docs)
- timmonsyim/presentation-skill, siril9/presentation-skill, gnipbao/knowledge-cat-ppt-skill, Noi1r/powerpoint-skill — READMEs via search snippets 2026

*Captured 2026-08-31 — next step: use this as spec for `nextreme-pptx` (extreme PPTX skill) following the `nextreme-docs` pattern.*
