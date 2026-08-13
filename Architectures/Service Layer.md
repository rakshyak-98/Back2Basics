[[Clean Architecture]] [[Multi-tier and Layered Architecture]] [[presentation layer]]

# Service Layer

> Service Layer holds business rules between HTTP handlers and the database — controllers stay thin.

---

## How it works

```txt
HTTP / UI  →  Controller  →  Service (rules + txn)  →  Repository  →  DB
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
3. **Persist** — repos write inside one transaction when needed.
4. **Return** — map domain result to HTTP/status.

---


## Configuration and commands

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

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Fat controllers | SQL / rules in routes | Move to service |
| Partial writes | No txn across repos | Wrap in unit-of-work |
| Circular deps | Service A↔B | Extract domain or events |
| Hard to test | Needs full HTTP | Unit-test service with fakes |

---


## Gotchas

> [!WARNING]
> **Anemic services** — if the service only forwards to the repo, you added a layer for nothing.

> [!WARNING]
> **Txn leakage** — opening transactions in controllers usually races and nests badly.

---


## When not to use

- **Tiny CRUD** — one handler + one query is fine until rules grow.
- **Pure BFF glue** — mapping APIs with no rules doesn’t need a service layer.


## Related

[[Clean Architecture]] [[Multi-tier and Layered Architecture]] [[presentation layer]] [[Idempotent-key]]

## Sources

- [Wikipedia — Service Layer](https://en.wikipedia.org/wiki/Service_Layer)
