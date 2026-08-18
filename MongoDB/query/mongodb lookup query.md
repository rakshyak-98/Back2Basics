[[MongoDB]] [[mongosh query]] [[MongoDB data populate]] [[mongoDB Group query]]

# mongodb lookup query

> `$lookup` joins collections in an aggregation — Mongo’s left outer join.

## Mental model

**Say it in one breath:** From each input document, find matches in another collection and attach them as an array field.

```txt
orders $lookup users on userId = _id  →  orders + users[]
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **localField / foreignField** | Equality join | “Simple key match.” |
| --- | --- | --- |
| **pipeline lookup** | Join with extra `$match` | “Filter related docs.” |
| **as** | Output array name | “Always an array (maybe empty).” |
| **`$unwind`** | Flatten array | “Careful with nulls.” |

## Standard config / commands

```js
db.orders.aggregate([
  { $lookup: {
      from: 'users',
      localField: 'userId',
      foreignField: '_id',
      as: 'user',
  }},
  { $unwind: { path: '$user', preserveNullAndEmptyArrays: true } },
])

// pipeline form
{ $lookup: {
    from: 'items',
    let: { oid: '$_id' },
    pipeline: [
      { $match: { $expr: { $eq: ['$orderId', '$$oid'] } } },
      { $project: { sku: 1, qty: 1 } },
    ],
    as: 'items',
}}
```

| Knob | Why it matters |

| Index on foreignField | Join speed |
| --- | --- |
| preserveNull | Left join vs drop |
| Project in pipeline | Smaller payloads |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Empty user arrays | type mismatch ObjectId/string | Cast ids consistently |
| Slow lookup | missing index | Index foreign key |
| Dup rows after unwind | many matches | Expect multiplicative rows |
| Huge as arrays | unbounded relations | `$limit` in pipeline |

## Gotchas

> [!WARNING]
> **ObjectId vs string** — equality fails silently → empty `as`.

> [!WARNING]
> **Lookup on huge collections without match** — full collection work per shard story; filter early.

## When NOT to use

- **Always-together data** — embed ([[mongodb denormalization]]).
- **Graph depth searches** — `$graphLookup` or external graph DB.

## Related

[[MongoDB data populate]] [[mongoDB Group query]] [[mongodb denormalization]]
