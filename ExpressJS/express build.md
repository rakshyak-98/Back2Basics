[[express concepts]] [[expressjs]] [[npm]] [[pm2]] [[docker container]]

# express build

> Express has no separate compiler — transpile TypeScript if needed, install production dependencies, and run `node` behind a process manager or container.





## Interview Relevance
Interviewers ask how you ship a Node HTTP service: dependency pruning, `NODE_ENV`, bind address, graceful shutdown, and why “works on my laptop” fails in containers.

## Sources
- [Express — Production best practices: performance and reliability](https://expressjs.com/en/advanced/best-practice-performance.html) — deep-dive
- [Node.js — Environment variables (`NODE_ENV`)](https://nodejs.org/en/learn/getting-started/nodejs-the-difference-between-development-and-production) — overview
- [Docker — Best practices for writing Dockerfiles](https://docs.docker.com/build/building/best-practices/) — overview

## Core Definition
A production Express build is the path from source to a long-lived Node process: compile or bundle, install runtime-only packages, bind a reachable address, and exit cleanly on deploy signals.

## Key Concepts
- **Development vs production:** hot reload and full `devDependencies` locally → stable process, production-only installs, quieter errors in production.
- **`NODE_ENV=production`:** flips caching and verbosity in Express and many libraries → wrong value means wrong behavior under load.
- **Bind address:** containers and Kubernetes probes need `0.0.0.0`, not `127.0.0.1`.
- **Graceful shutdown:** on `SIGTERM`, stop accepting connections and drain in-flight work before exit.

## Technical Details
```txt
source ──tsc or bundler──► dist/ ──node──► listen on PORT
```

| Environment | Typical pattern |
|---------------|-----------------|
| Local development | Hot reload (`tsx watch`, nodemon), full `devDependencies` |
| Production host | `npm ci --omit=dev`, `NODE_ENV=production` |
| Container | Bind `0.0.0.0`, health check on `/health` |

```bash
npm ci --omit=dev
npm run build   # tsc or bundler
NODE_ENV=production node dist/server.js
```

| Setting | Why it matters |
|---------|----------------|
| `NODE_ENV=production` | Caching, error verbosity, library behavior |
| Bind `0.0.0.0` | Required in containers and orchestrator probes |
| Graceful shutdown | Drain connections before exit on deploy |

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Cannot find module at runtime | Runtime package only in `devDependencies` | Move it to `dependencies` |
| Works locally, fails in Docker | Listening on `127.0.0.1` | Bind `0.0.0.0` |
| TypeScript path aliases fail | Runtime does not resolve `@/` | Resolve aliases at build time |
| Zombie process after deploy | No `SIGTERM` handler | Close server and drain before exit |

## Real-World Applications
API services behind [[pm2]], systemd, or Kubernetes; Docker images that run `node dist/server.js` with a `/health` probe.

**Example:** A pod restarts and connections drop mid-request — add a `SIGTERM` handler that calls `server.close()` and waits for in-flight requests before `process.exit`.

## Pros/Cons or Trade-offs
- **Pro:** Simple deploy story — compile once, run one Node process.
- **Con:** Long-lived `listen` is wrong for serverless — adapt to the platform entry point.
- **Con:** Path aliases and native addons fail silently if the image omits build tools or runtime deps.

## Comparison
- vs serverless handlers: no persistent `listen`; cold start and platform wrappers differ.
- vs static sites: CDN only — no Express process required.
- vs [[express concepts]]: concepts cover request flow; build covers how that process is packaged and run.

## Mistakes to Avoid
- Putting runtime packages only in `devDependencies`, then using `npm ci --omit=dev`.
- Binding `127.0.0.1` in containers so health checks cannot reach the process.
- Ignoring `SIGTERM` so deploys kill in-flight work.
- Relying on TypeScript path aliases at runtime without a resolver or bundler step.
