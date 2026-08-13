[[Operating System]] [[Buffer cache]] [[buffer flags]] [[buffer lifecycle]] [[Persistent Block Storage]]

# Buffer head

> A buffer head is the kernel’s descriptor linking one logical disk block to a page in the page cache — the legacy bridge between the block layer and memory management.

`struct buffer_head` (and modern helpers built on folios) answers: **which page**, **which block number**, **which device**, and **what state** (dirty, uptodate, locked). File systems and the block layer use buffer heads when I/O is expressed in fixed **sectors** rather than whole file pages.

## Role after the page-cache merge

Since the buffer cache merged into the [[Buffer cache]] (page cache), buffer heads do not represent a second copy of data — they **index** a slice of a cached page. Multiple buffer heads can reference different blocks within the same page.

## State machine (conceptual)

```txt
allocate bh → map to page → read I/O fills → mark uptodate
           → modify → set dirty ([[buffer flags]])
           → writeback → clear dirty → unlock
```

Concurrent access relies on locking buffer heads and page locks; races here cause filesystem corruption — why `fsync` and journal ordering matter ([[fsync]]).

## User-space visibility

Normal applications use paths and [[file descriptors]], not buffer heads. They matter when reading **kernel** or **filesystem** source, analyzing `block` layer traces, or debugging tunefs/block-size mismatches on [[Persistent Block Storage]].

## Sources

- Linux kernel documentation: [Buffer Head API](https://docs.kernel.org/core-api/buffer.html)
- Robert Love, *Linux Kernel Development* — buffer heads and page cache
- Wikipedia: [Buffer cache](https://en.wikipedia.org/wiki/Buffer_cache)
