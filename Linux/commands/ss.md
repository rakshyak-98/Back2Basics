[[Linux network commands]] [[half-open connections]] [[Epoll]] [[connection chrun]] [[eBPF]] [[netstat]]

# ss

> Socket statistics from the kernel — faster, richer replacement for netstat on modern Linux.

```txt
        ss ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Go-to tool for “who is listening,” CLOSE-WAIT vs TIME-WAIT, and Recv-Q/Send-Q…

## Sources
- [man ss](https://man7.org/linux/man-pages/man8/ss.8.html) — deep-dive
- [Wikipedia — ss (utility)](https://en.wikipedia.org/wiki/Ss_(utility)) — overview

## Key Concepts
- **LISTEN / ESTABLISHED / TIME-WAIT / CLOSE-WAIT:** states tell you handshake, app bugs, or churn.
- **Recv-Q / Send-Q:** unread bytes vs unacked bytes — slow app vs slow peer/network.
- **`-luntp`:** listen + UDP + numeric + TCP + process — default inventory one-liner.
- **Filters:** ss filter syntax (`sport = :443`), not grep alone.


- **Core:** `ss` reads `/proc/net/*` and netlink

## Technical Details
```
Client ──SYN──► LISTEN (ss -lnt)
         ◄──SYN-ACK──
         ESTABLISHED (ss -tn)
         ◄──FIN──  CLOSE-WAIT / TIME-WAIT (ss -tan state …)
```

| vs | ss | netstat |
|----|-----|---------|
| Speed on 10k+ sockets | Fast | Slow |
| TCP internals (`ss -ti`) | Yes | Limited |
| Default on modern distros | iproute2 | often deprecated |
| Process column (`-p`) | Needs root/CAP | Same |

```bash
ss -luntp
ss -tan
ss -s
ss -lntp 'sport = :443'
sudo ss -lntp 'sport = :443'
ss -tn dst 10.0.1.50 and dport = 5432
ss -ti
ss -tan state time-wait
ss -tan state established
ss -tan state syn-recv
ss -tan state close-wait
```

| State | Meaning | Worry when |
|-------|---------|------------|
| `LISTEN` | Accept queue open | Recv-Q ≈ backlog → SYN flood or slow accept |
| `ESTAB` | Connected | High Send-Q → peer not ACKing / network |
| `SYN-SENT` / `SYN-RECV` | Handshake in flight | Firewall, backlog, half-open |
| `CLOSE-WAIT` | Peer closed, app hasn’t `close()` | App bug — FD leak |
| `TIME-WAIT` | Local closed cleanly | Storm → ephemeral port exhaustion |
| `UNCONN` | UDP idle | Expected for datagram sockets |

- **Recv-Q:** bytes in kernel recv buffer not yet read → app slow or blocked ev…
- **Send-Q:** bytes sent, not ACKed → congestion or peer window zero.

- Half-open flow: `ss -s` → `state syn-recv` → `state close-wait -p` → `ss -ti`…

| Symptom | Check | Fix |
|---------|-------|-----|
| Port already in use | `ss -lntp 'sport = :8080'` | Kill stale process; reuse policy; restart |
| Process up, unreachable | `ss -lnt` vs curl/nc | Bound to `127.0.0.1`; wrong iface; firewall |
| Many CLOSE-WAIT | `ss -tan state close-wait -p` | App not closing after FIN |
| TIME-WAIT thousands | `ss -s`; count time-wait | [[connection chrun]] — reuse, port range |
| Listen backlog drops | Recv-Q on LISTEN | Raise `somaxconn`; faster accept |

## Mistakes to Avoid
- **Mistake:** Running without root and trusting an empty `-p` column
- **Mistake:** Running `ss` on the host namespace and expecting container local…
- **Mistake:** Grepping instead of learning ss filter syntax when the filter si…

## Pros/Cons or Trade-offs
- **Pro:** Fast, filterable, shows TCP internals (`-ti`).
- **Con:** Point-in-time only — no history without flow logs or eBPF.

## Comparison
- vs [[netstat]]: prefer `ss` everywhere modern Linux is available.
- vs tcpdump: `ss` is state; capture is payloads and packet timing.


### Use cases
- Port inventory, DB pool leak hunts, and load-balancer timeout / half-open dia…

- **Example:** nginx upstream stuck
