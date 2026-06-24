
> [!WARNING]
> No. PostgreSQL does not support an `ON UPDATE` column attribute at the schema definition level to automatically update a column value when the row changes (unlike MySQL's `ON UPDATE CURRENT_TIMESTAMP`).
- In PostgreSQL, you must implement this behavior using a `TRIGGER`.

### Implementation via Trigger

To update a "last modified" timestamp column, you must define a function and bind it to the table.

#### 1. Define the trigger function

```sql
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

#### 2. Attach the trigger to the table

```sql
CREATE TRIGGER set_timestamp
BEFORE UPDATE ON your_table_name
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();
```