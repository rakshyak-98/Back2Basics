[[MongoDB]] [[mongosh]] [[mognodb indexing]]

# mongosh query

> Everyday find/aggregate patterns in mongosh — filter, project, sort, explain.

---

## How it works

```txt
filter → project → sort → limit   (+ index)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Filter** | `$eq` / `$in` / ranges | “Equality first for indexes.” |
| **Projection** | Fields returned | “Cut payload.” |
| **Cursor** | Batched results | “Don’t `toArray` huge sets.” |
| **explain** | Winning plan | “IXSCAN or COLLSCAN.” |

---


## Configuration and commands

```js
db.orders.find({ status: 'paid', total: { $gte: 100 } }, { userId: 1, total: 1 })
  .sort({ createdAt: -1 }).limit(50)

db.orders.aggregate([
  { $match: { status: 'paid' } },
  { $group: { _id: '$userId', spend: { $sum: '$total' } } },
  { $sort: { spend: -1 } },
  { $limit: 20 },
])

db.orders.find({ status: 'paid' }).explain('executionStats')
```

| Knob | Why it matters |
|------|----------------|
| `$match` early | Shrink pipeline data |
| Covered query | Index has all fields |
| Hint | Force index when planner errs |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| COLLSCAN | explain | Add index |
| Slow sort | sort stage in memory | Index sort keys |
| Huge RAM in shell | `toArray` | iterate cursor |
| Wrong results | operator typo | `$eq` vs assignment mistakes |

---


## Gotchas

> [!WARNING]
> **`find({a: {$gt: 1, $lt: 5}})`** — combine range ops on one field carefully; know index bounds.

> [!WARNING]
> **Regex `/^foo/` can use index; `/foo/` often can’t.**

---


## When not to use

- **application production path** — driver with timeouts/pools.
- **Giant reporting** — warehouse / secondary + aggregate carefully.


## Related

[[mognodb indexing]] [[query/mongoDB Group query]] [[query/mongodb lookup query]]

## Sources

- [Wikipedia — mongosh query](https://en.wikipedia.org/wiki/mongosh_query)
