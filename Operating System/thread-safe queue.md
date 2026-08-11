[[Operating System]] [[multi-threaded]] [[thread pool]] [[atomic ring buffer]]

# Thread-safe queue

> A queue you can push/pop from many threads safely — locking or lock-free sync is built in.

---

## Mental model

**Say it in one breath:** Producers enqueue work; consumers dequeue; mutex+condition (or lock-free) keep structure and waiting correct.

```txt
producers ──put──► [ thread-safe queue ] ──get──► workers
                     │
                     └─ block / timeout / drop when full
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Thread-safe queue** | Concurrent queue ADT | “No external lock around every put/get.” |
| **Blocking queue** | Wait when empty/full | “Backpressure without busy spin.” |
| **Bounded** | Fixed capacity | “Protects memory under overload.” |
| **Condition variable** | Sleep until signal | “Wait for ‘not empty’ / ‘not full’.” |
| **Poison pill** | Sentinel to stop workers | “Enqueue shutdown marker once.” |
| **MPMC** | Many producers/consumers | “Default server work-queue shape.” |

### How the story goes

1. **Create** — bound size + policy (block versus throw).
2. **Produce** — `put` waits or fails if full.
3. **Consume** — `get` waits if empty.
4. **Shutdown** — poison pills or `close()` that wakes waiters.

---

## Standard config / commands

```python
from queue import Queue
q = Queue(maxsize=1000)   # bounded + blocking
q.put(item, timeout=1)
item = q.get(timeout=1)
q.task_done()
q.join()
```

```go
ch := make(chan Job, 1024) // bounded channel as queue
ch <- job
job := <-ch
close(ch)
```

| Knob | Why it matters |
|------|----------------|
| `maxsize` / buffer | Memory + backpressure |
| Timeout vs forever | Avoid stuck shutdown |
| Fairness | Starvation under many waiters |
| Separate hi/lo queues | Priority without one giant lock |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Threads stuck | Full queue + all workers blocked on put | Bound vs unbounded; more workers; drop policy |
| Lost tasks on exit | No drain / join | `join` / wait groups; poison pills |
| Latency spikes | Coarse lock / huge critical section | Smaller critical; shard queues |
| OOM | Unbounded queue | Cap size; load-shed |
| Duplicate processing | At-least-once + crash | Idempotent handlers |
| Deadlock with other locks | Lock order with queue mutex | Never hold app locks while blocking on queue |

---

## Gotchas

> [!WARNING]
> **“Queue” without bound** — hides overload until RAM dies.

> [!WARNING]
> **`task_done` forgotten** — `join()` hangs forever (Python).

> [!WARNING]
> **Lock-free ≠ wait-free** — CAS loops can still livelock under contention.

> [!WARNING]
> **Closing** — define once-close semantics; double-close panics in Go channels.

---

## When NOT to use

- **Single thread** — plain `collections.deque` / slice; no sync tax.
- **Huge payloads by value** — queue pointers/arenas; avoid copies.
- **Cross-machine** — use a broker (Kafka/SQS), not an in-process queue.

---

## Related

[[thread pool]] [[multi-threaded]] [[atomic ring buffer]] [[semaphores]] [[mutexes]] [[critical sections]]
