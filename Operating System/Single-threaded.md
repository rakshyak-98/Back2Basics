[[Operating System]] [[multi-threaded]] [[Thread]] [[non-blocking]] [[Blocking]]

# Single-threaded

> A single-threaded program has one call stack and one scheduler entity — concurrency must come from non-blocking I/O, events, or external processes, not sibling threads.

Examples: early Node.js event loop, Redis main thread (with helper I/O threads in newer versions), many embedded firmware loops.

## Advantages

- No [[mutexes]] on shared in-process state.
- Easier reasoning about [[Stack Frame]] and globals.
- Lower [[context switching]] than oversized thread pools.

## Limits

- One CPU-bound loop blocks everything — offload CPU work or use [[multi-threaded]] workers.
- Must use [[non-blocking]] / [[Epoll]] for many network clients.

## Sources

- Wikipedia: [Thread (computing)](https://en.wikipedia.org/wiki/Thread_(computing))
- Node.js documentation — event loop model
