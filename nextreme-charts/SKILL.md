---
name: nextreme-charts
description: "Generate publication-grade SVG charts from any data using Vega-Lite (with full Vega fallback for exotic types). Also supports QuickChart.io for zero-dependency PNG and ECharts for interactive HTML dashboards. This skill handles every chart type — bar, line, area, pie, scatter, box-plot, heatmap, candlestick, waterfall, sankey, radar, treemap, geographic, and more."
license: MIT
---

# Ultimate Charts

A unified charting skill centered on **Vega-Lite** — the most LLM-friendly, publication-grade declarative chart grammar. For the ~10% of chart types Vega-Lite doesn't handle natively, it falls back to **full Vega** (same toolchain, same themes). Two alternative engines (QuickChart.io, ECharts) are available for specific use cases.

---

## Engine Selection

| Context | Primary Engine | Output | Why |
|---------|---------------|--------|-----|
| **Papers, reports, docs** | Vega-Lite | **SVG** — vector, publication-grade | Themed (McKinsey/BCG/FT/Economist), offline, YAML specs |
| **Exotic charts** (candlestick, sankey, waterfall, radar, treemap) | **Vega** (full grammar) | **SVG** | Same `render.mjs`, same theme system, just a `--vega` flag |
| **Quick one-off PNG** | QuickChart.io | **PNG** | Zero deps, natural language input, light/dark built-in |
| **Interactive dashboards / BI** | Apache ECharts | **Interactive HTML** | 11 templates, live filtering, multi-panel layouts |
| **Headless server / bots** | Vega-Lite + Sharp | **PNG** | ~15MB, <500ms cold start, no browser |

---

## ⭐ Primary Engine: Vega-Lite (with Vega fallback)

This is the default path. It covers **all chart types** through a single toolchain.

### Chart Type Coverage

| Category | Chart Types | Engine | Template File |
|----------|-------------|--------|---------------|
| **Categorical** | Bar (vertical, horizontal, stacked, grouped), Pie/Donut | Vega-Lite | `templates/bar.yaml`, `templates/pie.yaml` |
| **Time Series** | Line, Area (stacked, streamgraph), Trail | Vega-Lite | `templates/line.yaml`, `templates/area.yaml` |
| **Distribution** | Histogram, Box Plot, Violin, Error Bar, Error Band | Vega-Lite v5 | `templates/box-plot.yaml` |
| **Correlation** | Scatter, Bubble, Dot Plot, Heatmap | Vega-Lite | `templates/scatter.yaml`, `templates/heatmap.yaml` |
| **Geographic** | Choropleth, Symbol Map, Connection Map | Vega-Lite + TopoJSON | `templates/geo.yaml` |
| **Financial** | **Candlestick**, OHLC | **Vega** (full) | `templates/candlestick.json` |
| **Flow** | **Sankey**, Chord | **Vega** (full) | `templates/sankey.json` |
| **Hierarchy** | **Treemap**, Sunburst | **Vega** (full) | `templates/treemap.json` |
| **Multi-dim** | **Radar**, Parallel Coordinates | **Vega** (full) | `templates/radar.json` |
| **Containment** | **Waterfall**, Funnel | **Vega** (full) | `templates/waterfall.json` |
| **Network** | Force-Directed Graph | **Vega** (full) | `templates/graph.json` |

### Workflow

```bash
# 90% of cases — Vega-Lite YAML spec → SVG
node ${CLAUDE_SKILL_DIR}/scripts/render.mjs \
  --spec chart.yaml \
  --output chart.svg \
  --theme mckinsey

# 10% exotic cases — full Vega JSON spec → SVG
node ${CLAUDE_SKILL_DIR}/scripts/render.mjs \
  --vega \
  --spec candlestick.json \
  --output chart.svg \
  --theme ft
```

### Available Themes (Vega-Lite & Vega)

| Theme | Flag | Primary | Best For |
|-------|------|---------|----------|
| Onsen | `--theme onsen` | Blue `#4d93e5` | Product dashboards |
| Neutral | `--theme neutral` | Grey `#374151` | Academic papers |
| Bain | `--theme bain` | Red `#CC0000` | Strategy consulting |
| McKinsey | `--theme mckinsey` | Blue `#1c3cdf` | Executive presentations |
| BCG | `--theme bcg` | Green `#29BA74` | Sustainability |
| Economist | `--theme economist` | Red `#E3120B` | Data journalism |
| FT | `--theme ft` | Teal `#0D7680` | Financial reporting |
| Deloitte | `--theme deloitte` | Lime `#86BC25` | Audit, advisory |

### Style Presets

```bash
--variant light    # Light background (default)
--variant dark     # Dark background
--size desktop     # 728x420px (default)
--size mobile      # 600x400px
--width 1200       # Custom width override
--height 600       # Custom height override
```

---

## Alternative Engines

### QuickChart.io (Zero-dependency PNG)

For when the user just wants a quick chart image without installing anything.

```bash
# 1. Write payload to file (NEVER shell-interpolate data)
cat > payload.json << 'EOF'
{
  "version": "4",
  "backgroundColor": "white",
  "width": 600,
  "height": 400,
  "chart": { "type": "bar", "data": { ... } }
}
EOF

# 2. POST with curl
curl -X POST https://quickchart.io/chart \
  -H 'Content-Type: application/json' \
  -d @payload.json \
  --output chart.png
```

See `references/quickchart.md` for theme tokens and all chart configs.

### Apache ECharts (Interactive HTML)

For BI dashboards, financial charts, and multi-panel interactivity.

See `references/echarts.md` for 11 templates and project setup.

---

## Decision Flow

```
User asks for chart
  ├─ Is this for a paper, report, or publication?
  │   └─ YES → Vega-Lite → SVG (--theme neutral for papers)
  ├─ Is this a candlestick, waterfall, sankey, treemap, or radar?
  │   └─ YES → Vega (full) → SVG (same --theme support)
  ├─ Is this a quick one-off visual with no local setup?
  │   └─ YES → QuickChart.io → PNG (~/Downloads/)
  ├─ Is this an interactive dashboard or BI tool?
  │   └─ YES → ECharts → HTML (project-based)
  ├─ Is this a headless server / automated report?
  │   └─ YES → Vega-Lite → PNG (Sharp, <500ms)
  └─ Default → Vega-Lite → SVG
```

## First-Time Setup (Vega-Lite Engine)

```bash
# Install the onsen-chart-skill
npx skills add onsen-ai/chart-skill

# Install dependencies (one-time, ~50MB)
cd ${CLAUDE_SKILL_DIR} && npm install --production
```

QuickChart.io and ECharts engines require no local dependencies.

## Best Practices

- **Data never touches the shell** — always write payloads to files with Write, then reference with `--spec` or `-d @file`
- **Specify the engine explicitly** in your instruction: "use Vega-Lite, bar chart, data: ..."
- **Use Vega (--vega flag)** when the chart type isn't in Vega-Lite's native marks
- **Templates** live in `templates/` — copy, modify data, and re-render
- **Themes apply to both Vega-Lite and full Vega** — the renderer handles both
