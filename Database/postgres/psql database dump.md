[[postgres]] [[psql essential]] [[migration]]

# psql database dump

> Snapshot a Postgres database to a file — `pg_dump` out, `pg_restore` (or `psql`) back in.

---

## Mental model

**Say it in one breath:** `pg_dump` reads a consistent snapshot of one DB; custom format (`-Fc`) is compressed and restore-selective; plain SQL is editable but slower to reload.

```txt
pg_dump ──► .sql (plain) or .dump (-Fc custom)
pg_restore / psql ──► target DB
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **pg_dump** | Logical backup of one database | “Not a filesystem copy of data files.” |
| **-Fc** | Custom compressed archive | “Faster restore; can pick tables.” |
| **pg_restore** | Load custom/directory dumps | “Won’t work on plain `.sql` — use `psql`.” |
| **globals** | Roles/tablespaces | “`pg_dumpall --globals-only` separately.” |

---

## Standard config / commands

```bash
# Plain SQL
pg_dump -U postgres -d inventory_db > inventory.sql
psql -U postgres -d new_db -f inventory.sql

# Custom (recommended)
pg_dump -U postgres -d inventory_db -Fc -f inventory.dump
createdb -U postgres new_db
pg_restore -U postgres -d new_db inventory.dump

# Remote via SSH
ssh user@host "pg_dump -Fc -U postgres inventory_db" > inventory.dump
```

| Knob | Why it matters |
|------|----------------|
| `-Fc` / `-Fd` | Parallel restore (`-j`), selective `-t` |
| `--no-owner` | Avoid role-mismatch failures on restore |
| `-h` / `-p` | Dump from remote host, not only local socket |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Permission denied | Role lacks SELECT on tables | Dump as superuser or grant SELECT |
| Restore role missing | Dump has OWNER TO | `--no-owner` or create roles first |
| `pg_restore` on `.sql` | Wrong tool | Use `psql -f` for plain dumps |
| Huge dump slow | Plain format / network | `-Fc`, compress, dump on same host |
| Extensions fail | Target missing extension | `CREATE EXTENSION` before restore |

---

## Gotchas

> [!WARNING]
> **One DB only** — `pg_dump` does not dump roles/cluster settings; use `pg_dumpall` for that.

> [!WARNING]
> **Active writers** — dump is consistent via MVCC snapshot, but long dumps hold that snapshot open (bloat risk).

---

## When NOT to use

- **Point-in-time recovery** — use continuous WAL archiving / PITR, not nightly logical dumps alone.
- **Multi-TB cold restore SLA** — physical base backups restore faster.

---

## Related

[[psql essential]] [[migration]] [[WAL (Write-Ahead Log)]] [[postgres]]
