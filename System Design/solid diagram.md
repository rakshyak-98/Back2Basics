[[System Design]] [[SOLID]] [[GRASP]]

# solid diagram

> SOLID diagrams — UML arrows that show whether you depend on an abstraction or a concrete mess.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#UML Notation summary]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Draw who knows whom. Dependency arrows should point toward stable abstractions (DIP), not from policy into MySQL drivers.

```txt
[OrderService] ………► «interface» PaymentGateway
                              △
                              │ realizes
                      [StripeGateway]
```

---

## Standard config / commands

```txt
# Quick sketch rules
1. Boxes = types; stickies = modules
2. Arrow = "knows about / compiles against"
3. Prefer dashed dependency to interfaces
4. Inheritance only when LSP holds
```

## UML Notation summary

| Relationship | Arrow | SOLID angle |
|--------------|-------|-------------|
| **Realization** | Dashed, hollow triangle | Implements abstraction (DIP/ISP) |
| **Generalization** | Solid, hollow triangle | Inheritance (LSP/OCP) |
| **Dependency** | Dashed, open arrow | Usage / knowledge direction |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Diagram shows cycles | A→B→A | Break with interface or events |
| Every class inherits one base | God hierarchy | Composition |
| Concrete DB type in domain box | DIP inverted | Port/adapter |
| Team argues arrow meaning | No legend | Stick to table above |
| Diagram ≠ code | Drift | Generate from imports or delete diagram |

---

## Gotchas

> [!WARNING]
> **Pretty UML ≠ design** — if code imports concrete, the diagram lied.

> [!WARNING]
> **Over-modeling** — sequence for the hot path beats 40-class wall charts.

---

## When NOT to use

- **Spike week** — whiteboard photo is enough.
- **Non-OOP services** — dataflow / sequence diagrams fit better.
- **Generated noise** — auto-UML of everything confuses more than helps.

---

## Related

[[SOLID]] [[GRASP]] [[DRY]]
