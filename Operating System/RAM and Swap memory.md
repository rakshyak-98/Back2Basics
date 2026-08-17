[[Operating System]] [[Heap memory]] [[Buffer cache]] [[OOM (Linux Out Of Memory)]] [[cgroup (Control Group)]] [[CPU IO Bound Task]] [[fsync]]

# RAM and Swap memory

> RAM holds running code, stacks, heaps, and cache; swap extends virtual memory to disk when physical pages are scarce — trading latency for capacity.

```txt
        RAM and Swap memor ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Classic ops interview: read `free -h`, explain buff/cache vs used, when swap …

## Sources
- [Linux kernel docs — MM concepts / swap](https://docs.kernel.org/admin-guide/mm/concepts.html) — deep-dive
- Linux `swapon(8)` manual page — overview
- [Wikipedia — Virtual memory](https://en.wikipedia.org/wiki/Virtual_memory) — overview

## Key Concepts
- **Anonymous vs file-backed:** heaps/stacks vs [[Buffer cache]] pages.
- **Swap:** pages cold anonymous memory to disk to free RAM.
- **Swappiness:** bias reclaim toward cache vs process pages (`vm.swappiness`).
- **Not durability:** power-off swap is not intentional persistence — [[fsync]] is for files.

## Technical Details
```bash
free -h
swapon --show
cat /proc/swaps
```

- High swap use → latency spikes on page faults ([[CPU IO Bound Task]]).
- [[cgroup (Control Group)]] `memory.max` can OOM-kill before swap helps.

## Mistakes to Avoid
- **Mistake:** Panic because `free` “available” looks low while buff/cache is r…
- **Mistake:** Enabling huge swap and calling the host “fine” while p99 latency…
- **Mistake:** Expecting swap to preserve application state across reboot

## Pros/Cons or Trade-offs
- **Pro:** Survives memory spikes without immediate OOM.
- **Con:** Thrashing turns the machine into a disk-bound crawl.
- **Trade-off:** more RAM vs accepting rare swap vs hard OOM kills.

## Comparison
- vs [[Heap memory]]: heap is process-virtual; RAM/swap is physical backing.
- vs [[Buffer cache]]: file cache is reclaimable; anonymous pages need swap or OOM under pressure.


### Use cases
- Latency-sensitive JVM/Go services often disable or minimize swap and size RAM…
