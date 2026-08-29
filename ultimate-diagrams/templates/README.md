# Diagram Templates

Ready-to-use SVG templates for the fireworks-tech-graph engine. Each template is a complete, styled diagram that demonstrates the semantic shape and arrow vocabulary for its diagram type.

## Templates

| Template | Diagram Type | Style | Key Elements |
|----------|-------------|-------|-------------|
| `agent-loop.svg` | AI Agent Workflow (ReAct) | `agentic-workflow` | User actor, LLM double-border rect, hex tools, cylinder memory, sync/async arrows |
| `system-architecture.svg` | Cloud Infrastructure | `system-architecture` | Load balancer, app servers, DB primary+replica, Redis cache, SQS queue, VPC+AZ boundaries |
| `sequence.svg` | API Sequence Call | `sequence` | 4 lifelines, activation bars, sync request/response arrows, error/exception path |
| `event-transit.svg` | Event-Driven Architecture | `event-transit` | 3 Kafka topics (pill shapes), producers, consumers with groups, produce/consume arrows |
| `c4-review.svg` | C4 Container Diagram (L2) | `c4-review` | Person actor, system boundary, 4 containers, DB cylinder, relationships with protocols |

## Usage

Each SVG is a standalone diagram. You can:

1. **Use directly** as a reference image in docs/presentations
2. **Modify the SVG** by editing node positions, labels, and colors
3. **Re-render via CLI** using a JSON spec equivalent (see SKILL.md and `references/diagram-types.md` for spec format)

## Creating New Templates

To add a new diagram template:

1. Design the layout and semantic elements
2. Follow the shape vocabulary: LLM=double-border, Agent=hexagon, Storage=cylinder, Decision=diamond, etc.
3. Follow the arrow semantics: solid=sync, dashed=async, thick=stream
4. Include semantic metadata in an SVG `<metadata>` tag:
   ```xml
   <metadata>
     <graph-role>my-diagram-type</graph-role>
     <semantic-role>description_of_purpose</semantic-role>
     <style>style-name</style>
     <generated-by>ultimate-diagrams</generated-by>
   </metadata>
   ```
5. Add a `<defs><marker>` for each arrow type used
6. Include a legend at the bottom explaining arrow and shape semantics
7. Add to this README table
