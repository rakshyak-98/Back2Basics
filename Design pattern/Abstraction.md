[[Design pattern]] [[Design pattern/OOPS]] [[Design pattern/Abstraction]]

# Abstraction

> Abstraction hides irrelevant detail behind a simpler model — so callers work with stable concepts (interfaces, APIs) instead of concrete implementation mechanics.





## Interview Relevance
Abstraction questions check hiding the right details — leaky and premature abstractions are common failure modes.

## Sources
- Gamma et al., *Design Patterns* (introduction to abstraction in OOP) — deep-dive

## Key Concepts
Abstraction is both a **principle** and a technique:

- **Data abstraction** — expose operations, hide representation (stack `push/pop`, not raw array index).
- **Procedural abstraction** — named operations that bundle steps (`connect()`, not socket syscalls).
- **Interface abstraction** — `PaymentProcessor` without naming Stripe fields.

Abstraction pairs with **encapsulation** (hide state) and **polymorphism** (many implementations behind one interface).

```text
Problem domain concept  →  Application service  →  Library API  →  OS / hardware
     (more abstract)                              (more concrete)
```

Good abstractions leak only what callers must decide; bad abstractions leak vendor quirks or force callers to know internals.

Many patterns **are** abstractions:

- [[Design pattern/Facade]] — simplified subsystem view
- [[Design pattern/Bridge]] — split interface from implementation
- [[Design pattern/Strategy pattern]] — abstract algorithm slot

## Mistakes to Avoid
- **Wrong abstraction** — forces awkward workarounds (leaky `UserDAO` that exposes SQL).
- **Premature abstraction** — one implementation dressed as an interface "for flexibility."
- **Abstraction inversion** — low-level details drive high-level names.

Ask: *What decision does this abstraction let the caller defer?*
