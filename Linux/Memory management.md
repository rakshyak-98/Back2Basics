[[process]] [[Linux cgroup]] [[OOM (Linux Out Of Memory)]] [[management/Linux out of memory daemon]]

# Memory management

> Linux memory management balances anonymous pages, file cache, swap, and cgroup limits — look here when workloads slow down or die with exit 137.

```txt
        Memory management ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers want `MemAvailable` vs free, page cache reclaimability, overcomm…

## Sources
- [Documentation/admin-guide/mm/](https://www.kernel.org/doc/html/latest/admin-guide/mm/index.html) — deep-dive
- [proc(5) — /proc/meminfo](https://man7.org/linux/man-pages/man5/proc.5.html) — overview

## Key Concepts
- **Anonymous vs file-backed:** Anon is process heap/stack; file cache is reclaimable until dirtied.
- **MemAvailable:** Best estimate of memory for new work without heavy swapping.
- **Overcommit:** Heuristic / always / never (`vm.overcommit_memory`)
- **Swappiness:** Bias between reclaiming cache and swapping anon (0–100).
- **cgroup memory:** Per-slice caps trigger local OOM before host exhaustion.


- **Core:** Physical RAM holds **anonymous** memory (heap, stack) and **page cache** (fil…

## Technical Details
```bash
free -h
cat /proc/meminfo | head -20
ps aux --sort=-%mem | head
slabtop -o
vmstat 1
swapon --show

dmesg -T | grep -i 'out of memory'
cat /proc/sys/vm/overcommit_memory   # 0=heuristic, 1=always, 2=strict
cat /proc/sys/vm/swappiness

# Diagnostic only — not a fix
sync; echo 3 | sudo tee /proc/sys/vm/drop_caches
```

| Field | Meaning |
|-------|---------|
| `MemAvailable` | Roughly usable without swapping |
| `Cached` | Page cache — often reclaimable |
| `SwapTotal` / `SwapFree` | Swap capacity and free |
| `Dirty` | Pages waiting writeback |

## Mistakes to Avoid
- **Mistake:** Treating “low free RAM” as an emergency when `MemAvailable` is f…
- **Mistake:** Using `drop_caches` as a production “fix.”
- **Mistake:** Setting container memory limits below the process’s real working…

## Pros/Cons or Trade-offs
- **Pro overcommit:** Higher utilization
- **Con overcommit:** Failure at page-fault time → OOM under load.
- **Pro swap:** Absorbs spikes; **con:** latency cliffs under pressure.

## Comparison
- vs [[OOM (Linux Out Of Memory)]]: OOM is the kill path when reclaim fails


### Use cases
- Sizing JVM/Node heaps under Kubernetes limits, explaining why `free` shows li…
