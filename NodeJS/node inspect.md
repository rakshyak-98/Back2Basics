[[NodeJS]] [[node debugger]] [[REPL]] [[node command]]

# node inspect

> Built-in CLI debugger — `node inspect script.js`; step with `n`/`s`/`c`, inspect with `repl`.

## Interview Relevance

Interviewers use **node inspect** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **next / step / out**, **backtrace (`bt`)**, **repl**.

## Sources

- [Node.js — Debugging](https://nodejs.org/en/learn/getting-started/debugging) — deep-dive
- [Wikipedia — node inspect](https://en.wikipedia.org/wiki/node_inspect) — overview

## Key Concepts

- **next / step / out:** Over / into / return — CLI stepping without an IDE.
- **backtrace (`bt`):** Call stack — How we got here.
- **repl:** Eval in frame — Print locals live.

## Technical Details

```txt
node inspect app.js → break → n/s/c/bt/repl → continue
```

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

## Real-World Applications

In production APIs and tooling, **node inspect** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Different from `--inspect`** — `node inspect` is the legacy CLI; CDP is `--inspect` + DevTools/VS Code; **Never pauses:** check No `debugger;` / break; fix: Add statement or `b <line>`.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Built-in CLI debugger — `node inspect script.js`; step with `n`/`s`/`c`, inspect…).
- **Con / when not:** **Day-to-day IDE debug** — VS Code [[node debugger]] is faster.
- **Con / when not:** **production** — don’t leave `debugger;` in shipped code.

## Comparison

vs [[node debugger]]: know when each applies — do not treat them as interchangeable. vs [[REPL]]: know when each applies — do not treat them as interchangeable. vs [[node command]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **Different from `--inspect`** — `node inspect` is the legacy CLI; CDP is `--inspect` + DevTools/VS Code.
- **Never pauses:** check No `debugger;` / break; fix: Add statement or `b <line>`
- **Can’t see vars:** check Not in `repl`; fix: Enter `repl`; exit with Ctrl+C
- **Wrong file:** check Sourcemaps / cwd; fix: Run entry you expect
- **Prefer GUI:** check CLI friction; fix: [[node debugger]] / DevTools
