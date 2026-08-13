[[Linux]] [[useradd]] [[usermod]] [[userdel]] [[passwd]] [[linux groups]] [[visudo]] [[getent]] [[chage]]

# user management

> Linux user management is accounts + groups + sudo — who can log in, own files, and elevate.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Files that define a user]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** UIDs in passwd, secrets in shadow, membership in group, elevation in sudoers — humans usually UID ≥1000.

```txt
identity  /etc/passwd   name:x:UID:GID:gecos:home:shell
secrets   /etc/shadow   name:hash:aging fields…
groups    /etc/group    name:x:GID:members
elevate   /etc/sudoers(+.d)   via [[visudo]]
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **UID ≥1000** | Normal login users (typical) | “System accounts sit below; don’t recycle UIDs casually.” |
| **`x` in passwd** | Password lives in shadow | “World-readable passwd, root-only shadow.” |
| **`!` / `*` in shadow** | Locked / no password | “Service accounts shouldn’t have a login password.” |
| **nologin / false** | Non-interactive shell | “Daemons don’t get a bash.” |
| **`-aG`** | Append supplementary groups | “Without `-a` you wipe group membership.” |

---

## Standard config / commands

```bash
whoami
id
getent passwd alice
getent group sudo

# Create admin-ish user (Ubuntu)
sudo adduser devopsuser
sudo usermod -aG sudo devopsuser
# or primitives:
sudo useradd -m -s /bin/bash admin1
sudo passwd admin1
sudo usermod -aG sudo admin1

# Lifecycle
sudo passwd -l alice          # lock
sudo passwd -u alice          # unlock
sudo chage -l alice           # aging
sudo userdel -r alice         # remove home too

# Permissions reminder
# u=owner  g=group  o=others   — chmod/chown
```

Useful groups: `sudo` (administrator), `docker`, `adm` (logs), `plugdev`, `lpadmin`.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Auth fails after create | No password / locked | `passwd`; check shadow `!` |
| sudo denied | Groups + sudoers | `id`; `sudo -l`; [[visudo]] |
| Permission on shared dir | Primary vs supplementary | Shared group + `chmod g+s` or ACLs |
| Orphan files after delete | Forgot migration | `find / -user UID`; change ownership first |
| Can’t SSH | Shell nologin / no home | `usermod -s`; create home |

---

## Files that define a user

| File | Holds |
|------|-------|
| `/etc/passwd` | Login name, UID, primary GID, home, shell |
| `/etc/shadow` | Password hash, aging, lock flags |
| `/etc/group` | Group names, GIDs, supplementary members |
| `/etc/gshadow` | Group passwords/admins (rare day-to-day) |
| `/etc/shells` | Legal login shells |
| `/etc/skel` | Template for new homes |

Shells: `/bin/bash` for humans; `/usr/sbin/nologin` or `/bin/false` for system users.

---

## Gotchas

> [!WARNING]
> **`usermod -G` without `-a` resets supplementary groups** — instant loss of `sudo`/`docker`.

> [!WARNING]
> **Deleting a user without `-r` leaves a home full of private data** — and UIDs may be reused later.

> [!WARNING]
> **UID reuse** — new user inheriting old UID owns leftover files. Prefer never reuse in short windows.

---

## When NOT to use

- **Central IdP** — use SSSD/LDAP; keep local root break-glass only.
- **application tenancy** — application users ≠ `/etc/passwd` rows.
- **Containers** — prefer numeric USER in image; don’t manage host users per pod.

---

## Related

[[useradd]] [[usermod]] [[userdel]] [[passwd]] [[linux groups]] [[visudo]] [[getent]] [[chage]] [[Linux]]
