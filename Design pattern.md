[[System Design/SOLID]] [[System Design/KISS]] [[System Design/DRY]] [[Design pattern/Dependency Injection]] [[Design pattern/Strategy pattern]] [[Design pattern/OOPS]]

# Design pattern

> Design patterns — named, reusable object designs; use them only where variation is real.





## Interview Relevance
Interviewers care less about reciting GoF names and more about *when* you reach for Strategy, Factory, Adapter, or DI — and when a plain function wins. Signal: encapsulate what varies; program to interfaces; composition over inheritance.

## Sources
- [Wikipedia — Software design pattern](https://en.wikipedia.org/wiki/Software_design_pattern) — overview
- [Refactoring.Guru — Design Patterns](https://refactoring.guru/design-patterns) — deep-dive (Shvets)

## Core Definition
A design pattern is a named solution to a recurring design problem in a given context. Patterns are vocabulary and structure — not a mandatory checklist for every class.

## Key Concepts
- **Encapsulate what varies:** Pull goals, platforms, vendors into modules; leave stable orchestration alone.
- **Program to an interface:** Depend on factories / strategies / adapters, not concrete vendor field names.
- **Composition over inheritance:** Stack decorators/wrappers instead of one mega-subclass tree.
- **SOLID (esp. SRP + OCP):** New variation = new type + register, not edit a giant `switch`.

## Technical Details
```txt
Client / REST
  → Facade (stable app API)
    → Command / Pipeline (Template Method)
      → Chain of Responsibility (validation)
      → Strategy (goal / algorithm)
      → Abstract Factory (platform service family)
      → Adapter + Decorator/Proxy (vendor quirks)
```

| Need | Pattern |
|------|---------|
| Swap algorithms at runtime | [[Design pattern/Strategy pattern]] |
| Fixed pipeline, swappable steps | [[Design pattern/Template Method]] |
| Vendor API ≠ domain model | [[Design pattern/Adapter]] |
| Too many `if (platform === …)` | [[Design pattern/Creation pattern/Abstract Factory]] · [[Design pattern/Factory Method]] |
| Validation chain | [[Design pattern/Chain of Responsibility]] |
| Many listeners | [[Design pattern/Observer]] |
| Undo / snapshot | [[Design pattern/Memento]] |
| Hide subsystem | [[Design pattern/Facade]] |
| Lazy / access control | [[Design pattern/Proxy]] |
| Behavior by state | [[Design pattern/State]] |
| Wire deps from outside | [[Design pattern/Dependency Injection]] |

**Creational:** [[Design pattern/Factory Method]] · [[Design pattern/Creation pattern/Abstract Factory]] · [[Design pattern/Builder]] · [[Design pattern/Singleton]]  
**Structural:** [[Design pattern/Adapter]] · [[Design pattern/Bridge]] · [[Design pattern/Decorator]] · [[Design pattern/Facade]] · [[Design pattern/Proxy]]  
**Behavioral:** [[Design pattern/Strategy pattern]] · [[Design pattern/Chain of Responsibility]] · [[Design pattern/Template Method]] · [[Design pattern/Observer]] · [[Design pattern/Command]] · [[Design pattern/State]] · [[Design pattern/Mediator]] · [[Design pattern/Memento]]

## Real-World Applications
Multi-platform checkout: Strategy per payment goal, Adapter per PSP quirks, Facade for the stable app API — new country = new classes, not a 400-line `if`.

## Pros/Cons or Trade-offs
- **Pro:** Shared language in reviews; localizes change at variation points.
- **Con:** Pattern theater — indirection without real variation hurts readability ([[System Design/KISS]], [[System Design/DRY]]).

## Comparison
vs algorithms/data structures: patterns organize *object collaboration*; DSAs organize *data and complexity*. vs frameworks: frameworks often embed patterns (DI containers, middleware chains). Principles: [[System Design/SOLID]] · [[Design pattern/OOPS]].

## Mistakes to Avoid
- Applying Singleton or Abstract Factory “because interviews.”
- Inheritance trees where a Strategy map would do.
- Naming every class after a pattern when a clear domain name is better.
