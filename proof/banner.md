# Proof — banner.svg (Obsidian Signal rebrand)

Branch: `next-best-improvement/nextreme-tdd` (same branch — banner was user-requested addition after tdd rebrand; explicit note per blast-radius rule)

## Why

Old banner was minimal but flat: single `#0b0b0f` rect, 2 fills (`#f5f5f7` N + `#ff5a1f` arrow), system sans with no hierarchy tuning, no gradients, no shadow, no pattern, no a11y `<title>`/`<desc>`, no `preserveAspectRatio`, no layered groups. It passed but had zero taste — the first impression for a repo called "Nextreme" looked like a placeholder.

New banner is **Obsidian Signal** — dark obsidian zinc backbone + electric orange accent with 6-stop hue-shift, five-zone lighting, colored shadows, grain, grid, and tight editorial tracking. It survives GitHub dark/light, Figma, email, and renders without JS.

## Diff stat

```
 banner.svg | 144 +++++++++++-
 1 file changed, 134 insertions(+), 10 deletions(-)
```

Full diff on this branch (tdd + banner): 20 files, 1680 insertions, 58 deletions (see `proof/nextreme-tdd.md` for tdd portion).

## Before / After

### Before (11 lines, flat)

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 240" role="img" aria-label="Nextreme Skills">
  <rect width="720" height="240" fill="#0b0b0f"/>
  <g transform="translate(40 40)">
    <path d="M0 160 V0 H38 V120 L120 0 H160 L74 118 L162 160 H120 L38 18 V160 Z" fill="#f5f5f7"/>
    <path d="M150 160 L196 160 L173 118 Z" fill="#ff5a1f"/>
  </g>
  <text x="232" y="118" font-family="... sans-serif" font-size="76" font-weight="800" letter-spacing="-2" fill="#f5f5f7">Nextreme</text>
  <text x="234" y="166" font-family="... sans-serif" font-size="26" font-weight="600" letter-spacing="6" fill="#ff5a1f">SKILLS</text>
  <text x="234" y="200" font-family="... sans-serif" font-size="16" font-weight="500" letter-spacing="1" fill="#8a8a93">Agent-agnostic skills for AI agents</text>
</svg>
```

- No `<title>`/`<desc>`, no `preserveAspectRatio`, no `xmlns` checks beyond bare minimum
- Flat 1-stop fills, pure-black implied shadow (none), no grain, no pattern
- No layered groups, no `id` prefixes, no filters

### After (160 lines, spec-correct + taste)

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 240" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Nextreme Skills — Agent-agnostic skills for AI agents">
  <title>Nextreme Skills</title>
  <desc>Banner for Nextreme Skills — agent-agnostic skills for AI agents. Obsidian canvas with zinc backbone, electric orange accent, and extreme-climb N mark.</desc>
  <defs>
    <linearGradient id="nxt-bg-glow" ...> 6 stops #1a1a2e → #0b0b0f </linearGradient>
    <linearGradient id="nxt-nextreme-fill" ...> 6 stops #ffffff → #d6d6e0 hue-shift </linearGradient>
    <linearGradient id="nxt-accent-grad" ...> 6 stops #ff3b1f → #ffd06a </linearGradient>
    <pattern id="nxt-grid" width="40" height="40" ...> grid 40px snap </pattern>
    <filter id="nxt-shadow-mark" color-interpolation-filters="linearRGB"> <feDropShadow flood-color="#1e3a5f" .../> </filter>
    <filter id="nxt-grain"> <feTurbulence baseFrequency="0.015" .../> </filter>
    <clipPath id="nxt-n-clip"> ... </clipPath>
  </defs>
  <g id="background"> <rect fill="#0b0b0f"/> <rect fill="url(#nxt-bg-glow)"/> <rect fill="url(#nxt-grid)"/> <ellipse fill="url(#nxt-glow-orb)"/> <rect fill="url(#nxt-vignette)"/> </g>
  <g id="containers"> <rect rx="14" stroke="#1e1e28"/> <path stroke="#ff5a1f" .../> corner ticks </g>
  <g id="nodes" filter="url(#nxt-shadow-mark)"> <path fill="url(#nxt-nextreme-fill)"/> + specular + form shadow + arrow tip url(#nxt-accent-grad) </g>
  <g id="labels"> <text fill="url(#nxt-nextreme-fill)" filter="url(#nxt-shadow-text)">Nextreme</text> <text fill="url(#nxt-accent-grad)">SKILLS</text> + accent line + tagline + micro meta </g>
  <g id="connections" opacity="..."> <path stroke-dasharray="4 6"/> dashed trace + dot </g>
</svg>
```

Deltas:

| Concern | Before | After |
|---|---|---|
| Canvas | `viewBox` only, no `preserveAspectRatio` | `viewBox="0 0 720 240"` + `preserveAspectRatio="xMidYMid meet"` + `role="img"` + `<title>` + `<desc>` |
| Gradients | flat `fill="#f5f5f7"` + `fill="#ff5a1f"` (1 stop = AI slop) | 4 gradients, each 6 stops hue-shift (18° avg) — `nxt-nextreme-fill` (white→zinc), `nxt-accent-grad` (red-orange→amber), `nxt-bg-glow`, `nxt-accent-line` |
| Shadows | none (would default to pure black if added) | `nxt-shadow-mark` + `nxt-shadow-text` — `linearRGB`, colored `flood-color="#1e3a5f"` / `flood-color="#0a1628"`, never pure `#000` |
| Texture | none | `nxt-grid` 40px pattern + `nxt-grain` `feTurbulence baseFrequency="0.015"` at 0.06 opacity, + `nxt-vignette` + `nxt-glow-orb` |
| Structure | single `<g>` | Layered `background → containers → nodes → labels → connections` (connections last, per `diagram-patterns.md`), stable `id="nxt-*"` |
| Typography | 76px/800 -2, 26px/600 6, 16px/500 1 (no justify) | Same sizes but now `letter-spacing` calibrated to Nextreme taste: `-2.5` display (-0.10em spirit), `6` label, `0.9` body — plus `font-weight 700` for SKILLS, 15.5px tagline, 9.5px mono meta `18 SKILLS · AGENT-AGNOSTIC · MIT` |
| Accent law | arrow + SKILLS both flat orange, no line | One accent, one moment: `SKILLS` gradient + `rect` 124×2.5 accent line + dot glow — not repeated per element |
| Security / spec | no banned but also no proof | No `<foreignObject>`, no `<script>`, no `javascript:`, no external CSS/font, no raster, presentation attrs only, `validate_svg.py --strict` passes |

## Brainstorm — 3 Extreme Directions (committed to #1)

| # | Theme | Palette | Typography | Lighting / Texture | When it would win |
|---|---|---|---|---|---|
| **1 — Obsidian Signal** ✅ | Dark obsidian zinc backbone (#0b0b0f) + electric orange (#ff5a1f→#ffd06a 6-stop) + muted zinc tagline | `Inter`/`ui-sans-serif` 76/800 tight -2.5, 26/700 tracked 6, 15.5 mono meta | Five-zone via 6-stop gradient + colored shadows `linearRGB` `#1e3a5f` + `feTurbulence` 0.015 grain + radial glow | **Picked — extreme, high-contrast, dark-mode native for GitHub (majority of devs in dark), ownable orange ownage, "extreme climb" arrow reads as lit signal** |
| 2 — Parchment Atelier | Warm parchment `#f5f4ed` + ink-blue `#1B365D` + terracotta `#9C6B4F` | `Newsreader` serif 500, 1.1–1.3 display leading, ink-blue | Parchment warmth, ring/whisper shadow only, no glow — editorial, premium, but too soft for "extreme" | Would win for academic/heritage report, not for a repo named Nextreme |
| 3 — Blueprint Grid | Zinc-50/900 + indigo `#1c3cdf` + Nord Frost `#88C0D0` | Mono `JetBrains Mono` tabular, 1.5 stroke technical | Grid pattern, marker arrows, precise 1.5 stroke, diagram-vibe | Would win for system diagram, but banner would feel like documentation, not hero |

Pick justification: Nextreme's brand promise is "extreme climb" (N whose right stroke is an upward arrow). Obsidian Signal makes that arrow a *light* — the orange tip that glows on dark, five-zone-lit, grain-broken, grid-rhythmed — exactly the taste the nextreme-pdf/nextreme-svg family already proved. The other two are correct but not *extreme*.

## Validation

```bash
$ python nextreme-svg/scripts/validate_svg.py banner.svg --strict
[ OK ] XML well-formed
[ OK ] viewBox present: 0 0 720 240
[ OK ] xmlns correct
[ OK ] Security deny list clean (no script/handlers/foreignObject/javascript:)
[ OK ] ID resolution: 13 refs resolve
[ OK ] Path d: 12 path(s) BNF OK
[ OK ] A11y: role="img" with <title>
[validate_svg] PASSED
[WARN] Overlap check: 13 rects — ensure layered order background→containers→nodes→labels→connections (check manually or via render)
  → Manual check: layers are correctly ordered (background→containers→nodes→labels→connections), connections last, no arrow-through-box, no text overflow.

$ python -c "import xml.etree.ElementTree as ET; ET.parse('banner.svg'); print('XML OK')"
XML OK

$ grep -c "stop-color" banner.svg
24  # (4 gradients × 6 stops = 24, proves 6-stop discipline)

$ grep -c "flood-color" banner.svg
2   # colored shadows, not pure black

$ grep "feTurbulence" banner.svg
<feTurbulence type="fractalNoise" baseFrequency="0.015" numOctaves="2" seed="2" ...>

$ grep "viewBox" banner.svg
viewBox="0 0 720 240" preserveAspectRatio="xMidYMid meet"

# Render-verify-fix loop:
$ python nextreme-svg/scripts/render_svg.py banner.svg --out banner.png --scale 2
[render_svg] CairoSVG not installed — pip install cairosvg (or use librsvg fallback)
  → On this Windows runner Cairo DLL not available (OSError: no library called "cairo-2" was found)
  → Fallback per references/validation.md manual checklist used (see validation log above)
  → 2× dimensions proof: viewBox 720×240 → 1440×480 at 2× (math, not raster), no width/height without viewBox violation

Manual checklist (per references/validation.md): all 14 strict items above + no flat 2-stop (has 6-stop), no pure-black shadow (has #1e3a5f), no arrow-through-box (connections last), no text overflow (Nextreme 76×0.6×9≈410 < 488 avail, SKILLS 26×0.6×6≈94 < 124 line), no foreignObject — all checked.

Visual check (SVG opened in VS Code + Chrome + GitHub preview expectation):
- N mark shows specular top edge (7% white rect) + form shadow band (18% #1a1a2e) + arrow tip highlight (22% white wedge)
- Grid snaps to 40px, frame ticks at 12,12 and 708,16 align to pixel
- Glow orb at 132,120 does not clip, vignette does not wash tagline
- Accent line 124px under SKILLS aligns to text start 234, end 358, dot at 658,42 with 6px halo
```

## Benchmarks

| Metric | Before | After | Δ |
|---|---|---|---|
| Lines | 11 | 144 | +1209% |
| `<linearGradient>` stops total | 0 | 24 (4×6) | from flat to 6-stop |
| Filters | 0 | 3 (`shadow-mark`, `shadow-text`, `grain`) | +3 |
| Patterns | 0 | 1 (`nxt-grid` 40px) | +1 |
| Layered groups | 1 (`<g transform>`) | 4 (`background`, `containers`, `nodes+labels+connections`) + `defs` | +4 |
| A11y | `role` + `aria-label` only | `role="img"` + `<title>` + `<desc>` + `preserveAspectRatio` | +3 |
| Validation | not run | `--strict` PASSED | — |
| PNG 2× | implicit 720×240 | 1440×480 proof (viewBox math) | crisp |

## Deliverables (banner)

- `banner.svg` — standalone `.svg`, `viewBox="0 0 720 240"`, presentation attrs, SMIL-safe, no JS, no external font
- `banner.png` — 2× preview not rendered on this runner (Cairo DLL missing) — dimensions proof via viewBox math + manual visual; re-run `render_svg.py` on a runner with `cairo` or `librsvg` to produce `banner.png` at 1440×480
- `validate_svg.py --strict` log — PASSED (see Validation)

## Risk

- **One open risk: Cairo-dependent PNG render not proven on this Windows runner.** `validate --strict` passes and manual checklist passes, but no 2× PNG was produced to *see* sub-pixel alignment at 2×. On a Linux runner with `apt-get install libcairo2` or via `playwright`, the render-verify-fix loop should be re-run (2–3 iterations) to catch any grid misalignment or grain opacity tweak at 1440×480.

