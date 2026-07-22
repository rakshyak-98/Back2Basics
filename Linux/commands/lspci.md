[[Linux system management]] [[dmidecode]] [[Linux configuration]]

# lspci

> One-line: list **PCI/PCIe devices** attached to the CPU — NICs, GPUs, storage controllers, USB bridges. **First step for "does the kernel see my hardware?"**

## Mental model

The kernel discovers PCI devices at boot and exposes them in `/sys/bus/pci/devices/`. `lspci` reads that tree and resolves vendor/device IDs via the **pci.ids** database. It shows what the OS sees — not whether drivers are loaded or firmware is healthy.

```
lspci ──► /sys/bus/pci ──► vendor:device ID ──► human name (pci.ids)
                │
                └── kernel driver bound? (see /sys/.../driver)
```

| Flag | Purpose |
|------|---------|
| `-v` | Verbose — driver, module, capabilities |
| `-vv` | Very verbose — config space details |
| `-k` | Show kernel driver handling each device |
| `-t` | Tree view — buses/bridges hierarchy |
| `-s <slot>` | Single device (`0000:03:00.0`) |
| `-n` | Numeric IDs only (no pci.ids lookup) |

## Standard config / commands

```bash
# Inventory
lspci

# Tree — understand topology (GPU behind bridge?)
lspci -tv

# Driver binding — "is my NIC using the right module?"
lspci -k

# Deep debug (firmware, link speed, MSI)
lspci -vv -s 0000:03:00.0

# Find GPU
lspci | grep -iE 'vga|3d|nvidia|amd'

# Find NVMe / storage
lspci | grep -iE 'nvme|sata|raid'

# Numeric IDs when pci.ids stale
lspci -n

# Update pci.ids (Debian)
sudo update-pciids
```

**Pair with driver status:**

```bash
# Device at slot
lspci -s 03:00.0 -k
# Kernel driver in use: nvidia
# Kernel modules: nvidia

ls -l /sys/bus/pci/devices/0000:03:00.0/driver
dmesg | grep -i '03:00.0'
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| GPU not in `nvidia-smi` | `lspci \| grep -i nvidia` | Reseat; IOMMU/ACS; driver install; `dmesg` |
| NIC missing | `lspci -k` | Enable in BIOS; passthrough conflict; driver module |
| "Unknown device" | `lspci -n` | Update pci.ids; new hardware needs newer kernel |
| Device shown, no driver | `lspci -k` shows no driver | `modprobe`; install `linux-modules-extra` |
| Wrong link speed | `lspci -vv` LnkSta | Reseat cable; BIOS Gen setting; bad slot |
| VM missing device | Hypervisor PCI attach | virtio/passthrough config; not visible = not passed |

## Gotchas

> [!WARNING]
> **lspci shows hardware presence, not function** — device can list while driver fails. Always check `dmesg` and `/sys/.../driver`.

> [!WARNING]
> **Containers** — lspci in Docker usually shows host PCI unless `--device` / privileged. Result may confuse.

> [!WARNING]
> **USB devices are not PCI** — USB sticks/webcams → `lsusb`, not lspci (unless USB controller itself).

> [!WARNING]
> **Slot numbering** — `0000:03:00.0` domain:bus:device.function — use full name with `-s` on multi-socket systems.

## When NOT to use

- **USB peripherals** → `lsusb`.
- **CPU/RAM inventory** → [[dmidecode]].
- **Block device health** → `smartctl`, `nvme cli`.
- **Network config** → [[ip]], [[ss]] — lspci only finds the card.

## Related

[[dmidecode]] [[Linux system management]] [[Linux configuration]] [[eBPF]]
