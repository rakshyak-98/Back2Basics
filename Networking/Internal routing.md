[[Networking]] [[localhost]] [[address port]] [[non-Routable address]]

# Internal routing

> Internal routing is same-LAN reachability — private IP to private IP with no internet hairpin required.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** If both hosts share a subnet (or routes between private nets), talk to the peer’s private IP:port — the default gateway is not in the path.

```txt
Laptop 192.168.1.10 ── switch ──► Pi 192.168.1.50:5000
                 (no NAT, no public IP needed)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Same L2/L3 segment** | Shared broadcast / subnet | “ARP resolves MAC; IP stays private.” |
| **Private IP** | RFC1918 address | “`10/8`, `172.16/12`, `192.168/16`.” |
| **Hairpin / NAT loopback** | LAN host → public IP → back in | “Often broken; prefer private IP on LAN.” |
| **Host firewall** | ufw/iptables on the target | “Port open on process ≠ open on firewall.” |

---

## Standard config / commands

```bash
# Target’s private IP
ip -4 addr show
hostname -I

# Is the service listening where you think?
ss -tlnp | grep 5000
# Prefer 0.0.0.0 or LAN IP — not only 127.0.0.1

# Connect from another LAN host
curl http://192.168.1.50:5000

# Allow inbound (example)
sudo ufw allow 5000/tcp
sudo ufw status
```

| Knob | Why it matters |
|------|----------------|
| Bind address | `127.0.0.1` blocks LAN clients |
| Subnet / VLAN | Different VLAN ⇒ need a router between them |
| mDNS / DHCP names | `hostname.local` helps; IP is the reliable debug target |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Connection refused | `ss -tlnp` on target | Start service; fix bind host/port |
| Timeout | `ping` / `traceroute`; ufw/SG | Same subnet? Allow port; fix Wi‑Fi AP isolation |
| Works via localhost only | Bound to loopback | Bind `0.0.0.0` or LAN IP |
| Phone can’t see laptop | AP client isolation | Disable isolation or use a travel router/VLAN that allows peer traffic |
| Used public IP from LAN | Hairpin NAT | Use private IP on LAN instead |

---

## Gotchas

> [!WARNING]
> **AP / “guest Wi‑Fi” isolation** — devices share SSID but cannot talk to each other.

> [!WARNING]
> **Wrong private IP after DHCP renew** — bookmarks rot; use DHCP reservation or mDNS.

> [!WARNING]
> **VPN split tunnel** — “internal” routes may go to the VPN instead of the LAN; check `ip route`.

---

## When NOT to use

- **Exposing a service to the internet** — use reverse proxy, VPN, or tunnel — not raw port-forward forever.
- **Assuming same Wi‑Fi = same network** — guest networks and VLANs lie.
- **Skipping authentication because “it’s LAN only”** — LAN is not a trust boundary on shared Wi‑Fi.

---

## Related

[[Networking]] [[localhost]] [[address port]] [[non-Routable address]] [[network gateway]] [[NAT (Network Address Translation)]]
