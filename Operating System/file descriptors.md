[[Operating System]] [[discriptors]] [[handle]] [[system call]] [[fsync]] [[Epoll]] [[non-blocking]] [[Buffer cache]]

# File descriptors

> A file descriptor is a small non-negative integer naming an open file, socket, pipe, or device — every read, write, and mmap goes through it.





## Interview Relevance
Walk fd table lifetime across `fork`/`exec`, `EMFILE` leaks, `O_NONBLOCK`, and why [[fsync]] takes an fd.

## Sources
- Kerrisk, *The Linux Programming Interface* — deep-dive
- Linux `open(2)`, `close(2)` manual pages — deep-dive
- [Wikipedia — File descriptor](https://en.wikipedia.org/wiki/File_descriptor) — overview

## Key Concepts
- **Per-process table:** integer indexes kernel open-file description.
- **0/1/2:** stdin/stdout/stderr by convention.
- **Sharing:** `dup`/`fork` share underlying offset/flags via refcount.
- **Close-on-exec:** `FD_CLOEXEC` for safe `exec`.

## Technical Details
Returned by `open()`, `socket()`, `pipe()`, `epoll_create1()`, etc. `dup2()` remaps stdio fds.

| Flag | Effect |
|------|--------|
| `O_NONBLOCK` | [[non-blocking]] readiness ([[Epoll]]) |
| `O_APPEND` | Writes always at end |
| `O_DIRECT` | Bypass [[Buffer cache]] (alignment rules) |

```bash
lsof -p PID
```

Alias spelling note: [[discriptors]]. Windows analog: [[handle]].

## Real-World Applications
Servers, shells redirecting stdio, and epoll-based proxies watching thousands of fds.

## Pros/Cons or Trade-offs
- **Pro:** Uniform I/O ABI across files/sockets/devices.
- **Con:** Process-wide limits; leak-prone.
- **Trade-off:** `O_DIRECT` control vs cache benefits.

## Comparison
- vs [[handle]]: same role, different OS token shape.
- vs paths: path is a name; fd is a live capability to an open object.

## Mistakes to Avoid
- Forgetting to close accepted sockets on all error paths.
- Assuming fds survive `exec` without checking cloexec.
- Using `O_DIRECT` without respecting alignment rules.
