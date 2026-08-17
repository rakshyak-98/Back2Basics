[[docker container]] [[docker file]] [[docker cli]] [[Docker Runtime Security]] [[AWS ECR]]

# docker OCI

> OCI (Open Container Initiative) — shared specs for image format and runtime so Docker, containerd, Podman, and CRI-O interoperate; `docker commit` is a practical escape hatch, not the ideal path.

```txt
        docker OCI ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers want to know that “Docker” sits on OCI image + runtime specs, th…

## Sources
- [Open Container Initiative](https://opencontainers.org/) — overview
- [OCI Image Specification](https://github.com/opencontainers/image-spec) — deep-dive
- [OCI Runtime Specification](https://github.com/opencontainers/runtime-spec) — deep-dive

## Key Concepts
- **Image index / manifest:** multi-arch pointers so one tag can resolve amd64 and arm64.
- **Runtime bundle:** rootfs + `config.json` consumed by runc.
- **Exposed vs published:** Dockerfile `EXPOSE` documents intent
- **`docker commit`:** snapshots the writable layer — handy for debug, bad for supply chain.


- **Core:** OCI standardizes how container images are packaged and how a runtime (often `…

## Technical Details
```txt
Dockerfile → OCI image → registry
                 ↓
         runtime (runc) → container process
```

```bash
docker commit <container> myfix:debug
docker port <container>
docker ps --format '{{.Names}}\t{{.Ports}}'
docker inspect --format='{{json .NetworkSettings.Ports}}' mycontainer

# Prefer rebuild
docker build -t myfix:1.2 .
```

| Concept | Meaning |
|---------|---------|
| Image index / manifest | Multi-arch pointers |
| Runtime bundle | rootfs + `config.json` for runc |
| Exposed vs published | Dockerfile `EXPOSE` ≠ host publish (`-p`) |

| Symptom | Check | Fix |
|---------|-------|-----|
| Port listed but closed externally | Not published / firewall | `-p`; host SG/firewall |
| Commit image missing files | Data was in a volume | Volumes aren’t in commit |
| “OCI runtime create failed” | runc / cgroup / seccomp | `docker info`; dmesg; profile |
| Arch mismatch | arm64 vs amd64 | Match platform; multi-arch manifest |
| Registry pull reject | Non-OCI / schema1 legacy | Re-push modern manifest |

## Mistakes to Avoid
- **Mistake:** Shipping `docker commit` images to production
- **Mistake:** Treating `EXPOSE` as opening host ports
- **Mistake:** Expecting volumes to appear inside a commit snapshot
- **Mistake:** Assuming OCI equals Docker-only tooling

## Pros/Cons or Trade-offs
- **Pro:** Interoperability — one image format across Docker, Podman, containerd, CRI-O.
- **Con:** Commit images include live hacks and possibly secrets — never ship them.
- **Con:** OCI defines format/runtime, not network policy or multi-tenant isolation strength.

## Comparison
- vs Docker-only mental model: Podman/CRI-O use the same specs with different UX.
- vs VM isolation: when you need strong multi-tenant boundaries, prefer VMs or gVisor/Firecracker (…
- vs application networking policy: service mesh / K8s NetworkPolicy — not OCI itself.


### Use cases
- Any modern registry push/pull (Docker Hub, ECR, GHCR) and every Kubernetes CR…

- **Example:** Debug a broken container with `docker commit` locally, then fix …
