[[process]] [[Linux cgroup]] [[Memory management]] [[Epoll]]

# eBPF

> Extended Berkeley Packet Filter (eBPF) lets verified programs run in the Linux kernel safely — for tracing, networking, security, and cgroup-aware policy without loading a custom kernel module.





## Interview Relevance
Hot SRE / platform topic: explain verifier + JIT, name attach points (tracepoints, XDP, cgroup), and give an ops use case (latency tracing, Cilium). Distinguishes “heard of bpftrace” from “knows why it is safer than a kernel module.”

## Sources
- [BPF Documentation — kernel.org](https://www.kernel.org/doc/html/latest/bpf/index.html) — deep-dive
- [bpf(2) man page](https://man7.org/linux/man-pages/man2/bpf.2.html) — deep-dive

## Core Definition
eBPF programs attach to kernel hooks. The **verifier** rejects unsafe code (unbounded loops, bad memory access); accepted programs are **JIT**-compiled. User space loads them via the `bpf()` syscall (libbpf, BCC, bpftrace).

## Key Concepts
- **Hooks:** Tracepoints, kprobes/uprobes, cgroup sockets, XDP on NICs, LSM hooks.
- **Verifier:** Static checks before the program may run in kernel context.
- **Maps:** Shared key/value state between programs and user space.
- **CO-RE / libbpf:** Compile once, run across kernel versions with BTF.
- **Privilege:** Often needs `CAP_BPF` / root; unprivileged BPF may be disabled.

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

Modern container networking (Cilium) and some IO policies attach BPF at **cgroup** or socket level — see [[Linux cgroup]].

| Symptom | Check |
|---------|-------|
| `bpf: Operation not permitted` | `kernel.unprivileged_bpf_disabled`; need CAP_BPF / root |
| Program load fails verifier | `dmesg` for verifier log; simplify accesses |
| No events | Wrong tracepoint — `bpftrace -l 'tracepoint:*'` |

## Real-World Applications
On a latency spike, run `bpftrace`/`biolatency` to see syscall or block-IO histograms without rebuilding the kernel or shipping a proprietary module.

## Pros/Cons or Trade-offs
- **Pro:** Safe, dynamic kernel instrumentation and high-performance datapaths without reboot.
- **Con:** Verifier limits complexity; tooling and kernel BTF requirements vary by distro age.

## Comparison
vs kernel modules: modules are powerful but crash the box on bugs; eBPF is constrained and verified. vs `strace`: strace stops on every syscall (heavy); eBPF aggregates in-kernel with far lower overhead. vs [[Epoll]]: epoll is a userspace I/O readiness API; eBPF observes/acts inside the kernel.

## Mistakes to Avoid
- Treating bpftrace one-liners as free on huge fleets without CPU budget checks.
- Debugging “no events” without confirming the tracepoint name exists on that kernel.
- Confusing classic cBPF (socket filters) with modern eBPF’s broader attach model.
