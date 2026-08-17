[[Database]] [[WiredTiger storage engine]] [[MySQL storage]] [[WAL (Write-Ahead Log)]]

# MMAP

> Memory-mapped I/O maps file pages into the process address space so the OS page cache serves database reads and writes—used by MongoDB WiredTiger, LMDB, and some SQLite configurations.





## Interview Relevance
mmap questions separate OS page-cache designs from explicit buffer-pool engines (PostgreSQL, InnoDB). Interviewers want tradeoffs: simpler caching vs less control over fsync and TLB pressure.

## Sources
- POSIX `mmap(2)` manual page — deep-dive
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 3 — overview
- [Wikipedia — Memory-mapped file](https://en.wikipedia.org/wiki/Memory-mapped_file) — overview

## Key Concepts
- **Map file → address space:** access virtual addresses; page faults load from disk via the OS.
- **OS page cache as buffer pool:** kernel handles caching and eviction.
- **Durability still needs discipline:** `MAP_SHARED` crash consistency requires careful WAL/fsync design.
- **Not universal:** relational engines often prefer explicit buffer pools + [[WAL (Write-Ahead Log)]].

## Technical Details
```txt
read() syscall path:  app buffer ◄── kernel ◄── disk
mmap path:            app accesses virtual address ──► page fault ──► OS loads page
```

The database engine treats file offsets as memory; the kernel handles caching and eviction.

| Benefit | Cost |
|---------|------|
| Simpler buffer management | Less explicit control over fsync timing |
| Fast random access on warm cache | `MAP_SHARED` crash consistency requires careful WAL design |
| Shared pages across processes | TLB pressure on huge mappings |

Relational engines (PostgreSQL, InnoDB) typically use explicit buffer pools plus [[WAL (Write-Ahead Log)]] rather than relying solely on mmap for durability. [[WiredTiger storage engine]] and LMDB illustrate mmap-oriented designs in other ecosystems.

## Real-World Applications
Embedded stores (LMDB, some SQLite modes) and engines that lean on the OS cache. Example: diagnosing “why is RSS huge?” on an mmap-backed store—much of the footprint is file-backed page cache, not necessarily a leak.

## Pros/Cons or Trade-offs
- **Pro:** Less custom cache code; warm random reads can be very fast.
- **Con:** Harder to control writeback/fsync; large mappings stress TLB; durability bugs are subtle.

## Comparison
vs explicit buffer pool (InnoDB/PostgreSQL): buffer pools give precise eviction and checkpoint control; mmap leans on the kernel. vs plain `read()`/`write()`: mmap avoids copying into user buffers but couples correctness to mapping flags and sync behavior.

## Mistakes to Avoid
- Assuming mmap alone equals durability — without WAL/fsync discipline, crashes corrupt data.
- Blaming “memory leaks” when RSS includes mapped file pages.
- Expecting PostgreSQL/InnoDB to behave like LMDB’s mmap model.
