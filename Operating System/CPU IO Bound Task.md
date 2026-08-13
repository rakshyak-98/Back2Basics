[[Operating System]] [[Blocking]] [[thread pool]] [[disk IOPS]] [[context switching]] [[multi-threaded]]

# CPU IO Bound Task

> A task is I/O-bound when it spends most of its time waiting on disk, network, or locks held by others — not executing instructions; sizing threads and hardware differs completely from CPU-bound work.

## Bound type drives design

| Profile | Dominant wait | Thread count | Hardware emphasis |
|---------|---------------|--------------|-------------------|
| CPU-bound | — | ≈ physical cores | [[base clock speed]], SIMD |
| I/O-bound | Disk / NIC / peer | Can exceed cores | Queue depth, [[disk IOPS]], bandwidth |
| Mixed | Both | Measure | Avoid blind turbo spend |

I/O-bound services benefit from [[non-blocking]] loops or larger [[thread pool]]s so one blocked [[Thread]] does not stall all work — up to the point where [[context switching]] overhead dominates.

## Diagnosis

```bash
pidstat -d 1 -p PID    # disk read/write
pidstat -w 1           # context switches while "idle"
iostat -xz 1           # device utilization
```

If CPU is low but latency high, look downstream: storage, DNS, database, or [[Blocking]] on a shared mutex.

## Sources

- Google SRE Book — capacity planning
- Kerrisk, *The Linux Programming Interface*
- Wikipedia: [I/O bound](https://en.wikipedia.org/wiki/I/O_bound)
