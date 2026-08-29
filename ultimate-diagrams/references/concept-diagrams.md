# concept-diagrams Reference

A secondary engine for educational/scientific/physical diagrams that fireworks-tech-graph doesn't target well. See https://github.com/NousResearch/concept-diagrams.

## Domain Coverage

| Domain | Diagram Types | Example |
|--------|--------------|---------|
| Physics | Structural | Force diagrams, circuit schematics, optics ray tracing |
| Chemistry | Flowchart / Structural | Reaction pathways, molecular structure, periodic trends |
| Biology | Structural / Flowchart | Cell anatomy, metabolic pathways, phylogenetic trees |
| Anatomy | Physical | Skeletal system, organ diagrams, cross-sections |
| Engineering | Physical / Infrastructure | Aircraft cross-sections, turbine diagrams, floor plans |
| Computer Science | API Map / Microservice | Graph algorithms, protocol layers, memory layouts |

## Diagram Types (8)

| Type | Description | Use Case |
|------|-------------|----------|
| `flowchart` | Process flow with decisions | Scientific workflows, experimental procedures |
| `structural` | Hierarchical decomposition | Cell structure, atomic models, taxonomy |
| `api_map` | Interface / contract mapping | API endpoints, protocol layers |
| `microservice` | Service topology | Distributed system architecture |
| `data_flow` | Information movement | Lab data pipeline, simulation I/O |
| `physical` | Physical object diagram | Aircraft cross-section, smartphone teardown |
| `infrastructure` | Network / hardware topology | Lab network, server rack layout |
| `ui_mockup` | Interface wireframe | Lab instrument UI, dashboard mockup |

## Color Ramps (9)

| Ramp | Light | Dark | Use Case |
|------|-------|------|----------|
| Slate | `#64748b` | `#94a3b8` | Neutral structure, backgrounds |
| Blue | `#3b82f6` | `#60a5fa` | Data flow, information |
| Green | `#22c55e` | `#4ade80` | Success, growth, biological |
| Red | `#ef4444` | `#f87171` | Error, critical, hot zones |
| Amber | `#f59e0b` | `#fbbf24` | Warning, cache, caution |
| Purple | `#a855f7` | `#c084fc` | AI, inference, thought |
| Teal | `#14b8a6` | `#2dd4bf` | Network, streaming, liquids |
| Rose | `#f43f5e` | `#fb7185` | Security, auth, vital signs |
| Cyan | `#06b6d4` | `#22d3ee` | Storage, persistence, cold |

## Auto Dark Mode

concept-diagrams automatically detects system preference. Override explicitly:

```html
<html data-theme="light">
<html data-theme="dark">
```

## Usage

```bash
# Clone the repository
git clone https://github.com/NousResearch/concept-diagrams.git
cd concept-diagrams

# Generate a diagram
python concept_diagram.py \
  --type structural \
  --subject physics \
  --config my_config.yaml \
  --output diagram.html

# The output is a standalone HTML file — open in any browser, or convert to PDF
```

## Configuration YAML

```yaml
type: structural
subject: physics
theme: auto
width: 1200
height: 900
elements:
  - type: node
    id: nucleus
    label: Nucleus
    color: red
    position: [400, 300]
  - type: node
    id: electron
    label: Electron
    color: blue
    position: [600, 200]
  - type: edge
    from: nucleus
    to: electron
    label: Coulomb Force
    style: dashed
```

## Output

- Single standalone HTML file (no external dependencies)
- Auto light/dark mode
- Scalable, print-ready
- Embedded CSS (no external stylesheets needed)
