[[user management]] [[linux groups]] [[usermod]] [[useradd]] [[getent]]

# groupadd

> One-line: create a new **group** entry in `/etc/group` (and `/etc/gshadow` if shadow groups enabled) — shared permissions, sudo rules, and service ACLs. **Kerrisk**.

## Mental model

Groups are numeric **GID** + name mappings. File permissions use UID for owner, GID for group (`ls -l` third column). Users gain group membership via primary group (set at `useradd`) or secondary groups (`usermod -aG`). `groupadd` only creates the group — it does not add members.

```
groupadd devops ──► /etc/group: devops:x:1005:
                         │
usermod -aG devops alice ──► alice in supplementary groups
```

| Command | Purpose |
|---------|---------|
| `groupadd name` | New group, GID auto from `/etc/login.defs` |
| `groupadd -g 1005 name` | Explicit GID (match NFS/LDAP) |
| `groupadd -r name` | System group (low GID range) |
| `groupmod -n new old` | Rename |
| `groupdel name` | Delete (must have no members as primary) |
| `gpasswd -a user group` | Add member |
| `gpasswd -d user group` | Remove member |

## Standard config / commands

```bash
# Create application group
sudo groupadd deploy

# System group for a daemon (GID < 1000 typically)
sudo groupadd -r myapp

# Fixed GID — NFS, cross-host consistency
sudo groupadd -g 1005 shared-data

# Add users
sudo usermod -aG deploy alice          # -a append; without -a replaces groups!
sudo gpasswd -a alice deploy

# Verify
getent group deploy
id alice
groups alice

# Set directory setgid so new files inherit group
sudo chgrp deploy /var/www/app
sudo chmod 2775 /var/www/app            # 2 = setgid

# Delete empty group
sudo groupdel oldproject
```

**Common production groups:**

| Group | Typical purpose |
|-------|-----------------|
| `sudo` / `wheel` | Elevated privileges via sudoers |
| `docker` | Docker socket access without root |
| `adm` | Read `/var/log` |
| `www-data` | Web server file ownership |

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| "group already exists" | `getent group name` | Use existing or pick new name |
| "GID already in use" | `getent group <gid>` | Choose free GID: `grep : /etc/group \| cut -d: -f3 \| sort -n` |
| User not in group after add | Session cached | Re-login; `newgrp deploy`; verify `id` |
| `usermod -G` wiped other groups | Forgot `-a` | Restore from backup; `usermod -aG g1,g2,user` |
| Permission denied on setgid dir | Wrong group / no membership | `ls -ld`; add user to group |
| `groupdel` fails | Primary group of user | Change user's primary group first |

## Gotchas

> [!WARNING]
> **`usermod -G` without `-a` replaces all supplementary groups** — classic lock-out from `sudo`/`docker`. Always `-aG`.

> [!WARNING]
> **Group membership is per-login-session** — adding user to group does not affect open SSH sessions until reconnect or `newgrp`.

> [!WARNING]
> **GID conflicts across hosts** — NFSv4/NFSv3 squash and shared volumes need consistent GIDs. Document GID map.

> [!WARNING]
> **`groupadd` on LDAP/SSSD systems** — may create local group shadowing directory group. Check `getent group`.

## When NOT to use

- **One-off file share for two users** → ACLs (`setfacl`) or project directories with setgid.
- **Cloud IAM** → AWS/GCP roles, not Unix groups.
- **Rename** → `groupmod -n`, not delete + add (breaks ownership).

## Related

[[user management]] [[linux groups]] [[usermod]] [[useradd]] [[getent]] [[passwd]]
