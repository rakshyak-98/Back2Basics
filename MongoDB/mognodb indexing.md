[[MongoDB]] [[mongosh query]] [[mongodb schema]]

# mognodb indexing

> Indexes make MongoDB finds fast — without them, every query is a collection scan.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Build indexes that match filter + sort order; each index speeds reads and slows writes.

```txt
Query {a:1,b:2} sort {c:1}  →  compound index {a:1,b:1,c:1}
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Single / compound** | One field vs several | “Equality fields first, then sort.” |
| **ESR** | Equality → Sort → Range | “Order keys that way.” |
| **IXSCAN vs COLLSCAN** | Index vs full scan | “explain() tells you.” |
| **TTL / text / 2dsphere** | Special indexes | “Expiry, search, geo.” |

---

## Standard config / commands

```js
db.users.createIndex({ email: 1 }, { unique: true })
db.users.createIndex({ name: 1, age: -1 })
db.places.createIndex({ loc: '2dsphere' })
db.articles.createIndex({ body: 'text' })
db.users.createIndex({ user_id: 'hashed' }) // shard key friendly

db.users.find({ email: 'a@b.c' }).explain('executionStats')
```

| Knob | Why it matters |
|------|----------------|
| Unique | Enforce invariants |
| Partial filter | Smaller index |
| Background (legacy) | Prefer rolling builds on replica set |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Slow query | `explain` → COLLSCAN | Add matching index |
| Write latency up | Too many indexes | Drop unused (`$indexStats`) |
| Unique violation | Dup keys | Clean data; fix app |
| Sort in memory | No index for sort | Extend compound index |

---

## Gotchas

> [!WARNING]
> **Left-prefix rule** — `{a:1,b:1}` helps `{a}` and `{a,b}`, not `{b}` alone.

> [!WARNING]
> **Indexes aren’t free** — each slows inserts/updates and uses RAM/disk.

---

## When NOT to use

- **Tiny collections** — scan is fine.
- **Fields never queried** — don’t index “just in case.”

## Related

[[mongosh query]] [[mongodb schema]] [[mongodb sharding]]
