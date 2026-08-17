[[Operating System]] [[Boot/UEFI]] [[logical partitions]] [[Persistent Block Storage]] [[inittramfs]]

# MBR

> The Master Boot Record is the first 512-byte sector at LBA 0 of a legacy BIOS-boot disk — it contains a tiny boot stub, four partition table entries, and a signature that tells the firmware where to find the bootable volume.

---

## Why It Matters

Storage and boot questions still surface MBR on older hardware, cloud images shipped for BIOS compatibility, and dual-boot setups. Understanding the 512-byte layout explains why you can only have four primary partitions (unless you use an extended partition), why disks larger than ~2 TiB need GPT, and why `dd`ing the wrong 512 bytes bricks boot. UEFI systems use GPT with an EFI System Partition, but many disks still carry a protective MBR in sector 0 for backward compatibility.

---

## Sources

- [Wikipedia — Master boot record](https://en.wikipedia.org/wiki/Master_boot_record) — Layout diagram, history, and the 2 TiB addressing limitation with 32-bit LBA.
- [GRUB Manual — BIOS installation](https://www.gnu.org/software/grub/manual/grub/grub.html#Installing-GRUB-using-grub_002dinstall) — How stage1/stage2 boot code embeds in the MBR and partition boot record.
- [UEFI Specification — GPT](https://uefi.org/specifications) — How GPT supersedes MBR on modern firmware while retaining a protective MBR at LBA 0.

---

## Key Concepts

### LBA 0 layout (512 bytes)

```txt
Byte 0–445:    Boot code (446 bytes maximum)
Byte 446–509:  4 × 16-byte partition table entries
Byte 510–511:  Boot signature 0x55 0xAA
```

Each 16-byte partition entry contains: boot flag (active), CHS start, partition type, CHS end, LBA start, sector count.

| Field | Size | Meaning |
|-------|------|---------|
| Boot flag | 1 byte | `0x80` = active (BIOS tries this partition first) |
| Partition type | 1 byte | `0x83` = Linux, `0x07` = NTFS, `0x82` = Linux swap, etc. |
| LBA start + count | 8 bytes each | Where the partition lives on disk |

### Boot flow (BIOS)

```txt
BIOS POST → read LBA 0 (MBR) → verify 0xAA55 → execute boot code
    → boot code loads stage2 / VBR from active partition → OS kernel
```

### Extended and logical partitions

Only four primary slots exist. An **extended partition** (type `0x05`) acts as a container for **logical partitions** — enabling more than four volumes on one disk. See [[logical partitions]].

### Size limit

MBR uses 32-bit sector counts with 512-byte sectors → maximum addressable disk ≈ **2 TiB** (2³² × 512). Larger disks require **GPT** ([[Boot/UEFI]]).

---

## Technical Details

### Inspect MBR on Linux

```bash
sudo fdisk -l /dev/sda
sudo dd if=/dev/sda bs=512 count=1 2>/dev/null | xxd | head
```

### Partition table operations

```bash
sudo fdisk /dev/sda          # interactive — MBR/GPT depending on label
sudo parted /dev/sda print
```

### Boot repair (GRUB on MBR disk)

```bash
# Reinstall GRUB to MBR — destructive if wrong disk
sudo grub-install --target=i386-pc /dev/sda
sudo update-grub
```

### Protective MBR on GPT disks

GPT disks still have an MBR-like sector 0 with a single partition entry spanning the whole disk (type `0xEE`). This prevents legacy tools from misinterpreting the disk as unpartitioned.

---

## Mistakes to Avoid

- Overwriting the MBR when you meant to rewrite only GRUB's embedded area — `dd if=zeros of=/dev/sda bs=446 count=1` destroys the partition table.
- Assuming MBR is required on UEFI-only systems — use GPT + ESP instead.
- Creating more than four primary partitions without an extended partition container.
- Ignoring that cloud images may ship MBR for BIOS compatibility even when the instance boots UEFI.

---

## Pros/Cons or Trade-offs

| Pro | Con |
|-----|-----|
| Universal on legacy BIOS firmware | Only four primary partitions |
| Simple 512-byte layout | ~2 TiB disk size limit |
| Well-understood boot repair tools | Tiny boot code field (446 bytes) — limited bootloader features |

---

## Comparison

| vs | Distinction |
|----|-------------|
| [[Boot/UEFI]] + GPT | Modern standard — ESP partition, unlimited partitions, >2 TiB |
| [[logical partitions]] | How MBR works around the four-primary limit |
| Protective MBR on GPT | Compatibility shim, not a real partition table |

---

## Use cases

- Legacy BIOS bare-metal servers and older VMs.
- Dual-boot Windows + Linux on older hardware.
- Forensics: reading LBA 0 to determine partition layout before mounting.
