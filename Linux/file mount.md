[[media mount as read only]] [[management/Linux file management]] [[etc files]]

# file mount

> Mounting attaches a filesystem to the directory tree — block devices, network shares, and loop images become accessible paths.

The kernel tracks mounts in `/proc/mounts`. `/etc/fstab` defines boot-time mounts. **systemd** also manages `.mount` units.

## Manual mount

```bash
# List
findmnt
mount | column -t

# Mount USB (example)
sudo mkdir -p /mnt/usb
sudo mount /dev/sdb1 /mnt/usb -o uid=1000,gid=1000

# Unmount (device busy?)
sudo umount /mnt/usb
lsof +f -- /mnt/usb
```

## `/etc/fstab` entry

```
UUID=abc-123  /data  ext4  defaults,noatime  0  2
```

Fields: device, mountpoint, type, options, dump, fsck pass.

```bash
sudo mount -a          # test fstab
sudo findmnt --verify  # systemd hosts
```

## Network filesystems

```bash
# NFS example
sudo mount -t nfs server:/export /mnt/nfs

# CIFS
sudo mount -t cifs //server/share /mnt/share -o credentials=/root/.smbcred
```

## Read-only remount

See [[media mount as read only]] when filesystem errors force ro.

## Related

[[inittramfs]] · [[management/grub]] · [[media mount as read only]]

## Sources

- `man 8 mount`, `man 5 fstab`
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
