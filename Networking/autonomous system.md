[[BGP]] [[CIDR (Classless Inter-Domain Routing)]] [[routing table]] [[NAT (Network Address Translation)]]

# Autonomous system

> An Autonomous System (AS) is how the Internet names who owns which IP blocks at the routing layer — one coherent routing policy under one ASN.

## Interview Relevance

Interviewers ask about ASNs and [[BGP]] to see if you understand multi-homing, route announcements, and why hijacks/RPKI matter — not just “AS means a big company.”

## Sources

- [RFC 4271 — A Border Gateway Protocol 4 (BGP-4)](https://www.rfc-editor.org/rfc/rfc4271) — deep-dive
- [RFC 1930 — Guidelines for creation, selection, and registration of an Autonomous System](https://www.rfc-editor.org/rfc/rfc1930) — overview
- [Wikipedia — Autonomous system (Internet)](https://en.wikipedia.org/wiki/Autonomous_system_(Internet)) — overview

## Core Definition

An Autonomous System is a set of IP prefixes under a single routing policy, identified by an Autonomous System Number (ASN), and exchanged with neighbors via [[BGP]].

## Key Concepts

- **ASN:** 16-bit (legacy) or 32-bit number → identity in the global routing system; private use includes 64512–65534 (and 32-bit private ranges).
- **Announcement:** you advertise prefixes you are authorized to originate → others learn reachability.
- **Routing policy:** what you announce, filter, and prefer (prepends, local-pref) → path selection is policy, not pure shortest path.
- **Single AS, many sites:** one coherent policy can span many physical locations.
- **RPKI / IRR:** cryptographic and registry filters → upstreams should reject unauthorized origins (hijack defense).

## Technical Details

```txt
AS64512 (your org)  ──BGP──►  AS15169 (Google)  ──►  global table
     │                              │
     └── announces 203.0.113.0/24   └── selects best path by policy
```

Service impact: multi-homing, cloud egress, and DDoS scrubbing all manipulate **which AS path** traffic takes.

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

| Symptom | Check | Fix |
|---------|-------|-----|
| Prefix unreachable from some regions | `bgp.tools` path view | Missing announcement; over-specific filter |
| Traffic via wrong ISP | AS path length / prepends | Tune local-pref; fix export policy |
| RPKI INVALID | `rpki-validator` | Fix ROA max-length and origin ASN |
| ASN not in global table | Registration not complete | Complete RIR SWIP; wait propagation |

## Real-World Applications

ISPs, large enterprises, and cloud providers each operate as ASes; BYOIP and multi-homed edges attach your prefixes to your ASN.

**Example:** Traffic prefers the “wrong” ISP after multi-homing — export policy or AS-path prepends need tuning; check path views before blaming the [[routing table]] on a single host.

## Pros/Cons or Trade-offs

- **Pro:** Clear administrative boundary for policy and abuse contact at Internet scale.
- **Con:** Running public BGP without filtering, RPKI, and on-call is operationally dangerous.
- **Con:** Private ASNs must not leak to the public Internet — upstreams should strip them.

## Comparison

- vs a single host [[routing table]]: the host table forwards locally; AS/BGP exchanges reachability between networks.
- vs [[CIDR (Classless Inter-Domain Routing)]]: CIDR is how prefixes are sized; an AS is who originates and policies them.
- vs cloud default ASN: provider peering policy differs from your corporate ASN — BYOIP/peering terms matter.

## Mistakes to Avoid

- Letting private ASN (64512+) leak to the public Internet.
- Ignoring more-specific hijacks — a `/24` announced inside your `/16` steals traffic if accepted.
- Running BGP at the edge without filters/RPKI when a static default or provider BGP would suffice for a single-homed site.
