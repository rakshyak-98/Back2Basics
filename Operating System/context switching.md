[[Operating System]] [[Thread]] [[multi-threaded]] [[SMT threads]] [[mutexes]] [[thread pool]] [[system call]] [[non-blocking]] [[Epoll]] [[cgroup (Control Group)]]

# Context switching

> A context switch saves one thread’s CPU registers and restores another’s — the scheduler tax that shows up as `cs` in vmstat when runnable work outruns clean core capacity.

```txt
        Context switching ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Explain voluntary vs involuntary switches, process vs thread switch cost (TLB…

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

- Mitigation:

- Size [[thread pool]] ≈ cores for CPU-bound work.
- Event loops for many idle connections ([[non-blocking]], [[Epoll]]).
- Avoid oversubscribing [[SMT threads]] with lock-heavy workers.

- [[cgroup (Control Group)]] CPU throttling increases involuntary switches unde…

## Mistakes to Avoid
- **Mistake:** Treating high `cs` as always bad
- **Mistake:** Spawning unbounded threads “for concurrency.”
- **Mistake:** Ignoring cgroup throttling as a source of involuntary switches

## Pros/Cons or Trade-offs
- **Pro:** Enables multitasking and overlap of I/O with compute.
- **Con:** Excess switches waste cycles and hurt cache locality.
- **Trade-off:** more threads for I/O concurrency vs switch overhead.

## Comparison
- vs [[mutexes]] contention: lock waits *cause* switches; fixing locks can cut `cs`.
- vs migration: moving across cores is related but includes cache migration cost.


### Use cases
- Diagnosing “high CPU but low useful work,” tuning worker counts, and explaini…
