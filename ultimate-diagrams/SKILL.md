---
name: ultimate-diagrams
description: Generate production-grade technical diagrams and system visuals — system architecture, cloud infrastructure, UML (all 14 types), AI/agent workflows (RAG, ReAct, multi-agent), C4 model, event-driven/message queue architectures, network topology, data flow pipelines, SRE/observability diagrams, and educational/scientific concept diagrams (physics, chemistry, biology, engineering). Uses fireworks-tech-graph CLI when installed for SVG/PNG output; otherwise uses a built-in HTML+SVG generator to produce standalone diagrams with PDF export. This is THE skill for ANY technical diagram or system visual — distinct from charts (data visualization) and flowcharts (process/business flow). Trigger whenever the user asks for a diagram of a system, architecture, network, topology, infrastructure, UML model, agent workflow, pipeline, or technical concept visualization — even if they don't explicitly name a specific diagram type.
license: MIT
---

# Ultimate Diagrams — Hybrid CLI/Built-in Engine

Generate production-grade technical diagrams using the best available engine. This skill supports **two rendering paths** that produce equivalent output quality:

| Path | When to Use | Output |
|------|-------------|--------|
| **CLI** (fireworks-tech-graph) | When `fireworks-cli` is available on the system | SVG, PNG, GIF — geometry-validated, semantic shapes |
| **Built-in** (HTML+SVG) | Fallback when CLI unavailable — always works | Standalone HTML + optional PDF via `scripts/generate_pdf.py` |

The skill automatically detects which path is available. Both produce equivalent visual quality.

---

## Quick Start

```python
import os, subprocess

# Check if fireworks-cli is available:
CLI_AVAILABLE = subprocess.run(["which", "fireworks-cli"] if os.name != "nt" else ["where", "fireworks-cli.exe"], capture_output=True).returncode == 0
```

If `CLI_AVAILABLE` is True, use the CLI path. Otherwise, use the built-in HTML+SVG generator described in this skill.

---

## Engine Selection

| Context | Primary Engine | Output Format | Why |
|---------|---------------|---------------|-----|
| **System architecture, cloud infra, microservices** | CLI preferred → Built-in fallback | SVG / standalone HTML | 12 visual styles, semantic boundaries, rectilinear routing |
| **UML diagrams** (all 14 types) | CLI preferred → Built-in fallback | SVG / standalone HTML | Full UML suite: class, sequence, state machine, activity, component, deployment, use case, communication, timing, interaction overview, composite structure, profile, object, package |
| **AI/Agent workflows** (RAG, ReAct, multi-agent) | CLI preferred → Built-in fallback | SVG / standalone HTML | Specialized shapes: LLM=double-border, Agent=hexagon, VectorStore=ringed cylinder |
| **C4 model** (Context/Container/Component) | CLI preferred → Built-in fallback | SVG / standalone HTML | Progressive disclosure, typed elements, protocol annotations |
| **Event-driven / message queues** | CLI preferred → Built-in fallback | SVG / standalone HTML | Topic rails, consumer groups, junction bridges |
| **Network topology** | CLI preferred → Built-in fallback | SVG / standalone HTML | Subnet grouping, device types, traffic flows |
| **Data flow / ETL pipelines** | CLI preferred → Built-in fallback | SVG / standalone HTML | Source→transform→sink, parallel paths |
| **SRE / observability** (golden signals, traces) | CLI preferred → Built-in fallback | SVG / standalone HTML | Ops-pulse style, critical paths, heatmaps |
| **Educational / scientific** (physics, chemistry, biology, engineering) | Built-in (HTML+SVG) | Standalone HTML | 9 semantic color ramps, auto dark mode, flat minimalist design system |
| **Physical / mechanical** (aircraft, turbines, floor plans) | Built-in (HTML+SVG) | Standalone HTML | Exploded views, cross-sections, scale-accurate layouts |
| **Quick sketch / brainstorming** | Built-in (HTML+SVG, sketch style) | Standalone HTML | Hand-drawn aesthetic, rapid iteration |

---

## Path A: CLI Engine (fireworks-tech-graph)

Use when `fireworks-cli` is installed.

### Prerequisites

```bash
npm install -g fireworks-tech-graph
# Verify:
fireworks-cli --version
```

### Diagram Type Coverage

| Category | Diagram Types | Style | 
|----------|--------------|-------|
| **System Architecture** | Cloud infra, microservices, VPCs, deployment | `architecture` |
| **AI / Agent Workflow** | RAG loops, ReAct cycles, multi-agent orchestration | `agent` |
| **UML** (14 types) | Class, sequence, state machine, activity, component, deployment, use case, communication, timing, interaction overview, composite structure, profile, object, package | `sequence` / `uml` |
| **C4 Model** | Context (L1), Container (L2), Component (L3) | `c4-review` |
| **Event-Driven** | Message queues, Kafka topics, event streams | `event-transit` |
| **Data Flow** | ETL pipelines, stream processing | `dataflow` |
| **Memory / Storage** | Cache hierarchies, vector DBs, tiering | `memory-tiering` |
| **Ops / SRE** | Golden signals, critical paths, trace trees | `ops-pulse` |
| **Comparison** | Feature parity, benchmarks, decision matrices | `comparison` |
| **Mind Map** | Brainstorming, knowledge graphs | `mindmap` |
| **Logic Flowchart** | Decision trees, business logic | `flowchart` |
| **Network Topology** | Subnets, routing, device topologies | `cloud-fabric` |

### CLI Workflow

```bash
# 1. Write a JSON spec for your diagram
cat > diagram.json << 'EOF'
{
  "type": "agent",
  "nodes": [
    {"id": "user", "label": "User", "role": "actor"},
    {"id": "llm", "label": "Claude 3.5", "role": "reasoning_engine"},
    {"id": "tools", "label": "Search Tool", "role": "tool"},
    {"id": "memory", "label": "Vector Store", "role": "vector_db"}
  ],
  "edges": [
    {"from": "user", "to": "llm", "kind": "sync_request"},
    {"from": "llm", "to": "tools", "kind": "async_event"},
    {"from": "tools", "to": "llm", "kind": "sync_response"},
    {"from": "llm", "to": "memory", "kind": "async_event"}
  ]
}
EOF

# 2. Render to SVG
fireworks-cli render \
  --type agent \
  --input diagram.json \
  --output diagram.svg \
  --style technical

# 3. (Optional) Render to high-res PNG
fireworks-cli render \
  --type agent \
  --input diagram.json \
  --output diagram.png \
  --width 1920

# 4. (Optional) Generate animated motion GIF
fireworks-cli render \
  --type agent \
  --input diagram.json \
  --output diagram.gif \
  --animate
```

### The render_diagram.py wrapper

The `scripts/render_diagram.py` wraps the CLI with sensible defaults and better error messages:

```bash
python scripts/render_diagram.py --type agent --input spec.json --output diagram.svg
python scripts/render_diagram.py --type sequence --input spec.json --output diagram.png --width 1920
```

If fireworks-cli is not installed, the script prints the spec as a JSON preview — this is a signal to switch to the **Built-in** path.

### Semantic Arrow System (for reference in both paths)

Arrows encode protocol semantics through color + dash pattern combinations:

| Arrow Style | Line Type | Semantic Meaning | SVG Equivalent |
|------------|-----------|-----------------|---------------|
| **Solid** | Full line | Synchronous request | `stroke-dasharray="none"` |
| **Dashed** | Dashed line | Asynchronous event | `stroke-dasharray="6,3"` |
| **Double** | Parallel lines | Bi-directional sync | Two parallel `<line>` elements |
| **Thick** | Bold line | High-throughput stream | `stroke-width="4"` |
| **Bridge** | Arc with mask | Non-intersecting crossing | Arc `<path>` with gap |

### CLI Visual Styles (12 Total)

| Style ID | Name | Best For |
|----------|------|----------|
| 1 | `system-architecture` | Cloud infra, microservices, VPCs |
| 2 | `dataflow` | ETL, stream processing, pipelines |
| 3 | `agentic-workflow` | LLM chains, RAG loops, agents |
| 4 | `sequence` | API calls, auth flows, lifelines |
| 5 | `memory-tiering` | Cache hierarchies, vector DBs |
| 6 | `comparison` | Feature parity, benchmarks |
| 7 | `concept-mindmap` | Brainstorming, knowledge graphs |
| 8 | `logic-flowchart` | Decision trees, business logic |
| 9 | `c4-review` | C4 model progressive disclosure |
| 10 | `cloud-fabric` | Deployment boundaries, ownership |
| 11 | `event-transit` | Event-driven systems, topics |
| 12 | `ops-pulse` | Observability, SRE, golden signals |

---

## Path B: Built-in HTML+SVG Generator

Use when fireworks-cli is not available. This path generates a **standalone HTML file** with inline SVG, which can be viewed in any browser and optionally converted to PDF.

### Universal Output Structure

Every built-in diagram is a single, self-contained HTML file:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    @page { size: A4 landscape; margin: 0.4in; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
           background: #eff1f5; color: #4c4f69; }
    .page { padding: 0.4in; min-height: 100vh; }
    .title { font-size: 26px; font-weight: 800; margin-bottom: 2px;
             color: #4c4f69; letter-spacing: -0.02em; }
    .subtitle { font-size: 14px; color: #6c6f85; margin-bottom: 24px; }
    svg.diagram { width: 100%; height: auto; display: block;
                  background: #eff1f5; border-radius: 8px; }
    .legend { margin-top: 20px; padding: 14px 18px; background: #e6e9ef;
              border-radius: 10px; font-size: 11px;
              display: flex; gap: 20px; flex-wrap: wrap; }
    .legend-item { display: flex; align-items: center; gap: 8px; }
    .legend-swatch { width: 20px; height: 2px; }
    @media (prefers-color-scheme: dark) {
      body { background: #1e1e2e; color: #cdd6f4; }
      .page { background: #1e1e2e; }
      .title { color: #cdd6f4; }
      .subtitle { color: #a6adc8; }
      svg.diagram { background: #1e1e2e; }
      .legend { background: #313244; }
    }
  </style>
</head>
<body>
  <div class="page">
    <div class="title">Diagram Title</div>
    <div class="subtitle">Description or context</div>
    <svg class="diagram" viewBox="0 0 1600 1000" xmlns="http://www.w3.org/2000/svg">
      <!-- Diagram elements go here -->
    </svg>
    <div class="legend">
      <!-- Arrow/shape legend for technical diagrams -->
    </div>
  </div>
</body>
</html>
```

### Color Palette — Catppuccin Latte (Default)

Use the **Catppuccin Latte** palette by default — it's warm, readable, and print-friendly. The dark variant (Catppuccin Mocha) is provided for presentations or dark-mode contexts. These are the exact tokens to use in your CSS:

```css
/* ════════════════════════════════════════════
   Catppuccin Latte (Light — DEFAULT)
   ════════════════════════════════════════════ */
:root {
  --bg-page:       #eff1f5;
  --bg-node:       #e6e9ef;
  --bg-group:      #dce0e8;
  --bg-highlight:  #fce5c2;

  --border-node:   #bcc0cc;
  --border-group:  #9ca0b0;
  --line-connector:#acb0be;
  --line-sync:     #1e66f5;
  --line-async:    #9ca0b0;
  --line-stream:   #8839ef;

  --text-primary:  #4c4f69;
  --text-secondary:#6c6f85;
  --text-muted:    #9ca0b0;
  --text-on-color: #eff1f5;

  --accent-blue:   #1e66f5;
  --accent-green:  #40a02b;
  --accent-red:    #d20f39;
  --accent-amber:  #df8e1d;
  --accent-purple: #8839ef;
  --accent-teal:   #179299;
  --accent-rose:   #e64553;
  --accent-cyan:   #04a5e5;
  --accent-lavender:#7287fd;
  --accent-mauve:  #8839ef;
  --accent-peach:  #fe640b;
  --accent-pink:   #ea76cb;
  --accent-sky:    #209fb5;

  --fill-llm:      #f4e8ff;
  --fill-agent:    #e1eeff;
  --fill-storage:  #e2f4e0;
  --fill-actor:    #fef1d5;
  --fill-database: #e6e9ef;
  --fill-queue:    #fde8f0;
  --fill-decision: #fce5c2;
}

/* ════════════════════════════════════════════
   Catppuccin Mocha (Dark — for presentations)
   ════════════════════════════════════════════ */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-page:       #1e1e2e;
    --bg-node:       #313244;
    --bg-group:      #45475a;
    --bg-highlight:  #37291e;

    --border-node:   #585b70;
    --border-group:  #6c7086;
    --line-connector:#6c7086;
    --line-sync:     #89b4fa;
    --line-async:    #6c7086;
    --line-stream:   #cba6f7;

    --text-primary:  #cdd6f4;
    --text-secondary:#a6adc8;
    --text-muted:    #6c7086;
    --text-on-color: #1e1e2e;

    --accent-blue:   #89b4fa;
    --accent-green:  #a6e3a1;
    --accent-red:    #f38ba8;
    --accent-amber:  #f9e2af;
    --accent-purple: #cba6f7;
    --accent-teal:   #94e2d5;
    --accent-rose:   #f5c2e7;
    --accent-cyan:   #89dceb;

    --fill-llm:      #392e55;
    --fill-agent:    #263b54;
    --fill-storage:  #223d2a;
    --fill-actor:    #4a3b22;
    --fill-database: #313244;
    --fill-queue:    #4a2840;
    --fill-decision: #4a3b22;
  }
}
**Use this exact palette.** Don't invent new colors. The warm latte background (`#eff1f5`) with the muted text (`#4c4f69`) and clean blue accents (`#1e66f5`) is what makes the output look polished and professional.

### Shape Vocabulary (Built-in Path)

Maintain consistent visual semantics. The shape of a node tells the reader what kind of thing it is:

| Shape | SVG Element | Semantic Meaning | Example Usage |
|-------|------------|-----------------|---------------|
| **Rounded rectangle** | `<rect rx="6">` | Generic service / component | App server, microservice, function |
| **Double-border rectangle** | `<rect rx="6">` with inner `<rect>` | LLM / AI model | GPT-4, Claude, LLaMA |
| **Hexagon** | `<polygon points="...">` | Agent / autonomous process | AI Agent, orchestrator, crawler |
| **Cylinder** | `<ellipse>` + `<rect>` | Database / storage | PostgreSQL, S3, Redis |
| **Pill** | `<rect rx="20">` | Queue / topic / stream | Kafka topic, SQS queue, event bus |
| **Diamond** | `<polygon points="...">` | Decision / branch | Router, conditional, gateway |
| **Circle / oval** | `<circle>` or `<ellipse>` | Actor / user / external | End user, external system |
| **Rounded square** | `<rect rx="4">` | Generic node | Default for unspecified types |
| **Edge line** | `<line>` or `<path>` | Connection / flow | API call, data flow, message |
| **Dashed edge** | `<line stroke-dasharray="6,3">` | Async / indirect | Event emission, webhook, callback |
| **Bold edge** | `<line stroke-width="4">` | Stream / high-throughput | Data stream, video feed, log flow |

### Coordinate System Convention

Use an adaptive `viewBox` that fits your content. The default for simple diagrams is `viewBox="0 0 1600 1000"` (wider A4 landscape). For complex diagrams with many elements, scale up — `2000 1200` or even `2400 1600`. The SVG will scale to fit the page width. **Use the grid. Place every element at explicit (x, y) coordinates on a 40px or 20px grid.**

```
+--(0,0)-------------------(1600,0)---+
|                                       |
|   [Title (centered, y=60)]           |
|   [Subtitle (centered, y=90)]        |
|                                       |
|   <--- diagram content region --->    |
|   Top margin area: 120px             |
|   Content area: y=120 to y=900       |
|   Bottom margin area: y=900-960      |
|                                       |
+--(0,1000)-----------------(1600,1000)-+
```

**Canvas sizing rules of thumb:**
| Number of Elements | Recommended viewBox | Spacing Grid |
|---|---|---|
| Up to 8 nodes | `1600 1000` | 40px |
| 8-15 nodes | `2000 1200` | 50px |
| 15-25 nodes | `2400 1600` | 60px |
| 25+ nodes | `3000 2000` or larger | 80px |

**Why this matters:** Complex diagrams with many nodes, edges, and labels need room to breathe. A cramped canvas causes overlapping nodes, clipped text, and unreadable labels. When in doubt, use a larger canvas — the HTML scales down to fit the page width, and the viewer can always zoom in.

---

## Built-in Layout Patterns by Diagram Type

### 1. System Architecture

**When to use**: Cloud infrastructure, microservices, deployment topology, service mesh.

**Layout strategy**: Group related services inside boundary boxes (representing VPCs, regions, or clusters). Services flow top-to-bottom or left-to-right. Use dashed boundary boxes for logical groupings.

```
┌──────────────────────────────────────────────────────────┐
│  ┌─ VPC ────────────────────────────────────────────┐   │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐    │   │
│  │  │  Load    │───▶│  App     │───▶│  Cache   │    │   │
│  │  │  Balancer│    │  Server  │    │  (Redis) │    │   │
│  │  └──────────┘    └──────────┘    └──────────┘    │   │
│  │                       │                           │   │
│  │                       ▼                           │   │
│  │                  ┌──────────┐    ┌──────────┐    │   │
│  │                  │  Primary │───▶│  Replica │    │   │
│  │                  │  DB      │    │  DB      │    │   │
│  │                  └──────────┘    └──────────┘    │   │
│  └──────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

**SVG recipe**:
- Use `<rect rx="8" fill="var(--bg-group)" stroke="var(--border-group)" stroke-dasharray="8,4">` for boundary boxes (VPC, region, cluster)
- Use `<rect rx="6" fill="var(--bg-node)" stroke="var(--border-node)">` for service nodes
- Use `<path marker-end="url(#arrow)">` for connections
- Place boundary box labels top-left inside the box using `<text>`

**Example coordinate layout** (1200×800 viewBox):
```
Center column (X=500 to X=700):   Core services
Left column  (X=100 to X=350):    Client / edge services  
Right column (X=800 to X=1050):   Data / storage services
Boundary boxes:                    VPC at Y=80 to Y=750 (full height)
                                  Public subnet Y=120-300
                                  Private subnet Y=320-720
```

### 2. AI / Agent Workflow

**When to use**: RAG loops, ReAct cycles, multi-agent orchestration, LLM chains, AI pipelines.

**Layout strategy**: Process flow left-to-right or as a feedback loop. Use **semantic shapes** to distinguish component types:
- LLMs get **double-border rectangles** — they're the reasoning engine
- Agents get **hexagons** — they take actions
- Vector stores get **cylinders** — they persist and retrieve
- Users get **circles/ovals** — they're human actors
- Tools get **rounded rectangles** — they're functions

```
    ┌────(User)────┐
         │    ▲
         ▼    │
    ┌╌╌╌╌╌╌╌╌╌╌┐       Sync request (solid)
    ╎  Claude   ╎  ──▶  ┌──────────┐
    ╎  3.5 Sonnet╎       │  Search  │
    └╌╌╌╌╌╌╌╌╌╌┘  ◀──  │  Tool    │
         │               └──────────┘
         ▼
    ┌──────────┐       Async event (dashed)
    │  Vector  │  ◀──  (embedding update)
    │  Store   │
    └──────────┘
```

**SVG recipe for double-border LLM**:
```svg
<!-- Outer rect -->
<rect x="450" y="200" width="200" height="60" rx="8"
      fill="var(--fill-llm)" stroke="var(--accent-purple)" stroke-width="2"/>
<!-- Inner rect (double-border effect) -->
<rect x="454" y="204" width="192" height="52" rx="6"
      fill="none" stroke="var(--accent-purple)" stroke-width="1.5"/>
<text x="550" y="228" text-anchor="middle" font-weight="600">Claude 3.5</text>
<text x="550" y="246" text-anchor="middle" font-size="11" fill="var(--text-muted)">LLM Reasoning Engine</text>
```

**SVG recipe for hexagon agent**:
```svg
<!-- Hexagon: center at (500,300), width 180, height 50 -->
<polygon points="410,300 500,275 590,300 500,325"
         fill="var(--fill-agent)" stroke="var(--accent-blue)" stroke-width="2"/>
<text x="500" y="305" text-anchor="middle" font-weight="600">Research Agent</text>
```

**SVG recipe for cylinder (vector store)**:
```svg
<!-- Cylinder body -->
<rect x="450" y="420" width="200" height="50" rx="0"
      fill="var(--fill-storage)" stroke="var(--accent-cyan)" stroke-width="1.5"/>
<!-- Cylinder top ellipse -->
<ellipse cx="550" cy="420" rx="100" ry="12"
         fill="var(--fill-storage)" stroke="var(--accent-cyan)" stroke-width="1.5"/>
<!-- Cylinder bottom ellipse -->
<ellipse cx="550" cy="470" rx="100" ry="12"
         fill="var(--fill-storage)" stroke="var(--accent-cyan)" stroke-width="1.5"/>
<text x="550" y="450" text-anchor="middle" font-weight="600">Vector Store</text>
```

### 3. UML Sequence Diagram

**When to use**: API call flows, authentication sequences, protocol handshakes, interaction protocols.

**Layout strategy**: Vertical lifelines with horizontal message arrows. Time flows downward. Each participant gets a vertical dashed line (the lifeline). Activation bars (thin rectangles on the lifeline) show when a participant is active.

```
  Client        API Gateway      Auth Service       User DB
    │                │                │                │
    │── POST /login ─▶               │                │
    │                │── validate() ─▶│                │
    │                │                │── SELECT ────▶│
    │                │                │◀── user data ─│
    │                │◀── JWT token ─│                 │
    │◀── 200 OK ────│                │                │
```

**Coordinate layout** (1200×800 viewBox):
```
Lifeline X positions: evenly spaced at X=150, X=400, X=650, X=900, X=1050
Lifeline Y range:     Y=150 to Y=700
Messages:             Horizontal lines between lifelines, Y increments by 60-80px
```

**SVG recipe**:
```svg
<!-- Lifeline -->
<line x1="150" y1="130" x2="150" y2="700"
      stroke="var(--line-connector)" stroke-width="1.5" stroke-dasharray="6,4"/>

<!-- Actor box at top -->
<rect x="100" y="80" width="100" height="40" rx="4"
      fill="var(--bg-node)" stroke="var(--border-node)"/>
<text x="150" y="105" text-anchor="middle" font-weight="600" font-size="13">Client</text>

<!-- Sync arrow (solid) -->
<line x1="150" y1="200" x2="400" y2="200"
      stroke="var(--line-sync)" stroke-width="2" marker-end="url(#arrowSync)"/>
<text x="275" y="194" text-anchor="middle" font-size="11" fill="var(--text-secondary)">POST /login</text>

<!-- Activation bar -->
<rect x="392" y="200" width="16" height="30" fill="var(--accent-blue)" opacity="0.3" rx="2"/>

<!-- Response arrow (dashed or solid return) -->
<line x1="650" y1="360" x2="400" y2="360"
      stroke="var(--line-async)" stroke-width="1.5" stroke-dasharray="6,3" marker-end="url(#arrowReturn)"/>
<text x="525" y="354" text-anchor="middle" font-size="11" fill="var(--text-secondary)">JWT token</text>
```

**Arrow markers** (add to `<defs>` section):
```svg
<defs>
  <marker id="arrowSync" viewBox="0 0 10 10" refX="10" refY="5"
          markerWidth="8" markerHeight="8" orient="auto">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--line-sync)"/>
  </marker>
  <marker id="arrowReturn" viewBox="0 0 10 10" refX="10" refY="5"
          markerWidth="8" markerHeight="8" orient="auto">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--line-async)"/>
  </marker>
  <marker id="arrowData" viewBox="0 0 10 10" refX="10" refY="5"
          markerWidth="8" markerHeight="8" orient="auto">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--line-stream)"/>
  </marker>
</defs>
```

### 4. Event-Driven Architecture

**When to use**: Kafka/messaging systems, event streams, pub/sub architectures, queue-based designs.

**Layout strategy**: Topics (pill shapes) in a horizontal rail at center. Producers above push events in; consumers below pull events out. Consumer groups shown as grouped boxes below topics.

```
  ┌─────────┐    ┌──────────┐    ┌───────────┐
  │  Web    │    │  Mobile  │    │  Cron     │
  │  App    │    │  App     │    │  Job      │
  └────┬────┘    └────┬─────┘    └─────┬─────┘
       │              │               │
       ▼              ▼               ▼
  ════════════════════════════════════════════ (Event Bus)
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │  Orders  │  │Payments  │  │Notific.  │
  │  Topic   │  │Topic     │  │Topic     │
  └────┬─────┘  └────┬─────┘  └────┬─────┘
       │              │             │
       ▼              ▼             ▼
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │Inventory │  │Billing   │  │Email     │
  │Service   │  │Service   │  │Service   │
  └──────────┘  └──────────┘  └──────────┘
```

**Coordinate layout** (1200×800 viewBox):
```
Producers:     Y=120-220, distributed horizontally (X=150, 450, 750, 950)
Topic rail:    Y=280-350, pill shapes with event bus line through them
Consumers:     Y=420-520, grouped under topics
Consumer grps: Y=560-620, dashed boxes around related consumers
```

**SVG recipe for topic pill**:
```svg
<!-- Topic pill -->
<rect x="150" y="280" width="200" height="50" rx="25"
      fill="var(--fill-queue)" stroke="var(--accent-rose)" stroke-width="2"/>
<text x="250" y="310" text-anchor="middle" font-weight="600">Orders Topic</text>

<!-- Event bus line -->
<line x1="0" y1="305" x2="1200" y2="305"
      stroke="var(--line-connector)" stroke-width="1" stroke-dasharray="4,4"/>
```

### 5. C4 Model (Context/Container/Component)

**When to use**: Software architecture documentation following the C4 model. Three levels: L1=System Context, L2=Container, L3=Component.

**Layout strategy**: Nested boundary boxes showing progressive detail. The outermost box is the system boundary. Inside are containers (services, databases, etc.) with technology annotations.

**L2 Container diagram layout**:
```
┌─ System: E-Commerce Platform ──────────────────────────────┐
│                                                              │
│  [Person] ──▶ ┌──[SPA]──────┐    ┌──[API Gateway]────────┐ │
│  Customer     │  React       │    │  FastAPI              │ │
│               │  User-facing │    │  Request routing      │ │
│               └─────────────┘    └────────┬───────────────┘ │
│                                           │                  │
│              ┌──[Background Wkrs]────┐    │                  │
│              │  Celery               │◀───┘                  │
│              │  Async processing     │                       │
│              └────────┬──────────────┘                       │
│                       │                                      │
│              ┌────────▼──────────────┐                       │
│              │  [Database]           │                       │
│              │  PostgreSQL           │                       │
│              │  Persistence          │                       │
│              └───────────────────────┘                       │
└──────────────────────────────────────────────────────────────┘
```

**SVG recipe for C4 container**:
```svg
<!-- Container node with tech label -->
<rect x="350" y="200" width="240" height="70" rx="6"
      fill="var(--bg-node)" stroke="var(--accent-blue)" stroke-width="2"/>
<rect x="350" y="200" width="240" height="24" rx="6"
      fill="var(--accent-blue)" opacity="0.1"/>
<text x="350" y="215" font-size="10" fill="var(--accent-blue)" font-weight="600">[Container: FastAPI]</text>
<text x="470" y="240" text-anchor="middle" font-weight="600">API Gateway</text>
<text x="470" y="256" text-anchor="middle" font-size="11" fill="var(--text-secondary)">Request routing and auth</text>

<!-- Person/actor (stick figure style) -->
<circle cx="120" cy="235" r="16" fill="var(--fill-actor)" stroke="var(--accent-amber)" stroke-width="2"/>
<line x1="120" y1="251" x2="120" y2="280" stroke="var(--accent-amber)" stroke-width="2"/>
<line x1="100" y1="260" x2="140" y2="260" stroke="var(--accent-amber)" stroke-width="2"/>
<line x1="120" y1="280" x2="100" y2="305" stroke="var(--accent-amber)" stroke-width="2"/>
<line x1="120" y1="280" x2="140" y2="305" stroke="var(--accent-amber)" stroke-width="2"/>
<text x="120" y="320" text-anchor="middle" font-weight="600">Customer</text>
<text x="120" y="334" text-anchor="middle" font-size="10" fill="var(--text-muted)">[Person]</text>
```

### 6. Data Flow / ETL Pipeline

**When to use**: Data pipelines, ETL jobs, stream processing, data movement diagrams.

**Layout strategy**: Left-to-right flow from sources → transforms → sinks. Parallel paths shown stacked vertically. Use cylinder shapes for data stores, rounded rects for processors.

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Raw     │───▶│  Clean   │───▶│ Validate │───▶│ Analyze  │
│  Data    │    │          │    │          │    │          │
│  (S3)    │    │          │    │          │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                                                    │
                                                    ▼
                                              ┌──────────┐
                                              │  Dashbd  │
                                              │  (BI)    │
                                              └──────────┘
```

---

## PDF Export (Both Paths)

After generating the diagram (SVG from CLI or HTML from built-in), offer to package it as a print-ready PDF:

```bash
# For built-in HTML output:
python <project_root>/scripts/generate_pdf.py output.html output.pdf [--landscape] [--paper-size A4]
```

The script tries Playwright first (best quality), then WeasyPrint, then pdfkit.

---

## Complete Workflow (Step by Step)

1. **Understand the request** — What kind of diagram? What's the content hierarchy?
2. **Choose the diagram type** — System architecture? UML? AI workflow? Event-driven?
3. **Check CLI availability** — `where fireworks-cli.exe` (Windows) or `which fireworks-cli` (Mac/Linux)
4. **Write a JSON spec** — Capture all nodes, edges, and metadata in a JSON file
5. **Render via best available path**:
   - CLI available → `fireworks-cli render ...` or `python scripts/render_diagram.py ...`
   - CLI unavailable → Generate HTML+SVG using the built-in patterns above
6. **Output the diagram** — Display it or save to file
7. **Optional: PDF export** — Run `scripts/generate_pdf.py` for a print-ready PDF
8. **Verify the output** — Check for clipped text, overlapping elements, missing labels

---

## References

- `references/diagram-types.md` — All supported diagram types with JSON spec examples
- `references/builtin-layouts.md` — Full layout patterns for the built-in generator
- `scripts/render_diagram.py` — CLI wrapper script
- Scripts from the parent project: `<project_root>/scripts/generate_pdf.py` — HTML→PDF

---

## Design Principles

- **Semantic shapes encode meaning** — Don't use rectangles for everything. A hexagon says "agent," a double-border says "LLM," a cylinder says "storage." Readers understand the diagram faster when shapes carry meaning.
- **Arrow styles encode protocol** — Solid = sync request, dashed = async event, bold = stream. Consistent arrow semantics make the "wiring" of the system readable at a glance.
- **Group related elements** — Use boundary boxes (VPC, subnet, region, cluster) with dashed strokes and light fills to group related services. Label the boundary, not just the services inside.
- **Include a legend** — Technical diagrams always include a small legend (bottom-right) explaining the shape and arrow conventions used.
- **Dark mode by default** — Generate diagrams with `@media (prefers-color-scheme: dark)` support so they look good in both light and dark contexts.
- **Coordinate precision** — Place every element at explicit (x, y) coordinates on a 20px grid. Don't rely on auto-layout. Measure and verify.
