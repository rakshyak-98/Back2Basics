[[Operating System]] [[Boot/UEFI]] [[Boot/Extensible Firmware interface (efi)]] [[MBR]] [[MBR(Master Boot Record)]]

# UEFI (2)

> Practical UEFI — firmware setup menus, ESP layout, Secure Boot, and the CSM fallback that still boots legacy MBR disks when “UEFI-only” fails.

This note complements [[Boot/UEFI]] with field operations: what you touch when a machine “will not boot” after disk clone, dual-boot, or RAID changes.

## Firmware setup concepts

- **Boot mode:** UEFI native versus Legacy/CSM — mismatch with partition scheme (GPT vs [[MBR]]) produces “no bootable device.”
- **Secure Boot:** when enabled, unsigned or unknown boot loaders fail unless enrolled (shim + MOK, or custom keys).
- **Boot order:** NVRAM entries point to `.efi` paths, not only disk order.
- **Fast Boot / Ultra Fast:** may skip USB enumeration — affects rescue USB keys.

## EFI System Partition (ESP)

- FAT32, flagged ESP on GPT, typically 100–550 MiB.
- Holds vendor-specific paths: `EFI/Microsoft/Boot`, `EFI/ubuntu`, `EFI/BOOT/BOOTX64.EFI`.
- Clone migrations must copy ESP **and** re-register NVRAM entries or run `efibootmgr`.

## When CSM still matters

Old images, some PXE chains, and MBR-only USB installers rely on **CSM** to emulate BIOS INT 13h disk access. Pure UEFI paths load PE/COFF binaries directly — no 446-byte stage in LBA 0.

```txt
UEFI-native:  GPT + ESP + .efi loader
Legacy/CSM:   MBR active partition + boot sector chain → GRUB/Windows VBR
```

## Recovery checklist

1. Confirm firmware mode matches disk label type (GPT/UEFI or MBR/legacy).
2. Mount ESP; verify `BOOTX64.EFI` or distribution shim exists.
3. `efibootmgr -v` — correct disk UUID and `.efi` path.
4. Disable Secure Boot temporarily to isolate signature issues.
5. For Linux, reinstall grub-efi to ESP from chroot.

## Sources

- UEFI Specification 2.10 — Boot Manager, Secure Boot
- Rod Smith, *Managing EFI Boot Loaders* (rEFInd documentation)
- Wikipedia: [UEFI](https://en.wikipedia.org/wiki/UEFI), [EFI System Partition](https://en.wikipedia.org/wiki/EFI_System_PARTITION)
