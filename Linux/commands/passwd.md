[[user management]] [[useradd]] [[userdel]] [[usermod]] [[getent]] [[Authentication command]] [[etc files]]

# passwd

> Changes or locks the password hash in `/etc/shadow` — PAM decides when that hash is actually checked.

## Interview Relevance

Interviewers want lock vs disable, shadow vs keys, and that `passwd -l` does not stop SSH public-key login.

## Sources

- [man passwd](https://man7.org/linux/man-pages/man1/passwd.1.html) — deep-dive
- [Wikipedia — passwd](https://en.wikipedia.org/wiki/passwd) — overview

## Core Definition

`passwd` updates the encrypted password field in `/etc/shadow`. PAM stacks under `/etc/pam.d/` decide when password checks apply — SSH with `PasswordAuthentication no` never uses this path for remote login.

## Key Concepts

- **User vs root:** user needs the current password; root can set without knowing the old one.
- **Lock (`-l`):** prepends `!` to the hash — password auth fails; keys may still work.
- **Expire (`-e` / `chage`):** force change at next password login — keys can bypass.
- **NSS/LDAP:** local `passwd` may not apply when identity lives in a directory.

## Technical Details

```
login attempt ──► PAM ──► /etc/shadow hash compare
                              ▲
                         passwd / chpasswd / usermod
```

| Actor | Command | Effect |
|-------|---------|--------|
| User | `passwd` | Change own password (needs current) |
| root | `passwd <user>` | Set password without knowing old |
| root | `passwd -l` | Lock hash — no password login |
| root | `passwd -u` | Unlock |
| root | `passwd -e` | Force change at next login |
| root | `passwd -d` | Delete password (often dangerous) |

```bash
passwd
sudo passwd deploy
sudo passwd -l compromised_user
sudo passwd -u compromised_user
sudo passwd -e contractor
echo 'user:NewSecurePass' | sudo chpasswd
sudo chage -l username
sudo chage -M 90 username
sudo chage -W 14 username
sudo chage -E 2026-12-31 username
sudo passwd -S username
getent shadow username | cut -d: -f1-2
```

`passwd -S`: `P` usable, `L` locked, `NP` no password.

| Symptom | Check | Fix |
|---------|-------|-----|
| Auth failure, password correct | Locked; wrong PAM; LDAP vs local | `passwd -S`; `getent passwd`; `nsswitch.conf` |
| Token manipulation error | `/etc/shadow` or disk full; read-only FS | `ls -l /etc/shadow`; `df -h /`; remount rw |
| `-e` did not force change | User uses SSH keys only | Key rotation policy; `chage` alone is not enough |
| Works locally, not SSH | `PasswordAuthentication` / PAM | `sshd -T`; `/etc/pam.d/sshd` |

## Real-World Applications

Break-glass password reset, locking a compromised interactive account, and password aging with `chage` for contractors.

**Example:** Offboard with more than `passwd -l` — combine lock, nologin shell, and key removal ([[userdel]] / disable playbook).

## Pros/Cons or Trade-offs

- **Pro:** Simple local credential control for break-glass and small fleets.
- **Con:** Wrong tool for central identity (AD/Okta/LDAP) and for SSH key-only hosts.

## Comparison

- vs [[usermod]] `-L` / nologin: fuller account disable than password lock alone.
- vs [[getent]]: query resolved account data across NSS sources before changing local shadow.

## Mistakes to Avoid

- Treating `passwd -l` as full disable — SSH keys, cron, and ownership remain.
- Putting passwords on the shell history line with `echo | chpasswd` on shared hosts.
- Using `passwd -d` (empty password) on production systems.
- Running local `passwd` against directory-backed users without checking `getent`.
