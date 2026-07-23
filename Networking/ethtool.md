[[10 NIC]] [[ss]] [[Linux]] [[MTU (Maximum Transmission Unit)]]

# ethtool

> NIC driver ioctl tool — inspect link state, speed/duplex, ring sizes, offload features, and driver stats at the hardware edge.

---

## Mental model

**ethtool** talks to the **NIC driver**, not just the kernel routing stack:

```txt
ethtool ──► driver ──► NIC firmware / PHY
              │
              └── ring buffers, checksum offload, TSO, LRO
```

Use when `ip link` shows UP but performance is wrong — cable/negotiation/offload issues live here, not in [[route]] tables.

---

## Standard config / commands

### Link and speed

```bash
ethtool eth0
ethtool -S eth0 | head -40          # driver stats (drops, errors)
ethtool -i eth0                     # driver/firmware version
```

### Force speed/duplex (lab / broken autoneg)

```bash
sudo ethtool -s eth0 speed 1000 duplex full autoneg off
# Persist via NM or udev — ethtool -s is lost on reboot
```

### Ring buffer / coalesce (latency vs throughput)

```bash
ethtool -g eth0                     # ring sizes
ethtool -G eth0 rx 4096 tx 4096
ethtool -c eth0                     # interrupt coalesce
```

### Offloads (cloud/virt often partial)

```bash
ethtool -k eth0
sudo ethtool -K eth0 tso off gso off   # debug checksum bugs
```

**Why `-S` stats:** `rx_missed_errors`, `rx_dropped` distinguish **NIC overflow** vs kernel backlog ([[ss]]).

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Link up, slow throughput | `Speed`, `Duplex`; `LnkSta` via lspci | Fix cable/SFP; match autoneg; replace optics |
| Packet loss at high PPS | `ethtool -S` drops | Increase rings; coalesce tuning; faster CPU |
| TCP checksum errors | `rx_errors`; `-k` offloads | Disable bad offload; update driver |
| Changes vanish on reboot | No persist rule | NM dispatcher script or systemd unit |

---

## Gotchas

> [!WARNING]
> **Virtio/vmxnet stats differ** — not all `-S` counters exist in VMs.

> [!WARNING]
> **Disabling TSO/GSO hurts CPU** — debug knob, not production default.

> [!WARNING]
> **Autoneg off wrong speed** — silent errors or half-duplex disaster.

---

## When NOT to use

Don't tune ring buffers before confirming **application and kernel** aren't the bottleneck (`ss -ti`, CPU softirq). ethtool is layer 1–2, not routing.

---

## Related

[[10 NIC]] [[ss]] [[MTU (Maximum Transmission Unit)]] [[TCP]] [[UDP]]
