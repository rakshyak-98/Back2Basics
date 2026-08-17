[[mysql]] [[mysql connection]] [[mysql query]] [[variables]]

# cli

> The `mysql` command-line client—interactive [[SQL]] shell and script runner for administering local or remote MySQL servers.

```txt
        cli ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Ops interviews expect fluent CLI: connect with TLS, run one-shot `-e`, script…

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

- Common modes:

```bash
# Run one statement
mysql -e "SHOW STATUS LIKE 'Threads_connected';"

# Execute script file
mysql mydb < schema.sql

# Skip column names in output (automation)
mysql -N -e "SELECT id FROM users LIMIT 5;"
```

- Interactive essentials:

```sql
SHOW DATABASES;
USE myapp;
SHOW TABLES;
DESCRIBE users;
\G   -- vertical output for wide rows (in mysql client)
```

- Secure passwords: prefer `mysql_config_editor` login paths over plaintext `-p…

## Mistakes to Avoid
- **Mistake:** Putting production passwords in shell history or CI logs
- **Mistake:** Running unreviewed SQL files against production without a transa…
- **Mistake:** Forgetting `--ssl-mode=REQUIRED` on public networks

## Pros/Cons or Trade-offs
- **Pro:** Universal, scriptable, works over SSH tunnels everywhere MySQL does.
- **Con:** Easy to leak passwords in shell history; interactive use does not replace monitored migration tooling.

## Comparison
- vs GUI clients: CLI is faster for scripts and remote jump hosts


### Use cases
- Incident checks (`Threads_connected`), applying schema scripts, and ad-hoc EX…
