[[Buffer cache]] [[buffer]] [[buffer lifecycle]] [[fsync]]

# Buffer head

> Per-block metadata wrapper in the kernel page cache — tracks dirty state, device/block identity, and LRU position for writeback and eviction.

---

## Mental model

Each cached disk block is represented by a **buffer head** (`struct buffer_head` in legacy terms; modern Linux ties this to the **page cache** and `bio` layer). The head is not the data — it is the **control record** for one logical block:

```txt
buffer head                    page (4 KiB may hold multiple blocks)
┌─────────────────┐           ┌──────────────────────────┐
│ device + block# │──────────►│ actual cached bytes      │
│ dirty? locked?  │           └──────────────────────────┘
│ LRU list ptr    │
│ ref count       │
└─────────────────┘
```

When user space calls `write()`, data lands in the page cache; the buffer head's **dirty bit** marks it for later flush. The **flusher thread** (`pdflush`/`bdi_writeback`) walks dirty heads and issues I/O. Eviction uses LRU timestamps on heads/pages — clean pages drop first; dirty pages must be written or discarded policy-dependent.

**Service impact:** runaway dirty buffers → memory pressure, long `sync` stalls, or sudden write bursts that saturate disk IOPS.

---

## Standard config / commands

### Inspect dirty page cache (proxy for buffer writeback pressure)

```bash
# Dirty + writeback memory (kB)
grep -E 'Dirty|Writeback|Cached' /proc/meminfo

# Per-block-device writeback tunables
sysctl vm.dirty_ratio vm.dirty_background_ratio vm.dirty_expire_centisecs
# dirty_background_ratio: start background flush (default ~10%)
# dirty_ratio: hard throttle for writers (default ~20%)
```

```bash
# Force flush (maintenance window only — latency spike)
sync
echo 3 | sudo tee /proc/sys/vm/drop_caches   # drops clean cache; does NOT skip fsync of dirty
```

### Tune for database / log-heavy workloads

```bash
# Lower latency spikes: flush earlier in background
sudo sysctl -w vm.dirty_background_ratio=5
sudo sysctl -w vm.dirty_ratio=15
# Persist in /etc/sysctl.d/99-dirty.conf
```

**Why:** high `dirty_ratio` lets apps buffer more in RAM (throughput↑) but causes multi-second stalls when the kernel finally throttles writers.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Sudden write latency spikes | `grep Dirty /proc/meminfo`; `iostat -x 1` | Lower `dirty_*` ratios; spread writes; faster disk |
| Data "written" but lost on crash | App uses `write()` without `fsync()` | Use `fsync`/`fdatasync` for durability contracts — see [[fsync]] |
| Memory full but `Cached` huge | Dirty pages not flushing (`Writeback` stuck) | Check disk health, D-state processes, RAID degraded |
| VM/container OOM with heavy I/O | Dirty page cache + cgroup memory | Set `memory.high`/`memory.max`; tune dirty ratios in guest |

---

## Gotchas

> [!WARNING]
> **`write()` returning success ≠ on disk.** The buffer head may still be dirty; only `fsync()` (or mount options like `sync`) guarantees persistence.

> [!WARNING]
> **`drop_caches` is not a durability tool.** It evicts clean pages; dirty data still needs writeback.

> [!WARNING]
> **Double caching:** user-space buffers + page cache = two copies. Direct I/O (`O_DIRECT`) bypasses page cache for DB engines that manage their own buffers.

---

## When NOT to use

Do not micro-manage buffer heads in application code — the kernel owns eviction and writeback. Reach for **`fsync` policy**, **mount options**, and **I/O schedulers** instead of trying to "flush one buffer head."

---

## Related

[[Buffer cache]] [[buffer lifecycle]] [[multiple levels of buffering]] [[disk IOPS]] [[fsync]]
