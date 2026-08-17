[[user management]] [[useradd]] [[passwd]] [[usermod]] [[groupadd]] [[getent]]

# userdel

> Removes the account from passwd/shadow/group — home/mail only if `-r`; other files stay as numeric UID orphans.





## Interview Relevance
Offboarding depth: `-r` destructiveness, UID reuse, and that cron/systemd/user processes need manual cleanup.

## Sources
- [man userdel](https://man7.org/linux/man-pages/man8/userdel.8.html) — deep-dive
- [Wikipedia — userdel](https://en.wikipedia.org/wiki/Userdel) — overview

## Core Definition
`userdel` removes the account lines from `/etc/passwd`, `/etc/shadow`, and `/etc/group` (primary group if user-private). Files owned by the UID remain unless `-r` removes home and mail spool.

## Key Concepts
- **`-r`:** remove home + mail spool — irreversible without backup.
- **UID reuse hazard:** new user can inherit orphaned file ownership.
- **Running processes:** stop/kill the user first or deletion fails / stays messy.
- **Not full offboard:** cron, systemd user units, Docker volumes, cloud IAM keys need separate cleanup.

## Technical Details
```
userdel ──► /etc/passwd, shadow, group
     │
     └─ -r ──► /home/user, /var/mail/user (if exists)
```

| Flag | Effect |
|------|--------|
| `-r` | Remove home dir + mail spool |
| `-f` | Force even if logged in (dangerous) |
| (none) | Account gone; files become numeric orphans |

```bash
id username
ps -u username
crontab -u username -l 2>/dev/null
find / -uid $(id -u username) 2>/dev/null | head

sudo passwd -l username
sudo usermod -s /sbin/nologin username
sudo pkill -u username
sudo userdel -r username

sudo find /var/www /opt -user username -exec chown serviceaccount:serviceaccount {} +
getent passwd username
```

| Symptom | Check | Fix |
|---------|-------|-----|
| User currently used by process | `ps -u user` | Stop services; `pkill -u user` |
| Home not removed | Forgot `-r` | `rm -rf` after backup confirm |
| Numeric UID owners | Deleted without reassign | `find -uid` + `chown` |
| LDAP/SSSD user | Not local | Directory tools — wrong tool |

## Real-World Applications
Contractor offboarding on bastion hosts: lock → nologin → kill processes → reassign web files → `userdel -r`.

## Pros/Cons or Trade-offs
- **Pro:** Clean local account removal when you own the UID space.
- **Con:** Easy to leave orphans or reuse UIDs dangerously.

## Comparison
- vs temporary disable: `passwd -l` / `chage -E` without deleting.
- vs rename: [[usermod]] `-l` / `-d -m`, not delete-recreate.

## Mistakes to Avoid
- `-r` without archive on non-throwaway hosts.
- Deleting then letting the next hire reuse the UID over leftover files.
- `userdel -f` on an active database/app user with open files.
