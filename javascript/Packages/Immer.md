[[javascript]] [[Packages/npm packages]] [[Redux/Immutability in Redux]]

# Packages/Immer

> Write “mutating” updates that produce immutable next state — Immer uses a draft proxy (powers RTK reducers).

---

## How it works

```txt
base → draft proxy → produce → next (immutable)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **draft** | Temporary mutable view | “Mutate draft; Immer records patches.” |
| **produce** | Main API | “Recipe function updates draft.” |
| **structural sharing** | Unchanged branches reuse refs | “Cheap React/Redux compares.” |


## Configuration and commands

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

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| “Cannot assign to read only” | Mutating outside produce | Only mutate draft |
| Returned undefined oddly | Recipe returned a value + mutated | Either mutate *or* return new root |
| Perf issues | Huge trees / frequent produce | Normalize; split state |
| Class instances weird | Proxies + classes | Prefer plain objects |

---


## Gotchas

> [!WARNING]
> **Don’t mutate `original` or freeze results** — only the draft.

> [!WARNING]
> **Returning a new object from recipe replaces root** — don’t mix with draft mutations carelessly.

---


## When not to use

- **Trivial one-field updates** — spread may be enough.
- **Hot per-frame game state** — proxy cost may matter; measure.

---


## Related

[[Redux/Immutability in Redux]] [[Redux toolkit]] [[mixin]]

## Sources

- [Wikipedia — Immer](https://en.wikipedia.org/wiki/Immer)
