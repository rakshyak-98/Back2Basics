<!-- note-strategy: operational -->
[[Networking]] [[routing table]] [[non-Routable address]]

# CIDR (Classless Inter-Domain Routing)

> CIDR writes an IP plus how many bits are the network — one slash instead of old Class A/B/C masks.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `192.168.1.0/24` means “first 24 bits are the network; the rest are hosts on that LAN.”

```txt
192.168.1.0/24
│            │
│            └─ prefix length (network bits)
└─ network base (host bits = 0)

/32 = one host
/0  = default route (match everything)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Prefix length** | How many leading bits identify the network | “`/24` is 256 addresses; ~254 usable hosts.” |
| **Network / host bits** | Fixed vs free bits in the address | “Longer prefix = smaller subnet.” |
| **Supernet / aggregate** | One route covering many smaller ones | “CIDR lets ISPs advertise fewer routes.” |
| **Overlap** | Two prefixes claim the same space | “Overlapping CIDRs break routing and VPN.” |
| **Private ranges** | RFC1918 space never on the public internet | “`10/8`, `172.16/12`, `192.168/16` stay inside.” |

### Common sizes (IPv4)

| CIDR | Hosts (approx) | Typical use |
|------|----------------|-------------|
| `/32` | 1 | Single host / VIP |
| `/24` | ~254 | Small LAN / VPC subnet |
| `/16` | ~65k | Large private block |
| `/0` | all | Default gateway route |

---

## Standard config / commands

```bash
# Show routes with prefixes
ip -4 route show
ip -6 route show

# Is this IP inside a prefix? (python one-liner)
python3 -c "import ipaddress; print(ipaddress.ip_address('10.1.2.3') in ipaddress.ip_network('10.0.0.0/8'))"

# Count usable hosts
python3 -c "import ipaddress; n=ipaddress.ip_network('10.0.0.0/24'); print(n.num_addresses-2)"
```

| Knob | Why it matters |
|------|----------------|
| VPC/subnet CIDR | Must not overlap peered VPCs or VPN pools |
| Security-group CIDR | Wrong `/8` opens half the internet |
| `0.0.0.0/0` | Default egress — every unmatched dest |
| `/32` ACL | Pin to one host — least privilege |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Hosts cannot talk on same “LAN” | Subnets differ (`/25` vs `/24`) | Put both in same prefix or route between them |
| VPN / peer connect fails | Overlapping CIDRs | Renumber one side; no shared `10.0.0.0/8` |
| Route present but no traffic | Wrong prefix on interface | `ip addr` vs `ip route` — align mask |
| “Too many” / “too few” IPs | Prefix math off by one | Remember network + broadcast; `/31`/`/32` special |
| ACL blocks everything | Used host IP as network | Use network address + correct length |

---

## Gotchas

> [!WARNING]
> **`/24` is not “class C”** — CIDR is bit-length only. Same `/24` idea works anywhere.

> [!WARNING]
> **Usable hosts ≠ 2^(32−n)** — subtract network and broadcast (except `/31` point-to-point, `/32` host).

> [!WARNING]
> **Overlapping private space** — two `10.0.0.0/16` clouds cannot peer cleanly without NAT or renumber.

---

## When NOT to use

- **Explaining old textbooks** — classful A/B/C is history; say CIDR.
- **Single-host firewall rules** — prefer `/32` (or exact IP) over a whole `/24`.
- **IPv6 sizing like IPv4** — don’t allocate tiny `/120`s by habit; follow your cloud’s IPv6 plan.

---

## Related

[[Networking]] [[routing table]] [[non-Routable address]] [[network gateway]] [[NAT (Network Address Translation)]]
