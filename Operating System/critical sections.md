[[Operating System]] [[mutexes]] [[semaphores]] [[multi-threaded]] [[Thread]]

# Critical sections

> A critical section is a stretch of code that must not run concurrently with other threads touching the same data — mutual exclusion makes those regions safe.





## Interview Relevance
Sync basics: what races look like, keep sections short, lock ordering, and priority inversion.

## Sources
- Herlihy & Shavit, *The Art of Multiprocessor Programming* — deep-dive
- Silberschatz — synchronization chapter — deep-dive
- [Wikipedia — Critical section](https://en.wikipedia.org/wiki/Critical_section) — overview

## Key Concepts
- **Mutual exclusion:** only one thread in the section for a given shared object.
- **Tools:** [[mutexes]], spinlocks, or lock-free atomics.
- **Short sections:** no I/O/blocking inside if avoidable.
- **Ordering:** global lock order prevents deadlock.

## Technical Details
```txt
Thread A: lock → read/modify/write shared → unlock
Thread B:        lock (waits) ───────────────► enters critical section
```

[[semaphores]] allow counting resources; mutexes are typically binary ownership.

Priority inversion: low-priority holder blocks high-priority waiter — real-time kernels add priority inheritance.

## Real-World Applications
Protecting shared counters, connection tables, and in-memory indexes in [[multi-threaded]] servers.

## Pros/Cons or Trade-offs
- **Pro:** Correct shared-memory concurrency.
- **Con:** Contention serializes; deadlock risk.
- **Trade-off:** coarse locks (simpler) vs fine locks (more parallelism, harder).

## Comparison
- vs [[mutexes]]: mutex is the lock object; critical section is the protected code region.
- vs message passing: avoid shared mutable state instead of guarding it.

## Mistakes to Avoid
- Holding locks across disk/network I/O.
- Inconsistent lock ordering across modules.
- “Fixing” races with `sleep` instead of real synchronization.
