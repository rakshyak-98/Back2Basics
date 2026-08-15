[[mysql table]] [[mysql index]] [[mysql normalization]] [[ACID]] [[MySQL Error]] [[mysql engine]]

# key Constraint

> MySQL constraints—PRIMARY KEY, UNIQUE, FOREIGN KEY, CHECK (8.0.16+)—that enforce row validity at insert/update time.

## Interview Relevance

Constraint questions check PRIMARY/UNIQUE/FK/CHECK literacy, InnoDB-only FKs, and why named constraints make [[MySQL Error]] messages actionable. Ties to [[ACID]] consistency as declared rules.

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

Foreign keys:

- Require indexed parent/child columns (index created automatically on child if missing)
- `ON DELETE CASCADE` propagates deletes—use deliberately
- InnoDB only ([[mysql engine]])

Naming: explicit constraint names (`CONSTRAINT fk_orders_user`) make [[MySQL Error]] messages actionable.

## Real-World Applications

Orders referencing users with `ON DELETE RESTRICT` so you cannot wipe customers who still have orders. Example: `CHECK (balance >= 0)` rejects bad ledger writes even if the application bug slips through.

## Pros/Cons or Trade-offs

- **Pro:** Database rejects invalid states; FKs document relationships.
- **Con:** Cascades can surprise; FK checks add write overhead; some legacy engines/settings disable FKs.

## Comparison

vs application-only validation: app checks are necessary for UX but race-prone without DB constraints. vs [[mysql normalization]]: normalization designs tables; constraints enforce the relationships that normalization implies.

## Mistakes to Avoid

- Relying on FKs with non-InnoDB engines — they are ignored or unavailable.
- Blind `ON DELETE CASCADE` on large graphs — accidental mass deletes.
- Unnamed constraints that produce opaque error text during incidents.
