[[SQL]] [[Database]]

GIN (Generalized Inverted Index) -> PostgreSQL supports GIN on `JSONB`, you can efficiently search fields inside the JSON without extracting them into separate columns.

Find all rows where `autoRenew` is `true`:
```sql
SELECT *
FROM audit_log
WHERE new_data @> '{"config":{"autoRenew":true}}';
```