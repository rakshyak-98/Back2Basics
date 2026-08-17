[[Clean Architecture]] [[Multi-tier and Layered Architecture]] [[presentation layer]] [[Idempotent-key]]

# Service Layer

> Service Layer holds business rules between HTTP handlers and the database — controllers stay thin.

```txt
        Service Layer ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Service Layer interviews check where business rules live

## Sources
- [Martin Fowler — Service Layer](https://martinfowler.com/eaaCatalog/serviceLayer.html) — deep-dive
- [Microsoft — N-tier](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/n-tier) — overview

## Key Concepts
```txt
- **Note:** HTTP / UI → Controller → Service (rules + txn) → Repository → DB
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Service** | Use-case / business logic | “Validation and multi-table rules live here.” |
| **Transaction boundary** | Begin/commit/rollback scope | “The service owns the unit of work.” |
| **Thin controller** | Map HTTP ↔ DTO only | “No SQL or pricing rules in the route.” |
| **Domain rule** | Business invariant | “Check inventory before charge.” |

### How the story goes (4 steps)

1. **Accept** — controller parses input.
2. **Decide** — service validates and applies rules.
- **Note:** 3. **Persist** — repos write inside one transaction when needed.
4. **Return** — map domain result to HTTP/status.

## Technical Details
```ts
// sketch — Nest / Express style
class OrderService {
  async place(cmd: PlaceOrder) {
    return this.uow.transaction(async (tx) => {
      await this.inventory.reserve(tx, cmd.sku, cmd.qty)
      return this.orders.create(tx, cmd)
    })
  }
}
```

| Knob | Why it matters |
|------|----------------|
| Txn in service | Multi-repo consistency |
| No DB in controller | Swap transport without rewriting rules |
| One service per use-case cluster | Avoid god-services |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Fat controllers | SQL / rules in routes | Move to service |
| Partial writes | No txn across repos | Wrap in unit-of-work |
| Circular deps | Service A↔B | Extract domain or events |
| Hard to test | Needs full HTTP | Unit-test service with fakes |

## Mistakes to Avoid
- **Mistake:** Anemic services
- **Mistake:** Txn leakage

## Pros/Cons or Trade-offs
- **Trade-off:** Tiny CRUD — one handler + one query is fine until rules grow.
- **Trade-off:** Pure BFF glue — mapping APIs with no rules doesn’t need a service layer.
