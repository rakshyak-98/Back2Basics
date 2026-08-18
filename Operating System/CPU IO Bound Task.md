[[Operating System]] [[thread pool]] [[Blocking]] [[multi-threaded]]

# CPU IO Bound Task

> CPU-bound burns cores on compute; I/O-bound spends time waiting on disk, network, or users.

## Mental model

**Say it in one breath:** Match concurrency tool to the bottleneck — processes/SIMD for CPU; threads/async for waits.

```txt
CPU-bound:  encode / hash / ML  →  needs cores (multiprocess)
IO-bound:   HTTP / DB / disk    →  needs concurrency while waiting
```

| Aspect | CPU-bound | I/O-bound |
| --- | --- | --- |
| Bottleneck | ALU / cache | Wait time |
| Threads help? | Little (GIL/contended) | Yes |
| Processes help? | Yes | Sometimes overkill |
| Async helps? | Rarely | Often |

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **CPU-bound** | Compute limited | “More cores or better algo.” |
| --- | --- | --- |
| **I/O-bound** | Wait limited | “Overlap waits with concurrency.” |
| **GIL** | Python one-bytecode-thread | “Threads won’t speed CPU Python.” |
| **Backpressure** | Slow consumers | “Bound queues or you OOM.” |
| **Pool split** | Separate executors | “Don’t mix encode + HTTP in one pool.” |
| **Amdahl** | Serial fraction | “8 cores ≠ 8× if 30% serial.” |

### How the story goes

1. **Measure** — CPU% high versus mostly idle/`epoll_wait`.
2. **Classify** — CPU versus I/O versus both.
3. **Pick** — process pool / C extension versus async/thread pool.
4. **Isolate** — never let CPU hogs occupy the I/O worker pool.

## Standard config / commands

```bash
# See wait vs run
pidstat -u -d 1
perf top
# Python patterns
# concurrent.futures.ProcessPoolExecutor  → CPU
# asyncio + httpx / ThreadPoolExecutor    → I/O
```

| Knob | Why it matters |

| Pool size ≈ cores | CPU workers |
| --- | --- |
| Pool size ≫ cores | I/O workers (cap!) |
| Queue maxsize | Protect memory |
| cgroup CPU quota | Noisy neighbor |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Latency↑ under “light” CPU job | Shared thread pool | Split CPU vs I/O executors |
| 100% one core, Python | GIL + threads | Processes or native code |
| Idle CPUs, slow API | Blocking I/O on event loop | Async drivers or worker threads |
| OOM with “more threads” | Unbounded queue | Bound + reject |
| No speedup after N cores | Amdahl / memory BW | Profile; reduce sharing |
| DB pool exhausted | I/O workers > DB conns | Align pool sizes |

## Gotchas

> [!WARNING]
> **Mixing pools** — one JPEG encode can stall hundreds of waiting HTTP handlers.

> [!WARNING]
> **“Async CPU”** — `await` doesn’t parallelize math; it only yields.

> [!WARNING]
> **Hyper-threading** — logical CPUs ≠ full speedup ([[SMT threads]]).

> [!WARNING]
> **I/O looks CPU** — JSON parse / compression after download is CPU-bound.

## When NOT to use

- **Tiny total work** — thread/process spawn costs dominate; do it inline.
- **Already one bottleneck service** — fix the DB/index before fan-out workers.
- **Real-time hard deadlines** — need scheduling class / isolation, not just “more async”.

## Related

[[thread pool]] [[Blocking]] [[non-blocking]] [[multi-threaded]] [[SMT threads]] [[Single-threaded]]
