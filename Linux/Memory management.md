[[process]] [[Linux cgroup]] [[OOM (Linux Out Of Memory)]] [[management/Linux out of memory daemon]]

# Memory management

> Linux memory management balances anonymous pages, file cache, swap, and cgroup limits — the first place to look when workloads slow down or die with exit 137.

Physical RAM holds **anonymous** memory (heap, stack) and **page cache** (file-backed pages the kernel can drop under pressure). The **swap** subsystem moves cold pages to disk. **Transparent huge pages** and **NUMA** policies affect latency on large servers.

## Operator visibility

```bash
free -h
cat /proc/meminfo | head -20

# Per-process RSS (rough)
ps aux --sort=-%mem | head

# Slab / kernel caches
slabtop -o

# Swap activity
vmstat 1
swapon --show
```

## Key `/proc/meminfo` fields

| Field | Meaning |
|-------|---------|
| `MemAvailable` | Estimate of memory available for new workloads without swapping |
| `Cached` | Page cache — often reclaimable |
| `SwapTotal` / `SwapFree` | Swap space in use |
| `Dirty` | Pages waiting writeback to disk |

## Pressure and OOM

When reclaim cannot free enough pages, the kernel invokes the **OOM killer** (global or per-cgroup). Symptoms: sudden process death, `dmesg` OOM lines, Kubernetes `OOMKilled`. See [[OOM (Linux Out Of Memory)]] and [[Linux cgroup]] `memory.max`.

```bash
dmesg -T | grep -i 'out of memory'
cat /proc/sys/vm/overcommit_memory   # 0=heuristic, 1=always, 2=strict
```

## Tunables (use with measurement)

```bash
# Drop caches — diagnostic only, not a fix
sync; echo 3 | sudo tee /proc/sys/vm/drop_caches

# Swappiness (0–100): tendency to swap vs drop cache
cat /proc/sys/vm/swappiness
```

## Related

[[OOM (Linux Out Of Memory)]] · [[Linux cgroup]] · [[management/Linux out of memory daemon]] · [[process]]

## Sources

- [Documentation/admin-guide/mm/](https://www.kernel.org/doc/html/latest/admin-guide/mm/index.html)
- `man 5 proc`
