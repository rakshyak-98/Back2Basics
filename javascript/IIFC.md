[[javascript]] [[hoisting]] [[Callback]] [[UMD global]] [[AMD module]]

# IIFC (IIFE)

> Immediately Invoked Function Expression — run a function once at definition time to make a private scope.

```txt
        IIFC (IIFE) ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use **IIFC (IIFE)** to check whether you can explain the mechani…

## Sources
- [MDN — IIFE](https://developer.mozilla.org/en-US/docs/Glossary/IIFE) — deep-dive
- [Wikipedia — IIFC](https://en.wikipedia.org/wiki/IIFC) — overview

## Key Concepts
- **IIFE:** Invoke at once — Scope before ES modules.
- **module pattern:** Return revealing API — Closure privacy.
- **async IIFE:** Top-level await polyfill — `(async () => { await … })()`.

## Technical Details
```txt
(function (global) { /* private */ return api })(window)
```

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

## Mistakes to Avoid
- **Mistake:** **ES modules already have scope**
- **Mistake:** **Async IIFE errors** — become unhandled rejections if not caught
- **Mistake:** **Not a function error:** check Missing `()` invoke
- **Mistake:** **ASI bug:** check `}(` after expression; fix: Leading semicolon
- **Mistake:** **Unhandled rejection:** check Async IIFE
- **Mistake:** **Globals leak:** check Forgot const/let

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Immediately Invoked Function Expression — run a function once at definition time…).
- **Con / when not:** **ESM/CJS modules** — use real modules.
- **Con / when not:** **React components**

## Comparison
- vs [[hoisting]]: know when each applies


### Use cases
- In production APIs and tooling, **IIFC** shows up whenever teams ship Node/JS…
