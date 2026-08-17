[[docker cli]] [[Docker compose]] [[docker container]] [[docker file]] [[Docker Runtime Security]] [[docker OCI]] [[INDEX]]

# Docker

> Docker packages apps into containers — same image on laptop and server; outages usually come from networking, mounts, or resource limits, not “the daemon is magic.”

```txt
        Docker ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Expect image vs container, layers, volumes vs bind mounts, networking, and wh…

## Sources
- [Docker — Overview](https://docs.docker.com/get-started/docker-overview/) — overview
- [OCI Runtime Spec](https://github.com/opencontainers/runtime-spec) — deep-dive
- [Wikipedia — Docker (software)](https://en.wikipedia.org/wiki/Docker_(software)) — overview

## Key Concepts
- **Engine stack:** CLI → `dockerd` → containerd → runc ([[docker OCI]]).
- **Image / container:** Immutable build artifact vs runtime instance ([[docker container]], [[docker …
- **Compose:** Multi-container apps from YAML ([[Docker compose]]).
- **Isolation limits:** Namespaces + cgroups — not a VM; kernel is shared.
- **Day-2 pain:** Networks, volume permissions, disk fill, CPU/memory limits ([[Docker Runtime …


- **Core:** Docker is a platform to build, ship, and run applications in isolated contain…

## Technical Details
```txt
docker CLI ──► dockerd ──► containerd ──► runc ──► container process
                    │
                    ├── images / layers
                    ├── networks / volumes
                    └── Compose stacks
```

| Symptom / need | Go to |
|----------------|-------|
| Build or run | [[docker cli]] · [[docker file]] |
| Multi-service local | [[Docker compose]] |
| Won’t start / exits | [[docker container]] · [[Docker Runtime Security]] |
| Supply chain / rootless | [[docker OCI]] · [[Docker Runtime Security]] |
| Swarm overlay | [[Swarm network]] |

| Breakage | Check | Fix |
|----------|-------|-----|
| Cannot connect to daemon | `systemctl status docker`; socket perms | Start daemon; `docker` group or rootless |
| Exits immediately | `docker logs`; exit code | Fix `CMD`/`ENTRYPOINT`; app crash |
| Port allocated | `ss -lntp` | Change mapping; stop conflict |
| Disk full | `docker system df` | prune; cap logs; move data-root |

## Mistakes to Avoid
- **Mistake:** Running containers as root with broad host mounts
- **Mistake:** Using `latest` tags in production
- **Mistake:** Ignoring healthchecks and restart policy until on-call pages
- **Mistake:** Treating containers as VMs (mutable SSH pets)

## Pros/Cons or Trade-offs
- **Pro:** Reproducible runtime; fast spin-up; huge ecosystem.
- **Con:** Shared kernel risk; easy to ship fat images; networking and volume semantics confuse newcomers.

## Comparison
- vs VM: stronger isolation, heavier. vs bare process: weaker isolation, simple…


### Use cases
- Local parity: Compose brings API + DB + redis with one file. CI builds a pinn…
