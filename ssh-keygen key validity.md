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

**Say it in one breath:** ssh-keygen key validity — plain job, how I run it, how I know it’s broken.


Whether a key is valid is determined by the server's configuration (e.g., whether the public key is present in `~/..ssh/authorized_keys`), not by the key itself.
`-V` option only applies when signing or inspecting certificates, not when generating key.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **ssh-keygen key validity** | Core idea of this note | “I can explain ssh-keygen key validity without jargon.” |
| **mental model** | How it works in one line | “Explain it without jargon first.” |
| **failure mode** | How it breaks | “Say what you check first.” |

---

## Standard config / commands

```bash
# reproduce with minimal input
# compare working vs broken env
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Unexpected result | inputs / versions | Reproduce minimal case |
| Works on one machine | env drift | Diff config and versions |
| Silent failure | logs / metrics | Add checks and alerts |

---

## Gotchas

> [!WARNING]
> Prefer simple words you can say in an interview.

---

## When NOT to use

- Skip it when a simpler existing tool already fits.

---

## Related

[[ssh-keygen key validity.md]]
