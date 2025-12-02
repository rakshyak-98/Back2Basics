

```sql
CREATE USER 'username'@'host' IDENTIFIED BY 'password';
```

```sql
GRANT ALL PRIVILEGES ON dbname.* ON dbname.* TO 'username'@'host';
GRANT SELECT, INSERT, UPDATE, DELETE ON mydb.* TO 'app'@'%';
```