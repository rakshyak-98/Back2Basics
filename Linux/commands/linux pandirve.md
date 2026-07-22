[[file mount]] [[Linux file management]] [[Linux system management]]

# USB pendrive (removable media)

> One-line: **USB flash drive** prep — partition, FAT/exfat format, safe mount/unmount. Filename was a typo (`pandirve`); not pandoc. **Classic ops task on bare-metal and air-gapped hosts.**

## Mental model

USB block device appears as `/dev/sdX` (whole disk) and `/dev/sdX1` (first partition). Kernel + udev may **auto-mount** under `/media/$USER/`. Manual workflow: identify device → unmount if busy → partition (optional) → mkfs → mount → sync before physical remove.

```
lsblk ──► /dev/sdb1 ──► mkfs.vfat ──► mount ──► cp data ──► umount ──► eject
```

| Filesystem | Use case |
|------------|----------|
| `vfat` (FAT32) | UEFI ESP, max compatibility; 4GB file limit |
| `exfat` | Large files; Windows/macOS/Linux with exfat-fuse |
| `ext4` | Linux-only; permissions preserved |

> [!WARNING]
> **Triple-check device node** — `mkfs` on `/dev/sdb` vs `/dev/sdb1` wipes wrong scope. Use `lsblk`, by-id paths in scripts.

## Standard config / commands

```bash
# Identify — look at SIZE and RM (removable)
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT,RM,MODEL
sudo fdisk -l /dev/sdb

# Unmount before format (was: pandrive typo in original note)
sudo umount /dev/sdb1
# if busy: sudo fuser -mv /dev/sdb1; close files; umount again

# FAT32 for universal swap (label optional)
sudo mkfs.vfat -F 32 -n USBDATA /dev/sdb1

# exFAT for large files
sudo mkfs.exfat -n USBDATA /dev/sdb1

# Mount manually
sudo mkdir -p /mnt/usb
sudo mount /dev/sdb1 /mnt/usb
# or with uid for desktop user write:
sudo mount -o uid=1000,gid=1000,umask=022 /dev/sdb1 /mnt/usb

# Safe removal — flush buffers
sync
sudo umount /dev/sdb1
sudo eject /dev/sdb                # or udisksctl power-off
```

**Partition from scratch (destructive):**

```bash
sudo parted /dev/sdb --script mklabel gpt mkpart primary fat32 1MiB 100%
sudo mkfs.vfat -F 32 /dev/sdb1
```

**Persist mount (servers) — use UUID in `/etc/fstab`:**

```bash
blkid /dev/sdb1
# UUID=XXXX  /mnt/usb  vfat  defaults,noauto,user  0  0
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `target is busy` on umount | Open file or cwd on mount | `fuser -mv /mnt/usb`; `cd /`; close apps |
| Device not appearing | USB port/cable | `dmesg \| tail`; try another port; `lsusb` |
| Read-only mount | Filesystem errors | `dmesg`; `fsck.vfat /dev/sdb1`; replace failing stick |
| Wrong `/dev/sdX` after replug | Names shuffle | Use `/dev/disk/by-id/usb-...` in scripts |
| `Permission denied` on copy | Mount options | Remount with `uid=` or run as root (avoid) |
| Slow writes | Cheap stick or USB2 | Expected; use exfat/ext4 for large sequential |

## Gotchas

> [!WARNING]
> **Never run `mkfs` on `/dev/sda` without confirming** — on some VMs sda is system disk. Match SIZE/MODEL in `lsblk`.

> [!WARNING]
> **Pulling without umount** — filesystem corruption; silent data loss. Always `sync && umount`.

> [!WARNING]
> **Auto-mount + manual mount** — double-mount confusion. One mount point at a time.

> [!WARNING]
> **FAT32 4GB file limit** — large ISOs need exfat or split archives.

## When NOT to use

- **Production data transfer** → encrypted media, signed artifacts, object storage — not random USB.
- **Document conversion** → that's **pandoc**, unrelated tool.
- **Persistent server storage** → proper block volume + ext4/xfs, not consumer flash.

## Related

[[file mount]] [[Linux file management]] [[Linux system management]] [[MBR]]
