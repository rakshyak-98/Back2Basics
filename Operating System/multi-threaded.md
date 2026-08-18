[[Operating System]] [[Single-threaded]] [[Thread]] [[thread pool]] [[mutexes]] [[critical sections]] [[context switching]]

# multi-threaded

> Multi-threaded means one process runs several threads that share memory — use more cores, overlap I/O, and pay for synchronization.

## Mental model

**Say it in one breath:** Threads share the heap and FDs; each has its own stack and register state — so you can parallelize CPU work if you protect shared writes.

```txt
Process
├─ Thread 1  stack + regs  ─┐
├─ Thread 2  stack + regs  ─┼─ shared: heap, globals, fd table
└─ Thread 3  stack + regs  ─┘
         │
         └─ scheduler → cores (true parallel) or time-slices
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Thread** | Schedulable unit inside a process | “Cheaper than a process; shares address space.” |
| --- | --- | --- |
| **Shared memory** | Heap/globals visible to all threads | “That’s why races appear — and why locks exist.” |
| **Parallel vs concurrent** | Parallel = same time on cores; concurrent = interleaved | “I need multiple cores for CPU speedup.” |
| **Context switch** | Save/restore thread state | “Too many threads → switch overhead dominates.” |
| **Race / deadlock** | Timing bugs / circular waits | “Correctness tax of shared mutable state.” |
| **Thread pool** | Reuse workers | “Don’t spawn unbounded threads per request.” |

### How the story goes (4 steps)

1. **Spawn** — create threads (or hand work to a [[thread pool]]).
2. **Share carefully** — mark immutable data; guard mutable with [[mutexes]] / atomics.
3. **Run** — CPU-bound work scales with cores; I/O-bound needs enough waiters, not infinite threads.
4. **Join / shut down** — drain queues; avoid leaking threads and locks.

## Standard config / commands

```bash
# How many OS threads is this process using?
ps -L -p <pid> | wc -l
ls /proc/<pid>/task | wc -l

# See runnable vs blocked
top -H -p <pid>
perf top -p <pid>

# Go
GOMAXPROCS=$(nproc)   # default ≈ CPU count
```

```java
// Java — bounded pool beats unbounded new Thread()
ExecutorService pool = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());
```

| Knob | Why it matters |

| Thread count | Rule of thumb: ~cores for CPU-bound; higher for blocking I/O |
| --- | --- |
| Stack size | Each thread costs stack (MBs add up) |
| Pool queue | Unbounded queue → latent OOM under overload |
| Affinity / cgroup CPU | Containers may have fewer cores than `nproc` on host |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Corrupt state | Shared writes without locks | Add critical sections; prefer immutability |
| Hang | `thread apply all bt` / deadlock | Fix lock order; timeouts |
| High load, low throughput | Too many threads / contention | Cap pool; profile locks |
| Works until traffic spike | Unbounded `new Thread` | [[thread pool]] + backpressure |
| Latency spikes | GC + thread storms | Bound concurrency; size heaps |

## Gotchas

> [!WARNING]
> **More threads ≠ more speed.** Past core count on CPU-bound work you pay [[context switching]] and cache thrash.

> [!WARNING]
> **Language “threads” may be green.** Go goroutines and Java virtual threads still need care with blocking native calls.

> [!WARNING]
> **Fork + threads** — only the forking thread survives in the child; locks held by others stay stuck. Prefer fork-before-thread or `posix_spawn`.

> [!WARNING]
> **UI / request thread blocked** — one long critical section freezes the whole user-visible path.

## When NOT to use

- **Simple I/O servers with an event loop** — [[Single-threaded]] + non-blocking I/O often wins for connection count.
- **Embarrassingly isolated jobs** — prefer processes / separate pods for blast-radius isolation.
- **Tiny scripts** — threading overhead and races are not worth it.

## Related

[[Single-threaded]] [[Thread]] [[thread pool]] [[mutexes]] [[critical sections]] [[semaphores]] [[context switching]] [[CPU IO Bound Task]] [[SMT threads]]
