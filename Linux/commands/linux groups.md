[[Commands]] [[user management]] [[useradd]] [[groupadd]] [[getent]] [[visudo]] [[passwd]]

# linux groups

> Groups bundle users for shared file access and sudo — one primary GID plus optional supplementary memberships.

```txt
        linux groups ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Expect primary vs supplementary, `usermod -aG`, session refresh, and why `get…

## Sources
- [group(5)](https://man7.org/linux/man-pages/man5/group.5.html) — deep-dive
- [credentials(7)](https://man7.org/linux/man-pages/man7/credentials.7.html) — overview

## Key Concepts
- **Primary GID:** Default group for new files.
- **Supplementary:** Extra groups (`docker`, `sudo`, `adm`) without changing primary.
- **`usermod -aG`:** Append — `-G` alone replaces the whole set.
- **Session credentials:** Group changes apply after re-login / `newgrp` / service restart.
- **No nested groups:** Linux groups don’t contain groups.


- **Core:** `/etc/passwd` stores each user’s **primary GID**

## Technical Details
```txt
/etc/passwd  → user:…:UID:GID:…     (primary)
/etc/group   → group:…:GID:u1,u2    (supplementary members)
```

```bash
id
id alice
groups alice
getent group docker

sudo groupadd developers
sudo usermod -aG developers alice
sudo gpasswd -a alice developers
sudo gpasswd -d alice developers
newgrp developers
```

| Phrase | Same action |
|--------|-------------|
| “Add group to user” | `usermod -aG group user` |
| “Add user to group” | `usermod -aG group user` / `gpasswd -a user group` |

| Symptom | Check | Fix |
|---------|-------|-----|
| In group but access denied | `id` in *this* session | Re-login / `newgrp`; restart daemons |
| Lost other groups | `-G` without `-a` | Restore with `-aG` list |
| `getent group` missing user | Primary-only membership | Check `id -gn` / `getent passwd` |
| File group wrong | Primary vs setgid dir | `chgrp`; `chmod g+s` on shared dirs |

## Mistakes to Avoid
- **Mistake:** `usermod -G` without `-a`
- **Mistake:** Expecting running daemons to pick up new groups without restart
- **Mistake:** Assuming `getent group` lists every user with that primary GID

## Pros/Cons or Trade-offs
- **Pro:** Simple shared access model on one host.
- **Con:** Session lag; no nesting; easy wipe with `-G`.
- **Trade-off:** Groups vs ACLs for fine-grained exceptions.

## Comparison
- vs [[groupadd]]: creates the group object


### Use cases
- Granting `docker` socket access, shared project dirs with setgid, and sudo vi…
