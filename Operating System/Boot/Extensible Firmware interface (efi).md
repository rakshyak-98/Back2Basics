[[Operating System]] [[Boot/UEFI]] [[Boot/UEFI (2)]] [[PCI (Peripheral Component Interconnect)]] [[OS program]]

# Extensible Firmware interface (efi)

> EFI is Intel’s 1990s firmware spec that evolved into UEFI — modular drivers, GPT disks, and PE/COFF boot apps instead of BIOS interrupt chains.





## Interview Relevance
Boot interviews: Boot vs Runtime Services, ExitBootServices, and that “EFI partition” in the field usually means modern UEFI + ESP.

## Sources
- UEFI Forum — [Specifications](https://uefi.org/specifications) — deep-dive
- [Wikipedia — Unified Extensible Firmware Interface](https://en.wikipedia.org/wiki/Unified_Extensible_Firmware_Interface) — overview
- Intel Platform Innovation Framework for EFI (archive) — overview

## Key Concepts
- **EFI → UEFI:** same core idea; UEFI is the industry-maintained successor.
- **Boot Services:** memory map, protocols, load images — torn down at `ExitBootServices`.
- **Runtime Services:** small subset survives into the OS (variables, clock, reset).
- **Field naming:** ESP, `.efi` PE32+ apps, OVMF for QEMU/KVM.

## Technical Details
| Phase | Role |
|-------|------|
| Boot Services | Memory map, protocol handles, load images — torn down when OS calls `ExitBootServices` |
| Runtime Services | Small subset survives into OS (variables, clock, reset) |

Boot loaders query GOP, block I/O, and simple file system protocols to read the kernel. Legacy BIOS used 16-bit real-mode interrupts; EFI/UEFI runs flat protected/long mode with hardware tables — closer to how an [[OS program]] expects memory.

Canonical modern path: [[Boot/UEFI]]; field ops: [[Boot/UEFI (2)]].

## Real-World Applications
OVMF guests, Secure Boot chains, and any talk of “EFI system partition” on GPT disks.

## Pros/Cons or Trade-offs
- **Pro:** Modular drivers and large-disk GPT boot model.
- **Con:** More complex than classic BIOS; variables/NVRAM footguns.
- **Trade-off:** UEFI-native simplicity vs CSM for legacy images.

## Comparison
- vs [[Boot/UEFI]]: UEFI is the unified modern spec; EFI is the historical Intel-origin name.
- vs BIOS: interrupt chains and MBR stage1 vs PE/COFF loaders on ESP.

## Mistakes to Avoid
- Treating “EFI” and “BIOS” as interchangeable in recovery docs.
- Forgetting ExitBootServices ends Boot Services forever for that boot.
- Confusing ESP contents with the OS root filesystem.
