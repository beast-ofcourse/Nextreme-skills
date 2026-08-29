# Core Diagramming Principles

To produce world-class technical diagrams, follow these non-negotiable engineering principles. These rules ensure diagrams are readable, maintainable, and technically accurate.

## 1. Semantic Integrity

Every element in a diagram must have a defined semantic role. Do not use shapes or colors purely for decoration.

| Element | Rule | Reason |
|---------|------|--------|
| **Nodes** | Must represent a distinct entity (Service, DB, Agent) | Prevents ambiguity in system boundaries |
| **Edges** | Must define a specific interaction (Sync, Async, Stream) | Clarifies communication protocols |
| **Colors** | Must follow the Style Matrix | Ensures consistency across different diagrams |
| **Groups** | Must represent logical boundaries (VPC, Region, Context) | Defines scope and security zones |

## 2. Layout and Geometry Rules

The fireworks-tech-graph engine enforces strict geometry to maintain professional standards.

- **Rectilinear Routing**: All edges must be rectilinear (right-angled) unless crossing via a bridge arc.
- **No Overlaps**: Collinear edge overlap is fatal. The engine will fail validation if edges occupy the same space.
- **Crossing Bridges**: When edges must cross, use a visible bridge arc and background mask to maintain legibility.
- **Port Allocation**: Shared nodes must have distinct, deterministically allocated ports for incoming and outgoing edges.

## 3. The C4 Hierarchy

For complex systems, always follow the C4 model for progressive disclosure of information:

1. **Level 1: Context** — The system as a whole and its relationship with users and other systems.
2. **Level 2: Container** — High-level technical building blocks (Web App, Database, API).
3. **Level 3: Component** — Internal components within a container.
4. **Level 4: Code** — (Optional) Implementation details for critical paths.

## 4. Visual Accessibility

Ensure diagrams are readable by everyone, regardless of environment or vision.

- **Dark Mode Support**: Use semantic color variables that adjust automatically between light and dark themes.
- **High Contrast**: Ensure a minimum contrast ratio of 4.5:1 for text labels.
- **Semantic Metadata**: Every SVG element must carry `data-graph-role` and `semantic-role` attributes for screen readers and programmatic analysis.

## 5. Geometry Validation

Before rendering, enforce these validation rules:

- **No orphan nodes**: Every node must have at least one edge.
- **No collinear overlaps**: Edges must not share the same path segment.
- **No dangling edges**: Every edge must connect two valid nodes.
- **Port limits**: No node may exceed its available port count.

> A diagram is a form of documentation. If a diagram requires a verbal explanation to be understood, it has failed its primary purpose.
