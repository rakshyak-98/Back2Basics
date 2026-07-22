[[Blocking Vs Non-Blocking]] [[file descriptors]] [[system call]] [[Event Loop]] [[context switching]]

# Non-blocking I/O

> Syscall returns immediately with data, partial data, or `EAGAIN`/`EWOULDBLOCK` — caller polls or uses an event loop — **Stevens**.

---

## Mental model

**Blocking:** `read(fd)` sleeps until data arrives — thread tied up, scheduler switches away.

**Non-blocking:** set `O_NONBLOCK` on fd; `read()`/`write()`/`accept()`/`connect()` return instantly. If operation can't complete: `-1` + `errno == EAGAIN` (or `EINPROGRESS` for connect).

```txt
blocking thread:  read() ──sleep──► data ──► return
non-blocking:     read() ──► EAGAIN ──► epoll_wait ──► read() ──► data
```

**Level-triggered vs edge-triggered (epoll):**
- **LT (default):** fd stays "ready" until you drain — forgiving.
- **ET:** notify once on transition — must read until `EAGAIN` or miss events.

**Not the same as async/await:** language async is syntactic sugar over non-blocking fds + reactor (epoll/kqueue/IOCP) + thread pool for CPU work.

**Service stack mapping:**
| Runtime | Reactor |
|---------|---------|
| Node.js | libuv → epoll/kqueue |
| Go net | netpoller + epoll |
| Java NIO | Selector / epoll (Linux) |
| nginx | epoll edge-triggered |

---

## Standard config / commands

### Set non-blocking (C)

```c
int fl = fcntl(fd, F_GETFL, 0);
fcntl(fd, F_SETFL, fl | O_NONBLOCK);
```

```c
ssize_t n = read(fd, buf, sizeof buf);
if (n < 0 && (errno == EAGAIN || errno == EWOULDBLOCK)) {
    /* register fd with epoll; return to event loop */
}
```

### Accept loop pattern

```c
int c = accept(listen_fd, ...);
if (c < 0 && errno == EAGAIN) return;  /* no pending connections */
fcntl(c, F_SETFL, O_NONBLOCK);
```

### Observe in prod

```shell
# Is fd non-blocking?
grep -l . /proc/PID/fd/* 2>/dev/null | head -1  # then
cat /proc/PID/fdinfo/N   # flags: O_NONBLOCK if set

strace -e read,write,accept,recv,send -p PID | grep EAGAIN

ss -tn state syn-recv   # backlog building if accept not keeping up
```

### Backpressure knobs

- **TCP:** listen backlog, read buffer drain rate, write buffer high-water marks.
- **Node:** pause/resume on streams; limit concurrent in-flight requests.
- **Go:** bounded channels; `http.Server` timeouts; `SetReadDeadline`.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| CPU 100%, low throughput | `strace` spam on EAGAIN tight loop | Fix busy-loop; use epoll/select; sleep/yield only as last resort |
| Connections stall silently | ET epoll, partial read | Read until EAGAIN on ET; or switch LT |
| Spurious wakeups / missed events | Edge-trigger without drain | Drain fd completely each wake |
| Latency under load | Event loop blocked on sync fs/CPU | Offload sync work to thread pool; see [[Blocking Vs Non-Blocking]] |
| `EMFILE` on accept burst | `accept` + slow fd handling | Accept queue + close excess; raise limits [[file descriptors]] |
| Works with curl, fails under load | Single-threaded loop starved | Scale workers; SO_REUSEPORT; profile event loop |

---

## Gotchas

> [!WARNING]
> **Busy-wait on EAGAIN** without epoll — burns a core. Classic bug when porting blocking code with "retry loops."

> [!WARNING]
> **Partial writes:** non-blocking `write()` may send fewer bytes — must buffer remainder and wait for `POLLOUT`.

> [!WARNING]
> **Disk "non-blocking" is messy.** Regular file I/O on Linux can still block in page cache path; true async disk often needs `io_uring` or thread pool — don't assume socket patterns apply to `read()` on ext4.

> [!WARNING]
> **Default blocking sockets in libraries.** Many HTTP clients create blocking fds unless configured — hidden thread pools block *for* you.

> [!WARNING]
> **`EINTR` vs `EAGAIN`:** signal interruption restarts syscalls differently — handle both in low-level loops.

**Containers:** CFS shares one event-loop thread easily starved if another container hogs CPU — p99 latency, not correctness bug.

---

## When NOT to use

- Simple CLI tools and batch jobs — blocking I/O + threads is fine.
- CPU-bound parallel work — threads/processes beat manual non-blocking complexity.
- When library already provides async API (don't rewrite epoll by hand unless you must).

---

## Related

[[Blocking Vs Non-Blocking]] [[Blocking]] [[file descriptors]] [[system call]] [[context switching]] [[thread pool]] [[CPU IO Bound Task]]
