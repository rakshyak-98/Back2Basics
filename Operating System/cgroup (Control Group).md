[[Operating System]] [[process]] [[RAM and Swap memory]] [[IPC namespace]] [[UTS namespace]] [[Linux/management/Linux cgroup]] [[logical partitions]] [[context switching]]

# cgroup (Control Group)

> Control groups (cgroups) are the Linux kernel mechanism that limits and accounts for CPU, memory, I/O, and pids — the enforcement layer behind containers and systemd slices.





## Interview Relevance
Container interviews: namespaces isolate *view*; cgroups isolate *resources*. Know v2 controllers (`memory.max`, CPU quota) and how OOM kills inside a group.

## Sources
- [Linux kernel docs — Control Groups v2](https://docs.kernel.org/admin-guide/cgroup-v2.html) — deep-dive
- systemd.resource-control(5) — deep-dive
- [Wikipedia — Cgroups](https://en.wikipedia.org/wiki/Cgroups) — overview

## Key Concepts
- **Unified hierarchy (v2):** processes attach to groups with controllers.
- **Limits:** CPU quota/weight, `memory.max`, `io`, `pids.max`.
- **Consumers:** Docker, Kubernetes, systemd slices write `/sys/fs/cgroup/`.
- **Pairing:** namespaces for identity/view; cgroups for budgets.

## Technical Details
| Controller | Limits |
|------------|--------|
| `cpu` | Quota, weight, burst |
| `memory.max` | RSS + cache charged to cgroup — OOM kill inside group |
| `io` | Bandwidth on block devices |
| `pids.max` | Fork bomb containment |

[[IPC namespace]], [[UTS namespace]], and PID/network namespaces **isolate view**; cgroups **isolate resources**. A pod is typically both.

```bash
systemd-cgls
cat /sys/fs/cgroup/user.slice/user-1000.slice/memory.current
cat /sys/fs/cgroup/.../cpu.stat   # nr_throttled → [[context switching]] pressure
```

See also [[Linux/management/Linux cgroup]] and [[logical partitions]] (conceptual analogy).

## Real-World Applications
Kubernetes pod limits, systemd `MemoryMax=`, and multi-tenant hosts preventing one job from starving others.

## Pros/Cons or Trade-offs
- **Pro:** Hard multi-tenant isolation and accounting.
- **Con:** Mis-sized limits cause mysterious throttling/OOM.
- **Trade-off:** strict caps vs bursting for latency spikes.

## Comparison
- vs namespaces: view vs resources.
- vs [[RAM and Swap memory]]: cgroups decide who may consume RAM; swap/OOM policy still applies underneath.

## Mistakes to Avoid
- Setting container memory == JVM heap with no headroom.
- Debugging host-wide metrics while the pod is CPU-throttled.
- Confusing cgroup OOM with host OOM without checking which group died.
