[[user management]] [[useradd]] [[passwd]] [[usermod]] [[groupadd]]

# userdel

> One-line: remove a local user account from `/etc/passwd` and optionally home + mail spool — offboarding and cleanup; irreversible without backups. **Kerrisk**.

## Mental model

`userdel` removes the account line from `/etc/passwd`, `/etc/shadow`, and `/etc/group` (primary group entry if it was user-private). Files owned by the UID **remain on disk** unless `-r` removes the home directory and mail spool — everything else (cron, systemd user units, `/var/spool/cron`, processes) needs manual cleanup.

```
userdel ──► /etc/passwd, shadow, group
     │
     └─ -r ──► /home/user, /var/mail/user (if exists)
```

| Flag | Effect |
|------|--------|
| `-r` | Remove home dir + mail spool |
| `-f` | Force removal even if user logged in (dangerous) |
| (none) | Account gone; files owned by old UID become numeric orphan |

## Standard config / commands

```bash
# Safe offboarding checklist (run as root)
id username                         # confirm UID/GID, groups
ps -u username                      # any running processes?
crontab -u username -l 2>/dev/null  # cron jobs?
find / -uid $(id -u username) 2>/dev/null | head   # orphaned files preview

# Standard removal with home
sudo userdel -r username

# Account only — keep home for forensic / handover
sudo userdel username

# Force (user still logged in — kicks on next action, risky)
sudo userdel -rf username

# Reassign orphaned files before delete (preferred on shared servers)
sudo find /var/www /opt -user username -exec chown serviceaccount:serviceaccount {} +
sudo userdel -r username

# Verify gone
getent passwd username              # should return nothing
grep username /etc/group            # secondary group memberships cleaned
```

**Pre-delete lock (recommended sequence):**

```bash
sudo passwd -l username             # block password login
sudo usermod -s /sbin/nologin username
sudo pkill -u username              # stop processes
sudo userdel -r username
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| "user is currently used by process" | `ps -u user` | Stop services; `pkill -u user`; then retry |
| "cannot remove entry in /etc/passwd" | User logged in on TTY | `who`; `pkill -KILL -u user` last resort |
| Home not removed | Forgot `-r` | `rm -rf /home/user` after backup confirm |
| Files show numeric UID owner | Deleted without reassign | `find -uid <old_uid>` + `chown` |
| User still in groups | Secondary memberships | `gpasswd -d user group` or edit `/etc/group` |
| LDAP/SSSD user | Not a local account | Remove from directory; `userdel` wrong tool |

## Gotchas

> [!WARNING]
> **`-r` is destructive** — no trash can. Snapshot or archive `/home/user` before delete on any non-throwaway host.

> [!WARNING]
> **UID reuse** — deleted UID reassigned to new user inherits orphaned file ownership. Reassign or delete files first.

> [!WARNING]
> **`userdel -f` on active DB/app user** — open files keep running; new user with same name gets wrong UID mapping in long-lived processes.

> [!WARNING]
> **Mail spool only** — `-r` does not purge `/var/spool/cron`, `~/.config/systemd/user`, docker volumes, or cloud IAM keys tied to that human.

## When NOT to use

- **Temporary disable** → `passwd -l`, `usermod -L`, `chage -E 1`.
- **Directory (LDAP/AD) accounts** → idm/directory admin tools.
- **Rename user** → `usermod -l newname -d /home/newname -m`.
- **Merge two accounts** → `chown` file migration, not delete-recreate.

## Related

[[user management]] [[useradd]] [[passwd]] [[usermod]] [[groupadd]] [[getent]]
