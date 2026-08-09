[[Linux]] [[media mount as read only]] [[fstab]]

# file mount

> Mount attaches a filesystem (disk, ISO, NFS, bind) onto a directory — the tree is how userland sees storage.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** device + fstype + options → directory; `/etc/fstab` makes it permanent; `findmnt` shows truth.

```txt
/dev/sdX1 ──mount──► /data
UUID=…   ──fstab──► reboot-safe
bind /a  ──mount --bind──► /b
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **mount point** | Empty dir target | “Don’t hide real files under a mount.” |
| **fstab** | Boot mounts | “Bad fstab can make the box unbootable.” |
| **UUID/LABEL** | Stable identity | “Prefer UUID over `/dev/sdX`.” |
| **bind mount** | Remap a directory | “Same inode tree, second path.” |
| **nofail / x-systemd** | Boot resilience | “Network mounts need `_netdev`.” |

---

## Standard config / commands

```bash
lsblk -f
sudo mount /dev/sdb1 /mnt/data
sudo mount -t nfs server:/export /mnt/nfs
sudo mount --bind /var/lib/docker /mnt/docker-view
findmnt
findmnt -T /var
# fstab line:
# UUID=… /data ext4 defaults,nofail 0 2
sudo mount -a
sudo umount /mnt/data
```

| Knob | Why it matters |
|------|----------------|
| `defaults,nofail` | Boot continues if disk missing |
| `_netdev` | Wait for network before NFS |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Target busy | `lsof`/`fuser -m` | Close files; lazy `umount -l` last resort |
| Wrong device after reboot | `/dev/sd` order | Switch fstab to UUID |
| NFS hang on boot | Missing `_netdev` | Add option; use automount |
| Permission weird | uid mapping / root_squash | Align IDs; check export opts |
| “already mounted” | `findmnt` | Umount or mount elsewhere |

---

## Gotchas

> [!WARNING]
> **Mount hides existing dir contents** — files under the mount point are invisible until umount.

> [!WARNING]
> **`umount -l` lazy** — detaches namespace now; I/O may still finish — don’t yank disks yet.

---

## When NOT to use

- **Copying data** — mount isn’t backup; use [[rsync]].
- **App config** — don’t mount over busy program dirs without stopping the service.

---

## Related

[[media mount as read only]] [[rsync]] [[lsof]] [[Linux file management]]
