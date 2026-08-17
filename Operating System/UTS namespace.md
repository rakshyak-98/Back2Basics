[[Operating System]] [[IPC namespace]] [[cgroup (Control Group)]] [[process]]

# UTS namespace

> The UTS namespace isolates hostname and NIS domain name — each container can `sethostname` without renaming the host.





## Interview Relevance
Container isolation checklist: UTS for hostname, IPC for SysV IDs, cgroups for resources — interviewers watch for mixing those up.

## Sources
- Linux `uts_namespaces(7)` manual page — deep-dive
- Linux `clone(2)`, `unshare(1)` manual pages — deep-dive
- [Wikipedia — Linux namespaces](https://en.wikipedia.org/wiki/Linux_namespaces) — overview

## Key Concepts
- **Isolated names:** hostname / domain per namespace.
- **Creation:** `clone(CLONE_NEWUTS)` or `unshare -u`.
- **Visible APIs:** `uname()`, `/proc/sys/kernel/hostname` show the namespaced view.
- **Not resources:** limits come from [[cgroup (Control Group)]].

## Technical Details
```bash
unshare -u hostname my-container-name
hostname   # my-container-name (inside only)
```

Pair with [[IPC namespace]], PID, and mount namespaces for container identity. Requires `CONFIG_UTS_NS`; creation historically needed `CAP_SYS_ADMIN`.

## Real-World Applications
Kubernetes pods and Docker containers each get a hostname for DNS/service identity without changing the node’s name.

## Pros/Cons or Trade-offs
- **Pro:** Safe multi-tenant hostnames.
- **Con:** Host tools see a different hostname than the container unless you enter the namespace.
- **Trade-off:** sharing UTS namespace between containers for specialized multi-process apps.

## Comparison
- vs [[IPC namespace]]: IPC isolates SysV/mqueue IDs; UTS isolates hostname.
- vs [[cgroup (Control Group)]]: cgroups limit CPU/RAM; UTS changes naming view only.

## Mistakes to Avoid
- Debugging with the node hostname while logs show the pod hostname (or vice versa).
- Assuming changing hostname in a container affects the physical host.
- Confusing UTS with user namespace (UIDs) or time namespace.
