[[Docker]] [[docker cli]] [[docker file]] [[Docker compose]]

# docker container

> Container — a running (or created) instance of an image: isolated process + writable layer + optional mounts/ports.

## Mental model

**Say it in one breath:** `docker run` = create + start from an image. Lifecycle: create → start → stop → rm. Data in the writable layer dies with `rm` unless volumes.

```txt
image (immutable) → container (writable layer + namespaces)
```

## Standard config / commands

```bash
docker run hello-world
docker run -it --rm ubuntu bash
docker run -d --name my-nginx -p 8080:80 nginx:latest
docker run -d -e MYSQL_ROOT_PASSWORD=secret --name mydb mysql:8.0
docker run -it -v "$(pwd)":/app python:3.11 bash

docker create --name my-container -p 9000:80 nginx
docker start my-container
docker start -ai my-container
```

| Flag | Why |
| --- | --- |
| `-d` | Detached |
| `-p host:container` | Publish port |
| `-v` / `--mount` | Persist or share files |
| `--rm` | Auto-delete on exit |
| `-e` / `--env-file` | Config |

## Snapshot a container

```bash
docker commit my-dev-container my-snapshot:2026-01-20
docker commit --author "you@email.com" -m "debug tools" c123 myproject/snap:debug

docker save -o backup.tar image:tag          # full image layers
docker import container-export.tar new:flat  # flat filesystem import
```

Prefer Dockerfile rebuilds over `commit` for production.

## Run with working directory

```bash
docker run -it -w /app ubuntu:24.04 bash
```

`-w` sets current working directory (created if missing).

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Exits immediately | `docker logs`; CMD | Fix entrypoint; run `-it` to debug |
| Port already allocated | `ss -tlnp` | Change `-p` or stop conflict |
| Can’t reach published port | bound to localhost only / firewall | `-p 0.0.0.0:…`; check UFW |
| Data lost after rm | No volume | Use named volume / bind mount |
| Permission denied on bind | UID mismatch | Match user or chown |
| `name already in use` | Stale container | `docker rm -f name` |

## Gotchas

> [!WARNING]
> **`commit` is not a build system** — unreproducible; use Dockerfile.

> [!WARNING]
> **`-p 80:80` needs root or cap** in hardened setups — map high host ports.

> [!WARNING]
> **`docker import` vs `load`** — import flattens; load restores layered `save`.

## When NOT to use

- **Multi-service local stacks** — [[Docker compose]].
- **Cluster scheduling** — Kubernetes/ECS.
- **Baking secrets into commit** — never.

## Related

[[docker cli]] [[docker file]] [[Docker compose]] [[docker OCI]]
