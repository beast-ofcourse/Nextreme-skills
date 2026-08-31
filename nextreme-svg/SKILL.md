---
name: nextreme-svg
description: >
  Create, optimize, animate, and restyle publication-grade SVG graphics — icons, logos, illustrations, diagrams, charts, patterns, and text art — with spec-correct W3C SVG 2, five-zone lighting, and geometry-validated layout. Outputs standalone .svg, HTML inline, React JSX, or Vue SFC as native vector. This is THE extreme skill for ANY SVG — distinct from PPTX (slides), PDF (paged docs), or PNG (raster). Trigger whenever the user asks for svg, SVG, icon, logo, illustration, diagram, chart, pattern, gradient, filter, mask, path, or “make it vector” — even vague “draw this” or “make a logo” without naming SVG. Also trigger for “optimize this SVG”, “animate this icon”, “restyle this illustration”. Do NOT trigger for raster JPG/PNG alone, PowerPoint, or Word.
license: MIT
compatibility: python>=3.9
---

# Nextreme SVG — The Extreme Vector Engine

This skill produces **spec-correct, illustration-grade, diagram-true SVGs** that survive anywhere: GitHub, Figma, browsers, email, and untrusted renders — no `<foreignObject>`, no JS, no external fonts, no raster fallback. Every output is valid W3C SVG 2 with measured viewBox, presentation-attributes (not CSS-in-markup), `SMIL`-only animation, and per-file QC. You get three deliverables: the **.svg** (or inline/React/Vue), the **2× PNG preview**, and the **validation proof**.

You are **unbound but spec-driven** — the user does not pick the domain or the format — **you do**, per content. A data story gets a chart with `viewBox` math; a mascot gets five-zone lighting with `feGaussianBlur` shadows; a system diagram gets a layered grid with `validate_svg.py` proofs. If they hand you a flat 2-stop gradient, you make it a 6-stop hue-shift; if they hand you a 20-node architecture note, you make it a layered diagram with routes, not a pile of boxes.

---

## Why This Is Not Generic

Most SVG skills are bounded: one domain (icons *or* diagrams), one format (`.svg` *or* React), one shot (no loop) — so every output looks like that tool. Generic “draw SVG” prompts are spec-blind: they miss `viewBox`/`preserveAspectRatio`, they use flat 2-stop gradients, pure-black shadows, `<text>` without `textPath`, and `width`/`height` without `viewBox` (breaks responsive). Overlay-chart skills paste a PNG inside an SVG and call it vector.

This fuses the very core of the 4 best SVG systems on GitHub (2026) and refuses their bounds.

| Generic | This skill |
|---|---|
| Flat 2-stop gradients, pure-black shadows, single `stroke` | 4–8 stops hue-shift, five-zone lighting, colored shadows (dark blue/purple/teal) + noise grain |
| One shot, no visual check | **Render-verify-fix loop** (2–8 iterations: SVG → PNG via CairoSVG/librsvg → AI sees → fixes) |
| Overlaps, text overflow, arrows through boxes | **5-step plan + layered order** (`background → containers → nodes → labels → connections` last) + 14 structural checks |
| CSS in markup, `<script>`, `javascript:` URLs, external fonts | **Spec-correct, CSS-independent**: presentation attrs + SMIL only, `role="img"` + `<title>`/`<desc>`, `aria-hidden` for decorative, `prefers-reduced-motion` |

> If the content wants a better path that no reference names (e.g., a meander thread inside a diagram), invent it — but keep it `viewBox`-driven, spec-valid, and `validate_svg.py` clean.

---

## Golden Code Quality Rules — ENFORCED

These are non-negotiable. Every SVG and every script this skill ships must pass them. Violation = task fails.

Keep code human-readable, small, and obvious. No AI slop.

* **Names tell the truth** — variables/functions reveal intent. No `data`, `info`, `result`, `handler`, `manager`, `helper`, `utils`, `foo`.
* **One job per unit** — if you need "and" to describe what a function does, split it. Files own one domain.
* **Guard clauses over nesting** — early returns, fail fast. No pyramids, no `else` after `return`. Nesting past 2–3 levels is a signal to restructure.
* **No duplication** — never copy-paste. Third occurrence of the same logic = must abstract. Two is coincidence, not a pattern.
* **No dead weight** — zero dead code, commented-out code, `console.log`, unused imports. Delete, don't comment out.
* **Types are contracts** — no `any`, no silent `as` casts, narrow `unknown` explicitly. At an untyped boundary (`JSON.parse`, third-party API), a cast is allowed only alongside visible runtime validation.
* **Errors never silent** — every failure path is handled, returned, or logged with context. Never an empty catch, never a swallowed promise.
* **No magic** — no unexplained numbers or strings. Name every constant. No cryptic one-liners.
* **Explicit dependencies** — no hidden globals, no surprise side effects. Inputs in, outputs out. Pure where possible.
* **Readability > cleverness** — code reads like prose: linear flow, consistent style, self-documenting. Comments explain why, not what.
* **No premature abstraction** — no wrappers, layers, or helpers you don't need today. YAGNI. Abstract on the real second pattern.
* **Leave it cleaner, not bigger** — boy-scout only on touched code.
* **State assumptions, don't guess silently** — if the spec is ambiguous, say what you assumed and why, in a comment or PR note.

**Auto-rejected AI slop:** placeholder `TODO` without a ticket, generic scaffolding, empty `try/catch`, `lorem`-ish names, duplicated boilerplate, over-engineered factories/managers, unvalidated `as` casts at boundaries, silent assumptions about ambiguous specs, inconsistent style within one file, **and SVG-level slop:** missing `viewBox`, `<foreignObject>`, `javascript:` URLs, external CSS/fonts, flat gradients, pure-black shadows, arrows through boxes, text overflow, missing `<title>`/`aria` on meaningful graphics, single-shot without loop.

---

## Format Selection — You Decide

| Context | You Pick | Why |
|---|---|---|
| **Most SVGs (default)** | **Standalone `.svg`** — `viewBox`, `preserveAspectRatio`, presentation attrs | Renders anywhere (GitHub, Figma, email), no JS, no external refs |
| **Web page needing animation** | **HTML + inline `<svg>` + CSS** (or `SMIL` for `<img>`-safe) | CSS `transform-box: fill-box` + `prefers-reduced-motion`; self-contained |
| **React / Next.js** | **React JSX** — `props` for `size`, `color`, `className` | Copy-paste component, no SVG runtime dep |
| **Vue** | **Vue SFC** — `<template>` + scoped styles | Same |
| **Diagram for docs + slides** | **.svg + 2× PNG** (PNG at 2× viewBox) | Crisp preview for social / docs, vector for PPTX |

All ship: `scripts/validate_svg.py` + `scripts/render_svg.py` + `requirements.txt`. You choose the format per content — state the one-line justification.

---

## Core Workflow — Spec-Correct, Taste-Driven

Each step ends on a **completion criterion**. Do not proceed until it passes.

### 1. Clarify — What Is This Graphic *For*?

Ask or infer: output type (icon, logo, illustration, diagram, chart, pattern, text art, or repair), audience, and where it will render (GitHub README vs Figma vs email). Extract: subject, action/pose, setting, style, mood. Use prompting tips: “an orange tabby cat doing tree pose yoga floating in deep space with nebula” beats “a cat in space” — but do not interrogate if you can infer sensible defaults.

Reference: `references/svg-spec.md` — output type → default `viewBox`/palette/a11y.

Completion criterion: output type is named (one of 7) and brief is specific (subject + style); no vague “make a logo” without palette/size.

### 2. Plan — Size to Text, Grid Before Drawing

Before writing any `<path>`, do the 5-step plan (from pkt-lab, now for all SVGs):

1. **Inventory** — list every element (nodes, labels, legends, textures)
2. **Grid** — pick `viewBox` and column/row grid (e.g., `0 0 1200 800` with 40px snap)
3. **Size-to-text** — measure every label’s approximate width (see `references/diagram-patterns.md` — `char × fontSize × 0.6` heuristic, or `typst query` if Typst on PATH)
4. **Route connections** — for diagrams/charts, route edges *before* drawing boxes so arrows never go through boxes/text
5. **Canvas size** — `viewBox` tightly fits content + 40px padding; no `width`/`height` without `viewBox`

Reference: `references/diagram-patterns.md` — the 5-step plan.

Completion criterion: inventory + grid (explicit `viewBox`) + size-to-text table (label → width) + routed connections — all written before first `<rect>`.

### 3. Design — Taste, Not Flat

Build with illustration taste, not defaults:

- **Gradients:** 4–8 stops with hue shifts (e.g., `#1B4F72 → #2E86AB → #A8DADC`), never flat 2-stop.
- **Five-zone lighting:** specular → light → half-tone → form shadow → reflected light (see `references/illustration-taste.md`).
- **Shadows:** colored (dark blue/purple/teal), `linearRGB`, never pure black; `feGaussianBlur` + `feOffset` chain.
- **Structure:** layered order `background → containers → nodes → labels → connections` (connections last, so arrows are never hidden behind boxes). Use stable `id` prefixes (`nxt-`).

Reference: `references/illustration-taste.md` — five-zone + filter chains.

Completion criterion: every fill is multi-stop or textured, every shadow is colored, every SVG has layered groups `#background, #containers, #nodes, #labels, #connections`.

### 4. Write — Spec-Correct Markup (No CSS-in-Markup)

Write clean, indented standalone SVG:

- **No `<foreignObject>`, no `<script>`, no event handlers, no `javascript:` URLs, no external CSS/fonts, no embedded raster, no `width`/`height` without `viewBox`.**
- **Styling:** presentation attributes (`fill`, `stroke`, `stroke-width`), not CSS classes. Animation: `SMIL` only (so it works in `<img>`), or CSS with `transform-box: fill-box` + `prefers-reduced-motion` for HTML inline.
- **Text:** `<text>` with `dominant-baseline`, `<tspan>`, `<textPath>` for curved, `aria` correct: `role="img"` + `<title>` + `<desc>` for meaningful, `aria-hidden="true"` for decorative. Multilingual via `lang`.
- **Paths:** full `d` BNF, smooth reflection (`S`, `T`), implicit lineto, arc flags — see `references/svg-spec.md`.

Reference: `references/svg-spec.md` — viewBox, paths, text, gradients, patterns, transforms, clipPath/mask, filters, stroke.

Completion criterion: SVG is well-formed XML, `viewBox` present, `xmlns="http://www.w3.org/2000/svg"` present, no banned tags/attrs.

### 5. Validate — Unzip Not Needed, But Prove

Run the bundled validator:

```bash
# skills.sh:
python ${CLAUDE_SKILL_DIR}/scripts/validate_svg.py icon.svg --strict
# local clone:
python nextreme-svg/scripts/validate_svg.py icon.svg --strict
# flags:
# --check-overlap  : fail on box overlaps, arrow-through-box
# --check-text     : fail on text overflow, viewBox mismatch
# --check-security : fail on javascript: URLs, external refs
```

It checks: XML well-formedness, ID resolution (`url(#id)` exists), `path` `d` sanity, `viewBox` vs `width`/`height`, security deny list (W3C/OWASP/DOMPurify), a11y, SMIL hijack.

Fix every error and rerun until clean. If code execution unavailable, use `references/validation.md` manual checklist.

Completion criterion: `validate_svg.py --strict` exits 0 (or manual checklist all checked).

### 6. Render-Verify-Fix Loop — See It Like a Human

The AI must *see* its output:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/render_svg.py icon.svg --out icon.png --scale 2
# or nextreme-svg/scripts/render_svg.py icon.svg --out icon.png --scale 2
```

Renders SVG → PNG via `CairoSVG` or `librsvg`/`cairosvg` (auto-detected), at 2× viewBox for crispness. Then visually inspect (or let Claude read the PNG): check misaligned joints (character), wrong proportions, flat colors, grid misalignment, rivers.

Iterate 2–8 times: icons 1–2, diagrams 2–3, scenes 3–5, characters 5–8. Each iteration fixes one class of issue.

Reference: `scripts/render_svg.py` — `render`, `status`, `reset`.

Completion criterion: PNG at 2× matches intent, no misaligned joint / flat gradient / overflow, `render_svg.py` shows iteration count and no new issue.

### 7. Animate / Restyle — Only If Content Wants It

- **Animate:** CSS `transform-box: fill-box` with correct `transform-origin`, or SMIL `<animate>` / `<animateTransform>` for self-contained. Always include `@media (prefers-reduced-motion: reduce) { * { animation: none } }`.
- **Restyle:** adjust `stop-color` hue, `feColorMatrix`, `feTurbulence` (`baseFrequency`, `numOctaves`) — never regenerate from scratch for a palette tweak.

Reference: `references/illustration-taste.md` — animation recipes + material simulation.

Completion criterion: animation is smooth at 60fps in preview PNG (no jank), reduced-motion respected; restyle changes palette without breaking layout.

### 8. Deliver — Vector + Preview + Proof

Always:
1. **The .svg** (or inline/React/Vue as requested) — spec-correct, editable, presentation-attrs.
2. **The 2× PNG** (when useful) — `* .png` at 2× viewBox, for docs/social.
3. **Validation log** — `validate_svg.py` output + PNG dimensions proof.

For markup repair, return the full corrected SVG, not a patch.

---

## Quick Picks — Starter Templates

Copy a template from `templates/` and fill; do not start from zero. Each is valid SVG with real content, not filler.

| Need | Template | Why this one |
|---|---|---|
| 24×24 icon | `icon.svg` — 24×24, `viewBox="0 0 24 24"`, `aria-hidden` option | Minimal, stroke 1.5, rounded caps |
| Brand logo | `logo.svg` — text + mark, `role="img"` + `<title>` | Presentation attrs, no CSS |
| Illustration / mascot | `illustration.svg` — five-zone, 6-stop gradient, noise | Character construction: thick rounded limbs + circle joints |
| Architecture diagram | `diagram.svg` — layered, 14 checks, `viewBox 1200×800` | `background→containers→nodes→labels→connections` |
| Chart | `chart.svg` — bar/line, native `<rect>` + `<path>`, legend | Vector, tabular-nums, no raster |
| Pattern | `pattern.svg` — `<pattern>` + `<linearGradient>` | Tileable, transformable |
| Spinner | `animation.svg` — SMIL `animateTransform` rotate | Self-contained, `prefers-reduced-motion` |
| Text art | `text.svg` — `<textPath>` on curve, `tspan` | Multilingual, `lang` |
| Filter showcase | `filter.svg` — `feGaussianBlur` + `feTurbulence` + `feColorMatrix` | Drop shadow, glow, grain |

All templates are `viewBox`-driven, `xmlns`-correct, accessibility-labeled. See `references/svg-spec.md` for the HTML boilerplate to copy for new docs.

---

## Troubleshooting — No Glitch Is “Weird — Ignore It”

| Glitch | Cause | Fix |
|---|---|---|
| Blurry on GitHub | Missing `viewBox` or `width`/`height` without `viewBox` | Set `viewBox="0 0 W H"` + `preserveAspectRatio="xMidYMid meet"` |
| Flat 2-stop gradient | Default `linearGradient` | 4–8 stops hue-shift + noise overlay (`feTurbulence` 0.015) |
| Pure-black shadow | `feDropShadow` default | Colored shadow: `flood-color="#1e3a5f"` + `color-interpolation-filters="linearRGB"` |
| Arrow through box | Routed after drawing | 5-step plan: route *before* drawing; `validate_svg.py --check-overlap` |
| Text overflow / clipped | No size-to-text | Measure label width (`char × 0.6 × fontSize`) before placing |
| `<foreignObject>` needed | Tried to embed HTML | Use `<text>` + `<tspan>` + `<textPath>` instead |
| Animation jank | `transform-origin` wrong | `transform-box: fill-box; transform-origin: 50% 50%` |
| “Works in browser, not email” | External CSS/font | Presentation attrs + SMIL only; inline `font-family` fallback |
| Validator: `javascript:` URL | `href="javascript:..."` | Remove handler, use `href="#id"` or `url(#id)` only |

---

## Reference Files

- `references/svg-spec.md` — 12 domains: viewBox, shapes, full `d` BNF, text/tspan/textPath, colors/fills, gradients, patterns, transforms, clipPath/mask, filters, stroke, markers.
- `references/illustration-taste.md` — five-zone lighting, multi-stop gradients, scene layering, character construction (thick rounded limbs + circle joints), animation recipes.
- `references/diagram-patterns.md` — 5-step plan, layered order, 14 structural checks, routing.
- `references/validation.md` — strict checklist: XML, IDs, path sanity, viewBox, security (no script/handlers), a11y, SMIL hijack.
- `scripts/validate_svg.py` — strict validator (XML well-formed, ID resolution, path `d`, viewBox, safety).
- `scripts/render_svg.py` — SVG → PNG at 2× via CairoSVG/librsvg, status/reset.
- `templates/` — 9 starters: `icon.svg`, `logo.svg`, `illustration.svg`, `diagram.svg`, `chart.svg`, `pattern.svg`, `animation.svg`, `text.svg`, `filter.svg`.

---

## Principles — The Nextreme Signature (Unbound, but Not Unruly)

- **You decide — but you justify.** Every domain/format choice ties to one line about content. “Why this viewBox?” is answered, not shrugged.
- **Spec-correct over pretty.** A prettier SVG that fails W3C is a failed SVG. If it can be presentation-attrs, it is.
- **Loop beats one-shot.** A deck without render-verify-fix will drift into flat gradients and misaligned joints the moment real content lands. Every SVG declares `viewBox`; validation + PNG proves it.
- **Layered is law.** `background → containers → nodes → labels → connections` is the contract that keeps arrows from hiding — hard-coded `z-index` breaks it.
- **Ghost the trivial.** If the task is a 20-line helper icon, ghost the full illustration loop — it was never that complex.
- **No glitch is minor.** One flat gradient / one pure-black shadow / one missing `viewBox` is a credibility leak. Zero is the bar.

<!--
  Nextreme brand signature — keep this shape when you fill the template:
  - Title is "Nextreme <Name> — The <Extreme> Engine" with three deliverables in the lead.
  - "Why This Is Not Generic" + comparison table + golden rules + engine table come before workflow.
  - Every workflow step ends on "Completion criterion:" (checkable, exhaustive).
  - "Quick Picks" + "Troubleshooting" + "Reference Files" + "Principles" in that order, same voice.
  Anyone opening a filled skill should think: "ah, the structure and the writing style — this is definitely Nextreme."
-->
