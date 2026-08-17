[[Database design]] [[mysql normalization]] [[SQL]] [[Database mistakes]] [[OLAP]] [[OLTP]]

# SQL normalization

> Decompose tables so each fact lives once — usually through third normal form (3NF) — eliminating redundant columns and update anomalies.





## Interview Relevance
Interviewers walk through 1NF→3NF/BCNF on a messy schema and ask when denormalization is intentional. Signal: you can spot partial and transitive dependencies and name the anomaly you are fixing.

## Sources
- Codd, E.F., relational model and normalization papers (1970s) — deep-dive
- [Wikipedia — Database normalization](https://en.wikipedia.org/wiki/Database_normalization) — overview
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 2 — overview
- Date, C.J., *An Introduction to Database Systems* (normalization chapters) — deep-dive

## Core Definition
Normalization is a design discipline: split relations so non-key attributes depend on the key, the whole key, and nothing but the key — reducing redundancy and making updates consistent.

## Key Concepts
- **1NF:** atomic columns; no repeating groups.
- **2NF:** no partial dependency on a composite key.
- **3NF:** non-key columns depend only on the key, not on other non-key columns.
- **BCNF:** every determinant is a candidate key (stricter than 3NF).
- **Update / insert / delete anomalies:** symptoms of storing the same fact in many places.
- **Intentional denormalization:** duplicate for read speed — document source of truth and refresh.

## Technical Details
| Form | Rule of thumb |
|------|---------------|
| **1NF** | Atomic columns; no repeating groups |
| **2NF** | No partial dependency on a composite key |
| **3NF** | Non-key columns depend only on the key |
| **BCNF** | Every determinant is a candidate key |

Example anomaly — `customer_city` on every `order` row:

- Customer moves cities → many order rows disagree unless all are updated.
- New customer with no orders → nowhere clean to store city if city lives only on orders.

**Fix:** `customers(id, city)` referenced by `orders(customer_id)`.

```txt
orders(order_id, customer_id, total, ...)
customers(customer_id, city, ...)     ← city depends on customer, not order
```

When to denormalize:

- [[OLAP]] reporting, read-heavy dashboards, caching layers.
- Document the **source of truth** and refresh strategy (trigger, ETL, application write).
- Do not denormalize by accident — that is a [[Database mistakes]] pattern.

## Real-World Applications
[[OLTP]] order systems keep customers, products, and line items normalized so price and address updates stay consistent; a warehouse star schema then denormalizes dimensions for scan speed.

## Pros/Cons or Trade-offs
- **Pro:** One place to update a fact; smaller write anomalies; clearer integrity with foreign keys.
- **Con:** More joins on read paths; over-normalization can hurt hot read latency.
- **Trade-off:** 3NF OLTP tables vs denormalized read models / [[OLAP]] facts.

## Comparison
vs [[mysql normalization]]: MySQL-flavored examples and engine notes; this note is the general SQL design frame. vs [[OLAP]] star schema: deliberate denormalization for analytics. vs document stores: nesting can replace some joins but recreates anomaly risks if duplicated fields diverge.

## Mistakes to Avoid
- Stopping at “we have foreign keys” without checking partial/transitive dependencies.
- Denormalizing for a rare report and paying write-anomaly cost on every order.
- Treating BCNF as mandatory everywhere — know the join cost you are accepting.
- Duplicating derived totals without a single owner for recalculation.
