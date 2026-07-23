[[Persistent Block Storage]] [[logical partitions]] [[OS program]]

# MBR (Master Boot Record)

> Legacy first-sector boot layout: tiny partition table + boot code — **being replaced by GPT/UEFI on modern iron**.

---

## Mental model

**MBR** is the **first 512-byte sector** (LBA 0) of a disk. Classic layout:

```txt
LBA 0 (512 bytes)
┌────────────────┬──────────────────────┬─────────┐
│ boot code      │ partition table      │ 0x55AA  │
│ ~446 bytes     │ 4 × 16-byte entries  │ sig     │
└────────────────┴──────────────────────┴─────────┘
```

- **Boot code:** BIOS loads this sector to `0x7C00` and jumps — chainloads stage-2 bootloader (GRUB `core.img`).
- **Partition table:** max **4 primary** partitions (or 3 primary + 1 extended → logical drives).
- **Signature `0xAA55`:** BIOS validates before boot.

**Limits that matter in prod:**
- **2 TiB** max addressable per partition (32-bit LBA × 512).
- **4 primary slots** — workarounds via extended partitions (fragile).
- **No checksum** — corrupted table boots wrong partition or not at all.

**GPT contrast:** GUID Partition Table at LBA 1+, protective MBR at LBA 0 for old BIOS compatibility. UEFI boots from EFI System Partition (FAT), not MBR code path.

---

## Standard config / commands

### Inspect (read-only first)

```shell
# Partition layout
sudo fdisk -l /dev/sda
lsblk -f
parted /dev/sda print

# MBR bytes (careful — destructive tools nearby)
sudo dd if=/dev/sda bs=512 count=1 | hexdump -C | tail
# last two bytes should be 55 aa

# GRUB on BIOS/MBR systems
sudo grub-install --target=i386-pc /dev/sda   # installs to disk, not partition
sudo update-grub
```

### Backup / restore partition table only

```shell
# Backup first sector (includes MBR code + table)
sudo dd if=/dev/sda of=sda-mbr.bin bs=512 count=1

# Restore TABLE only (skip first 446 bytes boot code if dual-boot sensitive)
# Prefer: sfdisk -d /dev/sda > partition-backup.txt
sudo sfdisk -d /dev/sda > sda-layout.txt
sudo sfdisk /dev/sda < sda-layout.txt   # after disk swap / recovery
```

### Cloud / VM images

- AWS legacy BIOS AMIs often still MBR-style; newer Nitro + UEFI use GPT.
- P2V migrations: Windows may need `bcdboot` repair if MBR vs GPT mismatch.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| "Operating system not found" | BIOS boot order; external disk | Select correct disk; reinstall bootloader |
| Boot drops to `grub rescue>` | `ls`, `set` in GRUB shell | `set root`; `linux /vmlinuz...`; `initrd`; `boot` — then fix grub.cfg |
| Partition >2TiB invisible/wrong | MBR limit | Convert to GPT (`gdisk`) — **backup first**; may need BIOS→UEFI |
| Only 4 partitions allowed | `fdisk -l` primary count | Convert one to extended (legacy) or move to GPT |
| Clone won't boot | Cloned MBR UUID / wrong disk order | Re-run `grub-install` on target disk; fix fstab UUIDs |
| 0x55AA missing | hexdump sector 0 | Disk not bootable; restore MBR or reinstall OS |
| Dual-boot wiped | Windows installer overwrote MBR | Restore Linux boot code; chainload Windows |

---

## Gotchas

> [!WARNING]
> **`grub-install /dev/sda1` is wrong** — install to **whole disk** `/dev/sda` on BIOS/MBR, not a partition.

> [!WARNING]
> **dd restore of full 512 bytes** overwrites boot code from another machine — partition table OK, boot code may not match your GRUB version.

> [!WARNING]
> **Mixing GPT + legacy MBR tools** — `fdisk` on GPT disk shows "gpt" — use `gdisk`/`parted`. Protective MBR is not your partition table.

> [!WARNING]
> **P2V with secure boot / UEFI** — MBR mental model doesn't apply; ESP partition + `efibootmgr` instead.

> [!WARNING]
> **RAID presents virtual disk** — install bootloader to **RAID member set the BIOS sees as bootable**, often the array `/dev/sda`, not individual members.

---

## When NOT to use

- **New bare-metal / cloud:** prefer **GPT + UEFI** unless you have explicit legacy BIOS requirement.
- Don't hand-edit partition table hex unless recovery mode — use `sfdisk`/`parted` scripted layouts.
- Don't assume MBR on NVMe — check `parted print` every time.

---

## Related

[[Persistent Block Storage]] [[logical partitions]] [[OS program]] [[kernel subsystem]]
