[[Networking]] [[CIDR (Classless Inter-Domain Routing)]] [[NAT (Network Address Translation)]] [[localhost]]

# non-Routable address

> Non-routable addresses stay on the private side — the public internet will not deliver packets to them.

---

## Mental model

**Say it in one breath:** Private and special-use IPs are for LAN, loopback, or link-local — routers on the internet drop or never advertise them.

```txt
Internet ──✗── 10.x / 172.16–31 / 192.168.x
                │
              Your LAN (NAT at the edge)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **RFC1918** | Classic private IPv4 ranges | “`10/8`, `172.16/12`, `192.168/16` are non-routable on the public net.” |
| **Loopback** | Only this host (`127.0.0.0/8`) | “`127.0.0.1` never leaves the machine.” |
| **Link-local** | Same L2 segment (`169.254/16`) | “APIPA — no DHCP; not a real LAN plan.” |
| **CGNAT** | ISP-shared private space (`100.64/10`) | “Your ‘public’ IP may still be behind carrier NAT.” |
| **Unreachable “from outside”** | No global route to that address | “Need NAT, VPN, or a public listener — not the private IP alone.” |

### Common non-routable / special IPv4

| Range | Role |
|-------|------|
| `10.0.0.0/8` | Private |
| `172.16.0.0/12` | Private |
| `192.168.0.0/16` | Private |
| `127.0.0.0/8` | Loopback |
| `169.254.0.0/16` | Link-local (APIPA) |
| `0.0.0.0/8` | “This network” / unspecified |
| `100.64.0.0/10` | Shared CGNAT space |

---

## Standard config / commands

```bash
ip -4 addr show
ip route show
curl -4 ifconfig.me          # what the internet sees (public / CGNAT face)

# Bind intentionally
# 127.0.0.1  → local only
# 0.0.0.0    → all interfaces (still private IPs on LAN NICs)
ss -tlnp | grep ':8080'
```

| Knob | Why it matters |
|------|----------------|
| Bind address | `127.0.0.1` = local only; LAN peers need the private NIC IP |
| Security group / UFW | Allow the *private* source CIDR, not a public guess |
| VPN / Tailscale | Gives a path into private space without exposing it |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Internet client can’t hit `192.168.x` | Expected — non-routable | Port-forward, reverse tunnel, VPN, or public LB |
| Service “down” from other hosts | Bound to `127.0.0.1` | Bind `0.0.0.0` or the LAN IP |
| Phone can’t reach laptop API | Using `localhost` on phone | Use laptop’s LAN IP ([[localhost]]) |
| Weird `169.254.x` address | No DHCP | Fix DHCP/router; don’t treat APIPA as production |
| Overlap after VPC peer | Same RFC1918 on both sides | Renumber or use NAT |

---

## Gotchas

> [!WARNING]
> **Private ≠ secure** — anyone on the LAN (or who joins the VPC) can still reach it.

> [!WARNING]
> **`0.0.0.0` listen ≠ public** — you still need a route/NAT/firewall hole for the internet.

> [!WARNING]
> **CGNAT `100.64/10`** — looks “private”; inbound from the internet still fails without ISP help.

---

## When NOT to use

- **Publishing a service to the world** — need a public IP, LB, or tunnel — not RFC1918 alone.
- **Cross-org peering without a plan** — colliding `10/8` blocks; design non-overlapping CIDRs first.
- **As a substitute for authentication** — “it’s internal” is not an access-control model.

---

## Related

[[Networking]] [[CIDR (Classless Inter-Domain Routing)]] [[NAT (Network Address Translation)]] [[localhost]] [[loopback]] [[network gateway]]
