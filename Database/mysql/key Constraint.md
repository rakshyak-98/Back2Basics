[[mysql table]] [[mysql index]] [[mysql normalization]] [[ACID]] [[MySQL Error]] [[mysql engine]]

# key Constraint

> MySQL constraints—PRIMARY KEY, UNIQUE, FOREIGN KEY, CHECK (8.0.16+)—that enforce row validity at insert/update time.

```txt
        key Constraint ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Constraint questions check PRIMARY/UNIQUE/FK/CHECK literacy, InnoDB-only FKs,…

## Sources
- [MySQL Reference Manual — CREATE TABLE](https://dev.mysql.com/doc/refman/en/create-table.html) — deep-dive
- [MySQL Reference Manual — FOREIGN KEY Constraints](https://dev.mysql.com/doc/refman/en/create-table-foreign-keys.html) — deep-dive

## Key Concepts
- **PRIMARY KEY / UNIQUE:** identity and uniqueness enforced by indexes.
- **FOREIGN KEY:** referential integrity; InnoDB only; child indexes required.
- **CHECK:** expression constraints (MySQL 8.0.16+).
- **Named constraints:** clearer error text and safer drops.

## Technical Details
```sql
PRIMARY KEY (id),
UNIQUE KEY uk_users_email (email),
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT,
CHECK (balance >= 0)
```

- Foreign keys:

- Require indexed parent/child columns (index created automatically on child if…
- `ON DELETE CASCADE` propagates deletes—use deliberately
- InnoDB only ([[mysql engine]])

- Naming: explicit constraint names (`CONSTRAINT fk_orders_user`) make [[MySQL …

## Mistakes to Avoid
- **Mistake:** Relying on FKs with non-InnoDB engines
- **Mistake:** Blind `ON DELETE CASCADE` on large graphs
- **Mistake:** Unnamed constraints that produce opaque error text during incide…

## Pros/Cons or Trade-offs
- **Pro:** Database rejects invalid states; FKs document relationships.
- **Con:** Cascades can surprise; FK checks add write overhead; some legacy engines/settings disable FKs.

## Comparison
- vs application-only validation: app checks are necessary for UX but race-pron…


### Use cases
- Orders referencing users with `ON DELETE RESTRICT` so you cannot wipe custome…
