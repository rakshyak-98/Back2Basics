[[Buffer cache]] [[file descriptors]] [[fsync]] [[How to manipulate memory directly]] [[context switching]]

# One-level storage system

> Classic OS mental model: disk and RAM are one addressable store via virtual memory — **Multics / early UNIX teaching canon**; explains page cache behavior today.

---

## Mental model

The **one-level store** illusion: programmers see a single large **virtual address space**. The OS + MMU map virtual pages to **RAM frames** or **disk blocks** transparently. There is no explicit `read()` in the mental model — a load instruction either hits RAM or page-faults and the kernel fills the page from disk.

```txt
Virtual address ──► page table ──► RAM frame (hot)
                              └──► not present ──► page fault ──► read from disk ──► frame
```

| Layer today | One-level store equivalent |
|-------------|---------------------------|
| **Virtual memory** | Uniform byte address space per process |
| **Page cache** | Disk pages cached in RAM — same physical pages mmap touches |
| **Swap** | Cold pages evicted to swap partition/file |
| **mmap** | File bytes appear as memory — no separate I/O API |
| **Demand paging** | Code/data loaded on first access, not at exec |

**Why staff engineers care:** every `read()`/`write()` on a warm file goes through the **page cache** anyway. Double-copy from "I'll mmap to be faster" often wins only at scale or random access patterns — see [[How to manipulate memory directly]].

---

## Standard config / commands

### Observe paging behavior

```shell
# Page faults (major = disk, minor = RAM mapping)
ps -o min_flt,maj_flt,cmd -p PID
cat /proc/PID/stat | awk '{print "minflt="$10, "majflt="$12}'

# System-wide fault rate
vmstat 1
# in column: si/so = swap in/out; us/sy = CPU; wa = I/O wait

# What's in page cache (approx)
free -h
# "buff/cache" — reclaimable on memory pressure

# Drop caches (lab only — never prod)
sync; echo 3 | sudo tee /proc/sys/vm/drop_caches
```

### Tuning knobs (Linux VM)

```shell
# Swappiness — how aggressively to swap vs drop cache (0–100)
cat /proc/sys/vm/swappiness          # default often 60
sudo sysctl vm.swappiness=10         # DB/analytics: prefer cache over swap

# Dirty page writeback
sysctl vm.dirty_ratio vm.dirty_background_ratio
# High dirty_ratio → burst fsync latency spikes ([[fsync]] note)
```

### Relate to application I/O

```txt
write() → dirty page in page cache → async flush by pdflush/flusher thread
fsync() → force dirty pages + metadata for THAT fd's file
mmap MAP_SHARED write → same dirty pages — msync/fsync for durability
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Sudden latency spikes | `majflt` rising; `vmstat` `wa` | Cold cache after deploy; insufficient RAM; preload/warm |
| OOM killer | `free -h`; cgroup limit | Process RSS + cache pressure; reduce footprint or add RAM |
| Thrashing | High `si/so` in vmstat | Working set > RAM; swap storm — reduce concurrency |
| "Written" data lost on crash | fsync policy | App must [[fsync]] WAL/checkpoints; page cache ≠ durable |
| mmap slower than read | Random access on huge file | Expected — fault-per-page; readahead tuning |
| One process eats RAM | `/proc/PID/smaps_rollup` | Leak vs legitimate cache; `MADV_DONTNEED` rarely in app code |

```shell
# Per-process RSS vs shared cache
pmap -x PID | tail -1
cat /proc/PID/smaps_rollup
```

---

## Gotchas

> [!WARNING]
> **Page cache is shared** — one service reads 10GB file; cache fills; other services evicted — noisy neighbor on same host.

> [!WARNING]
> **Double buffering** — DB (InnoDB buffer pool) + OS page cache = same bytes cached twice unless **O_DIRECT** — trade CPU for predictable latency.

> [!WARNING]
> **Minor vs major faults** — startup "fault storm" after fork/CoW (`copy-on-write`) looks like disk I/O in metrics but is RAM mapping.

> [!WARNING]
> **Container memory limit** — cgroup OOM counts cache charged to container depending on kernel version; `node_exporter` RSS misleading.

> [!WARNING]
> **One-level store is an illusion** — programmers still need [[fsync]] discipline; the kernel does not sync every write to disk.

---

## When NOT to use

- **Teaching junior devs pointer math** — start with virtual memory + page cache diagram, not Multics history.
- **Assuming uniform latency** — NUMA, swap, and disk tiers break the illusion; size RAM for working set.
- **Bypassing cache "for speed"** without measurement — O_DIRECT requires aligned buffers and complicates portability.

---

## Related

[[Buffer cache]] [[file descriptors]] [[fsync]] [[How to manipulate memory directly]] [[multiple levels of buffering]] [[OOM (Linux Out Of Memory)]]
