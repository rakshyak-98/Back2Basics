[[Operating System]] [[Boot/Extensible Firmware interface (efi)]] [[MBR]] [[Persistent Block Storage]] [[inittramfs]] [[Boot/UEFI (2)]] [[Linux/management/grub]]

# UEFI

> UEFI is modern PC firmware that initializes hardware, reads boot entries from NVRAM, and loads signed EFI apps from the ESP — replacing the 446-byte MBR boot-sector chain.

## Interview Relevance

Explain UEFI boot flow vs BIOS+MBR, GPT/ESP, Secure Boot, and why dual-boot is NVRAM entries not just an active flag.

## Sources

- [UEFI Spec 2.10 — Boot Manager](https://uefi.org/specs/UEFI/2.10/03_Boot_Manager.html) — deep-dive
- [Wikipedia — UEFI](https://en.wikipedia.org/wiki/UEFI) — overview
- Microsoft Learn — UEFI firmware documentation — overview

## Key Concepts

- **Boot manager:** `BootOrder` / `Boot####` choose an OS loader.
- **ESP:** FAT32 on GPT holding `.efi` loaders.
- **Secure Boot:** signature checks before loader runs.
- **CSM:** optional legacy MBR path — see [[Boot/UEFI (2)]].

## Technical Details

```txt
Power-on → SEC/PEI/DXE (platform init) → BDS boot manager
         → load .efi from ESP (EFI System Partition, FAT32, GPT)
         → optional Secure Boot signature check
         → OS loader loads kernel + [[inittramfs]]
         → kernel takes over (long mode on x86-64)
```

| Topic | Legacy BIOS | UEFI |
|-------|-------------|------|
| Partition table | [[MBR]] (2 TiB limit) | GPT (large disks) |
| Boot code location | First sector boot sector | Files on ESP |
| Security | No standard Secure Boot | Secure Boot, measured boot (TPM) |
| Handoff mode | 16-bit real mode chain | Protected/long mode with tables |

Ops: remount ESP to reinstall loaders; cloud images are often UEFI-GPT. Related: [[Boot/Extensible Firmware interface (efi)]], [[Linux/management/grub]].

## Real-World Applications

Bare-metal provisioning, dual-boot laptops, and cloud VM images that must match firmware mode.

## Pros/Cons or Trade-offs

- **Pro:** Large disks, Secure Boot, structured boot entries.
- **Con:** More moving parts (ESP + NVRAM) than classic MBR.
- **Trade-off:** UEFI-only purity vs CSM for old installers.

## Comparison

- vs [[MBR]]: sector stub vs file-based loaders on ESP.
- vs [[Boot/UEFI (2)]]: architecture vs recovery checklist.

## Mistakes to Avoid

- Installing GRUB to the wrong place (MBR vs ESP) for the firmware mode.
- Assuming “active partition” still controls UEFI boot selection.
- Ignoring Secure Boot when a custom kernel/loader suddenly “vanishes.”
