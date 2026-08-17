[[Operating System]] [[file descriptors]] [[handle]] [[system call]] [[Epoll]] [[non-blocking]]

# Discriptors

> “Discriptors” here means **descriptors** — kernel-managed integer handles (chiefly file descriptors) for open files, sockets, pipes, and epoll instances.

```txt
        Discriptors ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Same as [[file descriptors]]: fd table, leaks → `EMFILE`, and multiplexing wi…

## Sources
- Kerrisk, *The Linux Programming Interface* — file descriptors — deep-dive
- Linux `open(2)`, `fcntl(2)` manual pages — deep-dive
- [Wikipedia — File descriptor](https://en.wikipedia.org/wiki/File_descriptor) — overview

## Key Concepts
- **Canonical term:** file descriptor ([[file descriptors]]).
- **fd number:** index passed to [[system call]]s.
- **`struct file`:** offset, flags, ops for one open instance.
- **Windows analog:** opaque [[handle]]s.

## Technical Details
| Concept | Role |
|---------|------|
| fd number | Index user space passes to [[system call]] |
| `struct file` | Offset, flags, ops for one open instance |
| `dup()` / `fork()` | Share underlying file description |

- Limits (`RLIMIT_NOFILE`, `fs.file-max`) cause `EMFILE` when leaked.
- [[Epoll]] watches many descriptors for readiness

## Mistakes to Avoid
- **Mistake:** Editing only this alias and leaving [[file descriptors]] stale
- **Mistake:** Ignoring `FD_CLOEXEC` across `exec`
- **Mistake:** Raising limits forever instead of fixing descriptor leaks

## Pros/Cons or Trade-offs
- **Pro:** Simple integer ABI for I/O objects.
- **Con:** Easy to leak; process-wide limits.
- **Trade-off:** raising `nofile` vs fixing leaks.

## Comparison
- Canonical detail: [[file descriptors]].
- vs [[handle]]: Windows object-manager tokens vs Unix small integers.


### Use cases
- Long-running servers, reverse proxies, and any code that `accept`s without re…
