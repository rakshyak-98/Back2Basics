[[ExpressJS]] [[express concepts]] [[npm]] [[pm2]] [[Docker]]

# express build

> Express has no separate compiler — you transpile TypeScript if needed, install production dependencies, and run `node` behind a process manager or container orchestrator.

---

## How production differs from development

Development favors fast feedback: `tsx watch`, nodemon, or similar reload the process on file changes. Production favors a stable Node process with production-only dependencies, explicit port binding, and graceful shutdown on `SIGTERM`.

```txt
source ──tsc or bundler──► dist/ ──node──► listen on PORT
```

| Environment | Typical pattern |
|---------------|-----------------|
| Local dev | Hot reload, full `devDependencies` |
| Production host | `npm ci --omit=dev`, `NODE_ENV=production` |
| Container | Bind `0.0.0.0`, health check on `/health` |

---

## Commands

```bash
npm ci --omit=dev
npm run build   # tsc or bundler
NODE_ENV=production node dist/server.js
```

| Setting | Why it matters |
|---------|----------------|
| `NODE_ENV=production` | Caching, error verbosity, some library behavior |
| Bind `0.0.0.0` | Required in containers and Kubernetes probes |
| Graceful shutdown | Drain connections before exit on deploy |

---

## What breaks first

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Cannot find module at runtime | Dev dependency omitted incorrectly | Ensure runtime deps are in `dependencies`, not only `devDependencies` |
| Works locally, fails in Docker | Listening on `127.0.0.1` | Bind `0.0.0.0` |
| TypeScript path aliases fail | Runtime does not resolve `@/` paths | Resolve aliases at build time |
| Zombie process after deploy | No `SIGTERM` handler | Close server and drain before exit |

---

## When this pattern is wrong

- **Serverless handlers** — adapt to the platform entry point rather than a long-lived `listen`.
- **Static-only sites** — serve from a CDN; no Express process required.

---

## Related

[[express concepts]] · [[pm2]] · [[Docker]]
