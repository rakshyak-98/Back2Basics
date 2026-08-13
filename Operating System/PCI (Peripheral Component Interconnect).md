[[Operating System]] [[bus]] [[system bus]] [[Boot/UEFI]] [[Persistent Block Storage]]

# PCI (Peripheral Component Interconnect)

> PCI and its successor PCIe are standard local buses for attaching NICs, GPUs, NVMe controllers, and chipset devices — enumerated at boot with vendor/device IDs and BAR memory regions.

**PCIe** (Express) serial lanes replace parallel PCI but retain the **PCI** configuration model. Firmware ([[Boot/UEFI]]) and the kernel walk the **PCIe tree**, assign resources, and bind **drivers**.

```bash
lspci -nn
lspci -vv -s 01:00.0
```

## OS view

- **MMIO** — driver maps BAR into kernel space.
- **DMA** — devices transfer to RAM ([[Buffer cache]] pages).
- **MSI/MSI-X** — interrupts for completion events.

Hot-plug (some servers), ACS, and IOMMU (VT-d) affect virtualization passthrough.

Parent topic: [[bus]], [[system bus]].

## Sources

- PCI-SIG PCIe base specification
- Linux kernel documentation: [PCI Subsystem](https://docs.kernel.org/PCI/index.html)
- Wikipedia: [PCI Express](https://en.wikipedia.org/wiki/PCI_Express)
