[[MMAP]] [[Database]] [[WAL (Write-Ahead Log)]]

# WiredTiger storage engine

> Default MongoDB storage engine since 3.2—document-level concurrency, compression, and checkpoint-based durability with a journal for crash recovery.

## Features

- **Document-level locking** (not collection-wide)
- **Snappy/zlib/zstd compression** of cache pages
- **Checkpoint + journal** — similar mental model to [[write-ahead logging]]
- Uses [[MMAP]]-style cache integration with the OS page cache

## Contrast with MongoDB MMAPv1 (legacy)

WiredTiger replaced MMAPv1 for better write concurrency and compression.

## Sources

- MongoDB Documentation — [WiredTiger Storage Engine](https://www.mongodb.com/docs/manual/core/wiredtiger/)
- MongoDB Documentation — [Journaling](https://www.mongodb.com/docs/manual/core/journaling/)
