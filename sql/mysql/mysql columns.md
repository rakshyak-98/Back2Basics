```mysql
ALTER TABLE table_name
MODIFY COLUMN column_name data_type FIRST|AFTER other_column_name
```

> [!NOTE]
> - You **must** specify full column definition (type, nullability, default)
> - Multiple reorder operations → better done in single statement
> - Tools like Workbench may auto-drop/recreate table internally
> - Avoid frequent reorder in production (metadata lock + table rebuild)

```mysql
ALTER TABLE Users
ADD COLUMN created_at DATETIME AFTER email;
```