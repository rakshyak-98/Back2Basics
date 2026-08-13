[[ssh-keygen key validity.md]]

# ssh-keygen key validity

> An SSH key works only if the server trusts the public key — generation alone is not enough.

---

## How it works

Whether a key is valid is determined by the server's configuration (e.g., whether the public key is present in `~/..ssh/authorized_keys`), not by the key itself.
`-V` option only applies when signing or inspecting certificates, not when generating key.


---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |


## Gotchas

> [!WARNING]
> …


## Related

[[ssh-keygen key validity.md]]

## Sources

- [Wikipedia — ssh-keygen key validity](https://en.wikipedia.org/wiki/ssh-keygen_key_validity)
