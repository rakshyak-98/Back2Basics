[[process]] [[Linux cgroup]] [[OOM (Linux Out Of Memory)]] [[Epoll]] [[Memory management]]

# Linux Process Theory

> Process theory explains how the kernel schedules, isolates, and accounts for work — background you need before tuning PIDs, cgroups, or OOM behavior.





## Interview Relevance
Foundational systems interview material: `fork`/`exec`/`wait`, zombie vs orphan, task states (especially `D`), and how cgroups/namespaces compose into containers.

## Sources
- Kerrisk, *The Linux Programming Interface* — deep-dive
- `man 2 clone`, `man 7 namespaces` — deep-dive

## Core Definition
A **process** is an address space plus resources (file descriptors, credentials, namespaces). **Threads** are tasks sharing that address space. The scheduler picks runnable tasks; **cgroups** cap groups; **namespaces** isolate views (PID, mount, network).

## Key Concepts
- **fork → exec → exit → wait:** Lifecycle and reaping.
- **Zombie:** Exited child until the parent `wait`s.
- **States:** R/S/D/Z/T — especially uninterruptible `D` during I/O.
- **Copy-on-write:** `fork()` shares pages until write — memory accounting surprise.
- **Isolation kit:** cgroups, namespaces, capabilities, seccomp.

## Technical Details
```
fork() ──► child ──► execve("binary") ──► running ──► exit(status)
   │                                              │
   └─ parent waitpid() ◄── zombie until reaped ───┘
```

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

| Mechanism | What it isolates |
|-----------|------------------|
| **cgroup** | CPU, memory, IO, pids — [[Linux cgroup]] |
| **namespace** | PID tree, mounts, network, hostname |
| **capabilities** | Split root powers (CAP_NET_BIND_SERVICE, …) |
| **seccomp** | Filter syscalls |

Containers combine these; on bare metal you still see slices under systemd.

## Real-World Applications
A stuck deploy shows many `D` state processes on a failing NFS mount — SIGKILL will not help until storage recovers; fix the mount, not the kill signal.

## Pros/Cons or Trade-offs
- **Pro:** Rich isolation primitives enable containers and safe multi-tenant hosts.
- **Con:** Mental model is deep — misreading zombies as “leaked memory” or `D` as “ignore SIGKILL bug” wastes incident time.

## Comparison
vs [[process]]: operational commands (`ps`, signals) vs this theory note. vs threads: shared address space vs separate processes. vs [[OOM (Linux Out Of Memory)]]: OOM is what happens when memory accounting loses; process theory is the lifecycle underneath.

## Mistakes to Avoid
- Calling zombies a memory leak — they hold almost no resources beyond a task slot.
- Expecting `kill -9` to clear `D` state during broken disk/NFS I/O.
- Ignoring COW after fork when estimating memory for large parent processes.
