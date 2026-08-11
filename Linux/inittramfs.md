[[Linux]] [[grub]] [[systemd]]

# inittramfs

> initramfs (initial RAM filesystem) is a tiny root the kernel unpacks first — load modules, find disks, then pivot to the real root.

---

## Mental model

**Say it in one breath:** GRUB loads kernel+initramfs → `/init` mounts real root → `switch_root` into systemd as PID 1.

```txt
GRUB → kernel + initramfs.img
         │
         ├─ modules (storage, lvm, md, crypt)
         ├─ mount real root (UUID=…)
         └─ switch_root → /sbin/init
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **initramfs** | cpio archive on tmpfs | “Early userspace before real root.” |
| **update-initramfs / dracut** | Rebuild tools | “After kernel/module change, rebuild.” |
| **root=** | Kernel cmdline root | “Wrong UUID → emergency shell.” |
| **switch_root** | Pivot to real disk | “Then systemd becomes PID 1.” |
| **emergency shell** | Early boot failure | “Usually storage/LVM/crypt/module.” |

---

## Standard config / commands

```bash
sudo update-initramfs -u -k all          # Debian/Ubuntu
# Fedora: sudo dracut -f

lsinitramfs /boot/initrd.img-$(uname -r) | head
cat /proc/cmdline
blkid
```

| Knob | Why it matters |
|------|----------------|
| `root=UUID=` | Must match `blkid` |
| Hooks/modules | Include storage + crypto drivers |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Dropped to initramfs shell | `blkid`; modules | Fix UUID; rebuild with needed modules |
| Unbootable after kernel upgrade | Image stale | `update-initramfs -u` / `dracut -f` |
| LUKS won’t unlock | cryptsetup missing | Add crypt hooks; check `cryptdevice=` |
| LVM root missing | dm/lvm not in image | Include LVM in initramfs config |

---

## Gotchas

> [!WARNING]
> **Hand-edit `grub.cfg`** — prefer `/etc/default/grub` + `update-grub`.

> [!WARNING]
> **Out-of-tree storage drivers** forgotten in the image → boot dies only on that hardware.

---

## When NOT to use

- **Debugging application services** — get past pivot to real root first.
- **Cloud user-data issues** — cloud-initialize is after real root, not initramfs.

---

## Related

[[grub]] [[systemd]] [[file mount]] [[LSB (Linux Standard Base)]]
