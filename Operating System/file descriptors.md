[[Operating System]] [[discriptors]] [[handle]] [[system call]] [[fsync]] [[Epoll]]

# File descriptors

> A file descriptor is a small non-negative integer the kernel gives your process to name an open file, socket, pipe, or device — every read, write, and mmap goes through it.

Returned by `open()`, `socket()`, `pipe()`, `epoll_create1()`, etc. The integer indexes the process **file descriptor table**; `dup2()` can remap stdin/stdout/stderr (0, 1, 2).

## Lifetime and sharing

- **`fork()`** — table copied; refcounts shared until close.
- **`exec()`** — descriptors marked close-on-exec (`FD_CLOEXEC`) close automatically.
- **Leaks** — forgotten sockets → `EMFILE`; use `lsof -p PID`.

## Flags that change behavior

| Flag | Effect |
|------|--------|
| `O_NONBLOCK` | [[non-blocking]] readiness ([[Epoll]]) |
| `O_APPEND` | Writes always at end |
| `O_DIRECT` | Bypass [[Buffer cache]] (alignment rules) |

Durability syscalls operate on fds: [[fsync]] on a file fd pushes dirty pages for that file.

## Sources

- Kerrisk, *The Linux Programming Interface*
- Linux `open(2)`, `close(2)` manual pages
- Wikipedia: [File descriptor](https://en.wikipedia.org/wiki/File_descriptor)
