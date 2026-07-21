role -> can own objects and have privileges.
user -> A role that can log in.
Internally PostgreSQL stores both as roles.

```txt
PostgreSQL Server
│
├── Roles (Users)
│   ├── postgres
│   ├── app_user
│   ├── readonly_user
│   └── admin
│
├── Database: inventory
├── Database: payroll
└── Database: analytics
```
- A user exists at the server (cluster) level, not inside a single database.

```sql
\du -- List users
\l -- List database
\z users -- Show tables privileges
\conninfo -- show curretn connection info
```


```sql
CREATE USER app_user PASSWORD 'secret';

CREATE DATABASE inventory OWNER app_user;

\c inventory

GRANT USAGE, CREATE
ON SCHEMA public
TO app_user;

GRANT ALL PRIVILEGES
ON ALL TABLES IN SCHEMA public
TO app_user;

ALTER DEFAULT PRIVILEGES
IN SCHEMA public
GRANT ALL
ON TABLES
TO app_user;
```

```sql
CREATE USER myuser WITH PASSWORD 'mypassword';
-- or
CREATE ROLE app_user LOGIN PASSWROD 'secret';

CREATE DATABASE mydb OWNER myuser;
```

```sql
ALTER USER app_user PASSWORD 'new_password';

ALTER USER app_user RENAME TO inventory_user;

DROP USER app_user;

ALTER ROLE app_user LOGIN;
ALTER ROLE app_user NOLOGIN;
ALTER ROLE admin SUPERUSER;
ALTER ROLE admin NOSUPERUSER;
```

Transfer ownership first

```sql
REASSIGN OWNED BY app_user TO postgres;
DROP OWNED BY app_user;
DROP USER app_user;
```

```sql
ALTER USER app_user CREATEDB;
ALTER USER myuser WITH SUPERUSER;
```

```sql
ALTER ROLE app_user CREATEDB;
ALTER ROLE app_user NOCREATEDB;
ALTER ROLE app_user CREATEROLE;
ALTER ROLE replica REPLICATION;
```

```sql
-- database privileges
GRANT CONNECT
ON DATABASE inventory
TO app_user;

GRANT ALL PRIVILEGES
ON DATABASE inventory
TO app_user;

-- Schema privileges
GRANT USAGE
ON SCHEMA public
TO app_user;

GRANT CREATE
ON SCHEMA public
TO app_user;

-- Table privileges
GRANT SELECT
ON TABLE users
TO app_user;

GRANT SELECT, INSERT, UPDATE, DELETE
ON TABLE users
TO app_user;

GRANT ALL PRIVILEGES
ON TABLE users
TO app_USEr;

GRANT SELECT
ON ALL TABLES IN SCHEMA public
TO readonly;

ALTER DEFAULT PRIVILEGES
IN SCHEMA public
GRANT SELECT
ON TABLES
TO readonly;

```

```sql
-- All tables
GRANT SELECT
ON ALL TABLES IN SCHEMA public
TO readonly;

ALTER DEFAULT PRIVILEGES
IN SCHEMA public
GRANT SELECT
ON TABLES
TO readonly;
```

```sql
REVOKE INSERT
ON TABLE users
FROM app_user;
```

```sql
CREATE TABLE users (...);
```
- The creator becomes the owner.

```sql
ALTER TABLE users
OWNER TO app_user; -- Transfer ownership
```

```sql
-- Group roles Instead of granting permissions to each user
CREATE ROLE developers;

GRANT developers TO alice;
GRANT developers TO bob;

GRANT SELECT, INSERT
ON ALL TABLES IN SCHEMA public
TO developers;
```

```sql
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
```