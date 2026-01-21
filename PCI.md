Peripheral Component Interconnect

**PCI** in computers most commonly stands for **Peripheral Component Interconnect**.  
It is a **standard bus** (communication pathway) that allows different hardware components (like graphics cards, network cards, sound cards, storage controllers, wifi cards, etc.) to connect to the motherboard and communicate with the CPU and memory.

### Quick Overview of PCI Evolution (what most people mean today)

| Term                  | Full Name                                      | Introduced | Max Bandwidth (per lane) | Common Use Today | Status in 2026 |
|-----------------------|------------------------------------------------|------------|---------------------------|------------------|----------------|
| **PCI**               | Peripheral Component Interconnect              | 1992       | ~133 MB/s (32-bit @ 33 MHz) | Legacy systems   | **Obsolete**   |
| **PCI-X**             | PCI eXtended                                   | 1999       | ~1 GB/s (64-bit @ 133 MHz) | Old servers      | **Rare**       |
| **PCI Express** (PCIe) | PCI Express (most people just say "PCIe")      | 2003       | Varies by generation      | **Modern standard** | **Dominant**   |

**In 99% of modern conversations (2026), when someone says "PCI" or "PCI slot", they actually mean **PCI Express (PCIe)**.**

### PCIe Generations (current as of 2026)

| Generation | Year Released | Bandwidth per Lane | Typical Use Cases (2025–2026) |
|------------|---------------|---------------------|-------------------------------|
| **PCIe 3.0** | 2010         | ~1 GB/s            | Older GPUs, SSDs, budget motherboards |
| **PCIe 4.0** | 2017         | ~2 GB/s            | Mid-range GPUs, most NVMe SSDs (Gen4) |
| **PCIe 5.0** | 2019         | ~4 GB/s            | High-end GPUs (RTX 40/50 series), fast SSDs |
| **PCIe 6.0** | 2022         | ~8 GB/s            | Enterprise servers, latest flagship GPUs |
| **PCIe 7.0** | 2025 (final spec) | ~16 GB/s       | Emerging in high-end servers & AI hardware |

**x16** slot (most common for GPUs) multiplies the per-lane speed:
- PCIe 5.0 x16 → ~64 GB/s (one direction)
- PCIe 6.0 x16 → ~128 GB/s

### Physical Slots & Compatibility (Key Points)

PCIe slots come in different lengths (and backward compatible):

| Slot Type | Lanes | Typical Cards                          | Backward Compatible? |
|-----------|-------|----------------------------------------|-----------------------|
| **x1**    | 1     | Wi-Fi, sound, network, USB add-on     | Yes                   |
| **x4**    | 4     | NVMe SSD adapters, RAID controllers   | Yes                   |
| **x8**    | 8     | Some high-end network cards, older GPUs | Yes                   |
| **x16**   | 16    | Graphics cards (GPUs), compute cards  | Yes (shorter cards fit) |

**Important rules**:
- A **shorter card** (e.g. x4) **can** go into a **longer slot** (x16) — it just uses fewer lanes
- A **longer card** (x16) **cannot** fit into a shorter slot (x4/x8)
- PCIe is **backward and forward compatible** across generations (PCIe 5.0 GPU works in PCIe 3.0 slot, just slower)

### Common Confusion

| Term People Say | What They Usually Mean (2026) | What It Actually Was |
|-----------------|--------------------------------|----------------------|
| "PCI slot"      | **PCIe x16** slot             | Original PCI (obsolete) |
| "PCI card"      | **PCIe card**                 | Old 1990s PCI card |
| "PCIe Gen 4"    | PCIe 4.0                      | Modern standard |

### Visual Example (Typical Modern Motherboard Slots)

```
[PCIe x16]   ← GPU (graphics card) – usually reinforced
[PCIe x16]   ← Open or secondary GPU slot
[PCIe x8]    ← Sometimes for NVMe or RAID
[PCIe x4]    ← M.2 adapter or network card
[PCIe x1]    ← Wi-Fi / sound card
```

### Summary for 2026

- When someone says **"PCI"** today → they almost always mean **PCI Express (PCIe)**
- **PCIe** is the **current standard** for connecting GPUs, SSDs, network cards, etc.
- The most important thing for performance is:
  - **Generation** (5.0 or 6.0 is best for new hardware)
  - **Lane count** (x16 for GPUs, x4 for fast SSDs)
  - **Compatibility** (always works backward)
