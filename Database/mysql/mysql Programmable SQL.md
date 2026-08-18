[[mysql]] [[variables]] [[mysql function]] [[mysql triggers]]

# mysql Programmable SQL

> Dynamic SQL and stored routines inside MySQL — `PREPARE`/`EXECUTE`, procedures, functions, triggers, events.

## Mental model

**Say it in one breath:** `PREPARE` builds a statement with `?` placeholders; `EXECUTE … USING @vars` runs it; stored routines are reusable code living in the server (procedures/functions/triggers/events).

```txt
PREPARE stmt FROM 'UPDATE t SET c = ? WHERE id = ?'
SET @a = 1; SET @b = 2;
EXECUTE stmt USING @a, @b;
DEALLOCATE PREPARE stmt;
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Prepared statement** | Parse once, bind later | “Placeholders beat string concat.” |
| --- | --- | --- |
| **Stored procedure** | Callable batch of SQL | `CALL proc(…)` |
| **Function** | Returns one value in expressions | “Usable in SELECT list.” |
| **Trigger / Event** | On DML / on schedule | See sibling notes |
| **Session `@var`** | Bind values for EXECUTE | “Literals not allowed directly in USING.” |

## Standard config / commands

```sql
PREPARE stmt FROM 'UPDATE table_name SET column_name = ? WHERE id = 1';
SET @json = '[]';
EXECUTE stmt USING @json;
DEALLOCATE PREPARE stmt;

SHOW STATUS LIKE 'Prepared%';
SELECT STATEMENT_NAME, SQL_TEXT
FROM performance_schema.prepared_statements_instances;
```

| Kind | Job |
| --- | --- |
| PREPARE/EXECUTE | Dynamic SQL with binds |
| Procedure | Multi-statement workflows |
| Function | Scalar in SQL expressions |
| Trigger / Event | Auto / scheduled SQL |
| View | Named SELECT abstraction |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| EXECUTE USING literal fails | Docs require user vars | `SET @a=…; EXECUTE … USING @a` |
| Prepared leak | Status `Prepared_stmt_count` | DEALLOCATE; fix app not to leak |
| Dynamic table name | Can’t bind identifiers | Whitelist names; build carefully |
| Routine missing | Wrong schema | `SHOW PROCEDURE STATUS` / ROUTINES |

## Gotchas

> [!WARNING]
> **Identifiers can’t be `?`** — only values. Table/column names need careful whitelisting.

> [!WARNING]
> **`EXECUTE IMMEDIATE`** — MySQL Shell / other dialects; not classic mysqld SQL.

## When NOT to use

- **application-owned business logic** — keep orchestration in the service layer when you need testability/deploy independence.
- **Building SQL via string concat of user input** — use binds or reject.

## Related

[[mysql function]] [[mysql triggers]] [[mysql events 1]] [[variables]] [[mysql]]
