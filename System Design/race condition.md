[[System Design]] [[Concurrency]] [[Concurrent modification]] [[backpressure]]

# race condition

> Race condition — result depends on who wins the timing; two actors touch shared state without a safe order.

---

## Mental model

**Say it in one breath:** Unwanted concurrency — e.g. Node `data` events fire again before your async handler finished, so byte order / state machine corrupts.

```txt
Handler A still running ──┐
                          ├─ shared buffer / DB row
Next event starts ────────┘
```

| Domain | Classic race |
|--------|----------------|
| Streams | Process chunk N+1 before N finishes |
| HTTP | Double-submit creates two orders |
| Threads | Read-modify-write without lock/CAS |

---

## Standard config / commands

```js
// Node streams: pause until async work done
stream.on('data', async (chunk) => {
  stream.pause()
  try {
    await handle(chunk)
  } finally {
    stream.resume()
  }
})
// Or use for-await-of / pipeline with backpressure
```

```sql
-- DB: optimistic lock
UPDATE accounts SET bal = bal - 10, version = version + 1
WHERE id = $1 AND version = $2;
```

| Tool | Role |
|------|------|
| Mutex / channel | Exclusive critical section |
| Idempotency key | Safe retries |
| Queue + single consumer | Serialize work |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Intermittent wrong totals | No version/lock | Optimistic lock or transaction |
| Duplicate orders | Double click / retry | Idempotency key unique constraint |
| Corrupted binary stream | Async without pause | Pause/resume or serial pipeline |
| Heisenbug under load | Stress test + TSAN/race detector | Reproduce with parallel hammer |
| Lost updates in cache | GET-modify-SET | Lua/WATCH or singleflight |

---

## Gotchas

> [!WARNING]
> **`await` in an event handler does not block the emitter** — you must pause or use a serial async queue.

> [!WARNING]
> **Tests on one core hide races** — CI with load / race detectors.

> [!WARNING]
> **“It rarely happens”** — still a Sev-1 waiting for Black Friday.

---

## When NOT to use

- **Truly immutable / pure functions** — no shared mutable state → no race.
- **Single-threaded synchronized queues** — already serialized (still watch async escapes).
- **Over-locking everything** — prefer immutability / partitioning before coarse locks.

---

## Related

[[Concurrency]] [[Concurrent modification]] [[critical sections]] [[backpressure]] [[semaphores]]
