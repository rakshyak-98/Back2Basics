[[Linux configuration]] [[etc files]] [[services/systemd]]

# NTP sync

> NTP synchronization keeps clock skew within bounds — TLS, Kerberos, and distributed logs break when hosts disagree on time.

Modern Debian/Ubuntu use **systemd-timesyncd**; servers may run **chrony** or **ntpd**. Cloud VMs should sync to hypervisor or metadata NTP.

## systemd-timesyncd

```bash
timedatectl status
timedatectl show-timesync --all
systemctl status systemd-timesyncd
```

`/etc/systemd/timesyncd.conf`:
```ini
[Time]
NTP=ntp.example.com
FallbackNTP=time.google.com
```

## chrony (common on servers)

```bash
chronyc tracking
chronyc sources -v
```

## Verify

```bash
date -u
timedatectl
# offset should be sub-millisecond for chrony when tracked
```

## Related

[[commands/date]] · [[services/systemd]]

## Sources

- [systemd-timesyncd(8)](https://www.freedesktop.org/software/systemd/man/latest/systemd-timesyncd.service.html)
- [chrony documentation](https://chrony-project.org/documentation.html)
