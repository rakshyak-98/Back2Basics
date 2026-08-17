[[zed config]] [[Descriptive/DAP (Debug Adapter Protocol)]] [[Linux/commands/gdb]] [[flutter debugging]]

# Zed debugger

> Debug Adapter integration in Zed — launch or attach; on Linux, attach uses `ptrace` and can fail when Yama `ptrace_scope` blocks it.

```txt
        Zed debugger ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers on tooling screens: distinguish launch vs attach, and know `kernel.…

## Sources
- [Kernel — Yama LSM](https://www.kernel.org/doc/Documentation/security/Yama.txt) — deep-dive
- [Zed — Debugger](https://zed.dev/docs/debugger) — overview

## Key Concepts
- **Launch:** debugger starts the process.
- **Attach:** debugger joins a PID via `ptrace` (Linux).
- **Console modes:** commands vs expressions
- **Yama scope:** `ptrace_scope=1` (common default) restricts attaching to non-child processes.

## Technical Details
- Typical attach failure:

```text
Could not attach: The current value of ptrace_scope is 1
sudo sysctl -w kernel.yama.ptrace_scope=0
```

- Prefer temporary/session changes and understand the security trade-off

| Symptom | Check | Fix |
|---------|-------|-----|
| Attach fails | `ptrace_scope` | Lower scope (know the risk) or launch instead |
| Wrong process | PID | Re-select PID / restart debug config |
| Breakpoints unbound | Symbols / optimized build | Debug build; correct cwd |

## Mistakes to Avoid
- **Mistake:** Permanently setting `ptrace_scope=0` on shared hardening-sensiti…
- **Mistake:** Confusing “commands mode” console input with expression evaluati…
- **Mistake:** Attaching to the wrong PID after a restart

## Pros/Cons or Trade-offs
- **Pro:** Attach avoids restarting hard-to-reproduce state.
- **Con:** Loosening `ptrace_scope` weakens process isolation — use carefully.

## Comparison
- vs [[flutter debugging]]: Flutter has its own VM service path
- vs gdb attach: same kernel restriction class.


### Use cases
- Attach to a running Flutter/Android host process during a sticky bug

- **Example:** Hotel app Flutter frontend attach to PID fails on Ubuntu
