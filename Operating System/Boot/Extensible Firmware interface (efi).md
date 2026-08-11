[[Boot]] [[UEFI]] [[MBR]] [[UEFI (2)]]

# Extensible Firmware interface (efi)

> EFI is the firmware interface that replaced BIOS — modern systems run it as UEFI and boot loaders from an ESP.

---

## Mental model

**Say it in one breath:** EFI apps (`.efi`) run before the OS; they use GPT disks, optional networking, and Secure Boot policy.

```txt
BIOS era:  16-bit firmware → MBR sector
EFI/UEFI:  EFI bytecode/apps → ESP → OS loader
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **EFI** | Extensible Firmware Interface | “Intel’s BIOS replacement API.” |
| **UEFI** | Unified EFI | “What shipping PCs implement.” |
| **ESP** | EFI System Partition | “FAT partition of loaders.” |
| **GPT** | GUID Partition Table | “Required companion for big disks.” |
| **Secure Boot** | Signature gate | “Only trusted `.efi` runs.” |
| **EFI stub** | Kernel as EFI app | “Linux can be booted directly.” |

### How the story goes

1. **Power-on** — EFI initializes hardware.
2. **Select** — Boot#### NVRAM or default `\EFI\BOOT\BOOTX64.EFI`.
3. **Run loader** — shim/GRUB/systemd-boot/Windows Boot Manager.
4. **ExitBootServices** — OS owns RAM/devices.

---

## Standard config / commands

```bash
ls /sys/firmware/efi          # empty ⇒ not booted via EFI
efibootmgr -v
ls /boot/efi/EFI
sudo grub-install --target=x86_64-efi --efi-directory=/boot/efi
```

| Knob | Why it matters |
|------|----------------|
| Secure Boot | Module signing story |
| Boot timeout / order | Rescue USB priority |
| CSM off | Pure EFI path |
| HTTP(S) boot | Firmware provisioning |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| No `/sys/firmware/efi` | Legacy boot | Reinstall in UEFI mode |
| Large disk unbootable | MBR used | GPT + ESP ([[UEFI (2)]]) |
| Secure Boot loop | Bad signature | MOK enroll or signed shim |
| Missing boot entry | NVRAM cleared | `efibootmgr -c` or `--removable` |
| Dual boot overwritten | Last installer won | Repair entries for both OSes |
| Cloud Gen2 fail | BIOS image | Switch to UEFI image |

---

## Gotchas

> [!WARNING]
> **EFI ≈ UEFI in conversation** — UEFI is the standard; EFI is the ancestor name.

> [!WARNING]
> **ESP must be FAT** — ext4 `/boot` alone is not enough for firmware.

> [!WARNING]
> **Bitlocker + Linux** — Secure Boot/TPM policies interact; plan dual-boot.

> [!WARNING]
> **Alias notes** — deep dive boot order in [[UEFI]]; disk scheme in [[UEFI (2)]].

---

## When NOT to use

- **BIOS-only industrial PCs** — stay MBR until hardware refresh.
- **Microcontrollers** — no EFI; use vendor ROM/bootloaders.
- **Explaining PCIe** — wrong layer; see [[PCI (Peripheral Component Interconnect)]].

---

## Related

[[UEFI]] [[UEFI (2)]] [[MBR]] [[MBR(Master Boot Record)]] [[OS program]]
