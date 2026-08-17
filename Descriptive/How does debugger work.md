[[Descriptive]] [[DAP (Debug Adapter Protocol)]] [[LSP]] [[Debugger configuratoin]] [[go debugging]] [[node debugger]]

# How does debugger work

> Debugger — runs (or attaches to) a process, stops at breakpoints, lets you inspect memory/stack and step.

```txt
        How does debugger  ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Debugger questions check breakpoints, stepping, and how debug adapters talk t…

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts
```txt
run → hit BP → inspect → step/continue
```

| Mode | Meaning |
|------|---------|
| Launch | Debugger starts process |
| Attach | Join existing PID/port |
| Remote | gdbserver / debug port |

## Technical Details
```bash
node --inspect=9229 app.js
dlv exec ./app
gdb ./app
```

| Knob | Why it matters |
|------|----------------|
| Debug symbols | `-g` / unminified |
| Sourcemaps | TS/JS mapping |
| Optimized code | Vars may vanish |

## Mistakes to Avoid
> [!WARNING]
> **Prod attach** — security + perf; prefer careful sampling.

> [!WARNING]
> **Async stacks** — may need async call stacks enabled.

| Symptom | Check | Fix |
|---------|-------|-----|
| BP never hits | Wrong file/map | Sourcemaps; path |
| “Optimized out” | `-O2` | Debug build |
| Heisenbug | Timing | Log + reproduce less invasive |
| Attach refused | Permissions/port | Correct pid/port |

## Pros/Cons or Trade-offs
- **Trivial print bugs** — log first.
- **Race without repro** — `-race`/stress first.
