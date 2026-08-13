[[System Design/SOLID]] [[System Design/KISS]] [[System Design/DRY]] [[Design pattern/Dependency Injection]]

# Design Patterns

> Design patterns — reusable object designs; use only where variation is real. **Shvets**.

---

## Purpose

Patterns are **named solutions to recurring design problems**, not a checklist. In a multi-platform / multi-goal backend, every pattern that earned its keep mapped to a **variation point**: goals change, platforms multiply, vendor quirks need adapters, launch needs a fixed algorithm with swappable steps.

Four principles always beat twenty patterns:

| Principle | Meaning in code |
|-----------|-----------------|
| **Encapsulate what varies** | Pull goals, platforms, geo, vendor quirks into modules — leave stable orchestration alone |
| **Program to an interface** | Depend on factories / strategies / adapters — not vendor field names or concrete HTTP clients |
| **Favor composition over inheritance** | Stack decorators/wrappers instead of subclassing one mega-client for every concern combo |
| **SOLID (esp. SRP + OCP)** | One job per handler/strategy; new goals/platforms = new class + register, not edit switches |

```
Client / REST
  → Facade (stable app API)
    → Command / Pipeline (Template Method)
      → Chain of Responsibility (validation)
      → Strategy (goal / algorithm)
      → Abstract Factory (platform service family)
      → Adapter + Decorator/Proxy (vendor quirks)
```


## Where to go next

| Symptom / need | Go to |
|----------------|-------|
| Need to swap algorithms at runtime without `switch` | [[Design pattern/Strategy pattern]] |
| Need a fixed pipeline with swappable steps | [[Design pattern/Template Method]] |
| Vendor API does not match your domain model | [[Design pattern/Adapter]] |
| Too many `if (platform === …)` branches | [[Design pattern/Abstract Factory]] · [[Design pattern/Factory Method]] |
| Validation scattered across handlers | [[Design pattern/Chain of Responsibility]] |
| One object triggers many listeners | [[Design pattern/Observer]] |
| Undo / snapshot of object state | [[Design pattern/Memento]] |
| Hide a complex subsystem behind one call | [[Design pattern/Facade]] |
| Lazy or access-controlled object | [[Design pattern/Proxy]] |
| Behavior changes with internal state | [[Design pattern/State]] |
| Wiring dependencies from outside | [[Design pattern/Dependency Injection]] |


## Related topics in this domain

- **Creational:** [[Design pattern/Factory Method]] · [[Design pattern/Creation pattern/Abstract Factory]] · [[Design pattern/Builder]] · [[Design pattern/Singleton]]
- **Structural:** [[Design pattern/Adapter]] · [[Design pattern/Bridge]] · [[Design pattern/Decorator]] · [[Design pattern/Facade]] · [[Design pattern/Proxy]]
- **Behavioral:** [[Design pattern/Strategy pattern]] · [[Design pattern/Chain of Responsibility]] · [[Design pattern/Template Method]] · [[Design pattern/Observer]] · [[Design pattern/Command]] · [[Design pattern/State]] · [[Design pattern/Mediator]] · [[Design pattern/Memento]]
- **Principles:** [[System Design/SOLID]] · [[System Design/KISS]] · [[System Design/DRY]] · [[Design pattern/OOPS]]


## Related

[[System Design/SOLID]] · [[System Design/KISS]] · [[System Design/DRY]] · [[Design pattern/Dependency Injection]] · [[INDEX]]

## Sources

- [Wikipedia — Design pattern](https://en.wikipedia.org/wiki/Design_pattern)
