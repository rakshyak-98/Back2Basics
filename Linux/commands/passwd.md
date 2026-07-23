[[user management]] [[useradd]] [[userdel]] [[Authentication command]] [[chage]]

# passwd

> One-line: change or administratively control local **password hash** in `/etc/shadow` — not SSH keys, not LDAP; the gate for `su`/console/PAM password auth. **Kerrisk**.

## Mental model

`passwd` updates the encrypted password field in `/etc/shadow` (users can't read it; root can). PAM stacks (`/etc/pam.d/`) decide when password checks apply — SSH with `PasswordAuthentication no` never hits `passwd`'s verify path for remote login.

```
login attempt ──► PAM ──► /etc/shadow hash compare
                              ▲
                         passwd / chpasswd / usermod
```

| Actor | Command | Effect |
|-------|---------|--------|
| User | `passwd` | Change own password (needs current) |
| root | `passwd <user>` | Set password without knowing old |
| root | `passwd -l` | Lock (prepend `!` to hash — no password login) |
| root | `passwd -u` | Unlock |
| root | `passwd -e` | Force change at next login |
| root | `passwd -d` | Delete password (empty — often dangerous) |

Lock (`-l`) ≠ disable account — SSH keys may still work. Full disable → `usermod -L` + `usermod -s /sbin/nologin` or `chage -E 1`.

## Standard config / commands

```bash
# User changes own password
passwd

# Root sets/resets password (break-glass, new hire)
sudo passwd deploy

# Lock account — password auth fails; keys may still work
sudo passwd -l compromised_user

# Unlock after investigation
sudo passwd -u compromised_user

# Force password change on next login
sudo passwd -e contractor

# Bulk / scripting (no prompts)
echo 'user:NewSecurePass' | sudo chpasswd
sudo chpasswd <<< 'user:NewSecurePass'

# Password aging (better than -e for policy)
sudo chage -l username              # view policy
sudo chage -M 90 username           # max 90 days
sudo chage -W 14 username           # warn 14 days before
sudo chage -E 2026-12-31 username   # account expiry date

# Verify account state
sudo passwd -S username
# P = usable password  L = locked  NP = no password  PS = password set
getent shadow username | cut -d: -f1-2
```

**Hardening context** (see [[etc files]]):

```bash
# /etc/ssh/sshd_config — prefer keys, disable password SSH
PasswordAuthentication no
PermitRootLogin no
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| "Authentication failure" but password correct | Account locked; wrong PAM; LDAP vs local | `passwd -S user`; `getent passwd user`; check `/etc/nsswitch.conf` |
| User can't change password ("token manipulation") | `/etc/shadow` or disk full; read-only FS | `ls -l /etc/shadow`; `df -h /`; remount rw |
| Locked out after `-l` | Expected for passwords | `passwd -u` or restore from console/recovery |
| `-e` didn't force change | User uses SSH keys only | Keys bypass password expiry for SSH; use `chage -d 0` + key rotation policy |
| `passwd` works locally, not SSH | `PasswordAuthentication` / PAM | `sshd -T \| grep password`; `/etc/pam.d/sshd` |
| Weak password rejected | `pam_pwquality` / `libpam-pwquality` | Adjust `/etc/security/pwquality.conf` or use stronger password |

## Gotchas

> [!WARNING]
> **`passwd -l` locks password only** — SSH public keys, cron, and file ownership unchanged. Offboard with [[userdel]] or full account disable playbook.

> [!WARNING]
> **`chpasswd` in scripts logs to shell history** — use `chpasswd` with stdin from restricted file, not echo in shared history.

> [!WARNING]
> **Empty password (`passwd -d`)** — some PAM configs treat as "no password required". Never on production systems.

> [!WARNING]
> **NSS/LDAP/SSSD users** — local `passwd` may not apply; password lives in directory. Check `getent passwd user` source.

## When NOT to use

- **SSH key-only access** → manage `~/.ssh/authorized_keys`, not passwords.
- **Central identity (AD/Okta/LDAP)** → directory tools, not local `passwd`.
- **Service accounts** → `usermod -L` + nologin shell; no interactive password.
- **Secrets in apps** → vault/secrets manager, not Unix passwords.

## Related

[[user management]] [[useradd]] [[userdel]] [[usermod]] [[getent]] [[Authentication command]] [[etc files]]
