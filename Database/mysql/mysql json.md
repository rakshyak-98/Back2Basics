[[mysql columns]] [[mysql query]] [[mysql index]]

# mysql json

> MySQL native `JSON` type with binary storage and `JSON` functions—validate on write, query with paths, index via generated columns.

## Insert and query

```sql
INSERT INTO events (payload) VALUES ('{"type":"click","id":1}');
SELECT payload->>'$.type' AS event_type FROM events WHERE id = 1;
```

## Indexing

```sql
ALTER TABLE events ADD event_type VARCHAR(50)
  AS (JSON_UNQUOTE(JSON_EXTRACT(payload, '$.type'))) STORED,
  ADD INDEX idx_event_type (event_type);
```

Prefer relational columns for hot filters; JSON for evolving attributes.

## Sources

- MySQL Reference Manual — [JSON Functions](https://dev.mysql.com/doc/refman/en/json-functions.html)
- MySQL Reference Manual — [JSON Data Type](https://dev.mysql.com/doc/refman/en/json.html)
