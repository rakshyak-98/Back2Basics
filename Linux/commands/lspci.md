[[dmidecode]] [[Linux configuration]] [[nvidia-smi]] [[ip]] [[ss]]

# lspci

> lspci lists PCI devices the kernel sees — vendor/device IDs, topology, and which kernel driver is bound.

## Interview Relevance
Hardware triage: `lspci -nnk` for IDs + driver, distinguishing “device present” from “driver working,” and when to use lsusb/dmidecode instead.

## Sources
- [lspci(8)](https://man7.org/linux/man-pages/man8/lspci.8.html) — deep-dive
- [pci.ids](https://pci-ids.ucw.cz/) — overview

## Core Definition
The kernel discovers PCI devices at boot under `/sys/bus/pci/devices/`. `lspci` reads that tree and resolves names via **pci.ids**. It shows presence and binding hints — not firmware health or application readiness.

## Key Concepts
- **`-k`:** Kernel driver in use / modules.
- **`-v`/`-vv`:** IRQs, BARs, link speed, capabilities.
- **`-t`:** Bus/bridge tree.
- **vendor:device IDs:** Match quirks, firmware, DKMS packages.
- **Not USB:** Peripherals on USB need `lsusb`.

## Technical Details

```bash
lspci
lspci -tv
lspci -k
lspci -vv -s 0000:03:00.0
lspci | grep -iE 'vga|3d|nvidia|amd'
lspci | grep -iE 'nvme|sata|raid'
lspci -n
sudo update-pciids

lspci -s 03:00.0 -k
ls -l /sys/bus/pci/devices/0000:03:00.0/driver
dmesg | grep -i '03:00.0'
```

| Symptom | Check | Fix |
|---------|-------|-----|
| GPU missing from nvidia-smi | `lspci \| grep -i nvidia` | Reseat; driver; IOMMU; `dmesg` |
| NIC missing | `lspci -k` | BIOS; passthrough; `modprobe` |
| Unknown device | `lspci -n` | Update pci.ids; newer kernel |
| Device, no driver | `lspci -k` empty driver | Install modules; modprobe |
| Wrong link speed | `lspci -vv` LnkSta | Slot/cable/BIOS Gen |

## Real-World Applications
Confirming a GPU is visible before installing drivers, finding which module owns a NIC, and verifying PCI passthrough into a VM.

## Pros/Cons or Trade-offs
- **Pro:** Fast inventory of PCI topology and drivers.
- **Con:** Lists dead/broken devices that still enumerate.
- **Trade-off:** Numeric `-n` when pci.ids is stale vs human names when updated.

## Comparison
vs [[dmidecode]]: DMI/SMB BIOS inventory (CPU/RAM/serial). vs `lsusb`: USB tree. vs [[ip]]/[[ss]]: network config/sockets after the NIC is found. vs [[nvidia-smi]]: driver/runtime status after GPU is bound.

## Mistakes to Avoid
- Assuming “in lspci” means “working.”
- Using lspci inside unprivileged containers and trusting the view.
- Confusing USB gadgets with PCI devices.
