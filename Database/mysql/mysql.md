[[Database]] [[mysql connection]] [[cli]] [[mysql query]] [[mysql dump]]

# mysql

> MySQL is the SQL server you talk to for rows — store, query, and change data over a connection.

---

## Mental model

**Say it in one breath:** Client opens a session → sends SQL → server plans/executes → returns rows or an error; engines (usually InnoDB) own storage and locks.

```txt
App / mysql CLI
  │  TCP (+TLS)
  ▼
mysqld ──► parse → optimize → execute
              │
              ├─ buffer pool / indexes
              └─ InnoDB tablespace + redo ([[write-ahead logging]])
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Session** | One client connection’s state | “Variables and temp tables live on the connection.” |
| **Schema / database** | Namespace of tables | “USE db picks the default schema for unqualified names.” |
| **InnoDB** | Default storage engine | “Transactions, row locks, crash recovery — default for prod.” |
| **Primary key** | Clustered row identity | “InnoDB stores rows by PK; secondary indexes point at it.” |
| **EXPLAIN** | Plan without running the full cost story | “I check type / key / rows before tuning.” |
| **Slow query log** | Queries over a time threshold | “Production truth for what actually hurts.” |

### How the story goes (4 steps)

1. **Connect** — user@host + authentication plugin ([[cli]], [[mysql connection]]).
2. **Qualify** — pick database; tables live under it.
3. **Run SQL** — DML/DDL; engine handles locks/WAL.
4. **Observe** — `SHOW` / `EXPLAIN` / `performance_schema` when slow or wrong.

---

## Standard config / commands

```bash
mysql -u user -p -h 127.0.0.1 db_name
mysql --auto-rehash -u user -p db_name   # tab-complete table/column names
mysql -u user -p db_name < dump.sql      # import (create DB first)
```

```mysql
SHOW DATABASES;
USE db_name;
SHOW TABLES;
SHOW COLUMNS FROM t;
SHOW INDEX FROM t;
SELECT VERSION(), DATABASE(), CURRENT_USER();
SELECT * FROM t\G          -- vertical rows (many columns)
EXPLAIN SELECT ...;
pager less -S;             -- no-wrap pager; nopager to reset
```

| Knob | Why it matters |
|------|----------------|
| Host `127.0.0.1` vs `localhost` | `localhost` often uses Unix socket; IP forces TCP |
| `pager` / `\G` | Wide result sets stay readable in ops |
| Import via stdin | Idempotent restore path; prefer `--single-transaction` dumps for InnoDB |

Table size:

```mysql
SELECT table_name,
  ROUND((data_length + index_length) / 1024 / 1024, 2) AS size_mb
FROM information_schema.tables
WHERE table_schema = 'your_db' AND table_name = 'your_table';
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Access denied | `plugin` on `mysql.user`; socket vs TCP | Fix auth plugin / use correct host ([[cli]]) |
| Can’t find table | `SELECT DATABASE();` + `SHOW TABLES` | `USE` right schema; check grants |
| Query “hangs” | `SHOW PROCESSLIST`; locks | Kill blocker; fix missing index / long txn |
| Import fails mid-file | FK / duplicate key errors | `SET FOREIGN_KEY_CHECKS=0` only for trusted dump; then re-enable |
| Results wrap / unreadable | Terminal width | `pager less -S` or `\G` |
| Wrong plan | `EXPLAIN` + stats | Add/fix index; avoid functions on indexed cols |

---

## Gotchas

> [!WARNING]
> **`localhost` ≠ TCP** — on Linux, `localhost` often means socket; remote-style grants (`user@%`) won’t match.

> [!WARNING]
> **Dropping an FK index** — InnoDB needs the supporting index; drop the foreign key first (`SHOW CREATE TABLE`).

> [!WARNING]
> **Views look like tables** — `SHOW FULL TABLES WHERE Table_type = 'VIEW'` before `DROP`.

---

## When NOT to use

- **Document / graph / pure cache workloads** — Mongo / Neo4j / Redis fit better than forcing MySQL.
- **Analytics scans over huge history** — warehouse / columnar (or read replicas + careful design), not a hot OLTP primary.
- **“Just a file DB for one laptop script”** — SQLite is simpler unless you already need MySQL operations.

---

## Related

[[cli]] [[mysql connection]] [[mysql query]] [[mysql index]] [[mysql transaction]] [[mysql engine]] [[mysql dump]] [[ACID]] [[write-ahead logging]]
