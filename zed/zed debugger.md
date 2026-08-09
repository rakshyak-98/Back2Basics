[[zed]]

# zed debugger

> zed debugger — console is in 'commands' mode, prefix expressions with '?'.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** zed debugger — plain job, how I run it, how I know it’s broken.


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

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **zed debugger** | Core idea of this note | “I can explain zed debugger without jargon.” |
| **mental model** | How it works in one line | “Explain it without jargon first.” |
| **failure mode** | How it breaks | “Say what you check first.” |

---

## Standard config / commands

```bash
# reproduce with minimal input
# compare working vs broken env
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Unexpected result | inputs / versions | Reproduce minimal case |
| Works on one machine | env drift | Diff config and versions |
| Silent failure | logs / metrics | Add checks and alerts |

---

## Gotchas

> [!WARNING]
> Prefer simple words you can say in an interview.

---

## When NOT to use

- Skip it when a simpler existing tool already fits.

---

## Related

[[zed]]
