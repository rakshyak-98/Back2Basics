[[MySQL CLI]] [[INDEX]]

# Database/mysql CLI

> mysql client CLI — connect, batch SQL, and interactive meta-commands.

---

## mysql client

From [[MySQL CLI]].

```bash
mysql -h db.example.com -u app -p --ssl-mode=REQUIRED mydb
```

```bash
# Run one statement
mysql -e "SHOW STATUS LIKE 'Threads_connected';"

# Execute script file
mysql mydb < schema.sql

# Skip column names in output (automation)
mysql -N -e "SELECT id FROM users LIMIT 5;"
```
