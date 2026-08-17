[[Operating System]] [[Linux Process Theory]] [[NodeJS CLI]] [[Commands]] [[systemd]] [[Memory management]] [[Epoll]] [[INDEX]]

# Linux

> Linux — the kernel plus userland that runs most servers; you control processes, files, networking, and services from the shell.

```txt
        Linux ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Linux questions probe processes, permissions, networking basics, and how you …

## Sources
- [Linux man-pages project](https://www.kernel.org/doc/man-pages/) — deep-dive
- [Wikipedia — Linux](https://en.wikipedia.org/wiki/Linux) — overview
- [systemd documentation](https://systemd.io/) — overview

## Key Concepts
- **Process model:** PID, parent/child, signals, nice/priority ([[Linux Process Theory]], [[proces…
- **Filesystem:** Everything-as-file tradition
- **Init / services:** [[systemd]] units replace classic SysV for most distros.
- **Networking:** interfaces, routing, `ss`/`ip`, firewall ([[Commands]], [[ip]]).
- **Memory & I/O:** page cache, OOM killer, epoll for scalable I/O ([[Memory management]], [[Epol…


- **Core:** Linux is a Unix-like operating system kernel (plus distributions’ userland)

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

- Routing by job:

| Need | Start here |
|------|------------|
| Everyday commands | [[Commands]] · [[NodeJS CLI]] |
| Process debugging | [[Linux Process Theory]] · [[ps]] · [[top]] |
| Services | [[systemctl]] · [[journalctl]] |
| Packages | [[apt package manager]] |
| Memory pressure | [[OOM (Linux Out Of Memory)]] · [[Memory management]] |
| Desktop / display | [[display server]] · [[wayland]] · [[x11]] |

## Mistakes to Avoid
- **Mistake:** Debugging apps without checking disk, memory, and file descripto…
- **Mistake:** Running everything as root “to make it work.”
- **Mistake:** Confusing container PID 1 / signal behavior with bare-metal habi…

## Pros/Cons or Trade-offs
- **Pro:** Ubiquitous servers, rich tooling, scriptable ops.
- **Con:** Distro drift; permission and SELinux surprises; footguns with `rm`, `chmod`, and firewall rules.

## Comparison
- vs Windows Server: different service model, permissions, and tooling. vs macO…


### Use cases
- Production box: service won’t start → `systemctl status` → `journalctl -u` → …
