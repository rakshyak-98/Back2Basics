[[file mount]] [[management/grub]] [[etc files]]

# inittramfs

> The initial RAM filesystem (initramfs) is a cpio archive loaded by the bootloader — early userspace that mounts real root and hands off to PID 1.

The kernel unpacks **initramfs** into a tmpfs root. Scripts or **systemd** in initramfs load storage drivers (LVM, LUKS, RAID, NFS root), unlock encryption, then `switch_root` to the real `/`.

## Files (Debian/Ubuntu)

| Path | Role |
|------|------|
| `/boot/initrd.img-*` | Generated image |
| `/etc/initramfs-tools/` | Hooks and config |
| `update-initramfs` | Regenerate |

```bash
# List contents
lsinitramfs /boot/initrd.img-$(uname -r) | head

# Rebuild after driver/module change
sudo update-initramfs -u -k all
```

## RHEL family

```bash
dracut -f /boot/initramfs-$(uname -r).img $(uname -r)
```

## Boot failures involving initramfs

| Symptom | Check |
|---------|-------|
| `Gave up waiting for root device` | UUID in `/etc/fstab` vs actual; regenerate initramfs |
| Drop to initramfs shell | `cat /proc/cmdline`; unlock LUKS manually |
| Module not found | Add driver to initramfs hooks |

Emergency shell in initramfs:

```bash
# From busybox prompt
ls /dev/mapper
cryptsetup open ...
exit
```

## Related

[[management/grub]] · [[file mount]] · [[systemd]]

## Sources

- `man 8 update-initramfs`, `man 8 dracut`
- [kernel.org initramfs](https://www.kernel.org/doc/html/latest/admin-guide/initrd.html)
