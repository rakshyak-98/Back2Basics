[[process]] [[Linux process commands]] [[top]] [[Linux cgroup]] [[management/Linux resource management]]

# renice

> Changes the nice value of running processes — lower nice gets more CPU share when the machine is contended.

## Interview Relevance

Scheduler basics: nice range −20..19, only root can go negative, and cgroups/`cpu.max` beat renice for hard caps.

## Sources

- `man 1 renice` — deep-dive
- `man 7 sched` — deep-dive

## Core Definition

Linux CFS (Completely Fair Scheduler) uses nice as a relative weight. Nice −20 is highest priority; 19 is lowest. Raising priority (negative nice) requires root.

## Key Concepts

- **Relative, not absolute:** nice only matters under contention.
- **Root for negative nice:** unprivileged users can only make themselves nicer (lower priority).
- **ionice vs nice:** disk I/O class vs CPU share.
- **cgroups win:** hard CPU caps live in [[Linux cgroup]], not nice.

## Technical Details

```bash
renice +10 -p 1234
sudo renice -5 -p 1234
renice +5 -u www-data
```

In [[top]], press `r`, enter PID and new nice value.

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

## Real-World Applications

Lower priority of a overnight compression job so the API stays responsive during business hours.

## Pros/Cons or Trade-offs

- **Pro:** Instant, per-PID relief without restart.
- **Con:** Soft hint only — quotas and real-time classes override expectations.

## Comparison

- vs `nice` at start: renice mutates running tasks; `nice` wraps launch.
- vs cgroups: policy and hard limits for services/containers.

## Mistakes to Avoid

- Expecting renice to bypass cgroup CPU max.
- Habitually giving production daemons nice −20 instead of fixing capacity.
- Confusing ionice with CPU nice.
