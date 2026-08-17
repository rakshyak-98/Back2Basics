[[file mount]] [[management/grub]] [[etc files]] [[systemd]]

# inittramfs

> The initial RAM filesystem (initramfs) is a cpio archive the bootloader loads — early userspace that finds disks, unlocks encryption, mounts real root, then hands off to PID 1.





## Interview Relevance
Boot troubleshooting classic: “gave up waiting for root device,” LUKS unlock in the initramfs shell, and when to regenerate with `update-initramfs` / `dracut` after adding storage drivers.

## Sources
- `man 8 update-initramfs`, `man 8 dracut` — deep-dive
- [kernel.org initramfs / initrd](https://www.kernel.org/doc/html/latest/admin-guide/initrd.html) — overview

## Core Definition
The kernel unpacks **initramfs** into a tmpfs root. Hooks load storage drivers (LVM, LUKS, RAID, NFS root), unlock volumes, then `switch_root` to the real `/` and exec the real init (usually systemd).

## Key Concepts
- **Early userspace:** Runs before the real root filesystem is mounted.
- **Generated image:** Built from hooks/modules — not hand-edited on `/boot` long-term.
- **cmdline contract:** Root UUID/LABEL and cryptdevice args must match reality.
- **Emergency shell:** Drop to busybox when root cannot be mounted.
- **Distro tools:** `update-initramfs` (Debian) vs `dracut` (RHEL family).

## Technical Details
| Path | Role |
|------|------|
| `/boot/initrd.img-*` | Generated image (Debian/Ubuntu naming) |
| `/etc/initramfs-tools/` | Hooks and config |
| `update-initramfs` | Regenerate |

```bash
lsinitramfs /boot/initrd.img-$(uname -r) | head
sudo update-initramfs -u -k all
```

```bash
# RHEL family
dracut -f /boot/initramfs-$(uname -r).img $(uname -r)
```

| Symptom | Check |
|---------|-------|
| `Gave up waiting for root device` | UUID in `/etc/fstab` / cmdline vs actual; regenerate |
| Drop to initramfs shell | `cat /proc/cmdline`; unlock LUKS manually |
| Module not found | Add driver to initramfs hooks |

```bash
# From busybox prompt
ls /dev/mapper
cryptsetup open ...
exit
```

## Real-World Applications
After enabling LUKS or switching root to a new UUID, regenerate initramfs and update GRUB so the next reboot can unlock and mount root automatically.

## Pros/Cons or Trade-offs
- **Pro:** Flexible early boot (crypto, LVM, network root) without baking drivers into the kernel binary.
- **Con:** Wrong or stale image bricks boot until you recover from live media or the emergency shell.

## Comparison
vs initrd (legacy): same idea; initramfs is the modern cpio+tmpfs form. vs [[management/grub]]: GRUB loads kernel + initramfs; initramfs prepares root. vs real root `/`: initramfs is temporary and discarded after `switch_root`.

## Mistakes to Avoid
- Changing disk UUIDs or modules without `update-initramfs` / `dracut`.
- Hand-patching the image under `/boot` instead of fixing hooks and regenerating.
- Confusing a GRUB misconfig with an initramfs root-mount failure — check `/proc/cmdline` in the emergency shell.
