[[Operating System]] [[Blocking]] [[thread pool]] [[disk IOPS]] [[context switching]] [[multi-threaded]] [[non-blocking]] [[base clock speed]] [[Thread]]

# CPU IO Bound Task

> A task is I/O-bound when it spends most of its time waiting on disk, network, or locks — not executing instructions; thread and hardware sizing differ completely from CPU-bound work.

```txt
        CPU IO Bound Task ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask how you size a thread pool and whether adding cores helps

## Sources
- Google SRE Book — capacity planning — overview
- Kerrisk, *The Linux Programming Interface* — deep-dive
- [Wikipedia — I/O bound](https://en.wikipedia.org/wiki/I/O_bound) — overview

## Key Concepts
- **CPU-bound:** limited by instruction throughput / cores / SIMD.
- **I/O-bound:** limited by device latency, queue depth, bandwidth, or peer.
- **Mixed:** measure both; avoid buying CPU turbo for a disk-bound service.
- **Concurrency lever:** more waiters than cores can help I/O-bound work until [[context switching]] d…

## Technical Details
| Profile | Dominant wait | Thread count | Hardware emphasis |
|---------|---------------|--------------|-------------------|
| CPU-bound | — | ≈ physical cores | [[base clock speed]], SIMD |
| I/O-bound | Disk / NIC / peer | Can exceed cores | Queue depth, [[disk IOPS]], bandwidth |
| Mixed | Both | Measure | Avoid blind turbo spend |

- I/O-bound services benefit from [[non-blocking]] loops or larger [[thread poo…

```bash
pidstat -d 1 -p PID    # disk read/write
pidstat -w 1           # context switches while "idle"
iostat -xz 1           # device utilization
```

- If CPU is low but latency high, look downstream: storage, DNS, database, or […

## Mistakes to Avoid
- **Mistake:** Setting `workers = 2 × cores` for every service without measurin…
- **Mistake:** Calling a service “CPU-bound” because CPU% is low
- **Mistake:** Ignoring lock contention as a fake I/O wait (threads blocked on …

## Pros/Cons or Trade-offs
- **More threads (I/O-bound):** hide latency
- **More cores (CPU-bound):** linear help until memory bandwidth or lock conten…
- **Wrong classification:** spending on CPUs when the bottleneck is [[disk IOPS…

## Comparison
- vs [[Blocking]]: blocking is *how* you wait; bound type is *what* you wait on.
- vs [[multi-threaded]]: threads help I/O concurrency


### Use cases
- API gateways are often network I/O-bound (event loop). Image-encode workers a…
