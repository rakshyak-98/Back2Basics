[[10 NIC]] [[ss]] [[Linux]] [[MTU (Maximum Transmission Unit)]] [[TCP]] [[UDP]]

# ethtool

> ethtool talks to the NIC driver — link speed, offloads, rings, and drop counters live here, not in the routing table.

## Interview Relevance

Interviewers expect you to use `ethtool` when `ip link` is UP but throughput or errors look wrong — prove you can read Speed/Duplex, driver stats, and offloads before blaming the application.

## Sources

- [ethtool(8) — Linux man page](https://man7.org/linux/man-pages/man8/ethtool.8.html) — deep-dive
- [Linux — Scaling in the Linux Networking Stack](https://docs.kernel.org/networking/scaling.html) — overview
- [Wikipedia — ethtool](https://en.wikipedia.org/wiki/Ethtool) — overview

## Core Definition

`ethtool` is the userspace tool that queries and configures NIC driver settings (PHY link, rings, coalesce, checksum/TSO/GSO offloads, and hardware counters).

## Key Concepts

- **Driver path:** ethtool → driver → NIC firmware/PHY → not the routing stack.
- **Link negotiation:** Speed, Duplex, Autoneg → cable/SFP mismatches show up here.
- **Rings / coalesce:** buffer and interrupt batching → PPS vs latency trade-off.
- **Offloads:** TSO/GSO/checksum → CPU savings; buggy offloads cause “checksum errors.”
- **`-S` stats:** `rx_missed_errors`, `rx_dropped` → NIC overflow vs kernel backlog ([[ss]]).

## Technical Details

```txt
ethtool ──► driver ──► NIC firmware / PHY
              │
              └── ring buffers, checksum offload, TSO, LRO
```

```bash
ethtool eth0
ethtool -S eth0 | head -40          # driver stats (drops, errors)
ethtool -i eth0                     # driver/firmware version
```

```bash
sudo ethtool -s eth0 speed 1000 duplex full autoneg off
# Persist via NM or udev — ethtool -s is lost on reboot
```

```bash
ethtool -g eth0                     # ring sizes
ethtool -G eth0 rx 4096 tx 4096
ethtool -c eth0                     # interrupt coalesce
```

```bash
ethtool -k eth0
sudo ethtool -K eth0 tso off gso off   # debug checksum bugs
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Link up, slow throughput | `Speed`, `Duplex`; `LnkSta` via lspci | Fix cable/SFP; match autoneg; replace optics |
| Packet loss at high PPS | `ethtool -S` drops | Increase rings; coalesce tuning; faster CPU |
| TCP checksum errors | `rx_errors`; `-k` offloads | Disable bad offload; update driver |
| Changes vanish on reboot | No persist rule | NM dispatcher script or systemd unit |

## Real-World Applications

Debugging 1G fallback on “10G” servers, virtio offload bugs in VMs, and RX drops under high PPS.

**Example:** Throughput plateaus at ~110 MB/s — `ethtool eth0` shows `Speed: 1000Mb/s` after a bad SFP; replacing optics restores 10G.

## Pros/Cons or Trade-offs

- **Pro:** Direct visibility into L1/L2 and driver counters that `ip` does not show.
- **Con:** Many settings are ephemeral unless persisted via NetworkManager/udev.
- **Con:** Disabling TSO/GSO for debugging burns CPU if left off in production.

## Comparison

- vs `ip link` / routing: `ip` shows admin state and addresses; ethtool shows PHY/driver performance knobs.
- vs [[10 NIC]]: NIC is the hardware; ethtool is how you inspect and tune it.
- vs application/`ss` tuning: confirm L1/L2 first, then move up the stack.

## Mistakes to Avoid

- Tuning rings before confirming application and kernel aren’t the bottleneck (`ss -ti`, softirq).
- Leaving autoneg off at the wrong speed — silent errors or half-duplex disasters.
- Expecting identical `-S` counters on virtio/vmxnet — VM NICs differ.
- Treating ethtool as a routing tool — it does not fix default-gateway mistakes.
