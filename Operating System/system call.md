[[Operating System]] [[fsync]] [[file descriptors]] [[process]] [[Epoll]]

# System call

> A system call is how a user program asks the kernel for work — open files, create processes, send network data.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** User code traps into the kernel with a syscall number; the kernel runs a trusted handler and returns a result or `errno`.

```txt
user space                    kernel space
──────────                    ────────────
read(fd, buf, n)
   │
   ├─ syscall instruction ──► syscall table[NR]
   │                              │
   │                         do_sys_read …
   │                              │
   ◄────── return value / -ERR ───┘
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Syscall** | Controlled entry to the kernel | “Apps can’t touch devices directly; they call the kernel.” |
| **User mode / kernel mode** | CPU privilege rings | “Syscall flips mode; bad pointers are checked.” |
| **Syscall number** | Index into the table | “`openat`, `read`, `write`, `clone` each have an NR.” |
| **glibc wrapper** | C library stub around the trap | “You call `write()`; libc issues the syscall.” |
| **`errno`** | Thread-local error code | “`-1` return + `errno` explains failure.” |
| **`fsync`** | Durability syscall | “Force this file’s dirty data toward stable storage.” |

### How the story goes

1. **application** calls libc (`open`, `read`, `mmap`, `clone`, …).
2. **Trap** — arch-specific syscall instruction + number + arguments in registers.
3. **Kernel** looks up handler, checks credentials/limits, does work.
4. **Return** — success value or negative errno translated by libc.
5. **Heavy paths** — blocking syscalls sleep; non-blocking return `EAGAIN` ([[non-blocking]], [[Epoll]]).

### `fsync` (durability corner)

`write` hitting the [[Buffer cache]] is not enough after power loss. `fsync(fd)` / `fdatasync` push that file’s data (and needed metadata) toward stable storage. Mid-`fsync` power loss can still tear without journaling/COW — see [[fsync]].

### Computed calls (related idea, not a syscall)

Function pointers pick the callee at runtime (C “polymorphism”). The **syscall table** is the kernel’s version of “number → handler,” not something apps fill in.

---

## Standard config / commands

```bash
# Trace syscalls (lab / one process)
strace -p <pid>
strace -c ./app                 # counts / time summary
strace -e trace=file,network,desc -o /tmp/out.txt ./app

# Syscall list / numbers (kernel headers)
ausyscall --dump 2>/dev/null || cat /usr/include/asm/unistd_64.h | head

# Failure mode from the app side
# return -1 → perror / strerror(errno)

# Durability
# fsync(fd); fdatasync(fd); sync();  — see [[fsync]]
```

| Knob | Why it matters |
|------|----------------|
| `strace -c` | Find syscall-heavy hotspots (chatty `read`/`futex`) |
| `seccomp` | Filter allowed syscalls (containers) |
| `O_NONBLOCK` / `epoll` | Avoid blocking forever on one fd |
| `fsync` vs `fdatasync` | Metadata cost vs data-only durability |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Hang “doing nothing” | `strace -p` — stuck in `read`/`futex`/`poll` | Unblock peer; fix lock; use timeouts |
| `EAGAIN` / `EWOULDBLOCK` storm | Non-blocking fd without epoll | Wire [[Epoll]] / reactor correctly |
| `EMFILE` / `ENFILE` | fd limits | Close leaks; raise `NOFILE` ([[file descriptors]]) |
| Slow commits / p99 | `strace -e fsync -T` | Disk path; batch WAL; see [[fsync]] |
| `EPERM` / `EACCES` | Creds, capabilities, LSMs | Fix user, caps, SELinux/AppArmor |
| Works on bare metal, fails in container | seccomp / missing syscall | Adjust profile or avoid banned call |

---

## Gotchas

> [!WARNING]
> **libc ≠ kernel** — buffered `fwrite` may not syscall until flush; durability still needs `fflush` + `fsync`.

> [!WARNING]
> **`strace` slows and perturbs** — fine for debug; not a always-on profiler in prod (prefer eBPF).

> [!WARNING]
> **Not every failure is a syscall error** — logic bugs return success with wrong data; don’t only watch `errno`.

> [!WARNING]
> **Signal interruption** — some syscalls return `EINTR`; correct code retries or uses `SA_RESTART`.

---

## When NOT to use

- **Don’t raw-syscall from application code without need** — use libc/OS APIs; numbers differ by arch.
- **Don’t `sync()` in a hot request path** — global flush; use targeted [[fsync]] / group commit.
- **Don’t block the only event-loop thread on long syscalls** — offload or go non-blocking ([[Blocking]], [[Blocking Vs Non-Blocking]]).

---

## Related

[[fsync]] [[file descriptors]] [[Buffer cache]] [[process]] [[Linux Process Theory]] [[Epoll]] [[non-blocking]] [[Blocking]] [[Blocking Vs Non-Blocking]] [[eBPF]] [[handle]]
