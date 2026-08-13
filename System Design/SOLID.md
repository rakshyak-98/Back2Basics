[[System Design]] [[DRY]] [[GRASP]] [[solid diagram]]

# SOLID

> SOLID — five OOP habits: one reason to change, extend without edit, subtypes safe, small interfaces, depend on abstractions.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Program to interfaces; prefer composition; keep classes focused so a change in billing doesn’t break shipping.

| Letter | Rule | Plain |
|--------|------|-------|
| **S** | Single Responsibility | One actor/reason to change |
| **O** | Open/Closed | Extend via new types, don’t hack old ones |
| **L** | Liskov Substitution | Subtype usable wherever parent is |
| **I** | Interface Segregation | No fat interfaces clients half-implement |
| **D** | Dependency Inversion | High-level depends on abstractions |

```txt
OrderService → (interface) PaymentGateway
                    ↑
              StripeGateway / FakeGateway
```

---

## Standard config / commands

```ts
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

| Smell | SOLID hint |
|-------|------------|
| God class | Split S |
| `switch` on type forever | O — strategy/plugins |
| Override breaks callers | L |
| Empty methods “not supported” | I |
| `new Stripe()` deep inside | D — inject |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Change A breaks B | Shared class two reasons | Split responsibilities |
| Can’t add vendor without edits | Hard-coded concrete | Interface + new impl |
| Tests need real Stripe | No seam | Inject fake gateway |
| Subclass throws `NotImplemented` | ISP/LSP violation | Narrow interfaces |
| Parallel inheritance explosion | Composition needed | Strategy/decorator |

---

## Gotchas

> [!WARNING]
> **Interface soup** — DIP ≠ one-interface-per-function; keep meaningful ports.

> [!WARNING]
> **OCP dogma** — sometimes editing is cheaper than endless extension points.

> [!WARNING]
> **Anemic “SOLID” layers** — ceremony without boundaries still couples via DB.

---

## When NOT to use

- **Scripts and glue** — YAGNI over SOLID theater.
- **Performance-critical inner loops** — indirection has cost; measure.
- **Functional cores** — apply the ideas, not Java ceremony.

---

## Related

[[DRY]] [[GRASP]] [[solid diagram]] [[API design]]
