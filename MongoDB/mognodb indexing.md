[[MongoDB]] [[mongosh query]] [[mongodb schema]] [[mongodb sharding]]

# mognodb indexing

> Indexes make MongoDB finds fast — without them, every query is a collection scan.





## Interview Relevance
Index interviews check compound key order, ESR rule, covered queries, and when indexes hurt writes.

## Sources
- [MongoDB Manual](https://www.mongodb.com/docs/manual/) — deep-dive
- [MongoDB Docs home](https://www.mongodb.com/docs/) — overview

## Key Concepts
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

## Technical Details
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

## Pros/Cons or Trade-offs
- **Tiny collections** — scan is fine.
- **Fields never queried** — don’t index “just in case.”

## Mistakes to Avoid
> [!WARNING]
> **Left-prefix rule** — `{a:1,b:1}` helps `{a}` and `{a,b}`, not `{b}` alone.

> [!WARNING]
> **Indexes aren’t free** — each slows inserts/updates and uses RAM/disk.

| Symptom | Check | Fix |
|---------|-------|-----|
| Slow query | `explain` → COLLSCAN | Add matching index |
| Write latency up | Too many indexes | Drop unused (`$indexStats`) |
| Unique violation | Dup keys | Clean data; fix app |
| Sort in memory | No index for sort | Extend compound index |
