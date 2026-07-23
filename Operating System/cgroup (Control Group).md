[[Linux cgroup]] [[OOM (Linux Out Of Memory)]] [[Docker]] [[Kubernates]]

# cgroup (Control Group)

> Kernel mechanism to group processes and apply CPU, memory, I/O, and pids limits — foundation for systemd slices, Docker, and Kubernetes QoS.

---

## Mental model

**cgroups** answer: *which processes share a budget, and what happens when they exceed it?*

```txt
systemd slice
  └─ docker/kubepods
       └─ container cgroup
            ├─ memory.max  → OOM kill inside group
            ├─ cpu.max     → throttle
            └─ pids.max    → fork bomb cap
```

Modern Linux uses **cgroup v2** unified hierarchy at `/sys/fs/cgroup`. Legacy v1 split controllers per mount — still seen on older nodes.

**systemd** places every service in a cgroup automatically — forks stay in the same group (no orphan processes escaping limits).

> Full ops playbook: **[[Linux cgroup]]** (limits, triage, Docker/K8s knobs).

---

## Standard config / commands

### Quick inspect

```bash
systemd-cgls
systemctl status nginx.service   # shows cgroup path
cat /sys/fs/cgroup/$(systemd-cgls -p | grep nginx | awk '{print $3}')/memory.current 2>/dev/null
```

### systemd resource caps

```ini
# /etc/systemd/system/myapp.service.d/limits.conf
[Service]
MemoryMax=512M
CPUQuota=200%
TasksMax=1024
```

```bash
sudo systemctl daemon-reload && sudo systemctl restart myapp
```

### Docker

```bash
docker run -m 512m --cpus=1.5 myimage
docker inspect --format '{{.HostConfig.Memory}}' CONTAINER
```

**Why cgroups beat ulimit alone:** apply to **process tree**, survive fork/exec, integrate with orchestrators.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Process killed, exit 137 | `dmesg \| grep oom` cgroup name | Raise `memory.max`; fix leak — see [[Linux cgroup]] |
| CPU starvation | `cpu.stat` `nr_throttled` | Increase quota; reduce competing pods |
| Can't fork | `pids.max` | Raise TasksMax; fix fork bomb bug |
| Limits ignored | cgroup v1/v2 mix; delegate off | Mount v2; enable controllers in `cgroup.subtree_control` |

---

## Gotchas

> [!WARNING]
> **OOM kills the largest consumer in the cgroup** — may not be the leak if one process legitimately caches.

> [!WARNING]
> **Java/Go heap defaults ignore cgroup** unless `-XX:MaxRAMPercentage` / Go 1.19+ auto — classic container OOM.

> [!WARNING]
> **`--oom-score-adj` ≠ cgroup memory** — both affect who dies under pressure.

---

## When NOT to use

Don't hand-roll cgroup filesystem writes in production if **systemd/K8s/Docker** already manage hierarchy — fighting the init system breaks delegation.

---

## Related

[[Linux cgroup]] [[OOM (Linux Out Of Memory)]] [[TDP]] [[Docker]] [[Kubernates]]
