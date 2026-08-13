[[Operating System]] [[Boot/UEFI]] [[Boot/UEFI (2)]] [[PCI (Peripheral Component Interconnect)]]

# Extensible Firmware interface (efi)

> EFI (Extensible Firmware Interface) is Intel’s 1990s firmware specification that evolved into UEFI — same core idea: modular drivers, GPT disks, and PE/COFF boot applications instead of BIOS interrupt chains.

**EFI** introduced a driver model, boot services/runtime services split, and cross-platform abstractions. **UEFI** (Unified EFI) is the industry-maintained successor managed by the UEFI Forum. In conversation “EFI partition” and “UEFI boot” usually mean the modern unified spec ([[Boot/UEFI]]).

## EFI services (conceptual)

| Phase | Role |
|-------|------|
| Boot Services | Memory map, protocol handles, load images — torn down when OS calls `ExitBootServices` |
| Runtime Services | Small subset survives into OS (variables, clock, reset) |

Boot loaders query GOP (graphics), block I/O, and simple file system protocols to read the kernel from disk.

## Naming in the field

- **ESP** — EFI System Partition on GPT.
- **.efi files** — PE32+ executables the firmware runs directly.
- **OVMF** — open-source UEFI firmware for QEMU/KVM guests.

Legacy **BIOS** used 16-bit real-mode interrupt handlers; EFI/UEFI runs flat protected/long mode with tables describing hardware — closer to how an [[OS program]] expects memory.

## Sources

- UEFI Forum — [Specifications](https://uefi.org/specifications)
- Wikipedia: [Unified Extensible Firmware Interface](https://en.wikipedia.org/wiki/Unified_Extensible_Firmware_Interface) (EFI history)
- Intel Platform Innovation Framework for EFI (pre-UEFI documentation archive)
