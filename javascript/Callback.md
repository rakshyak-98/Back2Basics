[[javascript]] [[promise]] [[event listener]]

# Callback

> Function passed to be called later — Node-style `(err, value)` or browser event handlers; precursor to Promises.

---

## How it works

```txt
doWork(args, (err, result) => { … })
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **err-first** | Node convention | “First arg error or null.” |
| **continuation** | Next step as fn | “Control flow inverted.” |
| **promisify** | Wrap callback API | “`util.promisify`.” |


## Configuration and commands

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

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Callback hell | Deep nesting | promisify / async await |
| Double callback | Error + success paths | Guard `let called` |
| Lost error | Ignored first arg | Check `err` |
| Wrong `this` | Method as cb | bind / arrow |

---


## Gotchas

> [!WARNING]
> **Sync callbacks** (Array.map) vs async — don’t assume async scheduling.

> [!WARNING]
> **Mixing promise and callback** in one API — pick one style at the boundary.

---


## When not to use

- **New async Node APIs** — use promise variants (`fs/promises`).
- **Complex parallel flows** — Promise combinators / async utils.

---


## Related

[[promise]] [[event listener]] [[IIFC]]

## Sources

- [Wikipedia — Callback](https://en.wikipedia.org/wiki/Callback)
