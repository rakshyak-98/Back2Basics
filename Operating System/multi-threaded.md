[[Operating System]] [[Single-threaded]] [[Thread]] [[thread pool]] [[mutexes]] [[context switching]] [[Inter Process Communication]] [[Stack Frame]] [[Heap memory]] [[file descriptors]] [[critical sections]] [[CPU IO Bound Task]] [[Single Instruction, Multiple Data (SIMD)]] [[non-blocking]]

# Multi-threaded

> A multi-threaded program runs several threads in one process sharing address space and file descriptors — parallelism without [[Inter Process Communication]] for every byte.

```txt
        Multi-threaded ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** When threads beat processes, what is shared vs private, and how locks/races s…

## Sources
- Herlihy & Shavit, *The Art of Multiprocessor Programming* — deep-dive
- Silberschatz — threads chapter — deep-dive
- [Wikipedia — Thread (computing)](https://en.wikipedia.org/wiki/Thread_(computing)) — overview

## Key Concepts
- **Shared:** [[Heap memory]], open [[file descriptors]].
- **Private:** stack ([[Stack Frame]]), registers, TLS.
- **Scheduling:** independent [[context switching]] per [[Thread]].
- **Sync tax:** [[critical sections]] and [[mutexes]].

## Technical Details
- Helps with:

- Parallel CPU work on multiple cores ([[Single Instruction, Multiple Data (SIM…
- [[CPU IO Bound Task]] — one thread blocks while others run.
- Structured servers via [[thread pool]].

- Costs: contention, races, deadlocks

- Versus [[Single-threaded]] event loops: fewer locks, must use [[non-blocking]…

## Mistakes to Avoid
- **Mistake:** Unbounded thread-per-request
- **Mistake:** Sharing mutable state without synchronization
- **Mistake:** Ignoring lock contention while adding more threads

## Pros/Cons or Trade-offs
- **Pro:** Uses multiple cores; shared memory is fast.
- **Con:** Harder correctness; stack memory × thread count.
- **Trade-off:** threads vs processes vs async event loops.

## Comparison
- vs [[Single-threaded]]: concurrency without shared-heap races.
- vs multi-process: stronger isolation, heavier IPC.


### Use cases
- App servers, parallel compressors, and UI apps with background workers.
