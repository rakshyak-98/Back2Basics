[[ss]] [[route]] [[ip]] [[Linux]] [[ethtool]] [[loopback]] [[localhost]]

# NetworkManager (network managmeen)

> NetworkManager sits between kernel netlink and admin intent (CLI, GUI, cloud-init) — persistent connection profiles, not one-off `ip` commands.

```txt
        NetworkManager (ne ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask NetworkManager when routes or DNS “vanish after reboot”

## Sources
- [NetworkManager documentation](https://networkmanager.dev/docs/) — deep-dive
- [nmcli(1) — Linux man page](https://man7.org/linux/man-pages/man1/nmcli.1.html) — deep-dive
- [Wikipedia — NetworkManager](https://en.wikipedia.org/wiki/NetworkManager) — overview

## Key Concepts
- **Connection profile:** persistent intent → survives reboot; `ip route add` alone does not.
- **Device vs connection:** device is the iface; connection is the applied config.
- **DNS integration:** often via systemd-resolved stub → IP can work while name resolution fails.
- **Unmanaged interfaces:** dataplane NICs may be marked unmanaged → NM won’t fight CNI/networkd.
- **Cloud-init:** first-boot profiles can override manual edits → change the cloud config, not …


- **Core:** NetworkManager (NM) manages host network configuration via connection profile…

## Technical Details
```txt
cloud-init / nmcli / GUI
         │
         ▼
  NetworkManager ──► netlink ──► kernel (addrs, routes, rules)
         │
         └── dns (resolved stub), Wi-Fi supplicant, PPP/VPN plugins
```

- On many distros NM is the source of truth

```bash
nmcli general status
nmcli device status
nmcli connection show --active
nmcli device show eth0
```

```bash
nmcli connection up "Wired connection 1"
nmcli device connect eth0
nmcli connection modify "Wired connection 1" ipv4.method auto
nmcli connection up "Wired connection 1"
```

```bash
nmcli con mod "Wired connection 1" \
  ipv4.method manual \
  ipv4.addresses 10.0.1.50/24 \
  ipv4.gateway 10.0.1.1 \
  ipv4.dns "1.1.1.1 8.8.8.8"
nmcli con up "Wired connection 1"
```

```bash
nmcli con mod "Wired connection 1" +ipv4.routes "10.20.0.0/16 10.0.1.254"
nmcli con up "Wired connection 1"
```

```bash
nmcli con mod "Wired connection 1" ipv4.dns "10.0.0.53"
nmcli con mod "Wired connection 1" ipv4.ignore-auto-dns yes
```

- **Why `nmcli` over `ip` alone:** `ip route add` is ephemeral unless scripted

| Symptom | Check | Fix |
|---------|-------|-----|
| No default route | `nmcli dev`; `ip route` | `nmcli con up`; fix `ipv4.gateway`; autoconnect `yes` |
| DNS fails, IP works | `resolvectl status`; NM dns | Set `ipv4.dns`; disable bad DHCP option 6 |
| Changes lost on reboot | Edited `ip` not NM profile | Use `nmcli con mod`; check netplan render |
| Interface unmanaged | `NM_UNMANAGED` in logs | `nmcli dev set eth0 managed yes`; fix udev |
| VPN split tunnel wrong | `nmcli con show vpn` routes | Adjust route metrics; `ipv4.never-default` |

## Mistakes to Avoid
- **Mistake:** Installing NM alongside networkd and letting them fight over int…
- **Mistake:** Running `nmcli networking off` thinking it only kills Wi‑Fi
- **Mistake:** Editing cloud-image networking only in NM without updating cloud…
- **Mistake:** Tuning ethtool/rings before confirming the connection profile an…

## Pros/Cons or Trade-offs
- **Pro:** Profiles persist; CLI/GUI/cloud-init share one model.
- **Con:** Conflicts with systemd-networkd or CNI if both manage the same iface.
- **Con:** Cloud-init can silently reapply and undo manual NM edits.

## Comparison
- vs raw `ip`: ephemeral kernel state vs NM persistent profiles.
- vs systemd-networkd / netplan: alternate host network managers
- vs Kubernetes CNI: leave dataplane NICs unmanaged by NM on nodes.


### Use cases
- Laptops, desktops, and many cloud images use NM for Wi‑Fi, VPN, and persisten…

- **Example:** An engineer adds a static route with `ip route add`; after reboo…
