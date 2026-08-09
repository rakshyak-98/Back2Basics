[[Linux]] [[useradd]] [[passwd]] [[login shell]] [[process]]

# Setup Non-Login user from Running process

> Turn a long-running process’s identity into a proper system user — stable UID, nologin shell, owned files — without leaving orphan UIDs.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** note UID/files of the process → create matching system user → `chown` → restart under that user (systemd `User=`).

```txt
PID ──► uid/gid, cwd, open files
  │
  ├─ useradd --system --uid N --home … --shell nologin
  ├─ chown -R user:group data/
  └─ systemd User= / restart
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **system user** | Low UID, no login | “`--system` + `nologin`.” |
| **UID match** | Keep numeric owner | “Avoid mass chown when possible.” |
| **nologin** | Block interactive shell | “SSH keys alone aren’t enough if shell is nologin.” |
| **User=** | systemd drop privilege | “Service runs as that user.” |
| **orphan UID** | Files with deleted user | “`find -nouser` after mistakes.” |

---

## Standard config / commands

```bash
pid=1234
ps -o user,uid,gid,cmd -p "$pid"
sudo ls -l /proc/$pid/cwd /proc/$pid/fd | head

sudo useradd --system --uid 12345 --home /var/lib/myapp \
  --shell /usr/sbin/nologin myapp
sudo mkdir -p /var/lib/myapp
sudo chown -R myapp:myapp /var/lib/myapp

# systemd drop-in
# [Service]
# User=myapp
# Group=myapp
sudo systemctl daemon-reload
sudo systemctl restart myapp
```

| Knob | Why it matters |
|------|----------------|
| Fixed UID | Match existing file owners |
| Home path | State directory, not `/home` |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Permission denied after switch | Paths still root-owned | `chown` data + logs + sockets |
| useradd UID in use | `getent passwd` | Pick free UID or keep old |
| Service starts as root | Unit missing User= | Drop-in + restart |
| Can’t debug interactively | nologin | `sudo -u myapp` with explicit shell |

---

## Gotchas

> [!WARNING]
> **Changing UID under a live process** is messy — stop, chown, start.

> [!WARNING]
> **Shared UIDs across hosts** — pick a reserved range and document it.

---

## When NOT to use

- **One-off root cron** — fix the job instead of inventing a user.
- **Containers** — use image USER + K8s runAsUser, not host useradd.

---

## Related

[[useradd]] [[usermod]] [[passwd]] [[system service unit files]] [[process]]
