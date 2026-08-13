[[Operating System]] [[Buffer cache]] [[file descriptors]] [[system call]] [[Persistent Block Storage]]

# fsync

> fsync is the system call that pushes one file’s dirty cache data toward stable storage — the durability boundary databases rely on after a commit record is written.

`write()` success means data reached the [[Buffer cache]], not necessarily the NVMe platter or SSD flash. **`fsync(fd)`** (or `fdatasync` for data-only) schedules writeback for that file’s pages and waits for completion (modulo drive write cache policies).

## Related calls

| Call | Scope |
|------|--------|
| `fsync(fd)` | One file — data + needed metadata |
| `fdatasync(fd)` | Data only where possible |
| `sync()` | Global flush — heavy |

## Failure modes

- Drive **write cache** without capacitor — `fsync` returns success but data lost on power loss unless cache is disabled or battery-backed.
- Network filesystems — durability is only as strong as server guarantees.
- Containers — host crash still matters; [[Persistent Block Storage]] semantics pass through.

```bash
strace -e fsync -p PID
```

Pair with [[system call]] tracing and [[disk IOPS]] tuning for sync-heavy workloads.

## Sources

- Linux `fsync(2)` manual page
- PostgreSQL wiki — fsync and write reliability
- Wikipedia: [fsync](https://en.wikipedia.org/wiki/Syncing)
