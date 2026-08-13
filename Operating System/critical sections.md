[[Operating System]] [[mutexes]] [[semaphores]] [[multi-threaded]] [[Thread]]

# Critical sections

> A critical section is a stretch of code that must not run concurrently with other threads touching the same data — mutual exclusion makes those regions safe.

Without protection, two threads updating a counter or linked list can interleave into torn state. **Locks** ([[mutexes]], spinlocks) or **lock-free atomics** serialize access.

```txt
Thread A: lock → read/modify/write shared → unlock
Thread B:        lock (waits) ───────────────► enters critical section
```

## Rules of thumb

- Keep critical sections **short** — no I/O or blocking calls inside if avoidable.
- One lock ordering across the codebase prevents deadlock.
- [[semaphores]] allow counting resources; mutexes are typically binary ownership.

Priority inversion happens when a low-priority thread holds a lock a high-priority thread needs — real-time kernels add priority inheritance.

## Sources

- Herlihy & Shavit, *The Art of Multiprocessor Programming*
- Silberschatz — synchronization chapter
- Wikipedia: [Critical section](https://en.wikipedia.org/wiki/Critical_section)
