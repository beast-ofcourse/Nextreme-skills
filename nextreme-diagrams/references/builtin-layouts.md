# Built-in HTML+SVG Layout Reference

Detailed layout patterns and coordinate templates for generating technical diagrams as standalone HTML files with inline SVG, used when fireworks-cli is not available.

---

## General Layout Framework

### Color Palette (CSS Custom Properties)

All diagrams should include these CSS variables for consistent theming:

```css
:root {
  --bg: #ffffff;
  --bg-node: #f8fafc;
  --bg-group: #f1f5f9;
  --bg-highlight: #fef3c7;
  --text: #0f172a;
  --text-secondary: #475569;
  --text-muted: #94a3b8;
  --border: #cbd5e1;
  --border-group: #94a3b8;
  --line: #64748b;
  --line-sync: #3b82f6;
  --line-async: #94a3b8;
  --line-stream: #8b5cf6;
  
  /* Semantic accent colors */
  --blue: #3b82f6;
  --green: #22c55e;
  --red: #ef4444;
  --amber: #f59e0b;
  --purple: #a855f7;
  --teal: #14b8a6;
  --rose: #f43f5e;
  --cyan: #06b6d4;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0f172a;
    --bg-node: #1e293b;
    --bg-group: #334155;
    --bg-highlight: #422006;
    --text: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --border: #475569;
    --border-group: #64748b;
    --line: #94a3b8;
    --line-sync: #60a5fa;
    --line-async: #64748b;
    --line-stream: #a78bfa;
  }
}
```

### HTML Shell Template

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Diagram Title</title>
<style>
  @page { size: A4 landscape; margin: 0.4in; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); }
  .page { padding: 0.4in; min-height: 100vh; }
  .title { font-size: 24px; font-weight: 700; margin-bottom: 4px; }
  .subtitle { font-size: 14px; color: var(--text-secondary); margin-bottom: 20px; }
  svg.diagram { width: 100%; height: auto; display: block; }
  .legend { margin-top: 20px; padding: 12px; background: var(--bg-node); border-radius: 8px; font-size: 11px; display: flex; gap: 16px; flex-wrap: wrap; }
  .legend-item { display: flex; align-items: center; gap: 6px; }
  .legend-line { width: 24px; height: 2px; }
  /* ... color variables as defined above ... */
</style>
</head>
<body>
<div class="page">
  <div class="title">Diagram Title</div>
  <div class="subtitle">Description / context</div>
  <svg class="diagram" viewBox="0 0 1200 800" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <!-- arrow markers -->
    </defs>
    <!-- diagram content -->
  </svg>
  <!-- legend -->
</div>
</body>
</html>
```

---

## 1. System Architecture Layout

### Coordinate Map (1200×800 viewBox)

```
Y=0   ┌──────────────────────────────────────────────────┐
      │  ┌─ VPC Label ──────────────────────────────┐    │
Y=60  │  │   (dashed boundary box)                  │    │
      │  │                                           │    │
      │  │  ┌──────┐  ┌──────┐  ┌──────┐            │    │
Y=150 │  │  │ LB   │  │ App1 │  │ App2 │            │    │
      │  │  └──┬───┘  └──┬───┘  └──┬───┘            │    │
      │  │     │          │          │               │    │
      │  │     └──────────┼──────────┘               │    │
Y=250 │  │                ▼                          │    │
      │  │          ┌──────────┐                     │    │
      │  │          │  Cache   │                     │    │
Y=310 │  │          │  (Redis) │                     │    │
      │  │          └──────────┘                     │    │
      │  │                │                          │    │
      │  │                ▼                          │    │
Y=400 │  │  ┌─────────────────────┐                  │    │
      │  │  │  Database Cluster   │                  │    │
      │  │  │  ┌─────┐  ┌─────┐  │                  │    │
Y=460 │  │  │  │ Pri │  │ Rep │  │                  │    │
      │  │  │  └─────┘  └─────┘  │                  │    │
      │  │  └─────────────────────┘                  │    │
      │  │                                           │    │
Y=700 │  └───────────────────────────────────────────┘    │
Y=800 └──────────────────────────────────────────────────┘
```

### Node Placement

| Element | X | Y | Width | Height | Notes |
|---------|---|----|-------|--------|-------|
| VPC Boundary | 50 | 50 | 1100 | 660 | dashed, rx=10 |
| Public subnet boundary | 80 | 100 | 1040 | 200 | dashed, rx=6, lighter fill |
| Private subnet boundary | 80 | 320 | 1040 | 360 | dashed, rx=6, lighter fill |
| Load Balancer | 500 | 150 | 200 | 50 | center column |
| App Server 1 | 300 | 230 | 160 | 50 | left column |
| App Server 2 | 740 | 230 | 160 | 50 | right column |
| Cache (Redis) | 500 | 310 | 200 | 50 | center |
| DB Primary | 420 | 460 | 160 | 60 | cylinder shape |
| DB Replica | 620 | 460 | 160 | 60 | cylinder shape |
| DB Cluster box | 380 | 420 | 440 | 140 | inner group |

### SVG Recipe for Services

```svg
<!-- Service node -->
<rect x="500" y="150" width="200" height="50" rx="6" 
      fill="var(--bg-node)" stroke="var(--blue)" stroke-width="1.5"/>
<text x="600" y="180" text-anchor="middle" font-size="13" font-weight="600">Load Balancer</text>
<text x="600" y="194" text-anchor="middle" font-size="10" fill="var(--text-muted)">NLB / ALB</text>

<!-- Connection arrow -->
<line x1="600" y1="200" x2="600" y2="280" 
      stroke="var(--line-sync)" stroke-width="2" marker-end="url(#arrowSync)"/>

<!-- Boundary box (VPC / subnet) -->
<rect x="50" y="50" width="1100" height="660" rx="10" 
      fill="none" stroke="var(--border-group)" stroke-width="1.5" stroke-dasharray="8,4"/>
<rect x="50" y="50" width="120" height="28" rx="6" fill="var(--bg-group)" stroke="var(--border-group)" stroke-width="1.5"/>
<text x="110" y="69" text-anchor="middle" font-size="11" font-weight="600">AWS VPC</text>
```

---

## 2. AI / Agent Workflow Layout

### Coordinate Map (1200×800 viewBox)

For a RAG (Retrieval-Augmented Generation) workflow:

```
┌───┐          ┌╌╌╌╌╌╌╌╌╌╌┐         ┌──────────┐
│User│────────▶╎   LLM    ╎────────▶│  Search  │
└───┘  solid   ╎(Claude 3)╎  async  │  Tool    │
       sync    └╌╌╌╌╌╌╌╌╌╌┘         └──────────┘
                   │    ▲                 │
                   │    │  sync response  │
                   │    │                 │
                   ▼    │                 ▼
              ┌──────────┐          ┌──────────┐
              │  Vector   │◀────────│Embedding │
              │  Store    │  async  │  Model   │
              └──────────┘         └──────────┘
```

### Placement

| Element | X | Y | Width | Height | Shape |
|---------|---|----|-------|--------|-------|
| User (actor) | 120 | 320 | 60 | 60 | Circle/oval |
| LLM | 400 | 280 | 240 | 60 | Double-border rect |
| Search Tool | 800 | 180 | 160 | 50 | Rounded rect |
| Vector Store | 800 | 420 | 160 | 70 | Cylinder |
| Embedding Model | 800 | 640 | 160 | 50 | Rounded rect |

---

## 3. UML Sequence Diagram Layout

### Coordinate Map (1200×800 viewBox)

For a 4-participant sequence:

```
Timeline:  Y increases downward
Lifelines: X = 120, 380, 640, 900, 1080 (5 participants max)
           X spacing = 260px between lifelines

Messages are horizontal lines between lifelines, placed every 70px vertically:
  Y=200  Client ──────────▶ API Gateway       (solid, sync request)
  Y=270  API Gateway ──────▶ Auth Service      (solid, sync request)
  Y=340  Auth Service ──────▶ User DB          (solid, sync request)
  Y=410  User DB ◀─────────── Auth Service      (dashed, sync return)
  Y=480  Auth Service ◀─────── API Gateway      (dashed, sync return)
  Y=550  API Gateway ◀───────── Client          (dashed, sync return)

Optional: activation bars (thin rects on lifeline, height = message span)
  - Client:    Y=200 to Y=550, width=12, X=114
  - API Gate:  Y=200 to Y=550, width=12, X=374
```

### SVG Pattern Note

Each lifeline consists of:
1. A box at the top (80×30 or similar) with the participant name
2. A vertical dashed line extending down from the bottom of the box
3. Optionally, activation bars (thin colored rectangles) on the lifeline
4. Arrows between lifelines with labels

Keep the diagram clean: for more than 5 participants, increase the viewBox width or reduce label sizes.

---

## 4. Event-Driven Architecture Layout

### Coordinate Map (1200×800 viewBox)

```
Producers row:      Y=100-200
Event bus line:     Y=250 (horizontal line across full width)
Topics rail:        Y=260-350 (pill shapes centered on bus line)
Consumers row:      Y=400-500
Consumer groups:    Y=550-620 (optional, dashed boxes)
```

### Up to 4 Topics

Space topics evenly across the 200-1000 X range. For N topics, place centers at:

- 2 topics: X=400, X=800
- 3 topics: X=250, X=600, X=950
- 4 topics: X=200, X=466, X=733, X=1000

Each topic pill is 200×50 with rx=25.

Producers and consumers align vertically with their topic's center column.

---

## 5. Network Topology Layout

### Coordinate Map (1200×800 viewBox)

Multi-tier network with left-to-right flow:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Internet   │───▶│  Firewall   │───▶│  Web Tier   │
│             │    │             │    │  (DMZ)      │
└─────────────┘    └─────────────┘    └──────┬──────┘
                                             │
                                    ┌────────▼──────┐
                                    │  App Tier     │
                                    │  (Private)    │
                                    └───────┬───────┘
                                            │
                                    ┌───────▼───────┐
                                    │  Data Tier    │
                                    │  (Restricted) │
                                    └───────────────┘
```

Columns:
- Left (X=100-350): External / WAN
- Mid-left (X=400-600): Edge / DMZ
- Mid-right (X=650-850): Application
- Right (X=900-1100): Data / Storage

---

## 6. Data Flow / ETL Layout

### Coordinate Map (1200×800 viewBox)

Left-to-right pipeline with up to 6 stages:

```
X=80     X=280     X=480     X=680     X=880     X=1080
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│Source│→│Extract│→│Clean │→│Load  │→│Query │→│Report│
└──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘
```

Each stage node: 160×50, centered at Y=400.

For parallel paths (e.g., two concurrent transforms), stack them:
- Path 1: Y=350
- Path 2: Y=450
- Merge point at next stage center

---

## 7. Scientific / Educational Diagram Layout

### Coordinate Map (1200×800 viewBox)

Use a clean, generous layout with 40px grid spacing. Elements are larger with more padding.

| Ramp | Hex | Primary Use |
|------|-----|-------------|
| Slate | `#64748b` | Neutral structure |
| Blue | `#3b82f6` | Information flow |
| Green | `#22c55e` | Biological / growth |
| Red | `#ef4444` | Critical / hot |
| Amber | `#f59e0b` | Caution / energy |
| Purple | `#a855f7` | AI / inference |
| Teal | `#14b8a6` | Fluids / networks |
| Rose | `#f43f5e` | Vital signs |
| Cyan | `#06b6d4` | Storage / cold |

For scientific diagrams, prefer:
- Clean sans-serif font (Inter, system-ui)
- Full color fills with white text (instead of outlined shapes)
- Larger labels (14-16px for items, 11-12px for annotations)
- More whitespace between elements

---

## Legend Component

Every technical diagram should include a legend in the bottom-right corner:

```svg
<g class="legend" transform="translate(800, 680)">
  <rect x="0" y="0" width="350" height="100" rx="6" 
        fill="var(--bg-node)" stroke="var(--border)" stroke-width="1"/>
  <text x="10" y="18" font-size="11" font-weight="600">Legend</text>
  
  <!-- Sync arrow -->
  <line x1="10" y1="35" x2="40" y2="35" stroke="var(--line-sync)" stroke-width="2" marker-end="url(#arrowSync)"/>
  <text x="48" y="39" font-size="10" fill="var(--text-secondary)">Sync Request</text>
  
  <!-- Async arrow -->
  <line x1="10" y1="55" x2="40" y2="55" stroke="var(--line-async)" stroke-width="1.5" stroke-dasharray="6,3" marker-end="url(#arrowReturn)"/>
  <text x="48" y="59" font-size="10" fill="var(--text-secondary)">Async Event</text>
  
  <!-- Stream arrow -->
  <line x1="10" y1="75" x2="40" y2="75" stroke="var(--line-stream)" stroke-width="3" marker-end="url(#arrowData)"/>
  <text x="48" y="79" font-size="10" fill="var(--text-secondary)">Data Stream</text>
  
  <!-- Shapes (right column) -->
  <rect x="180" y="26" width="40" height="18" rx="4" fill="none" stroke="var(--border)"/>
  <text x="226" y="39" font-size="10" fill="var(--text-secondary)">Service</text>
  
  <rect x="180" y="46" width="40" height="18" rx="9" fill="none" stroke="var(--border)"/>
  <text x="226" y="59" font-size="10" fill="var(--text-secondary)">Queue/Topic</text>
  
  <polygon points="180,72 200,62 220,72 200,82" fill="none" stroke="var(--border)"/>
  <text x="226" y="76" font-size="10" fill="var(--text-secondary)">Decision</text>
</g>
```
