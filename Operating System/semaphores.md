[[Operating System]] [[mutexes]] [[critical sections]] [[Thread]] [[Inter Process Communication]]

# Semaphores

> A semaphore counts permits — threads wait when the count is zero and post when releasing a resource — generalizing [[mutexes]] from binary locks to N-way pools.

**POSIX semaphores** (`sem_wait`, `sem_post`) and **System V semaphores** (in [[IPC namespace]]) coordinate producers and consumers, connection pools, and [[critical sections]] with bounded occupancy.

```txt
count = 3 → three threads may enter; fourth blocks until post
```

Binary semaphore ≈ mutex (with different ownership semantics). Counting semaphore models empty/full slots in bounded buffers.

## Sources

- Dijkstra — semaphore original definition
- Kerrisk, *The Linux Programming Interface*
- Wikipedia: [Semaphore (programming)](https://en.wikipedia.org/wiki/Semaphore_(programming))
