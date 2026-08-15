[[user management]] [[linux groups]] [[usermod]] [[useradd]] [[getent]] [[passwd]]

# groupadd

> groupadd creates a Unix group (name + GID) — it does not add members; file permissions and sudo/docker access hang off group membership.

## Interview Relevance
Shows you know GID vs membership, `-r` system groups, and the classic `usermod -G` without `-a` lockout.

## Sources
- [groupadd(8)](https://man7.org/linux/man-pages/man8/groupadd.8.html) — deep-dive
- [group(5)](https://man7.org/linux/man-pages/man5/group.5.html) — overview

## Core Definition
Groups are numeric **GID** + name mappings. File permissions use UID for owner, GID for group (`ls -l` third column). Users join via primary group (`useradd`) or supplementary groups (`usermod -aG`). `groupadd` only creates the group.

## Key Concepts
- **Primary vs supplementary:** One primary GID; many secondary groups.
- **System groups (`-r`):** Low GID range for daemons.
- **Explicit GID (`-g`):** Needed for NFS / multi-host consistency.
- **Session cache:** New membership applies after re-login / `newgrp`.
- **/etc/group:** Local membership; LDAP/SSSD may shadow via NSS.

## Technical Details

```txt
groupadd devops ──► /etc/group: devops:x:1005:
usermod -aG devops alice ──► alice in supplementary groups
```

```bash
sudo groupadd deploy
sudo groupadd -r myapp
sudo groupadd -g 1005 shared-data

sudo usermod -aG deploy alice          # -a append; without -a replaces!
sudo gpasswd -a alice deploy

getent group deploy
id alice
groups alice

sudo chgrp deploy /var/www/app
sudo chmod 2775 /var/www/app            # setgid

sudo groupdel oldproject
```

| Group | Typical purpose |
|-------|-----------------|
| `sudo` / `wheel` | Elevated privileges via sudoers |
| `docker` | Docker socket access without root |
| `adm` | Read `/var/log` |
| `www-data` | Web server file ownership |

| Symptom | Check | Fix |
|---------|-------|-----|
| group already exists | `getent group name` | Use existing or new name |
| GID already in use | `getent group <gid>` | Choose free GID |
| User not in group after add | Session cached | Re-login; `newgrp`; verify `id` |
| `usermod -G` wiped groups | Forgot `-a` | Restore; always `-aG` |

## Real-World Applications
Shared deploy directories with setgid `2775`, and granting `docker`/`sudo` without making every operator root.

## Pros/Cons or Trade-offs
- **Pro:** Simple DAC sharing model on one host.
- **Con:** GID collisions across hosts; session lag; easy to wipe groups with `-G`.
- **Trade-off:** Unix groups vs ACLs (`setfacl`) for complex sharing.

## Comparison
vs [[useradd]]: creates users (with a primary group). vs [[linux groups]]: conceptual membership model. vs cloud IAM: different identity plane.

## Mistakes to Avoid
- `usermod -G` without `-a` (drops `sudo`/`docker`).
- Expecting open SSH sessions to pick up new groups immediately.
- Creating local groups that shadow LDAP/SSSD names without checking `getent`.
