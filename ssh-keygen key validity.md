# ssh-keygen key validity

> One-line: what / why for **ssh-keygen key validity** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

Whether a key is valid is determined by the server's configuration (e.g., whether the public key is present in `~/..ssh/authorized_keys`), not by the key itself.
`-V` option only applies when signing or inspecting certificates, not when generating key.

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
