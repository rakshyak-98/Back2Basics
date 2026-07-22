[[ss]] [[route]] [[ip]] [[Linux]]

# NetworkManager (network managmeen)

> One-line: default Linux userspace daemon that owns interface bring-up, DHCP, Wi-Fi, DNS, and routing — replaces manual `ifup`/static scripts on most desktops and servers.

---

## Mental model

**NetworkManager (NM)** sits between **kernel netlink** and **admin intent** (CLI, GUI, cloud-init):

```txt
cloud-init / nmcli / GUI
         │
         ▼
  NetworkManager ──► netlink ──► kernel (addrs, routes, rules)
         │
         └── dns (resolved stub), Wi-Fi supplicant, PPP/VPN plugins
```

Competes conceptually with **systemd-networkd**, **ifupdown**, **netplan** (Ubuntu renders into NM or networkd). On many distros **NM is the source of truth** — hand-editing `/etc/network/interfaces` gets overwritten on reboot.

**Service impact:** "I added a route but it vanished" → NM policy or cloud-init reapplied profile.

---

## Standard config / commands

### Status and devices

```bash
nmcli general status
nmcli device status
nmcli connection show --active
nmcli device show eth0
```

### Bring up / DHCP

```bash
nmcli connection up "Wired connection 1"
nmcli device connect eth0
nmcli connection modify "Wired connection 1" ipv4.method auto
nmcli connection up "Wired connection 1"
```

### Static IP (persistent)

```bash
nmcli con mod "Wired connection 1" \
  ipv4.method manual \
  ipv4.addresses 10.0.1.50/24 \
  ipv4.gateway 10.0.1.1 \
  ipv4.dns "1.1.1.1 8.8.8.8"
nmcli con up "Wired connection 1"
```

### Routes (persistent)

```bash
nmcli con mod "Wired connection 1" +ipv4.routes "10.20.0.0/16 10.0.1.254"
nmcli con up "Wired connection 1"
```

### DNS

```bash
nmcli con mod "Wired connection 1" ipv4.dns "10.0.0.53"
nmcli con mod "Wired connection 1" ipv4.ignore-auto-dns yes
```

**Why `nmcli` over `ip` alone:** `ip route add` is ephemeral unless scripted; NM stores in connection profile.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| No default route | `nmcli dev`; `ip route` | `nmcli con up`; fix `ipv4.gateway`; autoconnect `yes` |
| DNS fails, IP works | `resolvectl status`; NM dns | Set `ipv4.dns`; disable bad DHCP option 6 |
| Changes lost on reboot | Edited `ip` not NM profile | Use `nmcli con mod`; check netplan render |
| Interface unmanaged | `NM_UNMANAGED` in logs | `nmcli dev set eth0 managed yes`; fix udev |
| VPN split tunnel wrong | `nmcli con show vpn` routes | Adjust route metrics; `ipv4.never-default` |

---

## Gotchas

> [!WARNING]
> **Server minimal images** may disable NM — installing NM alongside networkd causes fight-over-interface.

> [!WARNING]
> **`nmcli networking off`** kills all NM-managed links — not just Wi-Fi.

> [!WARNING]
> **Cloud images** — cloud-init first boot profile overrides manual NM edits unless you change the cloud config.

---

## When NOT to use

On **Kubernetes nodes** or **router appliances**, teams often prefer **systemd-networkd** or CNI-managed interfaces — disable NM for dataplane NICs to avoid surprise DHCP.

---

## Related

[[ss]] [[route]] [[ip]] [[ethtool]] [[loopback]] [[localhost]]
