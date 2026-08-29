# Diagram Types Reference

All supported diagram types with JSON spec examples and CLI commands.

## 1. System Architecture

Cloud infrastructure, microservices, VPCs, deployment boundaries.

```json
{
  "type": "architecture",
  "nodes": [
    {"id": "lb", "label": "Load Balancer", "role": "load_balancer"},
    {"id": "app", "label": "App Server", "role": "compute"},
    {"id": "db", "label": "PostgreSQL", "role": "database"},
    {"id": "cache", "label": "Redis", "role": "cache"}
  ],
  "edges": [
    {"from": "lb", "to": "app", "kind": "sync_request"},
    {"from": "app", "to": "db", "kind": "sync_request"},
    {"from": "app", "to": "cache", "kind": "async_event"}
  ],
  "groups": [
    {"id": "vpc", "label": "AWS VPC", "nodes": ["app", "db", "cache"]}
  ]
}
```

```bash
fireworks-cli render --type architecture --input spec.json --output architecture.svg
```

## 2. AI / Agent Workflow

LLM chains, RAG loops, ReAct cycles, multi-agent orchestration.

```json
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
    {"from": "llm", "to": "memory", "kind": "async_event"},
    {"from": "memory", "to": "llm", "kind": "sync_response"}
  ]
}
```

```bash
fireworks-cli render --type agent --input spec.json --output agent-workflow.svg
```

## 3. Sequence Diagram

API calls, auth flows, protocol handshakes.

```json
{
  "type": "sequence",
  "lifelines": [
    {"id": "client", "label": "Client"},
    {"id": "api", "label": "API Gateway"},
    {"id": "service", "label": "Auth Service"},
    {"id": "db", "label": "User DB"}
  ],
  "messages": [
    {"from": "client", "to": "api", "label": "POST /login", "kind": "sync_request"},
    {"from": "api", "to": "service", "label": "validate()", "kind": "sync_request"},
    {"from": "service", "to": "db", "label": "SELECT user", "kind": "sync_request"},
    {"from": "db", "to": "service", "label": "user data", "kind": "sync_response"},
    {"from": "service", "to": "api", "label": "JWT token", "kind": "sync_response"},
    {"from": "api", "to": "client", "label": "200 OK", "kind": "sync_response"}
  ]
}
```

```bash
fireworks-cli render --type sequence --input spec.json --output sequence.svg
```

## 4. Event-Driven / Event Transit

Message queues, Kafka topics, event streams, consumer groups.

```json
{
  "type": "event-transit",
  "topics": [
    {"id": "orders", "label": "Orders Topic"},
    {"id": "payments", "label": "Payments Topic"},
    {"id": "notifications", "label": "Notifications Topic"}
  ],
  "producers": [
    {"id": "web", "label": "Web App", "produces": ["orders"]}
  ],
  "consumers": [
    {"id": "inventory", "label": "Inventory Service", "consumes": ["orders"]},
    {"id": "billing", "label": "Billing Service", "consumes": ["orders", "payments"]},
    {"id": "email", "label": "Email Service", "consumes": ["notifications"]}
  ]
}
```

```bash
fireworks-cli render --type event-transit --input spec.json --output event-transit.svg
```

## 5. C4 Model

Progressive disclosure: Context (L1), Container (L2), Component (L3).

```json
{
  "type": "c4-review",
  "level": 2,
  "context": {
    "system": "E-Commerce Platform",
    "users": ["Customer", "Admin"]
  },
  "containers": [
    {"id": "spa", "label": "Single Page App", "tech": "React", "responsibility": "User interface"},
    {"id": "api", "label": "API Gateway", "tech": "FastAPI", "responsibility": "Request routing"},
    {"id": "workers", "label": "Background Workers", "tech": "Celery", "responsibility": "Async processing"},
    {"id": "db", "label": "Database", "tech": "PostgreSQL", "responsibility": "Persistence"}
  ],
  "relationships": [
    {"from": "spa", "to": "api", "protocol": "HTTPS/REST"},
    {"from": "api", "to": "db", "protocol": "SQL"},
    {"from": "api", "to": "workers", "protocol": "Redis/RPC"}
  ]
}
```

```bash
fireworks-cli render --type c4-review --input spec.json --output c4-review.svg
```

## 6. Data Flow

ETL pipelines, stream processing, data movement.

```json
{
  "type": "dataflow",
  "sources": [
    {"id": "source", "label": "Raw Data", "format": "Parquet"}
  ],
  "transforms": [
    {"id": "clean", "label": "Clean"},
    {"id": "aggregate", "label": "Aggregate"}
  ],
  "sinks": [
    {"id": "warehouse", "label": "Data Warehouse"}
  ],
  "flows": [
    {"from": "source", "to": "clean"},
    {"from": "clean", "to": "aggregate"},
    {"from": "aggregate", "to": "warehouse"}
  ]
}
```

```bash
fireworks-cli render --type dataflow --input spec.json --output dataflow.svg
```

## 7. Memory / Storage Tiering

Cache hierarchies, vector database topology, data lifecycle.

```json
{
  "type": "memory-tiering",
  "tiers": [
    {"id": "l1", "label": "L1 Cache", "type": "hot", "capacity": "10GB", "latency": "<1ms"},
    {"id": "l2", "label": "L2 Cache", "type": "warm", "capacity": "100GB", "latency": "5ms"},
    {"id": "l3", "label": "Main DB", "type": "cold", "capacity": "10TB", "latency": "50ms"},
    {"id": "archive", "label": "Archive", "type": "frozen", "capacity": "100TB", "latency": "5s"}
  ],
  "policy": "LRU-eviction"
}
```

```bash
fireworks-cli render --type memory-tiering --input spec.json --output memory-tiering.svg
```

## 8. UML Diagrams

All 14 UML diagram types are supported through the sequence and architecture styles.

| UML Type | fireworks-tech-graph Style |
|----------|---------------------------|
| Class | `architecture` (with stereotype annotations) |
| Sequence | `sequence` |
| State Machine | `logic-flowchart` (with state annotations) |
| Activity | `dataflow` (with fork/join semantics) |
| Component | `c4-review` |
| Deployment | `architecture` (with node stereotypes) |
| Use Case | `concept-mindmap` (with actor oval shapes) |
| Communication | `sequence` (numbered messages) |
| Timing | `sequence` (with timing constraints) |
| Interaction Overview | `dataflow` (with interaction refs) |
| Composite Structure | `architecture` (with part aggregation) |
| Profile | `comparison` (with extension markers) |
| Object | `architecture` (instance-level) |
| Package | `architecture` (with namespace grouping) |
