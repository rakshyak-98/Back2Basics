[[docker container]] [[docker OCI]] [[Docker compose]] [[docker file]] [[Pods]]

# Docker Runtime Security

> Shrink the container attack surface: non-root, dropped capabilities, seccomp, read-only rootfs — defense in depth on a shared kernel.

## Interview Relevance

Interviewers test whether you know containers are namespaced processes (not VMs), and can name concrete controls: USER, capabilities, seccomp, no-new-privileges, and why mounting the Docker socket is host root.

## Sources

- [Docker — Seccomp security profiles](https://docs.docker.com/engine/security/seccomp/) — deep-dive
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker) — overview
- Liz Rice, *Container Security* (O'Reilly) — deep-dive
- Nigel Poulton, *Docker Deep Dive* — overview

## Core Definition

A container shares the host kernel; security is layered isolation (namespaces, cgroups, capabilities, seccomp, optional LSM) so application compromise stays least-privilege and cannot easily become host root.

## Key Concepts

- **Shared kernel:** namespaces (pid, net, mnt, …) + cgroups — isolation is strong but not a hypervisor boundary.
- **Capabilities:** subset of traditional root; drop ALL and add back minimally.
- **seccomp:** syscall filter; Docker’s default blocks dangerous calls (`reboot`, `mount`, …).
- **Read-only rootfs + no-new-privileges:** stop persistence and setuid escalation paths.
- **Defense in depth:** image hygiene + runtime flags + host LSM (AppArmor/SELinux).

## Technical Details

```
Host kernel
  └── container runtime (runc)
        ├── namespaces (pid, net, mnt, …)
        ├── cgroups (CPU/mem)
        ├── capabilities (subset of root)
        ├── seccomp (syscall filter)
        ├── AppArmor/SELinux (optional LSM)
        └── read-only rootfs + tmpfs/volumes for writes
```

### Non-root user (Dockerfile — primary lever)

```dockerfile
FROM gcr.io/distroless/nodejs20-debian12:nonroot
# or
FROM node:20-bookworm-slim
RUN groupadd -r app && useradd -r -g app -u 10001 app \
    && chown -R app:app /app
USER 10001:10001
WORKDIR /app
COPY --chown=app:app . .
```

```yaml
# compose / K8s pod securityContext overlap
services:
  api:
    user: "10001:10001"
    read_only: true
    security_opt:
      - no-new-privileges:true
```

### Drop capabilities

```bash
# Bad — never in prod unless you understand blast radius
docker run --privileged ...

# Good — explicit minimal add
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE myapp:443
```

```yaml
security_opt:
  - no-new-privileges:true
cap_drop:
  - ALL
cap_add:
  - NET_BIND_SERVICE   # only if binding <1024; prefer listen >1024
```

Default retained caps include `CHOWN`, `NET_RAW`, etc. — **drop ALL, add back minimally**.

### seccomp

```yaml
security_opt:
  - seccomp=/path/to/custom-seccomp.json
# or Docker's built-in:
  - seccomp=default.json
```

Custom profile workflow: run with `seccomp=unconfined` in staging, audit `auditd`/falco for syscalls, generate an allowlist.

### Read-only root filesystem

```bash
docker run --read-only --tmpfs /tmp:rw,noexec,nosuid,size=64m myapp
```

```yaml
read_only: true
tmpfs:
  - /tmp
  - /run
volumes:
  - app-cache:/var/cache/myapp   # explicit writable paths only
```

Kubernetes equivalent: `securityContext.allowPrivilegeEscalation: false` + `runAsNonRoot: true`.

### Resource + network isolation

```yaml
deploy:
  resources:
    limits:
      memory: 512M
      cpus: "0.5"
networks:
  - internal-only          # no published ports on sensitive tiers
```

### Hardening checklist

```
□ USER non-zero in Dockerfile (distroless/nonroot ideal)
□ read_only: true + tmpfs/volumes for writes
□ cap_drop: [ALL] + minimal cap_add
□ no-new-privileges:true
□ no --privileged, no host PID/net unless required
□ secrets via runtime secret mount, not ENV in image layers
□ scan images (Trivy/Grype); pin digests
□ host: Docker socket NOT mounted into app container
```

| Symptom | Check | Fix |
|---------|-------|-----|
| `Permission denied` writing file | read-only rootfs | Mount volume/tmpfs for that path |
| `Operation not permitted` | seccomp or cap drop | Add specific cap or syscall to profile |
| Can't bind port 80 | non-root | Listen 8080 + reverse proxy; or CAP_NET_BIND_SERVICE |
| App exits as root | Missing USER | Fix Dockerfile; verify `docker inspect User` |
| DNS works in development, fails hardened | `NET_RAW` dropped | Usually not needed; check outbound firewall |
| JVM/Node crash on seccomp | blocked syscall in logs | Custom seccomp allowlist for runtime |

## Real-World Applications

Production API containers, CI runners that must not own the host, and Kubernetes pods with matching `securityContext`.

**Example:** An API runs as UID 10001, read-only rootfs, `cap_drop: ALL`, and writes only to `/tmp` tmpfs — a remote code exploit cannot drop a binary on `/` or remount devices.

## Pros/Cons or Trade-offs

- **Pro:** Cheap, layered controls that raise the bar after application compromise.
- **Con:** Hardware/device workloads (GPU, BPF loaders) may need documented capability exceptions.
- **Con:** seccomp-unconfined or `--privileged` undoes the rest — security theater if mixed with root.

## Comparison

- vs VM / gVisor / Firecracker: stronger isolation when multi-tenant risk is high.
- vs image scanning alone: scanning finds known CVEs; runtime flags limit blast radius of unknown bugs.
- vs K8s-only hardening: compose hardening is useless if [[Pods]] ship with open `securityContext`.

## Mistakes to Avoid

- Mounting `/var/run/docker.sock` into app containers — the container owns the host (CI only with isolated runners).
- `--privileged` in production — disables seccomp and capability restrictions.
- Root in container plus a kernel breakout CVE — non-root raises the bar.
- Writable `/tmp` without `noexec`; baking `ENV API_KEY=` into layers.
- Assuming seccomp replaces MAC — AppArmor/SELinux still matter on the host.
