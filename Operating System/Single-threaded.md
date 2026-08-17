[[Operating System]] [[multi-threaded]] [[Thread]] [[non-blocking]] [[Blocking]] [[mutexes]] [[Stack Frame]] [[context switching]] [[Epoll]]

# Single-threaded

> A single-threaded program has one call stack and one scheduler entity — concurrency must come from non-blocking I/O, events, or external processes, not sibling threads.

```txt
        Single-threaded ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Explain how Redis/Node-style designs stay correct without locks, and what bre…

## Sources
- [Wikipedia — Thread (computing)](https://en.wikipedia.org/wiki/Thread_(computing)) — overview
- Node.js documentation — event loop model — overview

## Key Concepts
- **One stack / one OS thread:** no in-process sibling [[Thread]]s for app logic.
- **Concurrency without threads:** [[non-blocking]] I/O + event loop / [[Epoll]].
- **No shared-memory races:** often no [[mutexes]] on in-process state.
- **Escape hatch:** worker processes or [[multi-threaded]] helpers for CPU/blocking work.

## Technical Details
- Examples: early Node.js event loop, Redis main thread (with helper I/O thread…

- Advantages:

- Easier reasoning about [[Stack Frame]] and globals.
- Lower [[context switching]] than oversized thread pools.

- One CPU-bound loop blocks everything.
- Many network clients require [[non-blocking]] / [[Epoll]].

## Mistakes to Avoid
- **Mistake:** Doing heavy crypto/compression on the event-loop thread
- **Mistake:** Assuming “single-threaded” means “single-core forever”
- **Mistake:** Adding threads casually without a sync story once shared mutable…

## Pros/Cons or Trade-offs
- **Pro:** Simpler correctness; no lock ordering bugs.
- **Con:** One slow callback stalls all clients.
- **Trade-off:** single-threaded purity vs worker threads for heavy CPU.

## Comparison
- vs [[multi-threaded]]: multiple stacks and shared heap needing synchronization.
- vs [[Blocking]]: a single thread that blocks on I/O still stalls the whole program unless the run…


### Use cases
- Redis command processing, game main loops, and UI toolkits that keep renderin…
