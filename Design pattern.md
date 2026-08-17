[[System Design/SOLID]] [[System Design/KISS]] [[System Design/DRY]] [[Design pattern/Dependency Injection]] [[Design pattern/Strategy pattern]] [[Design pattern/OOPS]]

# Design pattern

> Design patterns — named, reusable object designs; use them only where variation is real.

```txt
        Design pattern ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers care less about reciting GoF names and more about *when* you rea…

## Sources
- [Wikipedia — Software design pattern](https://en.wikipedia.org/wiki/Software_design_pattern) — overview
- [Refactoring.Guru — Design Patterns](https://refactoring.guru/design-patterns) — deep-dive (Shvets)

## Key Concepts
- **Encapsulate what varies:** Pull goals, platforms, vendors into modules; leave stable orchestration alone.
- **Program to an interface:** Depend on factories / strategies / adapters, not concrete vendor field names.
- **Composition over inheritance:** Stack decorators/wrappers instead of one mega-subclass tree.
- **SOLID (esp. SRP + OCP):** New variation = new type + register, not edit a giant `switch`.


- **Core:** A design pattern is a named solution to a recurring design problem in a given…

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

- **Creational:** [[Design pattern/Factory Method]] · [[Design pattern/Creation…

## Mistakes to Avoid
- **Mistake:** Applying Singleton or Abstract Factory “because interviews.”
- **Mistake:** Inheritance trees where a Strategy map would do
- **Mistake:** Naming every class after a pattern when a clear domain name is b…

## Pros/Cons or Trade-offs
- **Pro:** Shared language in reviews; localizes change at variation points.
- **Con:** Pattern theater — indirection without real variation hurts readability ([[System Design/KISS]], [[System Design/DRY]]).

## Comparison
- vs algorithms/data structures: patterns organize *object collaboration*


### Use cases
- Multi-platform checkout: Strategy per payment goal, Adapter per PSP quirks, F…
