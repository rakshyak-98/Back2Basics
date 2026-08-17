[[Memory management]] [[OOM (Linux Out Of Memory)]] [[process]] [[management/Linux out of memory daemon]] [[management/Linux resource management]] [[renice]]

# Linux cgroups

> Control groups — kernel resource accounting and hard limits for CPU, memory, PIDs, and I/O (cgroup v2 unified under `/sys/fs/cgroup`).

```txt
        Linux cgroups ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Container/platform staple: v1 vs v2, `memory.max` vs `memory.high`, CPU throt…

## Sources
- [cgroup-v2 documentation — kernel.org](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html) — deep-dive
- [Wikipedia — cgroups](https://en.wikipedia.org/wiki/Cgroups) — overview

## Key Concepts
- **Hard vs soft:** `memory.max` kills; `memory.high` pressures/reclaims first.
- **CPU throttle ≠ kill:** CPU limits slow; memory overage can OOM.
- **Slices/scopes:** systemd and container runtimes place tasks in a tree.
- **PSI:** pressure stalls warn before hard failure.


- **Core:** cgroups group processes and apply limits/priorities. Modern distros mount cgr…

## Technical Details
```
/system.slice
  └─ docker.slice / kubepods.slice
       └─ container scope
            ├─ memory.max
            ├─ cpu.max
            └─ pids.max
```

```bash
mount | grep cgroup
stat -fc %T /sys/fs/cgroup/
cat /sys/fs/cgroup/cgroup.controllers
systemd-cgls
systemd-run --scope -p MemoryMax=512M stress-ng --vm 1 --vm-bytes 600M
```

| File | Meaning |
|------|---------|
| `memory.max` | Hard cap; OOM in cgroup |
| `memory.high` | Reclaim pressure before max |
| `memory.current` | Usage now |
| `memory.swap.max` | Swap limit (`0` = no swap) |
| `cpu.max` | `quota period` (e.g. `50000 100000` = 50% of one CPU) |
| `cpu.weight` | Relative share |
| `pids.max` | Fork bomb guard |

```bash
mkdir -p /sys/fs/cgroup/myapp
echo "+memory" | tee /sys/fs/cgroup/cgroup.subtree_control
echo 512M > /sys/fs/cgroup/myapp/memory.max
echo 0 > /sys/fs/cgroup/myapp/memory.swap.max
echo $$ > /sys/fs/cgroup/myapp/cgroup.procs
echo "50000 100000" > /sys/fs/cgroup/myapp/cpu.max
```

- Docker: `docker run -m 512m --memory-swap 512m`.
- Kubernetes: requests/limits; pod `OOMKilled` hit memory limit.
- CPU limit throttles rather than kills.

| Symptom | Check | Fix |
|---------|-------|-----|
| Exit 137 | `dmesg`; cgroup OOM | Raise `memory.max` or fix leak |
| App slow, CPU low | `cpu.max` throttle | Raise quota or optimize |
| Host fine, container dies | Limit vs heap | Size heap below cgroup (~75%) |
| Can’t write memory.max | Controller not delegated | Enable in parent `subtree_control` |

## Mistakes to Avoid
- **Mistake:** Memory limit without swap policy — latency death spiral from swap
- **Mistake:** Ignoring JVM/runtime ergonomics vs cgroup size
- **Mistake:** Assuming CPU limits pin exclusive cores (use cpuset for pinning)

## Pros/Cons or Trade-offs
- **Pro:** Hard multi-tenant isolation on one kernel.
- **Con:** Mis-sized limits cause throttling/OOM that looks like “random” app failure.

## Comparison
- vs [[renice]]: soft CPU hint vs hard caps.
- vs ulimits: RLIMIT still matters (files, etc.) alongside cgroups.
- vs [[OOM (Linux Out Of Memory)]]: global killer vs cgroup-local OOM.


### Use cases
- Cap a noisy batch job with `MemoryMax=` / `CPUQuota=` on a systemd scope, or …
