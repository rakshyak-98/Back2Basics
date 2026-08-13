[[javascript]] [[prototype]]

# Destructuring

> Unpack values from arrays/objects into bindings — shorter than manual indexing; defaults and rest supported.

---

## How it works

```txt
const { a: x = 1, ...rest } = obj
const [first, , third] = arr
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **rename** | `a: b` | “Bind prop `a` as `b`.” |
| **default** | `= value` | “When nullish/undefined (objects: undefined).” |
| **rest** | `...r` | “Remaining props/items.” |


## Configuration and commands

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

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Cannot destructure undefined | Null source | Default `= {}` / optional chain |
| Got `undefined` not default | `null` prop | Defaults only for `undefined` |
| Rest dropped keys | Needed them | Don’t omit in rest pattern |
| Confusion with TS types | `: Type` vs rename | Careful colon meaning |

---


## Gotchas

> [!WARNING]
> **Defaults don’t run for `null`** — only `undefined`.

> [!WARNING]
> **Parameter destructuring + no default** — `f(undefined)` throws.

---


## When not to use

- **Deep optional trees** — readability dies; intermediate variables help.
- **Huge objects once** — sometimes explicit access is clearer.

---


## Related

[[promise]] [[prototype]]

## Sources

- [Wikipedia — Destructuring](https://en.wikipedia.org/wiki/Destructuring)
