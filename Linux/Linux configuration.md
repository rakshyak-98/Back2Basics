[[etc files]] [[apt config]] [[terminal config]] [[editor config]] [[Linux Templates Directory]] [[system service unit files]] [[management/grub]] [[management/Linux system management]]

# Linux configuration

> Linux configuration is the sum of `/etc`, per-user dotfiles, kernel boot parameters, and systemd units that define how this host behaves.





## Interview Relevance
Senior ops signal: know which layer wins (image → distro defaults → `/etc` → `$HOME` → `/run`), prefer drop-ins over editing vendor files, and verify with read-back (`systemctl cat`, `sysctl`, `nginx -T`).

## Sources
- [FHS 3.0](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html) — overview
- [systemd.unit(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html) — deep-dive

## Core Definition
Layers stack: **image/CM baseline** → **distribution defaults** in `/usr` → **local overrides** in `/etc` and `/home` → **runtime** (`/run`). Debug “my change did nothing” by finding which layer actually won.

## Recall Cues
- Why do interviewers care about Senior ops signal: know which layer wins (image → distro defaults → `/etc` → `$HOME` → `/run`), prefer drop-ins over editing vendor files, and verify with read-back (`systemctl cat`, `sysctl`, `nginx -T`)?
- What is step 1: One change at a time; note rollback path?
- What is step 2: Prefer drop-in overrides over editing vendor files?
- What is step 3: Reload or restart only the affected daemon?
- What is step 4: Verify with read-back (`nginx -T`, `sshd -t`)?
- What mistake is **Editing `/usr/lib/systemd/system/*.service` and losing changes on package upgrade**?
- What mistake is **Changing a file that is overridden by a higher-priority drop-in**?
- What mistake is **Restarting unrelated services “just in case” after a one-line config tweak**?

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

Change discipline:
1. One change at a time; note rollback path.
2. Prefer drop-in overrides over editing vendor files.
3. Reload or restart only the affected daemon.
4. Verify with read-back (`nginx -T`, `sshd -t`).

## Mistakes to Avoid
- Editing `/usr/lib/systemd/system/*.service` and losing changes on package upgrade.
- Changing a file that is overridden by a higher-priority drop-in.
- Restarting unrelated services “just in case” after a one-line config tweak.

## Comparison
vs [[etc files]]: `/etc` is one major surface; this note is the whole stack. vs containers: image layers + runtime mounts play a similar “who wins” game. vs [[Linux Templates Directory]]: templates are vendor starting points; configuration is what you actually apply.

## Real-World Applications
Raise `net.core.somaxconn` via `/etc/sysctl.d/99-local.conf`, apply with `sysctl --system`, confirm with `sysctl net.core.somaxconn`, and leave the package’s defaults untouched.

## Pros/Cons or Trade-offs
- **Pro:** Text and layered — local policy without forking the distro.
- **Con:** Many surfaces mean easy shadowing; undocumented edits become tribal knowledge.
