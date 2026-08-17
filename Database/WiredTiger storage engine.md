[[MMAP]] [[Database]] [[WAL (Write-Ahead Log)]] [[write-ahead logging]] [[GridFS]] [[ACID]]

# WiredTiger storage engine

> Default MongoDB storage engine since 3.2 — document-level concurrency, compressed cache pages, and checkpoint-plus-journal durability for crash recovery.

```txt
        WiredTiger storage ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers contrast WiredTiger with legacy MMAPv1 and with relational buffe…

## Sources
- [MongoDB Documentation — WiredTiger Storage Engine](https://www.mongodb.com/docs/manual/core/wiredtiger/) — deep-dive
- [MongoDB Documentation — Journaling](https://www.mongodb.com/docs/manual/core/journaling/) — deep-dive
- [MongoDB Documentation — Storage](https://www.mongodb.com/docs/manual/core/storage/) — overview
- [WiredTiger documentation](https://source.wiredtiger.com/) — overview

## Key Concepts
- **Document-level concurrency:** writers on different documents do not take collection-wide locks.
- **Compression:** Snappy / zlib / zstd on cache pages and on-disk representations
- **Checkpoint:** consistent on-disk snapshot of data files.
- **Journal:** between checkpoints, records durable intent
- **Cache vs OS page cache:** WiredTiger manages its own cache


- **Core:** WiredTiger is MongoDB’s modern storage engine: B-tree (and related) structure…

## Technical Details
```txt
Client write
    │
    ├─► update in WiredTiger cache (document-level latch/lock)
    ├─► journal record (durability between checkpoints)
    └─► periodic checkpoint ──► data files on disk

Crash ──► recover from last checkpoint + replay journal
```

| Feature | WiredTiger | MMAPv1 (legacy) |
|---------|------------|-----------------|
| Lock granularity | Document-level | Collection / coarser |
| Compression | Built-in (Snappy/zlib/zstd) | Limited |
| Durability model | Checkpoint + journal | Memory-mapped files + journaling era-dependent |
| Status | Default since 3.2 | Removed from modern MongoDB |

- Operational knobs teams discuss: cache size, checkpoint frequency, journal co…

- Large files: [[GridFS]] sits above storage engines for blob chunking

## Mistakes to Avoid
- **Mistake:** Assuming MongoDB still behaves like MMAPv1 under load
- **Mistake:** Equating “in cache” with “durable across power loss” without jou…
- **Mistake:** Undersizing WiredTiger cache so the working set thrash-evicts co…
- **Mistake:** Treating [[GridFS]] as a storage-engine choice rather than a chu…

## Pros/Cons or Trade-offs
- **Pro:** High write concurrency, compression, modern default for MongoDB.
- **Con:** Cache sizing and checkpoint behavior need ops attention; different mental model than InnoDB.
- **Trade-off:** Stronger journal/checkpoint sync vs write latency.

## Comparison
- vs MMAPv1: WiredTiger won on concurrency and compression


### Use cases
- MongoDB clusters storing session documents, product catalogs, and event paylo…
