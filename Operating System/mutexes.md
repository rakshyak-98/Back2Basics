[[Operating System]] [[critical sections]] [[semaphores]] [[Thread]] [[context switching]]

# Mutexes

> A mutex (mutual exclusion lock) ensures at most one thread runs a protected [[critical sections]] region at a time — the default tool when shared mutable state must not race.

POSIX **`pthread_mutex_t`**, C++ `std::mutex`, Java `synchronized` — all map to kernel **futex** waits when contended: fast atomic try in user space, [[Blocking]] sleep if held.

## Practices

- Lock ordering prevents deadlock (always A then B).
- Hold locks briefly — no disk I/O inside if possible.
- Prefer higher-level message passing when ownership is unclear.

[[semaphores]] generalize to counting resources; mutexes are typically binary.

Heavy contention increases [[context switching]] and cache line bouncing between cores.

## Sources

- Kerrisk, *The Linux Programming Interface* — mutexes and futex
- Wikipedia: [Mutual exclusion](https://en.wikipedia.org/wiki/Mutual_exclusion)
