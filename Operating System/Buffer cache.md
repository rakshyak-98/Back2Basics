[[Operating System]] [[buffer]] [[buffer head]] [[fsync]] [[file descriptors]] [[Persistent Block Storage]] [[kernel subsystem]]

# Buffer cache

> On Linux the old “buffer cache” is not separate anymore — file and block data live in the unified page cache; buffer heads only describe how pages map to disk blocks.

```txt
        Buffer cache ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Expect questions on dirty pages, writeback vs `fsync`, and why a successful `…

## Sources
- [Linux kernel docs — Page Cache](https://docs.kernel.org/mm/page_cache.html) — deep-dive
- Robert Love, *Linux Kernel Development* — page cache and writeback — deep-dive
- Thomas-Krenn Wiki — Linux Page Cache Basics — overview

## Key Concepts
- **Unified page cache:** since Linux 2.4, file-backed and block-backed paths share one cache ([[kernel…
- **Dirty pages:** `write()` updates RAM and returns
- **Buffer head:** [[buffer head]] ties a logical block to a page for some block/filesystem path…
- **Readahead:** sequential reads prefetch pages into cache.

## Technical Details
- Historically: separate **page cache** (files) and **buffer cache** (block I/O…
- Today people still say “buffer cache” when discussing dirty blocks, writeback…

### Read path

```txt
read() → lookup inode page in page cache → hit: copy to user
                                        → miss: read disk, populate cache, then copy
```

- Unused clean pages are reclaimed under memory pressure before OOM.

### Write path and durability

- Writes mark pages **dirty** in RAM and return quickly.
- Flushing to [[Persistent Block Storage]] happens via:

- Background **writeback** (`bdi` / writeback threads)
- Explicit `sync()`, `fsync()` ([[fsync]]), `msync()`

- Power loss before flush means data existed only in cache

```bash
free -h              # "buff/cache" line
grep -E 'Dirty|Writeback' /proc/meminfo
echo 3 | sudo tee /proc/sys/vm/drop_caches   # lab only — drops clean cache
```

## Mistakes to Avoid
- **Mistake:** Equating `write()` success with durable on-disk state
- **Mistake:** Panic when `buff/cache` is large — often reclaimable
- **Mistake:** Using `drop_caches` on production hosts as routine ops

## Pros/Cons or Trade-offs
- **Pro:** Huge read/write amplification reduction; sequential workloads shine.
- **Con:** Crash without fsync loses recent writes.
- **Trade-off:** drop_caches in production hides real working-set behavior and hurts latency.

## Comparison
- vs [[buffer]]: generic byte region vs kernel page cache for block/file data.
- vs [[fsync]]: cache accelerates; fsync forces durability to media.


### Use cases
- PostgreSQL / MySQL rely on `fsync` (or equivalent) so checkpoints survive pow…
