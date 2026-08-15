[[MongoDB]] [[query/mongodb lookup query]] [[mongosh query]] [[query/mongoDB Group query]]

# mongodb view

> A MongoDB view is a saved aggregation pipeline — read-only, always reflects the source collection.

## Interview Relevance

Views questions check read-only aggregation shortcuts versus materialized collections.

## Sources

- [MongoDB Manual](https://www.mongodb.com/docs/manual/) — deep-dive
- [MongoDB Docs home](https://www.mongodb.com/docs/) — overview

## Key Concepts

```txt
orders ──$group/$sort──► orderSummaryView (read-only)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **View** | Named pipeline | “Reuse the same aggregation.” |
| **On-demand** | Computed at read | “Slow if pipeline is heavy.” |
| **No indexes on view** | Uses source indexes | “Index the underlying collection.” |
| **Materialized view** | Stored result (Atlas/ondemand) | “Trade freshness for speed.” |

## Technical Details

```js
db.createView('orderSummaryView', 'orders', [
  { $group: { _id: '$customerId', totalSpent: { $sum: '$amount' } } },
  { $sort: { totalSpent: -1 } },
])
db.orderSummaryView.find().limit(20)
```

| Knob | Why it matters |
|------|----------------|
| Pipeline cost | Runs every query |
| Source indexes | Only lever for speed |
| Permissions | Grant read on view, not raw |

## Pros/Cons or Trade-offs

- **Write path** — views are read-only.
- **Hot, simple filters** — a normal collection + index is clearer.

## Mistakes to Avoid

> [!WARNING]
> **Views are not caches** — heavy `$lookup` views will hurt under load.

> [!WARNING]
> **Typo in field names** — aggregation silently yields empty groups.

| Symptom | Check | Fix |
|---------|-------|-----|
| View query slow | `explain` on view | Simplify pipeline; index source |
| Can’t update via view | By design | Write to source collection |
| Wrong totals | Pipeline bug / nulls | Fix `$group`; handle missing fields |
| View missing | Wrong DB | `db.getCollectionNames()` |

