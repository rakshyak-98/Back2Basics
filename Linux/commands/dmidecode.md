reads the system DMI (Desktop Management Interface) / SMBIOS (System Management BIOS) table and displays hardware information stored by the BIOS/UEFI

```bash
dmidecode -t slot;
dmidcode -t system | grep -i "Product Name";
```

```bash
dmidecode -s system-manufacturer
dmideocde -s system-product-name
```


> [!NOTE]
> It reads firmware-provided information. Accuracy depends on what the BIOS/UEFI exposes.

```bash

dmidecode -t system
# manufacturer, product name, serial number, UUID, sku

dmidecode -t bios
# BIOS vendor, BIOS version, Release date, ROM size

dmidecode -t processor
# Socket, CPU Version, Core unit, Thread count, Max speed

dmideocde -t memory
# RAM size, Manufacturer, Part number, Serial number, DIMM slot, Form factor (DIMM/SODIMM)

dmidecode -t baseboard
# Manufacturer, Model, Version, Serial number

dmidecode -t chassis
# Desktop/laptop/server, Manufacturer, Asset tag, serial number

```

```bash
dmidecode -t slot
```
This list every physical slot on the motherboard, including empty ones, with:
- slow designation
- type `x16 PCI Express Gen4`, `x8 PCI Express Gen3`
- current usage

**Current occupied slots and what's installed in them**

```bash
ispci -vv | grep -i "PCI bridge"
ispci -tv
```
`ispic -tv` gives a tree view showing bus/slot hierarchy so you can map devices (GPU, NICs, NVMe, etc.) to physical slots.

**Confirm the installed T4 and its slot/link details**

```bash
ispci -d 10de: -vv
```
This filters to NVIDIA devices (vendor ID `10de`) and shows `LnkCap` (link capability — max supported width/speed) vs `LnkSta` (link status — actual negotiated width/speed) for the T4. Compare the two to catch lane-starving (e.g., a card that supports x16 but is only running at x8).

**Three possible outcomes:**

1. **`LnkSta` matches `LnkCap`** (e.g., both x16 @ 8GT/s) — the T4 is running at full capability. The slot it occupies is not a bandwidth bottleneck.
2. **`LnkSta` width is narrower than `LnkCap`** (e.g., `LnkCap: Width x16` but `LnkSta: Width x8`) — the card is lane-starved. This happens when the slot is electrically wired for fewer lanes than the physical connector suggests, or the riser/backplane split the lanes (the scenario the document flags under "Riser/backplane PCIe lane allocation").
3. **`LnkSta` speed is lower than `LnkCap`** (e.g., `LnkCap: 8GT/s` but `LnkSta: 2.5GT/s`) — a Gen3-capable card is being forced to Gen1 speed, usually indicating a misconfigured riser, a bad connection, or power-state throttling.