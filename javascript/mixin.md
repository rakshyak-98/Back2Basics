[[javascript]] [[prototype]] [[Packages/Immer]] [[React Pattern/Higher order Component (HOCs)]]

# mixin

> Copy or compose behavior into objects/classes — share methods without deep inheritance trees.

## Interview Relevance

Interviewers use **mixin** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **mixin**, **composition**, **conflict**.

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

## Real-World Applications

In production APIs and tooling, **mixin** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Order matters** — later `Object.assign` overwrites methods silently; **Stateful mixins** — shared mutable props on prototype bite everyone.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Copy or compose behavior into objects/classes — share methods without deep inher…).
- **Con / when not:** **One class needs the behavior** — just write a method.
- **Con / when not:** **React** — hooks/HOCs replaced mixin era (`React.createClass` mixins are gone).

## Comparison

vs [[prototype]]: know when each applies — do not treat them as interchangeable. vs [[Packages/Immer]]: know when each applies — do not treat them as interchangeable. vs [[React Pattern/Higher order Component (HOCs)]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **Order matters** — later `Object.assign` overwrites methods silently.
- **Stateful mixins** — shared mutable props on prototype bite everyone.
- **Wrong `this`:** check Detached method; fix: Call via object / bind
- **Method clash:** check Two mixins same name; fix: Rename; compose explicitly
- **Hard to trace:** check Too many mixins; fix: Prefer explicit helpers
- **Broken instanceof expectations:** check Prototype soup; fix: Document lineage
