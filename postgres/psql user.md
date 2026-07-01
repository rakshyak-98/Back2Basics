```sql

-- List users
\du 

-- List database
\l

```

```sql
CREATE USER myuser WITH PASSWORD 'mypassword';
CREATE DATABASE mydb OWNER myuser;
```

```sql
ALTER USER myuser CREATEDB;
ALTER USER myuser WITH SUPERUSER;
```

```sql
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
```