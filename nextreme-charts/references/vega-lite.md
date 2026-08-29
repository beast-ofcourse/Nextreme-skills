# Vega-Lite Chart Reference

Full reference for all Vega-Lite chart types and Vega fallback specs. 
**YAML is used for Vega-Lite, JSON for full Vega specs.**

---

## Chart Type Reference

### Category: Categorical Comparisons

#### Vertical Bar

```yaml
# Vertical Bar — best for comparing values across categories
title: Revenue by Quarter
mark: bar
data:
  values:
    - { quarter: Q1, revenue: 120000 }
    - { quarter: Q2, revenue: 185000 }
    - { quarter: Q3, revenue: 210000 }
    - { quarter: Q4, revenue: 245000 }
encoding:
  x: { field: quarter, type: nominal, title: null, sort: null }
  y: { field: revenue, type: quantitative, title: "Revenue ($)" }
```

#### Horizontal Bar

```yaml
# Horizontal Bar — best for ranking with long category labels
title: Feature Usage
mark: bar
data:
  values:
    - { feature: Search, users: 84 }
    - { feature: Export, users: 58 }
    - { feature: Filters, users: 45 }
encoding:
  y: { field: feature, type: nominal, title: null, sort: "-x" }
  x: { field: users, type: quantitative, title: "Users (%)" }
```

#### Stacked Bar

```yaml
# Stacked Bar — part-to-whole across categories
title: Tickets by Priority
mark: bar
data:
  values:
    - { month: Jan, priority: Low, count: 45 }
    - { month: Jan, priority: High, count: 12 }
    - { month: Feb, priority: Low, count: 52 }
    - { month: Feb, priority: High, count: 18 }
encoding:
  x: { field: month, type: nominal, title: null }
  y: { field: count, type: quantitative, title: Tickets }
  color: { field: priority, type: nominal, title: Priority }
```

#### Grouped Bar

```yaml
# Grouped Bar — side-by-side comparison across subcategories
title: Revenue by Region
mark: bar
data:
  values:
    - { region: NA, metric: Revenue, amount: 400 }
    - { region: NA, metric: Costs, amount: 280 }
    - { region: EU, metric: Revenue, amount: 350 }
    - { region: EU, metric: Costs, amount: 210 }
encoding:
  x: { field: region, type: nominal, title: Region }
  y: { field: amount, type: quantitative, title: Amount }
  color: { field: metric, type: nominal, title: Metric }
  xOffset: { field: metric, type: nominal }
```

#### Pie / Donut

```yaml
# Pie — proportions (use arc mark)
title: Market Share
mark: arc
data:
  values:
    - { product: A, share: 45 }
    - { product: B, share: 30 }
    - { product: C, share: 25 }
encoding:
  theta: { field: share, type: quantitative }
  color: { field: product, type: nominal, title: Product }
```

```yaml
# Donut — same as pie but with innerRadius
title: Market Share
mark: arc
params:
  - { name: innerRadius, value: 50 }
data:
  values:
    - { product: A, share: 45 }
    - { product: B, share: 30 }
    - { product: C, share: 25 }
encoding:
  theta: { field: share, type: quantitative }
  color: { field: product, type: nominal, title: Product }
```

---

### Category: Time Series

#### Line

```yaml
# Line — trends over time
title: Monthly Active Users
mark:
  type: line
  point: true
  strokeWidth: 2
data:
  values:
    - { month: Jan, users: 1200 }
    - { month: Feb, users: 2400 }
    - { month: Mar, users: 3800 }
    - { month: Apr, users: 3500 }
encoding:
  x: { field: month, type: ordinal, title: null }
  y: { field: users, type: quantitative, title: Users }
```

#### Multi-Series Line

```yaml
# Multi-Series — compare trends across groups
title: Revenue by Region
mark:
  type: line
  point: true
data:
  values:
    - { month: Jan, region: EMEA, revenue: 50000 }
    - { month: Jan, region: APAC, revenue: 30000 }
    - { month: Feb, region: EMEA, revenue: 62000 }
    - { month: Feb, region: APAC, revenue: 38000 }
encoding:
  x: { field: month, type: ordinal, title: null }
  y: { field: revenue, type: quantitative, title: Revenue }
  color: { field: region, type: nominal, title: Region }
```

#### Area

```yaml
# Area — magnitude over time
title: Cumulative Users
mark:
  type: area
  line: { strokeWidth: 2 }
data:
  values:
    - { month: Jan, total: 500 }
    - { month: Feb, total: 1200 }
    - { month: Mar, total: 2100 }
encoding:
  x: { field: month, type: ordinal, title: null }
  y: { field: total, type: quantitative, title: Users }
```

#### Stacked Area

```yaml
# Stacked Area — composition over time
title: Traffic Sources
mark:
  type: area
  line: true
data:
  values:
    - { month: Jan, source: Organic, visits: 400 }
    - { month: Jan, source: Paid, visits: 200 }
    - { month: Feb, source: Organic, visits: 500 }
    - { month: Feb, source: Paid, visits: 250 }
encoding:
  x: { field: month, type: ordinal, title: null }
  y: { field: visits, type: quantitative, title: Visits }
  color: { field: source, type: nominal, title: Source }
```

#### Trail (Ordered Path)

```yaml
# Trail — path with variable width (e.g. temperature over time)
title: CPU Temperature
mark: trail
data:
  values:
    - { time: 0, temp: 65 }
    - { time: 10, temp: 72 }
    - { time: 20, temp: 78 }
    - { time: 30, temp: 74 }
encoding:
  x: { field: time, type: quantitative }
  y: { field: temp, type: quantitative }
  size: { field: temp, type: quantitative }
```

---

### Category: Distribution & Statistics

#### Histogram

```yaml
# Histogram — bin continuous data
title: Salary Distribution
mark: bar
data:
  values:
    - { salary: 45000 }
    - { salary: 52000 }
    # ... more data points
transform:
  - bin: true
    field: salary
    as: bin_start
encoding:
  x: { field: bin_start, type: nominal, title: Salary Range }
  y: { aggregate: count, type: quantitative, title: Count }
```

#### Box Plot (Vega-Lite v5)

```yaml
# Box Plot — quartiles, median, outliers
title: Score Distribution by Team
mark: boxplot
data:
  values:
    - { team: A, score: 85 }
    - { team: A, score: 92 }
    - { team: B, score: 75 }
    # ... more data points
encoding:
  x: { field: team, type: nominal }
  y: { field: score, type: quantitative }
```

#### Error Bar

```yaml
# Error Bar — mean ± confidence interval
title: Response Time by Service
mark: errorbar
data:
  values:
    - { service: API, lower: 120, upper: 180 }
    - { service: DB, lower: 5, upper: 15 }
encoding:
  x: { field: service, type: nominal }
  y: { field: lower, type: quantitative }
  y2: { field: upper, type: quantitative }
```

#### Error Band

```yaml
# Error Band — confidence band around a trend
title: Forecast with Confidence
layer:
  - mark: errorband
    encoding:
      y: { field: lower, type: quantitative }
      y2: { field: upper, type: quantitative }
  - mark: line
    encoding:
      y: { field: mean, type: quantitative }
```

---

### Category: Correlation & Heatmap

#### Scatter Plot

```yaml
# Scatter — correlation between two variables
title: Duration vs Satisfaction
mark: point
data:
  values:
    - { duration: 5, score: 3.2 }
    - { duration: 12, score: 4.1 }
    - { duration: 8, score: 3.8 }
encoding:
  x: { field: duration, type: quantitative, title: "Duration (min)" }
  y: { field: score, type: quantitative, title: Score }
```

#### Bubble Chart

```yaml
# Bubble — scatter with 3rd dimension as size
title: Product Portfolio
mark: point
data:
  values:
    - { product: A, revenue: 400, growth: 15, market: 25 }
    - { product: B, revenue: 300, growth: 8, market: 40 }
encoding:
  x: { field: revenue, type: quantitative }
  y: { field: growth, type: quantitative }
  size: { field: market, type: quantitative }
```

#### Heatmap

```yaml
# Heatmap — intensity matrix
title: Activity by Hour and Day
mark: rect
data:
  values:
    - { day: Mon, hour: 9, value: 12 }
    - { day: Mon, hour: 10, value: 25 }
    # ... full grid
encoding:
  x: { field: hour, type: ordinal }
  y: { field: day, type: nominal }
  color: { field: value, type: quantitative, title: Count }
```

---

### Category: Geographic

#### Choropleth (GeoJSON required)

```yaml
# Choropleth — region shading
title: Population by State
mark: geoshape
data:
  - name: states
    url: path/to/states.geojson
    format: { type: json }
  - name: population
    values:
      - { id: AL, pop: 4900000 }
      - { id: AK, pop: 730000 }
transform:
  - lookup: properties.id
    from: { data: population, key: id, fields: [pop] }
encoding:
  color: { field: pop, type: quantitative }
```

#### Symbol Map

```yaml
# Symbol Map — points on a map
title: Office Locations
layer:
  - mark: geoshape
    data: { url: path/to/world.geojson, format: { type: json } }
  - mark: point
    data:
      values:
        - { lon: -74.0, lat: 40.7, city: NYC }
        - { lon: -0.13, lat: 51.5, city: London }
    encoding:
      longitude: { field: lon, type: quantitative }
      latitude: { field: lat, type: quantitative }
      color: { field: city, type: nominal }
```

---

## Full Vega Specs (Exotic Chart Types)

For chart types not in Vega-Lite's native marks, use full Vega JSON. Same render script with `--vega` flag.

### Candlestick

```json
{
  "$schema": "https://vega.github.io/schema/vega/v5.json",
  "title": { "text": "AAPL Daily" },
  "data": [
    {
      "name": "ohlc",
      "values": [
        { "date": "01-Nov", "open": 150, "high": 155, "low": 148, "close": 153 },
        { "date": "02-Nov", "open": 153, "high": 157, "low": 151, "close": 155 }
      ]
    }
  ],
  "scales": [
    { "name": "x", "type": "band", "domain": { "data": "ohlc", "field": "date" }, "range": "width", "padding": 0.2 },
    { "name": "y", "type": "linear", "domain": { "data": "ohlc", "fields": ["high", "low"] }, "range": "height", "zero": false }
  ],
  "marks": [
    { "type": "rule", "from": { "data": "ohlc" }, "encode": {
      "enter": {
        "x": { "scale": "x", "field": "date", "band": 0.5 },
        "y": { "scale": "y", "field": "low" },
        "y2": { "scale": "y", "field": "high" },
        "stroke": { "value": "#333" }
      }
    }},
    { "type": "rect", "from": { "data": "ohlc" }, "encode": {
      "enter": {
        "x": { "scale": "x", "field": "date", "band": 0.25 },
        "width": { "scale": "x", "band": 0.5 },
        "y": { "scale": "y", "field": "open" },
        "y2": { "scale": "y", "field": "close" },
        "fill": [
          { "test": "datum.open <= datum.close", "value": "#4CAF50" },
          { "value": "#F44336" }
        ]
      }
    }}
  ]
}
```

### Waterfall

```json
{
  "$schema": "https://vega.github.io/schema/vega/v5.json",
  "title": { "text": "P&L Waterfall" },
  "data": [
    {
      "name": "table",
      "values": [
        { "label": "Revenue", "value": 1000, "type": "total" },
        { "label": "COGS", "value": -400, "type": "negative" },
        { "label": "Gross", "value": 600, "type": "running" },
        { "label": "OpEx", "value": -200, "type": "negative" },
        { "label": "EBIT", "value": 400, "type": "running" }
      ]
    }
  ],
  "scales": [
    { "name": "x", "type": "band", "domain": { "data": "table", "field": "label" }, "range": "width", "padding": 0.3 },
    { "name": "y", "type": "linear", "domain": [-500, 1100], "range": "height" }
  ],
  "marks": [
    {
      "type": "rect",
      "from": { "data": "table" },
      "encode": {
        "enter": {
          "x": { "scale": "x", "field": "label" },
          "width": { "scale": "x", "band": true },
          "fill": [
            { "test": "datum.type === 'negative'", "value": "#F44336" },
            { "test": "datum.type === 'total'", "value": "#4CAF50" },
            { "value": "#2196F3" }
          ]
        },
        "update": {
          "y": { "scale": "y", "field": "value", "band": 0.5 },
          "y2": { "scale": "y", "value": 0 }
        }
      }
    }
  ]
}
```

See `templates/` for full Vega specs: `candlestick.json`, `waterfall.json`, `sankey.json`, `radar.json`, `treemap.json`, `graph.json`.

---

## Layer & Composition

Vega-Lite supports layered charts for combining marks:

```yaml
# Layered: bars + line on same axes
title: Revenue & Growth Rate
layer:
  - mark: bar
    data: { values: [{ month: Jan, rev: 100 }, { month: Feb, rev: 140 }] }
    encoding:
      x: { field: month, type: nominal }
      y: { field: rev, type: quantitative }
  - mark: line
    data: { values: [{ month: Jan, growth: 5 }, { month: Feb, growth: 8 }] }
    encoding:
      x: { field: month, type: nominal }
      y: { field: growth, type: quantitative, axis: { title: "Growth %" } }
      color: { value: "#E3120B" }
resolve:
  scale: { y: independent }
```

---

## Encoding Reference

| Property | Options | Description |
|----------|---------|-------------|
| `field` | string | Column name in data |
| `type` | `nominal`, `ordinal`, `quantitative`, `temporal`, `geojson` | Data type |
| `title` | string or `null` | Axis/legend title (null = hide) |
| `sort` | `"-x"`, `"-y"`, array | Sort order |
| `aggregate` | `sum`, `mean`, `count`, `median`, `min`, `max` | Aggregation |
| `bin` | `true` or `{ maxbins: 20 }` | Bin continuous data |
| `timeUnit` | `yearmonth`, `month`, `year` | Temporal granularity |
| `stack` | `zero`, `normalize`, `center` | Stacking behavior |
| `scale` | `{ zero: false }`, `{ domain: [0, 100] }` | Axis scaling |
