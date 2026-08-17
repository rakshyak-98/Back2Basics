[[NodeJS]] [[node inspect]] [[node command]] [[Runtime Errors]]

# REPL

> Read-Eval-Print-Loop — interactive Node prompt to try JS without a file.

```txt
        REPL ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use **REPL** to check whether you can explain the mechanism in p…

## Sources
- [Node.js — REPL](https://nodejs.org/api/repl.html) — deep-dive
- [Wikipedia — REPL](https://en.wikipedia.org/wiki/REPL) — overview

## Key Concepts
- **REPL:** Interactive eval — Explore APIs quickly.
- **`.load` / `.save`:** File ↔ session — Persist a scratchpad.
- **`require.main`:** Entry script — Often unset / odd in REPL.

## Technical Details
```txt
$ node → > 1+1 → 2
```

```bash
node                 # start REPL
.help
.load ./scratch.js
.save session.js
.exit
```

```js
// ESM tip outside REPL
import { fileURLToPath } from 'node:url'
import path from 'node:path'
const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
```

| Knob | Why it matters |
|------|----------------|
| `NODE_REPL_HISTORY` | Persist command history |
| `_` | Last result |

## Mistakes to Avoid
- **Mistake:** **Side effects stick** — vars and listeners remain until exit
- **Mistake:** **`__dirname` missing:** check ESM context
- **Mistake:** **`require.main` weird:** check REPL isn’t a file
- **Mistake:** **Top-level await:** check Old Node / mode

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Read-Eval-Print-Loop — interactive Node prompt to try JS without a file.).
- **Con / when not:** **Automated tests** — real files + test runner.
- **Con / when not:** **Long scripts** — write a `.js` and `node` it.

## Comparison
- vs [[node inspect]]: know when each applies


### Use cases
- In production APIs and tooling, **REPL** shows up whenever teams ship Node/JS…
