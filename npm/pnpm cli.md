[[npm]]

# pnpm cli

> pnpm cli — pnpm approve-builds — is a security feature. Its purpose is to explicitly allow packages to execute install/build scripts.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** pnpm cli — plain job, how I run it, how I know it’s broken.


`pnpm approve-builds` -> is a security feature. Its purpose is to explicitly allow packages to execute install/build scripts.
```bash
```
- there is supply-chain security risk.
Some npm packages execute scripts automatically during installation.
- `esbuild` needs to download a platform-specific binary during `postinstall`.
- instead of blindly executing it, `pnpm` may block it and ask for approval.
`pnpm approve-build` -> it opens interactive prompt to approve packages that are allowed to execute build/ install scripts. After approval, `pnpm` records the decision in your project configuration.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **pnpm cli** | Core idea of this note | “I can explain pnpm cli without jargon.” |
| **idempotent** | Safe to retry | “Retries must not double-charge.” |
| **config** | Knobs outside code | “Env-specific values stay out of source.” |

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
