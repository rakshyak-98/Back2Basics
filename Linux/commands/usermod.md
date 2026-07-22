[[useradd]] [[userdel]] [[passwd]] [[getent]] [[user management]] [[etc files]]

# usermod

> One-line: **mutate existing POSIX accounts** — shell, home, groups, login name. Always verify with `getent`; `/etc/passwd` alone lies when LDAP/sssd is in play.

## Mental model

`usermod` edits `/etc/passwd`, `/etc/shadow`, `/etc/group` (and gshadow) **for local accounts**. Changes to groups need `-aG` (append); bare `-G` **replaces** the supplementary group list. Active sessions keep old UID/GID until re-login.

```
usermod → /etc/passwd + shadow + group
Running process → still old UID until restart
NSS (sssd/LDAP) → usermod may not apply — use directory tools
```

| Flag | Effect | Risk |
|------|--------|------|
| `-s SHELL` | Login shell | Lock user if shell invalid |
| `-l NEW` | Rename login | Update home references, cron, mail |
| `-d DIR -m` | Home + move files | `-m` required to move existing home |
| `-g GROUP` | Primary group | Must exist (`groupadd`) |
| `-aG GROUP` | Append supplementary | **Safe** add to sudo/docker/etc |
| `-G g1,g2` | **Replace** all supp groups | Drops sudo if forgotten |
| `-L` / `-U` | Lock/unlock password | PAM still applies |

## Standard config / commands

```bash
# Interactive shell for service account
sudo usermod -s /bin/bash deploy

# Add to groups (append — production default)
sudo usermod -aG docker,sudo alice
id alice
groups alice

# Change primary group (new files inherit this GID)
sudo usermod -g developers alice

# Relocate home
sudo usermod -d /home/alice-new -m alice
# -m moves contents; fix systemd user units referencing old path

# Rename account
sudo usermod -l alice_new alice_old
sudo usermod -d /home/alice_new -m alice_new
# Update crontab, ssh AuthorizedKeys path comments, file ownership if needed

# Lock compromised account
sudo usermod -L compromised
sudo passwd -l compromised   # redundant with -L for password auth

# Verify truth (NSS)
getent passwd alice
getent group docker
```

**After group change:** user must **log out fully** (or `newgrp docker` for one shell) for supplementary groups to apply.

**Bulk ownership after UID change** (rare, dangerous):

```bash
# Only when UID intentionally changed — verify before running
sudo find / -uid OLD_UID -exec chown NEW_UID {} \; 2>/dev/null
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| "not in docker group" after usermod | `id` vs `id deploy` | Re-login; `-aG` not `-G`; verify `getent group docker` |
| Lost sudo | `groups user` | `usermod -aG sudo user`; was wiped by `-G` only |
| Can't login | `getent passwd`; shell path | `usermod -s /bin/bash`; nologin mistake |
| Home still old path | `grep alice /etc/passwd` | `-d` without `-m`; manual rsync + edit passwd |
| usermod: user in use | `who`; process list | Log out user; `-f` force (disruptive) |
| Change ignored | sssd/LDAP | Modify directory; local usermod wrong tool |

## Gotchas

> [!WARNING]
> **`usermod -G docker` without `-a`** — removes user from all other supplementary groups. Always `-aG`.

> [!WARNING]
> **Rename without `-m`** — home dir name mismatch; apps hardcode `/home/oldname`.

- **Running daemons** — User systemd services, cron, and long-lived workers keep old credentials until restarted.
- **NFS/SMB ownership** — UID mapping on NAS may not match local usermod.

## When NOT to use

- **LDAP/AD/FreeIPA accounts** — use `ipa user-mod`, `admod`, or vendor console.
- **Creating users** — [[useradd]] first; usermod is for mutation.
- **Temporary access** — prefer expiry on [[useradd]] or IAM-style keys with rotation.

## Related

[[useradd]] [[userdel]] [[passwd]] [[getent]] [[user management]] [[etc files]] [[linux groups]]
