[[Operating System]] [[file descriptors]] [[fsync]] [[process]] [[Epoll]] [[handle]] [[Thread]] [[Blocking]] [[non-blocking]] [[Buffer cache]] [[Linux/eBPF]]

# System call

> A system call is the controlled gateway from user mode into the kernel — open files, map memory, spawn processes, send packets — with privilege checks on every entry.

```txt
        System call ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Walk user→kernel transition (`syscall`/`svc`), errno returns, blocking vs `EA…

## Sources
- Kerrisk, *The Linux Programming Interface* — deep-dive
- Linux `syscall(2)` and man7.org syscall pages — deep-dive
- [Wikipedia — System call](https://en.wikipedia.org/wiki/System_call) — overview

## Key Concepts
- **Privilege boundary:** user cannot touch devices directly.
- **ABI:** syscall number + args in registers; trap to handler table.
- **Returns:** success value or `-1` + `errno`.
- **Blocking modes:** sleep ([[Blocking]]) vs `EAGAIN` ([[non-blocking]]).

## Technical Details
```txt
write(fd, buf, n) → libc stub → syscall → sys_write → VFS/block/net
```

- Tracing: `strace -p PID`; production: eBPF ([[Linux/eBPF]]).
- Durability example: [[fsync]] after [[Buffer cache]] writes.
- Objects named via [[file descriptors]] / [[handle]]s

## Mistakes to Avoid
- **Mistake:** Ignoring `EINTR` and short reads/writes
- **Mistake:** Assuming every libc function is a syscall
- **Mistake:** Using `strace` on huge fleets without sampling (overhead)

## Pros/Cons or Trade-offs
- **Pro:** Security and mediation in one place.
- **Con:** Mode-switch cost; over-syscalling hurts.
- **Trade-off:** rich syscalls vs vDSO/userpath shortcuts for hot ops.

## Comparison
- vs library call: libc may not enter the kernel (vDSO/pure user).
- vs ioctl: still a syscall, but device-specific multiplex.


### Use cases
- Every userspace program
