[[Operating System]] [[multi-threaded]] [[Thread]] [[non-blocking]] [[Blocking]] [[mutexes]] [[Stack Frame]] [[context switching]] [[Epoll]]

# Single-threaded

> A single-threaded program has one call stack and one scheduler entity — concurrency must come from non-blocking I/O, events, or external processes, not sibling threads.





## Interview Relevance
Explain how Redis/Node-style designs stay correct without locks, and what breaks when one CPU-bound loop stalls the whole process.

## Sources
- [Wikipedia — Thread (computing)](https://en.wikipedia.org/wiki/Thread_(computing)) — overview
- Node.js documentation — event loop model — overview

## Key Concepts
- **One stack / one OS thread:** no in-process sibling [[Thread]]s for app logic.
- **Concurrency without threads:** [[non-blocking]] I/O + event loop / [[Epoll]].
- **No shared-memory races:** often no [[mutexes]] on in-process state.
- **Escape hatch:** worker processes or [[multi-threaded]] helpers for CPU/blocking work.

## Technical Details
Examples: early Node.js event loop, Redis main thread (with helper I/O threads in newer versions), many embedded firmware loops.

Advantages:

- Easier reasoning about [[Stack Frame]] and globals.
- Lower [[context switching]] than oversized thread pools.

Limits:

- One CPU-bound loop blocks everything.
- Many network clients require [[non-blocking]] / [[Epoll]].

## Real-World Applications
Redis command processing, game main loops, and UI toolkits that keep rendering on one thread while offloading work.

## Pros/Cons or Trade-offs
- **Pro:** Simpler correctness; no lock ordering bugs.
- **Con:** One slow callback stalls all clients.
- **Trade-off:** single-threaded purity vs worker threads for heavy CPU.

## Comparison
- vs [[multi-threaded]]: multiple stacks and shared heap needing synchronization.
- vs [[Blocking]]: a single thread that blocks on I/O still stalls the whole program unless the runtime uses async primitives.

## Mistakes to Avoid
- Doing heavy crypto/compression on the event-loop thread.
- Assuming “single-threaded” means “single-core forever” — runtimes may still use helper threads.
- Adding threads casually without a sync story once shared mutable state appears.
