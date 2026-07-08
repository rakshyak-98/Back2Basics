reads the system DMI (Desktop Management Interface) / SMBIOS (System Management BIOS) table and displays hardware information stored by the BIOS/UEFI

```bash
dmidecode -t slot;
dmidcode -t system | grep -i "Product Name";
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