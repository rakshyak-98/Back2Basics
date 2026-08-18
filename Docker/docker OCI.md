[[Docker]] [[docker container]] [[docker file]] [[docker cli]]

# docker OCI

> OCI (Open Container Initiative) — shared specs for image format and runtime so Docker, containerd, Podman, and CRI-O interoperate; `docker commit` is a practical escape hatch, not the OCI ideal.

## Mental model

**Say it in one breath:** OCI **image-specification** = layers + configuration JSON. OCI **runtime-specification** = how to start a bundle (runc). Engines speak OCI so an image built with BuildKit runs under containerd.

```txt
Dockerfile → OCI image → registry
                 ↓
         runtime (runc) → container process
```

`docker commit` snapshots a container’s writable layer into a new image — handy for debug, bad for supply chain.

## Standard config / commands

```bash
docker commit <container> myfix:debug
docker port <container>
docker ps --format '{{.Names}}\t{{.Ports}}'
docker inspect --format='{{json .NetworkSettings.Ports}}' mycontainer

# Prefer rebuild
docker build -t myfix:1.2 .
```

| Concept | Meaning |
| --- | --- |
| Image index / manifest | Multi-arch pointers |
| Runtime bundle | rootfs + `config.json` for runc |
| Exposed vs published | Dockerfile `EXPOSE` ≠ host publish (`-p`) |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Port listed but closed externally | Not published / firewall | `-p`; host SG/firewall |
| Commit image missing files | Data was in a volume | Volumes aren’t in commit |
| “OCI runtime create failed” | runc / cgroup / seccomp | `docker info`; dmesg; profile |
| Arch mismatch | arm64 vs amd64 | Match platform; multi-arch manifest |
| Registry pull reject | Non-OCI / schema1 legacy | Re-push modern manifest |

## Gotchas

> [!WARNING]
> **Commit includes hacks and secrets** from the live container — don’t ship it.

> [!WARNING]
> **`EXPOSE` is documentation** — does not open host ports.

> [!WARNING]
> **OCI ≠ Docker-only** — Podman/CRI-O use the same specs with different UX.

## When NOT to use

- **production image creation** — Dockerfile + CI, not commit.
- **application networking policy** — service mesh / K8s NetworkPolicy, not OCI itself.
- **VM-level isolation needs** — strong multi-tenant → VMs or gVisor/Firecracker.

## Related

[[docker container]] [[docker file]] [[docker cli]] [[Docker Runtime Security]] [[AWS ECR]]
