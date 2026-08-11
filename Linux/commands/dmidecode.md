[[commands]] [[lspci]]

# dmidecode

> dmidecode prints SMBIOS/DMI tables from firmware — vendor, model, serial, slots, memory layout as the BIOS recorded them.

---

## Mental model

**Say it in one breath:** firmware strings about the chassis — great for inventory; not a live PCIe bandwidth meter.

```txt
UEFI/BIOS SMBIOS tables ──► dmidecode ──► system / baseboard / memory / slots
lspci ──► what is actually enumerated and link speed/width
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **SMBIOS / DMI** | Firmware inventory tables | “What the vendor burned in, not what Linux measured.” |
| **`-t system`** | Product / serial / UUID | “Asset tag and serial for CMDB.” |
| **`-s`** | One string keyword | “Script-friendly single values.” |
| **`-t slot`** | Physical slot labels | “Map empty vs occupied connectors.” |
| **`LnkCap` vs `LnkSta`** | Max vs negotiated PCIe | “From `lspci -vv` — catch lane starvation.” |

---

## Standard config / commands

```bash
sudo dmidecode -t system
sudo dmidecode -t bios
sudo dmidecode -t baseboard
sudo dmidecode -t chassis
sudo dmidecode -t processor
sudo dmidecode -t memory
sudo dmidecode -t slot

sudo dmidecode -s system-manufacturer
sudo dmidecode -s system-product-name
sudo dmidecode -s system-serial-number
```

Needs root (or CAP) — tables are under `/sys/firmware/dmi`.

---

## PCIe slot vs reality

```bash
sudo dmidecode -t slot
lspci -tv
lspci -vv | grep -i "PCI bridge"
# NVIDIA example
lspci -d 10de: -vv
```

| Outcome | Meaning |
|---------|---------|
| `LnkSta` ≈ `LnkCap` | Card running at capability |
| Width lower (x16→x8) | Lane-starved slot/riser |
| Speed lower (8GT→2.5GT) | Bad link / Gen fallback / power state |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Empty / “Not Specified” | VM or lazy BIOS | Expect blanks in clouds; use instance metadata |
| Permission denied | Not root | `sudo` |
| Serial looks fake | OEM placeholder | Cross-check baseboard serial / cloud ID |
| GPU slow, slots “x16” | Negotiated link | Compare `LnkCap`/`LnkSta` via `lspci` |
| Typo commands | `dmideocde` | It’s `dmidecode` |

---

## Gotchas

> [!WARNING]
> **Firmware can lie or omit fields** — especially VMs and cheap boards.

> [!WARNING]
> **Slot label ≠ electrical width** — always confirm with `lspci -vv` when performance matters.

> [!WARNING]
> **Serials are sensitive** — treat inventory exports as confidential.

---

## When NOT to use

- **Live CPU/RAM usage** — `top` / `free` / metrics agents.
- **Disk topology** — `lsblk` / `nvme list`.
- **Cloud instance type** — provider metadata API.

---

## Related

[[lspci]] [[commands]] [[Linux process commands]]
