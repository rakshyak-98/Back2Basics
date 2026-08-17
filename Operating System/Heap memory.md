[[Operating System]] [[RAM and Swap memory]] [[Browser memory]] [[OOM (Linux Out Of Memory)]] [[Stack Frame]] [[stack pointer]] [[cgroup (Control Group)]]

# Heap memory

> Heap memory is dynamically allocated process memory — `malloc`, `new`, GC arenas — growing independently of the call stack and subject to fragmentation and OOM policy.

```txt
        Heap memory ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers contrast stack vs heap, ask how allocators get pages from the ke…

## Sources
- Wilson et al., “Dynamic Storage Allocation: A Survey and Classification” — deep-dive
- Kerrisk, *The Linux Programming Interface* — memory allocation — deep-dive
- [Wikipedia — Dynamic memory allocation](https://en.wikipedia.org/wiki/Dynamic_memory_allocation) — overview

## Key Concepts
- **Stack vs heap:** stack is LIFO per thread ([[Stack Frame]], [[stack pointer]])
- **Allocator → kernel:** `brk` / `mmap` anonymous pages; RSS counts toward limits.
- **Fragmentation / leaks:** long-lived processes can grow RSS even with GC if native caches pin memory.
- **Swap interaction:** cold heap pages may go to [[RAM and Swap memory]]

## Technical Details
- Allocators (`malloc`, jemalloc, tcmalloc) request anonymous pages.
- Resident size (RSS) counts toward [[cgroup (Control Group)]] and can trigger …

```bash
pmap -x PID
cat /proc/PID/smaps_rollup
```

- [[Browser memory]] splits JS heap versus native renderer allocations.
- Managed runtimes trade safety for GC pauses and larger footprint.

## Mistakes to Avoid
- **Mistake:** Ignoring native allocations when only watching a managed heap me…
- **Mistake:** Setting container memory == JVM `-Xmx` with no headroom for meta…
- **Mistake:** Assuming `free()` always returns pages to the OS immediately (al…

## Pros/Cons or Trade-offs
- **Pro:** Flexible lifetimes; shared by all threads in the process.
- **Con:** Leaks, fragmentation, allocator lock contention.
- **Trade-off:** GC convenience vs pause/RSS unpredictability.

## Comparison
- vs [[Stack Frame]]: automatic, bounded, no free; heap is explicit/managed lifetime.
- vs [[Browser memory]]: browser total includes heaps across processes plus GPU/DOM.


### Use cases
- JVM/Go services tune heap size against container `memory.max`
