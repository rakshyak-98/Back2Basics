[[Docker]] [[docker cli]] [[Docker Runtime Security]] [[Docker compose]]

# docker file

> Dockerfile — recipe of layers: `FROM` base, `RUN`/`COPY` changes, `ENTRYPOINT`/`CMD` as the process that runs.

---

## Mental model

**Say it in one breath:** Each instruction usually adds a layer. Build caches layers until a line changes. `ENTRYPOINT` is the main process; `CMD` supplies default arguments (overridable).

```txt
FROM → RUN → COPY → … → ENTRYPOINT/CMD
  layer   layer   layer
```

| Instruction | Role |
|-------------|------|
| `FROM` | Base (or stage); may appear multiple times (multi-stage) |
| `RUN` | Execute at build time |
| `COPY`/`ADD` | Bring files into image (`COPY` preferred) |
| `ENTRYPOINT` | Fixed main binary (override with `--entrypoint`) |
| `CMD` | Default args / command if no entrypoint |

---

## Standard config / commands

```dockerfile
# Multi-stage slim prod
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
ENV NODE_ENV=production
COPY --from=build /app/dist ./dist
USER node
CMD ["node", "dist/server.js"]
```

```bash
docker build -t myapp:1.0 .
docker build --target build -t myapp:build .
docker info --format '{{.Driver}}'   # usually overlay2
```

| Knob | Why it matters |
|------|----------------|
| Order: deps COPY before app COPY | Cache `npm ci` when only app code changes |
| `.dockerignore` | Keeps secrets/node_modules out of context |
| Non-root `USER` | Runtime security baseline |

## Docker layered filesystem

Union mounts (overlay2) stack layers; containers add a thin writable layer. Shared bases save disk.

| Driver | Typical use |
|--------|-------------|
| overlay2 | Default modern Linux |
| fuse-overlayfs | Rootless |
| btrfs/zfs | When host uses those |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `COPY failed: file not found` | Context / `.dockerignore` | Fix path; build from right dir |
| Cache never busts / always busts | Layer order | Put volatile COPY last |
| Image huge | Intermediate junk | Multi-stage; alpine/distroless; squash carefully |
| Container ignores my command | ENTRYPOINT+CMD combo | Understand exec-form JSON arrays |
| Wrong arch on Apple/ARM | Platform | `--platform=linux/amd64` or multi-arch build |
| Build needs secrets | Secret in layer history | BuildKit secrets; never `ENV PASS=` |

---

## Gotchas

> [!WARNING]
> **`ADD` remote URLs / auto-tar** — surprising; prefer `COPY` + explicit `RUN curl`.

> [!WARNING]
> **Shell vs exec form** — `CMD npm start` vs `CMD ["npm","start"]` signal handling differs.

> [!WARNING]
> **Every `RUN` is a layer** — chain `apt-get update && install && clean` in one `RUN`.

---

## When NOT to use

- **configuration that changes per environment** — inject at runtime (environment/files), don’t bake 12 images.
- **Windows apps on Linux daemons** — wrong base OS.
- **Huge mutable data** — volumes, not image layers.

---

## Related

[[docker cli]] [[docker container]] [[Docker compose]] [[Docker Runtime Security]] [[AWS ECR]]
