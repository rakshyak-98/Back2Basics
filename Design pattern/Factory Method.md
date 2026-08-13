[[Design pattern]] [[Design pattern/Creation pattern/Abstract Factory]] [[Design pattern/Builder]]

# Factory Method

> Factory Method defines an interface for creating an object, but lets subclasses or registrars decide which concrete type to instantiate — deferring `new` to a dedicated creator.

## Core idea

Instead of:

```text
if (platform === "ios") product = new IOSButton();
else product = new AndroidButton();
```

the client calls `dialog.createButton()` and each dialog subclass returns the right button. Creation moves behind a virtual method or function hook.

```
Client → Creator.createProduct()
              ↓
    ConcreteCreatorA → ProductA
    ConcreteCreatorB → ProductB
```

## Relationship to other creational patterns

| Pattern | What varies | Who picks the type |
|---------|-------------|-------------------|
| **Factory Method** | Product subclass per creator | Subclass of creator |
| [[Design pattern/Creation pattern/Abstract Factory]] | Families of related products | Factory interface + concrete factories |
| [[Design pattern/Builder]] | Step-by-step assembly of one complex product | Builder with fluent steps |

Factory Method is the simplest "defer instantiation" pattern — one product type per creator.

## Implementation sketch (TypeScript)

```typescript
interface Product { render(): string }

abstract class Creator {
  abstract create(): Product
  run() { return this.create().render() }
}

class ConcreteCreator extends Creator {
  create() { return new ConcreteProduct() }
}
```

Registration tables (`Map<string, () => Product>`) are a functional variant without inheritance.

## When it helps

- Framework code must stay stable while product types grow (UI widgets per platform, parsers per format).
- You want Open/Closed: add a new creator + product without editing the client.

## Pitfalls

- Overkill when only one product type exists.
- Deep creator hierarchies mirror product hierarchies — consider [[Design pattern/Creation pattern/Abstract Factory]] if you create **families** (button + checkbox + dialog together).

## Sources

- Gamma et al., *Design Patterns* (Factory Method)
- [Factory method pattern — Wikipedia](https://en.wikipedia.org/wiki/Factory_method_pattern)
