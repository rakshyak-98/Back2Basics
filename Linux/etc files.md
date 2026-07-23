[[Linux configuration]] [[Authentication command]] [[passwd]] [[systemd]] [[SSH]]

# /etc files

> One-line: **persistent system configuration** under `/etc` — the first place to look when behavior differs after reboot or between hosts. **FHS + distro overlays (cloud-init, Ansible).**

## Mental model

`/etc` holds config consumed by daemons at start (or reload). Runtime state lives in `/var` and `/run`; binaries in `/usr/bin`. Many daemons **overwrite** or **include** fragments — editing the wrong file or missing a `systemctl reload` leaves you thinking you changed something when the running process didn't.

```
Package install ──► /etc/default|/etc/sysconfig (defaults)
                 ──► /etc/<daemon>/main.conf
                 ──► /etc/<daemon>.d/*.conf (drop-ins)
systemd ──► /etc/systemd/system/*.service (overrides)
```

| Pattern | Example | Note |
|---------|---------|------|
| Main config | `/etc/ssh/sshd_config` | Single file |
| Drop-in dir | `/etc/ssh/sshd_config.d/` | Preferred on newer OpenSSH |
| Defaults | `/etc/default/grub` | Sourced by scripts, not daemon directly |
| systemd override | `/etc/systemd/system/nginx.service.d/` | `systemctl daemon-reload` after edit |

## Standard config / commands

**SSH hardening** (break-glass: keep console/session open while testing):

```bash
sudoedit /etc/ssh/sshd_config
# Or drop-in (cleaner):
sudoedit /etc/ssh/sshd_config.d/99-hardening.conf
```

```
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
AllowUsers deploy admin
```

```bash
sudo sshd -t                    # syntax test — always before reload
sudo systemctl reload sshd      # or restart if reload unsupported
```

**Resolver & hosts:**

```bash
cat /etc/resolv.conf            # DNS (may be stub from systemd-resolved)
cat /etc/nsswitch.conf          # passwd/files vs sss vs ldap
cat /etc/hosts                  # static overrides
resolvectl status               # modern DNS truth
```

**Identity:**

```bash
cat /etc/passwd                 # users (see [[getent]] for NSS truth)
cat /etc/group
sudo cat /etc/shadow            # password hashes — root only
cat /etc/sudoers                # use visudo, never raw vim
sudo visudo
```

**PAM (login stack):**

```bash
ls /etc/pam.d/
cat /etc/pam.d/sshd
cat /etc/pam.d/common-auth      # Debian
```

**sysctl (kernel tunables):**

```bash
sysctl -a | grep somaxconn
echo 'net.core.somaxconn = 4096' | sudo tee /etc/sysctl.d/99-app.conf
sudo sysctl --system
```

**Limits:**

```bash
cat /etc/security/limits.conf
# or /etc/security/limits.d/*.conf
ulimit -n                       # verify session
```

**Find what you changed:**

```bash
sudo grep -r 'PasswordAuthentication' /etc/ssh/
sudo diff -ru /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
dpkg-query -W -f='${Conffiles}\n' openssh-server   # package-owned conffiles
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Config edit ignored | Wrong file; drop-in override | `sshd -T`; `nginx -T`; check `.d/` dirs |
| Locked out of SSH | Syntax error; bad AllowUsers | Console/recovery; `sshd -t`; revert drop-in |
| DNS works in dig, not apps | `/etc/resolv.conf` stub | [[systemd]]-resolved; fix `nsswitch` |
| Service won't start | Typo in unit or main conf | `journalctl -u svc -b`; validate syntax |
| Reboot reverted change | Edited generator output | Edit source in `/etc/default`, Netplan, NM |
| Permission denied on secret | World-readable key | `chmod 600`; correct owner |

## Gotchas

> [!WARNING]
> **Cloud images regenerate files** — `/etc/hosts`, `/etc/resolv.conf`, `/etc/machine-id` may be managed. Edit cloud-init/Ansible source, not symptom file.

> [!WARNING]
> **`/etc` merge on package upgrade** — conffile prompts (dpkg) or `.rpmnew` (RHEL). Diff after upgrades.

> [!WARNING]
> **Never edit `/usr/lib/systemd/system/*.service` directly** — use `/etc/systemd/system/` overrides.

> [!WARNING]
> **`sudoers` syntax errors lock everyone out** — always `visudo` (locks + validates).

## When NOT to use

- **Runtime tuning without persistence** → `sysctl -w`, `ip route` — know they'll vanish.
- **Secrets in plain `/etc`** → prefer secret store, systemd `LoadCredential`, vault.
- **Application config in Docker** → image/env/volume strategy, not host `/etc` mix.

## Related

[[Linux configuration]] [[Authentication command]] [[passwd]] [[SSH]] [[systemd]] [[getent]] [[visudo]]
