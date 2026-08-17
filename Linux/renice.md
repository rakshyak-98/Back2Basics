[[process]] [[Linux process commands]] [[top]] [[Linux cgroup]] [[management/Linux resource management]]

# renice

> Changes the nice value of running processes — lower nice gets more CPU share when the machine is contended.

```txt
        renice ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Scheduler basics: nice range −20..19, only root can go negative, and cgroups/…

## Sources
- `man 1 renice` — deep-dive
- `man 7 sched` — deep-dive

## Key Concepts
- **Relative, not absolute:** nice only matters under contention.
- **Root for negative nice:** unprivileged users can only make themselves nicer (lower priority).
- **ionice vs nice:** disk I/O class vs CPU share.
- **cgroups win:** hard CPU caps live in [[Linux cgroup]], not nice.


- **Core:** Linux CFS (Completely Fair Scheduler) uses nice as a relative weight. Nice −2…

## Technical Details
```bash
renice +10 -p 1234
sudo renice -5 -p 1234
renice +5 -u www-data
```

- In [[top]], press `r`, enter PID and new nice value.

| Tool | Resource |
|------|----------|
| `nice` / `renice` | CPU time share |
| `ionice` | Disk I/O class |
| cgroup `cpu.max` | Hard CPU cap |

| Symptom | Check |
|---------|-------|
| Batch job starves desktop | `renice +10` on batch PIDs |
| Critical daemon slow | Temporary `sudo renice -5` |
| Still throttled at high priority | cgroup quota — not nice |

## Mistakes to Avoid
- **Mistake:** Expecting renice to bypass cgroup CPU max
- **Mistake:** Habitually giving production daemons nice −20 instead of fixing …
- **Mistake:** Confusing ionice with CPU nice

## Pros/Cons or Trade-offs
- **Pro:** Instant, per-PID relief without restart.
- **Con:** Soft hint only — quotas and real-time classes override expectations.

## Comparison
- vs `nice` at start: renice mutates running tasks; `nice` wraps launch.
- vs cgroups: policy and hard limits for services/containers.


### Use cases
- Lower priority of a overnight compression job so the API stays responsive dur…
