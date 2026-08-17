[[javascript]] [[hoisting]] [[Callback]] [[UMD global]] [[AMD module]]

# IIFC (IIFE)

> Immediately Invoked Function Expression — run a function once at definition time to make a private scope.





## Interview Relevance
Interviewers use **IIFC (IIFE)** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **IIFE**, **module pattern**, **async IIFE**.

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

## Real-World Applications
In production APIs and tooling, **IIFC** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **ES modules already have scope** — IIFE rarely needed in modern apps; **Async IIFE errors** — become unhandled rejections if not caught.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Immediately Invoked Function Expression — run a function once at definition time…).
- **Con / when not:** **ESM/CJS modules** — use real modules.
- **Con / when not:** **React components** — don’t IIFE for render logic casually.

## Comparison
vs [[hoisting]]: know when each applies — do not treat them as interchangeable. vs [[Callback]]: know when each applies — do not treat them as interchangeable. vs [[UMD global]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **ES modules already have scope** — IIFE rarely needed in modern apps.
- **Async IIFE errors** — become unhandled rejections if not caught.
- **Not a function error:** check Missing `()` invoke; fix: Add invocation parens
- **ASI bug:** check `}(` after expression; fix: Leading semicolon
- **Unhandled rejection:** check Async IIFE; fix: `.catch` on the promise
- **Globals leak:** check Forgot const/let; fix: Use block/module scope
