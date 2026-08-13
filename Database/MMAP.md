[[Database]] [[WiredTiger storage engine]] [[MySQL storage]]

# MMAP

> Memory-mapped I/O maps file pages into the process address space so the OS page cache serves database reads and writes—used by MongoDB WiredTiger, LMDB, and some SQLite configurations.

## How it works

```txt
read() syscall path:  app buffer ◄── kernel ◄── disk
mmap path:            app accesses virtual address ──► page fault ──► OS loads page
```

The database engine treats file offsets as memory; the kernel handles caching and eviction.

## Tradeoffs

| Benefit | Cost |
|---------|------|
| Simpler buffer management | Less explicit control over fsync timing |
| Fast random access on warm cache | `MAP_SHARED` crash consistency requires careful WAL design |
| Shared pages across processes | TLB pressure on huge mappings |

Relational engines (PostgreSQL, InnoDB) typically use explicit buffer pools plus [[WAL (Write-Ahead Log)]] rather than relying solely on mmap for durability.

## Sources

- POSIX `mmap(2)` manual page
- Kleppmann, *DDIA*, Ch. 3
- Wikipedia — [Memory-mapped file](https://en.wikipedia.org/wiki/Memory-mapped_file)
