<!-- note-strategy: runbook -->
[[mysql]] [[cli]] [[mysql connection]] [[MySQL Engines]]

# MySQL Error

> Decode common MySQL failures — crashed tables, access denied, socket perms, client bind mistakes, apt key, and service start.

---

## Index

- [[#Triage (when things break)]]
- [[#Preconditions]]
- [[#Steps]]
- [[#Verification]]
- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Rollback]]
- [[#Escalation]]
- [[#Related]]

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Table marked as crashed | Engine MyISAM? | Backup `.MYD`/`.MYI`; `REPAIR TABLE` |
| Access denied root@_gateway | No matching user@host | CREATE USER for that host; RDS: app user |
| Socket error (13) | Perms on sock/dir | Fix group/perms; use TCP `-h 127.0.0.1` |
| mysql.service Error 22 | `journalctl`, my.cnf | Fix config/datadir perms; clear bad args |
| Bind parameters must be array | mysql2 execute + object | Array binds, `query()`, or `namedPlaceholders` |
| apt NO_PUBKEY | Repo key missing | Import vendor key |

---

## Preconditions

…

## Steps

1. …

## Verification

```bash
# …
```

## Mental model

**Say it in one breath:** Read the SQLSTATE/error number first; match class (authentication, file/socket, storage engine, client API); fix the layer that owns it — don’t `REPAIR` InnoDB like MyISAM.

```txt
Client error ──► auth / socket / bind API
Server error ──► table/engine / config / privileges
Install error ──► mysqld won’t start (journalctl)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **1045** | Access denied | “Wrong user@host or password.” |
| **2002** | Can’t reach socket/TCP | “Server down or socket perms.” |
| **145 / crashed** | MyISAM mark crashed | “Backup then REPAIR; not for InnoDB .ibd.” |
| **namedPlaceholders** | mysql2 object binds | “execute() wants arrays unless enabled.” |

---

## Standard config / commands

```bash
sudo systemctl status mysql
journalctl -xeu mysql.service
# socket warning /nonexistent home for mysql user:
sudo usermod -d /var/lib/mysql mysql
sudo usermod -s /usr/sbin/nologin mysql
```

```js
// mysql2: prefer query for SET ? object shorthand, or:
const pool = mysql.createPool({ namedPlaceholders: true, /* … */ })
// ? placeholders → array; :name → object
```

```bash
# apt NO_PUBKEY for MySQL repo (example key)
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B7B3B788A8D3785C
```

| Knob | Why it matters |
|------|----------------|
| Engine of table | REPAIR helps MyISAM; InnoDB needs restore/recovery |
| RDS | No remote root; SG + app user |
| `pool.query` vs `execute` | Object `SET ?` behaves differently |

---

## Gotchas

> [!WARNING]
> **REPAIR TABLE ≠ InnoDB fix** — don’t treat `.ibd` corruption like MyISAM.

> [!WARNING]
> **`su` /nonexistent warning** — mysql system user home; usually harmless but noisy; set home to datadir if needed.

---

## When NOT to use

- **Guessing REPAIR on production InnoDB** — restore from backup / use vendor recovery.
- **Disabling authentication to “unblock”** — fix the account/SG instead.

---

## Rollback

1. …

## Escalation

…

## Related

[[cli]] [[mysql connection]] [[mysql user]] [[MySQL Engines]] [[Configuration]]
