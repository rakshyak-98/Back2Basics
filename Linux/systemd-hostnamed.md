[[services/systemd]] [[Linux configuration]]

# systemd-hostnamed

> `systemd-hostnamed` is a D-Bus service that sets transient hostname, static hostname, and icon/chassis metadata — `hostnamectl` is the CLI front end.

## Commands

```bash
hostnamectl status
sudo hostnamectl set-hostname app01.example.com
sudo hostnamectl set-hostname app01 --static
sudo hostnamectl set-hostname edge --transient
```

## Files involved

| Source | File |
|--------|------|
| Static | `/etc/hostname` |
| Pretty | `/etc/machine-info` (`PRETTY_HOSTNAME`) |
| Transient | kernel hostname (until reboot) |

## Service

```bash
systemctl status systemd-hostnamed
busctl introspect org.freedesktop.hostname1
```

## Related

[[services/D-Bus]] · [[commands/busctl]] · [[etc files]]

## Sources

- [hostnamectl(1)](https://www.freedesktop.org/software/systemd/man/latest/hostnamectl.html)
- [org.freedesktop.hostname1](https://www.freedesktop.org/software/systemd/man/latest/org.freedesktop.hostname1.html)
