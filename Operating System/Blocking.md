[[Operating System]] [[Blocking Vs Non-Blocking]] [[non-blocking]] [[system call]] [[Thread]] [[context switching]] [[mutexes]] [[Epoll]]

# Blocking

> A blocking call holds the calling thread until the kernel finishes the work — disk, network, lock, or sleep — and that wait usually costs a context switch.





## Interview Relevance
Interviewers want you to explain what happens to a thread during a blocking `read`/`accept`, why thousands of blocked threads hurt, and when blocking is still the right model versus an event loop.

## Sources
- Kerrisk, *The Linux Programming Interface* — file I/O and threads — deep-dive
- Stevens & Rago, *Advanced Programming in the UNIX Environment* — deep-dive
- [Wikipedia — Blocking (computing)](https://en.wikipedia.org/wiki/Blocking_(computing)) — overview

## Key Concepts
- **Blocked thread:** kernel removes the thread from the run queue until an event (data ready, lock free, timer).
- **Context switch cost:** stacks, TLB/cache effects, scheduler bookkeeping — see [[context switching]].
- **Default I/O mode:** most fds start blocking; readiness APIs and `O_NONBLOCK` change that.
- **Simple vs scalable:** linear blocking code is easy; high concurrency favors [[non-blocking]] + [[Epoll]].

## Technical Details
When a [[Thread]] invokes a **blocking** [[system call]] such as `read()` on an empty pipe or `accept()` with no connection, the kernel marks the thread blocked, schedules another runnable thread, and later wakes the caller when data arrives (or a signal interrupts).

| Mode | If data not ready | Thread state |
|------|-------------------|--------------|
| Blocking (default) | Waits inside kernel | Blocked → [[context switching]] |
| [[non-blocking]] | Returns immediately with `EAGAIN` | Stays runnable |

### Common blocking points

- Disk and network I/O waiting on media or peer
- `pthread_mutex_lock` when the lock is held
- `futex` waits inside glibc mutexes ([[mutexes]])
- `poll()` / `select()` without timeout

## Real-World Applications
Small servers and batch jobs size a [[thread pool]] to concurrent blocking operations. Large connection counts move accept loops to non-blocking reactors and keep blocking work (disk, DB drivers) in worker pools.

## Pros/Cons or Trade-offs
- **Pro:** Sequential code mirrors the workflow; error handling is straightforward return codes.
- **Con:** Thread count grows with idle waiters — stack memory and scheduler pressure.
- **When fine:** workers ≈ concurrent operations.
- **When hurts:** one thread must multiplex many connections.

## Comparison
- vs [[non-blocking]]: non-blocking returns immediately; you wait in an event loop instead of the kernel sleep path.
- Side-by-side table and hybrids: [[Blocking Vs Non-Blocking]].

## Mistakes to Avoid
- Assuming “async language” means no blocking below — a sync DB driver still blocks the OS thread.
- Spawning one thread per connection without measuring stack and context-switch cost.
- Holding locks across blocking I/O — amplifies contention and deadlock risk.
