Control group `cgroup` in Linux are a feature that allows you to allocate, prioritize, and limit system resources (CPU, memory, I/O, etc.) for processes.
- they are useful for containerization (Docker, LXC), process isolation, and system performance tuning.

```shell
mount | grep cgroup; # view which version is enabled 
cat /sys/fs/cgroup/cgroup.controllers
```
The linux kernel provides two versions:
- `cgroup` v1 -> Hierarchical, separate controllers for CPU, memory, and I/O.
- `cgroup` v2 -> Unified hierarchy with a single controller for better management.

##### `cgroups` allow control over:
- **CPU** (`cpu, cpuacct`): Limit CPU usage per process.
- **Memory** (`memory`): Restrict RAM usage.
- **I/O** (`blkio`): Control disk read/write rates.
- **Network** (`net_cls, net_prio`): Prioritize network bandwidth.
- **Devices** (`devices`): Control device access.
- **Processes** (`pids`): Limit the number of processes.

```shell
systemctl status systemd-cgls; # list systemd-managed cgroups;
```