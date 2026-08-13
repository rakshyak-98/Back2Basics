[[mysql]] [[mysql Privileges]] [[mysql connection]]

# mysql user

> MySQL account definitions (`user`@`host`) with authentication plugins and privilege grants—principle of least privilege for applications and humans.

## Create application user

```sql
CREATE USER 'app'@'10.%' IDENTIFIED BY 'strong-password' REQUIRE SSL;
GRANT SELECT, INSERT, UPDATE, DELETE ON myapp.* TO 'app'@'10.%';
FLUSH PRIVILEGES;
```

## Authentication plugins

- `caching_sha2_password` — default MySQL 8
- `mysql_native_password` — legacy clients

## Inspect

```sql
SELECT user, host, plugin FROM mysql.user;
SHOW GRANTS FOR 'app'@'10.%';
```

Never use `root` for application connections.

## Sources

- MySQL Reference Manual — [CREATE USER](https://dev.mysql.com/doc/refman/en/create-user.html)
- MySQL Reference Manual — [Account Management](https://dev.mysql.com/doc/refman/en/account-management.html)
