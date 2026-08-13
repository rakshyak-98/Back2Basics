[[Operating System]] [[Blocking Vs Non-Blocking]] [[non-blocking]] [[system call]] [[Thread]] [[context switching]]

# Blocking

> A blocking operation holds the calling thread until the kernel can complete work — disk read, mutex, sleep — and that wait usually costs a context switch.

When a [[Thread]] invokes a **blocking** [[system call]] such as `read()` on an empty pipe or `accept()` with no connection, the kernel marks the thread blocked, schedules another runnable thread, and later wakes the caller when data arrives. From the application’s perspective the call does not return until the event happens (or a signal interrupts it).

## Blocking versus readiness

| Mode | If data not ready | Thread state |
|------|-------------------|--------------|
| Blocking (default) | Waits inside kernel | Blocked → [[context switching]] |
| [[non-blocking]] | Returns immediately with `EAGAIN` | Stays runnable |

Blocking code is simple to reason about: sequential reads and writes mirror human workflow. At high concurrency, thousands of blocked threads consume stack memory and scheduler bookkeeping — the classic motivation for event loops and [[Epoll]].

## Common blocking points

- Disk and network I/O waiting on media or peer
- `pthread_mutex_lock` when the lock is held
- `futex` waits inside glibc mutexes ([[mutexes]])
- `poll()` / `select()` without timeout

## Design tension

**When blocking is fine:** worker count matches concurrent operations (small server, batch job, thread pool sized to cores).

**When blocking hurts:** one thread must multiplex many connections — switch to non-blocking I/O and a reactor, or use async runtimes that hide blocking in a pool.

See [[Blocking Vs Non-Blocking]] for side-by-side trade-offs.

## Sources

- Kerrisk, *The Linux Programming Interface* — file I/O and threads
- Stevens & Rago, *Advanced Programming in the UNIX Environment*
- Wikipedia: [Blocking (computing)](https://en.wikipedia.org/wiki/Blocking_(computing))
