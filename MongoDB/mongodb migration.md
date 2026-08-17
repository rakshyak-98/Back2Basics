[[MongoDB]] [[mongodb schema]] [[MongoDB query validation]] [[mongosh]]

# mongodb migration

> MongoDB migrations are scripts that reshape documents — run carefully in batches with a rollback story.

```txt
        mongodb migration ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Migration reviews cover schema evolution without downtime

## Sources
- [MongoDB Manual](https://www.mongodb.com/docs/manual/) — deep-dive
- [MongoDB Docs home](https://www.mongodb.com/docs/) — overview

## Key Concepts
```txt
- **Note:** 1 deploy dual-read/write → 2 migrate docs → 3 remove old path
```

### Review map (words you can say)

| Word | Plain meaning | Say in review |
|------|---------------|------------------|
| **Expand/contract** | Dual support then cleanup | “Never require one deploy + full rewrite.” |
| **Batch cursor** | Migrate in chunks | “Avoid multi-hour locks / OOM.” |
| **migrate-mongo** | Versioned migration files | “Like Flyway for Mongo.” |
| **Idempotent migrate** | Safe re-run | “Skip already-migrated docs.” |

## Technical Details
```js
// batch rename field
const cursor = db.users.find({ newEmail: { $exists: false }, email: { $exists: true } }).limit(1000)
while (await cursor.hasNext()) {
  const doc = await cursor.next()
  await db.users.updateOne({ _id: doc._id }, { $rename: { email: 'newEmail' } })
}
```

```bash
npx migrate-mongo up
npx migrate-mongo status
```

| Knob | Why it matters |
|------|----------------|
| Batch size | Memory + oplog pressure |
| Idempotent filter | `$exists` / version field |
| Index before filter | Migration scan speed |

## Mistakes to Avoid
> [!WARNING]
> **`save` in a loop** — prefer `updateOne`/`bulkWrite`; `save` is easy to get wrong.

> [!WARNING]
> **No downtime plan** — changing required validators before backfill rejects writes.

| Symptom | Check | Fix |
|---------|-------|-----|
| Migration OOM | Unbounded `find()` | Cursor + limit batches |
| Half-migrated prod | Crash mid-run | Idempotent resume |
| App breaks mid-cutover | Only new field | Dual-read until done |
| Secondary lag | Huge writes | Throttle batches |

## Pros/Cons or Trade-offs
- **One-off analytics reshape** — aggregation `$out` may be enough.
- **Schema still unstable weekly** — stabilize product first.
