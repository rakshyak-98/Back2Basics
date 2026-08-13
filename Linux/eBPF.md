[[process]] [[Linux cgroup]] [[Memory management]]

# eBPF

> Extended Berkeley Packet Filter (eBPF) lets verified programs run in the Linux kernel safely — for tracing, networking, security, and cgroup-aware policy without loading a kernel module.

**eBPF** programs attach to kernel hooks (tracepoints, kprobes, cgroup sockets, XDP on NICs). The **verifier** checks them for bounded loops and safe memory access before **JIT** compilation. User space loads programs with `bpf()` syscall helpers (libbpf, BCC, bpftrace).

## What operators use it for

| Use case | Typical tools |
|----------|---------------|
| Latency / syscall tracing | `bpftrace`, BCC `execsnoop`, `biolatency` |
| Network policy / load balancing | Cilium, XDP programs |
| Security auditing | Falco, Tetragon |
| Performance counters | `perf`, CO-RE libbpf tools |

## Quick tracing examples

```bash
# bpftrace one-liners (package: bpftrace)
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_openat { printf("%s %s\n", comm, str(args->filename)); }'

# BCC: new processes
sudo /usr/share/bcc/tools/execsnoop

# List loaded programs
sudo bpftool prog show
sudo bpftool map show
```

## cgroup + eBPF

Modern container networking (Cilium) and some OOM / IO policies attach BPF programs at **cgroup** or socket level — see [[Linux cgroup]] for resource hierarchy.

## Debugging

| Symptom | Check |
|---------|-------|
| `bpf: Operation not permitted` | `kernel.unprivileged_bpf_disabled`; need CAP_BPF / root |
| Program load fails verifier | `dmesg` for verifier log; simplify accesses |
| No events | Wrong tracepoint name — `bpftrace -l 'tracepoint:*'` |

## Related

[[process]] · [[Epoll]] · [[Linux cgroup]]

## Sources

- [BPF Documentation — kernel.org](https://www.kernel.org/doc/html/latest/bpf/index.html)
- [bpf(2) man page](https://man7.org/linux/man-pages/man2/bpf.2.html)
