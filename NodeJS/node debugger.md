[[NodeJS]] [[node inspect]] [[REPL]] [[Runtime Errors]] [[Optimization]]

# node debugger

> Breakpoints and step-through for Node — Inspector protocol via `--inspect` / built-in debugger.

```txt
        node debugger ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use **node debugger** to check whether you can explain the mecha…

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

## Mistakes to Avoid
- **Mistake:** **`--inspect` on public interfaces**
- **Mistake:** **Async stack traces**
- **Mistake:** **Can’t attach:** check Port/firewall
- **Mistake:** **Breakpoint never hits:** check Sourcemaps / wrong file
- **Mistake:** **Hangs only under debug:** check Timing/race
- **Mistake:** **Prod compromised:** check Inspect on 0.0.0.0

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Breakpoints and step-through for Node — Inspector protocol via `--inspect` / bui…).
- **Con / when not:** **Production traffic debugging**
- **Con / when not:** **Flaky tests**

## Comparison
- vs [[node inspect]]: know when each applies


### Use cases
- In production APIs and tooling, **node debugger** shows up whenever teams shi…
