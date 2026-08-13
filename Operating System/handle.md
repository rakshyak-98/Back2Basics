[[Operating System]] [[file descriptors]] [[system call]] [[discriptors]]

# handle

> A handle is an opaque OS ID for an open resource — you pass it to syscalls; you never poke the kernel object directly.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Your process holds a token; the kernel maps that token to the real file, socket, or process object.

```txt
App                         Kernel
 handle / fd  ──────────►  object (file, socket, mutex, …)
   (number / pointer-sized cookie)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Handle** | Opaque resource reference | “I only use the API; the kernel owns the object.” |
| **File descriptor** | Unix integer handle | “On Linux, handles for I/O are fds — see [[file descriptors]].” |
| **Windows `HANDLE`** | Pointer-sized opaque value | “Same pattern, different type and APIs.” |
| **Dup / inherit** | Copy or pass the reference | “Child can receive the same open file description.” |
| **Close** | Drop the reference | “Last close may release the object.” |
| **Leak** | Forgot to close | “EMFILE / handle exhaustion under load.” |

> [!INFO]
> On Unix/Linux the everyday name is **file descriptor**. “Handle” is the portable idea (and the Windows term). Databases talk about “connection handles” the same way.

### How the story goes (4 steps)

1. **Open / create** — syscall returns a handle (`open`, `socket`, `CreateFile`).
2. **Operate** — `read`/`write`/`ioctl` with that ID.
3. **Duplicate / share** — `dup`, inherit-on-execute, or pass over SCM_RIGHTS.
4. **Close** — release; resources free when the last reference dies.

---

## Standard config / commands

```bash
# Unix: handles are fds
ls -l /proc/self/fd
lsof -p <pid>
ulimit -n

# See what a process holds
ls /proc/<pid>/fd
```

```c
int fd = open("file.txt", O_RDONLY);
// fd is the handle
close(fd);
```

| Knob | Why it matters |
|------|----------------|
| `RLIMIT_NOFILE` | Max handles per process |
| `O_CLOEXEC` | Don’t leak fds across `exec` |
| Inheritance flags | Surprising open sockets in children |
| Language finalizers | Non-deterministic close → exhaustion |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Too many open files` | `lsof -p`; `ulimit -n` | Close paths; raise limit; fix leaks |
| Child holds parent’s socket | Missing `CLOEXEC` | Set close-on-exec |
| Double-close crash | Use-after-close | Null out; ownership discipline |
| Windows `INVALID_HANDLE_VALUE` | Failed open | Check `GetLastError` — don’t use the handle |
| GC’d language “random” EMFILE | Finalizer delay | Explicit `close`/`using` |

---

## Gotchas

> [!WARNING]
> **Handle ≠ pointer to kernel memory.** Casting and dereferencing is undefined; only the OS API is legal.

> [!WARNING]
> **Two fds can alias one open file** (`dup`) — shared offset surprises.

> [!WARNING]
> **Closing stdin/stdout** and opening something else can reuse fd 0/1 — logs vanish into a socket.

> [!WARNING]
> **Windows vs Unix naming** — don’t assume a numeric fd API on Win32; use the right HANDLE calls.

---

## When NOT to use

- **Pure in-process objects** — ordinary pointers/references; no OS handle needed.
- **Cross-machine resources** — use network IDs / session tokens, not OS handles.
- **As a security boundary alone** — possession of a handle is power; combine with UID/capability checks.

---

## Related

[[file descriptors]] [[discriptors]] [[system call]] [[Epoll]] [[lsof]] [[non-blocking]]
