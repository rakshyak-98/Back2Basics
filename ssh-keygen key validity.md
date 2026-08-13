[[ssh-keygen key validity.md]]

# ssh-keygen key validity

> An SSH key works only if the server trusts the public key — generation alone is not enough.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** An SSH key works only if the server trusts the public key — generation alone is not enough.

Whether a key is valid is determined by the server's configuration (e.g., whether the public key is present in `~/..ssh/authorized_keys`), not by the key itself.
`-V` option only applies when signing or inspecting certificates, not when generating key.


---

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

[[ssh-keygen key validity.md]]
