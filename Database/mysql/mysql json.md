[[mysql columns]] [[mysql query]] [[mysql index]]

# mysql json

> MySQL native `JSON` type with binary storage and `JSON` functions—validate on write, query with paths, index via generated columns.

```txt
        mysql json ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** JSON-in-MySQL questions test path operators (`->>`), generated-column indexes…

## Sources
- [MySQL Reference Manual — JSON Data Type](https://dev.mysql.com/doc/refman/en/json.html) — deep-dive
- [MySQL Reference Manual — JSON Functions](https://dev.mysql.com/doc/refman/en/json-functions.html) — deep-dive

## Key Concepts
- **Validated JSON type:** binary storage, not opaque TEXT.
- **Path extraction:** `->` / `->>` and `JSON_EXTRACT`.
- **Indexing:** generated columns (STORED/VIRTUAL) + secondary indexes
- **Modeling rule:** hot filters as real columns; JSON for flexible attributes.

## Technical Details
```sql
INSERT INTO events (payload) VALUES ('{"type":"click","id":1}');
SELECT payload->>'$.type' AS event_type FROM events WHERE id = 1;
```

```sql
ALTER TABLE events ADD event_type VARCHAR(50)
  AS (JSON_UNQUOTE(JSON_EXTRACT(payload, '$.type'))) STORED,
  ADD INDEX idx_event_type (event_type);
```

- Prefer relational columns for hot filters; JSON for evolving attributes.

## Mistakes to Avoid
- **Mistake:** Filtering on JSON paths in hot queries without generated-column …
- **Mistake:** Putting core relational keys only inside JSON
- **Mistake:** Storing invalid-as-TEXT “JSON” instead of the native JSON type

## Pros/Cons or Trade-offs
- **Pro:** Schema flexibility without constant migrations for leaf attributes.
- **Con:** Easy to create unindexable query patterns; JSON-everywhere loses relational clarity and constraints.

## Comparison
- vs [[mysql columns]] typed fields: typed columns win for invariants and simpl…


### Use cases
- Event payloads and sparsely populated product attributes
