[[ExpressJS]] [[express concepts]] [[npm]]

# express build

> Express build/run — how you package and start an Express app (Node process, not a special “Express compiler”).

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Transpile/bundle if TypeScript, install production deps, run `node dist/server.js` behind a process manager. Express itself has no unique build step.

```txt
src ──tsc/bundler──► dist ──node──► listen :PORT
```

| Env | Notes |
|-----|-------|
| Dev | `tsx watch` / nodemon |
| Prod | `node` + pm2/systemd |
| Container | HEALTHCHECK on `/health` |

---

## Standard config / commands

```bash
npm ci --omit=dev
npm run build   # tsc
NODE_ENV=production node dist/server.js
```

| Knob | Why it matters |
|------|----------------|
| `NODE_ENV` | Cache/error verbosity |
| Port bind `0.0.0.0` | Containers |
| Graceful shutdown | Drain connections |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Cannot find module | Prod omit wrong | Include runtime deps |
| Works locally not Docker | Bind/host | `0.0.0.0` |
| TS path aliases fail | Runtime paths | Resolve at build |
| Zombie on deploy | No SIGTERM handler | Close server |

---

## Gotchas

> [!WARNING]
> **DevDependencies in prod image** — bloat/vulns.

> [!WARNING]
> **Listening only localhost in k8s** — probes fail.

---

## When NOT to use

- **Serverless handlers** — adapt framework or use native.
- **Static-only sites** — CDN.

---

## Related

[[express concepts]] [[pm2]] [[Docker]]
