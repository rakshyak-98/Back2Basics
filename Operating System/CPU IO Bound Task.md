[[Operating System]] [[Blocking]] [[thread pool]] [[disk IOPS]] [[context switching]] [[multi-threaded]] [[non-blocking]] [[base clock speed]] [[Thread]]

# CPU IO Bound Task

> A task is I/O-bound when it spends most of its time waiting on disk, network, or locks — not executing instructions; thread and hardware sizing differ completely from CPU-bound work.





## Interview Relevance
Interviewers ask how you size a thread pool and whether adding cores helps — the answer hinges on correctly classifying CPU-bound vs I/O-bound (or mixed) work.

## Sources
- Google SRE Book — capacity planning — overview
- Kerrisk, *The Linux Programming Interface* — deep-dive
- [Wikipedia — I/O bound](https://en.wikipedia.org/wiki/I/O_bound) — overview

## Key Concepts
- **CPU-bound:** limited by instruction throughput / cores / SIMD.
- **I/O-bound:** limited by device latency, queue depth, bandwidth, or peer.
- **Mixed:** measure both; avoid buying CPU turbo for a disk-bound service.
- **Concurrency lever:** more waiters than cores can help I/O-bound work until [[context switching]] dominates.

## Technical Details
| Profile | Dominant wait | Thread count | Hardware emphasis |
|---------|---------------|--------------|-------------------|
| CPU-bound | — | ≈ physical cores | [[base clock speed]], SIMD |
| I/O-bound | Disk / NIC / peer | Can exceed cores | Queue depth, [[disk IOPS]], bandwidth |
| Mixed | Both | Measure | Avoid blind turbo spend |

I/O-bound services benefit from [[non-blocking]] loops or larger [[thread pool]]s so one blocked [[Thread]] does not stall all work.

```bash
pidstat -d 1 -p PID    # disk read/write
pidstat -w 1           # context switches while "idle"
iostat -xz 1           # device utilization
```

If CPU is low but latency high, look downstream: storage, DNS, database, or [[Blocking]] on a shared mutex.

## Real-World Applications
API gateways are often network I/O-bound (event loop). Image-encode workers are CPU-bound (core count). Database-heavy request handlers are mixed — pool size tuned from `pidstat` / DB wait metrics.

## Pros/Cons or Trade-offs
- **More threads (I/O-bound):** hide latency — until stacks and switches cost more than they gain.
- **More cores (CPU-bound):** linear help until memory bandwidth or lock contention caps it.
- **Wrong classification:** spending on CPUs when the bottleneck is [[disk IOPS]].

## Comparison
- vs [[Blocking]]: blocking is *how* you wait; bound type is *what* you wait on.
- vs [[multi-threaded]]: threads help I/O concurrency; they do not multiply single-core CPU throughput.

## Mistakes to Avoid
- Setting `workers = 2 × cores` for every service without measuring wait vs run time.
- Calling a service “CPU-bound” because CPU% is low — that usually means it is waiting.
- Ignoring lock contention as a fake I/O wait (threads blocked on mutex, not disk).
