[[system call]] [[handle]] [[Buffer cache]] [[non-blocking]] [[cgroup (Control Group)]]

# File descriptors

> Per-process integer handles to open kernel objects (files, sockets, pipes, epoll sets) — **Stevens / Kerrisk**.

---

## Mental model

Every open I/O object in Unix is a **file descriptor (fd)**: a small non-negative integer index into the process's **fd table**. Each slot points at a **kernel `struct file`** (open file description) that holds offset, flags, and the underlying inode/socket.

```txt
process fd table          kernel open-file table
┌───┬───┐                 ┌──────────────┐
│ 0 │───┼──► stdin  ─────►│ struct file  │──► inode / socket / pipe
│ 1 │───┼──► stdout       └──────────────┘
│ 2 │───┼──► stderr              ▲
│ 3 │───┼──► socket               │ dup(2) / fork share same struct file
│ 4 │───┼──► log file             │ (shared offset unless O_CLOEXEC + close)
└───┴───┘
```

- **fd ≠ file**: `dup()`, `fork()`, and some language runtimes share one `struct file` across multiple fd numbers.
- **Limits are per-process** (soft/hard `RLIMIT_NOFILE`) and sometimes per-container via cgroups.
- **Leaked fds** (never closed connections, temp files, `Timer` handles in Node) accumulate until `EMFILE` — "too many open files" — often under load, not at startup.

**Service impact:** Node/Go/Java accept loops, DB connection pools, and reverse proxies are fd-heavy. One leaked socket per request × 10k RPS = outage in minutes.

---

## Standard config / commands

### Inspect what a process has open

```shell
# All open fds for PID (path or anon)
ls -l /proc/PID/fd

# Human-readable: which binary, cwd, fd count
lsof -p PID
lsof -i :8080                    # who holds the port?
lsof +L1                         # deleted files still held open (disk won't free)

# Count fds across process tree
ls /proc/PID/fd | wc -l
for p in $(pgrep myservice); do echo -n "$p "; ls /proc/$p/fd 2>/dev/null | wc -l; done
```

### Limits (soft vs hard)

```shell
ulimit -n                          # soft limit (what syscalls enforce today)
ulimit -Hn                         # hard limit (ceiling unless root raises it)
cat /proc/PID/limits | grep "open files"

# Persist for systemd service (preferred over shell ulimit)
# /etc/systemd/system/myservice.service.d/limits.conf
[Service]
LimitNOFILE=65535
```

```shell
# Raise hard limit for current shell (root), then soft
ulimit -Hn 1048576
ulimit -n 1048576
```

**Why two limits:** soft is what `open()`/`socket()` hit; hard caps how far an unprivileged process can raise soft without root. Orchestrators often set soft=hard in the unit file — verify with `systemctl show myservice -p LimitNOFILE`.

### Non-blocking and fd flags

```c
#include <fcntl.h>
int flags = fcntl(fd, F_GETFL, 0);
fcntl(fd, F_SETFL, flags | O_NONBLOCK);   // see [[non-blocking]]
fcntl(fd, F_SETFD, FD_CLOEXEC);           // don't leak to exec'd children
```

```shell
# Watch syscalls that create fds
strace -e trace=open,openat,socket,accept,dup,dup2,close -p PID
```

### Container / K8s

- Docker `--ulimit nofile=65535:65535` or Compose `ulimits`.
- K8s: no first-class fd limit; inherits node + container runtime defaults (often 1M on modern nodes, but **verify** — old images defaulted to 1024).
- Sidecars + app in one pod = **shared fd budget** on the cgroup/process tree depending on runtime.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `EMFILE: too many open files` | `ls /proc/PID/fd \| wc -l`; `lsof -p PID \| wc -l`; `cat /proc/PID/limits` | Close leaks; pool connections; raise `LimitNOFILE`; fix missing `close()` / `defer conn.Close()` |
| `EADDRINUSE` but nothing obvious | `lsof -i :PORT`; `ss -tlnp` | Kill stale holder; SO_REUSEADDR; ensure old workers exited |
| Disk full, `du` doesn't match | `lsof +L1` (deleted files still open) | Restart process holding deleted logs; rotate with `copytruncate` or proper reopen |
| Accept stops under load, low CPU | fd count vs limit; `ss -s` | Same as EMFILE; check accept backlog + connection draining |
| Child inherits sensitive fd | `ls -l /proc/PID/fd` after fork | Set `FD_CLOEXEC` on sensitive fds; use `O_CLOEXEC` on `open()` |
| Works on laptop, dies in prod | Compare `ulimit -n` local vs pod/systemd | Align limits in unit/Helm; don't rely on dev defaults |

---

## Gotchas

> [!WARNING]
> **Soft limit silently bites at scale.** Default 1024 is fine for a shell, fatal for a proxy or Node API at a few thousand concurrent keep-alives. Load tests are the usual first discovery.

> [!WARNING]
> **`dup()` / fork share offset.** Two fds, one file offset — interleaved `read()`/`write()` corrupts streams unless you use separate opens or locking.

> [!WARNING]
> **Language runtimes hide fds.** JVM (sockets, files, `Process`), Go (net poller epoll fd), Node (libuv handles) — `lsof` is ground truth, not your app's mental model.

> [!WARNING]
> **Epoll/kqueue fd is also an fd.** High-fanout servers: 1 epoll + N connections + M log files + pipe pairs for workers adds up fast.

**Node:** `server.maxConnections`, undici pool size, forgotten `clearInterval`, and `fs.createReadStream` without destroy — classic leak paths.

**Go:** `http.DefaultTransport` idle conns; always `Body.Close()` on responses even when discarding body.

**Java:** `-XX:MaxDirectMemorySize` is separate from fd count, but Netty direct buffers + many channels still correlate with connection hygiene.

---

## When NOT to use

- Don't raise `RLIMIT_NOFILE` to millions without raising **kernel** `fs.file-max` and monitoring real memory for socket buffers.
- Don't use fd count as sole capacity metric — also RAM, CPU, thread stacks, and backend connection limits.

---

## Related

[[non-blocking]] [[Blocking Vs Non-Blocking]] [[system call]] [[Buffer cache]] [[multiple levels of buffering]] [[cgroup (Control Group)]] [[context switching]]
