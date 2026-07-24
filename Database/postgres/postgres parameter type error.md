[[postgres/postgres Error]] [[postgres/psql essential]] [[connection pooling]] [[Prisma query]]

# PostgreSQL Error: `inconsistent types deduced for parameter $n`

> One-line: PostgreSQL inferred **different data types** for the **same placeholder (`$n`)** in one statement — fix by splitting placeholders or adding explicit casts.

## Mental model

Prepared statements bind each `$n` to **one** PostgreSQL type for the whole query. The planner deduces that type from **every** occurrence of the placeholder. If `$2` appears once as `TEXT` and once as `INTEGER`, Postgres cannot pick a single type and raises this error.

```
$params ──► $2 used in SET status (text) ──┐
            $2 used in WHERE version (int) ─┴──► type conflict → ERROR
```

## Common causes

### 1. Same parameter used for different column types

```sql
UPDATE products
SET status = $2          -- TEXT
WHERE id = $1
  AND version = $2;      -- INTEGER
```

### 2. `CASE` expression

```sql
CASE
    WHEN $2 THEN ...
END
```

Later:

```sql
SET status = $2
```

`$2` is expected to be both **BOOLEAN** and **TEXT**.

### 3. `COALESCE`

```sql
SET status = COALESCE($2, status)
```

Later:

```sql
WHERE version = $2
```

`$2` becomes both **TEXT** and **INTEGER**.

### 4. `NULL` parameter

```ts
client.query(sql, [id, null]);
```

If PostgreSQL cannot infer the type from the SQL context, the parameter type becomes ambiguous.

### 5. `VALUES` / `UNION`

```sql
VALUES ($1, $2)
UNION
SELECT id, true;
```

`$2` is inferred as **BOOLEAN**, even if intended to be another type.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `inconsistent types deduced for parameter $n` | Print SQL + param array | Find every `$n` occurrence |
| Same value, different columns | Column types in schema | Use separate placeholders (`$2`, `$3`) |
| `null` in params | Context around `$n` | Cast (`$2::text`) or pass typed value |
| `CASE` / `COALESCE` / `UNION` | Branches infer different types | Split placeholders or cast |

### Debugging steps

1. Print the SQL query.
2. Print the parameter array.
3. Find every occurrence of the reported placeholder (`$2`, `$3`, etc.).
4. Verify every occurrence expects the **same PostgreSQL data type**.

Example:

```sql
UPDATE products
SET status = $2
WHERE id = $1
   OR version = $2;
```

## Fixes

### Use different placeholders

```sql
UPDATE products
SET status = $2
WHERE version = $3;
```

Parameters:

```ts
[id, status, version]
```

### Explicit type casting

```sql
$2::text
$2::uuid
$2::integer
$2::boolean
```

### Pass the correct JavaScript type

Instead of:

```ts
["1"]
```

Use:

```ts
[1]
```

Or convert explicitly:

```ts
Number(value)
```

## Gotchas

> [!WARNING]
> **Reuse is only safe when every occurrence expects the same PG type** — even logically "the same value" needs separate placeholders across type contexts.

> [!WARNING]
> **`null` without context** — Postgres cannot always infer type; cast the placeholder or use separate params per branch.

## Rule of thumb

- Each placeholder (`$1`, `$2`, `$3`, ...) should represent **one logical value**.
- Reuse a placeholder **only if every occurrence expects the same PostgreSQL type**.
- If the same value is needed in different type contexts, use separate placeholders or explicit casts.

## Related

[[postgres/postgres Error]] [[postgres/psql essential]] [[connection pooling]] [[Prisma query]]
