[[Operating System]] [[multi-threaded]] [[Thread]] [[thread-safe queue]] [[mutexes]] [[CPU IO Bound Task]]

# thread pool

> A thread pool keeps N reusable workers and a queue — submit tasks instead of spawning a new thread every time.

## Mental model

**Say it in one breath:** Create workers once, park idle ones, hand them jobs from a queue — you cap concurrency and skip thread create/destroy cost.

```txt
  submit(task) → [ queue ] → worker-1 … worker-N → result / callback
                     ▲                │
                     └──── idle ←─────┘
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Worker** | Thread that runs tasks | “Fixed workers pull from the queue.” |
| --- | --- | --- |
| **Queue** | Pending work buffer | “Backpressure lives here — bounded vs unbounded.” |
| **Pool size** | Max concurrent threads | “Size to cores for CPU; higher if tasks block.” |
| **Rejection policy** | What if queue is full | “Caller runs, drops, or blocks — pick explicitly.” |
| **Thread churn** | Create/destroy per job | “Pools exist to kill churn under load.” |
| **Saturation** | All workers busy + queue full | “That’s your load-shed moment.” |

### Why pools exist

| Without a pool | With a pool |

| Thread create/destroy cost per task | Amortized over many tasks |
| --- | --- |
| Unbounded threads under spike | Hard cap on concurrency |
| Latency from cold starts | Warm idle workers |
| Easy to fork-bomb yourself | Controlled resource use |

### How the story goes (4 steps)

1. **Size** — pick N (cores for CPU-bound; measure for blocking I/O).
2. **Queue** — bound the queue; define reject/block behavior.
3. **Run** — workers loop: dequeue → execute → repeat.
4. **Shutdown** — stop intake, drain or cancel, join workers.

## Standard config / commands

```java
ThreadPoolExecutor exec = new ThreadPoolExecutor(
  4, 4,                 // core, max
  60L, TimeUnit.SECONDS,
  new ArrayBlockingQueue<>(1000),
  new ThreadPoolExecutor.CallerRunsPolicy()  // backpressure
);
```

```go
// Semaphore-as-pool
sem := make(chan struct{}, 8)
sem <- struct{}{}
go func() {
  defer func() { <-sem }()
  doWork()
}()
```

```bash
# Is the pool too big?
ps -L -p <pid> | wc -l
# Queue depth — app metrics (expose it!)
```

| Knob | Why it matters |

| Core / max threads | Elastic pools hide overload until memory dies |
| --- | --- |
| Queue capacity | Unbounded queue = latent OOM |
| Keep-alive | Trims idle threads in elastic pools |
| `CallerRunsPolicy` | Slows the producer — natural backpressure |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Latency climbs, CPU idle | Workers blocked on I/O/locks | More workers **or** non-blocking I/O |
| OOM / huge RSS | Unbounded queue of tasks | Bound queue; reject; load-shed |
| Tasks never run | Deadlock: task waits on pool result from same pool | Separate pools or async handoff |
| Spike creates thousands of threads | Not using a pool | Cap with pool / semaphore |
| Shutdown hangs | Tasks ignore interrupt | Cooperative cancel; timed `awaitTermination` |

## Gotchas

> [!WARNING]
> **Unbounded queue + fixed threads** looks “fine” until heap holds millions of pending jobs.

> [!WARNING]
> **Pool sized to host `nproc` inside a 2-CPU cgroup** oversubscribe — read container limits.

> [!WARNING]
> **Running pool tasks that submit to the same pool and wait** is a classic self-deadlock.

> [!WARNING]
> **ThreadLocal / request context** must be cleared between tasks or you leak identity across requests.

## When NOT to use

- **One background job at startup** — a single thread or `async` task is enough.
- **True parallel CPU across machines** — use a job queue + workers fleet, not one process pool.
- **Hard real-time** — pools add queueing jitter; use dedicated threads with known budgets.

## Related

[[multi-threaded]] [[Thread]] [[thread-safe queue]] [[mutexes]] [[semaphores]] [[CPU IO Bound Task]] [[context switching]] [[Single-threaded]]
