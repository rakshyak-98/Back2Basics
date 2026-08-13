[[Descriptive]] [[DAP (Debug Adapter Protocol)]] [[LSP]]

# How does debugger work

> Debugger — runs (or attaches to) a process, stops at breakpoints, lets you inspect memory/stack and step.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Insert breakpoints (software INT or hardware). On hit, freeze thread, map PC → source via debug information/sourcemaps, show frames/variables, then continue/step.

```txt
run → hit BP → inspect → step/continue
```

| Mode | Meaning |
|------|---------|
| Launch | Debugger starts process |
| Attach | Join existing PID/port |
| Remote | gdbserver / debug port |

---

## Standard config / commands

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

## Triage (when things break)

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

## When NOT to use

- **Trivial print bugs** — log first.
- **Race without repro** — `-race`/stress first.

---

## Related

[[DAP (Debug Adapter Protocol)]] [[Debugger configuratoin]] [[go debugging]] [[node debugger]]
