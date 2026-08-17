[[Linux network commands]] [[ip]] [[ss]] [[top]] [[netstat]]

# nload

> Live per-interface bandwidth graphs from `/proc/net/dev` — “is this NIC saturated?” not “which process?”.





## Interview Relevance
Shows you can pick the right granularity for network triage: interface rates first, then flow or process tools when the graph alone is not enough.

## Sources
- [nload on GitHub](https://github.com/rolandviehbeck/nload) — overview
- [Wikipedia — nload](https://en.wikipedia.org/wiki/nload) — overview

## Core Definition
`nload` polls `/proc/net/dev` (or pcap on some builds) and draws moving averages for incoming and outgoing throughput per interface — one screen, two graphs.

## Key Concepts
- **Per-interface only:** answers saturation of `eth0`/`ens5`, not which PID or remote IP.
- **Moving average window:** F2 shortens/lengthens the average — too long hides spikes.
- **Predictable naming:** cloud VMs often use `ens*` / `enp*`, not `eth0`.
- **Bond/VLAN:** traffic may appear on `bond0`, not the physical slave.

## Technical Details
```
/proc/net/dev ──► nload ──► TUI graph (in/out Mbps per iface)
```

| Tool | Granularity | Best for |
|------|-------------|----------|
| `nload` | Per interface | "Is eth0 pegged?" |
| `iftop` | Per connection | "Which remote IP?" |
| `nethogs` | Per process | "Which PID?" |
| `ip -s link` | Counter snapshot | Scripting, no TUI |
| `sar -n DEV` | Historical (sysstat) | Post-incident |

```bash
nload
nload eth0
nload ens5
nload -t 200 eth0
nload eth0 wlan0
```

Keys while running: ←/→ switch device, F2 options (avg window, unit), F5 save settings, `q` quit.

```bash
ip -s link show eth0
watch -n1 'ip -s link show eth0'
sar -n DEV 1 5
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Shows 0 on busy host | Wrong interface name | `ip link`; cloud uses `ens*`, not `eth0` |
| Graph flat but users slow | Not bandwidth (latency, CPU) | [[ss]], `ping`, app metrics |
| Can't identify culprit | Interface-level only | `iftop`, `nethogs`, `tcpdump` |
| Spikes not visible | Avg window too long | F2 → shorten avg time |

## Real-World Applications
Incident “is the uplink maxed?” — open `nload ens5` while correlating with load balancer metrics.

**Example:** SSH into a VM over the same interface you are measuring skews the graph; prefer a side-channel or short sample windows.

## Pros/Cons or Trade-offs
- **Pro:** Instant visual RX/TX without a monitoring stack.
- **Con:** No per-process attribution and not suitable as a production dashboard.

## Comparison
- vs `iftop` / `nethogs`: those answer who; nload answers how much on the NIC.
- vs `sar -n DEV`: historical; nload is live TUI only.

## Mistakes to Avoid
- Assuming `eth0` — always `ip link` first after predictable naming.
- Watching loopback (`lo`) and calling it “network” when local proxy/db chat dominates.
- Expecting nload on minimal images — install it or fall back to `ip -s link`.
