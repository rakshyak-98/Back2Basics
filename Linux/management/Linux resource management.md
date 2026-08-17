[[Linux cgroup]] [[renice]] [[OOM (Linux Out Of Memory)]] [[systemd]] [[Memory management]]

# Linux resource management

> Caps CPU, memory, I/O, and PIDs so one tenant cannot sink the host — niceness is soft; cgroups are hard.

```txt
        Linux resource man ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Soft vs hard controls: nice/ionice vs `MemoryMax`/`CPUQuota`, plus PSI as ear…

## Sources
- [cgroup-v2 documentation](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html) — deep-dive
- [systemd.resource-control(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html) — deep-dive

## Key Concepts
- **Soft:** `nice` / `ionice` — hints under contention.
- **Hard:** systemd resource properties backed by cgroups.
- **PSI:** `/proc/pressure/*` stalls before hard failure.
- **Heaps must honor limits:** JVM/Go must size to cgroup, not host RAM.

## Technical Details
```txt
soft: nice / ionice
hard: MemoryMax= CPUQuota= IOWeight= TasksMax=
observe: PSI /proc/pressure + systemd-cgtop
```

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

| Symptom | Check | Fix |
|---------|-------|-----|
| Throttled CPU | CPUQuota | Raise quota or fix hot loop |
| OOMKill in container | MemoryMax | Raise limit / fix leak |
| Disk latency spike | Heavy writer | ionice / IOWeight |
| Fork bomb | TasksMax | Set TasksMax; find spawner |

## Mistakes to Avoid
- **Mistake:** Limits without metrics — you only learn in outages
- **Mistake:** Trying to “fix” memory leaks with nice
- **Mistake:** Ignoring runtime heap vs cgroup mismatch

## Pros/Cons or Trade-offs
- **Pro:** Predictable multi-tenant behavior on shared hosts.
- **Con:** Over-limiting lone latency-critical tenants can hurt — sometimes size the machine instead.

## Comparison
- vs [[renice]]: soft only — won’t stop a runaway alone.
- vs [[Linux cgroup]]: this note is the ops policy layer; cgroup is the mechanism.


### Use cases
- Protect an API unit with `CPUQuota=200%` and `MemoryMax=1G`, watch PSI during…
