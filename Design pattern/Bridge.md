[[Design pattern]] [[Design pattern/Adapter]] [[Design pattern/Decorator]]

# Bridge

> Bridge splits a large abstraction from its implementation so both can vary independently — avoiding permanent binding between interface hierarchy and platform hierarchy.

```txt
        Bridge ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Comparison
```

## Why It Matters
- **Key signal:** Bridge tests separating abstraction from implementation so both hierarchies v…

## Sources
- Gamma et al., *Design Patterns* (Bridge) — deep-dive

## Key Concepts
```
Abstraction (e.g. RemoteControl)
    ↓ uses
Implementation interface (e.g. Device)
    ↓
ConcreteImplementation (TV, Radio)
```

- **Note:** `Abstraction` holds a reference to `Implementation` and forwards calls. New r…

## Technical Details
- Cross-platform graphics: `Window` abstraction with `RenderingEngine` implemen…
- UI code stays on `Window`; engine swaps at runtime or build time.

## Mistakes to Avoid
- **Mistake:** Extra indirection for a single fixed implementation
- **Mistake:** Confusing with [[Design pattern/Strategy pattern]]

## Comparison
- **vs Adapter**

| | Bridge | Adapter |
|---|--------|---------|
| Timing | Designed early | Retrofit legacy |
| Goal | Separate dimensions | Make incompatible work together |


### Use cases
- Two orthogonal axes of variation (shape × rendering, message × transport).
- You want to hide platform details from high-level code permanently.
