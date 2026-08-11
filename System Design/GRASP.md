[[System Design]] [[SOLID]] [[DRY]] [[API design]]

# GRASP

> GRASP — patterns for assigning responsibilities to classes/objects so the right object does the work.

---

## Mental model

**Say it in one breath:** General Responsibility Assignment Software Patterns — who creates what, who knows what, who controls the flow.

| Pattern | Plain ask |
|---------|-----------|
| **Information Expert** | Who has the data to decide? |
| **Creator** | Who should `new` this? |
| **Controller** | Who handles the system event / use-case? |
| **Low Coupling** | Who depends on few others? |
| **High Cohesion** | Are responsibilities related? |
| **Polymorphism** | Replace `switch(type)` with types |
| **Pure Fabrication** | Need a helper not in the domain? (e.g. Gateway) |
| **Indirection** | Insert a middle to cut coupling |
| **Protected Variations** | Stable interface around volatility |

---

## Standard config / commands

```txt
Design pass
1. List use-cases / events
2. Assign Controller per use-case
3. Put rules with Information Experts
4. Create objects near their Experts
5. Extract Pure Fabrications for infra (email, DB)
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| God service class | Too many responsibilities | Split controllers / experts |
| Domain imports SMTP SDK | Coupling | Pure Fabrication gateway |
| Switch on enum everywhere | Missed polymorphism | Strategy objects |
| Can’t test without DB | Creator/coupling | Inject factories |
| Feature touches 20 files | Low cohesion | Re-bound modules |

---

## Gotchas

> [!WARNING]
> **Controller ≠ MVC web controller only** — application/service layer entry.

> [!WARNING]
> **Over-fabrication** — not every line needs a ManagerFactoryBuilder.

> [!WARNING]
> **Expert with too much data** — becomes god object; split.

---

## When NOT to use

- **Scripts** — procedural is fine.
- **Anemic CRUD generators** — don’t fake rich domain.
- **Interview buzzword dump** — show one pattern applied cleanly.

---

## Related

[[SOLID]] [[DRY]] [[API design]] [[Architectural backend design principles]]
