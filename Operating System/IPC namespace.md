[[Operating System]] [[Inter Process Communication]] [[UTS namespace]] [[cgroup (Control Group)]] [[process]]

# IPC namespace

> The IPC namespace isolates System V semaphores, message queues, and shared memory identifiers — and POSIX message queue names — so containers cannot collide on key `12345`.

Created with `clone(CLONE_NEWIPC)` or `unshare -i`. Processes in different IPC namespaces see disjoint IPC object IDs even if numeric keys match.

## Related isolation

Linux namespaces stack:

- [[UTS namespace]] — hostname
- PID, mount, network, user namespaces
- [[cgroup (Control Group)]] — resource limits (not a namespace but paired)

```bash
unshare -i bash
ipcs   # view SysV objects in current namespace
```

## Sources

- Linux `ipc_namespaces(7)` manual page
- Linux `namespaces(7)` overview
- Wikipedia: [Linux namespaces](https://en.wikipedia.org/wiki/Linux_namespaces)
