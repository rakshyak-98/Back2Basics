[[Operating System]] [[process]] [[RAM and Swap memory]] [[IPC namespace]] [[Linux/management/Linux cgroup]]

# cgroup (Control Group)

> Control groups (cgroups) are the Linux kernel mechanism that limits and accounts for CPU, memory, I/O, and pids — the enforcement layer behind containers and systemd slices.

**Cgroups v2** (unified hierarchy) attach each process to groups with limits such as:

| Controller | Limits |
|------------|--------|
| `cpu` | Quota, weight, burst |
| `memory.max` | RSS + cache charged to cgroup — OOM kill inside group |
| `io` | Bandwidth on block devices |
| `pids.max` | Fork bomb containment |

Docker, Kubernetes, and systemd (`system.slice`, `user.slice`) all write cgroup files under `/sys/fs/cgroup/`.

## Interaction with namespaces

[[IPC namespace]], [[UTS namespace]], and PID/network namespaces **isolate view**; cgroups **isolate resources**. A pod is typically namespaces + cgroup limits together.

## Debugging

```bash
systemd-cgls
cat /sys/fs/cgroup/user.slice/user-1000.slice/memory.current
cat /sys/fs/cgroup/.../cpu.stat   # nr_throttled → [[context switching]] pressure
```

See also [[Linux/management/Linux cgroup]] and [[logical partitions]] (conceptual analogy: dividing machine resources).

## Sources

- Linux kernel documentation: [Control Groups v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)
- systemd.resource-control(5)
- Wikipedia: [Cgroups](https://en.wikipedia.org/wiki/Cgroups)
