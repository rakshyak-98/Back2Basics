[[Service Layer]] [[Multi-tier and Layered Architecture]] [[frontend layered architecture]]

# presentation layer

> Presentation layer is the UI/API edge — it shows data and takes input; it should not own business rules.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Browser, CLI, or HTTP adapters format requests/responses; [[Service Layer]] decides what is allowed.

```txt
User → View / Controller / BFF → Service → Data
         ↑ presentation lives here
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Presentation** | How users see/send data | “React pages or REST controllers.” |
| **DTO / view-model** | Shape for the wire/UI | “Don’t leak DB columns to the client.” |
| **Validation (syntax)** | Required fields, types | “Shape checks here; business rules deeper.” |
| **BFF** | Backend for frontend | “Aggregate APIs for one UI.” |

---

## Standard config / commands

```ts
// controller stays dumb
app.post('/orders', async (req, res) => {
  const dto = OrderDto.parse(req.body) // syntax
  const result = await orderService.place(dto) // rules
  res.status(201).json(OrderView.from(result))
})
```

| Knob | Why it matters |
|------|----------------|
| Parse at edge | Fail bad JSON early |
| Map errors → status | 400 vs 409 vs 500 |
| No SQL here | Keeps UI/API swappable |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Business rule in React | Pricing / authz in UI only | Move to service; UI is hint |
| Leaked DB errors | Raw ORM messages | Map to safe problem details |
| Fat pages | Data fetch + rules mixed | Split presentational vs container |
| CORS / auth at wrong layer | Token checks only in UI | Enforce on API too |

---

## Gotchas

> [!WARNING]
> **UI-only authorization** — attackers skip the browser; server must enforce.

> [!WARNING]
> **View knows the schema** — renaming columns breaks every screen; use DTOs.

---

## When NOT to use

- **Batch jobs / workers** — no presentation layer; call services directly.
- **Internal scripts** — CLI that is the product may fold layers until it hurts.

## Related

[[Service Layer]] [[frontend layered architecture]] [[Multi-tier and Layered Architecture]]
