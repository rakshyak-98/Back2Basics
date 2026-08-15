[[docker cli]] [[docker container]] [[Docker compose]] [[Docker Runtime Security]] [[AWS ECR]]

# docker file

> A Dockerfile is a layer recipe: `FROM` a base, `RUN`/`COPY` changes, then `ENTRYPOINT`/`CMD` as the process that runs.

## Interview Relevance

Interviewers probe layer caching, multi-stage builds, exec versus shell form, and why you never bake secrets into image layers.

## Sources

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/) — deep-dive
- [Best practices for writing Dockerfiles](https://docs.docker.com/build/building/best-practices/) — overview

## Key Concepts

- **Layers:** each instruction (roughly) adds a filesystem layer; order controls cache hits.
- **Multi-stage:** build in one stage, copy artifacts into a slim runtime stage — smaller, safer images.
- **ENTRYPOINT vs CMD:** ENTRYPOINT is the fixed main binary; CMD supplies default args (or the command if no entrypoint).
- **Union filesystem:** overlay2 stacks layers; the container adds a thin writable layer on top.

## Technical Details

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

| Driver | Typical use |
|--------|-------------|
| overlay2 | Default modern Linux |
| fuse-overlayfs | Rootless |
| btrfs/zfs | When host uses those |

| Symptom | Check | Fix |
|---------|-------|-----|
| `COPY failed: file not found` | Context / `.dockerignore` | Fix path; build from right dir |
| Cache never busts / always busts | Layer order | Put volatile COPY last |
| Image huge | Intermediate junk | Multi-stage; alpine/distroless; squash carefully |
| Container ignores my command | ENTRYPOINT+CMD combo | Understand exec-form JSON arrays |
| Wrong arch on Apple/ARM | Platform | `--platform=linux/amd64` or multi-arch build |
| Build needs secrets | Secret in layer history | BuildKit secrets; never `ENV PASS=` |

## Real-World Applications

CI builds reproducible application images; multi-stage Node/Go/Java builds ship only runtime bits to registries like [[AWS ECR]].

**Example:** Copy `package*.json`, run `npm ci`, then copy app source — dependency layers stay cached across code-only commits.

## Pros/Cons or Trade-offs

- **Pro:** Declarative, cacheable, reviewable image builds — the production path.
- **Con:** Mis-ordered layers waste CI time; fat images increase pull latency and attack surface.
- **Con:** Configuration that changes per environment should inject at runtime — do not bake twelve environment-specific images.

## Comparison

- vs `docker commit`: Dockerfile is reproducible; commit is a debug escape hatch ([[docker OCI]]).
- vs [[Docker compose]]: Dockerfile builds one image; Compose wires many containers.
- vs VM golden images: containers share the host kernel and layer filesystem — lighter, different isolation story ([[Docker Runtime Security]]).

## Mistakes to Avoid

- Preferring `ADD` for remote URLs / auto-tar — surprising; use `COPY` + explicit `RUN curl`.
- Shell form `CMD npm start` versus exec form `CMD ["npm","start"]` — signal handling differs (PID 1).
- Splitting `apt-get update` and install across `RUN`s — chain update, install, and clean in one layer.
- Putting huge mutable data in layers — use volumes instead.
- Windows apps on a Linux daemon — wrong base OS.
