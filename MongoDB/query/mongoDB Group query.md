[[MongoDB]] [[mongosh query]] [[query/mongodb lookup query]] [[mongodb view]]

# mongoDB Group query

> `$group` aggregates rows into buckets — sum, count, push — like SQL GROUP BY.

## Interview Relevance

Group/aggregate interviews check $group stages, accumulators, and memory limits.

## Sources

- [MongoDB Manual](https://www.mongodb.com/docs/manual/) — deep-dive
- [MongoDB Docs home](https://www.mongodb.com/docs/) — overview

## Key Concepts

```txt
$match → $group(_id, accumulators) → $sort → $project
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **`_id`** | Group key | “Null = one bucket for all.” |
| **`$sum` / `$avg`** | Accumulators | “Spend per user.” |
| **`$push` / `$addToSet`** | Collect values | “Watch memory.” |
| **allowDiskUse** | Spill to disk | “Big groups.” |

## Technical Details

```js
db.orders.aggregate([
  { $match: { status: 'paid' } },
  { $group: {
      _id: '$customerId',
      total: { $sum: '$amount' },
      n: { $sum: 1 },
  }},
  { $sort: { total: -1 } },
  { $limit: 50 },
])
```

| Knob | Why it matters |
|------|----------------|
| Early `$match` | Uses indexes; less memory |
| Compound `_id` | `{ day, country }` multi-key |
| `$project` after | Shape output |

## Pros/Cons or Trade-offs

- **Simple counts with a filter** — `countDocuments` may suffice.
- **Realtime per-request heavy groups** — precompute / rollups.

## Mistakes to Avoid

> [!WARNING]
> **`$push` entire docs** — easy OOM; push only needed fields.

> [!WARNING]
> **Grouping on unbound fields** — cardinality explosion.

| Symptom | Check | Fix |
|---------|-------|-----|
| Exceeded memory limit | huge `$push` | `$addToSet` sparingly; allowDiskUse; pre-match |
| Wrong totals | null fields | `$ifNull`; filter nulls |
| Slow group | no match | Index + match first |
| Too many groups | high-cardinality key | Bucket differently |

