[[Database]]

[notes webpage](https://sql.holt.courses/lessons/data/nodejs-and-postgresql)

> [!NOTE]
> In PostgreSQL, **creating a Foreign key constraint does not automatically create an index** on the referencing column.

## Create user

```bash
sudo -u postgres psql;
psql -h localhost -p 5432 -U username -d database_name; # login with user
```

pg has two ways to connect to a database: a client and a pool.

```sql
\du; -- view current roles

\l; -- list database
\c <db name> ; -- use the database
\dt; -- list tables
```

```sql
\dt; -- view database tables
\d <table name>; -- view the columns
```

## Constraints

```mysql
CREATE UNIQUE INDEX unique_fsd_not_null
ON hkAppNotification(floorNumber, shiftName, department)
WHERE floorNumber IS NOT NULL AND shiftName IS NOT NULL AND department IS NOT NULL;

```

## Restart the cluster

```bash

sudo pg_cttcluster 16 main stop;
sudo pg_dropcluster 16 main;
sudo pg_createcluter 16 main --start;

sudo systemctl start postgresql@16-main;
```

```bash
pg_lsclusters; # list of running clusters
sudo -u postgres psql; # connect to postgres db
```