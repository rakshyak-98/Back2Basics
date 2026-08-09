[[Database]] [[Database design]] [[OLTP]] [[OLAP]] [[Data access patterns]] [[mysql normalization]]

# SQL normalization

> Split tables so each fact lives once — stop update anomalies; pay with joins when you read.

---

## Index

- [[#Mental model]]
- [[#Interview map (words you can say)]]
- [[#Normal forms (1NF → 3NF)]]
- [[#Standard config / patterns]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Normalization is a set of rules that remove duplicate facts and bad dependencies so changing one business fact touches one place.

```txt
Denormalized row                 Normalized
────────────────                 ───────────
order + product name +           orders ──► order_items
customer address repeated        │
on every line item               ├──► products
                                 └──► customers
Update product name once         Update products.name once
```

OLTP schemas usually aim for **3NF** (or BCNF). Warehouses often **denormalize** on purpose ([[OLAP]]).

## Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Atomic** | One value per cell | “No comma-separated phone lists in one column.” |
| **1NF** | Atomic cells, no repeating groups | “Repeating phone1/phone2 columns fail 1NF.” |
| **2NF** | 1NF + no partial key dependency | “Non-key cols must depend on the *whole* composite PK.” |
| **3NF** | 2NF + no transitive dependency | “Dept head depends on department, not on employee id — split.” |
| **Update anomaly** | Change one fact, miss copies | “That’s why we normalize OLTP.” |
| **Denormalize** | Store copies for read speed | “OK for OLAP/cache if you own the sync story.” |

---

## Normal forms (1NF → 3NF)

| Form | Rule |
|------|------|
| **1NF** | Atomic values; unique column names; no repeating groups |
| **2NF** | 1NF + every non-key attribute depends on the **entire** primary key |
| **3NF** | 2NF + no non-key attribute depends on another non-key attribute |

### 1NF — atomic cells

**Before (not 1NF):**

```txt
| ID | Name  | Phone Numbers   |
|----|-------|-----------------|
| 1  | Alice | 12345, 67890    |
| 2  | Bob   | 54321           |
```

**After:**

```txt
| ID | Name  | Phone Number |
|----|-------|--------------|
| 1  | Alice | 12345        |
| 1  | Alice | 67890        |
| 2  | Bob   | 54321        |
```

(Better still: separate `phones` table with `person_id` FK.)

### 2NF — whole composite key

**Before:** PK `(OrderID, ProductID)` but `ProductName` depends only on `ProductID`.

**After:** `order_items(OrderID, ProductID, …)` + `products(ProductID, ProductName)`.

### 3NF — no transitive dependency

**Before:** `EmployeeID → Department → DeptHead` all in one table.

**After:** `employees(EmployeeID, Name, DepartmentID)` + `departments(DepartmentID, DeptHead)`.

---

## Standard config / patterns

```sql
-- Enforce relationships the normal form implies
CREATE TABLE products (
  product_id BIGINT PRIMARY KEY,
  name       TEXT NOT NULL
);

CREATE TABLE order_items (
  order_id   BIGINT NOT NULL REFERENCES orders(order_id),
  product_id BIGINT NOT NULL REFERENCES products(product_id),
  qty        INT NOT NULL CHECK (qty > 0),
  PRIMARY KEY (order_id, product_id)
);
```

| Pattern | Use |
|---------|-----|
| FK + `ON DELETE` policy | Keep 3NF relationships honest |
| Unique constraints | Natural keys (email, SKU) |
| Controlled denorm | Cached `product_name` on line item **plus** job/trigger to refresh |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Same customer address differs across rows | Duplicate facts | Normalize; single `customers` / `addresses` source |
| UPDATE product name leaves old orders wrong | Copied name without sync | Prefer FK + join; or versioned snapshot column with clear semantics |
| Join explosion / slow reports | Over-normalized OLAP path | Star schema / warehouse ([[OLAP]]); don’t force 3NF on analytics |
| NULL-heavy wide tables | Repeating group disguised as columns | Child table or JSONB with care ([[GIN]]) |
| Orphan line items | Missing FK | Add FK; backfill; ban app-only “soft” integrity |

---

## Gotchas

> [!WARNING]
> **JSON blob ≠ free pass** — stuffing arrays into one column violates 1NF spirit and breaks constraints; use JSON only when the document is opaque or indexed on purpose ([[GIN]]).

> [!WARNING]
> **Snapshot vs master data** — order line `unit_price` is often a **point-in-time copy** (correct), not a 2NF bug. Document which fields are historical.

- **BCNF** catches some 3NF edge cases with overlapping candidate keys — mention in interviews; rare in day-to-day CRUD.
- **mysql normalization** note may mirror examples — keep one mental model across engines.

---

## When NOT to use

- **OLAP / reporting marts** — star/snowflake and denormalized facts are the goal ([[OLAP]]).
- **Read-heavy caches** — Redis/materialized views intentionally duplicate.
- **Micro-entities for every attribute** — join hell; stop around 3NF unless anomalies hurt.

## Related

[[Database design]] [[OLTP]] [[OLAP]] [[Data access patterns]] [[mysql normalization]] [[GIN]] [[Database mistakes]] [[ACID]]
