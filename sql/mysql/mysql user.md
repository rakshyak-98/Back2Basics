
```sql
CREATE USER 'username'@'host' IDENTIFIED BY 'password';
```
- user just created but never granted perms
- perms were revoked
- migration/restore created empty grants

```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';
DROP USER 'username'@'host';
DROP USER 'app'@'%';
```

## For plugin (legacy clients)

```sql
ALTER USER 'app'@'%' IDENTIFIED WITH mysql_native_password BY 'newpwd';
SET PASSWORD FOR 'user'@'host' = PASSWORD('new');
```

```sql
GRANT ALL PRIVILEGES ON dbname.* ON dbname.* TO 'username'@'host';
FLUSH PRIVILEGES;

GRANT SELECT, INSERT, UPDATE, DELETE ON mydb.* TO 'app'@'%';
```