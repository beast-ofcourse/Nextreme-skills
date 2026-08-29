# QuickChart.io Reference (Alternative Engine)

For quick, zero-dependency PNG charts. Uses Chart.js under the hood via the QuickChart.io API.

## When to Use

- User wants a chart image **right now** without installing anything
- Simple bar, line, area, pie, doughnut, or horizontal bar
- Light/dark mode without local setup
- Not suitable for: sensitive data (sends to external API), exotic chart types, publication-grade vector output

## Workflow

1. **Parse the request**: chart type, data, theme (light/dark), title, output path, size
2. **Build Chart.js config JSON** with correct theme tokens
3. **Write the full request body** to `payload.json` (never shell-interpolate data)
4. **POST with curl**:
   ```bash
   curl -X POST https://quickchart.io/chart \
     -H 'Content-Type: application/json' \
     -d @payload.json \
     --output ~/Downloads/chart_$(date +%Y%m%d_%H%M%S).png
   ```
5. **Show result** by reading the generated image file

## Theme Tokens

| Token | Light | Dark |
|-------|-------|------|
| Canvas background | `#FFFFFF` | `#23262A` |
| Title text | `#17191A` | `#E8EAED` |
| Axis ticks / labels / legend | `#717B84` | `#959CA3` |
| Grid lines | `#EFF1F2` | `#3A4046` |
| Series 0 (primary) | `#0054FF` | `#75BAFF` |
| Series 1 | `#14B8A6` | `#2DD4BF` |
| Series 2 | `#8B5CF6` | `#A78BFA` |
| Series 3 | `#F97316` | `#FB923C` |
| Series 4 | `#EAB308` | `#FACC15` |
| Series 5 | `#EF4444` | `#F87171` |
| Segment border (pie) | `#FFFFFF` | `#23262A` |

## Chart Configurations

### Bar Chart
```json
{
  "type": "bar",
  "data": {
    "labels": ["A", "B", "C"],
    "datasets": [{
      "data": [10, 20, 30],
      "backgroundColor": "#0054FF",
      "borderRadius": 4
    }]
  }
}
```

### Line Chart
```json
{
  "type": "line",
  "data": {
    "labels": ["Jan", "Feb", "Mar"],
    "datasets": [{
      "data": [10, 20, 30],
      "borderColor": "#0054FF",
      "borderWidth": 2,
      "tension": 0.3,
      "pointRadius": 0,
      "fill": false
    }]
  }
}
```

### Pie / Doughnut
```json
{
  "type": "doughnut",
  "data": {
    "labels": ["Engineering", "Marketing", "Operations"],
    "datasets": [{
      "data": [45, 30, 25],
      "backgroundColor": ["#0054FF", "#14B8A6", "#8B5CF6"],
      "borderColor": "#FFFFFF",
      "borderWidth": 2
    }]
  },
  "options": {
    "cutout": "60%",
    "plugins": {
      "legend": { "display": true, "position": "bottom", "labels": { "usePointStyle": true, "font": { "family": "DM Sans" } } }
    }
  }
}
```

### Full request body
```json
{
  "version": "4",
  "backgroundColor": "white",
  "width": 600,
  "height": 400,
  "chart": CHART_CONFIG_GOES_HERE
}
```

## CRITICAL: Security

**NEVER interpolate user data into shell arguments.** Always write the request body to a file with the Write tool and POST with `curl -d @payload.json`. A stray quote, backtick, or `$(...)` in the data would break shell quoting and could execute arbitrary commands.

## Style Rules

- **DM Sans** typography on every text element (`"font": { "family": "DM Sans" }`)
- All Y-axes must have visible numeric tick values (never `display: false`)
- Rounded corners on bars (`borderRadius: 4`)
- Smooth line curves (`tension: 0.3`)
- Semi-transparent fills for area charts
- Dual Y-axis: both `y` and `y1` must have visible tick values
