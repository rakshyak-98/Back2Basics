[[Operating System]] [[system call]] [[Buffer cache]] [[context switching]] [[kernel ring buffer]] [[Thread]] [[Heap memory]] [[file descriptors]] [[Persistent Block Storage]]

# Kernel subsystem

> A kernel subsystem is a major functional area inside monolithic kernels like Linux — scheduler, MM, VFS, net, block — shared address space with modular boundaries.

## Interview Relevance

Map a syscall to the subsystem it hits (VFS vs net vs block) and name how modules/eBPF extend those areas.

## Sources

- Robert Love, *Linux Kernel Development* — deep-dive
- [Linux kernel docs — Core API](https://docs.kernel.org/core-api/index.html) — deep-dive
- [Wikipedia — Monolithic kernel](https://en.wikipedia.org/wiki/Monolithic_kernel) — overview

## Key Concepts

- **Monolithic sharing:** subsystems share kernel address space.
- **Clear APIs:** scheduler, MM, VFS, block, net.
- **Modules:** extend without full rebuild.
- **User entry:** almost always [[system call]].

## Technical Details

| Subsystem | Responsibility |
|-----------|------------------|
| Scheduler | [[Thread]] placement, [[context switching]] |
| MM | Pages, [[Heap memory]] backing, [[Buffer cache]] |
| VFS | Paths, inodes, [[file descriptors]] |
| Block layer | Queues to [[Persistent Block Storage]] |
| Net stack | Sockets, protocols |

Diagnostics: `procfs`, `sysfs`, tracepoints, [[kernel ring buffer]]. eBPF attaches to networking/tracing hooks.

## Real-World Applications

Driver modules, tracing production kernels, and explaining where a slow `read()` spends time.

## Pros/Cons or Trade-offs

- **Pro:** Fast in-kernel calls between subsystems.
- **Con:** Bugs can take down the whole machine.
- **Trade-off:** monolith performance vs microkernel isolation.

## Comparison

- vs userspace daemons: policy often in userspace; mechanism in subsystems.
- vs [[system call]]: syscall is the gate; subsystem is the implementation area.

## Mistakes to Avoid

- Blaming “the kernel” without naming the subsystem.
- Loading unsigned/out-of-tree modules without crash risk awareness.
- Ignoring module/taint state when debugging oopses.
