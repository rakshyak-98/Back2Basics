[[npm]]

# npm

> npm — it means the dependency resolution mechanism detected a mismatch between the expected versions of dependencies specified by a package and the actual…

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** npm — plain job, how I run it, how I know it’s broken.


```bash
npm root -g; # get the global npm node_modules location
```
### peer dependency conflict during the `npm install` process
`npm warn ERESOLVE overriding peer dependency`
- it means the dependency resolution mechanism detected a mismatch between the expected versions of dependencies specified by a package and the actual versions being installed.
##### how to resolve
```shell
npm info <package> peerDependencies; # view peer dependencies
npm install <package>; # install compatible peer dependencies
npm install --legacy-peer-deps; # force install peer dependencies
```
```shell
 => ERROR [frontend 5/6] COPY . .                                                                           21.5s
------
[+] Running 0/16] COPY . .:
 ⠸ Service frontend  Building                                                                              110.3s
failed to solve: cannot replace to directory /var/lib/docker/overlay2/x6ptivu3yyft92itkfpyjjb86/merged/usr/src/app/node_modules/@aws-sdk/client-cloudfront with file

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **npm** | Core idea of this note | “I can explain npm without jargon.” |
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
