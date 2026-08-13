[[Descriptive]] [[LSP]] [[Debugger configuratoin]]

# DAP (Debug Adapter Protocol)

> DAP is how editors talk to debuggers — breakpoints, stacks, and variables over a standard protocol (cousin of LSP).

---

## How it works

```txt
VS Code/Cursor ↔ DAP adapter ↔ node/gdb/lldb/…
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Adapter** | Protocol translator | “vscode-js-debug speaks DAP.” |
| **Launch/attach** | Start or join | “Same as debugger config.” |
| **Stopped event** | Hit breakpoint | “UI shows stack.” |
| **vs LSP** | Debug ≠ IntelliSense | “Different servers.” |

---


## Configuration and commands

```json
// launch.json request shapes map to DAP launch/attach
{ "type": "pwa-node", "request": "attach", "port": 9229 }
```

| Knob | Why it matters |
|------|----------------|
| Adapter extension | Must match language |
| Port / pipe | How IDE connects |
| Path mappings | Remote/container debug |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Adapter missing | extension | Install debugger extension |
| Can’t connect | port | Open debug port; firewall |
| Unbound BP | path map | Align remote paths |
| No variables | optimize-out | Debug build / less optimize |

---


## Gotchas

> [!WARNING]
> **LSP green ≠ DAP ready** — language server doesn’t set breakpoints.

> [!WARNING]
> **Container path mismatch** — breakpoints need `localRoot`/`remoteRoot`.

---


## When not to use

- **Log-only investigation** — sometimes enough.
- **production pausing** — prefer tracing/metrics.


## Related

[[LSP]] [[Debugger configuratoin]] [[How does debugger work]]

## Sources

- [Wikipedia — DAP](https://en.wikipedia.org/wiki/DAP)
