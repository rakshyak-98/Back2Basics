<!-- note-strategy: operational -->
[[mysql]] [[mysql engine]] [[MySQL storage]] [[write-ahead logging]]

# MySQL Engines

> Engine files are how MySQL keeps table bytes on disk — `.ibd` is InnoDB’s per-table data when `innodb_file_per_table` is on.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** With file-per-table, each InnoDB table lives in `datadir/db/table.ibd` (pages, indexes, not a CSV you edit).

```txt
datadir/
  dbname/
    table.ibd     ← InnoDB data + indexes (file-per-table)
    # MySQL 8: metadata in data dictionary (not .frm like 5.7)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **`.ibd`** | InnoDB tablespace file | “One file per table when file-per-table is ON.” |
| **innodb_file_per_table** | Separate vs system tablespace | “ON lets you reclaim space per table more easily.” |
| **Data dictionary** | MySQL 8 metadata store | “You can’t just copy `.ibd` without matching DD.” |
| **CSV engine** | Table stored as CSV text | “Handy for interchange; not for concurrent OLTP.” |
| **Binary pages** | Internal InnoDB layout | “Not for humans — use SQL / dump tools.” |

### Engines vs files (one line each)

| Engine | On disk (typical) |
|--------|-------------------|
| InnoDB | `.ibd` (+ redo in redo logs) |
| CSV | `.CSV` + `.CSM` metadata |
| MEMORY | Nothing durable |

---

## Standard config / commands

```ini
# my.cnf
[mysqld]
innodb_file_per_table = 1
datadir = /var/lib/mysql
```

```mysql
SHOW VARIABLES LIKE 'datadir';
SHOW VARIABLES LIKE 'innodb_file_per_table';

CREATE TABLE export_like (
  id INT NOT NULL,
  name VARCHAR(100) NOT NULL
) ENGINE=CSV;
```

| Knob | Why it matters |
|------|----------------|
| `innodb_file_per_table` | Per-table `.ibd` vs shared system tablespace |
| `datadir` | Where to look during disk / backup incidents |
| CSV engine | Readable files; table-level quirks / locking |

Path example: `/var/lib/mysql/your_db/your_table.ibd`

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Table won’t open after copy | Copied `.ibd` alone | Transportable tablespace / dump-restore — never raw copy casually |
| Disk full on one DB | Large `.ibd` files | Archive/purge; `OPTIMIZE` after big deletes (plan locks) |
| “Missing tablespace” | File deleted under mysqld | Restore from backup; don’t invent empty `.ibd` |
| CSV table corrupt | Manual file edits | Fix via SQL or recreate from known-good CSV |
| Space not returned after DELETE | InnoDB file size | Expected without rebuild/truncate strategy |

---

## Gotchas

> [!WARNING]
> **Don’t move `.ibd` without matching metadata** — MySQL 8 data dictionary must agree or the table won’t open.

> [!WARNING]
> **`.ibd` is not a backup format** — use `mysqldump`, physical backup tools, or official tablespace export.

> [!WARNING]
> **CSV engine ≠ InnoDB** — no transactions/FK; fine for dump-shaped tables, bad for hot paths.

---

## When NOT to use

- **Hand-editing `.ibd`** — always wrong.
- **CSV engine for multi-writer apps** — use InnoDB; export CSV when needed.
- **Assuming file delete = clean drop** — drop via SQL so the dictionary stays consistent.

---

## Related

[[mysql engine]] [[mysql]] [[MySQL storage]] [[mysql dump]] [[write-ahead logging]] [[memory engine]]
