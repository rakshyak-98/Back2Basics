[[Data structure/Data structure]] [[dsa intuition]] [[DSA algorithms]]

# ACPI

> ACPI (Advanced Configuration and Power Interface) is the OS–firmware contract for discovering hardware, configuring devices, and managing system power states — sleep, hibernate, and shutdown — without legacy BIOS-only h…

```txt
        ACPI ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Explain how the operating system hands off to firmware for sleep/wake, what A…

## Sources
- [UEFI Forum — ACPI specification](https://uefi.org/specifications) — deep-dive
- [Microsoft — ACPI overview](https://learn.microsoft.com/en-us/windows-hardware/drivers/acpi/) — overview
- [Linux kernel — ACPI documentation](https://www.kernel.org/doc/html/latest/firmware-guide/acpi/index.html) — deep-dive

## Key Concepts
- **Tables in memory:** DSDT/SSDT describe devices and power resources; firmware exposes them at boot.
- **AML bytecode:** Firmware encodes policy; OS interpreter runs methods on state changes.
- **Power states:** Global (G-states), sleep (S-states), device (D-states), processor (C-states).
- **OS ↔ firmware boundary:** OS calls ACPI methods; firmware owns low-level PMIC/embedded controller work.

## Technical Details
```txt
  Application / kernel drivers
           │
     ACPI subsystem (OS)
           │
   ACPI tables + AML interpreter
           │
   Firmware (UEFI/BIOS) + hardware
```

| State family | Meaning | Example |
|--------------|---------|---------|
| **G0** | Working | Normal run |
| **G1** | Sleeping | S1–S4 sleep |
| **G2** | Soft off | Shutdown, wake on LAN possible |
| **G3** | Mechanical off | Power removed |
| **S3** | Suspend to RAM | Laptop sleep |
| **S4** | Suspend to disk | Hibernate |

- Common Linux checks:

```bash
ls /sys/firmware/acpi/tables/
cat /sys/power/state
dmesg | grep -i acpi
```

| Symptom | Likely cause | Direction |
|---------|--------------|-----------|
| No sleep | Missing `_PTS` / `_WAK` | Firmware or DSDT bug |
| Wake failures | IRQ/GPIO wake miswired | ACPI _PRW resources |
| Battery wrong | ACPI battery objects | `_BST` / `_BIF` methods |

- ACPI replaced ad-hoc APM interfaces so one driver model works across vendors …

## Mistakes to Avoid
- **Mistake:** Blaming the OS for sleep bugs without reading `dmesg` ACPI errors
- **Mistake:** Patching DSDT without understanding AML side effects
- **Mistake:** Assuming `suspend` works when firmware never implemented S3

## Pros/Cons or Trade-offs
- **Pro:** Uniform OS power model across vendors.
- **Con:** AML is hard to debug; firmware bugs become OS bugs.
- **Trade-off:** ACPI flexibility vs opaque firmware behavior.

## Comparison
- vs legacy APM: ACPI is table-driven and extensible; APM was BIOS-centric and limited.
- vs [[UEFI]] alone: UEFI boots the machine; ACPI governs runtime power and device enumeration.


### Use cases
- Laptop sleep/wake, server power capping, thermal throttling coordination, and…
