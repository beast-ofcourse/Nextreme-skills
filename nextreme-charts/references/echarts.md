# Apache ECharts Reference (Alternative Engine)

For interactive web-based charts, BI dashboards, and multi-panel visualizations.

## When to Use

- User wants **interactive** charts (zoom, hover, filtering)
- Financial charts (candlestick with volume overlay)
- Multi-panel dashboards (KPI cards + charts)
- Complex layouts (heatmap, radar, waterfall, sankey)
- Not suitable for: static publication-grade output (SVG), quick one-off images

## Project Structure

```
output/chart-html/<project-name>/
  index.html        # Chart page (ECharts CDN)
  generate.py       # Reproducibility script
  data.json         # Data snapshot
  screenshot.png    # Exported image
  README.md         # Notes and data sources
```

## Available Templates

| Template | Best For | ECharts Feature |
|----------|----------|-----------------|
| `line.html` | Time-series trends | `type: 'line'`, smooth/monotone |
| `bar.html` | Category comparisons | `type: 'bar'`, horizontal/stacked |
| `pie.html` | Composition | `type: 'pie'`, rose/ring |
| `candlestick.html` | OHLCV price charts | `type: 'candlestick'` + bar volume |
| `scatter.html` | Correlation | `type: 'scatter'`, regression |
| `dashboard.html` | KPI cards + 2x2 chart grid | Multi-instance grid layout |
| `radar.html` | Multi-dimension scoring | `type: 'radar'` |
| `heatmap.html` | Matrix intensity | `type: 'heatmap'` |
| `dual-axis.html` | Different-scale series | Dual Y axes with color sync |
| `multi-panel.html` | Stacked panels (price + volume + RSI) | `dataset` + `grid` sharing X axis |
| `waterfall.html` | Incremental contribution | `type: 'bar'` stacked + floating |

## Workflow

1. **Pick template** from `templates/*.html`
2. **Create project folder**: `create_project(name, desc, sources)` from `build_chart.py`
3. **Build HTML**: `build_chart(template_name, data, options)` 
4. **Save**: `save_chart(html, project_dir)`, `save_data(data, project_dir)`, `save_generate_script(...)`
5. **Serve**: `preview_serve()` using `chart_server.py` on port 7860
6. **Export**: toolbar buttons in HTML, or `screenshot_chart(project_dir)` via Playwright

## Toolbar (required in every page)

```html
<button onclick="downloadPNG(this)">Download PNG</button>
<button onclick="copyToClipboard(this)">Copy Image</button>
<button onclick="saveToProject(this)">Save Image</button>
```

## Config Pattern

```javascript
const chart = echarts.init(document.getElementById('chart'));
chart.setOption({
  title: { text: 'Chart Title', left: 'center' },
  tooltip: { trigger: 'axis' },
  xAxis: { type: 'category', data: ['Jan', 'Feb', 'Mar'] },
  yAxis: { type: 'value' },
  series: [{ type: 'bar', data: [120, 200, 150] }]
});
window.CHART_INSTANCES = [chart];  // Required for export
```

## Notes

- Embed data directly in HTML (`const DATA = [...]`) to avoid CORS
- Register all chart instances in `window.CHART_INSTANCES` for multi-chart pages
- Use meaningful project names: `<topic>-<range>-<date>`
