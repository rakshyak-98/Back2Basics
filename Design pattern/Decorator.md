[[Design pattern]] [[Design pattern/Proxy]] [[Design pattern/Adapter]]

# Decorator

> Decorator wraps an object to add responsibilities dynamically while keeping the same interface — stacking layers instead of subclassing every combination.

## Structure

```
Component interface
  ConcreteComponent
  Decorator (holds Component, implements interface)
    ConcreteDecoratorA (+ border)
    ConcreteDecoratorB (+ scroll)
```

Client calls `decorated.operation()`; each decorator may pre/post-process and delegate inward.

## vs inheritance

Subclass explosion: `BorderedScrollableTextView` vs `ScrollableBorderedTextView`. Decorators compose:

```text
new ScrollDecorator(new BorderDecorator(new TextView()))
```

## vs Proxy

| | Decorator | Proxy |
|---|-----------|-------|
| Focus | Add behavior | Control access / lazy load |
| Transparency | Often multiple wrappers | Usually one proxy |

Both wrap and delegate; intent differs.

## When to use

- Optional features on streams (`io` wrappers in Go/Java).
- UI styling layers, middleware stacks.

## Pitfalls

- Order of decorators matters.
- Hard to reason about deep stacks — document composition order.
- Small objects — function composition may be simpler.

## Sources

- Gamma et al., *Design Patterns* (Decorator)
- [Decorator pattern — Wikipedia](https://en.wikipedia.org/wiki/Decorator_pattern)
