[[Linux]] [[process]] [[system call]] [[Stack Frame]]

# Linux Process Theory

> Linux starts a new program with fork then exec — copy the parent, then replace the child’s memory with the new binary.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `fork` clones the running process; `execve` loads a new program into that PID; the kernel builds the stack with `argv`/`envp` and jumps to `_start`.

```txt
Parent                    Child
  │                         │
  ├─ fork() ───────────────►│  (same code, COW memory, shared open fds)
  │                         │
  │                    execve(path, argv, envp)
  │                         │  wipe address space → load ELF
  │                         │  stack: argc / argv / envp / auxv
  │                         └─ jump to _start → main
  │
  └─ waitpid() ◄── exit status
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **fork** | Duplicate this process | “Child starts as a copy; PID differs; COW avoids full memcpy.” |
| **execve** | Replace memory with a new program | “Same PID, new code — fork+exec is how shells run commands.” |
| **COW** | Copy-on-write pages | “Pages stay shared until one side writes.” |
| **PCB / task_struct** | Kernel’s process record | “Scheduler and signals hang off the task struct.” |
| **Signal** | Async event to a process | “Ctrl-C is SIGINT; handlers run between syscalls.” |
| **Stack grows down** | High address → lower on push | “Heap grows up; they meet in the middle of the VA space.” |

### How the story goes (fork → exec → stack)

1. **fork** — parent calls `fork`/`clone`; child returns `0`, parent gets child PID; memory is COW-shared.
2. **execve** — kernel checks path + execute bits; maps text/data/bss; tears down old mappings.
3. **Stack setup** — allocate stack (`mmap`-backed region); push `argv`, `envp`, ELF aux vector; set `rsp`.
4. **Enter user code** — program counter → `_start` (libc) → `main`.
5. **Signals** — generated → pending → delivered; interruptible sleeps can wake; `D` state does not.

### Kernel ↔ program touch points (keep short)

| Area | Job |
|------|-----|
| **System calls** | Only safe door into the kernel ([[system call]]) |
| **Memory** | Per-process VA; page faults; heap/stack ([[Memory management]]) |
| **Scheduling** | Who runs next on which CPU |
| **IPC** | Pipes, shm, sockets ([[Inter Process Communication]]) |
| **Devices** | Drivers behind `open`/`read`/`write` |
| **Signals** | Async notify / kill / job control |

---

## Standard config / commands

```bash
# Watch fork/exec/wait live
strace -f -e trace=process,execve -o /tmp/trace.txt ./my-app

# Limits that shape new processes
ulimit -a
ulimit -s          # stack size (KB)
cat /proc/<pid>/limits

# After exec: confirm binary + args
ps -p <pid> -o pid,ppid,cmd
tr '\0' ' ' < /proc/<pid>/cmdline; echo
readlink /proc/<pid>/exe

# Signal surface
kill -l
cat /proc/<pid>/status | grep -E 'Sig|State|PPid'
```

| Knob | Why it matters |
|------|----------------|
| `ulimit -s` / `RLIMIT_STACK` | Stack overflow vs large recursive workloads |
| `RLIMIT_NPROC` | “fork: Resource temporarily unavailable” |
| `CLONE_*` flags | Threads vs processes (shared VM vs separate) |
| `strace -f` | Follow children through fork/exec |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `fork failed: EAGAIN` | `ulimit -u`; cgroup pids.max | Raise nproc / fix leak of child processes |
| Exec fails (`ENOENT` / `EACCES`) | `ls -l` path; shebang; arch (ELF) | Fix path, mode `+x`, interpreter, or wrong ISA |
| Child zombies pile up | Parent never `wait`s | Add reaper / `SIGCHLD` handler; use double-fork carefully |
| Segfault right after start | Stack/argv huge; bad ELF | Check `ulimit -s`; `readelf -h`; ASLR / loader errors in `dmesg` |
| Signal ignored | Custom handler / mask | Inspect `SigBlk`/`SigIgn` in `/proc/<pid>/status` |
| “Works in shell, fails under systemd” | Env / cwd / limits differ | Compare `systemctl show` Environment + Limits |

---

## Gotchas

> [!WARNING]
> **fork alone is not “run a program”** — without `exec`, the child keeps running the parent’s code. Shells and supervisors always pair them.

> [!WARNING]
> **Threads + fork** — only the calling thread survives in the child; locks held by other threads stay locked forever. Prefer `posix_spawn` or exec soon after fork.

> [!WARNING]
> **Signals during `D` state** — uninterruptible sleep (often disk/NFS) will not run your handler until I/O completes.

> [!WARNING]
> **Stack size is a soft trap** — deep recursion or huge locals blow the stack while RSS still looks small.

---

## When NOT to use

- **Don’t fork a huge multi-threaded server per request** — use a thread pool, async I/O ([[Epoll]]), or a worker process pool started once.
- **Don’t teach “new process = full memory copy”** — COW makes fork cheap until writes; still costly if the parent dirties all pages.
- **Don’t use raw signal handlers for complex logic** — keep them async-signal-safe; prefer `signalfd` / self-pipe patterns in servers.

---

## Related

[[process]] [[system call]] [[Thread]] [[Stack Frame]] [[stack pointer]] [[Memory management]] [[Inter Process Communication]] [[file descriptors]] [[Epoll]] [[OOM (Linux Out Of Memory)]] [[ELF (Editabl Linkable File)]]
