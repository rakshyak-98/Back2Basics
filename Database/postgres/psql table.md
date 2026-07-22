
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

#### 3. Attach schema

```sql
SET search_path to <schema1>, <scehma2>;

SELECT * FROM users;
```
- PostgreSQL first looks for: `<current_user>.users`  `public.users`, if not found, it returns an error

```sql
psql "postgresql://drm_tester:admin@localhost:5432/drm_streaming" \
  -c 'CREATE SCHEMA IF NOT EXISTS ott;'
```

## Table details

Schema -> The namespace containing the table (e.g., `public` `sales` `auth`) Multiple schemas can have tables with the same name.

Type -> The relation type. Common values: `table` `partitioned table` `foreign table`.

Owner -> The PostgreSQL role (user) that owns the table. The owner has special privileges, such as altering or dropping the table.

## Schema

A schema is a namespace inside a database that groups related database objects.

It can contain: tables, views, indexes, sequences, functions, types.
A schema helps organize objects and prevents name conflicts.

```txt
PostgreSQL Server
└── Database
    ├── Schema (public)
    │   ├── users
    │   ├── orders
    │   └── products
    ├── Schema (sales)
    │   ├── invoices
    │   └── customers
    └── Schema (analytics)
        ├── reports
        └── events
```

> [!NOTE]
> - Schema names are unique within a database, not across different databases.
> - Different schemas can contain tables with the same name.
> - Every object belongs to exactly one schema.
> - If you omit the schema name, PostgreSQL resolves it using the `saerch_path`.

**Why use schemas** -> instead of putting every table into one namespace

```text
public.users
public.orders
public.products
public.logs
public.audit
```

```text
auth.users
sales.orders
inventory.products
audit.logs
```
- you can have two tables with the same name in different schema.

### Access control

```sql
GRANT USAGE ON SCHEMA sales to analyst;
```
the analyst can access objects in `sales` without being granted access to every schema.

```sql
CREATE SCHEMA sales;

CREATE TABLE sales.orders (
	id INT PRIMARY KEY
)

DROP SCHEMA sales;
DROP SCHEMA sales CASCADE; -- Drop schema and all objects
```

```sql
SELECT * FROM sales.orders; 
```

```sql
\dn; -- view schemas
\dt sales.* -- list tables in a schema
```