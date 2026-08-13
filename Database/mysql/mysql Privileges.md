<!-- note-strategy: operational -->
[[mysql]] [[mysql user]] [[cli]]

# mysql Privileges

> GRANT/REVOKE who can read, write, or admin which databases — login alone is not permission.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** A MySQL account is `'user'@'host'`; privileges are granted at global (`*.*`), DB (`db.*`), table, or column scope. `USAGE` means “can authenticate, nothing else.”

```txt
CREATE USER ──► empty (USAGE)
GRANT SELECT… ON db.* ──► can read that DB
FLUSH PRIVILEGES ──► reload grant tables (rarely needed after GRANT in modern MySQL)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **GRANT** | Give privileges | “Least privilege: SELECT/INSERT only for the app.” |
| **REVOKE** | Take privileges away | “Drop GRANT OPTION so users can’t escalate.” |
| **USAGE** | Login placeholder | “Shows up when the user has no real rights.” |
| **SHOW GRANTS** | What this account has | “Debug access denied starting here.” |
| **host** | Where they may connect from | `'app'@'%'` vs `'app'@'10.%'` matters. |

---

## Standard config / commands

```sql
SHOW GRANTS FOR 'username'@'host';
SHOW PRIVILEGES;

GRANT SELECT, INSERT, UPDATE, DELETE ON db_name.* TO 'user'@'host';
GRANT ALL PRIVILEGES ON db_name.* TO 'user'@'host';

REVOKE ALL PRIVILEGES ON db_name.* FROM 'user'@'host';
REVOKE GRANT OPTION ON *.* FROM 'user'@'%';
```

| Knob | Why it matters |
|------|----------------|
| Scope `db.*` vs `*.*` | Global ALL is a prod footgun |
| `'user'@'host'` | Same name, different host = different account |
| `WITH GRANT OPTION` | Lets the user grant to others — avoid for apps |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Access denied for SELECT | `SHOW GRANTS` | GRANT needed privs on right scope |
| Can login, can do nothing | Only USAGE | GRANT real privileges |
| Works locally, fails remotely | Host part of account | Create `'user'@'%'` or specific IP |
| Still denied after GRANT | Wrong user@host / cached | Connect as that account; re-check grants |

---

## Gotchas

> [!WARNING]
> **`IDENTIFIED BY` on GRANT (old style)** — prefer `CREATE USER` then `GRANT`; don’t mix mental models.

> [!WARNING]
> **Partial revokes** — revoking ALL on `db.*` doesn’t remove global privileges.

---

## When NOT to use

- **application-level authorization** — DB GRANT is coarse; row/tenant rules belong in the application or RLS (Postgres).
- **Sharing one superuser** — never point the application at root.

---

## Related

[[mysql user]] [[mysql]] [[cli]] [[show query]]
