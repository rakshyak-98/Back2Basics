[[process]] [[Linux cgroup]] [[OOM (Linux Out Of Memory)]]

# Linux Process Theory

> Process theory explains how the kernel schedules, isolates, and accounts for work — the background you need before tuning PIDs, cgroups, or OOM behavior.

A **process** is an address space + resources (fds, credentials, namespaces). **Threads** are tasks sharing that address space. The scheduler picks runnable tasks on CPUs; **cgroups** cap groups of tasks; **namespaces** isolate views (PID, mount, network).

## Lifecycle

```
fork() ──► child ──► execve("binary") ──► running ──► exit(status)
   │                                              │
   └─ parent waitpid() ◄── zombie until reaped ───┘
```

## States (simplified)

| State | Meaning |
|-------|---------|
| R | Runnable |
| S | Interruptible sleep (waiting on event) |
| D | Uninterruptible sleep (usually I/O) — cannot SIGKILL until I/O completes |
| Z | Zombie — exited, awaiting parent |
| T | Stopped (job control / SIGSTOP) |

```bash
ps -eo stat,pid,cmd | head
```

## Isolation building blocks

| Mechanism | What it isolates |
|-----------|------------------|
| **cgroup** | CPU, memory, IO, pids — [[Linux cgroup]] |
| **namespace** | PID tree, mounts, network, hostname |
| **capabilities** | Split root powers (CAP_NET_BIND_SERVICE, …) |
| **seccomp** | Filter syscalls |

Containers combine these; on bare metal you still see slices under systemd.

## Copy-on-write after fork

`fork()` shares physical pages until written — important for memory accounting: fork bombs and large parent processes affect children.

## Related

[[process]] · [[Epoll]] · [[Linux cgroup]] · [[Memory management]]

## Sources

- Kerrisk, *The Linux Programming Interface*
- `man 2 clone`, `man 7 namespaces`
