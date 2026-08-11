[[mysql]] [[Configuration]] [[mysql dump]] [[mysql user]]

# cli

> The `mysql` CLI is the interactive client — connect, run SQL, import/export; auth plugins decide if `-p` works.

---

## Mental model

**Say it in one breath:** `mysql` speaks the wire protocol; on Debian/Ubuntu, OS `root` often uses `auth_socket`, so `mysql -u root -p` fails until you change the plugin or use `sudo`.

```txt
mysql client ──► Unix socket (localhost) or TCP (127.0.0.1)
                      │
                      ├─ auth_socket  → OS user must match
                      └─ password plugin → -p / .my.cnf
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **auth_socket** | Login as matching OS user | “Ubuntu root MySQL has no password path by default.” |
| **caching_sha2_password** | MySQL 8 default password plugin | “Old clients may need TLS or `allowPublicKeyRetrieval`.” |
| **Unix socket** | Local IPC path | “`localhost` → socket; IP → TCP.” |
| **SOURCE** | Run a SQL file in-session | “Import with FK checks considered.” |
| **mysqlcheck** | Table check/repair helper | “Health check before blaming the app.” |

---

## Standard config / commands

```bash
mysql -u root -p
sudo mysql -u root          # auth_socket path on Ubuntu
mysql -h 127.0.0.1 -u app -p db_name

mysqlcheck -u root -p mydb mytable
mysqld --verbose --help | grep -A1 'Default options'

mysqldump --no-create-info db_name > data-only.sql
```

```sql
SELECT user, host, plugin FROM mysql.user;

-- password-based root (dev only)
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'secret';
FLUSH PRIVILEGES;

-- back to socket auth
ALTER USER 'root'@'localhost' IDENTIFIED WITH auth_socket;
FLUSH PRIVILEGES;

SET FOREIGN_KEY_CHECKS = 0;
SOURCE safe_dump.sql;
SET FOREIGN_KEY_CHECKS = 1;
```

| Knob | Why it matters |
|------|----------------|
| `-h 127.0.0.1` vs no `-h` | TCP vs socket; grants differ by host |
| Auth plugin | Explains ERROR 1698 |
| `FOREIGN_KEY_CHECKS=0` | Bulk load only for trusted dumps |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `ERROR 1698` Access denied root | `plugin` = `auth_socket` | `sudo mysql` or switch plugin (dev) |
| Password always wrong | Plugin / wrong host | Match `user@host`; check plugin |
| Can’t connect remotely | bind-address / grants / firewall | Listen + `user@'%'` carefully + TLS |
| Import FK errors | Order of tables | Temporarily disable FK checks for trusted dump |
| Client too old for sha2 | Auth plugin errors | Upgrade client or adjust user plugin |

---

## Gotchas

> [!WARNING]
> **`ERROR 1698` is not “wrong password”** — it’s socket auth rejecting password login.

> [!WARNING]
> **Disabling FK checks is a footgun** — re-enable and validate; never leave off in app code.

> [!WARNING]
> **Root with a weak password over TCP** — fine for local docker lab; not for exposed hosts.

---

## When NOT to use

- **Interactive CLI as the application’s data access** — use a driver + pool.
- **Changing production root to `mysql_native_password` for convenience** — create least-privilege users instead.
- **Blind `FOREIGN_KEY_CHECKS=0` in application paths** — dumps/migrations only.

---

## Related

[[mysql]] [[Configuration]] [[mysql dump]] [[mysql user]] [[mysql Privileges]] [[SQL error]]
