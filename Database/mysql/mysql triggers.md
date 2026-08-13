[[mysql Programmable SQL]] [[mysql table]] [[ACID]]

# mysql triggers

> Row-level actions fired automatically on INSERT/UPDATE/DELETE—enforce audit columns, cascaded logic, or guard invalid transitions.

## Example

```sql
CREATE TRIGGER orders_set_updated BEFORE UPDATE ON orders
FOR EACH ROW SET NEW.updated_at = CURRENT_TIMESTAMP;
```

## Caveats

- Hidden from application code review
- Error in trigger fails entire statement
- Complicate [[mysql data migrations]] and bulk loads (`DISABLE TRIGGER` rarely used)

See also [[MySQL Triggers]] (duplicate topic path in vault).

## Sources

- MySQL Reference Manual — [CREATE TRIGGER](https://dev.mysql.com/doc/refman/en/create-trigger.html)
