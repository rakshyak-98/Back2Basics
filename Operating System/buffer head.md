[[Operating System]] [[Buffer cache]] [[buffer flags]] [[buffer lifecycle]] [[Persistent Block Storage]] [[file descriptors]] [[fsync]]

# Buffer head

> A buffer head is the kernel’s descriptor linking one logical disk block to a page in the page cache — the legacy bridge between the block layer and memory management.

```txt
        Buffer head ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Kernel reviews: after page-cache merge, buffer heads index slices of cache…

## Sources
- [Linux kernel docs — Buffer Head API](https://docs.kernel.org/core-api/buffer.html) — deep-dive
- Robert Love, *Linux Kernel Development* — buffer heads and page cache — deep-dive
- [Wikipedia — Buffer cache](https://en.wikipedia.org/wiki/Buffer_cache) — overview

## Key Concepts
- **Descriptor fields:** page, block number, device, state ([[buffer flags]]).
- **Sector-oriented I/O:** fixed blocks vs whole-file pages.
- **Not a second cache:** indexes a slice of a [[Buffer cache]] page.
- **Concurrency:** buffer-head and page locks prevent races during writeback.

## Technical Details
- `struct buffer_head` (and folio-era helpers) answers: which page, which block…

```txt
allocate bh → map to page → read I/O fills → mark uptodate
           → modify → set dirty ([[buffer flags]])
           → writeback → clear dirty → unlock
```

- Multiple buffer heads can reference different blocks within the same page.
- Ordering with journals and [[fsync]] prevents filesystem corruption.

- Normal apps use paths and [[file descriptors]], not buffer heads

## Mistakes to Avoid
- **Mistake:** Thinking buffer heads store a duplicate of page-cache data
- **Mistake:** Ignoring lock ordering between page lock and buffer-head lock
- **Mistake:** Debugging user apps by hunting buffer heads instead of fsync/I/O…

## Pros/Cons or Trade-offs
- **Pro:** Precise per-block state for the block layer.
- **Con:** Legacy complexity; modern code prefers folio/`address_space` paths where possible.
- **Trade-off:** keep buffer-head APIs for compatibility vs rewrite on newer abstractions.

## Comparison
- vs [[Buffer cache]]: cache holds pages; buffer head describes a block within/linked to them.
- vs [[buffer]]: generic user/kernel byte region vs kernel block descriptor.


### Use cases
- Filesystem implementers, crash dump analysis of stuck writeback, and teaching…
