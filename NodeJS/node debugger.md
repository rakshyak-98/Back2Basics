[[NodeJS]] [[node inspect]] [[REPL]] [[Runtime Errors]] [[Optimization]]

# node debugger

> Breakpoints and step-through for Node — Inspector protocol via `--inspect` / built-in debugger.

## Interview Relevance

Interviewers use **node debugger** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **Inspector**, **inspect-brk**, **debugger;**.

## Sources

- [Node.js — Debugging](https://nodejs.org/en/learn/getting-started/debugging) — deep-dive
- [Wikipedia — node debugger](https://en.wikipedia.org/wiki/node_debugger) — overview

## Key Concepts

- **Inspector:** Debug protocol — Same as Chrome for V8.
- **inspect-brk:** Pause on start — Catch boot issues.
- **debugger;:** Hardcoded breakpoint — Trips only when attached.

## Technical Details

```txt
node --inspect=9229 app.js → DevTools → chrome://inspect
node --inspect-brk app.js  → break before user code
```

```bash
node --inspect app.js
node --inspect-brk=0.0.0.0:9229 app.js  # careful: network exposure
```

```js
debugger // breakpoint when inspector connected
```

| Knob | Why it matters |
|------|----------------|
| Port 9229 | Default inspect port |
| VS Code launch.json | `runtimeArgs: ["--inspect"]` |
| `NODE_OPTIONS=--inspect` | Attach without code change |

## Real-World Applications

In production APIs and tooling, **node debugger** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **`--inspect` on public interfaces** — unauthenticated RCE surface. Tunnel instead; **Async stack traces** — enable async stacks in DevTools for promises.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Breakpoints and step-through for Node — Inspector protocol via `--inspect` / bui…).
- **Con / when not:** **Production traffic debugging** — prefer logs/metrics/traces.
- **Con / when not:** **Flaky tests** — fix determinism; don’t rely on stepping forever.

## Comparison

vs [[node inspect]]: know when each applies — do not treat them as interchangeable. vs [[REPL]]: know when each applies — do not treat them as interchangeable. vs [[Runtime Errors]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **`--inspect` on public interfaces** — unauthenticated RCE surface. Tunnel instead.
- **Async stack traces** — enable async stacks in DevTools for promises.
- **Can’t attach:** check Port/firewall; fix: Check listen address; localhost first
- **Breakpoint never hits:** check Sourcemaps / wrong file; fix: Map dist→src; break on resolved path
- **Hangs only under debug:** check Timing/race; fix: Look for race; don’t “fix” by sleeping
- **Prod compromised:** check Inspect on 0.0.0.0; fix: Bind localhost; auth tunnel
