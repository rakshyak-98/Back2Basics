[[Operating System]] [[Boot/UEFI]] [[Boot/Extensible Firmware interface (efi)]] [[MBR]] [[MBR(Master Boot Record)]]

# UEFI (2)

> Practical UEFI — firmware menus, ESP layout, Secure Boot, and CSM fallback that still boots legacy MBR when “UEFI-only” fails.

## Interview Relevance

Ops interview gold: mode mismatch (GPT/UEFI vs MBR/legacy), ESP + efibootmgr recovery, and Secure Boot isolation steps.

## Sources

- UEFI Specification 2.10 — Boot Manager, Secure Boot — deep-dive
- Rod Smith, *Managing EFI Boot Loaders* (rEFInd) — deep-dive
- [Wikipedia — UEFI](https://en.wikipedia.org/wiki/UEFI) — overview
- [Wikipedia — EFI System Partition](https://en.wikipedia.org/wiki/EFI_System_Partition) — overview

## Key Concepts

- **Boot mode:** UEFI native vs Legacy/CSM must match GPT vs [[MBR]].
- **Secure Boot:** unsigned loaders fail unless enrolled (shim + MOK / custom keys).
- **Boot order:** NVRAM entries point at `.efi` paths.
- **ESP:** FAT32 GPT partition holding vendor `EFI/...` trees.

## Technical Details

## Firmware setup concepts

- Fast Boot may skip USB enumeration — hurts rescue keys.
- Clone migrations must copy ESP **and** re-register NVRAM (`efibootmgr`).

## When CSM still matters

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

Complements [[Boot/UEFI]].

## Real-World Applications

Post-clone “no bootable device,” dual-boot repairs, and RAID/firmware menu debugging.

## Pros/Cons or Trade-offs

- **Pro:** Clear field checklist for the most common boot failures.
- **Con:** CSM keeps legacy footguns alive on “modern” boards.
- **Trade-off:** Secure Boot security vs temporary disable for diagnosis.

## Comparison

- vs [[Boot/UEFI]]: conceptual boot flow vs practical recovery.
- vs [[MBR]]: legacy sector chain vs ESP + NVRAM entries.

## Mistakes to Avoid

- Fixing only the OS partition and forgetting ESP/NVRAM.
- Mixing GPT disks with Legacy-only boot mode.
- Leaving Secure Boot disabled after a temporary test.
