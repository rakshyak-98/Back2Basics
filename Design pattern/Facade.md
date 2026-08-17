[[Design pattern]] [[Design pattern/Adapter]] [[Design pattern/Decorator]]

# Facade

> Facade offers a single simplified entry point to a subsystem — hiding many classes, protocols, and error modes behind one coordinated call.

```txt
        Facade ──┬── Why it matters
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               └── Comparison
```

## Why It Matters
- **Key signal:** Facade probes giving callers one simple entry to a messy subsystem

## Sources
- Gamma et al., *Design Patterns* (Facade) — deep-dive

## Technical Details
- Home theater: `watchMovie()` turns on projector, amp, player, dims lights

```
Client → Facade.watchMovie()
            → Subsystem classes (many steps, order matters)
```

- Facade does not block direct subsystem access

## Mistakes to Avoid
- **Mistake:** God facade that knows everything
- **Mistake:** Facade that becomes the only path and hides useful subsystem fea…

## Comparison
- **vs Adapter**

- Facade **simplifies** a subsystem


### Use cases
- Legacy modules with tangled APIs.
- Onboarding layer for complex SDKs (cloud deploy, media pipeline).
- Application service layer over repositories + messaging.
