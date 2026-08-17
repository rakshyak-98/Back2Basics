[[Networking]] [[CIDR (Classless Inter-Domain Routing)]] [[NAT (Network Address Translation)]] [[localhost]] [[loopback]] [[network gateway]]

# non-Routable address

> Non-routable addresses stay on the private side — the public internet will not deliver packets to them.

```txt
        non-Routable addre ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask RFC 1918 / non-routable space to confirm you know why privat…

## Sources
- [RFC 1918 — Address Allocation for Private Internets](https://www.rfc-editor.org/rfc/rfc1918) — deep-dive
- [RFC 6598 — IANA-Reserved IPv4 Prefix for Shared Address Space (CGNAT)](https://www.rfc-editor.org/rfc/rfc6598) — deep-dive
- [RFC 3927 — Dynamic Configuration of IPv4 Link-Local Addresses](https://www.rfc-editor.org/rfc/rfc3927) — overview
- [Wikipedia — Private network](https://en.wikipedia.org/wiki/Private_network) — overview

## Key Concepts
- **RFC 1918:** classic private IPv4 — `10/8`, `172.16/12`, `192.168/16`.
- **Loopback:** only this host (`127.0.0.0/8`) — `127.0.0.1` never leaves the machine.
- **Link-local:** same L2 segment (`169.254/16`) — APIPA; not a real LAN plan.
- **CGNAT:** ISP-shared private space (`100.64/10`)
- **Unreachable from outside:** no global route → need NAT, VPN, or a public listener.


- **Core:** Non-routable (special-use) addresses are prefixes that must not be forwarded …

## Technical Details
```txt
Internet ──✗── 10.x / 172.16–31 / 192.168.x
                │
              Your LAN (NAT at the edge)
```

| Range | Role |
|-------|------|
| `10.0.0.0/8` | Private |
| `172.16.0.0/12` | Private |
| `192.168.0.0/16` | Private |
| `127.0.0.0/8` | Loopback |
| `169.254.0.0/16` | Link-local (APIPA) |
| `0.0.0.0/8` | “This network” / unspecified |
| `100.64.0.0/10` | Shared CGNAT space |

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

| Symptom | Check | Fix |
|---------|-------|-----|
| Internet client can’t hit `192.168.x` | Expected — non-routable | Port-forward, reverse tunnel, VPN, or public LB |
| Service “down” from other hosts | Bound to `127.0.0.1` | Bind `0.0.0.0` or the LAN IP |
| Phone can’t reach laptop API | Using `localhost` on phone | Use laptop’s LAN IP ([[localhost]]) |
| Weird `169.254.x` address | No DHCP | Fix DHCP/router; don’t treat APIPA as production |
| Overlap after VPC peer | Same RFC1918 on both sides | Renumber or use NAT |

## Mistakes to Avoid
- **Mistake:** Treating private as secure
- **Mistake:** Assuming `0.0.0.0` listen makes a service public
- **Mistake:** Ignoring CGNAT `100.64/10`
- **Mistake:** Using overlapping `10/8` blocks across orgs without a renumberin…
- **Mistake:** Substituting “it’s internal” for authentication

## Pros/Cons or Trade-offs
- **Pro:** Conserves public IPv4; simple private addressing inside orgs.
- **Con:** Breaks end-to-end reachability — inbound needs NAT, VPN, or public frontends.
- **Con:** Overlapping RFC 1918 blocks break peering and mergers.

## Comparison
- vs public unicast: globally routable; private space is not.
- vs [[NAT (Network Address Translation)]]: NAT is how private hosts share a public face.
- vs [[CIDR (Classless Inter-Domain Routing)]]: CIDR is notation/sizing


### Use cases
- Home LANs, cloud VPCs, and CGNAT mobile networks all use non-routable space b…

- **Example:** A teammate shares `http://192.168.1.20:3000` with a remote colle…
