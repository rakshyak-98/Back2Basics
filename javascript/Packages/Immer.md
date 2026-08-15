[[javascript]] [[Packages/npm packages]] [[Redux/Immutability in Redux]] [[Redux toolkit]] [[mixin]]

# Packages/Immer

> Write “mutating” updates that produce immutable next state — Immer uses a draft proxy (powers RTK reducers).

## Interview Relevance

Interviewers use **Packages/Immer** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **draft**, **produce**, **structural sharing**.

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

## Real-World Applications

In production APIs and tooling, **Immer** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Don’t mutate `original` or freeze results** — only the draft; **Returning a new object from recipe replaces root** — don’t mix with draft mutations carelessly.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Write “mutating” updates that produce immutable next state — Immer uses a draft …).
- **Con / when not:** **Trivial one-field updates** — spread may be enough.
- **Con / when not:** **Hot per-frame game state** — proxy cost may matter; measure.

## Comparison

vs [[Packages/npm packages]]: know when each applies — do not treat them as interchangeable. vs [[Redux/Immutability in Redux]]: know when each applies — do not treat them as interchangeable. vs [[Redux toolkit]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **Don’t mutate `original` or freeze results** — only the draft.
- **Returning a new object from recipe replaces root** — don’t mix with draft mutations carelessly.
- **“Cannot assign to read only”:** check Mutating outside produce; fix: Only mutate draft
- **Returned undefined oddly:** check Recipe returned a value + mutated; fix: Either mutate *or* return new root
- **Perf issues:** check Huge trees / frequent produce; fix: Normalize; split state
- **Class instances weird:** check Proxies + classes; fix: Prefer plain objects
