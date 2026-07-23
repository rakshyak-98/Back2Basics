[[Linux]] [[OOM (Linux Out Of Memory)]] [[Linux cgroup]] [[process]] [[Linux Process Theory]]

# Linux Memory Management

> One-line: virtual memory = per-process address spaces + page cache + swap — OOM kills when overcommit meets real RAM pressure.

## Mental model

Each process sees a **virtual address space** (heap, mmap, stack). Physical RAM holds **resident** pages; unused file pages live in **page cache** (reclaimable). Kernel may **overcommit** — allocate more virtual memory than RAM until someone touches it.

```
┌──────────── process ────────────┐
│ stack (per-thread, grows down)  │
│ heap (malloc/brk, grows up)     │
│ mmap regions, code (.text)      │
└─────────────────────────────────┘
         ↓ page faults map to RAM or swap
┌──────── physical memory ────────┐
│ anon pages │ page cache │ slab  │
└─────────────────────────────────┘
```

**RSS** (resident set) ≈ RAM actually used by process. **VSZ** ≈ virtual size (often much larger).

---

## Standard config / commands

### Inspect process memory

```bash
ps aux --sort=-rss | head
top -o %MEM
pmap -x PID                        # detailed mapping
cat /proc/PID/status | grep -E 'VmRSS|VmSize|Threads'
cat /proc/PID/smaps_rollup         # kernel 4.14+ summary

go run main.go & pmap $!
```

### System-wide

```bash
free -h
vmstat 1
cat /proc/meminfo
slabtop
```

Key `meminfo` lines: `MemAvailable` (best "how much can I allocate"), `Cached`, `SwapFree`.

### Limits

```bash
ulimit -a
ulimit -v                        # virtual memory (KB) — rarely set
ulimit -m                        # physical — often unlimited on Linux
cat /proc/PID/limits
```

### Stack size (threads)

```bash
ulimit -s                        # default stack per thread (often 8192 KB)
pthread_create attr / `RLIMIT_STACK`
```

Single-threaded: one stack. Multi-threaded: **each thread** gets its own stack (typically 8 MB default × thread count adds up fast).

### Swap & swappiness

```bash
cat /proc/sys/vm/swappiness      # 0-100, tendency to swap anon pages
sudo sysctl vm.swappiness=10     # servers often lower; laptops higher
swapon --show
```

### OOM killer

```bash
dmesg | grep -i 'out of memory'
journalctl -k | grep -i oom
cat /proc/PID/oom_score_adj        # -1000 to 1000; lower = less likely victim
echo -17 | sudo tee /proc/PID/oom_score_adj   # protect critical daemon (careful)
```

See [[OOM (Linux Out Of Memory)]] and [[Linux cgroup]] for container limits.

---

## Single-thread vs multi-thread stacks

| Aspect | Single-thread | Multi-thread |
|--------|---------------|--------------|
| Stacks | One | One per thread |
| Heap | Process-wide | Shared across threads |
| Isolation | Stack overflow kills process | One thread stack overflow can corrupt process |
| Memory overhead | Lower | +(~MB × thread count) for stacks |
| Communication | N/A | Shared heap — needs sync ([[mutexes]]) |

Stack ops are fast (LIFO, compiler-managed). Thread stacks are allocated at thread creation — configure if deep recursion expected.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Process killed, no app log | `dmesg`, `journalctl -k` OOM | Reduce memory; cgroup limit; fix leak; add RAM |
| Slow before kill | Rising RSS in `top`; swap in | Memory leak profiling; restart policy |
| `Cannot allocate memory` but free shows GB | cgroup limit; `vm.overcommit`; max map count | `cat memory.max`; `sysctl vm.overcommit_memory` |
| Container OOMKilled (137) | `kubectl describe pod` / docker inspect | Raise limit or fix leak; see [[Linux cgroup]] |
| High cache, low Available | Normal — cache reclaims | Don't panic on `free` showing little "free" |
| Thread count explosion → RAM | `ps -o nlwp PID` | Pool threads; fix fork bomb |

```bash
# Leak suspicion — sample RSS over time
while sleep 5; do ps -o rss= -p PID; done
valgrind --tool=massif ./app    # dev only
```

---

## Gotchas

> [!WARNING]
> **`free` "available" vs "free"** — Linux uses spare RAM for cache; low "free" with high "available" is healthy.

> [!WARNING]
> **Overcommit** — `malloc` succeeds, OOM later on first touch under pressure.

> [!WARNING]
> **Go/Java RSS** — runtime retains heap; not always a leak. Check GC / heap profiles.

> [!WARNING]
> **Copy-on-write after fork** — [[clustering]] / prefork models spike memory briefly on write.

> [!WARNING]
> **THP (transparent huge pages)** — sometimes hurts latency on DB workloads; distro-dependent tuning.

---

## When NOT to use

- **Disabling OOM killer globally** — masks problems; tune per-service with cgroups instead.
- **Setting unlimited stack on all threads** — multi-GB virtual waste and mask recursion bugs.

---

## Related

[[Linux cgroup]] [[OOM (Linux Out Of Memory)]] [[management/Linux out of memory daemon]] [[process]] [[mutexes]]
