[[Operating System]] [[kernel subsystem]] [[fsync]] [[buffer]] [[file descriptors]]

# Buffer cache

> The buffer/page cache keeps recent disk blocks in RAM so reads avoid the disk and writes can flush later.

---

## Mental model

**Say it in one breath:** Linux caches file data in free RAM (page cache); “buff/cache” in `top` is mostly reclaimable — until dirty pages must hit disk.

```txt
app read/write
     │
     ▼
 page cache / buffer heads  ←── RAM (clean or dirty)
     │
     │  writeback / fsync / sync
     ▼
 block layer → disk / NVMe
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Page cache** | File-backed pages in RAM | “Modern Linux unifies caching around pages.” |
| **Buffer cache** | Block-oriented view (buffer heads) | “Still used for metadata/block I/O bookkeeping.” |
| **Dirty** | Modified in RAM, not yet on disk | “Power loss can lose dirty data without fsync.” |
| **Writeback** | Kernel flushes dirty pages | “Background flush vs hard throttle at dirty_ratio.” |
| **Reclaim** | Free cache under memory pressure | “Cache shrinks when apps need anon RAM.” |
| **`buff/cache`** | `free`/`top` column | “Not a memory leak — expect it to be large.” |

### How the story goes

1. **Read** — miss → disk → fill cache; hit → return from RAM.
2. **Write** — usually lands in cache as **dirty** (unless `O_SYNC` / sync mount).
3. **Writeback** — `pdflush`/writeback threads flush by ratio/time; [[fsync]] forces one file.
4. **Reclaim** — under pressure, clean pages go first; dirty must flush or block writers.

> [!INFO]
> Old teaching said “buffer cache vs page cache.” On modern Linux, file data is page-cache centric; [[buffer head]] still tracks block mappings for lower layers.

---

## Standard config / commands

```bash
# What’s cached / dirty
grep -E 'Buffers|Cached|Dirty|Writeback|MemAvailable' /proc/meminfo
free -h

# Writeback tunables (sysctl)
sysctl vm.dirty_ratio vm.dirty_background_ratio vm.dirty_expire_centisecs
# dirty_background_ratio ≈ start background flush (~10%)
# dirty_ratio ≈ throttle writers (~20%)

# Force flush (maintenance / lab — latency spike)
sync
echo 3 | sudo tee /proc/sys/vm/drop_caches   # drop clean caches only after sync

# Per-device / I/O view
iostat -x 1
```

```bash
# Persist softer writeback (example — tune with care)
# /etc/sysctl.d/99-dirty.conf
# vm.dirty_background_ratio = 5
# vm.dirty_ratio = 10
```

| Knob | Why it matters |
|------|----------------|
| `dirty_background_ratio` | Earlier background flush → fewer latency spikes |
| `dirty_ratio` | Hard stall for writers when too much dirty |
| `fsync` / `fdatasync` | Durability contract for one fd |
| `drop_caches` | Lab only — never “fix” prod by dropping cache routinely |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| “Memory almost full” but apps fine | `MemAvailable`, `Cached` | Normal cache use; don’t kill random processes |
| Write latency spikes | Dirty + writeback in `meminfo`; `iostat` | Lower dirty ratios; faster disk; batch fsync |
| Data missing after crash | App skipped fsync | Add durability protocol ([[fsync]], WAL) |
| Disk busy, CPU idle | Writeback storm / `wa` | Throttle writers; check RAID/NVMe health |
| DB double-caching | Large `shared_buffers` + OS cache | Size DB cache knowing OS still caches |
| Drop caches “fixed” it | Masked reclaim issue | Find leak / anon growth; don’t rely on drop |

---

## Gotchas

> [!WARNING]
> **`write()` success ≠ on disk** — only cache (and maybe controller cache) until [[fsync]] / barrier.

> [!WARNING]
> **Huge `buff/cache` is healthy** — free RAM is wasted RAM; panic on `used` without reading `available`.

> [!WARNING]
> **`echo 3 > drop_caches` needs root and hurts** — cold cache afterward; not a production tuning loop.

> [!WARNING]
> **NFS / VM writeback lies** — remote ack and hypervisor cache modes change durability ([[fsync]] gotchas).

---

## When NOT to use

- **Don’t “disable the cache” to make benchmarks look stable** — use proper sync flags or `direct I/O` only when the app owns caching (DB).
- **Don’t treat buffer cache as an app API** — apps use `read`/`write`/`mmap`/`fsync`; cache is kernel policy.
- **Don’t tune dirty_* blindly on shared hosts** — can starve neighbors; measure first.

---

## Related

[[kernel subsystem]] [[buffer]] [[buffer head]] [[buffer flags]] [[buffer lifecycle]] [[fsync]] [[multiple levels of buffering]] [[Persistent Block Storage]] [[disk IOPS]] [[Memory management]] [[RAM and Swap memory]] [[one-level storage system]]
