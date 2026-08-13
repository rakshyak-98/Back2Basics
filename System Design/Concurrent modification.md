<!-- note-strategy: operational -->
[[System Design]] [[race condition]] [[Eventual consistency]] [[IDOR]]

# Concurrent modification

> Concurrent modification — two writers read-modify-write the same record; last write wins unless you version or lock.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Gap between read and write lets another actor sneak in — status machines, counters, and document edits are classic victims.

```txt
A reads v1 ──edit──► writes v1'
B reads v1 ──edit──► writes v1''  (A’s change lost)
```

| Defense | How |
|---------|-----|
| Optimistic (`version`) | Update `WHERE version=?` |
| Pessimistic lock | `SELECT … FOR UPDATE` |
| Patch / CRDT | Merge fields |
| Queue single-thread | Serialize mutations |

---

## Standard config / commands

```sql
UPDATE tickets
SET status = 'closed', version = version + 1
WHERE id = $1 AND version = $2;
-- 0 rows → conflict → reload & retry
```

```http
If-Match: "etag-88"
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Silent lost updates | No version column | Add optimistic concurrency |
| Frequent `409` | Hot row | Smaller critical section; queue |
| Workflow skipped state | Check-then-act | Transition in one conditional update |
| API overwrites whole JSON | PUT blind | PATCH + ETag |
| Two admins clash | UX | Show conflict; merge UI |

---

## Gotchas

> [!WARNING]
> **`read → logic in app → write` without version** — distributed race by default.

> [!WARNING]
> **ETag on wrong representation** — weak validators surprise you.

> [!WARNING]
> **Locking too long** — holds kill throughput; prefer optimistic.

---

## When NOT to use

- **Append-only logs** — conflicts become new events.
- **Immutable objects** — create new versions instead of edit-in-place.
- **Single-writer partitions** — already serialized.

---

## Related

[[race condition]] [[ETAG or IF MATCH]] [[Eventual consistency]] [[critical sections]]
