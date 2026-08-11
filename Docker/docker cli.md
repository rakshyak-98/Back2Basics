[[Docker compose]] [[docker file]] [[docker container]] [[Docker Runtime Security]] [[INDEX]]

# docker cli

> Day-one Docker CLI for build, run, debug, and cleanup — **Docker docs** + on-call triage when containers misbehave.

---

## Mental model

```txt
Dockerfile → docker build → image (layers, immutable)
                ↓
         docker run → container (writable layer + mounts)
                ↓
         processes, networks, volumes (daemon-managed)
```

**Image** = template; **container** = running (or stopped) instance. **Build context** = everything sent to daemon during `docker build` (`.dockerignore` matters).

**Networking:** default bridge; user-defined networks for DNS between containers. **Volumes** persist past container delete; bind mounts tie to host path.

---

## Standard config / commands

### Validate Dockerfile

```bash
docker build --check .                    # BuildKit checks (syntax/policy)
docker buildx build --check .             # dry parse without full build
docker run --rm -i hadolint/hadolint < Dockerfile   # lint (not "urn")
```

Common lint failures: missing `.dockerignore`, `latest` tag in prod, root user, unpinned base image.

### Build

```bash
docker build -t myapp:latest .                              # context = cwd
docker build -f docker/Dockerfile -t myapp:1.0.0 .
docker build --no-cache -t myapp:latest .
docker build --build-arg NODE_ENV=production -t myapp:latest .
docker build --target builder -t myapp:builder .
```

### Run

```bash
docker run -d --name myapp -p 3000:3000 myapp:latest
docker run --rm -it myapp:latest /bin/sh    # ephemeral debug shell
docker exec -it myapp /bin/sh               # into running container
```

### Inspect & logs

```bash
docker ps -a
docker logs -f --tail 200 myapp
docker inspect myapp
docker inspect --format '{{json .NetworkSettings.Networks}}' myapp
docker top myapp
docker stats --no-stream
```

### Network

```bash
docker network ls
docker network create app-net
docker run -d --network app-net --name api myapp:latest

docker network disconnect app-net api
docker network connect --alias api-internal app-net api
```

### Volumes

```bash
docker volume create mydata
docker run -v mydata:/var/lib/data myapp:latest
docker run -v /host/path:/container/path:ro myapp:latest   # bind mount

docker volume ls
docker volume inspect mydata
```

**Ephemeral vs persistent:** container writable layer dies with `docker rm`; volumes and bind mounts survive.

### Image transfer

```bash
docker save myapp:latest | gzip > myapp.tar.gz
docker load < myapp.tar.gz
docker tag myapp:latest registry.example.com/myapp:v1
docker push registry.example.com/myapp:v1
```

### Compose plugin

```bash
sudo apt install docker-compose-plugin
docker compose up -d
docker compose logs -f api
docker compose down -v   # -v removes named volumes — careful in prod
```

### System maintenance

```bash
docker system df
docker system prune              # stopped containers, dangling images, unused networks
docker system prune -a             # all unused images — aggressive
docker system prune -a --volumes   # includes unused volumes — data loss risk
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Cannot connect to Docker daemon` | `systemctl status docker` | Start daemon; user in `docker` group; `DOCKER_HOST` |
| Build fails COPY missing file | Context vs `.dockerignore` | Fix path; adjust ignore; `docker build --progress=plain` |
| Container exits immediately | `docker logs`; exit code | Fix CMD; run interactively; check arch mismatch |
| Port already allocated | `ss -tlnp \| grep :3000` | Change `-p` mapping; stop conflicting container |
| Out of disk | `docker system df` | Prune; expand volume; logs rotation |
| Works locally, fails CI | Platform (`linux/amd64`) | `docker buildx build --platform linux/amd64` |
| DNS inside container broken | `docker exec cat /etc/resolv.conf` | Custom network; corporate proxy |
| Permission denied on bind mount | UID mismatch | Run as user; fix host perms; named volume |
| `no space left on device` during build | Layer cache | Prune; multi-stage build; smaller base |
| Network alias not resolving | Same user-defined network? | `docker network connect`; use service name in compose |

---

## Gotchas

> [!WARNING]
> **`docker system prune -a --volumes` in prod** — deletes unused volumes including orphaned DB data.

> [!WARNING]
> ** `:latest` pull surprise** — prod must pin digest or semver tag.

> [!WARNING]
> **Build context sends secrets** if `.env` not in `.dockerignore` — layers retain them until rebuilt.

> [!WARNING]
> **`docker commit` for prod images** — non-reproducible; fix Dockerfile instead.

> [!WARNING]
> **Bind mount overwrites image files** — empty host dir hides image content at mount point.

---

## When NOT to use

- **Production orchestration at scale** — [[Docker compose]] for dev; Kubernetes/systemd for prod HA.
- **Rootful Docker for untrusted code** — use rootless mode or sandbox ([[Docker Runtime Security]]).
- **Long-term log storage** — ship to journal/Loki; `docker logs` rotates with container.

---

## Related

[[Docker compose]] · [[docker file]] · [[docker container]] · [[Docker Runtime Security]] · [[kubectl]]
