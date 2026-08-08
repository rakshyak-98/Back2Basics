[[SQL]]

# Error: `Public Key Retrieval is not allowed`

> Error: `Public Key Retrieval is not allowed` — mySQL 8+ default to the caching_sha2_password and plugin, which requires the client to encrypt the password using the server's public

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Show query]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

- MySQL 8+ default to the `caching_sha2_password` and plugin, which requires the client to encrypt the password using the server's public key during authentication over insecure connections.
The JDBC driver (e.g., `com.mysql.cj.jdbc.Driver`) needs that public key to perform password encryption.
> [!NOTE] JDBC driver is not pre-configured with the server's public key
### Configs that cause this error
- MySQL user uses `caching_sha1_password`
```sql
SELECT user, plugin FROM mysql.user;
```

## Standard config / commands

…

## Show query

```sql
SHOW DATABASES;
SHOW TABLES;
SHOW TABLES FROM db_name;
SHOW COLUMNS FROM table_name;
SHOW FIELDS FROM table_name;
```

```sql
SHOW INDEX FROM table_name;
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
