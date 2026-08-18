[[mysql]] [[mysql table]] [[mysql query]]

# mysql json

> Store and query JSON documents in a column — extract with `->` / `->>`, build with `JSON_OBJECT` / `JSON_ARRAYAGG`.

## Mental model

**Say it in one breath:** `JSON` type validates JSON on write; path expressions pull fields; aggregators build nested payloads for APIs without application-side stitching.

```txt
row JSON column ──► -> '$.key' (JSON) / ->> '$.key' (text)
JSON_OBJECT / JSON_ARRAYAGG ──► build documents in SELECT
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **`->`** | Extract JSON, still JSON | “Keeps quotes/types as JSON.” |
| --- | --- | --- |
| **`->>`** | Extract as text | “Unquoted string for WHERE/compare.” |
| **JSON_EXTRACT** | Long form of `->` | “Same path language.” |
| **JSON_SET / REMOVE** | Patch document in place | “Partial update without full rewrite.” |
| **Generated column + index** | Index a path | “Don’t full-scan JSON for hot filters.” |

## Standard config / commands

```sql
SELECT JSON_OBJECT('id', id, 'name', name) FROM users;

SELECT data->'$.username' AS username FROM Users;
SELECT data->>'$.id' AS id, data->>'$.name' AS name FROM People;

SELECT user_id,
       JSON_ARRAYAGG(JSON_OBJECT('id', post_id, 'title', title)) AS posts
FROM user_posts
GROUP BY user_id;

UPDATE t SET content = JSON_SET(content, '$.a.b', 'x') WHERE id = 1;
UPDATE t SET content = JSON_REMOVE(content, '$.yourKey') WHERE id = 1;
```

| Knob | Why it matters |

| `JSON` vs `TEXT` | Typed JSON rejects invalid docs |
| --- | --- |
| Path `$.a[0].b` | Arrays are 0-based |
| Functional/generated index | Make frequent paths sargable |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Invalid JSON text | Bad insert string | Validate client-side; use JSON type |
| Compare fails on `->` | Comparing JSON to string | Use `->>` or `CAST` |
| Slow filter on path | No index on extracted path | Generated column + INDEX |
| `JSON_ARRAYAGG` NULL group | Empty set | `COALESCE(..., JSON_ARRAY())` |

## Gotchas

> [!WARNING]
> **`->` vs `->>`** — mixing them in WHERE is a classic “looks equal in UI, fails in SQL” bug.

> [!WARNING]
> **Partial updates still rewrite the value** — huge documents = heavy row updates; don’t abuse as a document DB.

## When NOT to use

- **Core relational fields** — put id/status/foreign keys in real columns.
- **Heavy document queries** — use a document store or normalize.

## Related

[[mysql table]] [[mysql query]] [[mysql function]] [[Vector database]]
