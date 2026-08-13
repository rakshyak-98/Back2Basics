[[Linux configuration]] [[file mount]] [[user management]] [[apt config]]

# etc files

> `/etc` holds host-local configuration — the authoritative text files operators edit (or template via configuration management) to define system behavior.

Unlike `/usr` (vendor defaults), **`/etc` is for administrators**. Many daemons read one file here at startup; changes often need service reload.

## High-traffic paths

| File / dir | Purpose |
|------------|---------|
| `/etc/fstab` | Filesystem mounts — [[file mount]] |
| `/etc/hosts` | Static name overrides |
| `/etc/resolv.conf` | DNS resolvers (may be managed by NetworkManager/systemd-resolved) |
| `/etc/ssh/sshd_config` | SSH server |
| `/etc/sudoers` | sudo policy — use [[visudo]] |
| `/etc/passwd`, `/etc/shadow` | Users — [[user management]] |
| `/etc/systemd/system/` | Unit overrides — [[system service unit files]] |
| `/etc/apt/` | APT config — [[apt config]] |
| `/etc/environment` | PAM-wide environment |

## Safe editing habits

```bash
# Backup before change
sudo cp -a /etc/ssh/sshd_config{,.bak.$(date +%F)}

# Validate syntax where tools exist
sudo sshd -t
sudo nginx -t
```

## What not to hand-edit

- `/etc/ld.so.cache` — run `ldconfig`
- Generated `resolv.conf` — fix NetworkManager or resolved config instead

## Related

[[Linux configuration]] · [[Linux Templates Directory]] · [[loggging]]

## Sources

- [Filesystem Hierarchy Standard — /etc](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html#etcOpt)
- `man 5 hosts`, `man 5 fstab`
