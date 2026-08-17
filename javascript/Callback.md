[[javascript]] [[promise]] [[event listener]] [[IIFC]]

# Callback

> Function passed to be called later — Node-style `(err, value)` or browser event handlers; precursor to Promises.

```txt
        Callback ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use **Callback** to check whether you can explain the mechanism …

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

## Mistakes to Avoid
- **Mistake:** **Sync callbacks** (Array.map) vs async
- **Mistake:** **Mixing promise and callback** in one API
- **Mistake:** **Callback hell:** check Deep nesting
- **Mistake:** **Double callback:** check Error + success paths
- **Mistake:** **Lost error:** check Ignored first arg; fix: Check `err`
- **Mistake:** **Wrong `this`:** check Method as cb; fix: bind / arrow

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Function passed to be called later — Node-style `(err, value)` or browser event …).
- **Con / when not:** **New async Node APIs**
- **Con / when not:** **Complex parallel flows**

## Comparison
- vs [[promise]]: Promises chain and surface rejection; raw callbacks need expl…


### Use cases
- In production APIs and tooling, **Callback** shows up whenever teams ship Nod…
