[[Operating System]] [[multi-threaded]] [[Single-threaded]] [[context switching]] [[mutexes]] [[process]] [[semaphores]] [[Heap memory]] [[thread pool]]

# Thread

> A thread is the unit of CPU scheduling inside a [[process]] — own stack and registers, shared address space and file descriptors with siblings.

```txt
        Thread ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Core OS question: process vs thread, what is shared vs private, and how races…

## Sources
- Silberschatz — threads and concurrency — deep-dive
- Linux `pthread(7)`, `clone(2)` manual pages — deep-dive
- [Wikipedia — Thread (computing)](https://en.wikipedia.org/wiki/Thread_(computing)) — overview

## Key Concepts
- **Schedulable entity:** kernel assigns threads to cores.
- **Shared:** address space, fds, signal dispositions (mostly).
- **Private:** stack, registers, thread-local storage.
- **Creation:** `pthread_create`, `clone`, or language runtimes (JVM threads, Go Ms).

## Technical Details
- The kernel scheduler runs threads and performs [[context switching]] when blo…

- Synchronize shared mutable state with [[mutexes]], [[semaphores]], or atomics

- Pools of workers: [[thread pool]].
- Contrasts: [[Single-threaded]], [[multi-threaded]].

## Mistakes to Avoid
- **Mistake:** Sharing mutable heap without synchronization
- **Mistake:** Creating unbounded threads per request
- **Mistake:** Ignoring stack size × thread count under memory limits

## Pros/Cons or Trade-offs
- **Pro:** Overlap I/O and CPU; use multiple cores in one process.
- **Con:** Races, deadlocks, stack memory per thread.
- **Trade-off:** many threads vs event-driven fewer threads.

## Comparison
- vs [[process]]: processes isolate memory; threads share it.
- vs green threads/goroutines: user-space tasks multiplexed onto OS threads.


### Use cases
- Web servers (one request per worker thread), parallel compute, and UI toolkit…
