[[mysql columns]] [[mysql query]] [[mysql index]]

# mysql json

> MySQL native `JSON` type with binary storage and `JSON` functions—validate on write, query with paths, index via generated columns.

## Interview Relevance

JSON-in-MySQL questions test path operators (`->>`), generated-column indexes, and the rule: relational columns for hot filters, JSON for evolving attributes.

## Sources

- [MySQL Reference Manual — JSON Data Type](https://dev.mysql.com/doc/refman/en/json.html) — deep-dive
- [MySQL Reference Manual — JSON Functions](https://dev.mysql.com/doc/refman/en/json-functions.html) — deep-dive

## Key Concepts

- **Validated JSON type:** binary storage, not opaque TEXT.
- **Path extraction:** `->` / `->>` and `JSON_EXTRACT`.
- **Indexing:** generated columns (STORED/VIRTUAL) + secondary indexes — not raw JSON blobs as B-trees.
- **Modeling rule:** hot filters as real columns; JSON for flexible attributes.

## Technical Details

```sql
INSERT INTO events (payload) VALUES ('{"type":"click","id":1}');
SELECT payload->>'$.type' AS event_type FROM events WHERE id = 1;
```

Indexing:

```sql
ALTER TABLE events ADD event_type VARCHAR(50)
  AS (JSON_UNQUOTE(JSON_EXTRACT(payload, '$.type'))) STORED,
  ADD INDEX idx_event_type (event_type);
```

Prefer relational columns for hot filters; JSON for evolving attributes.

## Real-World Applications

Event payloads and sparsely populated product attributes. Example: store analytics properties in JSON but index `event_type` via a generated column for dashboard filters.

## Pros/Cons or Trade-offs

- **Pro:** Schema flexibility without constant migrations for leaf attributes.
- **Con:** Easy to create unindexable query patterns; JSON-everywhere loses relational clarity and constraints.

## Comparison

vs [[mysql columns]] typed fields: typed columns win for invariants and simple indexes. vs PostgreSQL `jsonb` + [[GIN]]: similar problem, different operators and index types.

## Mistakes to Avoid

- Filtering on JSON paths in hot queries without generated-column indexes.
- Putting core relational keys only inside JSON.
- Storing invalid-as-TEXT “JSON” instead of the native JSON type.
