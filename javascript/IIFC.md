[[javascript]] [[hoisting]] [[Callback]]

# IIFC (IIFE)

> Immediately Invoked Function Expression — run a function once at definition time to make a private scope.

---

## How it works

```txt
(function (global) { /* private */ return api })(window)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **IIFE** | Invoke at once | “Scope before ES modules.” |
| **module pattern** | Return revealing API | “Closure privacy.” |
| **async IIFE** | Top-level await polyfill | “`(async () => { await … })()`.” |


## Configuration and commands

```js
const counter = (() => {
  let n = 0
  return { inc: () => ++n, value: () => n }
})()

;(async () => {
  await init()
})()
```

| Knob | Why it matters |
|------|----------------|
| Leading `;` | Avoid ASI merging with prior line |
| Arrow IIFE | `( () => {} )()` |
| Strict mode | `'use strict'` inside |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Not a function error | Missing `()` invoke | Add invocation parens |
| ASI bug | `}(` after expression | Leading semicolon |
| Unhandled rejection | Async IIFE | `.catch` on the promise |
| Globals leak | Forgot const/let | Use block/module scope |

---


## Gotchas

> [!WARNING]
> **ES modules already have scope** — IIFE rarely needed in modern apps.

> [!WARNING]
> **Async IIFE errors** — become unhandled rejections if not caught.

---


## When not to use

- **ESM/CJS modules** — use real modules.
- **React components** — don’t IIFE for render logic casually.

---


## Related

[[hoisting]] [[UMD global]] [[AMD module]]

## Sources

- [Wikipedia — IIFC](https://en.wikipedia.org/wiki/IIFC)
