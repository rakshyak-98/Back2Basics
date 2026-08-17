[[Design pattern]] [[Design pattern/Creation pattern/Abstract Factory]] [[Design pattern/Builder]]

# Factory Method

> Factory Method defines an interface for creating an object, but lets subclasses or registrars decide which concrete type to instantiate — deferring `new` to a dedicated creator.





## Interview Relevance
Factory Method checks deferred instantiation — subclasses or registrars pick the concrete type; contrast Abstract Factory families.

## Sources
- Gamma et al., *Design Patterns* (Factory Method) — deep-dive

## Key Concepts
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

## Technical Details
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

## Real-World Applications
- Framework code must stay stable while product types grow (UI widgets per platform, parsers per format).
- You want Open/Closed: add a new creator + product without editing the client.

## Comparison
**Relationship to other creational patterns**

| Pattern | What varies | Who picks the type |
|---------|-------------|-------------------|
| **Factory Method** | Product subclass per creator | Subclass of creator |
| [[Design pattern/Creation pattern/Abstract Factory]] | Families of related products | Factory interface + concrete factories |
| [[Design pattern/Builder]] | Step-by-step assembly of one complex product | Builder with fluent steps |

Factory Method is the simplest "defer instantiation" pattern — one product type per creator.

## Mistakes to Avoid
- Overkill when only one product type exists.
- Deep creator hierarchies mirror product hierarchies — consider [[Design pattern/Creation pattern/Abstract Factory]] if you create **families** (button + checkbox + dialog together).
