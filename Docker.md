[[docker cli]] [[Docker compose]] [[docker container]] [[docker file]] [[Docker Runtime Security]] [[docker OCI]] [[INDEX]]

# Docker

> Docker packages applications into isolated containers — same image runs on laptop and production; the first outage is usually networking, storage mounts, or resource limits, not the daemon itself.

---

## What Docker provides

Docker is an open platform to **develop, ship, and run** applications in loosely isolated **containers**. Containers bundle code, runtime, libraries, and config so hosts do not need matching toolchains installed locally.

| Piece | Role |
|-------|------|
| **Docker Engine** (`dockerd`) | Daemon: images, containers, networks, volumes |
| **Docker CLI** (`docker`) | Client → REST API over Unix socket or TCP |
| **containerd** | Lower-level runtime supervisor |
| **runc** | OCI-compliant process isolation ([[docker OCI]]) |
| **Docker Compose** | Multi-container apps from one YAML file |

```txt
docker CLI ──► dockerd ──► containerd ──► runc ──► container process
                    │
                    ├── images / layers
                    ├── networks / volumes
                    └── [[Docker compose]] stacks
```

## Where to go next

| Symptom / need | Go to |
|----------------|-------|
| Build or run containers | [[docker cli]] · [[docker file]] |
| Multi-service local stack | [[Docker compose]] |
| Container won't start / exits | [[docker container]] · [[Docker Runtime Security]] |
| Image supply chain / rootless | [[docker OCI]] · [[Docker Runtime Security]] |
| Swarm overlay networking | [[Swarm network]] |

## Related topics in this domain

- CLI and flags: [[docker cli]]
- Image build: [[docker file]]
- Lifecycle and inspect: [[docker container]]
- Production hardening: [[Docker Runtime Security]]

## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| `Cannot connect to Docker daemon` | `systemctl status docker`; socket permissions | Start daemon; add user to `docker` group or use rootless |
| Container exits immediately | `docker logs <id>`; exit code | Fix app crash; check `CMD`/`ENTRYPOINT` in [[docker file]] |
| Port already allocated | `ss -lntp`; other containers | Change host port mapping or stop conflicting service |
| Disk full on host | `docker system df` | `docker system prune`; cap logs; move data-root |
| Works locally, fails in CI | Image tag drift; build context | Pin image digests; verify `.dockerignore` |

## Sources

- [Docker — Get started overview](https://docs.docker.com/get-started/docker-overview/)
- [Wikipedia — Docker (software)](https://en.wikipedia.org/wiki/Docker_(software))
