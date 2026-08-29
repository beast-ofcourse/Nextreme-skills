# Visual Style Guide for High-Quality Flowcharts

## Color Palette (Theme Tokens)

Use these CSS variables to maintain a consistent "Roadmap" look:

```css
:root {
  --bg: #ffffff;
  --ink: #111111;
  --muted: #555555;
  --line: #5a78ff;
  --node-fill: #f8e39c;
  --node-border: #9a7b24;
  --section-fill: #f3df58;
  --section-border: #b29a10;
  --accent: #4b4fe3;
  --connector: #5a78ff;
}
```

## Typography

- **Title**: 28px+, Extra Bold (800+), Sans-serif.
- **Section Headers**: 18px-22px, Bold, Sans-serif.
- **Node Text**: 12px-14px, Medium/Regular, Sans-serif.
- **Annotations**: 10px-12px, Muted color, Sans-serif.

## Spacing & Layout

- **Central Spine**: A dashed or solid vertical line (e.g., `stroke-dasharray="5,5"`).
- **Node Sizing**: Uniform width for nodes in the same group (e.g., 180px - 220px).
- **Margins**: Minimum 0.5in on all sides for print safety.
- **Grid**: Align nodes to a 20px or 40px grid for visual rhythm.

## SVG Element Patterns

### Section Header (Spine Node)
```svg
<rect x="700" y="200" width="200" height="40" rx="4" fill="var(--section-fill)" stroke="var(--section-border)" stroke-width="2"/>
<text x="800" y="225" text-anchor="middle" font-weight="bold">Section Title</text>
```

### Subtopic Node
```svg
<rect x="400" y="200" width="180" height="30" rx="4" fill="var(--node-fill)" stroke="var(--node-border)" stroke-width="1"/>
<text x="490" y="220" text-anchor="middle">Subtopic Name</text>
```

### Connector (Curved)
```svg
<path d="M 600 220 C 650 220, 650 220, 700 220" fill="none" stroke="var(--connector)" stroke-width="2" stroke-dasharray="2,2"/>
```
