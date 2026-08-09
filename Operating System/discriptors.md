[[Operating System]] [[handle]] [[file descriptors]] [[system call]] [[Epoll]] [[fsync]]

# descriptors

> File descriptors (fds) are small integers your Unix process uses as handles for open files, sockets, and pipes — 0/1/2 are stdin/stdout/stderr.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `open`/`socket` returns an int; that int indexes your process fd table, which points at a kernel open-file object.

```txt
fd table (per process)          kernel
┌────┐
│ 0  │ → stdin  ──► struct file ──► inode / tty
│ 1  │ → stdout
│ 2  │ → stderr
│ 3  │ → listen socket
│ 4  │ → /var/log/app.log
└────┘
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **fd** | Integer I/O handle | “Everything is a file — sockets included.” |
| **0 / 1 / 2** | stdin / stdout / stderr | “Redirects just remappoint these slots.” |
| **Open file description** | Kernel object with offset/flags | “`dup` shares it; two fds, one offset.” |
| **EMFILE / ENFILE** | Per-process / system fd limit hit | “Classic leak symptom under load.” |
| **CLOEXEC** | Close across `exec` | “Prevent leaking sockets into children.” |
| **epoll/kqueue** | Wait on many fds | “Scalable readiness — see [[Epoll]].” |

> [!INFO]
> Filename `discriptors.md` is historical spelling; the concept is **file descriptors**. Prefer linking [[file descriptors]] / [[handle]] from other notes.

### How the story goes (4 steps)

1. **Create** — `open`, `socket`, `pipe`, `accept` → new fd number.
2. **Use** — `read` / `write` / `mmap` / `fcntl`.
3. **Watch** — `select` / `poll` / [[Epoll]] for readiness.
4. **Close** — `close(fd)`; last reference frees the kernel object.

---

## Standard config / commands

```bash
ls -l /proc/<pid>/fd
lsof -p <pid>
ss -tlnp                    # sockets ↔ pid/fd
ulimit -n                   # soft limit
cat /proc/<pid>/limits | grep 'open files'

# Raise soft limit (session)
ulimit -n 65535
```

```c
int fd = open("data.bin", O_RDONLY | O_CLOEXEC);
ssize_t n = read(fd, buf, sizeof buf);
close(fd);
```

| Knob | Why it matters |
|------|----------------|
| Soft vs hard `nofile` | Soft is what you hit; hard needs root/capabilities |
| systemd `LimitNOFILE=` | Service limit ≠ your shell ulimit |
| `O_NONBLOCK` | Non-blocking I/O on that fd |
| `dup2(fd, 1)` | Remap stdout — logging/redirect pattern |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Too many open files` | `lsof -p`; leak in accept loop | Close paths; pool caps; raise limit |
| Writes disappear | fd 1 remapped or closed | Audit `dup2` / daemonizing |
| Child inherits listen socket | No `CLOEXEC` | Set `FD_CLOEXEC` |
| `EBADF` | Use after close / wrong fd | Ownership; don’t share casually |
| High CPU in poll | Busy loop on never-blocking fd | Level vs edge trigger; fix events |

---

## Gotchas

> [!WARNING]
> **fd number reuse** — after `close(3)`, the next `open` may return 3 pointing at something else. Stale ints are dangerous.

> [!WARNING]
> **`fork` duplicates the table** — both share open file descriptions until close; offsets move for both.

> [!WARNING]
> **Language runtimes hide fds** (files, timers, watchers). EMFILE often comes from leaked sockets, not your explicit `open`.

> [!WARNING]
> **Citations / wiki dumps don’t debug prod** — use `/proc` and `lsof`, not glossary sites.

---

## When NOT to use

- **Windows-only code** — use `HANDLE` APIs; fds are a CRT compatibility layer with sharp edges.
- **As a substitute for paths** — fds refer to *open* objects; a path can be replaced underneath (`O_PATH` aside).
- **Cross-node identity** — an fd is local to one kernel; pass capabilities intentionally (SCM_RIGHTS), don’t invent magic numbers.

---

## Related

[[file descriptors]] [[handle]] [[system call]] [[Epoll]] [[lsof]] [[Buffer cache]] [[non-blocking]] [[fsync]]
