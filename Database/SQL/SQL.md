[[Database]] [[SQL Configurations]] [[ACID]] [[OLTP]] [[Database design]] [[Prisma]] [[psql essential]] [[mysql]]

# SQL

> Declarative language for relational data — say *what* rows you want; the engine plans *how* to get them. Injection safety is non-negotiable.

---

## Mental model

**Say it in one breath:** SQL is the interface to tables — `SELECT`/`INSERT`/`UPDATE`/`DELETE` plus DDL — executed inside transactions with isolation rules ([[ACID]]).

```txt
Client ──► parameterized SQL ──► parser → planner → executor
                │
                └── binds values separately (not string paste)
```

Classic injection demo (valid SQL if multi-statement is allowed):

```sql
SELECT * FROM user WHERE id = 3; DROP DATABASE test;
```

Most drivers **disable multi-statements by default** on purpose. Never “fix” that for convenience.

## Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Parameterized query** | SQL text + bound values | “User input never becomes SQL syntax.” |
| **Prepared statement** | Parsed once, executed many | “Plan reuse; still bind params every call.” |
| **DDL vs DML** | Schema change vs row change | “DDL often autocommits — plan migrations.” |
| **EXPLAIN** | Show the plan | “I verify index use before shipping.” |
| **Transaction** | Atomic unit of work | “Multi-row money moves need BEGIN/COMMIT.” |
| **ORM** | Maps objects ↔ SQL | “Still generates SQL; still need indexes.” |

---

## Standard config / commands

### Safe query (always)

```js
// mysql2 / node — placeholders, not string concat
const [rows] = await conn.execute(
  'SELECT id, email FROM users WHERE id = ? AND tenant_id = ?',
  [userId, tenantId]
)
```

```sql
-- Postgres
SELECT id, email FROM users WHERE id = $1 AND tenant_id = $2;
```

### Do **not** enable this in web apps

```js
mysql.createConnection({
  // ...
  multipleStatements: true, // opens stacked-query injection
})
```

### Read the plan

```sql
EXPLAIN (ANALYZE, BUFFERS)  -- Postgres
SELECT * FROM orders WHERE customer_id = 42;

EXPLAIN FORMAT=JSON         -- MySQL 8+
SELECT * FROM orders WHERE customer_id = 42;
```

| Practice | Why |
|----------|-----|
| Bind parameters | Blocks injection; correct types |
| Least-privilege DB user | `DROP DATABASE` should be impossible for app role |
| Explicit column lists | Stable APIs; fewer surprises on `ALTER` |
| Transactions for multi-step writes | See [[ACID]] |

ORMs ([[Prisma]], Sequelize-style clients) still need parameterization — never `$queryRawUnsafe` with concatenated input.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Data deleted / odd writes after user input | String-built SQL; `multipleStatements` | Parameterize; revoke DDL; rotate creds |
| Slow query | `EXPLAIN`; missing index | Index matching `WHERE`/`JOIN` ([[mysql index]], [[covering index]]) |
| “Works in CLI, fails in app” | Multi-statement / different SQL mode | Align modes; one statement per call |
| Duplicate rows on retry | No unique / idempotency | Unique constraint + upsert pattern |
| ORM N+1 | Query log / Prisma metrics | `include`/`join`; batch loader |
| Migration vs app SQL mismatch | Drift | [[database migration]] as source of truth |

---

## Gotchas

> [!WARNING]
> **String concatenation is injection** — even “escaped” ad-hoc escaping loses to encoding edge cases. Use driver bind APIs.

> [!WARNING]
> **`SELECT *` + `LIMIT` without `ORDER BY`** — non-deterministic rows; pagination lies under concurrency.

- **NULL semantics** — `= NULL` is unknown; use `IS NULL`. Three-valued logic surprises `NOT IN (…, NULL)`.
- **Implicit casts** — `WHERE indexed_col = '123'` may disable index use depending on types ([[postgres parameter type error]]).
- **Pool + session state** — `SET` / temp tables / last insert id may not stick in transaction-pooling mode ([[connection pooling]]).

---

## When NOT to use

- **Graph traversal as primary model** — specialized graph DB or careful recursive CTEs with eyes open.
- **Full-text / vector-only product** — FTS extensions or [[Vector database]]; pure SQL equality is the wrong tool.
- **Replacing a message queue** — tables-as-queues work until locking and vacuum pain; use a real queue for high fan-out.

## Related

[[Database]] [[SQL Configurations]] [[SQL error]] [[ACID]] [[OLTP]] [[Database design]] [[database migration]] [[Prisma]] [[mysql]] [[psql essential]] [[mysql index]] [[covering index]] [[connection pooling]] [[GIN]] [[Vector database]]
