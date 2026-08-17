[[Design pattern]] [[Design pattern/Adapter]] [[Design pattern/Decorator]]

# Bridge

> Bridge splits a large abstraction from its implementation so both can vary independently — avoiding permanent binding between interface hierarchy and platform hierarchy.





## Interview Relevance
Bridge tests separating abstraction from implementation so both hierarchies vary independently — timing differs from Adapter retrofit.

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

`Abstraction` holds a reference to `Implementation` and forwards calls. New remote features do not require new device subclasses; new devices do not require new remote subclasses.

## Technical Details
Cross-platform graphics: `Window` abstraction with `RenderingEngine` implementation (`DirectX`, `OpenGL`). UI code stays on `Window`; engine swaps at runtime or build time.

## Real-World Applications
- Two orthogonal axes of variation (shape × rendering, message × transport).
- You want to hide platform details from high-level code permanently.

## Comparison
**vs Adapter**

| | Bridge | Adapter |
|---|--------|---------|
| Timing | Designed early | Retrofit legacy |
| Goal | Separate dimensions | Make incompatible work together |

## Mistakes to Avoid
- Extra indirection for a single fixed implementation.
- Confusing with [[Design pattern/Strategy pattern]] — Bridge emphasizes **structural** split of abstraction/implementation hierarchies; Strategy emphasizes **algorithm** swap at runtime.
