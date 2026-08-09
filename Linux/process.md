[[Linux]] [[Linux Process Theory]] [[TTY (teletypewriter)]] [[file descriptors]]

# Process

> A process is a running program with its own PID, memory, and open files — the unit Linux schedules and isolates.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Linux starts a process with `fork`/`clone`, optionally replaces its image with `exec`, then schedules it until it exits and the parent reaps it.

```txt
disk binary ──exec──► address space (text/data/heap/stack)
                           │
                     open fds (0,1,2,…)
                           │
                     PID / TID / namespaces / cgroup
                           │
                     scheduler (R/S/D/T/Z …)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **PID** | Process id the kernel tracks | “Each running program gets a PID.” |
| **Task / TID** | Schedulable thread (Linux: same as PID for main) | “Linux schedules threads; the main one often shares the PID.” |
| **Virtual address space** | Private memory map the process sees | “Processes don’t share memory unless they ask.” |
| **pts / tty** | Controlling terminal device | “TTY `?` means no terminal — typical for daemons.” |
| **STAT** | One-letter run state in `ps`/`top` | “`D` is stuck in uninterruptible I/O; `Z` is a zombie.” |
| **Shebang (`#!`)** | First line naming the interpreter | “The kernel runs `/usr/bin/env bash` for that script.” |

### Process states (short)

| Letter | Meaning |
|--------|---------|
| **R** | Running or runnable |
| **S** | Interruptible sleep (waiting; signals wake it) |
| **D** | Uninterruptible sleep (usually disk I/O) |
| **T** | Stopped (job control / debugger) |
| **Z** | Zombie — exited, parent has not `wait`ed |

### pts vs tty

- **tty** — classic terminal device (`/dev/ttyN`, serial).
- **pts** — pseudo-terminal slave (`/dev/pts/N`); master end sits in the terminal emulator (SSH, gnome-terminal).
- Slave name starts with `pts/`; programs talk to the slave as if it were a real terminal.

### How the story goes (4 steps)

1. **Create** — parent `fork`/`clone` → child shares copy-on-write memory and open fds.
2. **Become** — child often `execve` loads a new binary (or shebang → interpreter).
3. **Run** — scheduler time-slices; process sleeps on I/O, signals, locks.
4. **Exit / reap** — child exits → zombie until parent `wait`/`waitpid` (or `init`/`systemd` adopts orphans).

---

## Standard config / commands

```bash
# Who owns this PID
ps -p <pid> -o user,pid,ppid,stat,tty,cmd

# Memory map (regions + permissions)
cat /proc/<pid>/maps
pmap -XX <pid>

# Enter namespaces of a containerized process (careful)
nsenter -t <pid> -m -u -i -n -p /bin/bash

# List your processes; kill by name / signal
pgrep -l -u "$USER"
kill -l                    # signal names
kill -s TERM <pid>         # polite stop
kill -s QUIT <pid>         # quit (often dumps core if enabled)
pkill -f 'my-app'          # by pattern — double-check matches

# Who listens (often next step after “process won’t die”)
sudo lsof -i -P -n | grep LISTEN
```

| Knob / view | Why it matters |
|-------------|----------------|
| `/proc/<pid>/maps` | See stack, heap, libs, permissions — OOM / segfault triage |
| `STAT` + `WCHAN` | Distinguish CPU burn vs I/O wait vs zombie |
| `TTY` column | Session-bound vs daemon (`?`) |
| Signal choice | `TERM` first; `KILL` (9) cannot be caught — last resort |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Port still in use after “kill” | `lsof -i :<port>`; child still alive | Kill the actual listener PID; check process group |
| Defunct / zombie rows | `ps -o pid,ppid,stat,cmd` → `Z` | Fix parent to `wait`; restart parent if stuck |
| Stuck “D” state | `cat /proc/<pid>/stack`; disk / NFS health | Fix storage/NFS; `KILL` will not help while in `D` |
| Wrong user owns process | `ps -p <pid> -o user` | Restart under correct user/systemd `User=` |
| Segfault / weird crash | `maps`, core, `dmesg` / journal | Bad pointer, stack overflow, ASLR mismatch — debug with gdb |
| Can’t attach debugger | Permissions / Yama | `CAP_SYS_PTRACE` or same user; check `/proc/sys/kernel/yama/ptrace_scope` |

---

## Gotchas

> [!WARNING]
> **`kill -9` is not cleanup** — it skips handlers; locks, temp files, and children can be left behind. Prefer `TERM`, then escalate.

> [!WARNING]
> **Zombie ≠ leak of memory** — a `Z` process holds almost no RAM; it is a slot waiting for `wait`. Hundreds of zombies mean a broken parent.

> [!WARNING]
> **`D` state ignores signals** — often blocked on disk or remote FS. Fix the I/O path; don’t spam `KILL`.

> [!WARNING]
> **Shebang path must exist** — `#!/usr/bin/python` fails on systems where Python is only `python3`. Prefer `#!/usr/bin/env python3`.

---

## When NOT to use

- **Don’t treat “process” as the isolation boundary for multi-tenant workloads** — use [[cgroup (Control Group)]], namespaces, or containers on top.
- **Don’t debug “which file is open” with only `ps`** — use [[lsof]] / `/proc/<pid>/fd` ([[file descriptors]]).
- **Don’t confuse thread CPU with process CPU** — see [[Thread]] and `top -H` / `ps -L`.

---

## Related

[[Linux Process Theory]] [[Linux process commands]] [[ps]] [[top]] [[lsof]] [[TTY (teletypewriter)]] [[file descriptors]] [[OOM (Linux Out Of Memory)]] [[Memory management]] [[system call]] [[Thread]] [[Inter Process Communication]]
