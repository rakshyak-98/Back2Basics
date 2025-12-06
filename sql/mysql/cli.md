```bash
mysql -u root -p
```
`ERROR 1698 (28000): Access denied for user 'root'@'localhost'`

- On Ubuntu/Debian, MySQL's root account users auth_socket (plugin).
- root can log in only via OS user = root, not via password. 

Why `mysql -u root -p` fails
- because MySQL root has no password-based authentication enabled.
- so any password (even correct) is rejected.

```sql
SELECT user, host, plugin FROM mysql.user;
```

> [!INFO]
> `SHOW PLUGINS`
> `SELECT * FROM information_scheme.plugins`
> `SELECT plugin_name, plugin_status FROM information_schema.plugins WHERE plugin_type = 'AUTHENTICATION'`

**Fix: change plugin to password-based**

```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
FLUSH PRIVILEGES;
```

**Revert back to auth_socket**

```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH auth_socket;
FLUSH PRIVILEGES;
```

```bash
mysqlcheck -u root -p mydb mytable; # check db table status.
```

```bash
mysqld --verbose --help | grep -A1 "Default options"
```

### Dump database
```bash
mysqldump --no-create-info <database> > only-data.sql
```

> [!NOTE]
> for bulk append imports, temporarily disable FK check.
```mysql
SET FOREIGN_KEY_CHECKS = 0;
SOURCE safe_dump.sql;
```
