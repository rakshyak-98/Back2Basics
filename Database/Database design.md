[[Database]] [[SQL normalization]] [[OLTP]] [[ACID]] [[Data access patterns]] [[database migration]] [[Database mistakes]]

# Database design

> Tables, keys, and constraints that keep facts correct and queries honest — schema is a contract, not just storage.

---

## Mental model

**Say it in one breath:** Good design makes illegal states hard to store — keys, FKs, CHECKs, and clear transaction boundaries do more than clever application code.

```txt
Entities → tables
Relationships → FKs / join tables
Invariants → PRIMARY/UNIQUE/CHECK/EXCLUDE
Access paths → indexes matching real queries ([[Data access patterns]])
Change → migrations ([[database migration]])
```

Normalize for [[OLTP]] write correctness ([[SQL normalization]]); denormalize only with an owned sync story.

## Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Primary key** | Stable row identity | “Surrogate `id` plus unique business keys where needed.” |
| **Foreign key** | Child must point at a real parent | “DB enforces orphans can’t land.” |
| **Invariant** | Rule that must always hold | “Prefer CHECK/generated column over hope.” |
| **Expand-contract** | Compatible schema evolve | “Add nullable → dual-write → backfill → enforce.” |
| **Tenant key** | Every row knows its customer | “Filter + constraint; never trust client alone.” |
| **Temporal overlap** | Two periods share time | “Use the interval overlap predicate + EXCLUDE.” |

---

## Standard patterns

### Independent scalar vs derived amount

Storing `total_amount` as a free column lets `100 - 5 + 10 ≠ 105` rows exist.

```sql
-- Pattern A: CHECK invariant
ALTER TABLE invoices ADD CONSTRAINT chk_invoices_total
CHECK (
  total_amount = (
    subtotal
    - COALESCE(discount_amount, 0)
    + COALESCE(tax_amount, 0)
  )
);

-- Pattern B: generated column (Postgres / MySQL 8+)
ALTER TABLE invoices
  DROP COLUMN total_amount,
  ADD COLUMN total_amount DECIMAL(12,2)
    GENERATED ALWAYS AS (
      subtotal - COALESCE(discount_amount, 0) + COALESCE(tax_amount, 0)
    ) STORED;
```

Line-item `unit_price` on an order is often a **historical snapshot** (correct denorm) — document that; don’t “fix” it by always joining live `products.price`.

### Sketch schema (DBML mental model)

```txt
users(id PK) ──< orders(user_id FK)
orders ──< order_items(order_id, product_id) >── products
merchants ──< products
```

Indexes follow **equality → range → ORDER BY** for hot queries; see [[covering index]] / [[mysql index]].

---

## Transaction correlation (audit)

Audit rows without a shared id cannot prove which changes were one business COMMIT.

```txt
HTTP request → generate correlation UUID → request context
       → same id on DB audit rows, app logs, outbox messages
```

```sql
INSERT INTO audit_log (transaction_correlation_id, table_name, ...)
VALUES ('TX-89AF', 'orders', ...);
-- same TX-89AF on payment_transactions + entitlements rows
```

Create the id **once** at the start of the operation; pass it unchanged. Timestamps alone are not correlation under concurrency.

---

## Overlapping validity periods

Two intervals `[start_a, end_a)` and `[start_b, end_b)` overlap iff:

```txt
start_a < end_b  AND  start_b < end_a
```

(Use `<=` if your intervals are closed; be consistent.)

```sql
-- Reject overlapping subscriptions per customer (Postgres)
ALTER TABLE subscriptions ADD CONSTRAINT subs_no_overlap
EXCLUDE USING gist (
  customer_id WITH =,
  tstzrange(start_at, end_at, '[)') WITH &&
);
```

Billing twice for the same window is almost always a missing overlap constraint, not a “rare race.”

---

## Multi-tenancy boundaries

Every tenant-owned row needs `tenant_id` (or equivalent) **in the row and in the query**.

| Failure | Fix |
|---------|-----|
| `WHERE id = $1` without tenant | Always `AND tenant_id = $tenant` |
| Shared “global” lookup table mixed with tenant data | Separate schemas/tables; explicit shared flag |
| Unique email global in multi-tenant SaaS | `UNIQUE (tenant_id, email)` unless product requires global |

RLS (Postgres row-level security) helps defense-in-depth; still pass tenant in the application.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Math-wrong invoice totals | Free-form total column | CHECK or generated column |
| Audit cannot reconstruct one checkout | No correlation id | Add `transaction_correlation_id` |
| Double subscription / double booking | Overlap logic | EXCLUDE / app transaction + overlap predicate |
| Customer A sees Customer B data | Missing tenant predicate | Composite unique keys; forced tenant filter; tests |
| Migration locks production | Single huge DDL | Expand-contract; online schema tools ([[database migration]], [[Alter table]]) |
| ORM model ≠ DB | Drift | Migrations as source of truth |

---

## Gotchas

> [!WARNING]
> **App-only invariants** — if the rule matters (money, tenancy, uniqueness), put a constraint in the DB. Two writers will bypass app checks.

> [!WARNING]
> **Soft deletes without unique care** — `UNIQUE(email)` blocks re-create after soft delete; use partial unique indexes (`WHERE deleted_at IS NULL`).

- **Wide “god” tables** — every feature adds a column; split bounded contexts when churn hurts.
- **FK `ON DELETE CASCADE`** — convenient until one delete wipes a tree; prefer explicit.
- **No transaction around multi-table writes** — design assumed atomicity you never coded ([[ACID]]).

---

## When NOT to use

- **Document soup for every entity** — JSONB everywhere loses constraints; use for genuinely schemaless payloads.
- **Premature sharding** — fix indexes and design first ([[OLTP]]).
- **Copying OLAP star schema into OLTP** — wrong write shape.

## Related

[[SQL normalization]] [[Database]] [[OLTP]] [[ACID]] [[OCC]] [[Data access patterns]] [[database migration]] [[Alter table]] [[Database mistakes]] [[connection pooling]] [[covering index]]
