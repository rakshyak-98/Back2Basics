[[docker container]] [[docker file]] [[Docker Runtime Security]] [[Swarm network]]

# Docker compose

> Multi-container apps as declarative YAML — `docker compose` v2 is a Docker CLI plugin, not a separate Python binary — Compose spec + **Docker Deep Dive** (Poulton).

## Mental model

Compose orchestrates **one host / one stack** (dev, CI, small prod). Not a cluster scheduler — that's Kubernetes.

```
docker compose up
    │
    ├── parse compose.yaml + .env
    ├── create project network (default: bridge)
    ├── pull/build images
    └── start containers with links, volumes, env
```

**v2 mental model:** `docker compose` (space) replaces legacy `docker-compose` (hyphen). Same Compose Specification; implementation is Go plugin talking to Docker Engine API.

```
Project name = directory name (or -p)
Service name = DNS name on default network  →  http://api:8080 from sibling container
```

## Standard config / commands

### Minimal production-shaped compose.yaml

```yaml
services:
  api:
    build:
      context: .
      target: production          # multi-stage Dockerfile
    image: myorg/api:${GIT_SHA:-dev}
    restart: unless-stopped       # not "always" unless you mean it
    read_only: true               # see [[Docker Runtime Security]]
    tmpfs:
      - /tmp
    env_file:
      - .env                      # never commit secrets; use .env.example in repo
    environment:
      DATABASE_URL: postgres://app@${DB_HOST}:5432/app
    secrets:
      - db_password
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 10s
      timeout: 3s
      retries: 3
      start_period: 30s
    networks:
      - backend
    deploy:                       # ignored by standalone compose except replicas in swarm mode
      resources:
        limits:
          cpus: "1.0"
          memory: 512M

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    volumes:
      - pgdata:/var/lib/postgresql/data   # named volume, NOT bind mount for DB data
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 5s
      retries: 5
    networks:
      - backend

secrets:
  db_password:
    file: ./secrets/db_password.txt   # mode 600 on host

volumes:
  pgdata:

networks:
  backend:
    driver: bridge
```

### CLI workflow

```bash
docker compose config          # validate + interpolate env
docker compose up -d --build
docker compose ps
docker compose logs -f api --since 5m
docker compose exec api sh
docker compose down            # stops + removes containers
docker compose down -v         # also removes named volumes — destructive
```

### depends_on + healthchecks

**Without `condition: service_healthy`**, `depends_on` only waits for container *start*, not app ready — race on first request.

```yaml
depends_on:
  redis:
    condition: service_started   # weak
  db:
    condition: service_healthy     # strong — use for DB migrations on boot
```

### Networks

| Pattern | Use |
|---------|-----|
| Default bridge per project | Service DNS `servicename` |
| `networks: [frontend, backend]` | Split public nginx from internal API |
| `external: true` | Join pre-created network (shared reverse proxy) |

### Secrets (compose-native)

Prefer `secrets:` + `_FILE` env vars over plaintext in `environment:`. Swarm mode mounts secrets; standalone compose bind-mounts secret file read-only.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `connection refused` between services | `docker compose ps`; wrong service name | Use service name not `localhost` cross-container |
| Works once, fails on restart | No healthcheck; app starts before DB | `condition: service_healthy` |
| Config change ignored | Old container running | `docker compose up -d --force-recreate` |
| Permission denied on bind mount | UID mismatch (root in container) | Named volume; or `user:` in compose |
| Secrets in `docker inspect` | Plain `environment:` | Move to secrets / external secret manager |
| Disk fills | Bind mount logs on host | Log driver limits; named volumes; rotation |
| `port is already allocated` | Host port clash | Change `ports:` or stop conflicting service |
| Prod outage after `down -v` | Operator ran destructive down | Backups; document runbooks; avoid `-v` in prod |

## Gotchas

> [!WARNING]
> **Bind mount database data dir** — SELinux (`:Z`), path drift, backup/restore pain, corrupt on laptop sleep. Use **named volumes** for state.

> [!WARNING]
> **`restart: always` on dev laptop** — Docker daemon restart resurrects everything; port conflicts at boot.

- **`version:` key deprecated** — Compose Spec doesn't require it; remove `version: '3.8'` from new files.
- **`.env` committed with prod creds** — compose auto-loads `.env`; gitignore it.
- **`build:` without pinned base image digest** — reproducibility drift.
- **`depends_on` ≠ orchestration** — no rolling update, no auto-heal beyond restart policy; use K8s/swarm for that.
- **Resource limits in compose** — `deploy.resources` applies in Swarm; for standalone use `mem_limit` / `cpus` (compose v2 supports both patterns — verify with `docker compose config`).

## When NOT to use

- **Multi-node HA, PDB, autoscaling** — [[kubectl]] / Kubernetes.
- **Secret rotation at scale** — Vault, cloud SM, not flat files on disk.
- **Compose in prod at large scale** — OK for single-node edge/small SaaS; plan migration path early.

## Related

[[docker container]] [[docker file]] [[Docker Runtime Security]] [[Swarm network]] [[Terraform docker]]
