[[SOLID]] [[GRASP]] [[System design]] [[API design]]

# solid diagram

> The SOLID diagram is a visual map of the five principles — how single responsibility, open/closed, Liskov substitution, interface segregation, and dependency inversion relate when drawing module boundaries.

```txt
        solid diagram ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Visual map of SOLID — use it to recall dependencies and violation shapes.

## Sources
- Robert C. Martin, *Clean Architecture* — concentric circles and dependency rule — overview
- Craig Larman — GRASP patterns alongside SOLID in object design — overview

## Key Concepts
- **Visual mnemonic:** for the five SOLID principles and their dependency arrows.
- **Use in reviews:** point at the violated letter on the diagram.
- **Pairs with [[SOLID]]:** prose definitions live on the sibling note.
- **Not a process:** diagram aids recall, not a methodology by itself.

## Technical Details
### Structural view

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

### How to read it in a design review

| Principle | Question on the diagram |
|-----------|-------------------------|
| **S** | Does this box do one job for one actor? |
| **O** | Can we add a new payment provider without editing order logic? |
| **L** | Can we substitute test doubles without `instanceof`? |
| **I** | Are interfaces minimal for each client? |
| **D** | Do arrows point **inward** toward domain, not outward toward frameworks? |

### Example: payment boundary

```txt
OrderService ──► PaymentGateway (interface)
                      ▲
            StripeGateway    FakeGateway (tests)
```

- `OrderService` depends on **PaymentGateway** (D).
- **StripeGateway:** is one implementation (O, L).
- Do not force `OrderService` to implement unused methods from a fat `PaymentAn…

## Mistakes to Avoid
- **Mistake:** Skipping failure modes until production
- **Mistake:** Ignoring idempotency, timeouts, or rollback where required
- **Mistake:** Optimizing or distributing before measuring the real bottleneck

## Pros/Cons or Trade-offs
- **Pro:** Fast recall under interview pressure.
- **Con:** Diagram without examples stays decorative.
- **Trade-off:** keep diagram lean vs annotating every edge case.

## Comparison
- **Controller** often sits at the top of the diagram (use-case entry).
- **Pure Fabrication** creates gateway classes at the bottom edge.
- **Information Expert** keeps rules in domain nodes, not in adapters.

- The diagram is a teaching aid


- vs [[SOLID]]: canonical explanations and trade-offs.
- vs [[GRASP]]: different responsibility vocabulary.


### Use cases
- Design whiteboards and onboarding for OO dependency rules.
