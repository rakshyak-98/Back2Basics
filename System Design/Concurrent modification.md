[[System Design]] [[race condition]] [[Eventual consistency]] [[IDOR]] [[ETAG or IF MATCH]] [[critical sections]]

# Concurrent modification

> Concurrent modification — two writers read-modify-write the same record; last write wins unless you version or lock.

## Interview Relevance

Optimistic concurrency (`version`/`If-Match`), lost updates, and when to serialize vs CRDT/append-only.

## Sources

- [Wikipedia — Optimistic concurrency control](https://en.wikipedia.org/wiki/Optimistic_concurrency_control) — overview
- Kleppmann, *Designing Data-Intensive Applications* — concurrency — deep-dive

## Key Concepts

- **Lost update:** both read v1; second write clobbers first.
- **Optimistic:** conditional update on version/ETag.
- **Pessimistic:** `SELECT … FOR UPDATE`.
- **Alternatives:** PATCH/CRDT, single-writer queue, immutable versions.

## Technical Details

```txt
A reads v1 ──edit──► writes v1'
B reads v1 ──edit──► writes v1''  (A’s change lost)
```

```sql
UPDATE tickets
SET status = 'closed', version = version + 1
WHERE id = $1 AND version = $2;
-- 0 rows → conflict → reload & retry
```

```http
If-Match: "etag-88"
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Silent lost updates | No version | Optimistic concurrency |
| Frequent 409 | Hot row | Smaller critical section; queue |
| Skipped workflow state | Check-then-act | One conditional transition |
| Blind PUT JSON | Whole replace | PATCH + ETag |

## Real-World Applications

Ticket systems, document editors, and inventory reservations.

## Pros/Cons or Trade-offs

- **Optimistic:** high throughput; retries under contention.
- **Pessimistic:** simpler conflicts; lock hold kills throughput.
- **Trade-off:** edit-in-place vs append-only event log.

## Comparison

- vs [[race condition]]: race is the general hazard; this is the RMW data pattern.
- vs [[Eventual consistency]]: eventual replicas need merge policies for concurrent writes.

## Mistakes to Avoid

- `read → app logic → write` with no version.
- Long-held DB locks.
- Weak ETags on the wrong representation.
