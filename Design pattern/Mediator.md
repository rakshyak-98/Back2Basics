[[Design pattern]] [[Design pattern/Observer]] [[Design pattern/Command]]

# Mediator

> Mediator centralizes how a set of objects communicate — so components talk through the mediator instead of forming a web of direct references.

```txt
        Mediator ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Comparison
```

## Why It Matters
- **Key signal:** Mediator reduces chaotic peer-to-peer coupling via a hub

## Sources
- Gamma et al., *Design Patterns* (Mediator) — deep-dive

## Key Concepts
```
A ↔ B ↔ C ↔ D   (many-to-many coupling)
```

With mediator:

```
A → Mediator → B
C → Mediator → D
```

- **Note:** Colleagues know only the mediator; the mediator routes messages and updates.

## Technical Details
- Chat room: users send to `ChatRoom`, not to each other directly.
- UI dialog controls coordinated by `DialogMediator` (font changes update label…

## Mistakes to Avoid
- **Mistake:** Mediator becomes a god object
- **Mistake:** Performance hotspot if every message funnels through one class

## Comparison
- **vs Observer**

| | Mediator | Observer |
|---|----------|----------|
| Flow | Often bidirectional routing | Subject notifies many observers |
| Center | Explicit hub object | Subject holds observer list |

- Mediator **reduces** arbitrary connections; Observer **broadcasts** events.


### Use cases
- Many peers with messy interdependencies (forms, air traffic control sim, collaboration UI).
- Reusable widgets that must not know about each other.
