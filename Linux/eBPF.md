[[process]] [[Linux cgroup]] [[Memory management]] [[Epoll]]

# eBPF

> Extended Berkeley Packet Filter (eBPF) lets verified programs run in the Linux kernel safely — for tracing, networking, security, and cgroup-aware policy without loading a custom kernel module.

```txt
        eBPF ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Hot SRE / platform topic: explain verifier + JIT, name attach points (tracepo…

## Sources
- [BPF Documentation — kernel.org](https://www.kernel.org/doc/html/latest/bpf/index.html) — deep-dive
- [bpf(2) man page](https://man7.org/linux/man-pages/man2/bpf.2.html) — deep-dive

## Key Concepts
- **Hooks:** Tracepoints, kprobes/uprobes, cgroup sockets, XDP on NICs, LSM hooks.
- **Verifier:** Static checks before the program may run in kernel context.
- **Maps:** Shared key/value state between programs and user space.
- **CO-RE / libbpf:** Compile once, run across kernel versions with BTF.
- **Privilege:** Often needs `CAP_BPF` / root; unprivileged BPF may be disabled.


- **Core:** eBPF programs attach to kernel hooks. The **verifier** rejects unsafe code (u…

## Technical Details
| Use case | Typical tools |
|----------|---------------|
| Latency / syscall tracing | `bpftrace`, BCC `execsnoop`, `biolatency` |
| Network policy / load balancing | Cilium, XDP programs |
| Security auditing | Falco, Tetragon |
| Performance counters | `perf`, CO-RE libbpf tools |

```bash
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_openat { printf("%s %s\n", comm, str(args->filename)); }'
sudo /usr/share/bcc/tools/execsnoop
sudo bpftool prog show
sudo bpftool map show
```

- Modern container networking (Cilium) and some IO policies attach BPF at **cgr…

| Symptom | Check |
|---------|-------|
| `bpf: Operation not permitted` | `kernel.unprivileged_bpf_disabled`; need CAP_BPF / root |
| Program load fails verifier | `dmesg` for verifier log; simplify accesses |
| No events | Wrong tracepoint — `bpftrace -l 'tracepoint:*'` |

## Mistakes to Avoid
- **Mistake:** Treating bpftrace one-liners as free on huge fleets without CPU …
- **Mistake:** Debugging “no events” without confirming the tracepoint name exi…
- **Mistake:** Confusing classic cBPF (socket filters) with modern eBPF’s broad…

## Pros/Cons or Trade-offs
- **Pro:** Safe, dynamic kernel instrumentation and high-performance datapaths without reboot.
- **Con:** Verifier limits complexity; tooling and kernel BTF requirements vary by distro age.

## Comparison
- vs kernel modules: modules are powerful but crash the box on bugs


### Use cases
- On a latency spike, run `bpftrace`/`biolatency` to see syscall or block-IO hi…
