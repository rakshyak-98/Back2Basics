[[mysql table]] [[mysql index]] [[mysql normalization]] [[ACID]]

# key Constraint

> MySQL constraints—PRIMARY KEY, UNIQUE, FOREIGN KEY, CHECK (8.0.16+)—that enforce row validity at insert/update time.

## Types

```sql
PRIMARY KEY (id),
UNIQUE KEY uk_users_email (email),
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT,
CHECK (balance >= 0)
```

## Foreign keys

- Require indexed parent/child columns (index created automatically on child if missing)
- `ON DELETE CASCADE` propagates deletes—use deliberately
- InnoDB only ([[mysql engine]])

## Naming

Explicit constraint names (`CONSTRAINT fk_orders_user`) make [[MySQL Error]] messages actionable.

## Sources

- MySQL Reference Manual — [CREATE TABLE Constraints](https://dev.mysql.com/doc/refman/en/create-table.html)
- MySQL Reference Manual — [FOREIGN KEY Constraints](https://dev.mysql.com/doc/refman/en/create-table-foreign-keys.html)
