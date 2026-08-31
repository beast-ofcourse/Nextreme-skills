# Engine Matrix — 4 Engines, You Choose

## 1. Decision Flow — Content Drives Engine

```
Need PDF
├─ Long-form / GOST / book (strict per-page QC, two-pass images)?
│  └─ typst on PATH? → Typst (page-as-canvas, layout_report)
├─ Need sub-100ms edge / no Chromium (Vercel Edge / CF Workers)?
│  └─ imprint-pdf (@imprint-pdf/react) — real Tailwind, no browser
├─ Need tagged PDF / print-native fallback without Chromium?
│  └─ WeasyPrint (paged media, PDF/UA)
└─ Default (best taste) → HTML + Tailwind + Playwright + Paged.js
     (Vercel/Stripe aesthetics, zinc backbone, CSS Grid, @page control)
```

You must justify the pick in one line about content.

---

## 2. HTML + Tailwind + Playwright + Paged.js (Default — Best Taste)

**What:** Static HTML + Tailwind CDN (or compiled Oxide), no React build, no component lib — flat DOM, geometric spacing, semantic tracking. Rendered via Playwright (`chromium`) + Paged.js polyfill for paged media (`@page`, `running()`, `target-counter`, `counter(page)`).

**Why default:** Only engine that gives full Tailwind + Grid + `@page` + print background + `target-counter` cross-refs with what-you-see-is-what-prints fidelity. What pdf-forge/Kami ship.

**Install:**

```bash
# Node + Playwright
npm install -D playwright
npx playwright install chromium
# Tailwind CDN needs internet; for offline:
npx tailwindcss -i ./src/input.css -o ./dist/tailwind.css
# Paged.js — do NOT include in source HTML; renderer injects paged.polyfill.js
```

**HTML contract (from Kami’s HTML Route):**

```html
<body style="margin:0"> <!-- mandatory: removes 8px browser margin -->
<style>
  @page { size: A4; margin: 20mm 15mm }
  @page :first { margin: 0 } /* cover full-bleed */
  .cover { width: 210mm; height: 297mm } /* exactly A4 when :first is 0 */
  pre, table, img { max-width: 100% } /* overflow guard */
</style>
```

**Renderer — `scripts/render_pdf.mjs` does it right:**

```js
// 1. Resolve Chromium (browser_helper.js: looks for system Chromium / Playwright cache)
// 2. Launch with error handling for missing libs (html_to_pdf.js 139-176)
// 3. page.setContent(html, { waitUntil: "networkidle" })
// 4. Inject paged.polyfill.js (html_to_pdf.js) — must not be in source
// 5. Wait delay (for Mermaid/KaTeX rendering)
// 6. Check counter-reset conflict (P paged.js 192-208)
// 7. page.pdf({ format: "A4", printBackground: true, preferCSSPageSize: true })
```

**Node entry — `scripts/render_pdf.mjs`:**

```bash
node ${CLAUDE_SKILL_DIR}/scripts/render_pdf.mjs --html ./build/report.html --out ./report.pdf --format A4
# local:
node nextreme-pdf/scripts/render_pdf.mjs --html ./build/report.html --out ./report.pdf
```

**Python router — `scripts/generate_pdf.py` (auto-detects engine):**

```bash
python ${CLAUDE_SKILL_DIR}/scripts/generate_pdf.py --html ./build/report.html --out ./report.pdf
# auto: Playwright if chromium available, else WeasyPrint, else Typst if --typst flag
```

**Full-bleed cover checklist (mandatory):**
- `body { margin: 0 }`
- `@page :first { margin: 0 }`
- `.cover { width: 210mm; height: 297mm; background: #... }`
- Missing any → white border = taste fail.

**Mermaid / KaTeX:**
- Mermaid: `theme: 'neutral'` for professional PDF, rendered as static SVG in Chromium before capture.
- KaTeX: LaTeX math via `katex` CDN, rendered before print.

**Overflow guards (from Kami HTML Route checks):**
- `table`, `pre`, `img` with `max-width: 100%`
- Flag blank/extremely low-content pages (check `page-break-after: always` misuse)
- Figure/table stats vs requirements.

---

## 3. Typst (Page-as-Canvas — Long-Form)

**What:** `typst compile` with templates `report`, `academic_ru`, `book`, `journal`, `resume` — each declares a page contract (`data/styles.json`: fill thresholds, tolerated underfill).

**When:** 20+ page report, GOST 7.32 (sections on fresh pages, figures after first mention, full-width tables caption-above), auto-fit single-page (resume stretches type until sheet full), meander spreads (diagonal photos + threading text via `meander`/`wrap-it`).

**Flow (beautiful-pdf-mcp):**

```bash
brew install typst  # or cargo install typst-cli
# 1. Budget
python -m beautiful_pdf_mcp estimate_page_budget --template journal --language en
# → words_per_page, lines_per_page

# 2. Create + add sections (JSON state)
doc = create_document(template="journal", language="en", preset_overrides={accent_color:"#1B365D"})
add_section(doc_id, "# Title", "Body to budget…")
add_image(doc_id, position="auto", width="column")  # two-pass: pass1 marks paragraph positions, pass2 anchors after:N
add_table(doc_id, headers=[...], rows=[...])

# 3. Preview (PNG per page + layout_report)
compile_preview(doc_id, pages="1-3")  # → PNG + {fill %, holes, defects}

# 4. Ship
compile_pdf(doc_id, "out.pdf", strict_layout=True)  # fails on hole mid-article
```

**Two-pass image:** Pass1 renders with invisible `typst query` marks, server asks where each paragraph landed, computes `after:N` anchors for `position:"auto"` images, Pass2 recompiles. No torn layout.

**Per-page QC (`src/layout_qc.py`):** Grades each page vs contract — e.g., `page 3: 6 lines short, add ~40 words` — so agent fixes arithmetically.

---

## 4. WeasyPrint (Print-Native Fallback)

**What:** `weasyprint` binary — paged media without Chromium. Light, print-CSS faithful, tagged PDF, no 300 MB browser.

**When:** Playwright unavailable (locked-down CI, no Node), or need `PDF/UA-1` tagged without Typst.

```bash
pip install weasyprint
weasyprint ./build/report.html ./report.pdf
# or via router:
python ${CLAUDE_SKILL_DIR}/scripts/generate_pdf.py --html ./build/report.html --out ./report.pdf --engine weasyprint
```

**Trade-off:** No CSS Grid animation fidelity, limited `target-counter` cross-refs, but correct `@page` and print background.

---

## 5. imprint-pdf (Edge — React + Tailwind Without Chromium)

**What:** `@imprint-pdf/react` — React reconciler → PdfNode IR → Tailwind Oxide resolver → Taffy (WASM Grid/Flex) + HarfBuzz + Knuth–Plass → `pdf-lib` writer. Sub-100ms edge cold, CSS Grid, variable fonts, PDF/X-4 + CMYK.

**When:** Vercel Edge / Cloudflare Workers, or you already are React.

```bash
pnpm add @imprint-pdf/react @imprint-pdf/core tailwindcss
npx imprint init  # wires Next.js/Vite plugin, scaffolds template+route
```

```tsx
import { pdf, Document, Page } from '@imprint-pdf/react';
export const GET = () => pdf(<Document><Page size="A4" className="p-12"><h1 className="text-3xl tracking-tight">Hello</h1></Page></Document>);
```

---

## 6. How to Choose — Honest

| Criterion | HTML+Playwright | Typst | WeasyPrint | imprint |
|---|---|---|---|---|
| Tailwind CDN | Full | No | Partial | Full (Oxide) |
| Grid | Yes | Yes (via meander) | Yes | Yes (Taffy) |
| HarfBuzz / Knuth-Plass | Chromium’s | Typst’s (best) | Pango | HarfBuzz |
| Page budget + two-pass images | No (heuristic) | Yes (contract) | No | No |
| Edge sub-100ms | No (browser 300 MB) | No | Yes | Yes |
| Tagged PDF | Via printBackground | No | Yes | Yes (PDF/UA-1) |
| Install | Node+Playwright | typst | pip | npm |
| Best for | Most PDFs, best taste | Long-form / GOST | Light fallback | Edge React |

If two tie, default to **HTML+Playwright** — broadest taste fidelity and what the skill’s templates are authored for.

---

## 7. Anti-Pitfalls (All Engines)

| Symptom | Cause | Fix |
|---|---|---|
| White border on cover | Missing `@page :first { margin: 0 }` or `body { margin: 0 }` | Add both |
| `rgba` tag double-rect | Tag bg `rgba` | Solid hex |
| Table spills | No `max-width: 100%` | `pre, table, img { max-width: 100% }` |
| `counter-reset` conflict | Custom `counter-reset` in CSS | Remove — Paged.js owns counters |
| Blank page | Accidental `page-break-after: always` | Remove, let Paged.js paginate |
| Paged.js corrupt layout | Loaded `paged.polyfill.js` in source HTML | Remove — renderer injects it |
