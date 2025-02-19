```shell
systemctl status systemd-oomd;
```
### What is `systemd-oomd`?
`systemd-oomd` is a user-space **Out-Of-Memory (OOM) killer** that monitors system memory and takes action when the system is under memory pressure. It is part of `systemd` and is an alternative to the traditional kernel OOM killer.

It uses **cgroup v2** memory pressure notifications to detect when memory is low and proactively kills processes to prevent system instability.

### How `systemd-oomd` Works
- Monitors **memory pressure** in [[Linux cgroup]].
- When a cgroup exceeds thresholds (`memory.low` and `memory.swap.max`), it takes action.
- Kills **entire cgroups** rather than individual processes.