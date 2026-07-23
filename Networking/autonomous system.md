[[BGP]] [[CIDR (Classless Inter-Domain Routing)]] [[routing table]]

# Autonomous system

> A network (or set of prefixes) under one administrative routing policy, identified globally by an **ASN** — the unit BGP uses to exchange reachability.

---

## Mental model

An **Autonomous System (AS)** is how the Internet names **who owns which IP blocks** at the routing layer:

```txt
AS64512 (your org)  ──BGP──►  AS15169 (Google)  ──►  global table
     │                              │
     └── announces 203.0.113.0/24   └── selects best path by policy
```

Key ideas:
- **ASN** — 16-bit (legacy) or 32-bit number; private use 64512–65534
- **Routing policy** — what you announce, filter, prefer (prepends, local-pref)
- **Single AS** can span many physical sites if one coherent policy

**Service impact:** multi-homing, cloud egress, and DDoS scrubbing all manipulate **which AS path** traffic takes.

---

## Standard config / commands

### Lookup ASN for prefix or IP

```bash
whois 203.0.113.0 | grep -i origin
# or RIPE Stat / bgp.tools web

# CLI tools
sudo apt install bgpq4
bgpq4 -A 15169 | head
```

### Local BGP (bird/frr) — conceptual

```bash
vtysh -c 'show ip bgp summary'
vtysh -c 'show bgp ipv4 unicast 203.0.113.0/24'
```

### Cloud

```bash
# AWS: AS 16509; customer brings own ASN for BYOIP
# Register ASN via RIR (ARIN/RIPE/APNIC) before announcing on internet
```

**Why filters matter:** announcing someone else's prefix = **BGP hijack** — upstreams should reject via RPKI/IRR.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Prefix unreachable from some regions | `bgp.tools` path view | Missing announcement; over-specific filter |
| Traffic via wrong ISP | AS path length / prepends | Tune local-pref; fix export policy |
| RPKI INVALID | `rpki-validator` | Fix ROA max-length and origin ASN |
| ASN not in global table | Registration not complete | Complete RIR SWIP; wait propagation |

---

## Gotchas

> [!WARNING]
> **Private ASN (64512+)** must not leak to public internet — upstream should strip.

> [!WARNING]
> **More-specific hijacks** — /24 announced inside your /16 steals traffic if accepted.

> [!WARNING]
> **Cloud default ASN** — peering policy differs from your corporate ASN.

---

## When NOT to use

Don't run BGP at the edge without **filtering, RPKI, and on-call** — default static routes or provider BGP are enough for single-homed sites.

---

## Related

[[BGP]] [[CIDR (Classless Inter-Domain Routing)]] [[routing table]] [[NAT (Network Address Translation)]]
