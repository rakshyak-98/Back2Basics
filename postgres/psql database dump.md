
```bash
pg_dump -U <username> -d <database_name> > database.sql; # Dump local PostgreSQL database
pg_dump -U <username> -d <database_name> -f inventory_db.dump # Dump in custom (compressed) format (recommended) 

pg_dump -h localhost -p 5432 -U postgres -d inventory_db -f inventory_db.dump # Dump with host and port

ssh user@remote-server "pg_dump -U postgres inventory_db" > inventory_db.sql
ssh user@remote-server "pg_dump -Fc -U postgres inventory_db" > inventory_db.dump # Compressed

```


restore
```bash
pg_restore -U postgres -d new_database database.dump;
```