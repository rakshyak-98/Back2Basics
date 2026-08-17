[[Operating System]] [[multi-threaded]] [[Thread]] [[CPU IO Bound Task]] [[context switching]] [[thread-safe queue]] [[mutexes]]

# Thread pool

> A thread pool keeps a fixed set of worker threads pulling tasks from a queue — amortizing create/destroy cost and bounding concurrency versus unbounded `pthread_create`.





## Interview Relevance
Pool sizing: ≈ cores for CPU-bound; more for I/O-bound until [[context switching]]/locks dominate.

## Sources
- *Java Concurrency in Practice* — thread pool sizing — deep-dive
- [Wikipedia — Thread pool](https://en.wikipedia.org/wiki/Thread_pool) — overview

## Key Concepts
- **Fixed workers + queue:** submit → [[thread-safe queue]] → idle worker runs.
- **Bound concurrency:** avoid thread explosion.
- **Sizing:** CPU-bound ≈ cores; I/O-bound ([[CPU IO Bound Task]]) may be higher.
- **Watch:** switches and [[mutexes]] contention.

## Technical Details
```txt
Submit task → queue ([[thread-safe queue]]) → idle worker runs → repeat
```

Used in Java `ExecutorService`, Go worker pools, nginx optional thread modules, and many app servers ([[multi-threaded]]).

## Real-World Applications
Request handlers, background job runners, and offloading blocking work from event loops.

## Pros/Cons or Trade-offs
- **Pro:** Reuse threads; predictable memory/concurrency.
- **Con:** Queue latency under overload; deadlocks if tasks block on the pool.
- **Trade-off:** abort/reject vs unbounded queue growth.

## Comparison
- vs thread-per-request: bounded vs unbounded concurrency.
- vs pure event loop: pools help blocking/CPU slices the loop cannot run.

## Mistakes to Avoid
- Unbounded queues that OOM under load.
- Running tasks that wait on the same pool (pool deadlock).
- Sizing only from core count for heavily I/O-bound work without measuring.
