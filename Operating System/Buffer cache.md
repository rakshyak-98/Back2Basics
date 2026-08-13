[[Operating System]] [[buffer]] [[buffer head]] [[fsync]] [[file descriptors]] [[Persistent Block Storage]]

# Buffer cache

> On Linux, the buffer cache is not a separate cache anymore — file and block data live in the unified page cache, with buffer heads describing how pages map to disk blocks.

Historically the kernel kept two caches: **page cache** for file contents and **buffer cache** for block-device I/O. Since Linux 2.4 they merged: all file-backed and block-backed paths share the **page cache** ([[kernel subsystem]] memory management). People still say “buffer cache” when discussing dirty blocks, writeback, and `sync` behavior.

## Read path

```txt
read() → lookup inode page in page cache → hit: copy to user
                                        → miss: read disk, populate cache, then copy
```

Readahead prefetches sequential pages. Memory is dynamic — unused cache pages are reclaimed under pressure before OOM.

## Write path and durability

Writes mark pages **dirty** in RAM and return quickly. Flushing to [[Persistent Block Storage]] happens via:

- Background **writeback** (`pdflush` / `bdi` threads)
- Explicit `sync()`, `fsync()` ([[fsync]]), `msync()`

Power loss before flush means data existed only in cache — databases depend on fsync semantics.

## Buffer heads

A [[buffer head]] (`struct buffer_head`) ties a logical disk block to a page cache page for block-layer I/O. Higher-level file I/O usually goes through `address_space` and folios; buffer heads remain relevant for some block and filesystem paths.

## Inspection

```bash
free -h              # "buff/cache" line
grep -E 'Dirty|Writeback' /proc/meminfo
echo 3 | sudo tee /proc/sys/vm/drop_caches   # lab only — drops clean cache
```

## Sources

- Linux kernel documentation: [Page Cache](https://docs.kernel.org/mm/page_cache.html)
- Robert Love, *Linux Kernel Development* — Chapter on page cache and writeback
- Thomas-Krenn Wiki — Linux Page Cache Basics
