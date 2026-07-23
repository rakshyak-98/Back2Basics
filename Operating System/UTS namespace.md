[[IPC namespace]] [[Linux]] [[Docker]] [[Kubernates]]

# UTS namespace

> Isolates hostname and NIS domain name — lets each container think it has its own `uname -n` without changing the host.

---

## Mental model

**UTS** (Unix Timesharing System) namespace splits the **kernel's hostname/domainname** per namespace:

```txt
Host (init UTS)          Container A UTS        Container B UTS
hostname: prod-node-1    hostname: web-abc      hostname: db-xyz
         │                       │                      │
         └─ same kernel, different uts.nodename per ns ─┘
```

Created via `clone(CLONE_NEWUTS)`, `unshare(CLONE_NEWUTS)`, or implicitly by runtimes (`docker run`, `kubectl run`). Child namespaces **copy** parent's hostname at creation time; changing one does not affect siblings.

**Not isolated by UTS alone:** network interfaces, `/etc/hosts` content (unless bind-mounted separately), or DNS — engineers often confuse hostname namespace with network namespace.

---

## Standard config / commands

### Inspect and set hostname in namespace

```bash
hostname                    # current UTS view
hostnamectl set-hostname mybox   # systemd (init namespace only; polkit)

# Inside container
docker run --hostname web01 alpine hostname
# → web01

# Manual unshare demo
sudo unshare -u /bin/bash
hostname isolated-host
```

### Docker / Kubernetes

```bash
docker run --hostname app --name app myimage
# K8s: spec.hostname on Pod (sets UTS hostname for pod sandbox)
```

```yaml
# Pod snippet
spec:
  hostname: my-pod-name
```

### Verify namespace

```bash
ls -l /proc/self/ns/uts
readlink /proc/PID/ns/uts
# Same inode → same UTS namespace
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Container shows host hostname | `--hostname` not set; host UTS shared | `docker run --hostname`; ensure not `--uts=host` |
| License/software binds to hostname | App reads `gethostname()` | Set stable `--hostname` or StatefulSet pod name |
| Monitoring duplicates host alerts | All containers report same hostname | Unique hostname per replica or use labels not hostname |
| `hostname` change doesn't persist | Ephemeral container restart | Set in orchestrator spec, not manual `hostname` cmd |

---

## Gotchas

> [!WARNING]
> **`--uts=host`** (Docker) shares host UTS — breaks hostname isolation; only use when legacy software requires host identity.

> [!WARNING]
> **`/etc/hosts` is a file**, not UTS — Kubernetes injects entries separately; hostname resolution may not match `hostname` output if hosts file differs.

> [!WARNING]
> **TLS cert CN/SAN** tied to hostname — changing UTS without updating certs breaks HTTPS inside mesh.

---

## When NOT to use

Do not rely on UTS for security boundaries — it's cosmetic identity. Combine with [[IPC namespace]], mount, network, and user namespaces for isolation.

---

## Related

[[IPC namespace]] [[Linux]] [[Docker]] [[Inter Process Communication]]
