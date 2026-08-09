[[SQL]] [[Database]] [[psql essential]] [[mysql index]] [[covering index]] [[OLTP]]

# GIN

> PostgreSQL inverted index for values with many keys inside one row — JSONB containment, arrays, full-text — look up element → matching rows.

---

## Index

- [[#Mental model]]
- [[#Interview map (words you can say)]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** A B-tree indexes one scalar per row. GIN (Generalized Inverted Index) indexes **each element** inside a composite value so “contains this key/token” is an index lookup.

```txt
Row 1: tags = {go, postgres, backend}
Row 2: tags = {flutter, mobile}
Row 3: tags = {go, docker}

GIN posting lists:
  go       → [1, 3]
  postgres → [1]
  backend  → [1]
  flutter  → [2]
  ...
```

Classic win: `JSONB @>` containment without exploding JSON into columns.

```sql
SELECT *
FROM audit_log
WHERE new_data @> '{"config":{"autoRenew":true}}';
```

## Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Inverted index** | Key → list of rows | “Like a book index: word points to pages.” |
| **GIN** | PG index access method for multi-key values | “Great for JSONB containment, arrays, `tsvector`.” |
| **GiST** | Different PG AM — ranges, geometry, trigram | “Pick GiST for `&&` ranges / PostGIS; GIN for contains.” |
| **`jsonb_path_ops`** | Smaller/faster GIN for `@>` only | “If I only need containment, use `jsonb_path_ops`.” |
| **Pending list** | Fast insert buffer before merge into main GIN | “Bulk load can leave a pending list; `gin_clean_pending_list`.” |
| **B-tree** | Scalar equality / range | “Equality on `user_id` stays B-tree; don’t GIN everything.” |

---

## Standard config / commands

### Create indexes

```sql
-- JSONB: default jsonb_ops (supports @>, ?, ?&, ?|, ...)
CREATE INDEX ON audit_log USING GIN (new_data);

-- Smaller/faster if you only use @>
CREATE INDEX ON audit_log USING GIN (new_data jsonb_path_ops);

-- Array contains
CREATE INDEX ON posts USING GIN (tags);

-- Full text
CREATE INDEX ON articles USING GIN (to_tsvector('english', body));
```

### Confirm the planner uses it

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM audit_log
WHERE new_data @> '{"config":{"autoRenew":true}}';
-- Want: Bitmap Index Scan on …_gin
```

### Ops knobs

```sql
-- After bulk COPY, force pending-list merge
SELECT gin_clean_pending_list('audit_log_new_data_idx'::regclass);

-- Size / usage
SELECT indexrelid::regclass, pg_size_pretty(pg_relation_size(indexrelid))
FROM pg_index
JOIN pg_class ON pg_class.oid = indexrelid
WHERE relname LIKE '%gin%';
```

| Knob | Why it matters |
|------|----------------|
| `jsonb_ops` vs `jsonb_path_ops` | Path ops ≈ smaller, `@>` only |
| `gin_pending_list_limit` | Larger = faster ingest, slower queries until flush |
| `fastupdate` | ON (default) buffers inserts; OFF = slower writes, fresher index |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Seq scan on `@>` query | `EXPLAIN`; index missing / wrong opclass | Create GIN; use `@>` not `->` equality without expression index |
| Inserts slow after GIN added | Index write amplification | Batch load then create index; or raise pending list / load with `fastupdate` |
| Index huge vs table | High-cardinality JSON keys | `jsonb_path_ops`; index expression on hot path only |
| Query still slow with Bitmap Heap Scan | Low selectivity / lots of heap hits | Narrow JSON; partial index; extract hot fields to columns + B-tree |
| “Operator does not exist” / no match | Wrong type (`json` vs `jsonb`) | Cast/store `jsonb`; recreate index |

---

## Gotchas

> [!WARNING]
> **`json` is not `jsonb`** — GIN wants `jsonb`. Plain `json` stores text; convert before indexing.

> [!WARNING]
> **Expression must match the query** — index on `(data->'a')` does not help `data @> …` and vice versa.

- **GIN update cost** — every INSERT/UPDATE rewrites posting lists; write-heavy wide JSONB can dominate I/O.
- **MySQL** — no GIN; use generated columns + B-tree / multi-valued indexes (8.0+) for JSON paths ([[mysql json]], [[mysql index]]).
- **Don’t index the whole document “just in case”** — index the containment shapes you actually query.

---

## When NOT to use

- **Point lookup by primary key / FK** — B-tree ([[covering index]] pattern).
- **Range queries on numbers/dates** — B-tree or BRIN; GIN is the wrong tool.
- **Tiny tables** — sequential scan wins; index only adds write cost.

## Related

[[SQL]] [[psql essential]] [[mysql index]] [[mysql json]] [[covering index]] [[OLTP]] [[Database design]] [[Data access patterns]]
