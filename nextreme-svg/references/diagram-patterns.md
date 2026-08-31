# Diagram Patterns — 5-Step Plan + Layered Order

## 5-Step Plan (Before First <rect>)

1. **Inventory** — list every box, label, legend, warning callout.
2. **Grid** — pick viewBox (e.g., `0 0 1200 800`) with 40px snap; columns via `COL_WIDTH = (W - (cols-1)*GUTTER)/cols`.
3. **Size-to-text** — label width = `charCount × fontSize × 0.6` (e.g., “Flux Data” 9ch × 14px × 0.6 ≈ 76px → need 80px box). Do this for every label before placing.
4. **Route connections** — draw invisible `a→b` lines first; if a line goes through a box or text, reroute via `C` bezier with 40px clearance.
5. **Canvas size** — viewBox tightly fits content + 40px padding; no `width`/`height` without `viewBox`.

## Layered Order (Never Break)

```svg
<svg viewBox="0 0 1200 800">
  <g id="background">…</g>
  <g id="containers">  <!-- VPCs, lanes, swimlanes -->
  <g id="nodes">       <!-- boxes, circles -->
  <g id="labels">      <!-- text -->
  <g id="connections"> <!-- arrows last → never hidden -->
</svg>
```

Connections last is law.

## 14 Structural Checks (validate_svg.py)

1. Box overlaps, 2. Text overflow, 3. Arrow-through-box, 4. Arrow-through-text, 5. Missing markers, 6. Tight spacing, 7. ViewBox mismatch, 8. Grid misalignment, 9. Layer violation, 10. ID resolution (`url(#id)` exists), 11. Path `d` sanity, 12. ViewBox vs width/height, 13. Security (no script), 14. A11y (`<title>`).

## Routing Tips

- Use `marker-end="url(#nxt-arrow)"` for arrows; `stroke-dasharray="6 3"` for async.
- Keep 40px clearance between parallel edges; 12px between label and box.
- Free color choice — just ensure contrast ≥4.5:1 and stroke-fill cohesion within diagram.
