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

## Allow private network host

```mysql
CREATE USER '<user>'@'<private ip>' IDENTIFIED BY '<password>';

GRANT ALL PRIVILEGES ON database_name.* TO 'nodeuser'@'<private ip>';
SHOW GRANTS FOR '<user>'@'<private ip>';
FLUSH PRIVILEGES;
```

```mysql
GRANT ALL PRIVILEGES ON hotel_cms.* TO 'nodeuser'@'192.168.3.106' IDENTIFIED BY 'password123';
FLUSH PRIVILEGES;
```