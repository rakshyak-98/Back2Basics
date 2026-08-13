<!-- note-strategy: operational -->
[[mysql]] [[SQL normalization]] [[Database design]]

# mysql normalization

> Normalize relational schemas to cut redundancy and update anomalies — 1NF→BCNF (and beyond) as interview vocabulary; denormalize only with a measured reason.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Put each fact in one place; keys determine attributes; if a column depends on only part of a composite key or on another non-key, split tables.

```txt
1NF  atomic cells, no repeating groups
2NF  no partial dependency on composite PK
3NF  no transitive dependency (A→B→C)
BCNF every determinant is a candidate key
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **1NF** | Atomic values | “No comma-separated phones in one cell.” |
| **2NF** | Full composite key dependency | “product_name doesn’t belong on order_line PK.” |
| **3NF** | No non-key → non-key | “city→state goes to a lookup.” |
| **BCNF** | Stricter 3NF | “Overlapping candidate keys fixed.” |
| **Anomaly** | Insert/update/delete pain | “Why we normalize.” |
| **Denormalize** | Add redundancy for read speed | “Only with a known query + refresh plan.” |

---

## Standard config / commands

No special MySQL knob — design + constraints:

```sql
-- 2NF fix sketch: split product attrs off order_items
CREATE TABLE products (
  product_id INT PRIMARY KEY,
  product_name VARCHAR(200) NOT NULL
);
CREATE TABLE order_items (
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  qty INT NOT NULL,
  PRIMARY KEY (order_id, product_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

| Form | Smell |
|------|-------|
| 1NF | Arrays/lists in a cell |
| 2NF | Attr depends on part of composite PK |
| 3NF | Attr depends on another attr |
| 4NF/5NF | Multi-valued / join dependency (rare in interviews) |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Update one fact in many rows | Redundant columns | Extract table + FK |
| Can’t insert without fake deps | Partial dependency | Split to 2NF |
| Inconsistent derived fields | Transitive deps | 3NF lookup tables |
| Join explosion / slow reads | Over-normalized hot path | Controlled denormalize + index |

---

## Gotchas

> [!WARNING]
> **Normalization ≠ MySQL feature** — it’s design; MySQL only enforces what you declare (PK/UNIQUE/FK).

> [!WARNING]
> **JSON columns** — easy 1NF violations; index generated paths if you filter them.

---

## When NOT to use

- **Reporting cubes** — star/snowflake or warehouse models ([[OLAP]]), not OLTP 5NF purity.
- **Read-heavy caches** — denormalized projections with clear ownership.

---

## Related

[[SQL normalization]] [[Database design]] [[key Constraint]] [[OLTP]] [[OLAP]]
