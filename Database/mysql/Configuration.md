[[mysql]] [[cli]] [[mysql dump]] [[SQL Configurations]]

# Configuration

> MySQL config is defaults + `my.cnf` / `.my.cnf` — client prefs, dump flags, and server knobs in one place.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Sections in option files map to programs — `[client]` shared, `[mysql]` CLI, `[mysqld]` server, `[mysqldump]` dumps.

```txt
~/.my.cnf  /  /etc/mysql/my.cnf
  [client]      user/host defaults for all clients
  [mysql]       pager, prompt
  [mysqld]      server: buffers, sql_mode, …
  [mysqldump]   dump safety flags
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Option file** | INI of defaults | “We pin dump and CLI defaults so humans don’t forget flags.” |
| **sql_safe_updates** | Block wide UPDATE/DELETE | “No WHERE (or LIMIT-less) mass updates from CLI.” |
| **single-transaction** | Consistent InnoDB dump | “Dump without locking every table for RR snapshot.” |
| **routines / triggers** | Stored programs in dump | “Default mysqldump omits them — pass flags.” |
| **Order of files** | Later overrides earlier | “Know which my.cnf won.” |

---

## Standard config / commands

```ini
# ~/.my.cnf (chmod 600 — contains secrets)
[client]
user=myuser
password=mypassword
host=127.0.0.1

[mysql]
pager=less -S
prompt="\u@\h [\d]> "

[mysqldump]
quick=TRUE
single-transaction=TRUE

[mysqld]
# server-side (needs restart / SET GLOBAL where allowed)
# sql_safe_updates=1   # also: SET sql_safe_updates=1 for session
```

```bash
mysqld --verbose --help | grep -A1 'Default options'   # which files are read
mysqldump --routines --triggers db_name > dump.sql
```

| Knob | Why it matters |
|------|----------------|
| `single-transaction` | Consistent InnoDB backup without `LOCK TABLES` for all |
| `--routines` / `--triggers` | Otherwise missing procedures/functions/triggers |
| `pager=less -S` | Ops readability for wide result sets |
| File mode `600` | Password in `.my.cnf` must not be world-readable |

Session safe updates:

```sql
SET sql_safe_updates = 1;
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Wrong user/host used | Option file order / `mysql --print-defaults` | Fix section; avoid conflicting files |
| Dump missing procedures | Dump flags | Add `--routines` (and `--triggers`) |
| Unsafe mass UPDATE blocked | `sql_safe_updates` | Add keyed WHERE or turn off for that session |
| Dump locked writers | Not using single-transaction | Enable for InnoDB; avoid MyISAM mix |
| Password leaked | `.my.cnf` perms | `chmod 600`; prefer secrets manager in prod |

---

## Gotchas

> [!WARNING]
> **`mysqldump` skips routines by default** — always decide explicitly for prod backups.

> [!WARNING]
> **Client `[mysqld]` knobs do nothing** — server options belong on the server host’s config.

> [!WARNING]
> **Passwords in `.my.cnf`** — convenient for ops laptops; never commit them.

---

## When NOT to use

- **Putting prod root passwords in world-readable config** — use IAM/secrets + least privilege.
- **Copying laptop `.my.cnf` into containers as the security model** — inject env/secrets at runtime.
- **Tuning random buffer sizes without metrics** — measure first ([[SQL Configurations]]).

---

## Related

[[cli]] [[mysql]] [[mysql dump]] [[SQL Configurations]] [[mysql user]] [[TLS (Transport Layer Security)]]
