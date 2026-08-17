[[file mount]] [[management/Linux file management]]

# media mount as read only

> When the kernel remounts a filesystem read-only, writes stop to limit corruption — usually after I/O errors or journal failure.





## Interview Relevance
Ops emergency path: confirm `ro` in mounts, read `dmesg`, fix the underlying disk/SAN issue, then remount `rw` — never force blindly.

## Sources
- `man 8 mount` — deep-dive
- [ext4 documentation — kernel.org](https://www.kernel.org/doc/html/latest/filesystems/ext4.html) — overview

## Core Definition
Common triggers: disk errors, full disk during journal write, SAN disconnect, failing SSD. The mount flag `ro` appears in `/proc/mounts` / `findmnt`.

## Recall Cues
- Why do interviewers care about Ops emergency path: confirm `ro` in mounts, read `dmesg`, fix the underlying disk/SAN issue, then remount `rw` — never force blindly?
- What is step 1: Stop heavy writers if possible?
- What is step 2: Read `dmesg` / SMART (`smartctl -a /dev/sdX`)?
- What is step 3: Filesystem check from maintenance mode or after umount?
- What is step 4: Remount `rw`; verify application writes?
- What mistake is **`mount -o remount,rw` without reading kernel logs first**?
- What mistake is **Running destructive `fsck` on a mounted dirty filesystem**?
- What mistake is **Ignoring RAID/LVM health when only the mount looks “broken.”**?

## Technical Details
```bash
findmnt / -o TARGET,OPTIONS
mount | grep ' / '
dmesg -T | tail -50
sudo mount -o remount,rw /
sudo journalctl -k -b | grep -iE 'error|ext4|I/O'
sudo fsck -f /dev/sdXN
```

Recovery workflow:

1. Stop heavy writers if possible.
2. Read `dmesg` / SMART (`smartctl -a /dev/sdX`).
3. Filesystem check from maintenance mode or after umount.
4. Remount `rw`; verify application writes.

Also check `pvdisplay`, `mdadm --detail` when LVM/RAID sits underneath.

## Mistakes to Avoid
- `mount -o remount,rw` without reading kernel logs first.
- Running destructive `fsck` on a mounted dirty filesystem.
- Ignoring RAID/LVM health when only the mount looks “broken.”

## Comparison
- vs intentional `ro` mounts: policy (ISO, media) vs emergency error path — same flag, different cause ([[file mount]]).

## Real-World Applications
Cloud VM root goes read-only after a flaky volume — stop services, snapshot if possible, fsck from rescue, remount, then replace the disk.

## Pros/Cons or Trade-offs
- **Pro:** Remount-ro often saves more data than continuing dirty writes.
- **Con:** Forcing `rw` on a dying disk can finish the corruption.
