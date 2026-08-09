[[Linux]] [[file mount]] [[rsync]]

# media mount as read only

> Mount removable or network media read-only when you must inspect without risk of writes — forensics, untrusted USB, golden images.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `mount -o ro` (and often `noload` for ext) blocks writers; still verify with `findmnt` before trusting it.

```txt
block device ──mount -o ro,noload──► /mnt/usb
                     │
                     └─ writes fail with EROFS
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **ro** | Read-only mount | “Kernel rejects writes with EROFS.” |
| **noload** | Skip ext journal replay | “Avoid writing replay to suspect disks.” |
| **loop** | File as block device | “Mount images without USB.” |
| **udisks** | Desktop automount | “May remount rw — check options.” |
| **bind remount** | Change flags in place | “`mount -o remount,ro`.” |

---

## Standard config / commands

```bash
sudo mount -o ro /dev/sdb1 /mnt/usb
sudo mount -o ro,noload /dev/sdb1 /mnt/usb   # ext*
sudo mount -o ro,loop image.iso /mnt/iso
findmnt /mnt/usb
mount | grep /mnt/usb
sudo mount -o remount,ro /mnt/usb
sudo umount /mnt/usb
```

| Knob | Why it matters |
|------|----------------|
| `ro,noload` | Safer for dirty ext journals |
| `uid=/gid=` (vfat) | Who can read the tree |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Still writable | `findmnt -o OPTIONS` | Remount `ro`; stop automounters |
| mount fails dirty fs | Journal needs replay | Prefer `noload` or image the disk first |
| Permission denied reading | FAT uid mapping | `uid=$UID` or read as root |
| Device busy on umount | Open files | `lsof +f -- /mnt/usb`; `fuser -m` |

---

## Gotchas

> [!WARNING]
> **`ro` is not tamper-evidence** — a malicious kernel module or wrong device path still hurts; image first for forensics.

> [!WARNING]
> **Desktop automount** can remount rw when you click the volume in the file manager.

---

## When NOT to use

- **Need to repair/write** — mount rw intentionally after backup.
- **Network shares with mandatory locks** — NFS `ro` still has cache semantics to understand.

---

## Related

[[file mount]] [[lsof]] [[rsync]] [[Linux file management]]
