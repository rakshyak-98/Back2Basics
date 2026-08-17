[[MMAP]] [[Database]] [[WAL (Write-Ahead Log)]] [[write-ahead logging]] [[GridFS]] [[ACID]]

# WiredTiger storage engine

> Default MongoDB storage engine since 3.2 — document-level concurrency, compressed cache pages, and checkpoint-plus-journal durability for crash recovery.





## Interview Relevance
Interviewers contrast WiredTiger with legacy MMAPv1 and with relational buffer-pool+WAL designs. Signal: document-level locks, compression, and journal/checkpoint durability — not collection-wide locks or “mmap equals durability.”

## Sources
- [MongoDB Documentation — WiredTiger Storage Engine](https://www.mongodb.com/docs/manual/core/wiredtiger/) — deep-dive
- [MongoDB Documentation — Journaling](https://www.mongodb.com/docs/manual/core/journaling/) — deep-dive
- [MongoDB Documentation — Storage](https://www.mongodb.com/docs/manual/core/storage/) — overview
- [WiredTiger documentation](https://source.wiredtiger.com/) — overview

## Core Definition
WiredTiger is MongoDB’s modern storage engine: B-tree (and related) structures in a cache with optional compression, document-level concurrency control, periodic checkpoints of data files, and a journal that hardens operations between checkpoints.

## Key Concepts
- **Document-level concurrency:** writers on different documents do not take collection-wide locks.
- **Compression:** Snappy / zlib / zstd on cache pages and on-disk representations — less I/O, more CPU.
- **Checkpoint:** consistent on-disk snapshot of data files.
- **Journal:** between checkpoints, records durable intent — mental cousin of [[write-ahead logging]].
- **Cache vs OS page cache:** WiredTiger manages its own cache; interactions with [[MMAP]]/OS cache differ from MMAPv1’s model.

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

Operational knobs teams discuss: cache size, checkpoint frequency, journal commit interval — trade latency for durability similar in spirit to relational sync-commit settings.

Large files: [[GridFS]] sits above storage engines for blob chunking — not a substitute for WiredTiger itself.

## Real-World Applications
MongoDB clusters storing session documents, product catalogs, and event payloads with secondary indexes; tune cache so the working set fits, and keep journaling on for replica-set durability expectations.

## Pros/Cons or Trade-offs
- **Pro:** High write concurrency, compression, modern default for MongoDB.
- **Con:** Cache sizing and checkpoint behavior need ops attention; different mental model than InnoDB.
- **Trade-off:** Stronger journal/checkpoint sync vs write latency.

## Comparison
vs MMAPv1: WiredTiger won on concurrency and compression — MMAPv1 is historical context only. vs [[MySQL storage]] / InnoDB: both use logging + checkpoints; InnoDB is page/row relational; WiredTiger is document-oriented. vs [[MMAP]]: mmap is a mapping technique; WiredTiger does not make “rely on OS page cache alone” the durability story.

## Mistakes to Avoid
- Assuming MongoDB still behaves like MMAPv1 under load.
- Equating “in cache” with “durable across power loss” without journal/checkpoint policy.
- Undersizing WiredTiger cache so the working set thrash-evicts constantly.
- Treating [[GridFS]] as a storage-engine choice rather than a chunking pattern on top.
