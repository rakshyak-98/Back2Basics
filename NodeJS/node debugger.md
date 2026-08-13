<!-- note-strategy: operational -->
[[NodeJS]] [[node inspect]] [[REPL]] [[Runtime Errors]]

# node debugger

> Breakpoints and step-through for Node — Inspector protocol via `--inspect` / built-in debugger.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Start with inspect flag → Chrome DevTools or VS Code attaches → set breakpoints, watch closures, profile CPU.

```txt
node --inspect=9229 app.js → DevTools → chrome://inspect
node --inspect-brk app.js  → break before user code
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Inspector** | Debug protocol | “Same as Chrome for V8.” |
| **inspect-brk** | Pause on start | “Catch boot issues.” |
| **debugger;** | Hardcoded breakpoint | “Trips only when attached.” |

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Can’t attach | Port/firewall | Check listen address; localhost first |
| Breakpoint never hits | Sourcemaps / wrong file | Map dist→src; break on resolved path |
| Hangs only under debug | Timing/race | Look for race; don’t “fix” by sleeping |
| Prod compromised | Inspect on 0.0.0.0 | Bind localhost; auth tunnel |

---

## Gotchas

> [!WARNING]
> **`--inspect` on public interfaces** — unauthenticated RCE surface. Tunnel instead.

> [!WARNING]
> **Async stack traces** — enable async stacks in DevTools for promises.

---

## When NOT to use

- **Production traffic debugging** — prefer logs/metrics/traces.
- **Flaky tests** — fix determinism; don’t rely on stepping forever.

---

## Related

[[node inspect]] [[REPL]] [[Optimization]]
