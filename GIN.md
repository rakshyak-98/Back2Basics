[[SQL]] [[Database]]

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

