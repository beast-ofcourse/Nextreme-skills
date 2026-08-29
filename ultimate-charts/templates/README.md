# Chart Templates

## Vega-Lite YAML Templates (Standard Chart Types)

These cover 90%+ of charting needs. Copy the YAML, replace `values` with your data, render.

| Template | Chart Type | File |
|----------|-----------|------|
| Vertical Bar | Categorical comparison | `bar.yaml` |
| Horizontal Bar | Ranking with long labels | `bar-horizontal.yaml` |
| Stacked Bar | Part-to-whole over categories | `bar-stacked.yaml` |
| Line | Time series trends | `line.yaml` |
| Multi-Series Line | Compare groups over time | `line-multi.yaml` |
| Area | Magnitude over time | `area.yaml` |
| Pie | Proportions (or donut with `innerRadius`) | `pie.yaml` |
| Scatter | Correlation between variables | `scatter.yaml` |
| Heatmap | Intensity matrix | `heatmap.yaml` |
| Box Plot | Distribution statistics (v5) | `box-plot.yaml` |

**Usage**: `node ${CLAUDE_SKILL_DIR}/scripts/render.mjs --spec templates/bar.yaml --output chart.svg`

## Vega JSON Templates (Exotic Chart Types)

For the ~10% not covered by Vega-Lite's native marks. These need the `--vega` flag.

| Template | Chart Type | File |
|----------|-----------|------|
| Candlestick | OHLCV financial charts | `candlestick.json` |
| Waterfall | Incremental contribution (P&L) | `waterfall.json` |
| Sankey | Flow between nodes | `sankey.json` |
| Radar | Multi-dimension scoring | `radar.json` |
| Treemap | Hierarchical proportion | `treemap.json` |

**Usage**: `node ${CLAUDE_SKILL_DIR}/scripts/render.mjs --vega --spec templates/candlestick.json --output chart.svg`

## Theme Support

All templates work with any theme flag:
```
--theme mckinsey --variant light
--theme ft --variant dark
--theme economist
```
