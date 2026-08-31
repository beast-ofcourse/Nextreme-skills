# SVG Spec — 12 Domains, No Hand-Waving

This is the spec you must honor. Every SVG you ship is valid W3C SVG 2, not “looks okay in Chrome.”

## 1. Canvas & viewBox (The Only Responsive Hook)

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" preserveAspectRatio="xMidYMid meet" width="100%" height="auto" role="img">
  <title>Descriptive title</title>
  <desc>What the graphic shows — for screen readers</desc>
```

- **Always `viewBox`, never `width`/`height` alone.** `width="100%" height="auto"` + `viewBox` = responsive. `width="800" height="600"` without `viewBox` = breaks on GitHub, email, Figma.
- `preserveAspectRatio="xMidYMid meet"` (default) — use `slice` only for full-bleed covers.

## 2. Shapes (Basic & Advanced)

`rect` (`rx`/`ry`), `circle`, `ellipse`, `line`, `polyline`, `polygon`, `path`. All via presentation attrs (`fill`, `stroke`, `stroke-width`), not CSS.

## 3. Path `d` — Full BNF (No Guesswork)

`M moveto` `L lineto` `H horizontal` `V vertical` `C cubic (x1,y1 x2,y2 x,y)` `S smooth cubic` `Q quadratic` `T smooth quadratic` `A arc (rx,ry x-axis-rotation large-arc-flag sweep-flag x,y)` `Z closepath`.

- Smooth reflection: `S` reflects previous `C`’s second control point; `T` reflects previous `Q`’s control.
- Implicit lineto: after `M x y`, subsequent `x y` pairs are `L`.
- Arc flags: `large-arc-flag` 0/1, `sweep-flag` 0/1 — both matter.

## 4. Text (`text`, `tspan`, `textPath`, multilingual)

```svg
<text x="600" y="400" text-anchor="middle" dominant-baseline="middle" font-family="Inter, sans-serif" font-size="16" fill="#1a1a1e">
  Hello <tspan fill="#1B4F72" font-weight="600">world</tspan>
</text>
<text><textPath href="#curve" startOffset="50%" text-anchor="middle">Curved</textPath></text>
```

- `text-anchor`: `start|middle|end`; `dominant-baseline: middle` for vertical center.
- Multilingual: `lang="ja"` + `font-family` stack with CJK fallback.

## 5. Colors & Fills

`sRGB` `fill="#1B4F72"` or `fill="url(#grad)"` (gradient/pattern). OKLCH via `color()` in modern browsers, but keep `fill` hex for email/GitHub safety.

## 6. Gradients (Not Flat)

```svg
<defs>
  <linearGradient id="nxt-grad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#1B4F72"/><stop offset="40%" stop-color="#2E86AB"/><stop offset="100%" stop-color="#A8DADC"/>
  </linearGradient>
</defs>
<rect fill="url(#nxt-grad)"/>
```

4–8 stops, hue-shift. `radialGradient` similar with `cx,cy,r`.

## 7. Patterns

```svg
<pattern id="nxt-pat" width="20" height="20" patternUnits="userSpaceOnUse"><circle r="1" cx="10" cy="10" fill="#1B4F72" opacity="0.12"/></pattern>
```

Tileable, transformable (`patternTransform="rotate(45)"`).

## 8. Transforms

`transform="translate(10 20) rotate(45 600 400) scale(1.2) matrix(1 0 0 1 10 20)"` — order matters (rightmost first).

## 9. clipPath & mask

```svg
<clipPath id="nxt-clip"><rect x="0" y="0" width="600" height="400" rx="12"/></clipPath>
<g clip-path="url(#nxt-clip)">...</g>
<mask id="nxt-mask"><rect fill="white"/><circle fill="black"/></mask>
```

`clipPath` = hard cut; `mask` = alpha.

## 10. Filters

`feGaussianBlur` (`stdDeviation`), `feDropShadow` (`dx,dy,stdDeviation,flood-color`, `color-interpolation-filters="linearRGB"` for colored shadows), `feColorMatrix`, `feTurbulence` (`baseFrequency="0.015" numOctaves="2"`), `feDisplacementMap`.

## 11. Stroke

`stroke="#1B4F72" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="6 3"` — caps matter for character limbs (`round`).

## 12. Markers

```svg
<defs><marker id="nxt-arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#6b7280"/></marker></defs>
<line marker-end="url(#nxt-arrow)"/>
```
