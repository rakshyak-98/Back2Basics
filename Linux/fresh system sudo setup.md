[[user management]] [[SSH]] [[Linux configuration]]

# Fresh system sudo setup

> One-line: **bootstrap a non-root admin safely** — sudo group, key-based SSH, visudo edits, and recovery paths before you lock yourself out. **First-boot checklist for VPS/bare metal.**

## Mental model

```
Install ──► create admin user ──► SSH key auth ──► verify sudo ──► harden sshd ──► disable root password login
                  │                                      │
                  └── never edit sudoers with plain editor ──► always visudo
```

| Group | Distro | Sudo access |
|-------|--------|-------------|
| `sudo` | Debian, Ubuntu | `%sudo ALL=(ALL:ALL) ALL` |
| `wheel` | RHEL, Fedora, Arch | `%wheel ALL=(ALL) ALL` |

Root should remain for break-glass; daily work as unprivileged user + `sudo`.

## Standard config / commands

**1. Create admin user (Ubuntu/Debian example):**

```bash
# As root on first login
adduser deploy
usermod -aG sudo deploy
id deploy   # groups must include sudo

# RHEL/Fedora
# useradd -m -G wheel deploy
```

**2. SSH key before touching passwords:**

```bash
# On your laptop — key first, password second
ssh-copy-id deploy@server
ssh deploy@server 'sudo -n true' 2>/dev/null || ssh deploy@server 'sudo true'  # verify sudo

# Server: ensure pubkey auth works BEFORE:
# PasswordAuthentication no
```

**3. visudo — the only safe editor for sudoers:**

```bash
sudo visudo                    # validates syntax before commit
sudo visudo -f /etc/sudoers.d/deploy   # drop-in fragment (preferred)

# Standard drop-in: full sudo for deploy group member
# /etc/sudoers.d/deploy
deploy ALL=(ALL:ALL) ALL
```

**4. NOPASSWD (use sparingly):**

```bash
# CI/automation only — document why
deploy ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart myapp
# NEVER: deploy ALL=(ALL) NOPASSWD: ALL   # equals root without audit trail
```

**5. Harden sshd (after key login verified):**

```bash
# /etc/ssh/sshd_config.d/99-hardening.conf
PermitRootLogin prohibit-password   # or no after admin confirmed
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3

sudo sshd -t && sudo systemctl reload sshd
# Keep current session open; open NEW terminal to test
```

**6. sudo logging (audit):**

```bash
# Defaults logfile=/var/log/sudo.log in sudoers (distro-dependent)
grep sudo /var/log/auth.log
journalctl _COMM=sudo
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `deploy is not in the sudoers file` | `groups deploy`; `getent group sudo` | Boot single-user/recovery; `usermod -aG sudo deploy` as root |
| `visudo` syntax error, sudo dead | `pkexec visudo` or recovery console | Fix line visudo flagged; never leave broken sudoers |
| Locked out after `PasswordAuthentication no` | Console/VNC/provider recovery | Mount disk; fix `sshd_config`; or inject key into `~deploy/.ssh/authorized_keys` |
| NOPASSWD stopped prompting but CI fails | `sudo -l -U deploy` | Command path must match **exact** binary in rule |
| `sudo: unable to resolve host` | `/etc/hosts` has `127.0.1.1 hostname` | Fix hostname mapping — annoyance, sometimes breaks scripts |
| Every sudo asks password in automation | Missing NOPASSWD for scoped cmd | Narrow NOPASSWD to required commands only |

**Lockout recovery (cloud VPS pattern):**

1. Provider **serial console / rescue mode** → mount root FS.
2. `chroot /mnt` or edit mounted `etc/sudoers.d/*`.
3. Re-enable `PasswordAuthentication yes` temporarily **or** paste pubkey into admin `authorized_keys`.
4. Reboot; fix properly; re-harden.

**Recovery checklist:**

```bash
# Rescue shell as root
mount /dev/sda1 /mnt
echo 'deploy ALL=(ALL:ALL) ALL' >> /mnt/etc/sudoers.d/deploy
chmod 440 /mnt/etc/sudoers.d/deploy
# Or reset sshd
sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /mnt/etc/ssh/sshd_config.d/*.conf
```

## Gotchas

> [!WARNING]
> **Order matters:** SSH key verified → then disable password auth. Reversing the order is the #1 fresh-VPS lockout.

> [!WARNING]
> **`chmod 777 /etc/sudoers`** or editing with `nano` without `visudo` — one typo disables **all** sudo.

- **`sudo` group empty on minimal images** — cloud images often ship root-only; create user before disconnecting root session.
- **Two sessions rule:** keep one root/ssh session open while reloading sshd.
- **`Defaults secure_path`** — scripts using `sudo cmd` may not see your custom `/usr/local/bin`; use full paths in sudoers.
- **Wheel on Debian** — group may exist but not be in sudoers unless configured; use `sudo` group on Ubuntu.

## When NOT to use

- **Shared developer laptops** — NOPASSWD ALL for convenience trades away sudo audit and password second factor.
- **Production app runtime as sudo user** — services get dedicated users, no shell, no sudo ([[Setup Non-Login user from Running process]]).
- **Disabling root entirely before testing admin** — always validate `deploy` sudo in a second session first.

## Related

[[user management]] [[SSH]] [[Linux configuration]] [[Commands]]
