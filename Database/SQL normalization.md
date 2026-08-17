[[Database design]] [[mysql normalization]] [[SQL]] [[Database mistakes]] [[OLAP]] [[OLTP]]

# SQL normalization

> Decompose tables so each fact lives once — usually through third normal form (3NF) — eliminating redundant columns and update anomalies.

```txt
        SQL normalization ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers walk through 1NF→3NF/BCNF on a messy schema and ask when denorma…

## Sources
- Codd, E.F., relational model and normalization papers (1970s) — deep-dive
- [Wikipedia — Database normalization](https://en.wikipedia.org/wiki/Database_normalization) — overview
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 2 — overview
- Date, C.J., *An Introduction to Database Systems* (normalization chapters) — deep-dive

## Key Concepts
- **1NF:** atomic columns; no repeating groups.
- **2NF:** no partial dependency on a composite key.
- **3NF:** non-key columns depend only on the key, not on other non-key columns.
- **BCNF:** every determinant is a candidate key (stricter than 3NF).
- **Update / insert / delete anomalies:** symptoms of storing the same fact in many places.
- **Intentional denormalization:** duplicate for read speed — document source of truth and refresh.


- **Core:** Normalization is a design discipline: split relations so non-key attributes d…

## Technical Details
| Form | Rule of thumb |
|------|---------------|
| **1NF** | Atomic columns; no repeating groups |
| **2NF** | No partial dependency on a composite key |
| **3NF** | Non-key columns depend only on the key |
| **BCNF** | Every determinant is a candidate key |

- Example anomaly — `customer_city` on every `order` row:

- Customer moves cities → many order rows disagree unless all are updated.
- New customer with no orders → nowhere clean to store city if city lives only …

- **Fix:** `customers(id, city)` referenced by `orders(customer_id)`.

```txt
orders(order_id, customer_id, total, ...)
customers(customer_id, city, ...)     ← city depends on customer, not order
```

- When to denormalize:

- [[OLAP]] reporting, read-heavy dashboards, caching layers.
- Document the **source of truth** and refresh strategy (trigger, ETL, applicat…
- Do not denormalize by accident — that is a [[Database mistakes]] pattern.

## Mistakes to Avoid
- **Mistake:** Stopping at “we have foreign keys” without checking partial/tran…
- **Mistake:** Denormalizing for a rare report and paying write-anomaly cost on…
- **Mistake:** Treating BCNF as mandatory everywhere
- **Mistake:** Duplicating derived totals without a single owner for recalculat…

## Pros/Cons or Trade-offs
- **Pro:** One place to update a fact; smaller write anomalies; clearer integrity with foreign keys.
- **Con:** More joins on read paths; over-normalization can hurt hot read latency.
- **Trade-off:** 3NF OLTP tables vs denormalized read models / [[OLAP]] facts.

## Comparison
- vs [[mysql normalization]]: MySQL-flavored examples and engine notes


### Use cases
- [[OLTP]] order systems keep customers, products, and line items normalized so…
