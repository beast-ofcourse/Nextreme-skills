---
name: nextreme-pdf
description: "Generate insane, taste-driven PDF documents — reports, proposals, resumes, portfolios, magazines, academic papers, letters — with unbound creative freedom: the AI decides palette, typography, and layout from content semantics. Fuses zinc-backbone + editorial parchment taste (pdf-forge + Kami), HarfBuzz/Knuth-Plass typography (imprint), page-as-canvas budget→compose→QC (beautiful-pdf-mcp), and token-driven doc types (minimax). Every PDF is HTML + Tailwind → Playwright/Paged.js, print-ready, no AI slop. This is THE extreme skill for ANY PDF — distinct from PPTX (slides), DOCX (Word), or SVG charts. Trigger whenever the user asks for pdf, PDF, report, proposal, resume, portfolio, magazine, brochure, whitepaper, or \"make it a PDF\" — even vague \"pretty document\" without naming PDF. Do NOT trigger for PPTX or DOCX alone."
license: MIT
compatibility: python>=3.9
---

# Nextreme PDF — The Taste-Driven, Unbound PDF Engine

This skill produces **print-ready, taste-driven PDFs** that look like they were art-directed, not auto-generated: warm or zinc canvas, disciplined tracking, geometric spacing, native vector charts, and per-page QC. Every output is a standalone `*.pdf` rendered from self-contained HTML + Tailwind (no React build step, no component library) via Playwright/Paged.js, with a **page-as-canvas** guarantee: each sheet is a finished block, not an accident. You get three deliverables: the **PDF**, the **HTML source**, and the **layout proof**.

You are **unbound but tasteful**. The user does not pick the palette, the type scale, or the cover — **you do**, from content semantics. A fintech report does not get the same ink-blue as a poetry portfolio; a dense academic paper does not get the same 4-grid as a one-pager. If they hand you a brand hex, you honor it; if they hand you one sentence, you invent the visual identity — but you do it with taste, not random color.

---

## Why This Is Not Generic (and Why Taste Matters)

Most AI PDFs are instantly recognizable as AI: positive letter-spacing, flat hierarchy, random accent, endless bullets, tables that spill, first page with white-border cover, and `lorem` where a chart should be. Operators then open Figma and redo it.

This fuses the **very core taste + engineering** of the 4 best PDF systems on GitHub (2026) and refuses their bounds:

**From syx-labs/pdf-forge (Vercel/Stripe aesthetics, HTML+Tailwind+Playwright):**
- **Zinc backbone:** 90% zinc shades, color as accent. **Semantic tracking** (4 negative levels: `display -0.10em`, `heading -0.06em`, `body -0.025em`, `label -0.01em` — positive tracking = AI marker), **geometric spacing** (4,8,12,16,24,32,48,64,80,96 — no arbitrary), **one accent, one moment** (gradient only on highest-impact element), **raw HTML** (flat DOM, predictable Playwright). You keep the system, drop the 16-template bound.

**From tw93/Kami (editorial parchment, 6 doc types bilingual):**
- **8 invariants:** parchment `#f5f4ed` (not white), single ink-blue `#1B365D` (warm-neutral only, no `#6b7280`), serif `Newsreader` headlines/body (Chinese: TsangerJinKai + Source Han Sans), serif weight locked 500, line-heights 1.1–1.3 / 1.4–1.45 / 1.5–1.55 (never 1.6+), solid hex tags (no `rgba` → WeasyPrint double-rect), depth via ring/whisper shadow only. You keep the editorial discipline, drop the single-accent lock.

**From tamimbinhakim/imprint-pdf (no Chromium, real typography):**
- **Real Tailwind (Oxide) + HarfBuzz + Taffy + Knuth–Plass + Plass page breaker** — edge sub-100ms, CSS Grid, variable fonts, PDF/X-4 + CMYK, vector Recharts. You keep the typographic truth (kerning, ligatures, widows/orphans/footnotes), drop the React-only bound.

**From Kreminskaya/beautiful-pdf-mcp (Typst, page-as-canvas):**
- **Budget → Compose → QC → Two-pass image placement:** `estimate_page_budget` (words/lines that fit one page *before* writing), compose to bottom of type area (carryover mid-sentence, no holes), per-page `layout_report` (fill %, defects), two-pass `after:N` image placement via `typst query` position marks. You keep the page-as-canvas guarantee, drop the Typst-only bound.

**From X-FRI/minimax-pdf (token-driven, 15 doc types):**
- **Token design system:** palette/typography/spacing derived from doc type; `palette.py` → `cover.py` → `render_cover.js` → `render_body.py` → `merge.py`; `h1→body→callout→table→chart→flowchart→divider` blocks; `CREATE`/`FILL`/`REFORMAT` routes. You keep the token coverage, drop the reportlab-only bound.

**Synthesis — taste-driven, unbound:**
- **You derive taste from content:** A warm academic report gets terracotta `#9C6B4F` on cream, a fintech report gets deep zinc + ink-blue, a portfolio gets atmospheric near-black + radial glow — not the template’s default. The tokens in `references/design-taste.md` are your law.
- **You respect the page as canvas:** Before writing, you budget; while composing, you fill to the bottom; after rendering, you QC fill and re-place images — never leave a half-empty page or a stranded photo.
- **You render via the best engine for the job:** HTML+Tailwind+Playwright/Paged.js for most (best CSS fidelity, see `references/engine-matrix.md`); Typst for GOST/academic when Typst is on PATH; WeasyPrint for print-native fallback. You choose — not the user.

> If the content wants a better cover that no reference names, invent it — but keep zinc or parchment discipline, negative tracking, geometric spacing, and one-accent law.

---

## Golden Code Quality Rules — ENFORCED

Same iron law as `nextreme-docs`/`nextreme-pptx`. Violation = task fails.

* **Names tell the truth** — `render_cover`, not `process_data`.
* **One job per unit** — a function that layouts a table does not also choose the palette.
* **Guard clauses over nesting** — fail fast. No pyramids.
* **No duplication** — third copy = abstract.
* **No dead weight** — zero dead code, unused imports.
* **Types are contracts** — no `any`/silent `as`; validate at boundaries.
* **Errors never silent** — every failure path logged with context.
* **No magic** — every `4px`, `Pt(11)`, `#hex` is a named token.
* **Explicit dependencies** — pure where possible.
* **Readability > cleverness** — linear flow, comments why not what.
* **No premature abstraction** — YAGNI.
* **Leave it cleaner** — boy-scout only on touched code.
* **State assumptions** — wrong-but-confident is worse than incomplete.

**Auto-rejected AI slop (PDF-level too):** `TODO` without ticket, `lorem`-ish, generic scaffolding, plus **PDF slop:** positive tracking, random accent per page, endless centered bullets, tables without banding, charts as raster screenshots, `Click to add` residue, any PDF that fails `validate_pdf.py`, overlapping text, rivers (gappy justified text), orphan/widow, and a cover with white-border (missing `@page :first { margin: 0}`).

---

## Design Taste — The Twist (Great Taste, Not Random Taste)

This is the skill’s signature — the taste that makes a PDF feel expensive.

**Canvas:**
- **Default:** **Zinc backbone** (90% `zinc-50` → `zinc-900`, color is accent). **Alternative:** **Parchment** `#f5f4ed` (warm, editorial) when the story is human, literary, or heritage — you choose. Never pure white `#fff` as body bg (too sterile).
- **Ink:** One ink. For zinc → `zinc-900`; for parchment → ink-blue `#1B365D` (warm-neutral, never cold `#6b7280`).
- **Warm check:** All neutrals warm-toned. No `rgba()` for tags (solid hex only).

**Tracking (all negative — positive = AI marker):**
- `tracking-display: -0.10em` (cover title), `tracking-heading: -0.06em` (H1/H2), `tracking-body: -0.025em` (prose), `tracking-label: -0.01em` (eyebrow, caption). Calibrated from Linear/Vercel/Framer.

**Spacing (geometric, no arbitrary):**
- `4, 8, 12, 16, 24, 32, 48, 64, 80, 96` — and only these. A 20px gap is a taste failure.

**One Accent, One Moment:**
- Accent appears once per spread as hero: cover title, first `h1` rule, or callout bar — not on every heading. Gradient (if any) on that single element only.

**Typography (two stacks, you pick):**
- **Sans editorial:** `Inter → Calibri → Arial` (body), `Newsreader → Georgia` (display), weight locked 500 for heads, line-height 1.1–1.3 (display), 1.4–1.45 (dense body), 1.5–1.55 (reading). Never 1.6+.
- **Serif authority:** `Newsreader`/ `EB Garamond` for long-form; `DM Serif` for covers. Mono `JetBrains Mono` for code/numbers (`tabular-nums`).

**Depth:** Ring shadow (`0 0 0 1px rgba(0,0,0,0.04)`) or whisper (`0 1px 2px rgba(0,0,0,0.04)`) — never hard `0 8px 32px` drop.

Reference: `references/design-taste.md` — full tokens, palettes (terracotta, Nord Frost, ink-wash, GitHub Light, etc.), and cover patterns (`fullbleed`, `split`, `typographic`, `frame`, `editorial`, `stripe`, `diagonal`).

---

## Engine Matrix — You Decide

| Context | You Pick | Why |
|---|---|---|
| **Most PDFs (default, best taste)** | **HTML + Tailwind CDN + Playwright + Paged.js** (`scripts/render_pdf.mjs` + `scripts/generate_pdf.py`) | Full Tailwind, Grid, `@page` print CSS, paged headers/footers, `target-counter` cross-refs; what pdf-forge/Kami ship |
| **Academic / GOST / book (long-form, strict pagination)** | **Typst** (`typst compile`, `beautiful-pdf-mcp` path) if `typst` on PATH | `estimate_page_budget` + per-page `layout_report` + two-pass `after:N` image placement — page-as-canvas guarantee |
| **Print-native / tagged PDF fallback** | **WeasyPrint** (`weasyprint`, `paged` media) | Print CSS, PDF/UA tagging without Chromium; lighter than Playwright |
| **Edge / serverless (sub-100ms)** | **imprint-pdf** (`@imprint-pdf/react`) if React + edge | HarfBuzz + Knuth-Plass without browser, but needs React wiring — you choose when edge matters |

All ship: `scripts/generate_pdf.py` is the router (auto-detects Playwright/Typst/WeasyPrint per `references/engine-matrix.md`). Install once: `pip install -r ${CLAUDE_SKILL_DIR}/requirements.txt` + `npm install` (for Playwright) or `brew install typst` (for academic).

---

## Core Workflow — Taste-Driven, Unbound

Each step ends on a completion criterion. Do not proceed until it passes.

### 1. Triage — What Is This Document *For*?

Ask or infer: audience, outcome, and action after page N. Extract: length hint (1-pager vs 200-page report), density (sparse pitch vs dense report), cover need (does it earn a full-bleed image?), and one banned invention (the dataset you will not hallucinate). Detect format: `slides` (16:9 1920×1080) vs `documents` (A4) — you choose per `pdf-forge` catalog.

Completion: one intent sentence + format + page-range + banned invention.

### 2. Budget — How Many Words Fit One Page?

Before writing, call `estimate_page_budget` (from beautiful-pdf-mcp): for chosen template (`report` A4 `Source Serif 4` vs `book` A5 vs `resume` two-col), get `words_per_page` / `lines_per_page`. Write *to size* — not trimmed after. For HTML+Tailwind, budget as `~550–650 words per A4` (dense body 1.45) or `~350` (sparse editorial) — see `references/design-taste.md` budgets.

Completion: per-template budget number written down; outline respects it (no 2000-word one-pager).

### 3. Route — You Pick Taste + Cover + Engine

For the whole doc, decide:
- **Taste:** zinc vs parchment, accent derived from semantics (not default). A warm academic report → terracotta `#9C6B4F` on cream; a fintech report → zinc `900` + ink-blue; a portfolio → near-black + Fraunces glow. Change `accent` → recolor rules/callouts/table headers everywhere. See `design-taste.md` accent guidance.
- **Cover pattern:** `fullbleed` (dark, dot grid, image), `split` (left panel + geometric), `typographic` (oversized word), `minimal` (white + 8px bar), `frame` (inset border), `editorial` (ghost letter), `stripe`/`diagonal`/`atmospheric` — from minimax’s 15. Never reuse the same cover twice in a row across docs without reason.
- **Engine:** per table above.

Completion: `taste: zinc+terracotta + tracking-display/heading/body + spacing scale` + `cover: minimal + accent #9C6B4F` + `engine: HTML+Tailwind+Playwright` — all justified in one line about content.

### 4. Compose — HTML That Is Valid Paged Media

Build self-contained HTML per `references/engine-matrix.md` recipe:

- **No component library.** Flat DOM, Tailwind CDN (`<script src="https://cdn.tailwindcss.com">` or compiled CSS via Oxide), semantic tracking classes, geometric spacing.
- **Paged headers/footers via CSS:** `@page { size: A4; margin: 20mm 15mm; @top-center { content: counter(page) } }`, `position: running(header)` for chapter-aware running heads, `target-counter` for cross-refs.
- **Cover = full bleed:** `body { margin: 0 }`, `@page :first { margin: 0 }`, `.cover { width: 210mm; height: 297mm }` — white-border cover is a taste fail.
- **Blocks:** `h1` (accent rule) → `h2` → `body` (justified with hyphenation, `hyphens: auto; text-wrap: pretty`) → `callout` (accent bar) → `table` (three-line, 1px top/bottom + header rule) → `chart` (SVG via Chart.js/Recharts, vector) → `figure` (image + `Figure N` caption) — never screenshot a table.

Reference: `references/design-taste.md` for the HTML boilerplate.

Completion: HTML opens in Chromium as print preview with no console errors, cover bleeds edge-to-edge, and `@page` margins match tokens.

### 5. Render — Playwright + Paged.js (Polyfill Injected)

Use the bundled renderer — it orchestrates Playwright correctly:

```bash
# skills.sh:
node ${CLAUDE_SKILL_DIR}/scripts/render_pdf.mjs --html ${CLAUDE_SKILL_DIR}/templates/report.html --out ./report.pdf
# or Python router (auto):
python ${CLAUDE_SKILL_DIR}/scripts/generate_pdf.py --html ./build/report.html --out ./report.pdf
# local clone:
python nextreme-pdf/scripts/generate_pdf.py --html ./build/report.html --out ./report.pdf
```

It: resolves Chromium via `browser_helper.js` (or `npx playwright install chromium`), launches with `playwright.chromium`, injects `paged.polyfill.js` (do **not** load Paged.js in source HTML — it corrupts layout), waits for `delay` (Mermaid/KaTeX), checks `counter-reset` conflict, then `page.pdf({ format: "A4", printBackground: true })`. See `references/engine-matrix.md` for the full Playwright flow.

Completion: `render_pdf.mjs` exits 0, PDF page count matches budget ±1, and first page is the cover (no blank).

### 6. QC — Per-Page Fill + Visual (Page-as-Canvas)

Beautiful-pdf-mcp’s QC is law: after render, the validator returns per-page `layout_report` (fill %, holes, defects). Every page but the last must be **filled to the bottom** (carryover mid-sentence, even mid-hyphen, is correct; a hole mid-article is a defect). Then `compile_preview` (PNG per page via `pdf2image`/`pdftoppm`) for visual check.

```bash
python ${CLAUDE_SKILL_DIR}/scripts/validate_pdf.py ./report.pdf --strict
# checks: valid PDF header, page count vs budget, overflow (img/table > page width), anomalous blank pages, rivers (word gaps), orphan/widow via line count, cover bleed
```

If a page is 6 lines short → add ~40 words arithmetically (not guesswork). If an image stranded → two-pass `after:N` placement. `strict_layout: true` refuses to ship a defective PDF.

Reference: `references/validation.md`.

Completion: `validate_pdf.py --strict` exits 0, every page but last is a clean block, no image tears the layout.

### 7. Iterate — Fix the Source, Not the Artifact

If QC fails, fix the HTML source (tokens, block order, image `after:N`), not the PDF bytes. Re-render and re-QC until clean — the loop is the craft.

Completion: two consecutive QC passes with 0 new issues.

### 8. Deliver

Always:
1. **The PDF** — print-ready, valid `%PDF`, tagged where needed.
2. **The HTML source** — so they can re-render or restyle without you.
3. **Layout proof** — `validate_pdf.py` log + PNG previews of pages 1–3 (cover, dense, sparse) as taste evidence.

---

## Document-Type Quick Picks

Copy a template from `templates/` and fill; do not start from zero. Each is valid HTML with Tailwind tokens and proper `@page`.

| Need | Template | Why this taste |
|---|---|---|
| Business report (7–12p) | `report.html` | Dark `report` fullbleed cover (dot grid, Playfair), zinc body, three-line tables, chart vectors |
| Proposal (6–10p) | `proposal.html` | `split` cover (Syne), problem→solution, pricing table, signature |
| Resume (1–2p strict) | `resume.html` | `typographic` cover (oversized word, DM Serif), auto-fit to 1 page, two-col on A4 |
| Portfolio (6–10p) | `portfolio.html` | `atmospheric` near-black + radial glow, Fraunces, meander spreads (diagonal photos + threading text) |
| Magazine / editorial (6p) | `magazine.html` | Warm cream `Lora + Cormorant`, meander threading, pull quotes |
| Letter | `letter.html` | Single page, parchment optional, letterhead running header |
| Minimal handout | `minimal.html` | White + 8px accent bar (Cormant Garamond), single accent moment |

All templates are A4, zinc or parchment per doc semantics, vector charts (no screenshots). See `references/document-types.md`.

---

## Troubleshooting (Taste Fail vs Glue Fix)

| Taste fail | Cause | Fix |
|---|---|---|
| Cover has white border | Missing `@page :first { margin: 0 }` or `body { margin: 0 }` | Add both; `.cover` must be `210mm×297mm` |
| Positive tracking | Used `tracking-wider` (positive) | Use semantic tokens: `tracking-display -0.10em` etc. |
| Random accent per page | Chose `accent_lt` for every `h2` | One accent per spread — only `h1` rule / callout bar |
| `rgba` tag double-rect | Tag bg `rgba(0,0,0,0.04)` | Solid hex (`#f4f4f5`), WeasyPrint bug |
| Hard shadow | `shadow-lg` | `ring-1 ring-black/5` or `shadow-sm` whisper |
| Rivers (gappy justify) | `text-justify: inter-word` without hyphenation | `hyphens: auto; text-wrap: pretty;` + `hyphenate-limit-chars: 6 3 2` |
| Table spills | No `max-width: 100%` or pre/table/img > page | `pre, table, img { max-width: 100% }` |
| Blank anomalous page | `page-break-after: always` left behind | Remove; Paged.js handles pagination |
| Chart as raster | Pasted PNG screenshot | Use SVG (Recharts/Visx) or `ChartData` → native vector |
| PDF valid but taste flat | Used default palette + Inter everywhere | Derive accent from semantics (see `design-taste.md` — terracotta for warm academic, Nord Frost for Nordic, ink-wash for素雅) |

---

## Reference Files

- `references/design-taste.md` — the taste system: zinc vs parchment, tracking, spacing, one-accent law, 10 palettes (terracotta, Nord, ink-wash, etc.), cover patterns, line-height law.
- `references/engine-matrix.md` — 4 engines (HTML+Tailwind+Playwright/Paged.js, Typst page-as-canvas, WeasyPrint, imprint edge), install and Playwright flow.
- `references/document-types.md` — 7+ doc types, budgets, required blocks, bento-like layout rhythm for docs.
- `references/validation.md` — per-page fill QC, overflow, rivers, orphan/widow, cover-bleed, layout_report gate.
- `scripts/generate_pdf.py` — HTML→PDF router (HTML → Playwright/Paged.js → PDF; Typst/WeasyPrint fallback).
- `scripts/render_pdf.mjs` — HTML→PDF via Playwright (Chromium resolve, Paged.js polyfill, wait for Mermaid/KaTeX).
- `scripts/validate_pdf.py` — PDF QC (page count vs budget, overflow, blank pages, cover bleed, %PDF header).
- `templates/` — `report.html`, `proposal.html`, `resume.html`, `portfolio.html`, `magazine.html`, `letter.html`, `minimal.html` — all taste-driven.

---

## Principles (Taste Is Law, But Not Prison)

- **Taste is derived, not random.** Every palette/type/spacing choice ties to one sentence about content. “Why terracotta?” is answered.
- **Page as canvas.** A document that leaves a hole mid-article is unfinished. Fill to the bottom, carryover cleanly, re-place images in two passes.
- **One accent, one moment.** Restraint is the flex. Gradient once, zinc the rest.
- **Negative tracking or not at all.** Positive tracking is the AI marker — never use it.
- **Raw HTML over component bloat.** Flat DOM + Tailwind tokens is predictable for Playwright; component stacks drift.
- **Validate the render, not the intent.** The PDF is the truth; the HTML is the source. Fix the source until the per-page fill is clean.
