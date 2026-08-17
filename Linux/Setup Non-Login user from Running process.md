[[user management]] [[process]] [[system service unit files]] [[services/systemd]] [[fresh system sudo setup]]

# Setup Non-Login user from Running process

> Service accounts should run daemons without login shells — create a system user, assign file ownership, and run the process under that UID via systemd.

```txt
        Setup Non-Login us ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Hardening basics: least privilege, `nologin` shell, systemd `User=`

## Sources
- [useradd(8)](https://man7.org/linux/man-pages/man8/useradd.8.html) — deep-dive
- [systemd.service — User=](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html) — deep-dive

## Key Concepts
- **Core:** A **system user** (`useradd --system`) gets a low UID, usually no home, and `…

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

## Mistakes to Avoid
- **Mistake:** Creating a system user with `/bin/bash` “just in case.”
- **Mistake:** Changing `User=` without `chown` on state directories
- **Mistake:** Using `usermod -G` without `-a` when adding supplementary groups…

## Pros/Cons or Trade-offs
- **Pro:** Blast radius limited if the app is compromised; clearer audit trail.
- **Con:** Extra ownership/permission work on upgrades and shared sockets.
- **Trade-off:** Shared group for multi-process apps vs one UID per binary.

## Comparison
- vs running as your login user: fine for dev, wrong for services


### Use cases
- Migrating an app started as root in a screen session onto a proper systemd un…
