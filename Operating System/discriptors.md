[[Operating System]] [[file descriptors]] [[handle]] [[system call]] [[Epoll]]

# Discriptors

> “Discriptors” in this vault refers to **descriptors** — kernel-managed integer handles (chiefly file descriptors) that stand for open objects: files, sockets, pipes, and epoll instances.

The spelling matches legacy notes; canonical term: **file descriptor** ([[file descriptors]]). On Unix, `open()`, `socket()`, and `accept()` return small integers; the process **descriptor table** maps them to `struct file` entries in the kernel.

## Descriptor table essentials

| Concept | Role |
|---------|------|
| fd number | Index user space passes to [[system call]] |
| `struct file` | Offset, flags, ops for one open instance |
| `dup()` / `fork()` | Share underlying file description |

Limits (`RLIMIT_NOFILE`, `fs.file-max`) cause `EMFILE` when leaked — common in long-running servers.

Windows uses opaque **handles** ([[handle]]) instead of small integers, but the abstraction role is the same.

## Multiplexing

[[Epoll]] (and `poll`, `select`) watches many descriptors for readiness — foundation of non-blocking servers ([[non-blocking]]).

## Sources

- Kerrisk, *The Linux Programming Interface* — file descriptors
- Linux `open(2)`, `fcntl(2)` manual pages
- Wikipedia: [File descriptor](https://en.wikipedia.org/wiki/File_descriptor)
