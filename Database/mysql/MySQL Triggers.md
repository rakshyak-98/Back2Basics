[[mysql triggers]] [[mysql Programmable SQL]] [[mysql table]]

# MySQL Triggers

> Automatic stored procedures attached to table events—same concept as [[mysql triggers]]; this note covers operational patterns and pitfalls.

## Audit pattern

```sql
CREATE TRIGGER audit_orders AFTER UPDATE ON orders
FOR EACH ROW
INSERT INTO orders_audit(order_id, old_total, new_total, changed_at)
VALUES (OLD.id, OLD.total, NEW.total, NOW());
```

## Testing

Triggers run in the same transaction as the triggering statement—rollback undoes both.

## Migration tip

Export trigger definitions with `mysqldump --triggers` during [[mysql dump]].

## Sources

- MySQL Reference Manual — [Triggers](https://dev.mysql.com/doc/refman/en/triggers.html)
