[[SQL]]

# SQL

> One-line: what / why for **SQL** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

> [!INFO] in most libraries, *multi statements are disallowed by default* to prevent SQL injection
```mysql
SELECT * FROM user WHERE id = 3; DROP DATABASE test;
```
- this is valid SQL syntax if urn directly in the MySQL cli or with `multiStatements: true`
- Enable `multipleStatement`
```js
const conn = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '',
  database: 'test',
  multipleStatements: true // <== Add this
});
```
- use parameterized queries or [[ORM]] (e.g., [[Prisma]], [[Sequelize]]) to avoid injections.

## Standard config / commands

…

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
