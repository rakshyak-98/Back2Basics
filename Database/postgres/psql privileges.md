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

