[[docker container]] [[docker file]] [[Docker Runtime Security]] [[Swarm network]] [[Terraform docker]]

# Docker compose

> Compose runs a multi-service stack on one host from a YAML file — great for development, CI, and small single-node production; not a cluster scheduler.

```txt
        Docker compose ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask Compose to see if you know service DNS, healthchecks versus …

## Sources
- [Compose Specification](https://github.com/compose-spec/compose-spec/blob/master/spec.md) — deep-dive
- [Docker Compose overview](https://docs.docker.com/compose/) — overview

## Key Concepts
- **One host / one stack:** `docker compose up` parses YAML + `.env`, creates a project network, builds/p…
- **v2 CLI:** `docker compose` (plugin) replaces legacy `docker-compose` (hyphen)
- **Project + service DNS:** project name defaults to directory (or `-p`)
- **Health-gated start:** without `condition: service_healthy`, `depends_on` only waits for container s…

## Technical Details
```
docker compose up
    │
    ├── parse compose.yaml + .env
    ├── create project network (default: bridge)
    ├── pull/build images
    └── start containers with links, volumes, env
```

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

- Prefer `secrets:` + `_FILE` environment variables over plaintext in `environm…
- Swarm mounts secrets

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

## Mistakes to Avoid
- **Mistake:** Bind-mounting database data directories
- **Mistake:** `restart: always` on a development laptop
- **Mistake:** Leaving the deprecated `version:` key
- **Mistake:** Treating `depends_on` as orchestration
- **Mistake:** Secret rotation at scale with flat files

## Pros/Cons or Trade-offs
- **Pro:** One YAML describes the whole stack — fast iteration, shared with teammates and CI.
- **Con:** No multi-node HA, PDB, or autoscaling — plan a migration path early for large production.
- **Con:** Resource `deploy.resources` is Swarm-oriented; standalone needs `mem_limit` / `cpus` patterns verified with `docker compose config`.

## Comparison
- vs [[kubectl]] / Kubernetes: Compose is single-host
- vs [[Swarm network]]: Swarm adds multi-host overlay and routing mesh
- vs plain `docker run`: Compose owns networks, volumes, and dependency order declaratively.


### Use cases
- Local full-stack development, CI integration tests, and small single-node Saa…

- **Example:** An API and Postgres share a `backend` network
