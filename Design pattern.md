[[System Design/SOLID]] [[System Design/KISS]] [[System Design/DRY]] [[Design pattern/Dependency Injection]]

# Design Patterns

> Design patterns — reusable object designs; use only where variation is real. **Shvets**.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Decision table — which pattern when]]
- [[#How to extend (project playbook)]]
- [[#Triage (when patterns go wrong)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

Patterns are **named solutions to recurring design problems**, not a checklist. In a multi-platform / multi-goal backend (e.g. Meta Marketing API), every pattern that earned its keep mapped to a **variation point**: goals change, platforms multiply, Graph quirks need adapters, launch needs a fixed algorithm with swappable steps.

Four principles always beat twenty patterns:

| Principle | Meaning in code |
|-----------|-----------------|
| **Encapsulate what varies** | Pull goals, platforms, geo, vendor quirks into modules — leave stable orchestration alone |
| **Program to an interface** | Depend on factories / strategies / adapters — not Meta field names or concrete HTTP clients |
| **Favor composition over inheritance** | Stack decorators/wrappers instead of subclassing `MetaClient` for every concern combo |
| **SOLID (esp. SRP + OCP)** | One job per handler/strategy; new goals/platforms = new class + register, not edit switches |

```
Client / REST
  → Facade (stable app API)
    → Command / Pipeline (Template Method)
      → Chain of Responsibility (validation)
      → Strategy (goal / algorithm)
      → Abstract Factory (platform service family)
      → Adapter + Decorator/Proxy (vendor IO)
      → Observer (side-effects)
```

## Standard config / commands

…

## Decision table — which pattern when

| You see this variation… | Reach for | Not this |
|-------------------------|-----------|----------|
| Algorithm family swapped at runtime (goals, pay methods) | [[Design pattern/Strategy pattern]] | `if/switch` on goal id everywhere |
| Product *family* differs by platform (campaign/adset/ad) | [[Design pattern/Creation pattern/Abstract Factory]] | Platform `if` inside every service |
| Single product type chosen by config | [[Design pattern/Factory Method]] | Scattered `new ConcreteX()` |
| Complex object built step-wise from wizard fields | [[Design pattern/Builder]] | 12-arg constructor |
| Incompatible vendor payload ↔ domain model | [[Design pattern/Adapter]] | Controllers touching Graph fields |
| Two independent hierarchies (API vs transport) | [[Design pattern/Bridge]] | Class explosion |
| Cross-cutting: log, retry, auth around a client | [[Design pattern/Decorator]] · Proxy | Subclass per concern combo |
| App needs one simple entry to a subsystem | [[Design pattern/Facade]] | Routes calling 8 services |
| Ordered checks until one fails / all pass | [[Design pattern/Chain of Responsibility]] | God `validateEverything()` |
| Fixed algorithm, steps overridden per platform | [[Design pattern/Template Method]] | Copy-paste launch flows |
| Side-effects after an event (metrics, audit) | [[Design pattern/Observer]] | Pipeline knowing every subscriber |
| Action as object (queue, undo, audit) | [[Design pattern/Command]] | Inline side-effects in controller |
| Need test doubles / swap impl | [[Design pattern/Dependency Injection]] | Hard-coded `new` in class bodies |

## How to extend (project playbook)

When the variation point is already patterned, **extend at the registration seam** — do not invent a parallel structure:

| Change request | Extension point |
|----------------|-----------------|
| New campaign **goal** | New `GoalStrategy` + register in strategy map |
| New ad **platform** | New platform factory + pipeline subclass; register in factory method |
| New launch **check** | Append validation handler to the chain |
| New launch **side-effect** | Subscribe on the event bus (Observer) |
| Complex request assembly | Builder step, not ad-hoc object mutation |
| Graph client concerns | Decorator / Proxy wrap — never subclass per combo |
| App entry to Marketing APIs | Keep one Facade; do not bypass from routes |

Document the pattern → module map in-repo when you add or relocate a pattern (keeps the next engineer from inventing a twin).

## Triage (when patterns go wrong)

| Symptom | Check | Fix |
|---------|-------|-----|
| Every feature touches 15 files | Pattern tax with no variation | Collapse to plain functions ([[System Design/KISS]]) |
| Still editing `switch(goal)` in 6 places | Strategy not registered / bypassed | One registry; ban direct switches |
| Controllers know Meta field names | Facade/Adapter skipped | Route → Facade → Adapter only |
| `MetaClient` subclass tree | Inheritance for cross-cutting | Decorator stack |
| God service: validate + map + HTTP + orchestrate | Missing SRP / Template Method | Split pipeline steps |
| Tests can't mock Graph | Concrete client constructed inside | [[Design pattern/Dependency Injection]] at composition root |
| "We have all 23 GoF patterns" | Pattern tourism | Delete unused; keep map of *real* variation only |

## Gotchas

> [!WARNING]
> **Pattern first, problem second** produces unreadable code. Apply a pattern only when you have a real variation or collaboration problem — not because the book lists it.

- **Composition root matters** — factories and DI wiring belong in one place (`main` / runtime module); business modules must not `new` vendor clients.
- **Interfaces that mirror one vendor** are not interfaces — they leak Meta/Graph into the domain. Adapter owns the translation.
- **Observer vs pipeline** — if every subscriber is required for correctness, it's not a side-effect; put it in the Template Method steps.
- **Singleton for "convenience"** — process-wide wiring (Graph version, event bus) is fine; hiding mutable global state is not.

## When NOT to use

- Trivial CRUD with one vendor and one code path — patterns add indirection without payoff.
- "Future platforms" with no second platform scheduled — YAGNI; extract Factory when the second arrives.
- Forcing every GoF pattern into a greenfield app — start with Facade + Strategy at real seams only.

## Related

[[Design pattern/Strategy pattern]] [[Design pattern/Facade]] [[Design pattern/Adapter]] [[Design pattern/Decorator]] [[Design pattern/Factory Method]] [[Design pattern/Creation pattern/Abstract Factory]] [[Design pattern/Builder]] [[Design pattern/Chain of Responsibility]] [[Design pattern/Template Method]] [[Design pattern/Observer]] [[Design pattern/Command]] [[Design pattern/Bridge]] [[Design pattern/Dependency Injection]] [[System Design/SOLID]] [[System Design/KISS]]
