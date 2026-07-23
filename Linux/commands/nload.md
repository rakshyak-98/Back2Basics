[[Linux network commands]] [[ip]] [[ss]] [[top]]

# nload

> One-line: real-time **per-interface bandwidth** graph in the terminal — quick "who is saturating the NIC?" without Prometheus. **Legacy but still useful on jump boxes.**

## Mental model

`nload` polls `/proc/net/dev` (or pcap on some builds) and draws moving averages for **incoming** and **outgoing** throughput per interface. One screen, two graphs — not per-process, not per-connection.

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

## Standard config / commands

```bash
# All interfaces, interactive switch with arrow keys
nload

# Single interface
nload eth0
nload ens5                    # common on cloud VMs

# Specify refresh interval (milliseconds)
nload -t 200 eth0

# Multiple interfaces at once
nload eth0 wlan0

# Units: human readable (default kbit/s); toggle in UI with 'm'
# Keys while running:
#   ←/→  switch device
#   F2   show options (avg window, unit)
#   F5   save settings
#   q    quit
```

**Quick alternatives when nload isn't installed:**

```bash
# One-shot counters
ip -s link show eth0

# Watch mode
watch -n1 'ip -s link show eth0'

# Per-second from sar (needs sysstat)
sar -n DEV 1 5
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Shows 0 on busy host | Wrong interface name | `ip link`; cloud uses `ens*`, not `eth0` |
| Graph flat but users report slowness | Problem not bandwidth (latency, CPU) | [[ss]], `ping`, app metrics |
| Can't identify culprit | Interface-level only | `iftop`, `nethogs`, `tcpdump` |
| Spikes not visible | Avg window too long | F2 → shorten avg time in nload |
| Permission errors | Rare; needs cap for some modes | Run as root or use `ip -s link` |

## Gotchas

> [!WARNING]
> **Interface names changed** — `eth0` → `enp0s3` / `ens5` with predictable naming. Always `ip link` first.

> [!WARNING]
> **VLAN/bond slaves** — traffic may show on bond0, not physical NIC. Watch the interface actually carrying traffic.

> [!WARNING]
> **Loopback (`lo`) spikes** — local proxy/db on same host looks like "network" on lo; filter to external iface.

> [!WARNING]
> **Not installed by default** on minimal images — `apt install nload`; don't assume presence in runbooks.

## When NOT to use

- **Per-process attribution** → `nethogs`, eBPF tools.
- **Historical analysis** → `sar`, Grafana, flow logs.
- **Production dashboards** → proper monitoring stack.
- **Headless automation** → parse `/proc/net/dev` or `ip -s link`.

## Related

[[Linux network commands]] [[ip]] [[ss]] [[top]] [[netstat]]
