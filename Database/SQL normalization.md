[[Database design]] [[mysql normalization]] [[SQL]] [[Database mistakes]]

# SQL normalization

> Decompose tables to eliminate redundant facts and update anomalies—usually through third normal form (3NF)—so each fact is stored once and dependencies follow the key.

## Normal forms (practical view)

| Form | Rule of thumb |
|------|---------------|
| **1NF** | Atomic columns; no repeating groups |
| **2NF** | No partial dependency on a composite key |
| **3NF** | Non-key columns depend only on the key, not on other non-key columns |
| **BCNF** | Every determinant is a candidate key |

## Example anomaly without normalization

Storing `customer_city` on every `order` row duplicates data—change the customer's city and historical orders show inconsistent cities unless you update all rows.

**Fix:** `customers(id, city)` referenced by `orders(customer_id)`.

## When to denormalize

[[OLAP]] reporting, read-heavy dashboards, or caching layers may duplicate columns intentionally. Document the **source of truth** and refresh strategy; do not denormalize by accident.

## Sources

- Codd, E.F., relational normalization papers (1970s)
- Wikipedia — [Database normalization](https://en.wikipedia.org/wiki/Database_normalization)
- Kleppmann, *DDIA*, Ch. 2
