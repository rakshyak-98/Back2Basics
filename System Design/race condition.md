[[Concurrent modification]] [[backpressure]] [[Concurrent modification]] [[Distributed computing]]

# race condition

> A race condition occurs when the outcome depends on the interleaving of concurrent operations on shared mutable state — without synchronization, order is undefined and bugs are intermittent.





## Interview Relevance
Interleaving hazard; TOCTOU; fixes via atomics/locks/queues — and tests that catch it.

## Sources
- Herlihy & Shavit, *The Art of Multiprocessor Programming* — overview
- Go documentation — `-race` detector — overview
- Martin Kleppmann, *Designing Data-Intensive Applications* — concurrency and transactions — deep-dive

## Key Concepts
- **Outcome depends on interleaving** of concurrent operations.
- **TOCTOU:** check then act without atomicity.
- **Fixes:** locks, atomics, queues, DB constraints, CAS.
- **Tests:** stress/concurrency tests; not only happy path.

## Technical Details
### Where races appear

```txt
Handler A still running ──┐
                          ├─ shared buffer / database row / cache key
Handler B starts ─────────┘
```

| Domain | Classic race |
|--------|--------------|
| Event streams | Process chunk N+1 before N finishes |
| HTTP | Double-submit creates two orders |
| Threads | Read-modify-write without lock or compare-and-swap |
| Distributed | Two replicas write conflicting versions ([[Eventual consistency]]) |

### Mitigations

```javascript
// Node.js streams: pause until async work completes
stream.on('data', async (chunk) => {
  stream.pause()
  try {
    await handle(chunk)
  } finally {
    stream.resume()
  }
})
```

```sql
UPDATE accounts
SET balance = balance - 10, version = version + 1
WHERE id = $1 AND version = $2;
-- rows affected 0 → optimistic conflict, retry or fail
```

| Tool | Role |
|------|------|
| Mutex / channel | Exclusive critical section |
| Idempotency key | Safe retries without duplicate side effects |
| Single-consumer queue | Serialize work per entity |
| Compare-and-swap / version column | Detect lost updates ([[Concurrent modification]]) |
| Database transaction | Atomic multi-row updates on one node |

### Debugging intermittent failures

| Symptom | Direction |
|---------|-----------|
| Wrong totals under load | Missing version or transaction |
| Duplicate orders | Double click or retry without idempotency |
| Corrupted stream | Async handler without [[backpressure]] pause |
| Heisenbug | Stress test; Go race detector; ThreadSanitizer |

**Check-then-act** outside a transaction is almost always a race: `if balance >= 10 then deduct` — two threads both pass the check.

## Real-World Applications
Shared counters, checkout inventory, and multi-threaded caches.

## Pros/Cons or Trade-offs
- **Pro of awareness:** prevents Heisenbugs in prod.
- **Con:** Over-locking kills throughput.
- **Trade-off:** coarse locks vs careful lock-free designs.

## Comparison
- vs [[Concurrent modification]]: RMW lost updates are a common race class.
- vs [[critical sections]]: critical sections are how you eliminate races on shared data.

## Mistakes to Avoid
- Skipping failure modes until production.
- Ignoring idempotency, timeouts, or rollback where required.
- Optimizing or distributing before measuring the real bottleneck.
