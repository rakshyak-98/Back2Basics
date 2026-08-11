[[management]] [[Linux cgroup]] [[renice]] [[OOM (Linux Out Of Memory)]]

# Linux resource management

> Resource management caps CPU, memory, I/O, and PIDs so one tenant can’t sink the host — niceness is soft; cgroups are hard.

---

## Mental model

**Say it in one breath:** nice/ionice hint the schedulers; cgroups/`systemd` quotas enforce; measure with `pressure` and `systemd-cgtop`.

```txt
soft: nice / ionice
hard: MemoryMax= CPUQuota= IOWeight= TasksMax=
observe: PSI /proc/pressure + systemd-cgtop
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **cgroup** | Accounting + limits | “Containers are cgroups + namespaces.” |
| **CPUQuota** | Percent of one CPU | “200% ≈ two cores.” |
| **MemoryMax** | Hard RAM cap | “Hit → cgroup OOM.” |
| **PSI** | Pressure stall info | “Early warning before OOM.” |
| **nice** | Soft CPU priority | “Won’t cap a runaway alone.” |

---

## Standard config / commands

```bash
systemctl set-property myapp.service MemoryMax=1G CPUQuota=100%
systemctl show myapp.service -p MemoryMax,CPUQuota
systemd-cgtop
cat /proc/pressure/memory
renice -n 10 -p PID
ionice -c 3 -p PID
```

| Knob | Why it matters |
|------|----------------|
| `MemoryHigh` vs `Max` | Throttle vs kill |
| slice hierarchy | Shared budgets |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Throttled CPU | CPUQuota | Raise quota or fix hot loop |
| OOMKill in container | MemoryMax | Raise limit / fix leak |
| Disk latency spike | Heavy writer | ionice / IOWeight |
| Fork bomb | TasksMax | Set TasksMax; find spawner |

---

## Gotchas

> [!WARNING]
> **Limits without metrics** — you only learn in outages; watch PSI/cgtop.

> [!WARNING]
> **JVM/Go heaps vs cgroup** — apps must honor container memory, not host RAM.

---

## When NOT to use

- **Latency-critical lone tenants** — over-limit can hurt; size the machine instead.
- **Trying to “fix” leaks with nice** — won’t reclaim RSS.

---

## Related

[[Linux cgroup]] [[renice]] [[OOM (Linux Out Of Memory)]] [[systemd]]
