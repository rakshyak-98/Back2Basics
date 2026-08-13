[[NodeJS]] [[node debugger]] [[REPL]]

# node inspect

> Built-in CLI debugger — `node inspect script.js`; step with `n`/`s`/`c`, inspect with `repl`.

---

## How it works

```txt
node inspect app.js → break → n/s/c/bt/repl → continue
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **next / step / out** | Over / into / return | “CLI stepping without an IDE.” |
| **backtrace (`bt`)** | Call stack | “How we got here.” |
| **repl** | Eval in frame | “Print locals live.” |


## Configuration and commands

```bash
node inspect app.js
# in debugger:
#   c / n / s / o / bt / l / repl / watch('x') / b 12 / q
```

```js
debugger // pause when inspector attached
```

| Cmd | Why it matters |
|-----|----------------|
| `c` continue | Next breakpoint |
| `n` / `s` / `o` | Step over / in / out |
| `watch('expr')` | Auto-print on stop |
| `break <line>` | Set breakpoint |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Never pauses | No `debugger;` / break | Add statement or `b <line>` |
| Can’t see vars | Not in `repl` | Enter `repl`; exit with Ctrl+C |
| Wrong file | Sourcemaps / cwd | Run entry you expect |
| Prefer GUI | CLI friction | [[node debugger]] / DevTools |

---


## Gotchas

> [!WARNING]
> **Different from `--inspect`** — `node inspect` is the legacy CLI; CDP is `--inspect` + DevTools/VS Code.

---


## When not to use

- **Day-to-day IDE debug** — VS Code [[node debugger]] is faster.
- **production** — don’t leave `debugger;` in shipped code.

---


## Related

[[node debugger]] [[REPL]] [[node command]]

## Sources

- [Wikipedia — node inspect](https://en.wikipedia.org/wiki/node_inspect)
