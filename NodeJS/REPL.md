[[NodeJS]] [[node inspect]] [[node command]]

# REPL

> Read-Eval-Print-Loop — interactive Node prompt to try JS without a file.

---

## Mental model

**Say it in one breath:** Type an expression, get a result; `.load` / `.save` move code between the session and files. Not a real script file — `require.main` / paths behave differently.

```txt
$ node → > 1+1 → 2
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **REPL** | Interactive eval | “Explore APIs quickly.” |
| **`.load` / `.save`** | File ↔ session | “Persist a scratchpad.” |
| **`require.main`** | Entry script | “Often unset / odd in REPL.” |

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `__dirname` missing | ESM context | Build from `import.meta.url` |
| `require.main` weird | REPL isn’t a file | Don’t rely on it for path logic |
| Top-level await | Old Node / mode | Newer Node REPL supports TLA |

---

## Gotchas

> [!WARNING]
> **Side effects stick** — vars and listeners remain until exit.

---

## When NOT to use

- **Automated tests** — real files + test runner.
- **Long scripts** — write a `.js` and `node` it.

---

## Related

[[node command]] [[node inspect]] [[Runtime Errors]]
