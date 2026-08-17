[[Operating System]] [[Inter Process Communication]] [[UTS namespace]] [[cgroup (Control Group)]] [[process]]

# IPC namespace

> The IPC namespace isolates System V semaphores, message queues, and shared-memory IDs — and POSIX message-queue names — so containers do not collide on key `12345`.

```txt
        IPC namespace ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Container interviews expect: namespaces isolate *visibility*

## Sources
- Linux `ipc_namespaces(7)` manual page — deep-dive
- Linux `namespaces(7)` overview — overview
- [Wikipedia — Linux namespaces](https://en.wikipedia.org/wiki/Linux_namespaces) — overview

## Key Concepts
- **Isolated IPC objects:** same numeric keys in different namespaces are different objects.
- **Creation:** `clone(CLONE_NEWIPC)` or `unshare -i`.
- **Paired with:** PID, mount, net, user, [[UTS namespace]]
- **Scope:** SysV IPC + POSIX mqueue names

## Technical Details
```bash
unshare -i bash
ipcs   # view SysV objects in current namespace
```

- Linux namespaces stack together for containers: isolation of view ([[IPC name…

## Mistakes to Avoid
- **Mistake:** Debugging host `ipcs` while the bug is inside a container’s name…
- **Mistake:** Assuming Unix domain sockets are gated by IPC namespace (they ar…
- **Mistake:** Confusing “no IPC namespace” with “no IPC possible”

## Pros/Cons or Trade-offs
- **Pro:** Safe multi-tenant use of SysV IPC.
- **Con:** Debugging `ipcs` from the host shows a different universe than inside the container.
- **Trade-off:** sharing IPC namespace between containers (rare) for specialized multi-process apps.

## Comparison
- vs [[Inter Process Communication]]: IPC is the mechanism family
- vs [[cgroup (Control Group)]]: cgroups limit CPU/RAM; namespaces hide names/IDs.


### Use cases
- Docker/Kubernetes give each pod its own IPC namespace so legacy apps using fi…
