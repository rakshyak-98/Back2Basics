[[GRASP]] [[DRY]] [[solid diagram]] [[API design]] [[System design]]

# SOLID

> SOLID names five object-oriented design habits that keep modules focused, substitutable, and open to extension without turning every change into a shotgun edit.





## Interview Relevance
Define each SOLID letter with a one-line example and a violation smell.

## Sources
- Robert C. Martin, "The Principles of OOD" — [butunclebob.com](https://blog.cleancoder.com/uncle-bob/2020/10/18/Solid-Relevance.html) — overview
- Barbara Liskov & Jeannette Wing, "A Behavioral Notion of Subtyping" (1994) — Liskov Substitution Principle foundation — overview
- Bertrand Meyer, *Object-Oriented Software Construction* (Prentice Hall, 1997) — Open/Closed Principle — overview

## Key Concepts
- **S — Single Responsibility:** one reason to change per module.
- **O — Open/Closed:** extend via new types, not endless edits.
- **L — Liskov:** subtypes must honor the parent contract.
- **I — Interface Segregation:** no fat interfaces clients half-use.
- **D — Dependency Inversion:** depend on abstractions, not concretions.


### Dependency inversion in practice

```txt
OrderService → PaymentGateway (interface)
                    ↑
              StripeGateway / FakeGateway (tests)
```

```typescript
interface PaymentGateway {
  charge(cents: number, customerId: string): Promise<string>
}

class OrderService {
  constructor(private payments: PaymentGateway) {}

  async checkout(order: Order) {
    return this.payments.charge(order.total, order.customerId)
  }
}
```

Production injects `StripeGateway`; tests inject `FakeGateway` — no network calls required.

### Smells and which principle speaks to them

| Smell | Principle | Remedy direction |
|-------|-----------|------------------|
| God class handling billing, email, and reports | S | Split by change driver |
| Endless `switch (provider)` | O | Strategy or plugin registry |
| Subclass throws "not supported" | L / I | Narrow the interface or use composition |
| Tests require real external services | D | Inject interfaces at boundaries |
| Parallel inheritance hierarchies | O / composition | Favor has-a over is-a |

## Technical Details
### The five principles

| Letter | Name | In plain language |
|--------|------|-------------------|
| **S** | Single Responsibility | A module should have one reason to change — one actor or concern. |
| **O** | Open/Closed | Extend behavior with new types; avoid editing stable code for every variant. |
| **L** | Liskov Substitution | Subtypes must honor the contract of their base type — callers should not need `instanceof` checks. |
| **I** | Interface Segregation | Many small interfaces beat one fat interface that forces empty implementations. |
| **D** | Dependency Inversion | High-level policy depends on abstractions; low-level details implement them. |

Robert C. Martin introduced the acronym; the ideas draw on earlier work by Barbara Liskov, Bertrand Meyer, and others.

### Over-application risks

| Pitfall | Reality |
|---------|---------|
| Interface soup | Not every function needs its own interface — meaningful ports at boundaries suffice |
| Open/Closed dogma | Sometimes editing three lines is cheaper than a new abstraction layer |
| Anemic layers | Empty data transfer objects with all logic in services — ceremony without real seams |
| Performance | Virtual dispatch and indirection have cost; measure hot paths |

Scripts, one-off glue, and throwaway spikes should not carry full SOLID ceremony ([[KISS]]).

*When would you choose composition over inheritance?* When behavior varies independently of the type hierarchy — most policy and integration code.

## Real-World Applications
Class/module design in large codebases and hexagonal/ports-and-adapters services.

## Pros/Cons or Trade-offs
- **Pro:** Change isolation and testability.
- **Con:** Over-fragmentation into tiny types.
- **Trade-off:** SOLID purity vs [[KISS]] delivery speed.

## Comparison
- **GRASP** answers *who should own this responsibility?* (Information Expert, Creator, Controller).
- **SOLID** answers *how should types relate?* at class and interface boundaries.
- **System design** applies the same separation at service scale: domain logic should not embed HTTP or SQL dialect.


- vs [[GRASP]]: GRASP assigns responsibilities; SOLID constrains dependency shape.
- vs [[solid diagram]]: diagram is the visual mnemonic for these five.

## Mistakes to Avoid
- Skipping failure modes until production.
- Ignoring idempotency, timeouts, or rollback where required.
- Optimizing or distributing before measuring the real bottleneck.
