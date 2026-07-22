[[PCI (Peripheral Component Interconnect)]] [[bus]] [[base clock speed]] [[RAM and Swap memory]]

# System bus

> High-speed interconnect between CPU, memory, and I/O — defines bandwidth and latency ceilings for the whole machine.

---

## Mental model

The **system bus** is the plumbing that moves addresses, data, and control between major components:

```txt
        ┌─────────┐
        │   CPU   │
        └───┬─────┘
            │  system bus / fabric
    ┌───────┼───────┬──────────┐
    ▼       ▼       ▼          ▼
 Memory  PCIe   Chipset    (other sockets via UPI/IF)
           │
        NIC, NVMe, GPU
```

Historical **shared parallel bus** (FSB) is largely replaced by **point-to-point serial links**:
- **Intel UPI** / **AMD Infinity Fabric** — socket-to-socket
- **DMI** — CPU to PCH
- **PCIe** — CPU/root complex to peripherals

**Effective bandwidth** is always less than line rate — protocol overhead, contention, NUMA remote memory, and small I/O ops matter more than peak Gbps on the spec sheet.

---

## Standard config / commands

### See topology and NUMA

```bash
lscpu | grep -E 'NUMA|Socket|MHz'
numactl --hardware
lstopo-no-graphics    # hwloc — bus tree visualization
```

### PCIe link speed (NIC/NVMe bottleneck)

```bash
lspci -vv | grep -E 'LnkCap|LnkSta'   # Gen x width
sudo lspci -s 0000:01:00.0 -vv | grep LnkSta
```

### Memory bandwidth sanity check

```bash
# Package-dependent — install mbw or use STREAM benchmark
mbw -n 10 256
```

**Why NUMA matters:** on multi-socket boxes, memory attached to another socket crosses the **inter-socket bus** — 2–3× latency vs local.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| NVMe/NIC below rated speed | `LnkSta` degraded (Gen1 x1) | Reseat card; BIOS ASPM settings; cable |
| High latency on multi-socket DB | `numastat`; allocation on wrong node | `numactl --interleave` or bind process to node with memory |
| PCIe errors in dmesg | `dmesg \| grep -i aer` | Faulty hardware; firmware; reduce overclock |
| Memory bandwidth saturated | `perf stat -e cycles,mem_load_uops` | Fewer copies; NUMA-local buffers; faster RAM channels |

---

## Gotchas

> [!WARNING]
> **Marketing "bus speed" ≠ application throughput** — small random I/O hits latency, not GB/s headline numbers.

> [!WARNING]
> **PCIe lanes are shared** — chipset slots and M.2 may mux — check motherboard block diagram.

> [!WARNING]
> **C-state / ASPM** can downshift link width for power — adds wake latency for bursty workloads.

---

## When NOT to use

Don't architect around "buy a faster bus" without profiling — often the fix is **fewer crossings** (copy elimination, batching, local NUMA node) not faster hardware.

---

## Related

[[PCI (Peripheral Component Interconnect)]] [[bus]] [[disk IOPS]] [[base clock speed]] [[RAM and Swap memory]]
