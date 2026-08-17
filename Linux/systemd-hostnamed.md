[[services/systemd]] [[services/D-Bus]] [[commands/busctl]] [[Linux configuration]] [[etc files]]

# systemd-hostnamed

> D-Bus service behind `hostnamectl` — sets static, transient, and pretty hostname metadata.

```txt
        systemd-hostnamed ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Small systemd ecosystem question: static vs transient hostname, which files c…

## Sources
- [hostnamectl(1)](https://www.freedesktop.org/software/systemd/man/latest/hostnamectl.html) — deep-dive
- [org.freedesktop.hostname1](https://www.freedesktop.org/software/systemd/man/latest/org.freedesktop.hostname1.html) — deep-dive

## Key Concepts
- **Static:** persists in `/etc/hostname` across reboot.
- **Transient:** kernel hostname until reboot (DHCP/cloud-init often sets this).
- **Pretty / chassis:** human metadata in `/etc/machine-info`.
- **D-Bus API:** `hostnamectl` is a client of `systemd-hostnamed`.

## Technical Details
```bash
hostnamectl status
sudo hostnamectl set-hostname app01.example.com
sudo hostnamectl set-hostname app01 --static
sudo hostnamectl set-hostname edge --transient
systemctl status systemd-hostnamed
busctl introspect org.freedesktop.hostname1
```

| Source | File |
|--------|------|
| Static | `/etc/hostname` |
| Pretty | `/etc/machine-info` (`PRETTY_HOSTNAME`) |
| Transient | kernel hostname (until reboot) |

## Mistakes to Avoid
- **Mistake:** Setting only transient and expecting it after reboot
- **Mistake:** Fighting cloud-init that rewrites hostname every boot
- **Mistake:** Assuming `hostname` CLI and `hostnamectl` always show the same f…

## Pros/Cons or Trade-offs
- **Pro:** One CLI for hostname + machine metadata with policy-friendly D-Bus access.
- **Con:** Cloud-init/DHCP can fight static settings if not coordinated.

## Comparison
- vs editing `/etc/hostname` alone: misses pretty/transient and may skip hostnamed hooks.
- vs [[services/D-Bus]]: hostnamed is one of many systemd D-Bus services.


### Use cases
- Standardize VM names after clone: set static hostname, verify DHCP did not le…
