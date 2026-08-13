[[Design pattern]] [[Design pattern/Abstraction]] [[System Design/SOLID]]

# OOPS

> Object-oriented programming organizes code around objects that combine state and behavior — using encapsulation, abstraction, inheritance, and polymorphism to manage change at scale.

## Four pillars

| Pillar | Meaning | Practical signal |
|--------|---------|------------------|
| **Encapsulation** | Hide internal state; expose operations | `private` fields + methods |
| **Abstraction** | Simpler surface than implementation | Interfaces, [[Design pattern/Abstraction]] |
| **Inheritance** | Reuse via extension | Base classes (use sparingly) |
| **Polymorphism** | One interface, many behaviors | Override, interface impl |

## Composition over inheritance

Prefer embedding objects and interface implementation over deep subclass trees — aligns with [[Design pattern/Decorator]], [[Design pattern/Strategy pattern]], and **favor composition over inheritance** from GoF.

## SOLID (common OOP design rules)

Linked in vault as [[System Design/SOLID]] — Single responsibility, Open/closed, Liskov substitution, Interface segregation, Dependency inversion. Patterns often implement these principles mechanically.

## OOP vs other paradigms

- **Procedural** — functions + data structures; fine for scripts and pipelines.
- **Functional** — immutable data + functions; reduces shared mutable state bugs.
- **OOP** — strong when domain entities have lifecycle and varied behavior behind stable interfaces.

Many systems mix paradigms (Go structs + interfaces, Rust traits, TypeScript classes + functions).

## Patterns map to OOP problems

See hub [[Design pattern]] routing table — creational (who creates), structural (how parts compose), behavioral (how objects collaborate).

## Pitfalls

- Anemic domain model — data classes with all logic in services.
- God objects — one class knows every rule.
- Inheritance for code reuse only — fragile base classes.

## Sources

- Gamma et al., *Design Patterns*
- [Object-oriented programming — Wikipedia](https://en.wikipedia.org/wiki/Object-oriented_programming)
