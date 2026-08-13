[[Operating System]] [[system call]] [[Buffer cache]] [[context switching]] [[kernel ring buffer]]

# Kernel subsystem

> A kernel subsystem is a major functional area inside monolithic kernels like Linux — scheduler, memory management, VFS, networking, block layer — sharing address space but modular boundaries.

Linux organizes work into subsystems with clear APIs:

| Subsystem | Responsibility |
|-----------|------------------|
| Scheduler | [[Thread]] placement, [[context switching]] |
| MM | Pages, [[Heap memory]] backing, [[Buffer cache]] |
| VFS | Paths, inodes, [[file descriptors]] |
| Block layer | Queues to [[Persistent Block Storage]] |
| Net stack | Sockets, protocols |

Loadable **kernel modules** extend subsystems without full rebuild. eBPF programs attach to hooks in networking and tracing.

User entry is almost always [[system call]]; diagnostics use `procfs`, `sysfs`, `tracepoints`, and [[kernel ring buffer]] messages.

## Sources

- Robert Love, *Linux Kernel Development*
- Linux kernel documentation: [Core API](https://docs.kernel.org/core-api/index.html)
- Wikipedia: [Monolithic kernel](https://en.wikipedia.org/wiki/Monolithic_kernel)
