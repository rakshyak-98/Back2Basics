[[Design pattern]] [[Design pattern/Factory Method]] [[Design pattern/Builder]]

# Abstract Factory

> Abstract Factory provides an interface for creating **families** of related objects without naming concrete classes — so a UI kit or cloud SDK can swap entire platforms behind one factory.

```txt
        Abstract Factory ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Abstract Factory interviews probe creating families of related products witho…

## Sources
- Gamma et al., *Design Patterns* (Abstract Factory) — deep-dive

## Key Concepts
- **Note:** A dialog needs a button and a checkbox that **match** the same platform skin

Abstract Factory groups creation:

```
AbstractFactory
  createButton()  → Button
  createCheckbox() → Checkbox

WinFactory → WinButton + WinCheckbox
MacFactory → MacButton + MacCheckbox
```

- **Note:** The client depends only on `AbstractFactory` and `Button`/`Checkbox` interfac…

## Technical Details
```typescript
interface UIFactory {
  createButton(): Button
  createCheckbox(): Checkbox
}

function render(form: Form, factory: UIFactory) {
  form.add(factory.createButton())
  form.add(factory.createCheckbox())
}
```

- Switch `WinFactory` vs `MacFactory` once at application bootstrap.

## Pros/Cons or Trade-offs
| Gain | Cost |
|------|------|
| Enforces compatible product sets | Many interfaces and classes |
| Removes platform `if` chains from UI code | Adding a **new product kind** touches every factory |

- Single product type — use [[Design pattern/Factory Method]].
- Products are unrelated — separate factories or direct construction suffice.

## Comparison
- **vs Factory Method**

| | Factory Method | Abstract Factory |
|---|----------------|------------------|
| Scope | One product per creator | Multiple related products |
| Structure | Creator subclass | Factory interface + product interfaces |
| Typical use | One variation axis | Platform / theme / vendor family |

- Abstract Factory often **uses** Factory Methods internally for each product s…

### Use cases
- Multiple products must stay consistent (themes, cross-platform UI, database driver families).
- You already have [[Design pattern/Adapter]] layers per vendor and need coordinated creation.
