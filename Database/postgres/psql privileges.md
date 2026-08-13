<!-- note-strategy: operational -->
[[postgres]]

# psql privileges

> One-line: what / why for **psql privileges** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

```txt
drm_tester = arwdDxtm / drm_tester +
            │         │
            │         └── grantor
            └──────────── privileges
```
- `+` means there are more [[ACL (postgreSQL)]] entries associated with the object
| Letter | Privilege  | Meaning                            |
| ------ | ---------- | ---------------------------------- |
| `a`    | INSERT     | Can insert rows                    |
| `r`    | SELECT     | Can read rows                      |
| `w`    | UPDATE     | Can update rows                    |
| `d`    | DELETE     | Can delete rows                    |
| `D`    | TRUNCATE   | Can truncate the table             |
| `x`    | REFERENCES | Can create foreign-key references  |
| `t`    | TRIGGER    | Can create triggers                |
| `m`    | MAINTAIN   | Can perform maintenance operations |

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
