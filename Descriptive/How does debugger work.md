[[Descriptive]] [[DAP (Debug Adapter Protocol)]] [[LSP]]

# How does debugger work

> Debugger — runs (or attaches to) a process, stops at breakpoints, lets you inspect memory/stack and step.

---

## How it works

```txt
run → hit BP → inspect → step/continue
```

| Mode | Meaning |
|------|---------|
| Launch | Debugger starts process |
| Attach | Join existing PID/port |
| Remote | gdbserver / debug port |

---


## Configuration and commands

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

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| BP never hits | Wrong file/map | Sourcemaps; path |
| “Optimized out” | `-O2` | Debug build |
| Heisenbug | Timing | Log + reproduce less invasive |
| Attach refused | Permissions/port | Correct pid/port |

---


## Gotchas

> [!WARNING]
> **Prod attach** — security + perf; prefer careful sampling.

> [!WARNING]
> **Async stacks** — may need async call stacks enabled.

---


## When not to use

- **Trivial print bugs** — log first.
- **Race without repro** — `-race`/stress first.

---


## Related

[[DAP (Debug Adapter Protocol)]] [[Debugger configuratoin]] [[go debugging]] [[node debugger]]

## Sources

- [Wikipedia — How does debugger work](https://en.wikipedia.org/wiki/How_does_debugger_work)
