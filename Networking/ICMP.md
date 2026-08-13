<!-- note-strategy: operational -->
[[Networking]] [[auto-pong]] [[MTU (Maximum Transmission Unit)]] [[Packet Fragment]]

# ICMP

> ICMP (Internet Control Message Protocol) is the network’s error-and-echo channel — ping and “frag needed” ride here, not your app port.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Hosts and routers send small control messages (echo, unreachable, time exceeded) so you can diagnose paths and so IP can signal problems.

```txt
ping:  Echo Request ──► peer
       Echo Reply   ◄── peer   (auto-pong in the kernel)

PMTUD: packet + DF too big ──► router
       ICMP Dest Unreachable (frag needed) ◄──
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Echo Request / Reply** | ping / pong | “Liveness + RTT, not app health.” |
| **Dest Unreachable** | No route / port / needfrag | “PMTUD depends on frag-needed.” |
| **Time Exceeded** | TTL hit zero | “What traceroute listens for.” |
| **Sequence number** | Matches reply to request | “Detect loss; wrap at 65535.” |
| **ICMPv6** | IPv6 control plane | “Neighbor discovery uses it too — don’t blanket-block.” |

### Echo sequence (ping)

| Field | Job |
|-------|-----|
| Identifier | Which ping process |
| Sequence | Which probe in the series |
| RTT | Send time vs reply time |

---

## Standard config / commands

```bash
ping -c 4 8.8.8.8
ping -c 4 -W 2 <host>           # per-probe deadline
ping -M do -s 1472 <host>       # DF + size → PMTUD helper

traceroute <host>               # UDP/ICMP variants by OS
mtr -rw <host>                  # ongoing loss/latency view
```

| Knob | Why it matters |
|------|----------------|
| `-M do` / DF | Surfaces path MTU problems |
| Firewall ICMP allowlist | Echo vs unreachable vs time-exceeded are different |
| Rate limits | Cloud providers throttle ICMP — flaky ping ≠ flaky TCP |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| ping fails, HTTPS works | ICMP blocked | Allow echo or stop using ping as sole check |
| Large transfers hang | Frag-needed dropped | Allow ICMP type 3 code 4 (v4) / Packet Too Big (v6) |
| traceroute all `* * *` | Probes filtered | Try TCP traceroute; check intermediate ACLs |
| High loss on ping only | ICMP policed | Measure with TCP/`mtr` on real ports |

---

## Gotchas

> [!WARNING]
> **Silent ICMP block breaks PMTUD** — classic “small packets work, large payloads stall” blackhole.

> [!WARNING]
> **ping success ≠ service up** — probe the listening TCP/UDP port or HTTP path.

> [!WARNING]
> **IPv6** — filtering “all ICMP” breaks Neighbor Discovery and PMTUD; be surgical.

---

## When NOT to use

- **Primary production health checks** — check the application protocol.
- **Security through “block all ICMP”** — you trade stealth for brittle paths.
- **Assuming sequence gaps mean malice** — loss, reorder, and rate limits are common.

---

## Related

[[Networking]] [[auto-pong]] [[MTU (Maximum Transmission Unit)]] [[Packet Fragment]] [[TCP]] [[UDP]]
