[[MongoDB]] [[mongodb schema]] [[MongoDB data populate]]

# mongodb denormalization

> Denormalization copies data into documents you’ll read together — fewer joins, more update fan-out.

---

## How it works

```txt
User.name ──duplicate──► Order.customerName (fast read)
                 ↑ update must sync copies
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Embed** | Nest subdocs | “Comments inside post.” |
| **Duplicate** | Copy fields | “Store sellerName on listing.” |
| **Update fan-out** | Many docs to fix | “Rename user → patch all orders.” |
| **16MB limit** | Doc size cap | “Don’t embed unbounded arrays.” |

---


## Configuration and commands

```js
// embed for bounded 1-to-few
{ _id, title, comments: [{ userId, text, at }] }

// duplicate for display fields
{ _id, sellerId, sellerName, price }
```

| Knob | Why it matters |
|------|----------------|
| Bound array size | Avoid 16MB / huge rewrites |
| Source of truth id | Keep `sellerId` even if name copied |
| Migration plan | How renames propagate |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Stale display name | Missed fan-out | Job to sync; or read live |
| Doc too large | unbounded embed | Cap, bucket, or ref |
| Painful updates | Over-duplicated | Normalize hot fields |
| Slow populate chains | Too normalized | Embed read-together data |

---


## Gotchas

> [!WARNING]
> **Unbounded arrays** — “embed all events” will hit 16MB and rewrite cost.

> [!WARNING]
> **Two sources of truth** — without sync jobs, copies drift.

---


## When not to use

- **Highly shared mutable data** — normalize + join/lookup.
- **Strong relational constraints** — SQL may fit better.


## Related

[[mongodb schema]] [[MongoDB data populate]] [[query/mongodb lookup query]]

## Sources

- [Wikipedia — mongodb denormalization](https://en.wikipedia.org/wiki/mongodb_denormalization)
