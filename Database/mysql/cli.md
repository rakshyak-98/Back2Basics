[[mysql]] [[mysql connection]] [[mysql query]] [[variables]]

# cli

> The `mysql` command-line client—interactive [[SQL]] shell and script runner for administering local or remote MySQL servers.

## Connect

```bash
mysql -h db.example.com -u app -p --ssl-mode=REQUIRED mydb
```

## Common modes

```bash
# Run one statement
mysql -e "SHOW STATUS LIKE 'Threads_connected';"

# Execute script file
mysql mydb < schema.sql

# Skip column names in output (automation)
mysql -N -e "SELECT id FROM users LIMIT 5;"
```

## Interactive essentials

```sql
SHOW DATABASES;
USE myapp;
SHOW TABLES;
DESCRIBE users;
\G   -- vertical output for wide rows (in mysql client)
```

Secure passwords: prefer `mysql_config_editor` login paths over plaintext `-p` on shared hosts.

## Sources

- MySQL Reference Manual — [4.5.1 mysql — The MySQL Command-Line Client](https://dev.mysql.com/doc/refman/en/mysql.html)
