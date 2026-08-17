[[etc files]] [[apt config]] [[terminal config]] [[editor config]] [[Linux Templates Directory]] [[system service unit files]] [[management/grub]] [[management/Linux system management]]

# Linux configuration

> Linux configuration is the sum of `/etc`, per-user dotfiles, kernel boot parameters, and systemd units that define how this host behaves.

```txt
        Linux configuratio ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Senior ops signal: know which layer wins (image → distro defaults → `/etc` → …

## Sources
- [FHS 3.0](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html) — overview
- [systemd.unit(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html) — deep-dive

## Key Concepts
- **Core:** Layers stack: **image/CM baseline** → **distribution defaults** in `/usr` → *…

## Technical Details
| Surface | Examples |
|---------|----------|
| `/etc` | [[etc files]] |
| systemd | [[system service unit files]], drop-ins |
| Kernel cmdline | `/etc/default/grub` → [[management/grub]] |
| sysctl | `/etc/sysctl.d/*.conf` |
| User session | `~/.bashrc`, `~/.config/` |
| Packages | [[apt config]], [[apt package manager]] |

```bash
systemctl cat nginx.service
sysctl net.ipv4.ip_forward
cat /proc/cmdline
```

- Change discipline:

1. One change at a time; note rollback path.
2. Prefer drop-in overrides over editing vendor files.
3. Reload or restart only the affected daemon.
4. Verify with read-back (`nginx -T`, `sshd -t`).

## Mistakes to Avoid
- **Mistake:** Editing `/usr/lib/systemd/system/*.service` and losing changes o…
- **Mistake:** Changing a file that is overridden by a higher-priority drop-in
- **Mistake:** Restarting unrelated services “just in case” after a one-line co…

## Pros/Cons or Trade-offs
- **Pro:** Text and layered — local policy without forking the distro.
- **Con:** Many surfaces mean easy shadowing; undocumented edits become tribal knowledge.

## Comparison
- vs [[etc files]]: `/etc` is one major surface


### Use cases
- Raise `net.core.somaxconn` via `/etc/sysctl.d/99-local.conf`, apply with `sys…
