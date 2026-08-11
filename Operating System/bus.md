[[Operating System]] [[system bus]] [[PCI (Peripheral Component Interconnect)]] [[OS program]]

# Bus

> A bus is the shared highway chips use to move addresses and data — CPU, memory, and devices take turns on the wires/lanes.

---

## Mental model

**Say it in one breath:** Older designs share parallel lines; modern PCIe/USB are serial links — still “buses” in architecture talk.

```txt
CPU  ↔  chipset/root  ↔  memory controller
                └─ I/O buses (PCIe, SATA, USB, …)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **System bus** | CPU–memory–chipset path | “Feeds the core; starvation = stalls.” |
| **Front-side bus** | Legacy CPU–northbridge | “Replaced by on-die controllers.” |
| **Memory bus** | DRAM channel | “Width × rate = bandwidth.” |
| **I/O bus** | Peripherals | “PCIe today; PCI yesterday.” |
| **Arbitration** | Who owns the bus | “Avoid collisions / fair access.” |
| **Bandwidth vs latency** | Throughput vs delay | “Wide bus can still have high latency.” |

### How the story goes

1. **Request** — master wants read/write.
2. **Arbitrate** — grant ownership / schedule packets.
3. **Transfer** — move data (burst, lanes, flits).
4. **Complete** — ack / interrupt / DMA done.

---

## Standard config / commands

```bash
# See downstream buses from Linux
lspci
lsusb
cat /proc/bus/input/devices
# Perf: memory vs QPI/UPI is vendor-specific; use pcm / perf uncore events
```

| Knob | Why it matters |
|------|----------------|
| Clock / link speed | Raw throughput |
| Width / lanes | Parallelism |
| DMA vs PIO | CPU overhead |
| Topology (NUMA) | Cross-node bus cost |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| CPU wait on memory | Bandwidth counters | Better locality; fewer copies |
| Device too slow | Link width/speed | Slot/lanes; cables; Gen mismatch |
| Intermittent errors | Signal integrity | Reseat; replace riser |
| High latency I/O | Shared saturated link | Move device; QoS; fewer peers |
| DMA faults | IOMMU groups | Mapping / VFIO setup |
| Confusion “which bus” | Diagram the path | Name PCIe vs USB vs i2c |

---

## Gotchas

> [!WARNING]
> **“Faster bus” marketing** — peak GB/s ≠ your app’s achieved bandwidth.

> [!WARNING]
> **Shared ≠ free** — USB hubs and PCIe switches add contention.

> [!WARNING]
> **Endian / width** — multi-byte on weird buses needs protocols ([[endian]]).

> [!WARNING]
> **MCU “bus”** — APB/AHB inside chips; different from PCIe slots.

---

## When NOT to use

- **application IPC** — use sockets/queues; don’t romanticize hardware buses.
- **Network fabric design** — Ethernet/InfiniBand notes, not this.
- **Choosing a DB** — storage protocol ≠ motherboard bus lecture.

---

## Related

[[system bus]] [[PCI (Peripheral Component Interconnect)]] [[endian]] [[disk IOPS]] [[Electronic Control Unit (ECU)]]
