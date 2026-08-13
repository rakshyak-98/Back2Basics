[[Operating System]] [[buffer]] [[Buffer cache]] [[buffer flags]] [[buffer head]] [[fsync]] [[multiple levels of buffering]]

# buffer lifecycle

> Buffer lifecycle is the path a kernel (or app) buffer takes — allocate, fill, use, write back, then reuse or free.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Buffers are rented, not eternal — they move through queues until clean enough to evict or dirty enough to flush.

```txt
allocate → queue → fill (read disk / copy user write)
                → mark dirty (if modified)
                → writeback (pdflush / flusher threads)
                → clean → evict / reuse under memory pressure
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Allocate** | Get a buffer from free memory / pool | “We pay allocation unless we pool.” |
| **Dirty** | Modified vs backing store | “Dirty pages must write back before reclaim.” |
| **Writeback** | Flush dirty data to disk | “Background flushers + explicit `fsync`.” |
| **Clean** | Matches disk (or never written) | “Clean pages can be dropped under pressure.” |
| **Eviction** | Remove from cache to free RAM | “Hot working set should stay resident.” |
| **Pool / freelist** | Reuse buffers | “Avoid allocate/free per packet.” |

### How the story goes (classic kernel sketch)

1. **Allocation** — buffer taken from free memory when a read/write needs caching.
2. **Queuing / filling** — tied to a block; filled from disk (read) or from user data (write).
3. **Use** — serves further reads; marked dirty on writes.
4. **Writeback** — dirty buffers flushed by flusher threads or [[fsync]].
5. **Eviction** — clean buffers reclaimed when RAM is tight — see [[RAM and Swap memory]].

application-level pools follow the same story: acquire → fill → consume → release to pool.

---

## Standard config / commands

```bash
# Dirty page pressure
cat /proc/meminfo | egrep 'Dirty|Writeback|Buffers|Cached'
sysctl vm.dirty_ratio vm.dirty_background_ratio vm.dirty_expire_centisecs

# Who is flushing
ps aux | grep -E 'kworker|flush'

# Force a sync point (blunt instrument)
sync
# App should prefer fsync on specific fds — [[fsync]]
```

```c
// App pool sketch
buf = pool_acquire();
fill(buf);
use(buf);
pool_release(buf);   // back to freelist — not free() every time
```

| Knob | Why it matters |
|------|----------------|
| `vm.dirty_*` | When background writeback starts vs when writers stall |
| Pool size | Too small → alloc churn; too big → RAM waste |
| `O_SYNC` / `fsync` | Sync lifecycle to durability requirements |
| Buffer flags | State bits (dirty/locked/uptodate) — see [[buffer flags]] |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Write latency spikes | Dirty ratio hit; disk saturated | Tune dirty_* ; faster disk; batch commits |
| Data missing after crash | Lifecycle stopped at page cache | [[fsync]] / barriers on commit |
| Memory grows without bound | Buffers never released / leak | Return to pool; bound cache |
| Read amplification | Tiny buffers / cold cache | Larger I/O size; warm wisely |
| Stale reads after write | Missing flush between writers/readers on raw devices | Correct flags + sync protocol |

---

## Gotchas

> [!WARNING]
> **Lifecycle ≠ durability.** A buffer can be “complete” in RAM and still vanish on power loss without [[fsync]].

> [!WARNING]
> **Double free / use-after-release** in custom pools is as bad as heap corruption — poison on release in debug builds.

> [!WARNING]
> **Writeback storms** after quiet periods — many dirty pages flush at once; watch `Dirty` in `/proc/meminfo`.

> [!WARNING]
> **Blocking in allocate under pressure** — GFP flags / reclaim can stall your hot path; size pools ahead of traffic.

---

## When NOT to use

- **One-shot tiny CLI** — malloc/free once; a pool is noise.
- **When page cache already does the job** — don’t duplicate a second userspace cache without a reason.
- **Cross-process sharing without a plan** — use [[shared memory]] + clear ownership, not ad-hoc buffer pointers.

---

## Related

[[buffer]] [[Buffer cache]] [[buffer flags]] [[buffer head]] [[fsync]] [[multiple levels of buffering]] [[RAM and Swap memory]] [[disk IOPS]]
