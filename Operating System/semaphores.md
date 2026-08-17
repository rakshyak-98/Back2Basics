[[Operating System]] [[mutexes]] [[critical sections]] [[Thread]] [[Inter Process Communication]] [[IPC namespace]]

# Semaphores

> A semaphore counts permits — threads wait at zero and post when releasing a resource — generalizing [[mutexes]] from binary locks to N-way pools.





## Interview Relevance
Counting vs binary semaphores, producer-consumer, and SysV semaphores living in an [[IPC namespace]].

## Sources
- Dijkstra — semaphore original definition — overview
- Kerrisk, *The Linux Programming Interface* — deep-dive
- [Wikipedia — Semaphore (programming)](https://en.wikipedia.org/wiki/Semaphore_(programming)) — overview

## Key Concepts
- **Count of permits:** `wait` decrements (blocks at 0); `post` increments.
- **Binary ≈ mutex-like** (ownership semantics differ).
- **Counting:** models empty/full slots, connection pools.
- **IPC variants:** POSIX vs System V (namespaced).

## Technical Details
```txt
count = 3 → three threads may enter; fourth blocks until post
```

POSIX: `sem_wait`, `sem_post`. System V semaphores coordinate across processes ([[Inter Process Communication]]) and respect [[IPC namespace]] in containers.

Used with [[critical sections]] when bounded occupancy matters — not only exclusive ownership.

## Real-World Applications
Bounded buffers, connection pools, and classic producer-consumer labs.

## Pros/Cons or Trade-offs
- **Pro:** Natural model for N identical resources.
- **Con:** Easy to mismanage posts/waits; harder to reason than scoped mutex guards.
- **Trade-off:** semaphore vs condition variables + mutex for complex predicates.

## Comparison
- vs [[mutexes]]: exclusive ownership vs counting permits.
- vs lock-free rings: semaphores often pair with queues for blocking policy.

## Mistakes to Avoid
- Using a binary semaphore as a mutex without clarifying ownership/reentrancy.
- Forgetting to destroy/unlink named semaphores.
- Spurious wakeups-style logic bugs when replacing condvars carelessly.
