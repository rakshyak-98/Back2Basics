[[Operating System]] [[bus]] [[system bus]] [[Persistent Block Storage]]

# PCI (Peripheral Component Interconnect)

> PCI/PCIe is the motherboard bus for add-in cards — today “PCI” almost always means PCI Express lanes to GPUs, NICs, and NVMe.

---

## Mental model

**Say it in one breath:** Devices sit on a tree of PCIe links; generation × lane count sets bandwidth; OS enumerates BARs and IRQs.

```txt
CPU/Root complex
   ├─ x16 slot  (GPU)
   ├─ x4        (NVMe / NIC)
   └─ x1        (Wi-Fi)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **PCIe** | PCI Express | “Serial lanes replace classic parallel PCI.” |
| **Lane (x1…x16)** | Parallel serial links | “GPU wants x16; NVMe often x4.” |
| **Generation** | Encoding speed class | “Gen4 ≈ 2× Gen3 per lane.” |
| **BAR** | Base Address Register | “Where the device’s MMIO lives.” |
| **Root complex** | CPU-side PCIe host | “Enumerates the tree at boot.” |
| **Hotplug** | Add/remove under OS | “Needs slot + OS support.” |

### How the story goes

1. **Enumerate** — firmware/OS walks the PCIe tree.
2. **Assign** — BARs, MSI/MSI-X interrupts.
3. **Bind** — kernel driver claims vendor:device ID.
4. **Train** — link width/speed; may downtrain on bad signal.

---

## Standard config / commands

```bash
lspci -nn
lspci -vv -s 01:00.0 | egrep 'LnkCap|LnkSta|NUMA'
ls /sys/bus/pci/devices
# Rescan (careful)
echo 1 | sudo tee /sys/bus/pci/rescan
```

| Knob | Why it matters |
|------|----------------|
| Slot wiring vs length | x16 slot may be x8 electrically |
| Bifurcation | Split x16 into x8x8 for two devices |
| ACS / IOMMU | VFIO / security isolation |
| Power / ASPM | Latency vs watts |

Generations (approx per-lane one-way): Gen3 ~1 GB/s, Gen4 ~2, Gen5 ~4, Gen6 ~8.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| GPU/NIC “not found” | `lspci`; seat/power | Reseat; PSU cables; rescan |
| Slow NVMe | `LnkSta` width/speed | x4/Gen expected? Check bifurcation/cables |
| Code 10 / driver bind fail | `dmesg`; IOMMU groups | Firmware; correct driver; ACS |
| Random disconnects | AER / `dmesg` | Riser quality; ASPM quirks |
| VM no passthrough | IOMMU off / group | Enable VT-d/AMD-Vi; isolate group |
| Wrong bandwidth math | Forgot encoding overhead | Use real Gen×lanes tables |

---

## Gotchas

> [!WARNING]
> **“PCI slot” in 2026 = PCIe** — classic 33 MHz PCI is museum hardware.

> [!WARNING]
> **Physical x16 ≠ electrical x16** — read the motherboard manual.

> [!WARNING]
> **Backward compatible, not equal speed** — Gen5 card in Gen3 slot runs Gen3.

> [!WARNING]
> **Hotplug ≠ guaranteed** — many desktop slots aren’t.

---

## When NOT to use

- **USB gadgets / simple HATs** — different buses.
- **On-SoC peripherals** — AMBA/AXI inside the chip, not a PCIe slot.
- **Legacy ISA fantasies** — use USB-serial bridges instead.

---

## Related

[[bus]] [[system bus]] [[Persistent Block Storage]] [[disk IOPS]] [[Electronic Control Unit (ECU)]]
