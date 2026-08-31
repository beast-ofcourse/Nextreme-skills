# Templates — 9 Starters, Spec-Correct

Copy a file, replace the bracketed content with real story, run `validate_svg.py` + `render_svg.py`. Each is valid W3C SVG 2, presentation-attrs, `viewBox`-driven, layered (`background→containers→nodes→labels→connections`), and accessibility-labeled.

**Validate:**
```bash
# skills.sh:
python ${CLAUDE_SKILL_DIR}/scripts/validate_svg.py nextreme-svg/templates/icon.svg --strict
python ${CLAUDE_SKILL_DIR}/scripts/render_svg.py nextreme-svg/templates/icon.svg --out /tmp/icon.png --scale 2
# local:
python nextreme-svg/scripts/validate_svg.py templates/icon.svg --strict
```

**9 starters:**

| File | viewBox | What it proves |
|---|---|---|
| `icon.svg` | `0 0 24 24` | Minimal 24, stroke 1.5 round, `aria-hidden` |
| `logo.svg` | `0 0 340 80` | Wordmark + mark, 3-stop gradient, `role="img"` + `<title>` |
| `illustration.svg` | `0 0 1200 800` | 6-stop sky, five-zone + colored shadow + noise, back-to-front |
| `diagram.svg` | `0 0 1200 800` | Layered 14-checks, `marker-end`, `size-to-text`, `viewBox` tight |
| `chart.svg` | `0 0 1200 500` | Native `<rect>` bars, `tabular-nums`, hue-shift accent |
| `pattern.svg` | `0 0 400 400` | `<pattern patternTransform>` tileable |
| `animation.svg` | `0 0 200 200` | SMIL `animateTransform` rotate, `prefers-reduced-motion` |
| `text.svg` | `0 0 600 200` | `<textPath>` + `<tspan>`, `lang`, `dominant-baseline` |
| `filter.svg` | `0 0 400 240` | `feGaussianBlur linearRGB` drop/glow + `feTurbulence` grain |

Each ships with 2× PNG via `render_svg.py` for docs/social.
