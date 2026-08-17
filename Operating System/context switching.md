[[Operating System]] [[Thread]] [[multi-threaded]] [[SMT threads]] [[mutexes]] [[thread pool]] [[system call]] [[non-blocking]] [[Epoll]] [[cgroup (Control Group)]]

# Context switching

> A context switch saves one thread’s CPU registers and restores another’s — the scheduler tax that shows up as `cs` in vmstat when runnable work outruns clean core capacity.





## Interview Relevance
Explain voluntary vs involuntary switches, process vs thread switch cost (TLB), and mitigations (pool sizing, event loops).

## Sources
- Silberschatz, Galvin & Gagne, *Operating System Concepts* — CPU scheduling — deep-dive
- [Linux kernel docs — Scheduler](https://docs.kernel.org/scheduler/index.html) — deep-dive
- [Wikipedia — Context switch](https://en.wikipedia.org/wiki/Context_switch) — overview

## Key Concepts
- **Triggers:** timer preemption, blocking [[system call]], lock wait, yield.
- **Process vs thread switch:** address-space change costs more (MMU/TLB).
- **Direct cost:** microseconds in scheduler paths.
- **Indirect cost:** cold caches/branch predictors — often dominates.

## Technical Details
```bash
vmstat 1          # cs column
pidstat -w 1      # voluntary vs involuntary
perf stat -e context-switches,cpu-migrations -p PID
```

Mitigation:

- Size [[thread pool]] ≈ cores for CPU-bound work.
- Event loops for many idle connections ([[non-blocking]], [[Epoll]]).
- Avoid oversubscribing [[SMT threads]] with lock-heavy workers.

[[cgroup (Control Group)]] CPU throttling increases involuntary switches under quota pressure.

## Real-World Applications
Diagnosing “high CPU but low useful work,” tuning worker counts, and explaining latency cliffs under oversubscription.

## Pros/Cons or Trade-offs
- **Pro:** Enables multitasking and overlap of I/O with compute.
- **Con:** Excess switches waste cycles and hurt cache locality.
- **Trade-off:** more threads for I/O concurrency vs switch overhead.

## Comparison
- vs [[mutexes]] contention: lock waits *cause* switches; fixing locks can cut `cs`.
- vs migration: moving across cores is related but includes cache migration cost.

## Mistakes to Avoid
- Treating high `cs` as always bad — some wait-driven switches are healthy.
- Spawning unbounded threads “for concurrency.”
- Ignoring cgroup throttling as a source of involuntary switches.
