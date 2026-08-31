# Best SVG Generation Skills — Deep Research (2026-08-31)

**Question:** Which GitHub skills are best-in-class for SVG generation in 2026, what do they cover, and what should `nextreme-svg` borrow?

**Method:** Live web search (2026-08-31) + doc fetch on primary GitHub READMEs (stars, architecture, scripts, references), plus cross-check vs W3C SVG 2 spec coverage.

---

## 1. Executive Summary — Top 4 for Different Jobs

| Rank | Skill | Created | Focus | Engine | When to Pick |
|---|---|---|---|---|---|
| **1** | **Zacklinkk/svg-foundry-skill** | 2026-03-25 | **Knowledge-driven, 12 SVG domains** | Pure SVG spec (no renderer lock-in) + 127 refs | **Generalist #1** — icons, illustrations, charts, logos, animations from scratch, 4 output formats |
| **2** | **upbrew-tech/svg-creator-skill** | 2026-01-12 | **Illustration + character** | Rich gradients, five-zone lighting, render-verify-fix loop | **Character / scene / mascots** — the only one with human-illustrator loop (2–8 iterations) |
| **3** | **pkt-lab/svg-diagram** | 2026-03-19 | **Architecture/flow diagrams** | Closed loop: plan → layered SVG → validate_svg.py (14 checks) → render_svg.py → fix | **Technical diagrams for docs** — GitHub-safe, layered, no JS |
| **4** | **jawwadfirdousi/agent-skills svg-creator** | 2026-02-02 | **Spec-correct, safe, accessible** | W3C SVG 2, CSS-independent, SMIL-only, strict validator | **Production SVG that must be safe in untrusted contexts** (no external refs, no JS) |

If you must pick **one to fork for an extreme skill**, merge **(1)’s spec coverage** + **(2)’s render-verify-fix loop** + **(3)’s diagram discipline** + **(4)’s safety/accessibility** — no current skill does all four at once.

---

## 2. Full Field — 9 Skills Scanned

### Tier 1 — Spec Complete

**Zacklinkk/svg-foundry-skill** — https://github.com/Zacklinkk/svg-foundry-skill — 2026-03-25 — Apache 2.0 — site: zacklinkk.github.io/svg-foundry-skill

Knowledge-driven, not script-driven. 127 reference files across 6 topics (Essentials, Text Layout, Colors & Visuals, Animations, Web Integration, Modern Techniques) covering 12 SVG spec areas: canvas & viewBox, shapes, full path commands (M/L/H/V/C/S/Q/T/A/Z), text/tspan/textPath, colors/fills, gradients, patterns, transforms, clipPath/mask, filters (blur, shadow, colorMatrix, turbulence), stroke, markers.

4 capabilities: Create (icons/illustrations/charts/logos/animations), Optimize (performance/a11y/responsive), Animate (CSS/SMIL/stroke-drawing), Restyle (gradients/patterns/filters).

4 output formats: standalone `.svg`, HTML + inline SVG + CSS animations, React component (JSX props), Vue component (scoped). Trigger: `draw SVG, create SVG, SVG icon, SVG animation, SVG chart` or `/svg-craft`. 5-step workflow (clarify → design → animate → integrate → deliver) + accessibility-first (`<title>`, `aria-labelledby`, `prefers-reduced-motion`). MIT-like Apache 2.

**Why it leads:** Only skill that claims *full path* + *filters* + *textPath* + *modern techniques* in one knowledge base. No renderer lock-in — output is spec-correct SVG you can ship anywhere.

### Tier 1 — Illustration Loop

**upbrew-tech/svg-creator-skill** — https://github.com/upbrew-tech/svg-creator-skill — 2026-01-12 — Apache 2.0

An Agent Skill for production-quality SVG illustrations, characters & animations with a **render-verify-fix loop** (the AI actually sees its PNG and corrects).

Loop: Write SVG (encoded best practices: multi-stop gradients 4–8 stops with hue shifts, five-zone lighting specular→light→half-tone→form-shadow→reflected-light, colored shadows never pure black, noise texture, drop shadow filters via linearRGB) → Render to PNG (CairoSVG or Chromium, auto-detected) → Visually inspect (misaligned joints? flat colors? wrong proportions?) → Fix and re-render — iterates 2–8 times (icons 1–2, diagrams 2–3, scenes 3–5, characters 5–8).

Character construction: thick rounded `stroke-linecap="round"` limbs, circle joint covers after limbs, torso→legs→arms→head incremental, 8-head proportions (or large-head cartoon). Animation: CSS `transform-box: fill-box`, SMIL for self-contained `<img>`, `prefers-reduced-motion` always. Scene: back→front layering, atmospheric haze, ground shadows, vignette.

Skill structure: `SKILL.md` (~170 lines) + `references/advanced-techniques.md` (885 lines: filter chains, feTurbulence, materials glass/metal/fabric, atmospheric fog/rain/fire, animation recipes, data viz, patterns) + `scripts/svg_loop.py` (render/finish/status/reset) + examples.

Compatible with Claude.ai / Claude Code / Codex / Cursor / Windsurf etc. — agent-agnostic via agentskills.io.

### Tier 1 — Diagram Discipline

**pkt-lab/svg-diagram** — https://github.com/pkt-lab/svg-diagram — 2026-03-19 — MIT

Claude Code skill for clean, professional SVG architecture & flow diagrams — no ASCII art, no broken renders. Standalone `.svg` that renders on GitHub/GitLab/browser. Types: architecture, flowcharts, sequence, component, boot flow/pipeline, network topology, memory maps.

Closed-loop pipeline (the most disciplined for diagrams):
1. Plan layout (5-step: inventory → grid → size-to-text → route connections → canvas size) *before* writing SVG
2. Generate layered SVG (`<svg>` → `#background` → `#containers` → `#nodes` → `#labels` → `#connections` — connections last so arrows never hidden)
3. Structural `validate_svg.py` (14 checks: overlaps, text overflow, arrow-through-box/text, missing markers, tight spacing, viewBox mismatch, grid misalignment, layer violations)
4. Visual self-review (`render_svg.py` → PNG via librsvg+cairo, Claude reads image)
5. Fix loop until clean

GitHub-safe: no `<foreignObject>`, no JS, no external refs. Free color choice (just contrast + consistency). Trigger: natural `draw`/`visualize`/`diagram` or `/svg-diagram`.

### Tier 1 — Safe & Accessible

**jawwadfirdousi/agent-skills svg-creator** — https://github.com/jawwadfirdousi/agent-skills/tree/main/svg-creator — 2026-02-02 — MIT — 5 allowed-tools (`Write Read Bash`)

Creates/edits/validates/packages high-quality SVGs: icons, logos, illustrations, diagrams, charts, patterns, inline code. Auto-invokes on `make me an SVG of …`, `design a 24×24 icon`, `give me a logo`, `create a diagram`, `fix this SVG`.

Workflow: identify output type → pick defaults (viewBox/palette/a11y) → write clean standalone markup (valid XML, stable IDs, `role="img"`+`<title>`/`<desc>` or `aria-hidden`) → validate via `scripts/validate_svg.py` (XML well-formedness, ID resolution, path-data sanity, viewBox, safety) or manual checklist → retry until clean → return `.svg` or inline `<svg>` element.

Quality bar: `references/svg-quality-standard.md`, starter templates `references/svg-templates.md`, path guide `references/svg-path-guide.md` (BNF, smooth-curve reflection, arc parsing), security `references/svg-security.md` (W3C/OWASP/DOMPurify deny list: no `<script>`, handlers, `javascript:` URLs, external CSS/fonts, raster data, `foreignObject`), validation checklist. **No CSS in markup** — styled with presentation attributes, animated with SMIL only, so it renders same in any compliant viewer.

Examples: 9 production SVGs (static + animated). `examples/` + `agents/openai.yaml` for Codex.

### Tier 2 — Diagram / Animated

**qaz1230sp/ink-graph** — https://github.com/qaz1230sp/ink-graph — 2026-05-08 — MIT

Animated SVG technical diagrams from natural language. 11 themes (corporate to sci-fi HUD), 14 diagram types (architecture, flowchart, data-flow, sequence, dependency, mind-map, class, ER, state-machine, component, network-topology, timeline, comparison, use-case), CSS/SMIL animation (edge flow, hover glow, entrance, CRT flicker), zero JS (pure SVG+CSS), zero renderer lock-in, optional PNG via librsvg. `scripts/layout.py` auto-layout (Python 3.10+, Graphviz). Trigger: `npx skills add qaz1230sp/ink-graph`.

**ChanMeng666/svg-animation-studio** — https://github.com/ChanMeng666/svg-animation-studio

Composable SVG animation system via Claude Code. 4 skills (`/svg-animate`, `/svg-verify`, `/svg-add-primitive`, `/svg-export`) + 3 subagents (`svg-verifier`, `lib-extender`, `svg-explorer`) + 25 motion/shape/filter primitives (e.g., `motion.createJump`, `shapes.createPixelCharacter`). Every animation via named primitives → system compounds (Sprint 1: 4 presets + 25 primitives, 5th preset `purple-robot-jumping` from one sentence reusing 6 primitives). `svg-verifier` dirty-context visual grading, `lib-extender` restricted to `lib/primitives`, snapshot-tested (Vitest), Next.js preview, SVGO keep `viewBox/title/desc`. Discipline: `New primitives → /svg-add-primitive`, `New preset must reuse ≥1 primitive`.

**swogjs/skillstead svg-infographic** — https://github.com/swogjs/skillstead — Beta — Claude Code

Flat, structured SVG infographics + crisp 2× PNGs (PNG at 2× viewBox for share). Compute-first layout (layout computed numerically before drawing), source-controlled, Korean/CJK-safe, flat/struct. Types: architecture/cloud topology, technical infographics, before/after, process/data flows, roadmaps, 2×2 matrices, onion model, etc. 13 examples (SVG+2×PNG) checked for no text overflow, correct CJK, matching SVG/PNG dimensions, a11y metadata.

### Tier 2 — Guardrailed / Platform

**pq-dong/GenSvg** — https://github.com/pq-dong/GenSvg

Streaming JSONL → SVG via Vercel AI SDK, Zod guardrailed. Not skill-first: AI outputs JSON Patches (RFC 6902) conforming to a Catalog (available elements via Zod), not raw SVG strings — renderer converts JSON spec → SVG string/React component, streaming incremental. Phases: agentic iteration (patches), dynamic data binding, self-healing (feed validation error back), domain catalogs (`@svg-render/charts`), headless CLI.

**seeb4coding/SVG-ORA-Studio** — https://github.com/seeb4coding/svg-ora-studio — 2025-12-09 — React + TypeScript, browser-only, Google Gemini 3.0 + OpenRouter, canvas editor, layer controls, real-time refinement. Not skill-first; frontend platform with AI generation + refinement (change colors, strokes, clean paths).

---

## 3. What Makes a Skill “World-Class” for SVG in 2026

Extracted pattern:

1. **Knowledge as spec, not script:** 127 reference files (svg-foundry) or strict path BNF (jawwad) — AI guides via knowledge, not hardcoded snippets.
2. **Render-verify-fix loop:** upbrew (2–8 iterations, AI sees PNG) and pkt-lab (structural + visual) prove loop beats one-shot.
3. **Layered, spec-correct structure:** `background → containers → nodes → labels → connections` (pkt-lab) or `p:sp` containment (upbrew) ensures arrows never hidden.
4. **Safety + a11y by default:** No `<script>`/handlers, `role="img"` vs `aria-hidden`, `prefers-reduced-motion`, stable IDs.
5. **Output multiplicity:** Standalone `.svg` + HTML inline + React/Vue components (svg-foundry) or SVG + 2× PNG (skillstead) — ship where used.

---

## 4. Recommendation for `nextreme-svg` (the extreme skill to build)

**Positioning:** `nextreme-docs` disciplined Word, `nextreme-pptx` disciplined geometry — `nextreme-svg` should be **spec-correct + illustration-grade + diagram-true**, the one skill that is safe to render in an untrusted email *and* beautiful enough for a keynote.

**Borrow:**

- From **svg-foundry** — 12-domain knowledge base + 4 formats (especially React/Vue for Nextreme web)
- From **upbrew** — render-verify-fix loop + five-zone lighting + character incremental build
- From **pkt-lab** — 5-step plan + layered order + 14 structural checks (overlaps, arrow-through-box)
- From **jawwad** — validator (`validate_svg.py`) + security deny list + presentation-attributes (not CSS) + SMIL-only

**Must-have to be #1:**

- `compatibility: python>=3.9` + `requirements.txt` (`cairosvg` or `librsvg` for render, `lxml` for validation) — ship `scripts/` + `templates/` + `references/` via `skills.sh` (same fix done for docs/pptx)
- `references/svg-spec.md` with spec tokens (viewBox, preserveAspectRatio, path BNF) + `references/svg-taste.md` (zinc/parchment palettes, tracking, geometric spacing — reuse nextreme-pdf taste)
- `scripts/validate_svg.py` — OOXML-like for SVG: unzip not needed, but check `viewBox` vs `width/height`, `path` `d` sanity, `<text>` overflow, `clipPath`/`mask` id resolution, `aria` presence
- `scripts/render_svg.py` — SVG → PNG via `cairosvg`/`librsvg` for visual self-review (like pkt-lab)
- `templates/` — 9 starters (icon 24×24, logo, illustration, diagram, chart, pattern, animation, text-path, filter) — each valid SVG with real content, not filler

**Anti-patterns to reject:** `<foreignObject>`, `javascript:` URLs, external fonts, CSS-in-markup (use presentation attributes), flat 2-stop gradients, pure-black shadows, `viewBox` missing (responsive break), 1-shot without loop.

---

## 5. Sources (High-Trust, 2026)

- Zacklinkk/svg-foundry-skill — https://github.com/Zacklinkk/svg-foundry-skill — 2026-03-25, Apache 2.0, 127 refs, 12 domains, 4 formats
- upbrew-tech/svg-creator-skill — https://github.com/upbrew-tech/svg-creator-skill — 2026-01-12, Apache 2.0, render-verify-fix, 885-line advanced-techniques
- pkt-lab/svg-diagram — https://github.com/pkt-lab/svg-diagram — 2026-03-19, 14 checks, layered, librsvg+cairo
- jawwadfirdousi/agent-skills svg-creator — https://github.com/jawwadfirdousi/agent-skills/tree/main/svg-creator — 2026-02-02, validator + security + SMIL-only
- qaz1230sp/ink-graph — https://github.com/qaz1230sp/ink-graph — 2026-05-08, 11 themes, 14 types, CSS/SMIL, zero JS
- ChanMeng666/svg-animation-studio — https://github.com/ChanMeng666/svg-animation-studio — 25 primitives, 4 skills + 3 subagents, Vitest snapshots
- swogjs/skillstead svg-infographic — https://github.com/swogjs/skillstead — Beta, compute-first, 2× PNG, CJK-safe
- pq-dong/GenSvg — https://github.com/pq-dong/GenSvg — JSONL streaming, Zod Catalog
- seeb4coding/SVG-ORA-Studio — https://github.com/seeb4coding/svg-ora-studio — 2025-12-09, browser, Gemini
- plus cross-checks: W3C SVG 2, OWASP, DOMPurify (via jawwad security ref)

*Captured 2026-08-31 — next step: use this as spec for `nextreme-svg` following the `nextreme-docs`/`nextreme-pptx` pattern.*
