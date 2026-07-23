[[Linux]] [[process]] [[Linux cgroup]] [[Commands]]

# eBPF

> One-line: run **verified sandboxed programs in the kernel** to observe or steer traffic, syscalls, and latency — without loading a kernel module. **Kerrisk / BPF docs + production observability practice.**

## Mental model

eBPF is a **JIT’d bytecode VM inside the kernel**. You attach small programs to hooks (kprobes, tracepoints, XDP, tc, cgroup, LSM, …); the **verifier** proves they terminate and cannot crash the kernel; maps pass data to user space.

```
App syscall ──► kernel hook ──► eBPF program ──► map / perf ring ──► bpftool / bpftrace / agent
                     ▲
               verifier (must pass)
```

| Layer | Tool | Operator use |
|-------|------|--------------|
| Inspect loaded programs | `bpftool` | What’s running, map dumps, pin paths |
| One-shot scripts | `bpftrace` | Fast triage on a box |
| Custom tools | BCC (Python) / libbpf (CO-RE) | Repeatable prod tooling |
| Dataplane | Cilium, Katran, Pixie | You debug their BPF, not rewrite the stack |

**CO-RE (Compile Once — Run Everywhere):** BTF + relocations let one binary run across kernel versions. Without CO-RE you ship per-kernel objects or rebuild on every node — painful in mixed fleets.

## Standard config / commands

```bash
# Kernel support (need 4.x+; 5.x+ for most prod tooling)
uname -r
grep CONFIG_BPF /boot/config-$(uname -r)   # CONFIG_BPF=y, CONFIG_BPF_SYSCALL=y

# What's loaded
sudo bpftool prog list
sudo bpftool map list
sudo bpftool link list                      # 5.7+ attachment handles

# Pin namespace (Cilium, systemd, custom agents persist here)
ls /sys/fs/bpf/

# One-liner latency (needs tracepoint support)
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_openat { @["open"] = count(); }
END { print(@); clear(@); }'

# BCC examples (package: bpfcc-tools)
sudo biolatency    # block I/O latency histogram
sudo execsnoop     # new processes
sudo tcplife       # TCP conn lifetime
sudo tcpretrans    # retransmits → packet loss / congestion signal
```

**Attach points operators actually use:**

| Hook | Question it answers |
|------|---------------------|
| kprobe / kretprobe | Function entry/return latency |
| tracepoint | Stable kernel events (preferred over kprobes when available) |
| `xdp` / `tc` | Drop, redirect, count packets before stack |
| cgroup skb | Per-container egress policy |
| USDT | User-space probes (needs symbols / build flags) |

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Failed to load BPF program` / verifier log | `dmesg \| tail`; run with `bpftool prog load` verbose | Reduce loops, bound memory, avoid illegal derefs; simplify program |
| `R1 type=scalar expected=ptr` in verifier dump | Read verifier rejection line-by-line | Init all vars; check null checks; use CO-RE helpers not raw casts |
| Tool works on one kernel, fails on another | `uname -r`; compare BTF: `ls /sys/kernel/btf/vmlinux` | Rebuild with CO-RE + matching libbpf; pin kernel floor in fleet |
| High CPU after attaching probe | `top` + `bpftool prog show id N` | Narrow probe set; use sampling; detach stale programs |
| `cannot attach kprobe` | `grep CONFIG_KPROBES`; secure boot / lockdown | Use tracepoints; or tracepoint-only build |
| Cilium / Pixie agent crash-loop | `bpftool prog`; agent logs; map pressure | Upgrade agent; check kernel BPF feature matrix |
| No events in bpftrace | `bpftrace -l 'tracepoint:*'` | Wrong probe name; missing CAP_BPF / root; probe disabled in kernel |

**Verifier failure playbook:**

1. Capture full verifier log (`-v` or kernel log).
2. Find first `R*` register type mismatch — that’s the bug, not the last line.
3. Common fixes: initialize stack slots; use `bpf_probe_read_kernel()` instead of direct deref; cap `#pragma unroll` loops.

**Production use cases (what staff actually deploy):**

- **Latency:** `biolatency`, `runqlat`, `offcputime` — “disk slow vs CPU wait vs lock” in one session.
- **Packet drop:** XDP drop counters; `tc` clsact; Cilium `hubble observe`; correlate with `ss -ti` retrans.
- **Syscall tracing:** `opensnoop`, `execsnoop`, `capable` — “what is this container doing?” without strace flood.
- **Security:** LSM BPF (file open, socket connect) — policy without kernel rebuild.

## Gotchas

> [!WARNING]
> **strace is not eBPF.** strace stops the world (ptrace); eBPF is lower overhead but needs kernel support and careful attach scope.

> [!WARNING]
> **Probes in prod:** kprobes on hot paths (e.g. `tcp_sendmsg`) can hurt at high QPS. Prefer tracepoints, sampling, or dedicated observability agents.

- **Map limits:** `kernel.bpf.max_*` sysctl and memlock ulimit — large maps fail mysteriously on first deploy.
- **BTF missing on custom kernels:** CO-RE tools silently fail or need `/sys/kernel/btf/vmlinux` from kernel package.
- **Orphan programs:** Crash without cleanup → `bpftool prog list` shows ghosts; reboot or manual detach.
- **Cgroup v1 vs v2:** cgroup-bpf attachment semantics differ; container runtimes assume v2 on modern distros.

## When NOT to use

- **First-line app debugging** — logs, metrics, and `strace -c` beat BPF for “why did my Python script fail”.
- **Permanent business logic in BPF** — keep policy in user space unless you need line-rate dataplane (XDP/LB).
- **Kernel without BPF syscall** — embedded/old kernels: use `perf`, `ftrace`, or vendor APM instead.
- **Full packet capture replacement** — eBPF samples/counts; use `tcpdump`/PCAP when you need every frame legally retained.

## Related

[[Epoll]] [[Linux cgroup]] [[process]] [[Linux out of memory daemon]] [[Commands]] [[Linux network commands]]
