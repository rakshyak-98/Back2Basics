[[javascript]] [[promise]] [[event listener]] [[IIFC]]

# Callback

> Function passed to be called later — Node-style `(err, value)` or browser event handlers; precursor to Promises.





## Interview Relevance
Interviewers use **Callback** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **err-first**, **continuation**, **promisify**.

## Sources
- [MDN — Callback function](https://developer.mozilla.org/en-US/docs/Glossary/Callback_function) — overview
- [Wikipedia — Callback](https://en.wikipedia.org/wiki/Callback) — overview

## Key Concepts
- **err-first:** Node convention — First arg error or null.
- **continuation:** Next step as fn — Control flow inverted.
- **promisify:** Wrap callback API — `util.promisify`.

## Technical Details
```txt
doWork(args, (err, result) => { … })
```

```js
import { readFile } from 'node:fs'
import { promisify } from 'node:util'

readFile('a.txt', 'utf8', (err, data) => {
  if (err) return console.error(err)
  console.log(data)
})

const read = promisify(readFile)
const data = await read('a.txt', 'utf8')
```

| Knob | Why it matters |
|------|----------------|
| Always handle `err` | Silent failures |
| Don’t call cb twice | Hard bugs |
| Prefer promises for new code | Composability |

## Real-World Applications
In production APIs and tooling, **Callback** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Sync callbacks** (Array.map) vs async — don’t assume async scheduling; **Mixing promise and callback** in one API — pick one style at the boundary.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Function passed to be called later — Node-style `(err, value)` or browser event …).
- **Con / when not:** **New async Node APIs** — use promise variants (`fs/promises`).
- **Con / when not:** **Complex parallel flows** — Promise combinators / async utils.

## Comparison
vs [[promise]]: Promises chain and surface rejection; raw callbacks need explicit error-first discipline. vs [[event listener]]: know when each applies — do not treat them as interchangeable. vs [[IIFC]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **Sync callbacks** (Array.map) vs async — don’t assume async scheduling.
- **Mixing promise and callback** in one API — pick one style at the boundary.
- **Callback hell:** check Deep nesting; fix: promisify / async await
- **Double callback:** check Error + success paths; fix: Guard `let called`
- **Lost error:** check Ignored first arg; fix: Check `err`
- **Wrong `this`:** check Method as cb; fix: bind / arrow
