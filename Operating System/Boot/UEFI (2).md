[[Operating System]] [[Boot/UEFI]] [[Boot/Extensible Firmware interface (efi)]] [[MBR]] [[MBR(Master Boot Record)]]

# UEFI (2)

> Practical UEFI — firmware menus, ESP layout, Secure Boot, and CSM fallback that still boots legacy MBR when “UEFI-only” fails.

```txt
        UEFI (2) ──┬── Why it matters
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Ops review gold: mode mismatch (GPT/UEFI vs MBR/legacy), ESP + efibootmgr …

## Sources
- UEFI Specification 2.10 — Boot Manager, Secure Boot — deep-dive
- Rod Smith, *Managing EFI Boot Loaders* (rEFInd) — deep-dive
- [Wikipedia — UEFI](https://en.wikipedia.org/wiki/UEFI) — overview
- [Wikipedia — EFI System Partition](https://en.wikipedia.org/wiki/EFI_System_Partition) — overview

## Technical Details
### Recovery checklist

1. Confirm firmware mode matches disk label type (GPT/UEFI or MBR/legacy).
2. Mount ESP; verify `BOOTX64.EFI` or distribution shim exists.
3. `efibootmgr -v` — correct disk UUID and `.efi` path.
4. Disable Secure Boot temporarily to isolate signature issues.
5. For Linux, reinstall grub-efi to ESP from chroot.

- Complements [[Boot/UEFI]].

## Mistakes to Avoid
- **Mistake:** Fixing only the OS partition and forgetting ESP/NVRAM
- **Mistake:** Mixing GPT disks with Legacy-only boot mode
- **Mistake:** Leaving Secure Boot disabled after a temporary test

## Pros/Cons or Trade-offs
```txt
UEFI-native:  GPT + ESP + .efi loader
Legacy/CSM:   MBR active partition + boot sector chain → GRUB/Windows VBR
```


- **Pro:** Clear field checklist for the most common boot failures.
- **Con:** CSM keeps legacy footguns alive on “modern” boards.
- **Trade-off:** Secure Boot security vs temporary disable for diagnosis.

## Comparison
- vs [[Boot/UEFI]]: conceptual boot flow vs practical recovery.
- vs [[MBR]]: legacy sector chain vs ESP + NVRAM entries.


### Use cases
- Post-clone “no bootable device,” dual-boot repairs, and RAID/firmware menu de…
