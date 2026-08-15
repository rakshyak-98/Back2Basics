[[Operating System]] [[Inter Process Communication]] [[UTS namespace]] [[cgroup (Control Group)]] [[process]]

# IPC namespace

> The IPC namespace isolates System V semaphores, message queues, and shared-memory IDs — and POSIX message-queue names — so containers do not collide on key `12345`.

## Interview Relevance

Container interviews expect: namespaces isolate *visibility*; cgroups isolate *resources*. IPC namespace is the concrete example for SysV/`ipcs` collisions.

## Sources

- Linux `ipc_namespaces(7)` manual page — deep-dive
- Linux `namespaces(7)` overview — overview
- [Wikipedia — Linux namespaces](https://en.wikipedia.org/wiki/Linux_namespaces) — overview

## Key Concepts

- **Isolated IPC objects:** same numeric keys in different namespaces are different objects.
- **Creation:** `clone(CLONE_NEWIPC)` or `unshare -i`.
- **Paired with:** PID, mount, net, user, [[UTS namespace]]; limits via [[cgroup (Control Group)]].
- **Scope:** SysV IPC + POSIX mqueue names — not all IPC (e.g. Unix sockets use network/mount view).

## Technical Details

```bash
unshare -i bash
ipcs   # view SysV objects in current namespace
```

Linux namespaces stack together for containers: isolation of view ([[IPC namespace]], [[UTS namespace]], …) plus resource caps ([[cgroup (Control Group)]]).

## Real-World Applications

Docker/Kubernetes give each pod its own IPC namespace so legacy apps using fixed SysV keys do not clash on a shared host.

## Pros/Cons or Trade-offs

- **Pro:** Safe multi-tenant use of SysV IPC.
- **Con:** Debugging `ipcs` from the host shows a different universe than inside the container.
- **Trade-off:** sharing IPC namespace between containers (rare) for specialized multi-process apps.

## Comparison

- vs [[Inter Process Communication]]: IPC is the mechanism family; this namespace isolates identifiers.
- vs [[cgroup (Control Group)]]: cgroups limit CPU/RAM; namespaces hide names/IDs.

## Mistakes to Avoid

- Debugging host `ipcs` while the bug is inside a container’s namespace.
- Assuming Unix domain sockets are gated by IPC namespace (they are not).
- Confusing “no IPC namespace” with “no IPC possible”.
