[[Design pattern]] [[Design pattern/Creation pattern/Abstract Factory]] [[Design pattern/Builder]]

# Factory Method

> Factory Method defines an interface for creating an object, but lets subclasses or registrars decide which concrete type to instantiate — deferring `new` to a dedicated creator.

```txt
        Factory Method ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Comparison
```

## Why It Matters
- **Key signal:** Factory Method checks deferred instantiation

## Sources
- Gamma et al., *Design Patterns* (Factory Method) — deep-dive

## Key Concepts
Instead of:

```text
if (platform === "ios") product = new IOSButton();
else product = new AndroidButton();
```

- **Note:** the client calls `dialog.createButton()` and each dialog subclass returns the…

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

- Registration tables (`Map<string, () => Product>`) are a functional variant w…

## Mistakes to Avoid
- **Mistake:** Overkill when only one product type exists
- **Mistake:** Deep creator hierarchies mirror product hierarchies

## Comparison
- **Relationship to other creational patterns**

| Pattern | What varies | Who picks the type |
|---------|-------------|-------------------|
| **Factory Method** | Product subclass per creator | Subclass of creator |
| [[Design pattern/Creation pattern/Abstract Factory]] | Families of related products | Factory interface + concrete factories |
| [[Design pattern/Builder]] | Step-by-step assembly of one complex product | Builder with fluent steps |

- Factory Method is the simplest "defer instantiation" pattern


### Use cases
- Framework code must stay stable while product types grow (UI widgets per platform, parsers per fo…
- You want Open/Closed: add a new creator + product without editing the client.
