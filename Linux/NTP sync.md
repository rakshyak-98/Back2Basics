[[Linux configuration]] [[etc files]] [[services/systemd]] [[date]]

# NTP sync

> NTP (Network Time Protocol) keeps host clocks close enough that TLS, Kerberos, and distributed logs stay trustworthy.

```txt
        NTP sync ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Shows you know clock skew breaks auth and debugging, can name `systemd-timesy…

## Sources
- [systemd-timesyncd.service](https://www.freedesktop.org/software/systemd/man/latest/systemd-timesyncd.service.html) — deep-dive
- [chrony documentation](https://chrony-project.org/documentation.html) — deep-dive
- [RFC 5905 — NTPv4](https://www.rfc-editor.org/rfc/rfc5905) — overview

## Key Concepts
- **Skew vs drift:** Skew is current offset; drift is how fast the clock runs wrong.
- **systemd-timesyncd:** Lightweight SNTP client common on desktops and small VMs.
- **chrony:** Preferred on servers
- **Step vs slew:** Large offsets may jump (step); small ones adjust gradually (slew).
- **Trust:** Wrong NTP source is as bad as no sync for Kerberos/TLS validity windows.


- **Core:** Clients poll trusted time sources and gradually steer the local clock. Cloud …

## Technical Details
```bash
timedatectl status
timedatectl show-timesync --all
systemctl status systemd-timesyncd

chronyc tracking
chronyc sources -v

date -u
timedatectl
```

- `/etc/systemd/timesyncd.conf`:

```ini
[Time]
NTP=ntp.example.com
FallbackNTP=time.google.com
```

| Symptom | Check | Fix |
|---------|-------|-----|
| TLS/Kerberos “not yet valid” | `timedatectl`; offset | Fix NTP; wait for sync or force step if allowed |
| timesyncd inactive | `systemctl status` | Enable service; open UDP/123 egress |
| chrony not tracking | `chronyc sources -v` | Reachable sources; firewall; config pool |

## Mistakes to Avoid
- **Mistake:** Debugging “random auth failures” without checking clock offset f…
- **Mistake:** Pointing production at random public NTP without knowing policy …
- **Mistake:** Assuming cloud images always stay synced after snapshot restore

## Pros/Cons or Trade-offs
- **Pro timesyncd:** Simple, enough for most clients.
- **Con timesyncd:** Weaker than chrony for stratum discipline and large step r…
- **Pro chrony:** Better for servers and VMs that sleep or change networks.
- **Con:** Still need egress to trusted sources or an internal stratum.

## Comparison
- vs manual `date -s`: temporary and drifts again. vs PTP (Precision Time Proto…


### Use cases
- After a VM restore or long suspend, clocks jump
