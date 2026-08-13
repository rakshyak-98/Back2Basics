[[Memory management]] [[Linux cgroup]] [[management/Linux out of memory daemon]] [[process]]

# OOM (Linux Out Of Memory)

> The OOM killer terminates processes when the kernel cannot satisfy a memory allocation after reclaim — globally or inside a cgroup that hit `memory.max`.

Linux distinguishes **global OOM** (whole machine out of memory) from **cgroup OOM** (container or systemd slice over its limit). Both appear in `dmesg`; cgroup kills often show exit code **137** (SIGKILL).

## Recognize OOM

```bash
dmesg -T | grep -iE 'oom|killed process'
journalctl -k | grep -i oom

# cgroup v2 events (path varies)
cat /sys/fs/cgroup/<slice>/memory.events
# oom, oom_kill counters
```

Example kernel line:
```
Out of memory: Killed process 12345 (java) total-vm:... anon-rss:...
```

## Who gets killed?

The kernel scores tasks with **oom_score**; **oom_score_adj** (−1000 to +1000) biases the choice. Lower adj = less likely to die.

```bash
cat /proc/self/oom_score
cat /proc/self/oom_score_adj
echo -100 | sudo tee /proc/<pid>/oom_score_adj   # protect critical daemon (use sparingly)
```

## cgroup limits vs host OOM

| Layer | Trigger | Fix |
|-------|---------|-----|
| Container `memory.max` | Usage over cgroup cap | Raise limit or fix leak; set JVM/Node heap below cap |
| systemd `MemoryMax=` | Slice over unit limit | Adjust unit; see [[Linux cgroup]] |
| Host global | No RAM + swap left | Add RAM, reduce cache pressure, enable swap, kill hog |

## systemd-oomd / oomd

Userspace daemons can kill before hard kernel OOM — see [[management/Linux out of memory daemon]].

## Related

[[Memory management]] · [[Linux cgroup]] · [[Error status code]] · [[management/Linux resource management]]

## Sources

- [OOM Killer — kernel admin guide](https://www.kernel.org/doc/html/latest/admin-guide/mm/oom-killer.html)
- cgroup v2 `memory.max`: https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html
