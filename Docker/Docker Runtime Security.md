[[docker container]] [[docker OCI]] [[Docker compose]] [[docker file]]

# Docker Runtime Security

> Shrink the container attack surface: non-root, dropped caps, seccomp, read-only rootfs — **Docker Deep Dive** (Poulton) + **Container Security** (Liz Rice).

## Mental model

A container is **namespaced processes** on shared kernel — not a VM. Security = **defense in depth**:

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

**Goal:** compromise of app → contained to least privilege; no host root, no new privs, no sensitive syscalls.

## Standard config / commands

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

### Drop capabilities (default Docker already drops many)

```bash
# Bad — never in prod unless you understand blast radius
docker run --privileged ...

# Good — explicit minimal add
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE myapp:443

# Compose
security_opt:
  - no-new-privileges:true
cap_drop:
  - ALL
cap_add:
  - NET_BIND_SERVICE   # only if binding <1024 as non-root alternative use >1024
```

Default retained caps include `CHOWN`, `NET_RAW`, etc. — **drop ALL, add back minimally**.

### seccomp

Docker default seccomp profile blocks ~40 dangerous syscalls (`reboot`, `mount`, …).

```yaml
# Stricter (verify app still runs — glibc, JVM may need syscalls)
security_opt:
  - seccomp=/path/to/custom-seccomp.json
# or Docker's built-in:
  - seccomp=default.json
```

**Custom profile workflow:** run with `seccomp=unconfined` in staging, audit `auditd`/falco for syscalls, generate allowlist.

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

Writable rootfs = attacker can drop binaries, modify `/etc`, install persistence.

### no-new-privileges

Prevents `setuid` binaries from gaining privs (e.g. exploited `ping` setuid).

```yaml
security_opt:
  - no-new-privileges:true
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

## Hardening checklist

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

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Permission denied` writing file | read-only rootfs | Mount volume/tmpfs for that path |
| `Operation not permitted` | seccomp or cap drop | Add specific cap or syscall to profile |
| Can't bind port 80 | non-root | Listen 8080 + reverse proxy; or CAP_NET_BIND_SERVICE |
| App exits as root | Missing USER | Fix Dockerfile; verify `docker inspect User` |
| DNS works in dev, fails hardened | `NET_RAW` dropped | Usually not needed; check outbound firewall |
| JVM/Node crash on seccomp | blocked syscall in logs | Custom seccomp allowlist for runtime |

## Gotchas

> [!WARNING]
> **Mounting `/var/run/docker.sock`** — container owns the host. CI pattern only with isolated runners.

> [!WARNING]
> **`--privileged` disables seccomp + caps** — equivalent to near-root on host. Ban in prod policy.

- **Root in container + breakout CVE** — kernel bug + root = host compromise; non-root raises bar.
- **Writable `/tmp` exec** — mount `tmpfs` with `noexec` where possible.
- **Image secrets in layers** — `ENV API_KEY=` baked forever; use runtime inject + `.dockerignore`.
- **LSM disabled hosts** — seccomp ≠ MAC; AppArmor/SELinux adds profile on top.
- **K8s `securityContext` wins** — don't harden compose but leave K8s pods wide open.

## When NOT to use

- **Hardware/device containers** (GPU, BPF loaders) — may legitimately need extra caps; document exception.
- **seccomp-unconfined as default** — only narrow debug window.
- **Security theater** — read-only rootfs while running root with `--privileged` undoes everything.

## Related

[[docker container]] [[docker OCI]] [[Docker compose]] [[docker file]] [[Pods]]
