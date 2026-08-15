[[Operating System]] [[Linux Process Theory]] [[CLI]] [[Commands]] [[systemd]] [[Memory management]] [[Epoll]] [[INDEX]]

# Linux

> Linux — the kernel plus userland that runs most servers; you control processes, files, networking, and services from the shell.

## Interview Relevance
Linux questions probe processes, permissions, networking basics, and how you debug with `ps`, `ss`, logs, and systemd. Staff signal: reason about OOM, file descriptors, and cgroups — not only memorize commands.

## Sources
- [Linux man-pages project](https://www.kernel.org/doc/man-pages/) — deep-dive
- [Wikipedia — Linux](https://en.wikipedia.org/wiki/Linux) — overview
- [systemd documentation](https://systemd.io/) — overview

## Core Definition
Linux is a Unix-like operating system kernel (plus distributions’ userland). Applications run as processes with virtual memory, interact via system calls, and are isolated by UIDs, namespaces, and optional containers.

## Key Concepts
- **Process model:** PID, parent/child, signals, nice/priority ([[Linux Process Theory]], [[process]]).
- **Filesystem:** Everything-as-file tradition; mounts, permissions, inodes ([[file mount]], [[etc files]]).
- **Init / services:** [[systemd]] units replace classic SysV for most distros.
- **Networking:** interfaces, routing, `ss`/`ip`, firewall ([[Commands]], [[ip]]).
- **Memory & I/O:** page cache, OOM killer, epoll for scalable I/O ([[Memory management]], [[Epoll]], [[OOM (Linux Out Of Memory)]]).

## Technical Details
```txt
User apps
   │ syscalls
   ▼
Kernel (sched, VFS, net, mm)
   │
   ▼
Hardware / hypervisors / containers
```

Routing by job:

| Need | Start here |
|------|------------|
| Everyday commands | [[Commands]] · [[CLI]] |
| Process debugging | [[Linux Process Theory]] · [[ps]] · [[top]] |
| Services | [[systemctl]] · [[journalctl]] |
| Packages | [[apt package manager]] |
| Memory pressure | [[OOM (Linux Out Of Memory)]] · [[Memory management]] |
| Desktop / display | [[display server]] · [[wayland]] · [[x11]] |

## Real-World Applications
Production box: service won’t start → `systemctl status` → `journalctl -u` → check ports with `ss -lntp` → confirm disk and OOM. Same mental model inside containers (still Linux, smaller userland).

## Pros/Cons or Trade-offs
- **Pro:** Ubiquitous servers, rich tooling, scriptable ops.
- **Con:** Distro drift; permission and SELinux surprises; footguns with `rm`, `chmod`, and firewall rules.

## Comparison
vs Windows Server: different service model, permissions, and tooling. vs macOS: Darwin/BSD userland similarities, not identical. Containers ([[Docker]]) share the host kernel — Linux skills transfer directly.

## Mistakes to Avoid
- Debugging apps without checking disk, memory, and file descriptor limits.
- Running everything as root “to make it work.”
- Confusing container PID 1 / signal behavior with bare-metal habits.
