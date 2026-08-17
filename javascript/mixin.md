[[javascript]] [[prototype]] [[Packages/Immer]] [[React Pattern/Higher order Component (HOCs)]]

# mixin

> Copy or compose behavior into objects/classes — share methods without deep inheritance trees.

```txt
        mixin ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use **mixin** to check whether you can explain the mechanism in …

## Sources
- [Wikipedia — mixin](https://en.wikipedia.org/wiki/mixin) — overview

## Key Concepts
- **mixin:** Reusable behavior fragment — Horizontal reuse vs vertical inheritance.
- **composition:** Own a helper object — Often clearer than mixin.
- **conflict:** Same method name — Last assign wins — dangerous.

## Technical Details
```txt
Object.assign(Target.prototype, editableMixin)
```

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

## Mistakes to Avoid
- **Mistake:** **Order matters**
- **Mistake:** **Stateful mixins**
- **Mistake:** **Wrong `this`:** check Detached method
- **Mistake:** **Method clash:** check Two mixins same name
- **Mistake:** **Hard to trace:** check Too many mixins
- **Mistake:** **Broken instanceof expectations:** check Prototype soup

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Copy or compose behavior into objects/classes — share methods without deep inher…).
- **Con / when not:** **One class needs the behavior** — just write a method.
- **Con / when not:** **React**

## Comparison
- vs [[prototype]]: know when each applies


### Use cases
- In production APIs and tooling, **mixin** shows up whenever teams ship Node/J…
