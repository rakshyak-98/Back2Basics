[[SOLID]] [[GRASP]] [[System design]] [[API design]]

# solid diagram

> The SOLID diagram is a visual map of the five principles — how single responsibility, open/closed, Liskov substitution, interface segregation, and dependency inversion relate when drawing module boundaries.

---

## Structural view

```txt
                    ┌─────────────────────────┐
                    │   High-level policy     │
                    │   (use cases, domain)   │
                    └───────────┬─────────────┘
                                │ depends on abstractions (D)
                    ┌───────────▼─────────────┐
                    │   Abstractions / ports  │
                    │   (small interfaces)  │  ← Interface Segregation (I)
                    └───────────┬─────────────┘
                                │ implemented by
                    ┌───────────▼─────────────┐
                    │   Low-level details     │
                    │   (database, HTTP, SDK) │
                    └─────────────────────────┘

Within domain layer:
  S — one reason to change per class
  O — extend via new types, not edits to stable code
  L — subtypes honor parent contracts
```

## How to read it in a design review

| Principle | Question on the diagram |
|-----------|-------------------------|
| **S** | Does this box do one job for one actor? |
| **O** | Can we add a new payment provider without editing order logic? |
| **L** | Can we substitute test doubles without `instanceof`? |
| **I** | Are interfaces minimal for each client? |
| **D** | Do arrows point **inward** toward domain, not outward toward frameworks? |

## Example: payment boundary

```txt
OrderService ──► PaymentGateway (interface)
                      ▲
            StripeGateway    FakeGateway (tests)
```

`OrderService` depends on **PaymentGateway** (D). **StripeGateway** is one implementation (O, L). Do not force `OrderService` to implement unused methods from a fat `PaymentAndEmailAndLogging` interface (I).

## Relationship to [[GRASP]]

- **Controller** often sits at the top of the diagram (use-case entry).
- **Pure Fabrication** creates gateway classes at the bottom edge.
- **Information Expert** keeps rules in domain nodes, not in adapters.

The diagram is a teaching aid — production code may collapse layers in small services ([[KISS]]), but the dependency direction should still point inward.

## Sources

- Robert C. Martin, *Clean Architecture* — concentric circles and dependency rule.
- Craig Larman — GRASP patterns alongside SOLID in object design.
