[[Descriptive]] [[DAP (Debug Adapter Protocol)]] [[LSP]] [[How does debugger work]] [[unbound breakpoint]]

# Debugger configuratoin

> Debugger configuration wires your editor to a debug adapter — breakpoints, launch vs attach, and environment.

## Interview Relevance

Launch/attach config interviews check env vars, source maps, and unbound breakpoints.

## Sources

- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts

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

## Technical Details

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

## Pros/Cons or Trade-offs

- **One-line print in a script** — logging may be faster.
- **production live traffic** — prefer tracing; debugger pauses freeze work.

## Mistakes to Avoid

> [!WARNING]
> **Debugging minified prod without maps** — useless; use source maps or attach to non-minified.

> [!WARNING]
> **Multiple launch configs** — wrong one selected silently.

| Symptom | Check | Fix |
|---------|-------|-----|
| Unbound breakpoint | maps / path | Enable sourcemaps; match paths |
| Can’t attach | port/pid | Correct debug port |
| Env missing | launch env | Copy required vars |
| Breaks in wrong file | path mapping | Fix `sourceMapPathOverrides` |

