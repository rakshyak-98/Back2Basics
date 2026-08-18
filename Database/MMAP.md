[[Database]] [[WAL (Write-Ahead Log)]] [[fsync]] [[WiredTiger storage engine]] [[Buffer cache]] [[How to manipulate memory directly]]

# MMAP

> Map a file into the process address space — the OS page cache becomes your buffer pool; load and write look like pointer access.

## Mental model

**Say it in one breath:** `mmap` ties file bytes to virtual memory so reads/writes are loads/stores; the kernel faults pages in and writes dirty pages out.

```txt
Process VA                    Kernel                    Disk
───────────                   ──────                    ────
ptr = mmap(file)  ──fault──►  page cache ◄──────────►  file pages
store *ptr        ──dirty──►  same pages  ──writeback / msync──►
```

Databases historically used mmap as a **storage engine** (MongoDB MMAPv1; some embedded engines). Modern MongoDB uses [[WiredTiger storage engine]] (not MMAPv1). Many engines prefer an explicit buffer pool + [[WAL (Write-Ahead Log)]] so they control eviction and [[fsync]] timing.

OS-level mmap mechanics: [[How to manipulate memory directly]].

## Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **mmap** | Map file ↔ virtual memory | “I touch memory; the kernel does the I/O.” |
| --- | --- | --- |
| **Page fault** | First touch loads from disk/cache | “Working set too big ⇒ fault storm.” |
| **Dirty page** | Modified mapped page not yet on disk | “Durability needs `msync` / `fsync`, not just `store`.” |
| **Buffer pool** | Engine-managed cache | “Explicit pool beats mmap when you need predictable eviction.” |
| **Double caching** | Engine cache + OS page cache | “mmap engines lean on OS cache; WiredTiger can use direct I/O.” |
| **MMAPv1** | Old MongoDB engine | “Removed; don’t design new systems around it.” |

## Standard config / commands

### See pressure (Linux)

```bash
# Faults / major faults — rising major faults ⇒ working set not in RAM
ps -o min_flt,maj_flt,rss,vsz,cmd -p <pid>
sar -B 1 5          # pgscank, majflt/s
grep -E 'pgfault|pgmajfault' /proc/vmstat
```

### Durability when *you* use mmap in an app

```c
// After critical writes into a shared mapping:
msync(addr, len, MS_SYNC);   // or fsync(fd) on the underlying file
```

### MongoDB (historical vs today)

```txt
MMAPv1  → mmap + journal (legacy; removed)
WiredTiger → cache + journal / WAL-style durability  ([[WiredTiger storage engine]])
```

| Knob / signal | Why it matters |

| RSS vs file size | Mapped ≠ resident; only touched pages cost RAM |
| --- | --- |
| Major fault rate | Working set > RAM |
| `dirty_ratio` / writeback | Latency spikes when kernel flushes ([[Buffer cache]]) |
| Explicit `fsync` policy | Crash safety — see [[WAL (Write-Ahead Log)]], [[fsync]] |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Latency cliffs under load | `majflt`, `sar -B`, iowait | More RAM; shrink working set; engine with controlled cache |
| Data “saved” missing after crash | No `msync`/`fsync` | Durability protocol; don’t trust store alone |
| Huge VSZ, OOM killer | Large maps + overcommit | Cap cache; avoid mapping entire multi-TB file blindly |
| Double memory use | Engine cache + OS cache | `O_DIRECT` / tuned WiredTiger; or accept mmap single-cache model |
| MongoDB old docs mention mmap | Version check | Upgrade path to WiredTiger; ignore MMAPv1 tuning |

## Gotchas

> [!WARNING]
> **`mmap` write ≠ durable** — like `write()` into the page cache. Crash safety still needs `msync`/`fsync` and usually a WAL.

> [!WARNING]
> **SIGBUS on truncate/short reads** — accessing a hole past EOF in a shared map can kill the process; engines must handle file size carefully.

- **TLB / huge maps** — multi-TB maps stress virtual memory; not free.
- **Concurrent writers** — need your own locking; mmap does not give transactions.
- **Power-of-two allocation folklore** — some mmap-era allocators sized chunks that way; irrelevant to modern WiredTiger sizing.

## When NOT to use

- **New general-purpose DB design** — prefer explicit buffer pool + WAL (Postgres, InnoDB, WiredTiger).
- **Need strict latency SLOs under memory pressure** — kernel eviction is harder to reason about than your own pool.
- **Network filesystems with weak mmap semantics** — local SSD first.

## Related

[[How to manipulate memory directly]] [[Buffer cache]] [[fsync]] [[WAL (Write-Ahead Log)]] [[WiredTiger storage engine]] [[ARIES]] [[ACID]] [[memory engine]]
