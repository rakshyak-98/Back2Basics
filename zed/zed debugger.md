[[zed]]

# zed debugger

> One-line: what / why for **zed debugger** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

```text
Console is in 'commands' mode, prefix expressions with '?'.
Tried to launch debugger with: {
  "request": "attach",
  "name": "Attach New Session Setup",
  "pid": 32126,
  "cwd": "/home/mihir/GitHub/hotelApp_Flutter_Frontend"
}
error: Could not attach: The current value of ptrace_scope is 1, which can cause ptrace to fail to attach to a running process. To fix this, run:
	sudo sysctl -w kernel.yama.ptrace_scope=0
For more information, see: https://www.kernel.org/doc/Documentation/security/Yama.txt.
```
- The debugger is trying to attach to an already running process using Linux's `ptrace()` system call

## Standard config / commands

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
