[[Operating System]] [[Buffer cache]] [[file descriptors]] [[system call]] [[Persistent Block Storage]] [[disk IOPS]]

# fsync

> fsync pushes one file’s dirty cache data toward stable storage — the durability boundary databases rely on after writing a commit record.

```txt
        fsync ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Durability classic: `write` ≠ durable

## Sources
- Linux `fsync(2)` manual page — deep-dive
- PostgreSQL wiki — fsync and write reliability — deep-dive
- [Wikipedia — fsync](https://en.wikipedia.org/wiki/Sync_(Unix)) — overview

## Key Concepts
- **`write()`:** data reaches [[Buffer cache]], not necessarily media.
- **`fsync(fd)`:** writeback for that file’s data + needed metadata; waits.
- **`fdatasync`:** data-focused where possible.
- **`sync()`:** global flush — heavy.

## Technical Details
| Call | Scope |
|------|--------|
| `fsync(fd)` | One file — data + needed metadata |
| `fdatasync(fd)` | Data only where possible |
| `sync()` | Global flush — heavy |

- Failure modes:

- Drive write cache without capacitor
- Network filesystems — only as strong as server guarantees.
- Containers — host crash still matters

```bash
strace -e fsync -p PID
```

- Pair with [[disk IOPS]] for sync-heavy workloads.

## Mistakes to Avoid
- **Mistake:** Believing `write` return means crash-safe
- **Mistake:** Calling `sync()` in a tight loop on a multi-tenant host
- **Mistake:** Ignoring disk write-cache policy in durability claims

## Pros/Cons or Trade-offs
- **Pro:** Explicit durability for critical files.
- **Con:** Latency and IOPS cliffs under frequent sync.
- **Trade-off:** `fdatasync` speed vs full metadata safety of `fsync`.

## Comparison
- vs [[Buffer cache]]: cache makes writes fast; fsync forces them out.
- vs `fflush`: user-space buffer only — not disk.


### Use cases
- PostgreSQL/MySQL commit paths, write-ahead logs, and editors that “save” safe…
