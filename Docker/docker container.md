[[docker cli]] [[docker file]] [[Docker compose]] [[docker OCI]]

# docker container

> A container is a running (or created) instance of an image: isolated process, writable layer, and optional mounts and ports.





## Interview Relevance
Interviewers check image versus container, publish flags, volume persistence, and why `docker commit` is not a build system.

## Sources
- [Docker — Run a container](https://docs.docker.com/engine/containers/run/) — overview
- [Docker — Container lifecycle](https://docs.docker.com/engine/containers/) — deep-dive

## Key Concepts
- **Image → container:** immutable template plus a writable layer and namespaces.
- **Lifecycle:** `create` / `start` / `run` / `stop` / `rm`; `--rm` deletes on exit.
- **Publish vs expose:** `-p host:container` publishes; Dockerfile `EXPOSE` alone does not.
- **Persistence:** named volumes and bind mounts survive `docker rm`; the writable layer does not.

## Technical Details
```txt
image (immutable) → container (writable layer + namespaces)
```

```bash
docker run hello-world
docker run -it --rm ubuntu bash
docker run -d --name my-nginx -p 8080:80 nginx:latest
docker run -d -e MYSQL_ROOT_PASSWORD=secret --name mydb mysql:8.0
docker run -it -v "$(pwd)":/app python:3.11 bash

docker create --name my-container -p 9000:80 nginx
docker start my-container
docker start -ai my-container
docker run -it -w /app ubuntu:24.04 bash
```

| Flag | Why |
|------|-----|
| `-d` | Detached |
| `-p host:container` | Publish port |
| `-v` / `--mount` | Persist or share files |
| `--rm` | Auto-delete on exit |
| `-e` / `--env-file` | Configuration |
| `-w` | Working directory (created if missing) |

### Snapshot a container

```bash
docker commit my-dev-container my-snapshot:2026-01-20
docker commit --author "you@email.com" -m "debug tools" c123 myproject/snap:debug

docker save -o backup.tar image:tag          # full image layers
docker import container-export.tar new:flat  # flat filesystem import
```

Prefer Dockerfile rebuilds over `commit` for production. `import` flattens; `load` restores layered `save`.

| Symptom | Check | Fix |
|---------|-------|-----|
| Exits immediately | `docker logs`; CMD | Fix entrypoint; run `-it` to debug |
| Port already allocated | `ss -tlnp` | Change `-p` or stop conflict |
| Can’t reach published port | bound to localhost only / firewall | `-p 0.0.0.0:…`; check UFW |
| Data lost after rm | No volume | Use named volume / bind mount |
| Permission denied on bind | UID mismatch | Match user or chown |
| `name already in use` | Stale container | `docker rm -f name` |

## Real-World Applications
One-off debug shells, long-running services on a single host, and the building block under [[Docker compose]] and Kubernetes pods.

**Example:** `docker run -d --name my-nginx -p 8080:80 nginx:latest` publishes container port 80 on host 8080 for a quick reverse-proxy smoke test.

## Pros/Cons or Trade-offs
- **Pro:** Fast start, dense packing, easy cleanup with `--rm`.
- **Con:** Multi-service local stacks need [[Docker compose]]; clusters need Kubernetes/ECS.
- **Con:** Secrets in environment or commit layers leak via `inspect` and image history.

## Comparison
- vs image: image is the template; container is the instance.
- vs VM: shared kernel, thinner isolation ([[Docker Runtime Security]]).
- vs `docker commit` workflow: unreproducible — fix the [[docker file]] instead.

## Mistakes to Avoid
- Using `commit` as a production build system.
- Mapping `-p 80:80` in hardened setups without understanding root/capability needs — prefer high host ports.
- Confusing `docker import` (flat) with `docker load` (layered).
- Expecting data in the writable layer to survive `docker rm`.
