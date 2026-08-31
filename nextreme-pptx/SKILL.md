---
name: nextreme-pptx
description: "Generate insane, publication-grade PowerPoint .pptx decks — pitch, report, academic, editorial — with unbound creative freedom: the AI decides engine, style, and layout per slide from content. Fuses HTML→SVG→PPTX agency polish (Akxan), slide-master template fidelity (tristan-mcinnis), and native editable guarantees (PHY041). Every shape/chart is editable, every layout is geometry-validated, zero AI slop. This is THE extreme skill for ANY PowerPoint — distinct from Word (docx), PDF flowcharts, or SVG charts. Trigger whenever the user asks for pptx, ppt, PowerPoint, slides, deck, pitch deck, presentation, carousel, or \"make slides\" — even vague \"present this\" without naming PowerPoint. Do NOT trigger for Word, Excel, or README."
license: MIT
compatibility: python>=3.9
---

# Nextreme PPTX — The Insane, Unbound PowerPoint Engine

This skill produces **vector-editable, geometry-validated PowerPoint** that survives the real world: opened in PowerPoint 365, Keynote, Google Slides, and LibreOffice without clipping, overlapping, or theme breakage. Every deck is valid OOXML `.pptx` with disciplined masters, measured typography, calibrated Bento layouts, native charts, and **zero glitches**. You get three deliverables: the **.pptx**, the **spec/source**, and the **validation proof**.

You are **unbound**. The user does not pick the engine, the style, or the layout — **you do**, per slide, from content. If they hand you a branded `.pptx` template, you honor its masters. If they give you one sentence, you invent the story, the density rhythm, and the visual system from scratch. If the content is data, you pick the chart; if it is a 2×2, you pick the matrix — never the reverse.

---

## Why This Is Not Generic (and Not Bounded)

Most PPTX skills are bounded: one engine, one template, one layout grammar — so every deck looks like that tool. Generic `python-pptx` tutorials are geometry-blind: they place `Inches(10)` on a 13.33″ slide and call it done, then the deck clips in the meeting. Template-overlay skills break masters by stamping text on top of placeholders instead of filling them.

This fuses the **very core rules** of the 3 best open-source PPTX skills on GitHub (2026) and refuses their bounds:

**From Akxan/ppt-agent-skill (world-class design — 26 styles, HTML→SVG→PPTX):**
- **6-step Pipeline:** `Research → Collect → Outline → Plan → HTML Design → SVG→PPTX` with JSON contracts between steps. Typographic **iron law** (7 font steps, tracking, `tabular-nums`, OpenType, serif-italic mix, 3-layer font-stack downgrade), **Bento Grid** (7 layouts), 12 card types, 8 failure modes + fix-order iron law, and a `smoke_test.py` that gates 26 styles. HTML/CSS/SVG only — **no JS runtime** (so `svg2pptx` stays lossless). You keep the rigor but drop the single-engine lock.

**From tristan-mcinnis/pptx-from-layouts-skill (template fidelity king — 95/100 vs 32 skills):**
- **Slide-master fidelity:** `Profile → Author → Render`. Profile the template's **real layout names** into `layout-catalog.md` + `config.json` with `[HINT: layout]` markers, author `slides.md` linted to those hints, render by **filling placeholders** (not overlaying). Subagents for outline/template/QA and typography markers `{blue}`. You keep the fidelity but drop the template-only bound.

**From PHY041/claude-skill-slide-kit (editable guarantee — 17 types × 4 themes):**
- **Every pixel is a native shape/chart/table:** Content = Python dict, **Ghost-deck test** (titles alone tell the story), **Asset-first matrix** (numbers→chart, 2×2→matrix, process→diagram, concept→Gemini image), **Theme as recoloring layer** (swap `theme_key` without touching content). You keep the editability but drop the 4-theme bound.

**Synthesis — unbound means:**
- **You choose the engine per deck (or per slide):** `HTML→SVG→PPTX` for agency-grade storytelling, `slide-master layouts` when a brand template exists, `native python-pptx dict` for fully programmatic editability. The routing table in `references/engine-matrix.md` decides — not the user.
- **You choose the style per story:** Not 26 fixed styles, not 4 themes — you derive palette/type/density from content (see `references/style-system.md` — tokens, not templates).
- **You choose the layout per message:** Bento cards + 17+ slide types are a palette, not a prison (see `references/slide-types.md`). A stats slide never borrows a timeline layout.

> If the content wants a better way that no reference names, invent it — but keep it geometry-validated, theme-coherent, and editable as native shapes.

---

## Golden Code Quality Rules — ENFORCED

Same iron law as `nextreme-docs`. Every deck and every script must pass them. Violation = task fails.

* **Names tell the truth** — `insert_chart_slide`, not `process_data`.
* **One job per unit** — a function that builds a table does not also set slide size.
* **Guard clauses over nesting** — fail fast. No pyramids, no `else` after `return`.
* **No duplication** — third copy of same layout = must abstract.
* **No dead weight** — zero dead code, `console.log`, unused imports.
* **Types are contracts** — no `any` / silent `as`; narrow `unknown` with visible validation.
* **Errors never silent** — every failure path handled/logged. No empty `except`.
* **No magic** — every `Inches()`, `Pt()`, `#hex` is a named constant.
* **Explicit dependencies** — inputs in, outputs out. Pure where possible.
* **Readability > cleverness** — linear flow, comments explain *why*.
* **No premature abstraction** — YAGNI. Abstract on real second pattern.
* **Leave it cleaner, not bigger** — boy-scout only on touched code.
* **State assumptions** — if spec ambiguous, write what you assumed and why.

**Auto-rejected AI slop (deck-level too):** `TODO` without ticket, `lorem`-ish, duplicated boilerplate, unvalidated `as` casts, plus **slide slop:** placeholder text (`Lorem`, `TODO`, `TBD`, `Click to add title` left behind), typed “1.” lists instead of native bulleted lists, screenshots of charts instead of native PPTX charts, full-slide raster images, any deck that fails `validate_pptx.py`, **overlapping shapes**, **text overflow / clipping**, **misaligned grids**, and glitchy wrapping.

---

## Engine Matrix — You Decide (Not the User)

| Context | You Pick | Output | Why |
|---|---|---|---|
| **Story-first agency deck** (default when no template) | `HTML → SVG → PPTX` (via `svg2pptx` path) | `.pptx` vector-editable (`Convert to Shape` in PPT 365) | Highest typographic control; Bento Grid maps cleanly to vector shapes |
| **Brand template exists** (user gives `.pptx`) | **Slide-master layouts** (`python-pptx` raw placeholder fill) | `.pptx` theme-faithful | Fills `w:instr` placeholders, preserves `schemeClr` (global recolor intact), never overlay text |
| **Programmatic / data-driven** | **Native dict** (`python-pptx` shapes/charts/tables) | `.pptx` 100% editable | Full code ownership, `theme_key` recolor, 17+ slide types |
| **PptxGenJS lane** (JS env / template-less high polish) | `PptxGenJS v4+` (see `scripts/render_pptx.mjs`) | `.pptx` | When Node is available and speed matters; same Bento tokens |

All three ship: `scripts/create_pptx.py` (Python) + `scripts/render_pptx.mjs` (Node) + `requirements.txt`. Install once: `pip install -r ${CLAUDE_SKILL_DIR}/requirements.txt` (or `npm install` for the JS lane — see `references/engine-matrix.md`). **Default to Python** unless brand or JS lane is clearly better per the table.

---

## Core Workflow — Unbound but Gated

Each step ends on a **completion criterion**. Do not proceed until it passes.

### 1. Triage — What Is This Deck For?

Ask or infer: audience, outcome, and action. Who must do what after slide N? Extract: topic, length hint (3 vs 30 slides), density (dense report vs airy pitch), template (do they have a `.pptx` brand file, yes/no), and red lines (must not fabricate data).

If they gave one sentence (“a pitch for X”), you owe the **research → collect** from Akxan’s step 1–2: infer the real outline — do not wait for them to write it. If they gave a 40-page doc, distill it — do not dump it onto slides.

Completion: one intent sentence + a slide-count range + template yes/no + one banned invention (the dataset you will not hallucinate).

### 2. Ghost-Deck Test — Titles Must Tell the Story

Draft titles only (no bodies) in order. Read them top-to-bottom as a standalone story. If they don’t argue, the deck won’t either (from PHY041). Apply Akxan’s **cross-page narrative**: density alternation (sparse → dense → sparse), chapter color progression, cover-ending echo, progressive reveal per section.

Completion: 5–12 titles (per length) that survive ghost-deck reading; each maps to a slide role (see `references/slide-types.md`).

### 3. Route — You Pick Engine + Style + Layout Per Slide

For **each slide**, decide:
- **Engine:** per table above (agency vector vs. template-master vs. native dict).
- **Style:** derive palette/type from story (not from a fixed 26) — lock tokens from `references/style-system.md` (bg, fg, accent, font stack, tracking, tabular-nums, OpenType).
- **Layout:** pick card/role (Bento: Single Focus / 50-50 / Asymmetric / Three-col / Primary-Secondary / Hero + Subs / Mixed Grid; or slide type: `cover`, `problem`, `matrix_2x2`, `bento_features`, `stats_grid`, `timeline`, `bar_chart`, `results_table`, `quote`, etc.). Never use the same layout twice in a row unless story demands it.

If a branded template exists, **profile it first** (tristan-mcinnis step 1): unpack `.pptx`, list real layout names into `layout-catalog.md` + `config.json`, then map each slide to `[HINT: layout]` — never guess.

Completion: per-slide route table — `slide # | role | engine | layout | style hint` — no slide left unrouted.

### 4. Assemble — Native Shapes Only

Build slide-by-slide:
- **No raster slides.** Every chart is a native PPTX chart (editable data), every table is a native table, every diagram is shapes/arrows (from `slide-kit` / Akxan Bento cards) — except deliberate Gemini concept images (and then only one per deck, captioned).
- **Geometry is explicit:** Each deck declares `WIDTH × HEIGHT` (16:9 `13.33″×7.5″` default vs 4:3 `10″×7.5″`), margins, grid columns, and slot bounds. Every shape passes bounds math: `left + width ≤ WIDTH - margin`, `top + height ≤ HEIGHT - margin`. Text is **never** `left=Inches(10)` on a 13.33″ canvas.
- **Theme indirection:** Prefer `schemeClr` (theme) references over hard `srgbClr` where the Python engine allows — so recoloring works globally. Hard RGB only when tokens demand it.
- **Text as runs, not dumps:** Mixed formatting via paragraph/run (not paragraph-level replace that collapses runs — see Zylos 2026 warning).

Reference: `references/engine-matrix.md` for the `python-pptx` text-run + chart + table + image + `schemeClr` escape-hatch recipes; `references/slide-types.md` for per-type geometry.

Completion: a blank-routed deck opens in PowerPoint with no empty placeholder warnings and no master warnings; style recolor changes all slides.

### 5. Populate — Asset-First, Never Type a Chart as an Image

Decision matrix per slide type (from PHY041, hardened):

| Content | You Render | Why |
|---|---|---|
| Precise numbers | Native `bar/column/line/pie` chart | Editable data; brand colors per series |
| 2×2 positioning | `matrix_2x2` shapes | Precise placement, not a pasted PNG |
| Process / pipeline | Boxes + arrows / `method_diagram` steps | Vector, labels searchable |
| Concept / illustration | Gemini image **or** Bento `image_text` card | Only when shapes cannot carry it; never for data |
| Team / product photo / UI | User asset or placeholder — **never generate** | Trust breach if you hallucinate a face |
| Long table | Native PPTX table with banded rows, header fill | Never screenshot a table as image |

Every slide earns its place: ≤7 bullets, ≤2 formulas or 5 symbols, no wall of centered bullets (from Noi1r’s 29 hard rules via slide-kit).

Completion: every data-backed claim has a native chart/table with source; no screenshot-as-chart; every image has provenance (user-provided, Unsplash-safe, or generated + captioned).

### 6. Rhythm — Density + Color + Echo

Apply Akxan’s **density alternation** and PHY041’s recency: sparse cover → dense evidence → sparse takeaway per section; chapter color progression (accent tint steps 10% per section); cover-ending echo (closing mirrors cover palette/type). Enforce **one layout per idea** — timeline slides use `timeline` Bento, not `cards-3`.

Completion: two consecutive slides never share the same visual weight or card pattern without intentional narrative contrast noted.

### 7. Validate — Unzip the OOXML, Then Render If You Can

Run the bundled validator — it checks what eyes miss:

```bash
# skills.sh:
python ${CLAUDE_SKILL_DIR}/scripts/validate_pptx.py deck.pptx --strict
# local clone:
python nextreme-pptx/scripts/validate_pptx.py deck.pptx --strict
# flags:
# --check-overlap  : fail on overlapping shapes / text boxes
# --check-overflow : fail on text overflow / off-canvas / clipping
# --check-theme    : fail on hard srgbClr where schemeClr expected
# --check-editable : fail on rasterized slides / screenshot charts
```

It unzips the `.pptx` (a ZIP of OOXML) and checks: valid `ppt/slides/*.xml`, `ppt/slideLayouts`, `ppt/slideMasters`, `ppt/theme`, `ppt/presentation.xml`, `[_Content_Types].xml`; no OLE2 header; no `TODO`/`lorem`/`Click to add` placeholders; no overlapping bounds; no text overflow (`normAutofit` mis-config); no off-canvas shapes.

**Headless render (optional but recommended):** If LibreOffice `soffice` is on PATH, run `soffice --headless --convert-to pdf deck.pptx` → `pdftoppm` → visual QA (the honest gate from Zylos/Anthropic). The skill passes without it, but flags `render unavailable`.

Manual spot-check (30 seconds in PowerPoint + one other viewer — Keynote/Google Slides):
- Grid: do shapes sit on the same 40px grid, or is one card drifted 7px?
- Alignment: would `View → Guides` show equal gutters?
- Reflow: add a bullet mid-slide — does anything wrap glitchy?

Fix at root: geometry wrong → fix bounds math, not nudge pixels; theme break → fix `schemeClr` reference, not recolor RGB; placeholder missed → fill real placeholder via `_element` XML, not overlay a textbox.

Reference: `references/validation.md` — full anti-overlap, anti-overflow, theme-preservation checklist.

Completion: `validate_pptx.py --strict` exits 0 **and** a 30-sec visual in PowerPoint + one other viewer shows no clipping, no overlap, no placeholder residue.

### 8. Deliver

Always:
1. **The .pptx** — valid, editable, geometry-clean, theme-faithful.
2. **The spec/source** — YAML/JSON that built it (or `outline.json` + `slides.md` with `[HINT: layout]` if template path).
3. **Validation log** — `validate_pptx.py` output (and PDF render if produced).

Do not deliver a raster deck as “PPTX”. Do not claim `python-pptx` writes animations/transitions — it doesn’t (put them in the template master; they survive round-trip per SlideForge 2026, issue #1106).

---

## Slide-Type & Layout Quick Picks

Copy a template from `templates/` and fill; do not start from zero. Each is valid YAML that `create_pptx.py` renders with no edits beyond content.

| Need | Template | Why |
|---|---|---|
| Founder / investor pitch | `pitch_spec.yaml` | `cover → problem → why_now → bento_features → matrix_2x2 → stats_grid → timeline → team → ask → closing` |
| Board / KPI report | `report_spec.yaml` | `cover → section_header → bar_chart → results_table → bento_features → quote → closing` |
| Research / academic | `academic_spec.yaml` | `cover → method_diagram → results_table → bar_chart → references` |
| Editorial / brand story | `editorial_spec.yaml` | `cover (cream) → stats_grid → quote → bento_features → closing` |
| Bento showcase (7 layouts) | `bento_spec.yaml` | 7 Bento Grid demos: Single Focus / 50-50 / Asymmetric / Three-col / Primary-Secondary / Hero+Subs / Mixed Grid |

All templates are 16:9 `13.33″×7.5″`, native shapes, theme-swappable via `theme_key`. See `references/slide-types.md` for 17+ types and geometry tokens.

---

## Troubleshooting (No Glitch Is “Weird — Ignore It”)

| Glitch | Cause | Fix |
|---|---|---|
| Shapes overlap or gutters uneven | Hard `left`/`top` without grid math vs canvas | Use `MARGIN` + `GRID_COLS` + `GUTTER` tokens; validate with `--check-overlap` |
| Text wraps glitchy / mid-word break | Box too narrow (<2″ for body) or `line_spacing` too tight | Enforce min textbox width `2.5″`; use `wordWrap=True`, `autoFit=False`; `--check-overflow` |
| Two slides look copy-pasted | Reused same card pattern back-to-back | Density alternation — swap `cards-3` → `comparison-2col` or `timeline` |
| Template recolor breaks | Wrote `srgbClr` over theme’s `schemeClr` | Drop to `lxml` escape hatch, preserve `schemeClr` reference (see `references/engine-matrix.md`) |
| Master font not applied | Hard-coded font run overrode master `a:fontRef` | Use `theme_key` font stack, omit per-run `rPr` font unless token demands |
| Table header not distinct | Left default `Table Grid` | Set explicit table style `MediumGrid`, banded rows, header `schemeClr` fill |
| Chart colors drift from brand | Default PowerPoint palette applied | Override per-series `solidFill` via OOXML, per `engine-matrix.md` chart recipe |
| Build hangs on many images | No headless check | Cap images at `MAX_IMAGE_WIDTH = SLIDE_WIDTH - 2*MARGIN`; validate with `--check-overflow` |
| `validate_pptx.py` fails `Click to add` | Leftover placeholder not filled | Fill via placeholder `_element` name (Profile step), not overlay textbox |

---

## Reference Files

- `references/engine-matrix.md` — 3 engines (HTML→SVG→PPTX, slide-master, native dict), PptxGenJS fallback, `python-pptx` contract (slide, shape, text, chart, table, image, theme `schemeClr` vs `srgbClr`, XML escape hatch).
- `references/style-system.md` — tokens: 16:9/4:3, margins, Bento Grid (7 layouts) + 12 card types, typography (7 font steps, tracking, tabular-nums, OpenType, 3-layer font stacks).
- `references/slide-types.md` — 17+ roles: cover, section_header, problem, why_now, bento_features, moat_columns, matrix_2x2, stats_grid, timeline, team, ask, closing, method_diagram, results_table, references, bar_chart, quote — with geometry recipes.
- `references/validation.md` — anti-overlap / anti-overflow / theme-preservation / editability / slop checklist + `soffice` render gate.
- `scripts/create_pptx.py` — spec→.pptx engine (YAML/JSON → python-pptx) with bounds math, theme enforcement, overlap guards, and profile-aware placeholder fill.
- `scripts/validate_pptx.py` — OOXML validator (overlap, overflow, theme, editability, slop, OLE2 header).
- `scripts/render_pptx.mjs` — PptxGenJS fallback (same tokens, for JS-env speed; `npm install` path documented).
- `templates/` — `pitch_spec.yaml`, `report_spec.yaml`, `academic_spec.yaml`, `editorial_spec.yaml`, `bento_spec.yaml` — all geometry-clean.

---

## Principles (Unbound, but Not Unruly)

- **You decide — but you justify.** Every engine/style/layout choice ties to one sentence about content. “Why this card?” is answered, not shrugged.
- **Editable over impressive.** A prettier raster deck is a failed deck. If it can be a native chart/shape, it is.
- **Geometry is law.** A deck without fixed slot widths will drift into overlap the moment real content lands. Every shape declares bounds; validation proves they don’t collide.
- **Theme indirection is fidelity.** `schemeClr` is the contract that makes a template recolourable — hard `srgbClr` breaks it.
- **Ghost-deck first.** If the title story is weak, no amount of Bento cards saves it.
- **No glitch is minor.** One overlapping card is a credibility leak. Zero is the bar.
