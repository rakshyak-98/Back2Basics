[[Operating System]] [[RAM and Swap memory]] [[Browser memory]] [[OOM (Linux Out Of Memory)]] [[Stack Frame]]

# Heap memory

> Heap memory is dynamically allocated process memory — malloc, new, garbage-collected arenas — growing independently of the call stack and subject to fragmentation and OOM policy.

Contrast **stack** ([[Stack Frame]], [[stack pointer]]): automatic, LIFO, fixed per thread. **Heap** allocations persist until `free()` or GC; poor patterns cause leaks and fragmentation.

## Kernel interaction

Allocators (`malloc`, jemalloc, tcmalloc) request anonymous pages with `brk()` / `mmap()`. Resident size (RSS) counts toward [[cgroup (Control Group)]] and triggers [[OOM (Linux Out Of Memory)]] when over limit. Swap ([[RAM and Swap memory]]) may page cold heap pages to disk — disastrous for latency-sensitive JVM/Go heaps.

```bash
pmap -x PID
cat /proc/PID/smaps_rollup
```

## Browser and language runtimes

[[Browser memory]] splits JS heap versus native renderer allocations. Managed runtimes trade developer safety for GC pauses and larger footprint.

## Sources

- Wilson et al., “Dynamic Storage Allocation: A Survey and Classification”
- Kerrisk, *The Linux Programming Interface* — memory allocation
- Wikipedia: [Dynamic memory allocation](https://en.wikipedia.org/wiki/Dynamic_memory_allocation)
