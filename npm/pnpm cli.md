[[npm]]

# pnpm cli

> pnpm cli — pnpm approve-builds — is a security feature. Its purpose is to explicitly allow packages to execute install/build scripts.

---

## Mental model

**Say it in one breath:** pnpm cli — pnpm approve-builds — is a security feature. Its purpose is to explicitly allow packages to execute install/build scripts.

`pnpm approve-builds` -> is a security feature. Its purpose is to explicitly allow packages to execute install/build scripts.
```bash
```
- there is supply-chain security risk.
Some npm packages execute scripts automatically during installation.
- `esbuild` needs to download a platform-specific binary during `postinstall`.
- instead of blindly executing it, `pnpm` may block it and ask for approval.
`pnpm approve-build` -> it opens interactive prompt to approve packages that are allowed to execute build/ install scripts. After approval, `pnpm` records the decision in your project configuration.


---

## Standard config / commands

```bash
# version + config path
# dry-run when available
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Retry storm | backoff / jitter | Cap retries; circuit break |
| Config drift | plan/apply or lockfile | Single source of truth |
| Poison message | DLQ | Quarantine and alert |

---

## Gotchas

> [!WARNING]
> Make retries safe or you will duplicate side effects.

---

## When NOT to use

- Avoid the tool if a simpler built-in covers the job.

---

## Related

[[npm]]
