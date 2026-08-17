[[Design pattern]] [[Design pattern/Proxy]] [[Design pattern/Adapter]]

# Decorator

> Decorator wraps an object to add responsibilities dynamically while keeping the same interface — stacking layers instead of subclassing every combination.





## Interview Relevance
Decorator checks open/closed extension by wrapping the same interface — stacked behavior versus subclass explosion.

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

Client calls `decorated.operation()`; each decorator may pre/post-process and delegate inward.

## Real-World Applications
- Optional features on streams (`io` wrappers in Go/Java).
- UI styling layers, middleware stacks.

## Comparison
**vs inheritance**

Subclass explosion: `BorderedScrollableTextView` vs `ScrollableBorderedTextView`. Decorators compose:

```text
new ScrollDecorator(new BorderDecorator(new TextView()))
```

**vs Proxy**

| | Decorator | Proxy |
|---|-----------|-------|
| Focus | Add behavior | Control access / lazy load |
| Transparency | Often multiple wrappers | Usually one proxy |

Both wrap and delegate; intent differs.

## Mistakes to Avoid
- Order of decorators matters.
- Hard to reason about deep stacks — document composition order.
- Small objects — function composition may be simpler.
