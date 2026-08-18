[[mysql]] [[covering index]] [[mysql query]] [[mysql engine]]

# mysql index

> An index is a sorted lookup structure so MySQL finds rows without scanning the whole table — pay write cost for read speed.

## Mental model

**Say it in one breath:** InnoDB clusters rows by primary key; secondary indexes are B+ trees that store key columns + PK, then optionally jump to the row.

```txt
WHERE / JOIN / ORDER
        │
        ▼
 Secondary B+ tree ──► PK ──► clustered row (unless covering)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Clustered index** | Table data ordered by PK | “PK lookup is a direct leaf hit.” |
| --- | --- | --- |
| **Secondary index** | Extra B+ tree → PK | “Non-PK filters use secondary, then fetch row.” |
| **Covering index** | Index has all selected columns | “No bookmark lookup — index-only.” |
| **Composite / leftmost** | Multi-column; prefix matters | “`(a,b,c)` helps `a` and `a,b`, not `b` alone.” |
| **Cardinality** | How unique the values are | “Low-cardinality alone often won’t filter enough.” |
| **HASH index** | Equality-only; MEMORY engine | “InnoDB ignores HASH; it stays BTREE.” |

### Why indexes matter (short)

- Bad: `WHERE city=? AND status=? ORDER BY created_at` with only `(city)` → scan + filesort.
- Good: `(city, status, created_at)` matching left-to-right use.
- Bad: `WHERE YEAR(created_at)=2025` → function kills index use.
- Good: range on bare column: `created_at >= '2025-01-01' AND created_at < '2026-01-01'`.

## Standard config / commands

```mysql
SHOW INDEX FROM your_table;

CREATE INDEX idx_city_status_created ON hotels (city, status, created_at);
ALTER TABLE t DROP INDEX idx_name;

-- constraints / FK supporting indexes
SELECT CONSTRAINT_NAME, COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'db' AND TABLE_NAME = 'orders';

-- usage heat (drop cold indexes)
SELECT OBJECT_SCHEMA, OBJECT_NAME, INDEX_NAME, COUNT_STAR
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE INDEX_NAME IS NOT NULL
ORDER BY COUNT_STAR DESC;
```

| Knob | Why it matters |

| Column order in composite | Matches WHERE/JOIN/ORDER left-to-right |
| --- | --- |
| Select list | `SELECT *` often ruins covering |
| Index count | Each write updates every index — aim ~3–6/table unless measured |

`HASH` only on MEMORY (InnoDB silently uses BTREE):

```mysql
CREATE TABLE mem_t (id INT, name VARCHAR(100), INDEX name_idx (name) USING HASH)
ENGINE=MEMORY;
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Full table scan | `EXPLAIN` → `type=ALL` | Add selective index; fix sargability |
| Filesort / temp table | `Extra` in EXPLAIN | Extend composite to cover ORDER BY |
| High write latency | Many indexes on hot table | Drop unused via performance_schema |
| Index “not used” | Function/cast on column | Rewrite predicate; store normalized value |
| Wrong engine for HASH | `SHOW INDEX` / engine | Use MEMORY or accept BTREE on InnoDB |
| FK drop fails | Index needed by FK | Drop FK, then index |

## Gotchas

> [!WARNING]
> **`USING HASH` on InnoDB is a no-op** — only MEMORY supports HASH; check with `SHOW INDEX`.

> [!WARNING]
> **Leftmost prefix** — index `(a,b)` does not help `WHERE b = ?` alone.

> [!WARNING]
> **Too many indexes** — every INSERT/UPDATE/DELETE maintains all of them; unused indexes are pure tax.

## When NOT to use

- **Tiny tables** — full scan can beat index + lookup overhead.
- **Write-heavy, rarely filtered columns** — index cost > benefit.
- **Low-cardinality flags alone** — combine into composite or skip.
- **Blind “index every column”** — measure with EXPLAIN + slow log.

## Related

[[covering index]] [[mysql]] [[mysql query]] [[mysql engine]] [[mysql lock]] [[OLTP]]
