[[Operating System]] [[critical sections]] [[semaphores]] [[Thread]] [[context switching]] [[Blocking]]

# Mutexes

> A mutex (mutual exclusion lock) ensures at most one thread runs a protected [[critical sections]] region at a time — the default tool when shared mutable state must not race.

```txt
        Mutexes ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Futex fast-path, lock ordering, hold-time rules, and mutex vs semaphore.

## Sources
- Kerrisk, *The Linux Programming Interface* — mutexes and futex — deep-dive
- [Wikipedia — Mutual exclusion](https://en.wikipedia.org/wiki/Mutual_exclusion) — overview

## Key Concepts
- **Binary ownership:** one holder at a time.
- **Futex path:** atomic try in user space; [[Blocking]] sleep if contended.
- **Ordering:** always acquire locks in one global order.
- **Hold briefly:** avoid I/O inside the lock.

## Technical Details
- POSIX `pthread_mutex_t`, C++ `std::mutex`, Java `synchronized`

- [[semaphores]] generalize to counting resources; mutexes are typically binary.

- Heavy contention increases [[context switching]] and cache-line bouncing betw…
- Prefer message passing when ownership is unclear.

## Mistakes to Avoid
- **Lock ordering cycles::** → deadlock
- **Mistake:** Doing disk/network I/O while holding a mutex
- **Mistake:** Using a mutex where a concurrent queue/message pass would remove…

## Pros/Cons or Trade-offs
- **Pro:** Simple correctness model for shared memory.
- **Con:** Deadlocks, priority inversion, contention collapse.
- **Trade-off:** coarse vs fine-grained locking.

## Comparison
- vs [[semaphores]]: counting permits vs exclusive ownership.
- vs atomics/lock-free: mutexes are easier; lock-free needs careful proofs.


### Use cases
- Protecting shared maps, connection tables, and reference counts in [[Thread]]…
