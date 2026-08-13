[[mysql]] [[mysql Privileges]] [[cli]]

# mysql user

> Create and manage MySQL accounts as `'user'@'host'` — password, plugin, then GRANT.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Identity is the pair user+host; creating a user does not grant data access; change passwords with `ALTER USER`; drop the exact `user@host` you created.

```txt
CREATE USER 'app'@'10.0.0.%' IDENTIFIED BY '…'
        │
        ▼
GRANT … ON db.* TO 'app'@'10.0.0.%'
        │
        ▼
App connects matching host pattern
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **`'u'@'h'`** | Account identity | “root@localhost ≠ root@%.” |
| **CREATE USER** | Make the login | “Then GRANT — empty user can’t query.” |
| **ALTER USER** | Password / plugin | “Prefer over ancient SET PASSWORD.” |
| **mysql_native_password** | Legacy auth plugin | “Only for old clients; prefer caching_sha2.” |
| **FLUSH PRIVILEGES** | Reload grant tables | “Rarely needed after CREATE/GRANT today.” |

---

## Standard config / commands

```sql
CREATE USER 'username'@'host' IDENTIFIED BY 'password';
ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';
DROP USER 'app'@'%';

-- Legacy clients
ALTER USER 'app'@'%' IDENTIFIED WITH mysql_native_password BY 'newpwd';

GRANT SELECT, INSERT, UPDATE, DELETE ON mydb.* TO 'app'@'%';
CREATE USER 'nodeuser'@'192.168.3.106' IDENTIFIED BY '…';
GRANT ALL PRIVILEGES ON hotel_cms.* TO 'nodeuser'@'192.168.3.106';
SHOW GRANTS FOR 'nodeuser'@'192.168.3.106';
```

| Knob | Why it matters |
|------|----------------|
| Host `%` vs IP | Security vs convenience |
| Auth plugin | Client compatibility |
| Least privilege | App user ≠ DBA |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Access denied (password YES) | Wrong user@host or password | Create matching host account |
| Login works, queries fail | No GRANTs | [[mysql Privileges]] |
| Plugin mismatch | Client vs `mysql.user.plugin` | ALTER USER … IDENTIFIED WITH … |
| Works on localhost only | Only `@localhost` exists | Add `@'%'` or app subnet |

---

## Gotchas

> [!WARNING]
> **GRANT … IDENTIFIED BY (old)** — creates/alters users as a side effect; use explicit CREATE USER.

> [!WARNING]
> **RDS/Aurora** — no real remote root; create an app master user in the console.

---

## When NOT to use

- **One shared DB user for all humans** — use SSO/operations jump + per-person accounts.
- **Embedding root in the application** — create a narrow application account.

---

## Related

[[mysql Privileges]] [[mysql connection]] [[cli]] [[mysql]]
