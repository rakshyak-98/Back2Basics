[[process]] [[Linux process commands]]

# renice

> `renice` changes scheduling priority (nice value) for running processes — lower nice means more CPU time when the machine is contended.

Linux uses **CFS** (Completely Fair Scheduler). Nice ranges **−20** (highest priority) to **19** (lowest). Only root can set negative nice values.

## Usage

```bash
# Lower priority of PID 1234 (higher nice number)
renice +10 -p 1234

# Raise priority (requires root)
sudo renice -5 -p 1234

# By user or group
renice +5 -u www-data
```

Interactive `top`: press `r`, enter PID and new nice value.

## nice vs ionice vs cgroups

| Tool | Resource |
|------|----------|
| `nice` / `renice` | CPU time share |
| `ionice` | Disk I/O class |
| [[Linux cgroup]] `cpu.max` | Hard CPU cap |

## Debugging CPU contention

| Symptom | Check |
|---------|-------|
| Batch job starves desktop | `renice +10` on batch PIDs |
| Critical daemon slow | `sudo renice -5 -p PID` — temporary relief only |
| Throttling despite high nice | cgroup `cpu.max` or CPU quota — not nice |

## Related

[[process]] · [[top]] · [[Linux cgroup]] · [[management/Linux resource management]]

## Sources

- `man 1 renice`, `man 7 sched`
