[[file mount]] [[management/Linux file management]]

# media mount as read only

> When the kernel remounts a filesystem read-only, writes stop to limit corruption — usually after I/O errors or journal failure.

```txt
        media mount as rea ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Ops emergency path: confirm `ro` in mounts, read `dmesg`, fix the underlying …

## Sources
- `man 8 mount` — deep-dive
- [ext4 documentation — kernel.org](https://www.kernel.org/doc/html/latest/filesystems/ext4.html) — overview

## Key Concepts
- **Core:** Common triggers: disk errors, full disk during journal write, SAN disconnect,…

## Technical Details
```bash
findmnt / -o TARGET,OPTIONS
mount | grep ' / '
dmesg -T | tail -50
sudo mount -o remount,rw /
sudo journalctl -k -b | grep -iE 'error|ext4|I/O'
sudo fsck -f /dev/sdXN
```

- Recovery workflow:

1. Stop heavy writers if possible.
2. Read `dmesg` / SMART (`smartctl -a /dev/sdX`).
3. Filesystem check from maintenance mode or after umount.
4. Remount `rw`; verify application writes.

- Also check `pvdisplay`, `mdadm --detail` when LVM/RAID sits underneath.

## Mistakes to Avoid
- **Mistake:** `mount -o remount,rw` without reading kernel logs first
- **Mistake:** Running destructive `fsck` on a mounted dirty filesystem
- **Mistake:** Ignoring RAID/LVM health when only the mount looks “broken.”

## Pros/Cons or Trade-offs
- **Pro:** Remount-ro often saves more data than continuing dirty writes.
- **Con:** Forcing `rw` on a dying disk can finish the corruption.

## Comparison
- vs intentional `ro` mounts: policy (ISO, media) vs emergency error path


### Use cases
- Cloud VM root goes read-only after a flaky volume
