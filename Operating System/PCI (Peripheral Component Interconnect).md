[[Operating System]] [[bus]] [[system bus]] [[Boot/UEFI]] [[Persistent Block Storage]] [[Buffer cache]]

# PCI (Peripheral Component Interconnect)

> PCI and its successor PCIe are the standard local buses for NICs, GPUs, NVMe, and chipset devices — enumerated at boot with vendor/device IDs and BAR memory regions.

```txt
        PCI (Peripheral Co ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Systems / kernel interviews: enumerate devices (`lspci`), explain BARs/MMIO, …

## Sources
- PCI-SIG PCIe base specification — deep-dive
- [Linux kernel docs — PCI Subsystem](https://docs.kernel.org/PCI/index.html) — deep-dive
- [Wikipedia — PCI Express](https://en.wikipedia.org/wiki/PCI_Express) — overview

## Key Concepts
- **PCIe vs PCI:** serial lanes replace parallel PCI; configuration space model remains.
- **Enumeration:** firmware ([[Boot/UEFI]]) and kernel walk the PCIe tree, assign resources, bin…
- **BARs / MMIO:** device registers mapped into address space.
- **DMA + MSI/MSI-X:** device↔RAM transfers and completion interrupts.

## Technical Details
```bash
lspci -nn
lspci -vv -s 01:00.0
```

- **MMIO:** — driver maps BAR into kernel space.
- **DMA:** — devices transfer to RAM ([[Buffer cache]] pages).
- **MSI/MSI-X:** — interrupts for completion events.

- Hot-plug (some servers), ACS, and IOMMU (VT-d) affect virtualization passthro…

- Parent topics: [[bus]], [[system bus]].

## Mistakes to Avoid
- **Mistake:** Ignoring IOMMU groups when planning GPU/NIC passthrough
- **Mistake:** Assuming `lspci` absence means “no driver”
- **Mistake:** Tuning only software queues while the PCIe link trains at a degr…

## Pros/Cons or Trade-offs
- **Pro:** Ubiquitous, discoverable, high bandwidth with modern lane counts.
- **Con:** Topology/NUMA and ACS quirks complicate multi-host and SR-IOV setups.
- **Trade-off:** more lanes / generations vs power and platform cost ([[TDP]] of the whole system).

## Comparison
- vs [[system bus]]: system bus is the broader interconnect idea
- vs on-chip buses in MCUs: ECUs may use simpler interconnects; servers center on PCIe.


### Use cases
- NVMe SSDs, 100GbE NICs, and GPUs all appear as PCIe endpoints
