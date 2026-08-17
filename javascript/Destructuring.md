[[javascript]] [[prototype]] [[promise]]

# Destructuring

> Unpack values from arrays/objects into bindings — shorter than manual indexing; defaults and rest supported.





## Interview Relevance
Interviewers use **Destructuring** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **rename**, **default**, **rest**.

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

## Real-World Applications
In production APIs and tooling, **Destructuring** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Defaults don’t run for `null`** — only `undefined`; **Parameter destructuring + no default** — `f(undefined)` throws.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Unpack values from arrays/objects into bindings — shorter than manual indexing; …).
- **Con / when not:** **Deep optional trees** — readability dies; intermediate variables help.
- **Con / when not:** **Huge objects once** — sometimes explicit access is clearer.

## Comparison
vs [[prototype]]: know when each applies — do not treat them as interchangeable. vs [[promise]]: know when each applies — do not treat them as interchangeable. vs [[prototype]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **Defaults don’t run for `null`** — only `undefined`.
- **Parameter destructuring + no default** — `f(undefined)` throws.
- **Cannot destructure undefined:** check Null source; fix: Default `= {}` / optional chain
- **Got `undefined` not default:** check `null` prop; fix: Defaults only for `undefined`
- **Rest dropped keys:** check Needed them; fix: Don’t omit in rest pattern
- **Confusion with TS types:** check `: Type` vs rename; fix: Careful colon meaning
