[[Design pattern]] [[Design pattern/Abstraction]] [[System Design/SOLID]]

# OOPS

> Object-oriented programming organizes code around objects that combine state and behavior — using encapsulation, abstraction, inheritance, and polymorphism to manage change at scale.

```txt
        OOPS ──┬── Why it matters
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               └── Comparison
```

## Why It Matters
- **Key signal:** OOP reviews want encapsulation, inheritance, polymorphism, and abstraction…

## Sources
- Gamma et al., *Design Patterns* — deep-dive

## Technical Details
- **Four pillars:** 

| Pillar | Meaning | Practical signal |
|--------|---------|------------------|
| **Encapsulation** | Hide internal state; expose operations | `private` fields + methods |
| **Abstraction** | Simpler surface than implementation | Interfaces, [[Design pattern/Abstraction]] |
| **Inheritance** | Reuse via extension | Base classes (use sparingly) |
| **Polymorphism** | One interface, many behaviors | Override, interface impl |

- **Composition over inheritance:** 

- Prefer embedding objects and interface implementation over deep subclass trees

- **SOLID (common OOP design rules):** 

- Linked in vault as [[System Design/SOLID]]
- Patterns often implement these principles mechanically.

- **Patterns map to OOP problems:** 

- See hub [[Design pattern]] routing table

## Mistakes to Avoid
- **Mistake:** Anemic domain model — data classes with all logic in services
- **Mistake:** God objects — one class knows every rule
- **Mistake:** Inheritance for code reuse only — fragile base classes

## Comparison
- **OOP vs other paradigms**

- **Procedural** — functions + data structures; fine for scripts and pipelines.
- **Functional** — immutable data + functions; reduces shared mutable state bugs.
- **OOP** — strong when domain entities have lifecycle and varied behavior behind stable interfaces.

- Many systems mix paradigms (Go structs + interfaces, Rust traits, TypeScript …
