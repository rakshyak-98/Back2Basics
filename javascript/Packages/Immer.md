[[javascript]] [[Packages/npm packages]] [[Redux/Immutability in Redux]] [[Redux toolkit]] [[mixin]]

# Packages/Immer

> Write “mutating” updates that produce immutable next state — Immer uses a draft proxy (powers RTK reducers).

```txt
        Packages/Immer ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use **Packages/Immer** to check whether you can explain the mech…

## Sources
- [Immer — Docs](https://immerjs.github.io/immer/) — deep-dive
- [Wikipedia — Immer](https://en.wikipedia.org/wiki/Immer) — overview

## Key Concepts
- **draft:** Temporary mutable view — Mutate draft; Immer records patches.
- **produce:** Main API — Recipe function updates draft.
- **structural sharing:** Unchanged branches reuse refs — Cheap React/Redux compares.

## Technical Details
```txt
base → draft proxy → produce → next (immutable)
```

```js
import { produce } from 'immer'

const next = produce(state, (draft) => {
  draft.user.name = 'Ada'
  draft.tags.push('admin')
})
```

| Knob | Why it matters |
|------|----------------|
| `current(draft)` | Read plain object mid-recipe |
| `original(draft)` | Base snapshot |
| Freeze (dev) | Catch accidental mutates of result |

## Mistakes to Avoid
- **Mistake:** **Don’t mutate `original` or freeze results** — only the draft
- **Mistake:** **Returning a new object from recipe replaces root**
- **Mistake:** **“Cannot assign to read only”:** check Mutating outside produce
- **Mistake:** **Returned undefined oddly:** check Recipe returned a value + mu…
- **Mistake:** **Perf issues:** check Huge trees / frequent produce
- **Mistake:** **Class instances weird:** check Proxies + classes

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Write “mutating” updates that produce immutable next state — Immer uses a draft …).
- **Con / when not:** **Trivial one-field updates** — spread may be enough.
- **Con / when not:** **Hot per-frame game state**

## Comparison
- vs [[Packages/npm packages]]: know when each applies


### Use cases
- In production APIs and tooling, **Immer** shows up whenever teams ship Node/J…
