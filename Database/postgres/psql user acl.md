[[postgres]]

# psql user acl

> psql user acl — the Access Control List (ACL) for the drm_streaming database. It shows which roles have which privileges.

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
drm_streaming | {=Tc/drm_tester,drm_tester=CTc/drm_tester}
```
is the Access Control List (ACL) for the `drm_streaming` database. It shows which roles have which privileges.
```sql
-- {=Tc/drm_tester,drm_tester=CTc/drm_tester}
```
Entry 1: `=Tc/drm_tester`
- No role name before `=` means `PUBLIC` (all users).
- `Tc` are the privileges `T (temporary)`  `c (connect)`
- `/drm_tester` means the privileges were granted by `drm_tester`
Entry 2: `drm_tester=CTc/drm_tester`
- role `drm_tester=`
- `C (Create)`
To remove public access
```sql
REVOKE CONNECT ON DATABASE drm_streaming FROM PUBLIC;
REVOKE TEMPORARY ON DATABASE drm_streaming FROM PUBLIC;
```
```sql
REVOKE ALL PRIVILEGES
ON DATABASE drm_streaming
FROM PUBLIC;
```

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
