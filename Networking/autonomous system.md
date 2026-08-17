[[BGP]] [[CIDR (Classless Inter-Domain Routing)]] [[routing table]] [[NAT (Network Address Translation)]]

# Autonomous system

> An Autonomous System (AS) is how the Internet names who owns which IP blocks at the routing layer — one coherent routing policy under one ASN.

```txt
        Autonomous system ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask about ASNs and [[BGP]] to see if you understand multi-homing…

## Sources
- [RFC 4271 — A Border Gateway Protocol 4 (BGP-4)](https://www.rfc-editor.org/rfc/rfc4271) — deep-dive
- [RFC 1930 — Guidelines for creation, selection, and registration of an Autonomous System](https://www.rfc-editor.org/rfc/rfc1930) — overview
- [Wikipedia — Autonomous system (Internet)](https://en.wikipedia.org/wiki/Autonomous_system_(Internet)) — overview

## Key Concepts
- **ASN:** 16-bit (legacy) or 32-bit number → identity in the global routing system
- **Announcement:** you advertise prefixes you are authorized to originate → others learn reachab…
- **Routing policy:** what you announce, filter, and prefer (prepends, local-pref) → path selection…
- **Single AS, many sites:** one coherent policy can span many physical locations.
- **RPKI / IRR:** cryptographic and registry filters → upstreams should reject unauthorized ori…


- **Core:** An Autonomous System is a set of IP prefixes under a single routing policy, i…

## Technical Details
```txt
AS64512 (your org)  ──BGP──►  AS15169 (Google)  ──►  global table
     │                              │
     └── announces 203.0.113.0/24   └── selects best path by policy
```

- Service impact: multi-homing, cloud egress, and DDoS scrubbing all manipulate…

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

- **Why filters matter:** announcing someone else's prefix = **BGP hijack**

| Symptom | Check | Fix |
|---------|-------|-----|
| Prefix unreachable from some regions | `bgp.tools` path view | Missing announcement; over-specific filter |
| Traffic via wrong ISP | AS path length / prepends | Tune local-pref; fix export policy |
| RPKI INVALID | `rpki-validator` | Fix ROA max-length and origin ASN |
| ASN not in global table | Registration not complete | Complete RIR SWIP; wait propagation |

## Mistakes to Avoid
- **Mistake:** Letting private ASN (64512+) leak to the public Internet
- **Mistake:** Ignoring more-specific hijacks
- **Mistake:** Running BGP at the edge without filters/RPKI when a static defau…

## Pros/Cons or Trade-offs
- **Pro:** Clear administrative boundary for policy and abuse contact at Internet scale.
- **Con:** Running public BGP without filtering, RPKI, and on-call is operationally dangerous.
- **Con:** Private ASNs must not leak to the public Internet — upstreams should strip them.

## Comparison
- vs a single host [[routing table]]: the host table forwards locally
- vs [[CIDR (Classless Inter-Domain Routing)]]: CIDR is how prefixes are sized
- vs cloud default ASN: provider peering policy differs from your corporate ASN


### Use cases
- ISPs, large enterprises, and cloud providers each operate as ASes

- **Example:** Traffic prefers the “wrong” ISP after multi-homing
