[[Design pattern]] [[Design pattern/Proxy]] [[Design pattern/Adapter]]

# Decorator

> Decorator wraps an object to add responsibilities dynamically while keeping the same interface — stacking layers instead of subclassing every combination.

```txt
        Decorator ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Pitfalls
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Decorator checks open/closed extension by wrapping the same interface

## Sources
- Gamma et al., *Design Patterns* (Decorator) — deep-dive

## Key Concepts
```
Component interface
  ConcreteComponent
  Decorator (holds Component, implements interface)
    ConcreteDecoratorA (+ border)
    ConcreteDecoratorB (+ scroll)
```

- **Note:** Client calls `decorated.operation()`

## Mistakes to Avoid
- **Mistake:** Order of decorators matters
- **Mistake:** Hard to reason about deep stacks — document composition order
- **Mistake:** Small objects — function composition may be simpler

## Comparison
- **vs inheritance**

- Subclass explosion: `BorderedScrollableTextView` vs `ScrollableBorderedTextVi…

- ```text
- new ScrollDecorator(new BorderDecorator(new TextView()))
- ```

- **vs Proxy**

| | Decorator | Proxy |
|---|-----------|-------|
| Focus | Add behavior | Control access / lazy load |
| Transparency | Often multiple wrappers | Usually one proxy |

- Both wrap and delegate; intent differs.


### Use cases
- Optional features on streams (`io` wrappers in Go/Java).
- UI styling layers, middleware stacks.
