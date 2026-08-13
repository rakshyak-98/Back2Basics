[[user management]] [[process]] [[system service unit files]]

# Setup Non-Login user from Running process

> Service accounts should run daemons without login shells — create a system user, assign file ownership, and run the process under that UID via systemd.

## Create system user

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin myapp
id myapp
```

`--system` allocates UID in system range; `/usr/sbin/nologin` prevents interactive login.

## From existing process

```bash
# Who runs this now?
ps -o user=,pid,cmd -p 1234

# Files owned by wrong user
sudo chown -R myapp:myapp /var/lib/myapp
```

## systemd unit

```ini
[Service]
User=myapp
Group=myapp
UMask=0077
NoNewPrivileges=yes
```

## Related

[[user management]] · [[fresh system sudo setup]] · [[services/systemd]]

## Sources

- `man 8 useradd`
- [systemd.service — User=](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html)
