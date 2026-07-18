- automatically executes when a specific table event occurs - like an `INSERT` `UPDATE` or `DELETE`.

> [!WARNING]
> - MySQL does **not maintain dedicated logs** for trigger executions — triggers run silently within the same transaction as the statement that fired them.  
> - However, you can **implement logging manually** using one of these approaches:

- Each trigger runs
	- BEFORE or AFTER a table event
	- On INSERT, UPDATE or DELETE

```mysql
CREATE TRIGGER trigger_name(
)
BEFORE INSERT
ON tableName
FOR EACH ROW
BEGIN
	SET NEW.created_at = NOW();
END;
```

- `BEFORE` → runs before the row is written
- `AFTER` → runs after the change is committed
- `NEW` → reference to inserted/updated values
- `OLD` → reference to deleted/previous values
- `FOR EACH ROW` → trigger executes per affected row

**Example audit log**
```mysql
CREATE TRIGGER log_hotel_update
AFTER UPDATE ON hotels
FOR EACH ROW
INSERT INTO hotel_audit (hotel_id, old_name, new_name, changed_at)
VALUES (OLD.id, OLD.name, NEW.name, NOW());
```

## View all the triggers
```sql
SELECT TRIGGER_NAME FROM information_schema.TRIGGERS WHERE TRIGGER_SCHEMA = DATABASE();
```

```sql
DROP TRIGGER IF EXISTS after_hotel_update_create_pages;
```

