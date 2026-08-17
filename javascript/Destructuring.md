[[javascript]] [[prototype]] [[promise]]

# Destructuring

> Unpack values from arrays/objects into bindings — shorter than manual indexing; defaults and rest supported.

```txt
        Destructuring ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use **Destructuring** to check whether you can explain the mecha…

## Sources
- [MDN — Destructuring](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring) — deep-dive
- [Wikipedia — Destructuring](https://en.wikipedia.org/wiki/Destructuring) — overview

## Key Concepts
- **rename:** `a: b` — Bind prop `a` as `b`.
- **default:** `= value` — When nullish/undefined (objects: undefined).
- **rest:** `...r` — Remaining props/items.

## Technical Details
```txt
const { a: x = 1, ...rest } = obj
const [first, , third] = arr
```

```js
function f({ id, name = 'anon' } = {}) { /* … */ }
const { data: { items = [] } = {} } = response
const [head, ...tail] = list
```

| Knob | Why it matters |
|------|----------------|
| `= {}` on params | Allow `f()` with no args |
| Computed keys | `[key]: value` |
| Array holes | Skip with commas |

## Mistakes to Avoid
- **Mistake:** **Defaults don’t run for `null`** — only `undefined`
- **Mistake:** **Parameter destructuring + no default** — `f(undefined)` throws
- **Mistake:** **Cannot destructure undefined:** check Null source
- **Mistake:** **Got `undefined` not default:** check `null` prop
- **Mistake:** **Rest dropped keys:** check Needed them
- **Mistake:** **Confusion with TS types:** check `: Type` vs rename

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Unpack values from arrays/objects into bindings — shorter than manual indexing; …).
- **Con / when not:** **Deep optional trees**
- **Con / when not:** **Huge objects once**

## Comparison
- vs [[prototype]]: know when each applies


### Use cases
- In production APIs and tooling, **Destructuring** shows up whenever teams shi…
