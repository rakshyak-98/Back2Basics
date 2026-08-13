[[Operating System]] [[IPC namespace]] [[cgroup (Control Group)]] [[process]]

# UTS namespace

> The UTS namespace isolates the system hostname and NIS domain name — each container can call `sethostname` without renaming the host.

**UTS** (Unix Time-sharing System legacy name) namespace copied on `clone(CLONE_NEWUTS)` or `unshare -u`. `uname()` and `/proc/sys/kernel/hostname` reflect the namespace view.

```bash
unshare -u hostname my-container-name
hostname   # my-container-name (inside only)
```

Pair with [[IPC namespace]], PID, and mount namespaces for container identity — distinct from [[cgroup (Control Group)]] resource limits.

Requires `CONFIG_UTS_NS`; creation historically needed `CAP_SYS_ADMIN`.

## Sources

- Linux `uts_namespaces(7)` manual page
- Linux `clone(2)`, `unshare(1)` manual pages
- Wikipedia: [Linux namespaces](https://en.wikipedia.org/wiki/Linux_namespaces)
