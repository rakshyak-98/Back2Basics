[[process]] [[Linux cgroup]] [[OOM (Linux Out Of Memory)]] [[Epoll]] [[Memory management]]

# Linux Process Theory

> Process theory explains how the kernel schedules, isolates, and accounts for work — background you need before tuning PIDs, cgroups, or OOM behavior.

```txt
        Linux Process Theo ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Foundational systems interview material: `fork`/`exec`/`wait`, zombie vs orph…

## Sources
- Kerrisk, *The Linux Programming Interface* — deep-dive
- `man 2 clone`, `man 7 namespaces` — deep-dive

## Key Concepts
- **fork → exec → exit → wait:** Lifecycle and reaping.
- **Zombie:** Exited child until the parent `wait`s.
- **States:** R/S/D/Z/T — especially uninterruptible `D` during I/O.
- **Copy-on-write:** `fork()` shares pages until write — memory accounting surprise.
- **Isolation kit:** cgroups, namespaces, capabilities, seccomp.


- **Core:** A **process** is an address space plus resources (file descriptors, credentia…

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

- Containers combine these; on bare metal you still see slices under systemd.

## Mistakes to Avoid
- **Mistake:** Calling zombies a memory leak
- **Mistake:** Expecting `kill -9` to clear `D` state during broken disk/NFS I/O
- **Mistake:** Ignoring COW after fork when estimating memory for large parent …

## Pros/Cons or Trade-offs
- **Pro:** Rich isolation primitives enable containers and safe multi-tenant hosts.
- **Con:** Mental model is deep — misreading zombies as “leaked memory” or `D` as “ignore SIGKILL bug” wastes incident time.

## Comparison
- vs [[process]]: operational commands (`ps`, signals) vs this theory note. vs …


### Use cases
- A stuck deploy shows many `D` state processes on a failing NFS mount
