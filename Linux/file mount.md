[[media mount as read only]] [[management/Linux file management]] [[etc files]] [[inittramfs]]

# file mount

> Mounting attaches a filesystem to the directory tree — block devices, network shares, and loop images become accessible paths under a mountpoint.





## Interview Relevance
Ops essential: read `findmnt`/`/proc/mounts`, write a correct `/etc/fstab` line (UUID, options, dump/fsck fields), and recover from busy umount or read-only remount.

## Sources
- `man 8 mount`, `man 5 fstab` — deep-dive
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html) — overview

## Core Definition
The kernel tracks mounts in `/proc/mounts`. `/etc/fstab` defines boot-time mounts; **systemd** also manages `.mount` units. Mount options control rw/ro, atime, and ownership for foreign filesystems.

## Key Concepts
- **Device → mountpoint → type → options:** The four core fstab ideas (plus dump/fsck pass).
- **UUID/LABEL over `/dev/sdX`:** Device letters move; UUIDs do not.
- **Busy umount:** Open files or cwd under the mount block `umount`.
- **Network FS:** NFS/CIFS add credentials, soft/hard, and timeout behavior.
- **ro remount:** Errors or explicit policy — [[media mount as read only]].

## Technical Details
```bash
findmnt
mount | column -t

sudo mkdir -p /mnt/usb
sudo mount /dev/sdb1 /mnt/usb -o uid=1000,gid=1000

sudo umount /mnt/usb
lsof +f -- /mnt/usb
```

```
UUID=abc-123  /data  ext4  defaults,noatime  0  2
```

Fields: device, mountpoint, type, options, dump, fsck pass.

```bash
sudo mount -a
sudo findmnt --verify

sudo mount -t nfs server:/export /mnt/nfs
sudo mount -t cifs //server/share /mnt/share -o credentials=/root/.smbcred
```

## Real-World Applications
Attach a data disk by UUID in `fstab` with `noatime`, verify with `mount -a` in a change window, and confirm with `findmnt /data` after reboot.

## Pros/Cons or Trade-offs
- **Pro:** Explicit, auditable attachment of storage into the namespace.
- **Con:** Wrong fstab can delay or break boot (initramfs / emergency mode) — always test and prefer UUID.

## Comparison
vs copying files into a directory: without a mount, a path is just an empty dir on the parent filesystem. vs bind mounts: remount an existing tree at another path without a new device. vs [[inittramfs]]: early boot must find and mount real root before these fstab entries fully apply.

## Mistakes to Avoid
- Using `/dev/sdb1` in fstab on systems where disk order changes.
- Forcing `umount -l` without understanding lazy unmount leaves processes on a detached tree.
- Ignoring a remount-ro after filesystem errors — see [[media mount as read only]].
