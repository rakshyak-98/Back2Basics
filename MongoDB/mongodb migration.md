<!-- note-strategy: operational -->
[[MongoDB]] [[mongodb schema]]

# mongodb migration

> MongoDB migrations are scripts that reshape documents — run carefully in batches with a rollback story.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Change the application to read both shapes, backfill, then drop the old field — expand/contract, not big-bang.

```txt
1 deploy dual-read/write → 2 migrate docs → 3 remove old path
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Expand/contract** | Dual support then cleanup | “Never require one deploy + full rewrite.” |
| **Batch cursor** | Migrate in chunks | “Avoid multi-hour locks / OOM.” |
| **migrate-mongo** | Versioned migration files | “Like Flyway for Mongo.” |
| **Idempotent migrate** | Safe re-run | “Skip already-migrated docs.” |

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Migration OOM | Unbounded `find()` | Cursor + limit batches |
| Half-migrated prod | Crash mid-run | Idempotent resume |
| App breaks mid-cutover | Only new field | Dual-read until done |
| Secondary lag | Huge writes | Throttle batches |

---

## Gotchas

> [!WARNING]
> **`save` in a loop** — prefer `updateOne`/`bulkWrite`; `save` is easy to get wrong.

> [!WARNING]
> **No downtime plan** — changing required validators before backfill rejects writes.

---

## When NOT to use

- **One-off analytics reshape** — aggregation `$out` may be enough.
- **Schema still unstable weekly** — stabilize product first.

## Related

[[mongodb schema]] [[MongoDB query validation]] [[mongosh]]
