[[etc files]] [[apt config]] [[terminal config]] [[editor config]] [[Linux Templates Directory]]

# Linux configuration

> Linux configuration is the sum of files in `/etc`, per-user dotfiles, kernel boot parameters, and systemd units that define how this host behaves.

Layers stack: **image/CM baseline** → **distribution defaults** in `/usr` → **local overrides** in `/etc` and `/home` → **runtime** (`/run`). Know which layer wins before debugging "my change did nothing."

## Configuration surfaces

| Surface | Examples |
|---------|----------|
| `/etc` | [[etc files]] |
| systemd | [[system service unit files]], drop-ins |
| Kernel cmdline | `/etc/default/grub` → [[management/grub]] |
| sysctl | `/etc/sysctl.d/*.conf` |
| User session | `~/.bashrc`, `~/.config/` |
| Packages | [[apt config]], [[apt package manager]] |

## Inspect effective config

```bash
# systemd unit after merges
systemctl cat nginx.service

# sysctl
sysctl net.ipv4.ip_forward

# Boot cmdline
cat /proc/cmdline
```

## Change discipline

1. One change at a time; note rollback path.
2. Prefer drop-in overrides over editing vendor files.
3. Reload or restart only the affected daemon.
4. Verify with read-back (`nginx -T`, `sshd -t`).

## Related

[[etc files]] · [[management/Linux system management]] · [[editor config]]

## Sources

- [FHS 3.0](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- [systemd.unit(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html)
