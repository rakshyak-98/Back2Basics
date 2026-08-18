[[Operating System]] [[system call]] [[file descriptors]] [[Buffer cache]]

# OS program

> User programs run in user space — they ask the kernel (via syscalls) for files, memory, and devices.

## Mental model

**Say it in one breath:** application code + libc live in user mode; privileged work happens only after a syscall traps into kernel mode.

```txt
printf("hi\n")
   → libc buffers in user space
   → write(1, …) syscall
   → kernel → tty/driver → screen
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **User space** | Unprivileged app memory | “Can’t touch devices directly.” |
| --- | --- | --- |
| **Kernel space** | Trusted OS code | “Drivers and syscall handlers live here.” |
| **Syscall** | Controlled entry | “Trap, handle, return.” |
| **libc** | C library wrappers | “`printf` may buffer before `write`.” |
| **fd** | Handle to a kernel object | “`1` is stdout.” |
| **Context switch** | Mode/process change | “Syscall isn’t always a full process switch.” |

### How the story goes

1. **Run** — loader maps binary; CPU in user mode.
2. **Need service** — open/read/write/mmap/clone…
3. **Trap** — kernel validates, does work (maybe sleep).
4. **Return** — value or `errno`; application continues.

## Standard config / commands

```bash
# See a program’s kernel interactions
strace -f -o /tmp/t ./app
lsof -p <pid>
cat /proc/<pid>/maps
# stdout is fd 1 — prove it
ls -l /proc/self/fd
```

| Knob | Why it matters |

| `strace` | Map user calls → syscalls |
| --- | --- |
| `/proc/pid/fd` | Live descriptor table |
| ulimit / cgroup | Caps on what the program may consume |
| seccomp | Which syscalls are allowed |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| No console output | libc buffer not flushed | newline, `fflush`, or `write` |
| Hang in “program” | `strace` shows blocking syscall | Fix peer/fd/timeout |
| Permission denied | uid/caps/LSM | Fix creds or path |
| Works as root only | Capability needed | Drop root; add specific cap |
| Crash only under load | Stack/heap / fd exhaustion | Limits + leak fix |
| Container differs | seccomp / mounts | Adjust profile / volumes |

## Gotchas

> [!WARNING]
> **Buffered stdio lies** — crash before flush loses the last prints; use line buffering or `write`.

> [!WARNING]
> **“Kernel space” isn’t a place apps mmap for fun** — only via defined interfaces (`/dev`, syscalls).

> [!WARNING]
> **Threads share fd table** — one close surprises another thread ([[multi-threaded]]).

> [!WARNING]
> **Signal + syscall** — `EINTR` retries needed on some paths.

## When NOT to use

- **In-kernel modules for application logic** — keep policy in user space; smaller blast radius.
- **Busy-spin on devices from userland** — use proper drivers / `poll`/`epoll`.
- **Bypassing the kernel with `/dev/mem` in production** — last resort, not a product architecture.

## Related

[[system call]] [[file descriptors]] [[discriptors]] [[Buffer cache]] [[fsync]] [[TTY (teletypewriter)]]
