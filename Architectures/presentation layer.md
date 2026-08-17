[[Service Layer]] [[Multi-tier and Layered Architecture]] [[frontend layered architecture]]

# presentation layer

> Presentation layer is the UI/API edge — it shows data and takes input; it should not own business rules.

```txt
        presentation layer ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Presentation-layer questions check thin UI/API edges

## Sources
- [Martin Fowler — Presentation Domain Separation](https://martinfowler.com/eaaCatalog/presentationDomainSeparation.html) — deep-dive
- [Wikipedia — Presentation layer](https://en.wikipedia.org/wiki/Presentation_layer) — overview

## Key Concepts
```txt
User → View / Controller / BFF → Service → Data
         ↑ presentation lives here
```

### Review map (words you can say)

| Word | Plain meaning | Say in review |
|------|---------------|------------------|
| **Presentation** | How users see/send data | “React pages or REST controllers.” |
| **DTO / view-model** | Shape for the wire/UI | “Don’t leak DB columns to the client.” |
| **Validation (syntax)** | Required fields, types | “Shape checks here; business rules deeper.” |
| **BFF** | Backend for frontend | “Aggregate APIs for one UI.” |

## Technical Details
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

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Business rule in React | Pricing / authz in UI only | Move to service; UI is hint |
| Leaked DB errors | Raw ORM messages | Map to safe problem details |
| Fat pages | Data fetch + rules mixed | Split presentational vs container |
| CORS / auth at wrong layer | Token checks only in UI | Enforce on API too |

## Mistakes to Avoid
- **Mistake:** UI-only authorization
- **Mistake:** View knows the schema

## Pros/Cons or Trade-offs
- **Trade-off:** Batch jobs / workers — no presentation layer; call services directly.
- **Trade-off:** Internal scripts — CLI that is the product may fold layers until it hurts.
