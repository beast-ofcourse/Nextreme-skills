# Design Taste — The Expensive PDF System

This is the taste that makes a PDF feel like it cost $1,000/page — not $0.00 from a prompt. Copy these tokens verbatim; do not invent.

## 1. Canvas — Zinc vs Parchment (Pick Per Story)

| Canvas | Hex | When | Body Text | Neutrals |
|---|---|---|---|---|
| **Zinc** (default) | `zinc-50 #fafafa` bg, `zinc-900 #18181b` ink | Tech, fintech, report, proposal — any document where trust = precision | `zinc-900` | Warm? No — zinc is neutral but you warm it with tracking/spacing, not hue |
| **Parchment** | `#f5f4ed` | Human, literary, heritage, editorial, portfolio — warm story | ink-blue `#1B365D` | All neutrals warm-toned: `zinc` → `stone` mix, never cold `#6b7280` |

**Rule:** Never pure white `#fff` as body bg (too sterile). Parchment gets `Newsreader` serif for headlines+body; zinc gets `Inter`/`Newsreader` mix (sans for UI, serif for authority).

**Depth:** `ring-1 ring-black/[0.04]` or `shadow-sm` whisper (`0 1px 2px rgba(0,0,0,0.04)`) — never hard `shadow-lg`.

---

## 2. Palettes — Content-Driven, Not Template-Driven (10 Presets)

Derive accent from semantics, then derive `accent_lt` by lightening toward white (or `accent_dark` toward ink). One accent per spread.

| Palette | Accent | Bg Tint | Best For | Cover Pattern |
|---|---|---|---|---|
| **Ink Blue** (default) | `#1B365D` | `zinc-50` | Corporate, trust | `report` fullbleed (dot grid, Playfair) |
| **Terracotta** | `#9C6B4F` | `#fdf6f0` (cream) | Warm academic, heritage | `report` terracotta on cream |
| **Nord Frost** | `#4A6741` → `nord` `blue-gray #4A5A6B` | `nord-50 #f2f4f8` | Nordic, clean tech | `minimal` Nord |
| **Ink Wash** | `#2d2d2d` (pure gray-black) | `#f9f9f7` | Ink-wash 素雅,素雅 | `inkwash` (single gray) |
| **Chinese Red** | `#9e2b25` | `#fff7ed` warm paper | 中式正式, Chinese formal | `frame` red |
| **Tufte** | `#b91c1c` (deep red point) on `zinc-50` | `zinc-50` | Tufte minimal,留白 | `tufte` (red dot) |
| **Ocean Breeze** | `#0891b2` teal | `#ecfeff` | Fresh, natural | `stripe` teal |
| **GitHub Light** | `#0969da` blue | `white` | Developer | `github` blue-white |
| **Warm Academic** | `#9C6B4F` terracotta | `#fdf6f0` | Thesis, paper | `classic-thesis` |
| **Editorial** | `#E11D48` rose | `#fff1f2` cream | Magazine | `editorial` ghost letter |

**Accent law:** Choose by industry/purpose/audience — not by “safe” default. Muted, desaturated tones win; vivid primaries fail. When in doubt, go darker/neutral. See `minimax-pdf` palette.py guidance.

---

## 3. Typography — The Expensive Stack

**Stacks:**

| Role | Zinc Deck | Parchment Deck | Fallback |
|---|---|---|---|
| **Display / Cover** | `Newsreader` serif 800 | `TsangerJinKai02` / `Noto Serif CJK SC` + `Newsreader` | `Charter` / `Georgia` |
| **Heading / Body** | `Inter` sans 400 + `Newsreader` serif 500 (mix) | `TsangerJinKai02` headlines (500) + `Source Han Sans` body | `Helvetica Neue` / `Arial` |
| **UI / Caption** | `Inter` | `Inter` | — |
| **Mono / Numbers** | `JetBrains Mono` | `JetBrains Mono` | `Consolas` / `Menlo` |

**Hard invariants (from Kami + pdf-forge):**
- Serif weight locked 500 (no bold heads).
- Line-heights: `display 1.1–1.3`, `dense body 1.4–1.45`, `reading body 1.5–1.55` — **never 1.6+**.
- Tracking **all negative**: `display -0.10em`, `heading -0.06em`, `body -0.025em`, `label -0.01em`. Positive tracking = AI marker.

**Tags / Chips:** `solid hex` only (e.g., `bg-zinc-900 text-white`). `rgba()` triggers WeasyPrint double-rect bug.

**Justification:** `text-align: justify; hyphens: auto; text-wrap: pretty; hyphenate-limit-chars: 6 3 2;` + aggressive Knuth–Plass costs (via Typst/imprint when available) so no rivers.

---

## 4. Spacing — Geometric (No Arbitrary)

`4, 8, 12, 16, 24, 32, 48, 64, 80, 96` and only these. A 20px gap is a taste failure. `12` = `0.75rem`, `16` = `1rem`, `24` = `1.5rem` etc. In HTML: `p-4`, `gap-6`, `mt-12`, `py-24` — always from this scale.

---

## 5. Covers — 7 Patterns You Must Know (From Minimax 15, Distilled)

| Pattern | Geometry | Typeface | When |
|---|---|---|---|
| `fullbleed` | Dark bg, edge-to-edge image or dot grid, no white border (`@page :first { margin: 0 }`) | `Playfair Display` | Report (trust) |
| `split` | Left panel (title) + right geometric (SVG cut) | `Syne` | Proposal |
| `typographic` | Oversized first word (display 800, tracking-display), rest small | `DM Serif Display` | Resume |
| `minimal` | White + single 8px accent bar top | `Cormorant Garamond` | Handout |
| `frame` | Inset border `inset 16px`, corner ornaments | `Cormorant` | Certificate / formal |
| `editorial` | Ghost letter (200pt, `text-zinc-100`, behind title) | `Bebas Neue` | Magazine |
| `stripe` / `diagonal` | 3 horizontal bands or SVG angled cut | `Barlow Condensed` / `Montserrat` | Modern / poster |
| `atmospheric` | Near-black + radial glow, grayscale image | `Fraunces` | Portfolio |

**One accent, one moment:** Cover accent appears only on the hero element (title, rule, or glow) — not on every line.

---

## 6. Body Blocks — Tailwind Primitives (From Minimax + Forge)

- `h1` (accent rule `w-12 h-1 bg-accent` above title, `tracking-heading`),
- `h2` (`text-lg font-semibold tracking-heading`),
- `body` (justified, `leading-[1.55] tracking-body`, supports `<strong>` + `<em>`),
- `bullet` (• with `pl-6`, custom `::marker` color `accent`),
- `callout` (`border-l-4 border-accent bg-zinc-50 p-4`),
- `table` (three-line: `border-t border-b border-zinc-900`, header `uppercase tracking-label text-xs`, row `border-b border-zinc-100`),
- `figure` (`max-width: 100%`, `Figure N:` caption `text-xs text-zinc-500 tracking-label`),
- `chart` (Recharts SVG, vector), `divider` (`hr border-zinc-200`), `pagebreak` (`break-after: page`).

---

## 7. HTML Boilerplate — Self-Contained, Paged.js-Ready

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Newsreader:opsz,wght@6..72,500;600&display=swap" rel="stylesheet">
<style>
  @page { size: A4; margin: 20mm 15mm; @top-center { content: counter(page) " / " counter(pages); font-size: 8pt; color: #71717a } }
  @page :first { margin: 0 } /* full-bleed cover, no white border */
  body { margin: 0; font-family: Inter, system-ui, sans-serif; color: #18181b; line-height: 1.55; letter-spacing: -0.025em; }
  h1 { font-family: Newsreader, Georgia, serif; font-weight: 500; font-size: 22pt; letter-spacing: -0.06em; line-height: 1.25 }
  pre, table, img { max-width: 100% }
</style>
</head>
<body class="bg-zinc-50">
  <section class="cover" style="width:210mm; height:297mm; background:#1B365D; color:white; display:flex; align-items:center; justify-content:center;">
    <h1 class="text-5xl font-extrabold" style="letter-spacing:-0.10em">Cover Title</h1>
  </section>
  <main class="p-12">
    <div class="h-1 w-12 bg-[#1B365D] mb-4"></div>
    <h1>Section</h1>
    <p class="text-justify" style="hyphens:auto; text-wrap:pretty">Body…</p>
  </main>
</body>
</html>
```

Do **not** load `paged.polyfill.js` in source — `render_pdf.mjs` injects it.

---

## 8. Budgets — Write To Size (Per-Template)

| Template | Page | Words/Page | When |
|---|---|---|---|
| `report` | A4, Source Serif 4, 11pt, 1.55 | 550–650 | Business report |
| `book` | A5, PT Serif | 300–350 | Fiction/non-fiction |
| `letter` | A4, Source Sans 3 | 400 | Single page |
| `resume` | A4 two-col | 350 | Auto-fit: scale up until sheet full (no hole) |
| `magazine` | A4, Lora + Cormorant | 500 | Editorial, meander spreads |

Call `estimate_page_budget` (Typst) or use heuristic above before writing.
