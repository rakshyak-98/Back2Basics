[[Descriptive]] [[DAP (Debug Adapter Protocol)]] [[LSP]]

# Debugger configuratoin

> Debugger config wires your editor to a debug adapter — breakpoints, env, and program args in one launch profile.

---

## How it works

```txt
IDE ↔ DAP adapter ↔ runtime (node/python/gdb)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Launch vs attach** | Start process vs join | “Attach to running PID.” |
| **Breakpoint** | Pause line | “Unbound if sourcemap missing.” |
| **sourcemap** | Compiled → source | “TS/JS need maps.” |
| **cwd / env** | Process context | “Wrong cwd = missing files.” |

---


## Configuration and commands

```json
{
  "type": "node",
  "request": "launch",
  "name": "API",
  "program": "${workspaceFolder}/dist/index.js",
  "env": { "NODE_ENV": "development" },
  "sourceMaps": true
}
```

| Knob | Why it matters |
|------|----------------|
| `outFiles` / maps | Hit TS breakpoints |
| `skipFiles` | Skip node internals |
| `console` | Integrated vs external |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Unbound breakpoint | maps / path | Enable sourcemaps; match paths |
| Can’t attach | port/pid | Correct debug port |
| Env missing | launch env | Copy required vars |
| Breaks in wrong file | path mapping | Fix `sourceMapPathOverrides` |

---


## Gotchas

> [!WARNING]
> **Debugging minified prod without maps** — useless; use source maps or attach to non-minified.

> [!WARNING]
> **Multiple launch configs** — wrong one selected silently.

---


## When not to use

- **One-line print in a script** — logging may be faster.
- **production live traffic** — prefer tracing; debugger pauses freeze work.


## Related

[[DAP (Debug Adapter Protocol)]] [[How does debugger work]] [[unbound breakpoint]]

## Sources

- [Wikipedia — Debugger configuratoin](https://en.wikipedia.org/wiki/Debugger_configuratoin)
