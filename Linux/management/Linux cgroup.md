[[Linux]] [[Memory management]] [[OOM (Linux Out Of Memory)]] [[process]]

# Linux cgroups

> Linux cgroups — cgroups (control groups) group processes and apply limits/priorities. Modern distros mount cgroup v2 unified at /sys/fs/cgroup.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#cgroup v2 — memory (containers)]]
- [[#cgroup v2 — CPU]]
- [[#Other controllers (brief)]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**cgroups** (control groups) group processes and apply limits/priorities. Modern distros mount **cgroup v2** unified at `/sys/fs/cgroup`.

```
/system.slice
  └─ docker.slice / kubepods.slice
       └─ container scope
            ├─ memory.max
            ├─ cpu.max
            └─ pids.max
```

v1 (legacy): separate hierarchies per controller (`memory`, `cpuacct`, …). v2: one tree, all controllers.

---

## Standard config / commands

### Detect version

```bash
mount | grep cgroup
# cgroup2 on /sys/fs/cgroup type cgroup2
stat -fc %T /sys/fs/cgroup/    # cgroup2fs = v2

cat /sys/fs/cgroup/cgroup.controllers
cat /sys/fs/cgroup/cgroup.subtree_control
```

### systemd views

```bash
systemd-cgls
systemctl status user.slice
systemd-run --scope -p MemoryMax=512M stress-ng --vm 1 --vm-bytes 600M
```

---

## cgroup v2 — memory (containers)

| File | Meaning |
|------|---------|
| `memory.max` | Hard cap (bytes); OOM kill in cgroup |
| `memory.high` | Throttle/reclaim pressure before max |
| `memory.current` | Usage now |
| `memory.swap.max` | Swap limit (0 = no swap) |

```bash
# Manual cgroup (root)
mkdir -p /sys/fs/cgroup/myapp
echo "+memory" | tee /sys/fs/cgroup/cgroup.subtree_control
echo 512M > /sys/fs/cgroup/myapp/memory.max
echo 0 > /sys/fs/cgroup/myapp/memory.swap.max    # common for latency-sensitive
echo $$ > /sys/fs/cgroup/myapp/cgroup.procs
```

### Docker / Compose

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
    mem_swappiness: 0
```

```bash
docker run -m 512m --memory-swap 512m myimage   # swap disabled when equal
docker stats
```

### Kubernetes

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

Pod OOMKilled → hit `memory.limit`; check `kubectl describe pod` → `Last State: Terminated, Reason: OOMKilled`.

---

## cgroup v2 — CPU

| File | Meaning |
|------|---------|
| `cpu.max` | `quota period` — e.g. `50000 100000` = 50% of one CPU |
| `cpu.weight` | Relative share (1–10000, default 100) |
| `cpuset.cpus` | Pin to CPU list |
| `cpuset.mems` | NUMA nodes |

```bash
echo "50000 100000" > /sys/fs/cgroup/myapp/cpu.max   # 0.5 CPU
echo 200 > /sys/fs/cgroup/myapp/cpu.weight           # 2× default weight vs siblings
```

Docker: `--cpus=0.5` or `--cpu-shares=512` (legacy mapping).

Kubernetes CPU limit: **throttled**, not killed — unlike memory.

---

## Other controllers (brief)

| Controller | v2 knob | Use |
|------------|---------|-----|
| `pids.max` | max processes in cgroup | fork bombs |
| `io.max` | per-device BPS/IOPS | noisy neighbor disk |
| `rdma` | RDMA device limits | HPC |

v1 names still appear in old docs: `cpuacct`, `blkio`, `net_cls`.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Container exits 137 | `dmesg`; cgroup OOM | Raise `memory.max` or fix leak |
| App slow, CPU low | CPU throttling | `cat cpu.max`; raise quota or optimize |
| Host fine, container dies | Limit too low vs JVM/Node heap | Set `-Xmx` / `--max-old-space-size` **below** cgroup limit (~75%) |
| Can't write memory.max | Wrong cgroup level | Enable controller in `cgroup.subtree_control` on parent |
| systemd unit ignores limit | Wrong property | `MemoryMax=` in unit, not only `LimitAS` (different) |

```bash
# Current usage for a Docker container
CID=$(docker inspect -f '{{.Id}}' mycontainer)
cat /sys/fs/cgroup/system.slice/docker-${CID}.scope/memory.current
cat /sys/fs/cgroup/system.slice/docker-${CID}.scope/memory.max
```

Path varies by distro (cgroup driver: systemd vs cgroupfs).

---

## Gotchas

> [!WARNING]
> **Memory limit without swap limit** — container swaps → latency death spiral. Set `memory.swap.max=0` or equal total.

> [!WARNING]
> **JVM/container ergonomics** — JVM reads cgroup limits for default heap; mismatch after Java 8u191+ but verify version.

> [!WARNING]
> **CPU limits ≠ exclusive cores** — throttling is bursty; use `cpuset` for pinning.

> [!WARNING]
> **v1 and v2 mixed mounts** — some hosts hybrid; Docker may use v2 delegation.

> [!WARNING]
> **`memory.high` vs `memory.max`** — high causes reclaim pressure; max kills. Use high for soft SLO.

---

## When NOT to use

- **Bare-metal tuning without measurement** — wrong `cpu.max` hides bottlenecks; profile first.
- **Replacing ulimits entirely** — RLIMIT_NOFILE etc. still matter alongside cgroups.

---

## Related

[[Memory management]] [[OOM (Linux Out Of Memory)]] [[management/Linux out of memory daemon]] [[process]] [[management/Linux resource management]]
