[[ethtool]] [[MTU (Maximum Transmission Unit)]] [[TCP]] [[UDP]] [[Egress traffic]] [[Egress and Ingress]]

# NIC (10 NIC)

> Network Interface Card — hardware (or virtio) port that moves L2 frames between host memory and the wire; 10G is the common server step-up from 1G.

```txt
        NIC (10 NIC) ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask about NICs to see if you separate line rate from application…

## Sources
- [Wikipedia — Network interface controller](https://en.wikipedia.org/wiki/Network_interface_controller) — overview
- [ethtool(8) — Linux manual page](https://man7.org/linux/man-pages/man8/ethtool.8.html) — deep-dive
- [Linux — Scaling in the Linux Networking Stack](https://docs.kernel.org/networking/scaling.html) — deep-dive

## Key Concepts
- **NIC / netdev:** terminates Ethernet (or IB) and exposes a kernel interface (`eth0`, `ens5`).
- **Line rate vs goodput:** headline Gbps is theoretical; TCP window, RTT, and loss dominate WAN.
- **PPS bottleneck:** small packets can exhaust CPU/IRQ before you hit Gbps.
- **Multi-queue / RSS:** spreads RX interrupts across cores — single-queue NICs pin one CPU.

Speed tiers (common server):

| Speed | Approx throughput (theoretical) |
|-------|----------------------------------|
| 1 GbE | ~125 MB/s |
| 10 GbE | ~1.25 GB/s |
| 25/100 GbE | datacenter / AI fabric |

- **Note:** **10G** is the usual step up when 1G saturates (storage, video ingest, Kubern…

## Technical Details
```txt
App ──socket──► kernel TCP/IP ──► driver ring ──► NIC ──► switch
                                      ▲
                                      └── [[ethtool]] stats, offloads
```

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

- **Why multiple queues:** single-queue NIC + many cores → one CPU handles all …

| Symptom | Check | Fix |
|---------|-------|-----|
| Throughput plateaus below 10G | `ethtool` speed; PCIe width | Fix autoneg; x8 vs x16 slot; upgrade instance |
| High CPU on RX | `softnet_stat`; drops in `ethtool -S` | RSS queues; XDP; kernel bypass (DPDK) last resort |
| Latency spikes | coalesce settings | Tune `ethtool -c`; disable LRO on forwarders |
| VM shows 10G but slow | Credit-based limit | Right-size instance; check [[Egress traffic]] caps |

## Mistakes to Avoid
- **Mistake:** Equating line rate with application throughput
- **Mistake:** Enabling jumbo frames without end-to-end path support
- **Mistake:** Reading bonding/VLAN stats on the wrong iface (slave vs master)
- **Mistake:** Deploying 10G NICs without matching switch ports and storage

## Pros/Cons or Trade-offs
- **Pro:** Higher line rate removes the NIC as the first bottleneck for local/datacenter transfers.
- **Con:** Needs matching switch ports, cabling, and often more CPU for PPS.
- **Con:** Cloud “10G” may still be credit-limited by instance type.
- **Trade-off:** Jumbo frames (9000 MTU) help bulk transfers only if the entire path agrees.

## Comparison
- vs [[ethtool]]: NIC is the hardware/netdev; ethtool is how you query and tune it.
- vs [[MTU (Maximum Transmission Unit)]]: frame size policy on the path
- vs [[Egress traffic]] caps: a fast NIC does not bypass cloud NAT or internet egress limits.


### Use cases
- Database replicas, video ingest nodes, and Kubernetes workers that saturate 1…

- **Example:** Backup job tops out at ~110 MB/s on a “10G” VM
