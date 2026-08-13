[[Operating System]] [[Boot/Extensible Firmware interface (efi)]] [[MBR]] [[Persistent Block Storage]] [[inittramfs]]

# UEFI

> UEFI (Unified Extensible Firmware Interface) is modern PC firmware that initializes hardware, reads boot entries from NVRAM, and loads signed EFI applications from the EFI System Partition — replacing the 446-byte MBR boot sector chain.

After power-on, the CPU starts firmware at a reset vector. **UEFI** runs in 32- or 64-bit mode with drivers, protocols, and a **boot manager** defined by the UEFI specification. The boot manager consults variables such as `BootOrder` and `Boot####` to choose an OS loader (for example `\EFI\ubuntu\shim.efi` → GRUB → Linux kernel).

## Boot flow (simplified)

```txt
Power-on → SEC/PEI/DXE (platform init) → BDS boot manager
         → load .efi from ESP (EFI System Partition, FAT32, GPT)
         → optional Secure Boot signature check
         → OS loader loads kernel + [[inittramfs]]
         → kernel takes over (long mode on x86-64)
```

## Versus legacy BIOS + MBR

| Topic | Legacy BIOS | UEFI |
|-------|-------------|------|
| Partition table | [[MBR]] (2 TiB limit) | GPT (large disks) |
| Boot code location | First sector boot sector | Files on ESP |
| Security | No standard Secure Boot | Secure Boot, measured boot (TPM) |
| Handoff mode | 16-bit real mode chain | Protected/long mode with tables |

Many machines ship **UEFI with CSM** (Compatibility Support Module) to boot old MBR images — see [[Boot/UEFI (2)]] for practical firmware menu behavior.

## Operations relevance

- Reinstalling boot loaders requires mounting the ESP (`/boot/efi`).
- Dual-boot means multiple NVRAM entries, not only an “active” partition flag.
- Cloud images are often UEFI-GPT; bare-metal automation must align partition layout with firmware mode.

Related: [[Boot/Extensible Firmware interface (efi)]] (EFI naming history), [[Linux/management/grub]].

## Sources

- UEFI Specification 2.10 — [Boot Manager](https://uefi.org/specs/UEFI/2.10/03_Boot_Manager.html)
- Wikipedia: [UEFI](https://en.wikipedia.org/wiki/UEFI)
- Microsoft Learn: UEFI firmware documentation
