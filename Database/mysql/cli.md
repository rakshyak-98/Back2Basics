[[mysql]] [[mysql connection]] [[mysql query]] [[variables]]

# cli

> The `mysql` command-line client—interactive [[SQL]] shell and script runner for administering local or remote MySQL servers.





## Interview Relevance
Ops interviews expect fluent CLI: connect with TLS, run one-shot `-e`, script restores, and avoid putting passwords on shared command lines. Shows you can inspect servers without a GUI.

## Sources
- [MySQL Reference Manual — mysql Command-Line Client](https://dev.mysql.com/doc/refman/en/mysql.html) — deep-dive

## Key Concepts
- **Interactive shell and batch runner:** same binary for exploration and automation.
- **Connection flags:** host, user, database, SSL mode.
- **Output control:** `-N` / `-B` for scripts; `\G` for wide rows interactively.
- **Secret hygiene:** prefer login paths over plaintext `-p` on shared hosts.

## Technical Details
```bash
mysql -h db.example.com -u app -p --ssl-mode=REQUIRED mydb
```

Common modes:

```bash
# Run one statement
mysql -e "SHOW STATUS LIKE 'Threads_connected';"

# Execute script file
mysql mydb < schema.sql

# Skip column names in output (automation)
mysql -N -e "SELECT id FROM users LIMIT 5;"
```

Interactive essentials:

```sql
SHOW DATABASES;
USE myapp;
SHOW TABLES;
DESCRIBE users;
\G   -- vertical output for wide rows (in mysql client)
```

Secure passwords: prefer `mysql_config_editor` login paths over plaintext `-p` on shared hosts.

## Real-World Applications
Incident checks (`Threads_connected`), applying schema scripts, and ad-hoc EXPLAIN. Example: on-call runs `mysql -e "SHOW FULL PROCESSLIST"` via bastion to find a stuck transaction without opening a GUI.

## Pros/Cons or Trade-offs
- **Pro:** Universal, scriptable, works over SSH tunnels everywhere MySQL does.
- **Con:** Easy to leak passwords in shell history; interactive use does not replace monitored migration tooling.

## Comparison
vs GUI clients: CLI is faster for scripts and remote jump hosts; GUIs help browse schemas. vs application drivers: CLI is for humans/ops; pools and prepared statements live in app code ([[mysql connection]]).

## Mistakes to Avoid
- Putting production passwords in shell history or CI logs.
- Running unreviewed SQL files against production without a transaction/backup plan.
- Forgetting `--ssl-mode=REQUIRED` on public networks.
