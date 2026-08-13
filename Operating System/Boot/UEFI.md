<!-- note-strategy: operational -->
[[Boot]] [[MBR]] [[Extensible Firmware interface (efi)]]

# UEFI

> UEFI (Unified Extensible Firmware Interface) boots the machine — POST, drivers, then hand off to an OS loader on the ESP.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Firmware finds an EFI System Partition (FAT), runs `.efi` bootloaders, optionally enforces Secure Boot signatures, then starts the kernel.

```txt
Power on → UEFI POST → discover disks
       → ESP (FAT) → BOOTX64.EFI / vendor loader
       → Secure Boot check (optional)
       → kernel + initramfs
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **UEFI** | Modern firmware API (replaces BIOS) | “Boots via EFI apps, not 512-byte MBR code.” |
| **ESP** | EFI System Partition | “FAT partition holding `.efi` loaders.” |
| **Secure Boot** | Only signed loaders run | “Stops unsigned bootkits; breaks custom kernels unless enrolled.” |
| **GPT** | GUID partition table | “UEFI expects GPT; large disks OK.” |
| **CSM / Legacy** | BIOS compatibility mode | “Emulates MBR boot; dying on new hardware.” |
| **NVRAM vars** | Boot order stored in firmware | “`Boot0001` entries point at loaders.” |

### How the story goes

1. **POST** — initialize CPU/RAM/devices.
2. **Discover** — GPT + ESP; network boot optional (HTTP/PXE variants).
3. **Load** — run selected `.efi` (shim → GRUB → Linux EFI stub).
4. **Hand off** — ExitBootServices; kernel owns the machine.

---

## Standard config / commands

```bash
# Firmware boot entries (Linux)
efibootmgr -v
ls /boot/efi/EFI

# Install GRUB for UEFI
sudo grub-install --target=x86_64-efi --efi-directory=/boot/efi
sudo update-grub

# Disk layout check
sudo parted /dev/sda print   # expect gpt + esp flag
```

| Knob | Why it matters |
|------|----------------|
| Secure Boot on/off | Signed modules / custom kernels |
| Boot order | USB vs disk vs network |
| Fast Boot | May skip USB devices |
| CSM disabled | Forces pure UEFI path |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| “No bootable device” | ESP missing / wrong path | Create FAT ESP; reinstall `.efi` |
| Secure Boot violation | Unsigned loader | Sign/enroll MOK or disable SB in lab |
| Boots old kernel only | NVRAM order / leftover entries | `efibootmgr` reorder; clean stale |
| Disk >2 TiB on “BIOS” | Legacy MBR limits | Use UEFI+GPT |
| Dual-boot lost Windows | Overwrote EFI entry | Repair with Windows/`bcdedit` + `efibootmgr` |
| VM won’t UEFI boot | Firmware set to BIOS | Enable UEFI in hypervisor |

---

## Gotchas

> [!WARNING]
> **ESP ≠ `/boot` always** — `/boot` can be ext4; ESP must be FAT and flagged `esp`.

> [!WARNING]
> **Secure Boot + third-party modules** — NVIDIA/DKMS often need MOK enrollment.

> [!WARNING]
> **Don’t `dd` an MBR image onto a GPT UEFI disk** — you trash the protective MBR / tables.

> [!WARNING]
> **Cloud images** — Nitro/Azure Gen2 want UEFI; Gen1 BIOS AMIs won’t boot there.

---

## When NOT to use

- **Ancient hardware with BIOS-only** — stay on MBR + CSM (or replace hardware).
- **Tiny embedded with custom ROM** — may not speak UEFI at all.
- **You only needed partition layout** — see [[UEFI (2)]] / [[MBR]] for MBR versus GPT choice.

---

## Related

[[Extensible Firmware interface (efi)]] [[UEFI (2)]] [[MBR]] [[MBR(Master Boot Record)]] [[logical partitions]] [[Persistent Block Storage]]
