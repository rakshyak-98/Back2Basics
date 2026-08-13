[[Operating System]] [[Heap memory]] [[Buffer cache]] [[OOM (Linux Out Of Memory)]] [[cgroup (Control Group)]]

# RAM and Swap memory

> RAM holds running code, stacks, heaps, and cache; swap extends virtual memory to disk when physical pages are scarce — trading latency for capacity.

Linux uses **anonymous** pages (heap, stack) and **file-backed** pages ([[Buffer cache]]). Under pressure the **swap** subsystem pages cold anonymous memory to a swap file or partition, freeing RAM.

```bash
free -h
swapon --show
cat /proc/swaps
```

## Behavior

- High swap use → latency spikes on page faults ([[CPU IO Bound Task]]).
- `vm.swappiness` biases reclaim toward cache versus process pages.
- [[cgroup (Control Group)]] `memory.max` can OOM-kill before swap helps.

Swap is not a durability mechanism — powered-off swap does not preserve intentional persistence ([[fsync]] matters for files).

## Sources

- Linux kernel documentation: [Swap Management](https://docs.kernel.org/admin-guide/mm/concepts.html)
- Linux `swapon(8)` manual page
- Wikipedia: [Virtual memory](https://en.wikipedia.org/wiki/Virtual_memory)
