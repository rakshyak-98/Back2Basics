[[ethtool]] [[MTU (Maximum Transmission Unit)]] [[TCP]] [[Egress traffic]]

# NIC (10 NIC)

> Network Interface Card — hardware (or virtio) port that moves L2 frames between host memory and the wire; 10G = ~10 Gbps line rate baseline for server workloads.

---

## Mental model

A **NIC** terminates Ethernet (or IB) and exposes a **kernel netdev** (`eth0`, `ens5`):

```txt
App ──socket──► kernel TCP/IP ──► driver ring ──► NIC ──► switch
                                      ▲
                                      └── [[ethtool]] stats, offloads
```

Speed tiers (common server):
| Speed | Approx throughput (theoretical) |
|-------|----------------------------------|
| 1 GbE | ~125 MB/s |
| 10 GbE | ~1.25 GB/s |
| 25/100 GbE | datacenter / AI fabric |

**10G** is the usual step up when 1G saturates (storage, video ingest, K8s node east-west). Bottleneck moves to **PCIe lanes**, **CPU softirq**, and **packet rate** (PPS), not headline Gbps alone.

---

## Standard config / commands

### Identify NIC and link

```bash
ip link show
ethtool eth0 | grep -E 'Speed|Duplex|Link'
lspci | grep -i ethernet
```

### Driver and firmware

```bash
ethtool -i eth0
dmesg | grep -i eth0
```

### IRQ / RPS scaling (high PPS)

```bash
cat /proc/interrupts | grep eth0
# Consider RPS/XPS, irqbalance, or tuned driver RSS queues
```

### Cloud ENI (AWS example)

```bash
# Instance type dictates max ENI bandwidth — check AWS docs
ip -s link show ens5
```

**Why multiple queues:** single-queue NIC + many cores → one CPU handles all RX interrupts.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Throughput plateaus below 10G | `ethtool` speed; PCIe width | Fix autoneg; x8 vs x16 slot; upgrade instance |
| High CPU on RX | `softnet_stat`; drops in `ethtool -S` | RSS queues; XDP; kernel bypass (DPDK) last resort |
| Latency spikes | coalesce settings | Tune `ethtool -c`; disable LRO on forwarders |
| VM shows 10G but slow | Credit-based limit | Right-size instance; check [[Egress traffic]] caps |

---

## Gotchas

> [!WARNING]
> **Line rate ≠ application throughput** — TCP window, RTT, and loss dominate WAN.

> [!WARNING]
> **Jumbo frames (9000 MTU)** — end-to-end path must support; mismatch → black hole or fragmentation.

> [!WARNING]
> **Bonding/VLAN** — stats on slave vs master; troubleshoot correct iface.

---

## When NOT to use

Don't deploy 10G NICs without **switch ports and storage** to match — 10G east-west with 1G uplink shifts bottleneck to [[Egress traffic]] only.

---

## Related

[[ethtool]] [[MTU (Maximum Transmission Unit)]] [[TCP]] [[UDP]] [[Egress and Ingress]]
