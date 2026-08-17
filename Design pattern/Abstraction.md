[[Design pattern]] [[Design pattern/OOPS]] [[Design pattern/Abstraction]]

# Abstraction

> Abstraction hides irrelevant detail behind a simpler model — so callers work with stable concepts (interfaces, APIs) instead of concrete implementation mechanics.

```txt
        Abstraction ──┬── Why it matters
               ├── Sources
               ├── Concepts
               └── Pitfalls
```

## Why It Matters
- **Key signal:** Abstraction questions check hiding the right details

## Sources
- Gamma et al., *Design Patterns* (introduction to abstraction in OOP) — deep-dive

## Key Concepts
Abstraction is both a **principle** and a technique:

- **Data abstraction:** — expose operations, hide representation (stack `push/pop`, not raw array ind…
- **Procedural abstraction:** — named operations that bundle steps (`connect()`, not socket syscalls).
- **Interface abstraction:** — `PaymentProcessor` without naming Stripe fields.

- **Note:** Abstraction pairs with **encapsulation** (hide state) and **polymorphism** (m…

```text
- **Note:** Problem domain concept → Application service → Library API → OS / hardware
     (more abstract)                              (more concrete)
```

- **Note:** Good abstractions leak only what callers must decide

Many patterns **are** abstractions:

- **[[Design pattern/Facade]]:** [[Design pattern/Facade]] — simplified subsystem view
- **[[Design pattern/Bridge]]:** [[Design pattern/Bridge]] — split interface from implementation
- **[[Design pattern/Strategy:** [[Design pattern/Strategy pattern]] — abstract algorithm slot

## Mistakes to Avoid
- **Mistake:** **Wrong abstraction**
- **Mistake:** **Premature abstraction**
- **Mistake:** **Abstraction inversion**

Ask: *What decision does this abstraction let the caller defer?*
