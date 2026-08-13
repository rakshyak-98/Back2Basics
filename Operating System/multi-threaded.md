[[Operating System]] [[Single-threaded]] [[Thread]] [[thread pool]] [[mutexes]] [[context switching]]

# Multi-threaded

> A multi-threaded program runs several threads of control in one process sharing address space and file descriptors — parallelism without separate [[Inter Process Communication]] for every byte.

Each [[Thread]] has its own stack ([[Stack Frame]]) but shares [[Heap memory]] and open [[file descriptors]]. The kernel schedules threads independently → [[context switching]].

## When multi-threading helps

- Parallel CPU work on multiple cores ([[Single Instruction, Multiple Data (SIMD)]] is orthogonal — data parallelism inside one thread).
- [[CPU IO Bound Task]] workloads — one thread blocks on I/O while others run.
- Structured servers using [[thread pool]].

## Costs

- [[critical sections]] and [[mutexes]] — contention serializes work.
- Harder debugging — [[Stack trace]] per thread, races, deadlocks.

Versus [[Single-threaded]] event loops: fewer locks, must use [[non-blocking]] I/O for concurrency.

## Sources

- Herlihy & Shavit, *The Art of Multiprocessor Programming*
- Silberschatz — threads chapter
- Wikipedia: [Thread (computing)](https://en.wikipedia.org/wiki/Thread_(computing))
