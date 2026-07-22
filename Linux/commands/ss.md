[[Linux network commands]] [[half-open connections]] [[Epoll]] [[connection chrun]]

# ss

> One-line: **socket statistics from the kernel** — faster, richer `netstat` replacement for listening ports, TCP state, queues, and process ownership. **First tool for “what is connected to what?”**

## Mental model

`ss` reads `/proc/net/*` and netlink — same truth the kernel uses for TCP/UDP state. No DNS, no guessing from `/proc/<pid>/fd` alone.

```
Client ──SYN──► LISTEN (ss -lnt)
         ◄──SYN-ACK──
         ESTABLISHED (ss -tn)
         ◄──FIN──  CLOSE-WAIT / TIME-WAIT (ss -tan state …)
```

| vs | ss | netstat |
|----|-----|---------|
| Speed on 10k+ sockets | Fast | Slow (linear scan) |
| TCP internals (`ss -ti`) | Yes | Limited |
| Default on modern distros | iproute2 | often symlink/deprecated |
| Process column (`-p`) | Needs root/CAP | Same |

## Standard config / commands

**Flags mnemonic:** `-l` listen, `-a` all (listen + established), `-n` numeric, `-t` TCP, `-u` UDP, `-p` process, `-i` TCP info.

```bash
# Baseline inventory (your old one-liner, expanded)
ss -luntp
# -l listening  -u UDP  -n no DNS  -t TCP  -p process (root)

# All TCP with state + queues
ss -tan

# Summary histogram — first stop in incidents
ss -s

# One port, who owns it
ss -lntp 'sport = :443'
sudo ss -lntp 'sport = :443'   # -p needs priv

# Established to a backend
ss -tn dst 10.0.1.50 and dport = 5432

# Sockets owned by a PID
ss -tp | awk -v pid=1234 '$0 ~ "pid="pid'

# TCP timer info (keepalive, retrans)
ss -ti

# Filter by TCP state (ss syntax, not grep)
ss -tan state time-wait
ss -tan state established
ss -tan state syn-recv
ss -tan state close-wait
```

**Common TCP state codes:**

| State | Meaning | Worry when |
|-------|---------|------------|
| `LISTEN` | Accept queue open | `Recv-Q` ≈ backlog → SYN flood or slow accept |
| `ESTAB` | Connected | High `Send-Q` → peer not ACKing / network issue |
| `SYN-SENT` / `SYN-RECV` | Handshake in flight | Many stuck → firewall, SYN backlog, half-open |
| `FIN-WAIT-1/2` | Local closed, waiting peer | Normal drain; huge counts → churn |
| `CLOSE-WAIT` | Peer closed, local app hasn’t `close()` | **App bug** — FD leak, missing cleanup |
| `TIME-WAIT` | Local side closed cleanly | Storm → ephemeral port exhaustion ([[connection chrun]]) |
| `UNCONN` | UDP idle | Expected for datagram sockets |

**Recv-Q / Send-Q (TCP):**

- `Recv-Q`: bytes in kernel recv buffer not yet read by app → app slow or blocked event loop ([[Epoll]]).
- `Send-Q`: bytes sent, not ACKed → network congestion or peer window zero.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| “Port already in use” | `ss -lntp 'sport = :8080'` | Kill stale process; `SO_REUSEADDR` policy; systemd restart |
| Service unreachable but process up | `ss -lnt` vs `curl` / `nc` | Binding `127.0.0.1` only; wrong interface; firewall |
| DB pool exhausted | `ss -tn dst dbhost:5432 \| wc -l` | Leaked connections; lower pool; fix CLOSE-WAIT in app |
| Many `CLOSE-WAIT` | `ss -tan state close-wait -p` | App not closing after FIN; trace code path |
| `TIME-WAIT` thousands | `ss -s`; `ss -tan state time-wait \| wc -l` | [[connection chrun]] — keepalive, reuse, tune `ip_local_port_range` |
| Half-open / ghost clients | `ss -tan state syn-recv`; [[half-open connections]] | LB timeout; `tcp_syncookies`; app read side dead |
| Listen backlog drops | `ss -lnt` Recv-Q on LISTEN line | Increase `somaxconn`; faster accept loop |
| Mystery outbound | `ss -tnp` as root | Identify PID; block egress if exfil |

**Half-open diagnosis flow:**

1. `ss -s` — synrecv count, timewait, orphaned.
2. `ss -tan state syn-recv` — stuck handshakes?
3. `ss -tan state close-wait -p` — local app not closing?
4. `ss -ti` on affected ESTAB — retrans, rtt, cwnd.

```bash
# Example: nginx upstream stuck
ss -tan state established '( dport = :8080 )' | wc -l
ss -o state established '( dport = :8080 )'   # timer=keepalive detail
```

## Gotchas

> [!WARNING]
> **Without root, `-p` is empty or partial.** Always `sudo ss -luntp` when you need the owning process.

- **Filters use ss syntax** — `ss filter` not grep; wrong filter silently returns empty.
- **`ss -s` “TCP: inuse X orphaned Y”** — orphaned = no socket owner in userspace; often mid-close or namespace edge cases.
- **Containers:** run `ss` **inside** the net namespace (`nsenter`, `docker exec`) — host view shows veth, not app’s localhost.
- **IPv6 bracket notation** — filters may need `( sport = :443 )` form for clarity.

## When NOT to use

- **Packet contents or TLS plaintext** — use `tcpdump` / wire capture.
- **Routing / ARP / firewall rules** — `ip route`, `iptables/nft`, `conntrack -L`.
- **Historical connections** — `ss` is point-in-time; use flow logs or eBPF for past state.

## Related

[[Linux network commands]] [[half-open connections]] [[Epoll]] [[connection chrun]] [[eBPF]]
