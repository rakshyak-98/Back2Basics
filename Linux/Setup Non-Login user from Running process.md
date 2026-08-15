[[user management]] [[process]] [[system service unit files]] [[services/systemd]] [[fresh system sudo setup]]

# Setup Non-Login user from Running process

> Service accounts should run daemons without login shells — create a system user, assign file ownership, and run the process under that UID via systemd.

## Interview Relevance
Hardening basics: least privilege, `nologin` shell, systemd `User=` — interviewers watch for “run everything as root” vs proper system users.

## Sources
- [useradd(8)](https://man7.org/linux/man-pages/man8/useradd.8.html) — deep-dive
- [systemd.service — User=](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html) — deep-dive

## Core Definition
A **system user** (`useradd --system`) gets a low UID, usually no home, and `/usr/sbin/nologin` (or `/bin/false`) so nobody can SSH in as that account. The running service drops to that UID via the unit file.

## Key Concepts
- **System vs human user:** System UIDs for daemons; no interactive login.
- **nologin shell:** Rejects interactive sessions; does not stop `sudo -u` execution.
- **Ownership:** Data dirs must match the service UID/GID or permission errors follow.
- **systemd User=/Group=:** Preferred over setuid hacks in the binary.
- **NoNewPrivileges / UMask:** Extra hardening knobs on the unit.

## Technical Details

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin myapp
id myapp

# Who runs this now?
ps -o user=,pid,cmd -p 1234

# Files owned by wrong user
sudo chown -R myapp:myapp /var/lib/myapp
```

```ini
[Service]
User=myapp
Group=myapp
UMask=0077
NoNewPrivileges=yes
```

## Real-World Applications
Migrating an app started as root in a screen session onto a proper systemd unit with a dedicated `myapp` user and locked-down `/var/lib/myapp`.

## Pros/Cons or Trade-offs
- **Pro:** Blast radius limited if the app is compromised; clearer audit trail.
- **Con:** Extra ownership/permission work on upgrades and shared sockets.
- **Trade-off:** Shared group for multi-process apps vs one UID per binary.

## Comparison
vs running as your login user: fine for dev, wrong for services. vs containers: still map to a non-root UID inside the image. See [[user management]].

## Mistakes to Avoid
- Creating a system user with `/bin/bash` “just in case.”
- Changing `User=` without `chown` on state directories.
- Using `usermod -G` without `-a` when adding supplementary groups later.
