[[Operating System]] [[Buffer cache]] [[buffer flags]] [[buffer lifecycle]] [[Persistent Block Storage]] [[file descriptors]] [[fsync]]

# Buffer head

> A buffer head is the kernel’s descriptor linking one logical disk block to a page in the page cache — the legacy bridge between the block layer and memory management.





## Interview Relevance
Kernel interviews: after page-cache merge, buffer heads index slices of cached pages — they are not a second copy of the data.

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
`struct buffer_head` (and folio-era helpers) answers: which page, which block, which device, what state.

```txt
allocate bh → map to page → read I/O fills → mark uptodate
           → modify → set dirty ([[buffer flags]])
           → writeback → clear dirty → unlock
```

Multiple buffer heads can reference different blocks within the same page. Ordering with journals and [[fsync]] prevents filesystem corruption.

Normal apps use paths and [[file descriptors]], not buffer heads — relevant when reading kernel/fs source or debugging block-size issues on [[Persistent Block Storage]].

## Real-World Applications
Filesystem implementers, crash dump analysis of stuck writeback, and teaching the block↔page bridge.

## Pros/Cons or Trade-offs
- **Pro:** Precise per-block state for the block layer.
- **Con:** Legacy complexity; modern code prefers folio/`address_space` paths where possible.
- **Trade-off:** keep buffer-head APIs for compatibility vs rewrite on newer abstractions.

## Comparison
- vs [[Buffer cache]]: cache holds pages; buffer head describes a block within/linked to them.
- vs [[buffer]]: generic user/kernel byte region vs kernel block descriptor.

## Mistakes to Avoid
- Thinking buffer heads store a duplicate of page-cache data.
- Ignoring lock ordering between page lock and buffer-head lock.
- Debugging user apps by hunting buffer heads instead of fsync/I/O traces.
