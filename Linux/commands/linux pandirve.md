[[file mount]] [[Linux file management]] [[media mount as read only]] [[MBR]]

# USB pendrive (removable media)

> Removable USB storage shows up as a block device — identify with lsblk, filesystem it, mount it, sync, then unmount before you pull it.





## Interview Relevance
Ops hygiene: never guess `/dev/sdX`, prefer by-id paths, FAT32 vs exFAT limits, and `umount` before yanking the stick.

## Sources
- [lsblk(8)](https://man7.org/linux/man-pages/man8/lsblk.8.html) — overview
- [mount(8)](https://man7.org/linux/man-pages/man8/mount.8.html) — deep-dive

## Core Definition
A USB block device appears as `/dev/sdX` (disk) and `/dev/sdX1` (partition). Kernel/udev may auto-mount under `/media/$USER/`. Manual workflow: identify → unmount if busy → partition/mkfs if needed → mount → sync → umount/eject.

## Key Concepts
- **Whole disk vs partition:** `mkfs` on `sdb` vs `sdb1` wipes different scopes.
- **Filesystem choice:** vfat (compat, 4GB file limit), exfat (large files), ext4 (Linux perms).
- **Busy mounts:** open cwd/files block `umount` — use `fuser`.
- **Stable names:** `/dev/disk/by-id/usb-…` survives sdX reshuffles.
- **Persistence:** UUID in fstab with `noauto` for occasional mounts.

## Technical Details
```txt
lsblk ──► /dev/sdb1 ──► mkfs ──► mount ──► cp ──► umount ──► eject
```

```bash
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT,RM,MODEL
sudo fdisk -l /dev/sdb

sudo umount /dev/sdb1
sudo fuser -mv /dev/sdb1

sudo mkfs.vfat -F 32 -n USBDATA /dev/sdb1
sudo mkfs.exfat -n USBDATA /dev/sdb1

sudo mkdir -p /mnt/usb
sudo mount /dev/sdb1 /mnt/usb
sudo mount -o uid=1000,gid=1000,umask=022 /dev/sdb1 /mnt/usb

sync
sudo umount /dev/sdb1
sudo eject /dev/sdb

sudo parted /dev/sdb --script mklabel gpt mkpart primary fat32 1MiB 100%
blkid /dev/sdb1
# UUID=XXXX  /mnt/usb  vfat  defaults,noauto,user  0  0
```

| Symptom | Check | Fix |
|---------|-------|-----|
| target is busy | Open files/cwd | `fuser -mv`; `cd /`; close apps |
| Device missing | Port/cable | `dmesg`; `lsusb`; try another port |
| Read-only mount | FS errors | `fsck.vfat`; replace failing stick |
| Wrong sdX after replug | Name shuffle | Use `/dev/disk/by-id/…` |
| FAT32 copy fails on big file | 4GB limit | Use exfat/ext4 |

## Real-World Applications
Building a FAT32 installer stick, moving large ISOs via exFAT, and safely removing media on a headless server after `sync && umount`.

## Pros/Cons or Trade-offs
- **Pro vfat:** Universal across OSes and firmware.
- **Con vfat:** 4GB file limit; weak permissions.
- **Trade-off:** Consumer flash for sneaker-net vs encrypted/object storage for production data.

## Comparison
vs [[file mount]] / fstab volumes: pendrives are transient; server disks are persistent. vs pandoc: unrelated — the filename typo “pandirve” is USB, not document conversion.

## Mistakes to Avoid
- Running `mkfs` without confirming SIZE/MODEL in `lsblk` (system disk footgun).
- Pulling the stick without `umount`.
- Hard-coding `/dev/sdb1` in scripts.
