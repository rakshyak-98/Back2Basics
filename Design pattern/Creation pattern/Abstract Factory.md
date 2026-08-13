[[Design pattern]] [[Design pattern/Factory Method]] [[Design pattern/Builder]]

# Abstract Factory

> Abstract Factory provides an interface for creating **families** of related objects without naming concrete classes — so a UI kit or cloud SDK can swap entire platforms behind one factory.

## Problem

A dialog needs a button and a checkbox that **match** the same platform skin. Factory Method per widget still leaves mismatched pairs if callers pick concrete types independently.

Abstract Factory groups creation:

```
AbstractFactory
  createButton()  → Button
  createCheckbox() → Checkbox

WinFactory → WinButton + WinCheckbox
MacFactory → MacButton + MacCheckbox
```

The client depends only on `AbstractFactory` and `Button`/`Checkbox` interfaces.

## vs Factory Method

| | Factory Method | Abstract Factory |
|---|----------------|------------------|
| Scope | One product per creator | Multiple related products |
| Structure | Creator subclass | Factory interface + product interfaces |
| Typical use | One variation axis | Platform / theme / vendor family |

Abstract Factory often **uses** Factory Methods internally for each product slot.

## Example shape

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

Switch `WinFactory` vs `MacFactory` once at application bootstrap.

## Trade-offs

| Gain | Cost |
|------|------|
| Enforces compatible product sets | Many interfaces and classes |
| Removes platform `if` chains from UI code | Adding a **new product kind** touches every factory |

## When to use

- Multiple products must stay consistent (themes, cross-platform UI, database driver families).
- You already have [[Design pattern/Adapter]] layers per vendor and need coordinated creation.

## When to skip

- Single product type — use [[Design pattern/Factory Method]].
- Products are unrelated — separate factories or direct construction suffice.

## Sources

- Gamma et al., *Design Patterns* (Abstract Factory)
- [Abstract factory pattern — Wikipedia](https://en.wikipedia.org/wiki/Abstract_factory_pattern)
