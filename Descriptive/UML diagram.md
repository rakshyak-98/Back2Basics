[[System Design/HES Architecture]] [[Design pattern]] [[Architectures/DSL (Domain Specific Language)]] [[Projects/marketplace app]]

# UML diagram

> Standardized boxes-and-lines notation for structure, behavior, and deployment — design reviews and onboarding — **UML 2.x subset for engineers**.

## Mental model

UML is a **visual DSL** for software design. Use a **small subset** in practice: class, sequence, component, deployment. Diagrams are contracts for conversation, not exhaustive code generators.

```
┌──────────────┐         ┌──────────────┐
│   Client     │ ──────► │   API        │
└──────────────┘  HTTP   └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │   Database   │
                         └──────────────┘
```

| Diagram | Answers |
|---------|---------|
| **Class** | Types, fields, relationships |
| **Sequence** | Message order over time |
| **Component** | Modules / services |
| **Deployment** | Nodes, containers, networks |

## Standard config / commands

### Class diagram notation

| Symbol | Meaning |
|--------|---------|
| `+` | public attribute or operation |
| `-` | private |
| `#` | protected |
| `{static}` | underlined in tools — class-level |

```
┌─────────────────────┐
│      OrderService   │
├─────────────────────┤
│ - repo: OrderRepo   │
├─────────────────────┤
│ + createOrder(): Order │
└─────────────────────┘
```

### Relationships (pick one correctly)

| Type | Meaning | Arrow |
|------|---------|-------|
| **Association** | Uses / knows | solid line |
| **Inheritance (Generalization)** | is-a | hollow triangle ▷ |
| **Realization** | implements interface | dashed ▷ |
| **Dependency** | temporary use | dashed → |
| **Aggregation** | has-a (shared) | hollow diamond ◇ |
| **Composition** | has-a (owns lifecycle) | filled diamond ◆ |

### Mermaid in markdown (this vault)

```mermaid
classDiagram
  class OrderService {
    -OrderRepo repo
    +createOrder() Order
  }
  OrderService --> OrderRepo
```

### Sequence (debug async flows)

```mermaid
sequenceDiagram
  Client->>API: POST /orders
  API->>DB: INSERT
  DB-->>API: id
  API-->>Client: 201
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Diagram disagrees with code | Drift | Regenerate from code or mark "aspirational" |
| Every class on one sheet | Unreadable | Layer diagrams: domain / infra / deploy |
| Wrong arrow type | Relationship semantics | Composition vs aggregation vs dependency |
| Stakeholders confused | Too much UML | Switch to C4 or box diagram for execs |
| Tool lock-in | Proprietary format | Store Mermaid/PlantUML in git |

## Gotchas

> [!WARNING]
> **Auto-generated class diagrams from Java** expose every getter — useless noise. Curate public surface only.

- **Sequence diagrams** must show **return messages** for async (dashed) or readers miss errors.
- **Deployment diagram ≠ K8s YAML** — note replicas, LB, external SaaS.
- **State machines** — don't mix with sequence unless showing transitions explicitly.

## When NOT to use

- Solo script < 500 LOC — comment + function names beat ceremony.
- Real-time pair programming — whiteboard sketch beats formal UML latency.

## Related

[[Architectures/DSL (Domain Specific Language)]] [[Descriptive/Mermaid (DSL)]] [[Design pattern]] [[System Design/HES Architecture]]
