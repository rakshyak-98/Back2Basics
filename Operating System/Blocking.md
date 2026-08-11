[[Operating System]] [[Blocking Vs Non-Blocking]] [[non-blocking]] [[Epoll]] [[context switching]] [[system call]]

# Blocking

> Blocking means a call waits until the kernel finishes the work — your thread sleeps instead of returning early.

---

## Mental model

**Say it in one breath:** A blocking syscall parks the thread until data, space, or a lock is ready; non-blocking returns immediately with `EAGAIN` if not.

```txt
Blocking:     thread ── read() ── sleep ──────────────► wake ──► data
Non-blocking: thread ── read() ── EAGAIN ──► do other work ──► epoll wait
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Blocking I/O** | Syscall waits for readiness | “Thread is off-CPU until the disk/network answers.” |
| **Non-blocking I/O** | Syscall returns now | “Must retry or wait on epoll/poll/select.” |
| **Blocking API** | App waits for completion (maybe on a pool) | “JS async still ‘blocks’ the request logically.” |
| **Sync on main thread** | Event loop stuck in one call | “Never `fs.readFileSync` in a hot Node path.” |
| **Thread pool** | Extra threads for blocking work | “libuv / DB pools hide blocking from the loop.” |
| **Head-of-line** | One slow block stalls others on that thread | “One thread-per-connection limits blast radius.” |

### Decision sketch

| Situation | Prefer |
|-----------|--------|
| Simple CLI / low concurrency | Blocking I/O — easy code |
| Many idle connections | Non-blocking + [[Epoll]] / reactor |
| Node main thread | Async APIs; no long sync syscalls |
| CPU-heavy work | Separate threads/processes — not “non-blocking I/O” alone |

Canonical deep compare: [[Blocking Vs Non-Blocking]] · practical flags: [[non-blocking]].

---

## Standard config / commands

```bash
# Is this fd non-blocking?
python3 - <<'PY'
import fcntl, os, sys
fd = int(sys.argv[1])
flags = fcntl.fcntl(fd, fcntl.F_GETFL)
print('O_NONBLOCK' if flags & os.O_NONBLOCK else 'blocking')
PY

# See blocking syscalls live
strace -p <pid>                 # read/futex/poll hangs
perf top

# Socket / file flags
# fcntl(fd, F_SETFL, O_NONBLOCK)
```

```c
// Blocking read — returns when ≥1 byte or error/EOF
ssize_t n = read(fd, buf, sizeof buf);

// Non-blocking — may return -1/EAGAIN
fcntl(fd, F_SETFL, O_NONBLOCK);
```

| Knob | Why it matters |
|------|----------------|
| `O_NONBLOCK` | Per-fd; inherited quirks across `dup` carefully |
| Timeouts (`SO_RCVTIMEO`, `select` timeout) | Bound blocking waits |
| Pool size | Too small → queue latency; too big → overload |
| `epoll` edge vs level | Wakeup discipline for non-blocking sockets |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Service throughput collapses | One thread stuck in `read`/`write` | Timeouts; non-blocking; more workers |
| Event loop lag (Node) | Sync fs/crypto/JSON on main | Move to async / worker |
| `accept` stall | Single-threaded accept + slow handler | Separate accept loop; non-blocking + epoll |
| Mysterious `D` state | Blocking on disk/NFS | Fix storage; don’t expect signals to help |
| Spiky latency | Lock blocking + I/O blocking | Profile futex + I/O; shrink critical sections |
| `EAGAIN` busy-loop | Non-blocking without wait | Use epoll/poll — never spin |

---

## Gotchas

> [!WARNING]
> **Non-blocking is not free speed** — wrong use causes busy-poll CPU or missed wakeups.

> [!WARNING]
> **Buffered stdio can still block** — `fwrite` eventually syscalls; large flush can stall.

> [!WARNING]
> **DNS / libc helpers may block** — `getaddrinfo` surprises async apps; use async resolvers.

> [!WARNING]
> **Go/Java “blocking” looks cheap** — still consumes OS threads under the hood when all block on I/O.

---

## When NOT to use

- **Don’t force non-blocking for a batch job of ten files** — blocking keeps the code honest and short.
- **Don’t block the UI / event-loop thread on network** — users feel freezes; use async or a worker.
- **Don’t assume “async keyword” removed kernel blocking** — check what the runtime actually does on the wire.

---

## Related

[[Blocking Vs Non-Blocking]] [[non-blocking]] [[Epoll]] [[system call]] [[file descriptors]] [[Thread]] [[thread pool]] [[context switching]] [[CPU IO Bound Task]] [[Inter Process Communication]]
