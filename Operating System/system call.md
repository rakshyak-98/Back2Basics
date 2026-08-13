[[Operating System]] [[file descriptors]] [[fsync]] [[process]] [[Epoll]] [[handle]]

# System call

> A system call is the controlled gateway from user mode into the kernel — open files, map memory, spawn processes, send packets — with privilege checks on every entry.

User code cannot touch device registers directly. It places the **syscall number** and arguments in registers, executes `syscall` (x86-64) or `svc` (ARM), and traps to the kernel handler table.

```txt
write(fd, buf, n) → libc stub → syscall → sys_write → VFS/block/net
```

Returns success value or `-1` with `errno`. Blocking syscalls sleep the [[Thread]] ([[Blocking]]); non-blocking return `EAGAIN` ([[non-blocking]]).

Tracing: `strace -p PID`; production: eBPF ([[Linux/eBPF]]).

Durability example: [[fsync]] after [[Buffer cache]] writes.

## Sources

- Kerrisk, *The Linux Programming Interface*
- Linux syscall(2), individual syscall pages on man7.org
- Wikipedia: [System call](https://en.wikipedia.org/wiki/System_call)
