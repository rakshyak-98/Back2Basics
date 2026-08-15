[[Commands]] [[Linux Process Theory]] [[process]] [[Linux process commands]]

# gdb

> gdb (GNU Debugger) stops a program mid-flight — inspect stack, memory, and variables when it crashes or misbehaves.

## Interview Relevance
Shows you can get a backtrace from a core or live attach, know symbols/build-id matter, and that attaching pauses production.

## Sources
- [GDB User Manual](https://sourceware.org/gdb/current/onlinedocs/gdb/) — deep-dive
- [gdb(1)](https://man7.org/linux/man-pages/man1/gdb.1.html) — overview

## Core Definition
gdb loads a binary (ideally with debug symbols), runs or attaches to a PID, or opens a core dump. You set breakpoints, continue, and inspect threads/stack/memory. Matching build-id/symbols turns addresses into function names.

## Key Concepts
- **bt / bt full:** Backtrace; with locals.
- **Attach vs core:** Live pause vs post-mortem.
- **Symbols:** Stripped bins limit usefulness; debuginfo packages help.
- **ptrace_scope:** Yama often blocks attach unless parent/sudo.
- **Threads:** `info threads` / `thread apply all bt`.

## Technical Details

```bash
gdb ./myapp
(gdb) run arg1 arg2

gdb -p <pid>

gdb ./myapp /var/lib/systemd/coredump/...

(gdb) bt
(gdb) bt full
(gdb) info threads
(gdb) thread apply all bt
(gdb) info proc mappings
(gdb) x/32xg $rsp
(gdb) print varname
(gdb) break main
(gdb) continue
(gdb) quit
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Attach denied | Yama ptrace_scope | sudo; parent process; careful sysctl |
| Useless addresses | Stripped binary | Install debuginfo; matching build |
| Production stall | Live attach | Prefer core/`coredumpctl` / profilers |
| Wrong core | Mismatched binary | Same build that produced the dump |

## Real-World Applications
Explaining a segfault from `coredumpctl gdb`, catching a deadlock with all-thread backtraces, and verifying a null deref hypothesis on a staging binary with symbols.

## Pros/Cons or Trade-offs
- **Pro:** Ground truth for crashes and weird state.
- **Con:** Stops the process; steep on optimized/stripped builds.
- **Trade-off:** gdb deep dive vs sampling (`perf`) for CPU without full stop.

## Comparison
vs [[process]]/`ps`: listing vs inspecting insides. vs strace: syscalls vs source-level stack. vs production APM: continuous telemetry vs interactive debug.

## Mistakes to Avoid
- Attaching to a latency-sensitive prod process casually.
- Analyzing cores with the wrong binary/build-id.
- Ignoring thread stacks on multi-threaded hangs.
