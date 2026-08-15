[[Linux configuration]] [[file mount]] [[user management]] [[apt config]] [[Linux Templates Directory]] [[loggging]]

# etc files

> `/etc` holds host-local configuration — the authoritative text files operators edit (or template via configuration management) to define how this machine behaves.

## Interview Relevance
FHS literacy: know that `/etc` is admin config (not `/usr`), name high-traffic paths (`fstab`, `sshd_config`, `sudoers`), and describe safe edit/validate habits.

## Sources
- [Filesystem Hierarchy Standard — /etc](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html#etcOpt) — overview
- `man 5 hosts`, `man 5 fstab` — deep-dive

## Core Definition
Unlike `/usr` (vendor-shipped), **`/etc` is for local administrators**. Daemons read these files at start/reload; configuration management should own them rather than one-off drift.

## Key Concepts
- **Host-local authority:** This machine’s policy lives here.
- **conffiles:** Package managers merge upgrades carefully — see [[Linux Templates Directory]].
- **Validate then reload:** Prefer `sshd -t` / `nginx -t` before restart.
- **Generated files:** Some paths (often `resolv.conf`) are managed by NetworkManager or systemd-resolved — do not hand-edit blindly.

## Technical Details

| File / dir | Purpose |
|------------|---------|
| `/etc/fstab` | Filesystem mounts — [[file mount]] |
| `/etc/hosts` | Static name overrides |
| `/etc/resolv.conf` | DNS resolvers (may be managed) |
| `/etc/ssh/sshd_config` | SSH server |
| `/etc/sudoers` | sudo policy — use [[visudo]] |
| `/etc/passwd`, `/etc/shadow` | Users — [[user management]] |
| `/etc/systemd/system/` | Unit overrides — [[system service unit files]] |
| `/etc/apt/` | APT config — [[apt config]] |
| `/etc/environment` | PAM-wide environment |

```bash
sudo cp -a /etc/ssh/sshd_config{,.bak.$(date +%F)}
sudo sshd -t
sudo nginx -t
```

Do not hand-edit `/etc/ld.so.cache` — run `ldconfig`. Fix NetworkManager/resolved config instead of fighting a generated `resolv.conf`.

## Real-World Applications
Before opening SSH from a change window: back up `sshd_config`, run `sshd -t`, reload, and keep a console session open in case auth breaks.

## Pros/Cons or Trade-offs
- **Pro:** Human-readable, diffable, easy to template and audit.
- **Con:** Drift accumulates without configuration management; partial edits leave services in split-brain with drop-ins.

## Comparison
vs `/usr`: vendor defaults and binaries — upgrades overwrite. vs `/run`: runtime state, gone on reboot. vs [[Linux configuration]]: this note is the `/etc` surface; that note covers the full stack including sysctl and user dotfiles.

## Mistakes to Avoid
- Editing `/etc/sudoers` with plain vim instead of `visudo` (syntax error lockout risk).
- Changing `resolv.conf` that is a symlink managed by systemd-resolved.
- Editing vendor files under `/usr` “because the package put an example there.”
