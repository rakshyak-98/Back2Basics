[[SQL]] [[Database]]

# GIN

> One-line: what / why for **GIN** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

GIN (Generalized Inverted Index) -> PostgreSQL supports GIN on `JSONB`, you can efficiently search fields inside the JSON without extracting them into separate columns.
Find all rows where `autoRenew` is `true`:
```sql
SELECT *
FROM audit_log
WHERE new_data @> '{"config":{"autoRenew":true}}';
```
GIN (Generalized Inverted Index) -> PostgreSQL index type optimized for values containing multiple searchable elements
```txt
-- instead of
row -> Value
-- GIN stores
element -> list of rows containing that element -- this is called inverted index
-- GIN Index
go         -> [1, 3]
postgres   -> [1]
backend    -> [1]
flutter    -> [2]
mobile     -> [2]
docker     -> [3]
```

## Standard config / commands

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
