# Visual Language and Style Matrix

The fireworks-tech-graph library supports twelve distinct diagram types, each optimized for specific engineering domains.

## Standard Styles (1-8)

| Diagram Type | Primary Use Case | Key Visual Elements | Color Palette Focus |
|-------------|-----------------|--------------------|--------------------|
| **System Architecture** | Cloud infrastructure, microservices | Isometric boxes, cloud icons | Blue (Compute), Green (Storage) |
| **Data Flow** | ETL pipelines, stream processing | Cylinders (Storage), Rounded Rects | Gradient blues, thick arrows |
| **Agentic Workflow** | LLM chains, RAG loops | Brain icons (LLM), Tool icons | Purple (Intelligence), Teal (Tools) |
| **Sequence Diagram** | API calls, auth flows | Lifelines, activation bars | Monochromatic with highlights |
| **Memory Tiering** | Cache hierarchies, vector DBs | Pyramids, latency-capacity scales | Heatmap (Red to Blue) |
| **Comparison Matrix** | Feature parity, benchmarks | Quadrants, feature tables | Green (Pass), Red (Fail) |
| **Concept Mind Map** | Brainstorming, knowledge graphs | Central nodes, radiating branches | Multi-color branching |
| **Logic Flowchart** | Decision trees, business logic | Diamonds (Decisions), Rectangles | Logic-driven (True/False) |

## Advanced Engineering Styles (9-12)

| Style ID | Name | Primary Use Case | Semantic Requirements |
|----------|------|-----------------|----------------------|
| 9 | `c4-review` | C4 Model reviews | Typed elements, responsibilities, protocols |
| 10 | `cloud-fabric` | Deployment boundaries | Acyclic boundaries, explicit ownership |
| 11 | `event-transit` | Event-driven systems | Topic rails, junctions, consumer groups |
| 12 | `ops-pulse` | Observability and SRE | Golden signals, critical paths, trace trees |

## Semantic Arrow Definitions

Arrows in fireworks-tech-graph carry semantic weight. Use the following standards to ensure technical clarity:

| Arrow Style | Line Pattern | Semantic Meaning | Usage Example |
|------------|-------------|-----------------|---------------|
| **Solid** | `──────────` | Synchronous Request | REST API call, Direct Function Call |
| **Dashed** | `- - - - - -` | Asynchronous Event | Message Queue, Webhook, Callback |
| **Double** | `══════════` | Bi-directional Sync | WebSocket, Database Replication |
| **Thick** | `━━━━━━━━━━` | High-Throughput Stream | Kafka Stream, Video Feed |
| **Bridge** | Arc with mask | Path Crossing | Non-intersecting edge crossing |

## Semantic Shape Vocabulary

Shapes encode entity roles in the diagram. Do not use shapes interchangeably:

| Shape | Semantic Role | Example Entities |
|-------|--------------|-----------------|
| Rectangle (rounded) | Standard service | API, Worker, App |
| Double-border rectangle | LLM / AI model | GPT-4, Claude, LLaMA |
| Hexagon | Agent / autonomous system | Orchestrator, Router |
| Cylinder | Storage / persistence | Database, S3, Vector Store |
| Ringed cylinder | Vector DB | Pinecone, Chroma, Weaviate |
| Diamond | Decision / router | Branch, gateway, classifier |
| Circle | Actor / user | End user, external system |
| Pill shape | Event / message | Kafka topic, SQS queue |

## Style Configuration Reference

```json
{
  "style": "agentic-workflow",
  "theme": {
    "mode": "light",
    "primary": "#6f42c1",
    "secondary": "#20c997",
    "background": "#ffffff",
    "text": "#1a1a2e"
  },
  "typography": {
    "nodeLabel": "Inter, 14px, bold",
    "edgeLabel": "Inter, 11px, regular",
    "heading": "Inter, 18px, bold"
  },
  "geometry": {
    "routing": "rectilinear",
    "nodePadding": 24,
    "edgeSpacing": 12,
    "portAllocation": "deterministic"
  }
}
```

> All generated diagrams carry rich metadata (`data-graph-role`, `semantic-role`) in the SVG source, enabling programmatic analysis and high-fidelity accessibility support.
