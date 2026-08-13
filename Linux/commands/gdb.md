[[commands]] [[Linux Process Theory]] [[process]]

# gdb

> gdb (GNU Debugger) stops a program mid-flight — inspect stack, memory, and variables when it crashes or misbehaves.

---

## How it works

```txt
binary (+ symbols) ──► gdb ──► run / attach PID
                         │
                         ├─ breakpoints / catchpoints
                         ├─ backtrace (bt)
                         └─ print / examine memory
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **`bt` / `bt full`** | Backtrace | “First thing after a crash — where were we?” |
| **`attach` / `-p`** | Live process | “Don’t restart; attach to the hung PID.” |
| **Symbols / `-g`** | Debug info | “Without symbols you get addresses, not names.” |
| **core dump** | Memory snapshot at crash | “`gdb binary core` post-mortem.” |
| **`thread apply all bt`** | All threads’ stacks | “Deadlocks show who waits on whom.” |

---


## Configuration and commands

```bash
# Start
gdb ./myapp
(gdb) run arg1 arg2

# Attach live
gdb -p <pid>
# or: gdb ./myapp <pid>

# Core
gdb ./myapp /var/lib/systemd/coredump/...   # or core.1234

# Inside gdb
(gdb) bt
(gdb) bt full
(gdb) info threads
(gdb) thread apply all bt
(gdb) info proc mappings
(gdb) x/32xg $rsp          # examine stack (x86_64)
(gdb) print varname
(gdb) break main
(gdb) continue
(gdb) quit
```

| Need | Command |
|------|---------|
| Where did we crash? | `bt` |
| Local vars in frame | `bt full` / `info locals` |
| Memory map | `info proc mappings` |
| Follow fork | `set follow-fork-mode child` |

Build with symbols: `gcc -g -O0` for debug; production often needs `debuginfod` or separate debug packages.

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| `No symbol table` | Stripped binary | Install `-dbgsym` / rebuild with `-g` |
| Attach denied | ptrace scope | `sudo`; check `/proc/sys/kernel/yama/ptrace_scope` |
| Hang on attach | Threads blocked | `thread apply all bt`; look for locks |
| Core not produced | ulimit / systemd | `ulimit -c unlimited`; `coredumpctl` |
| Optimized code lies | `-O2` inlining | Expect odd line numbers; use `-O0` for repro |

---


## Gotchas

> [!WARNING]
> **Attaching pauses the process** — on production, prefer core/`coredumpctl` or sampling profilers unless you accept downtime.

> [!WARNING]
> **ASLR / stripped bins** — addresses alone rarely help without symbols and matching build-id.

> [!WARNING]
> **Yama ptrace_scope=1** (common) — only parent can ptrace; use sudo or adjust carefully.

---


## When not to use

- **Language-native debuggers** — Delve (Go), `pdb`/`debugpy` (Python), Chrome DevTools — when they fit better.
- **Perf / latency profiling** — `perf`, eBPF, continuous profilers.
- **“Just restart it” incidents** — gather core + logs first if the bug is rare.

---


## Related

[[process]] [[Linux Process Theory]] [[Linux process commands]] [[commands]]

## Sources

- [Wikipedia — gdb](https://en.wikipedia.org/wiki/gdb)
