[[Docker compose]] [[docker file]] [[docker container]] [[Docker Runtime Security]] [[kubectl]]

# docker cli

> Day-one Docker CLI for build, run, debug, and cleanup — the on-call toolkit when containers misbehave.

## Interview Relevance

Interviewers watch how you build with context/`.dockerignore`, debug with logs/inspect, and avoid destructive `prune` mistakes in production.

## Sources

- [Docker CLI reference](https://docs.docker.com/reference/cli/docker/) — deep-dive
- [Docker Engine overview](https://docs.docker.com/engine/) — overview

## Key Concepts

- **Image vs container:** image = template; container = running or stopped instance with a writable layer.
- **Build context:** everything sent to the daemon during `docker build` — `.dockerignore` matters for size and secrets.
- **Networks & volumes:** user-defined networks give DNS between containers; volumes persist past container delete; bind mounts tie to a host path.
- **Compose plugin:** `docker compose` orchestrates multi-service stacks on one host ([[Docker compose]]).

## Technical Details

```txt
Dockerfile → docker build → image (layers, immutable)
                ↓
         docker run → container (writable layer + mounts)
                ↓
         processes, networks, volumes (daemon-managed)
```

### Validate Dockerfile

```bash
docker build --check .                    # BuildKit checks (syntax/policy)
docker buildx build --check .             # dry parse without full build
docker run --rm -i hadolint/hadolint < Dockerfile   # lint
```

Common lint failures: missing `.dockerignore`, `latest` tag in production, root user, unpinned base image.

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

Ephemeral versus persistent: container writable layer dies with `docker rm`; volumes and bind mounts survive.

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
docker compose down -v   # -v removes named volumes — careful in production
```

### System maintenance

```bash
docker system df
docker system prune              # stopped containers, dangling images, unused networks
docker system prune -a             # all unused images — aggressive
docker system prune -a --volumes   # includes unused volumes — data loss risk
```

| Symptom | Check | Fix |
|---------|-------|-----|
| `Cannot connect to Docker daemon` | `systemctl status docker` | Start daemon; user in `docker` group; `DOCKER_HOST` |
| Build fails COPY missing file | Context vs `.dockerignore` | Fix path; adjust ignore; `docker build --progress=plain` |
| Container exits immediately | `docker logs`; exit code | Fix CMD; run interactively; check arch mismatch |
| Port already allocated | `ss -tlnp \| grep :3000` | Change `-p` mapping; stop conflicting container |
| Out of disk | `docker system df` | Prune; expand volume; logs rotation |
| Works locally, fails CI | Platform (`linux/amd64`) | `docker buildx build --platform linux/amd64` |
| DNS inside container broken | `docker exec cat /etc/resolv.conf` | Custom network; corporate proxy |
| Permission denied on bind mount | UID mismatch | Run as user; fix host permissions; named volume |
| `no space left on device` during build | Layer cache | Prune; multi-stage build; smaller base |
| Network alias not resolving | Same user-defined network? | `docker network connect`; use service name in compose |

## Real-World Applications

Local development loops, CI image builds, and first-response triage when a service container will not stay up.

**Example:** `docker logs -f --tail 200 myapp` plus `docker inspect` network JSON pinpoints a mis-attached network after a bad recreate.

## Pros/Cons or Trade-offs

- **Pro:** One CLI covers build, run, network, volume, and transfer — fast feedback.
- **Con:** Not a cluster orchestrator — use [[kubectl]] or systemd for production HA at scale.
- **Con:** Rootful Docker for untrusted code is risky — prefer rootless or sandbox ([[Docker Runtime Security]]).

## Comparison

- vs [[Docker compose]]: CLI manages one container at a time; Compose owns multi-service YAML.
- vs [[kubectl]]: Engine-local versus cluster API.
- vs Podman CLI: similar UX; different daemon/rootless defaults, same OCI images.

## Mistakes to Avoid

- `docker system prune -a --volumes` in production — deletes unused volumes including orphaned database data.
- Relying on `:latest` in production — pin digest or semver tag.
- Sending secrets in build context because `.env` is missing from `.dockerignore`.
- Using `docker commit` for production images.
- Bind-mounting an empty host directory over image content at the mount point.
- Treating `docker logs` as long-term log storage — ship to journal/Loki.
