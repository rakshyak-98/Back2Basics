[[Operating System]] [[Thread]] [[multi-threaded]] [[SMT threads]] [[mutexes]] [[thread pool]]

# Context switching

> A context switch saves one thread’s CPU registers and restores another’s — the scheduler tax that shows up as `cs` in vmstat when you have more runnable work than cores can serve cleanly.

Triggered by timer preemption, blocking [[system call]], lock contention, or explicit yield. **Process switch** (different address space) costs more than **thread switch** within one process because MMU state and TLB entries may change.

## Costs

- **Direct:** microseconds in kernel scheduler paths.
- **Indirect:** cold caches and branch predictors — often dominates on hot loops.

## Measurement

```bash
vmstat 1          # cs column
pidstat -w 1      # voluntary vs involuntary
perf stat -e context-switches,cpu-migrations -p PID
```

## Mitigation patterns

- Size [[thread pool]] to ~cores for CPU-bound work.
- Prefer event loops for many idle connections ([[non-blocking]], [[Epoll]]).
- Avoid oversubscribing [[SMT threads]] with lock-heavy workers.

[[cgroup (Control Group)]] CPU throttling increases involuntary switches under quota pressure.

## Sources

- Silberschatz, Galvin & Gagne, *Operating System Concepts* — CPU scheduling
- Linux kernel documentation: [Scheduler](https://docs.kernel.org/scheduler/index.html)
- Wikipedia: [Context switch](https://en.wikipedia.org/wiki/Context_switch)
