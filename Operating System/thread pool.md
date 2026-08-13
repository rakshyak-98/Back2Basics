[[Operating System]] [[multi-threaded]] [[Thread]] [[CPU IO Bound Task]] [[context switching]] [[thread-safe queue]]

# Thread pool

> A thread pool keeps a fixed set of worker threads pulling tasks from a queue — amortizing thread creation cost and bounding concurrency versus unbounded `pthread_create`.

Pattern:

```txt
Submit task → queue ([[thread-safe queue]]) → idle worker runs → repeat
```

Size for **CPU-bound** work ≈ core count; **I/O-bound** ([[CPU IO Bound Task]]) may use more workers but watch [[context switching]] and lock contention ([[mutexes]]).

Used in Java `ExecutorService`, Go worker pools, nginx optional thread module.

## Sources

- Java Concurrency in Practice — thread pool sizing
- Wikipedia: [Thread pool](https://en.wikipedia.org/wiki/Thread_pool)
