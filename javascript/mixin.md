[[javascript]] [[prototype]] [[Packages/Immer]]

# mixin

> Copy or compose behavior into objects/classes — share methods without deep inheritance trees.

---

## Mental model

**Say it in one breath:** A mixin is a bag of methods you assign onto a prototype or fold into a class. Prefer composition (has-a) when possible; mixins when many types need the same behavior.

```txt
Object.assign(Target.prototype, editableMixin)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **mixin** | Reusable behavior fragment | “Horizontal reuse vs vertical inheritance.” |
| **composition** | Own a helper object | “Often clearer than mixin.” |
| **conflict** | Same method name | “Last assign wins — dangerous.” |

## Standard config / commands

```js
const canSpeak = {
  speak() { return this.phrase },
}
class Robot {}
Object.assign(Robot.prototype, canSpeak)

// Or functional
const withSpeak = (Base) => class extends Base {
  speak() { return this.phrase }
}
```

| Knob | Why it matters |
|------|----------------|
| Assign to prototype | Shared methods |
| Instance assign | Per-object overrides |
| TypeScript mixins | Constrained generics pattern |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Wrong `this` | Detached method | Call via object / bind |
| Method clash | Two mixins same name | Rename; compose explicitly |
| Hard to trace | Too many mixins | Prefer explicit helpers |
| Broken instanceof expectations | Prototype soup | Document lineage |

---

## Gotchas

> [!WARNING]
> **Order matters** — later `Object.assign` overwrites methods silently.

> [!WARNING]
> **Stateful mixins** — shared mutable props on prototype bite everyone.

---

## When NOT to use

- **One class needs the behavior** — just write a method.
- **React** — hooks/HOCs replaced mixin era (`React.createClass` mixins are gone).

---

## Related

[[prototype]] [[React Pattern/Higher order Component (HOCs)]] [[Packages/Immer]]
