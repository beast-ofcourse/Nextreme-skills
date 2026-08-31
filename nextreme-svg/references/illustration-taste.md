# Illustration Taste — Five-Zone Lighting, Not Flat

## Five-Zone Lighting (Specular → Reflected)

From upbrew: every fill is 5 zones, not 1.

```
Specular (highlight, near-white, 8% area) → Light (mid-tone, 35%) → Half-tone (transition, 25%) → Form shadow (dark, 22%) → Reflected light (subtle lift, 10%)
```

In SVG: 6-stop gradient with `hue-shift` + `feGaussianBlur` for soft edge + `feOffset` for form shadow.

- **Colored shadows:** `flood-color="#1e3a5f"` (dark blue/purple/teal), `color-interpolation-filters="linearRGB"`, never pure `#000`.
- **Noise:** `feTurbulence baseFrequency="0.015" numOctaves="2" seed="2"` + `feColorMatrix` at 0.06 opacity to break digital perfection.

## Multi-Stop Gradients

4–8 stops, each hue-shifted 8–12° (e.g., `#1B4F72 → #2E86AB → #3A9AD9 → #A8DADC`). Flat 2-stop is the top marker of AI slop.

## Scene Composition

- Back-to-front: sky → far → mid → foreground → vignette (`radialGradient` at edges, 0.08 opacity).
- Atmospheric haze: `feGaussianBlur stdDeviation="1.2"` + `opacity="0.12"` between layers.
- Ground shadow: `ellipse` with `feGaussianBlur` at base of figure.

## Character Construction (Thick Rounded Limbs)

1. **Limbs:** `stroke="…"` `stroke-width="14"` `stroke-linecap="round"` `stroke-linejoin="round"` — creates tapered natural shapes.
2. **Joints:** `circle` joint covers (`r = stroke-width/2 + 1`) drawn *after* limbs — clean, connected.
3. **Build order:** torso → legs → arms → head → details — verify each step via `render_svg.py`.
4. **Proportions:** 8-head for realistic, 3-head for cute (large head).

## Drop Shadows (One Logic)

`linearRGB` blur: `feGaussianBlur stdDeviation="3"` → `feOffset dx="0" dy="4"` → `feComposite` — `0 0 0 1px rgba(0,0,0,0.04)` ring + `shadow-sm` whisper. Never hard `0 8px 32px`.

## Animation (CSS vs SMIL)

- **HTML inline:** CSS `transform-box: fill-box; transform-origin: 50% 50%; animation: float 3s ease-in-out infinite` + `@media (prefers-reduced-motion: reduce) { * { animation: none } }`
- **Standalone `<img>`:** SMIL `<animateTransform attributeName="transform" type="rotate" from="0 60 60" to="360 60 60" dur="2s" repeatCount="indefinite"/>`
- Timings: breathing 3–4s, walking 1–1.2s, bouncing 0.5–0.8s.
