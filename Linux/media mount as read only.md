[[file mount]] [[management/Linux file management]]

# media mount as read only

> A filesystem remounted read-only usually means the kernel detected errors or I/O failure — writes are blocked to prevent further corruption.

Common triggers: disk errors, full disk during journal write, SAN disconnect, failing SSD. The mount flag `ro` appears in `/proc/mounts`.

## Confirm read-only

```bash
findmnt / -o TARGET,OPTIONS
mount | grep ' / '
dmesg -T | tail -50
```

## Remount read-write (after fixing cause)

```bash
# ext4 root — often requires remount
sudo mount -o remount,rw /

# If busy or fails, check why
sudo journalctl -k -b | grep -iE 'error|ext4|I/O'
```

**Do not** force `rw` on a failing disk without backup — risk data loss.

## Recovery workflow

1. Stop writers (`systemctl stop` heavy services if possible).
2. Read `dmesg` / SMART (`smartctl -a /dev/sdX`).
3. Filesystem check from maintenance mode or umount:
   ```bash
   sudo fsck -f /dev/sdXN
   ```
4. Remount `rw`; verify application writes.

## LVM / RAID

Underlying PV or array degradation can surface as ro — check `pvdisplay`, `mdadm --detail`.

## Related

[[file mount]] · [[management/Linux file management]]

## Sources

- `man 8 mount` — remount options
- [ext4 documentation — kernel.org](https://www.kernel.org/doc/html/latest/filesystems/ext4.html)
