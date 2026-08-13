<!-- note-strategy: operational -->
[[Boot]] [[UEFI]] [[MBR]] [[Persistent Block Storage]]

# UEFI (2)

> Pick GPT for UEFI boots and MBR for legacy BIOS — wrong pair = USB/disk that won’t boot on the target machine.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Partition table and firmware mode must match — BIOS reads MBR code; UEFI reads ESP on GPT (protective MBR only for compatibility).

```txt
Target firmware     Disk layout        Boot path
BIOS / CSM     →    MBR (+ optional) → boot code in LBA0
UEFI           →    GPT + ESP (FAT)  → *.efi on ESP
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **MBR disk** | Old partition scheme | “4 primary slots; 2 TiB limit.” |
| **GPT disk** | GUID table | “UEFI default; redundant headers.” |
| **Protective MBR** | Dummy MBR on GPT | “Stops old tools from ‘repartitioning’.” |
| **ESP** | EFI System Partition | “FAT with bootloaders.” |
| **Legacy BIOS USB** | MBR + syslinux/GRUB i386-pc | “For old laptops.” |
| **UEFI USB** | GPT + `/EFI/BOOT/BOOTX64.EFI` | “For modern PCs.” |

### How the story goes

1. **Know the target** — BIOS-only, UEFI-only, or both.
2. **Partition** — MBR or GPT accordingly.
3. **Install bootloader** — `i386-pc` versus `x86_64-efi`.
4. **Test** — on real firmware; VMs lie if misconfigured.

---

## Standard config / commands

```bash
sudo parted /dev/sdb print
# USB for UEFI:
#   parted: mklabel gpt → mkpart ESP fat32 1MiB 512MiB → set 1 esp on
# USB for legacy BIOS:
#   parted: mklabel msdos → bootable primary → grub-install --target=i386-pc
sudo grub-install --target=x86_64-efi --efi-directory=/mnt/esp --removable
```

| Knob | Why it matters |
|------|----------------|
| `msdos` vs `gpt` label | Firmware compatibility |
| `esp` flag | UEFI finds the FAT |
| `--removable` | Writes `\EFI\BOOT\BOOTX64.EFI` |
| Hybrid ISO | Tries both worlds; still fails some boxes |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| UEFI PC ignores USB | No ESP / no BOOTX64.EFI | GPT+FAT ESP; remake EFI files |
| Old PC ignores USB | GPT-only stick | Add MBR boot or make msdos stick |
| Boots on VM, not bare metal | Secure Boot / Fast Boot | Sign or disable SB; enable USB |
| “Invalid partition table” | Mixed tools rewrote label | Recreate one scheme cleanly |
| Dual-mode stick flaky | Hybrid assumptions | Ship two images |
| Disk >2 TiB on BIOS | MBR limit | UEFI+GPT only path |

---

## Gotchas

> [!WARNING]
> **Formatting “UEFI” as MBR** — may boot on one laptop and nowhere else.

> [!WARNING]
> **`--removable` vs NVRAM** — removable path doesn’t create firmware Boot#### entries.

> [!WARNING]
> **Windows + Linux USB tools** — Rufus “MBR for UEFI” is a special case; know what it wrote.

> [!WARNING]
> **This note is layout choice** — firmware internals live in [[UEFI]] / [[Extensible Firmware interface (efi)]].

---

## When NOT to use

- **Cloud disk templates** — follow image (Gen2 UEFI versus Gen1 BIOS); don’t invent hybrids.
- **Embedded raw flash** — may use neither classic MBR nor GPT.
- **You already standardized on UEFI-only fleet** — always GPT+ESP; skip MBR path.

---

## Related

[[UEFI]] [[Extensible Firmware interface (efi)]] [[MBR]] [[MBR(Master Boot Record)]] [[logical partitions]]
