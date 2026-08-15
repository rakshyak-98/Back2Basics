[[autonomous system]] [[CIDR (Classless Inter-Domain Routing)]] [[routing table]] [[Internal routing]]

# BGP

> Border Gateway Protocol is how autonomous systems exchange reachability on the public internet — outages here are policy and peering problems, not a missing default route on one host.

## Interview Relevance

Staff interviews use BGP to test inter-domain thinking: AS paths, eBGP vs iBGP, policy over shortest-path metrics, and how prefix leaks or hijacks show up as "the internet is broken" rather than a local default-route mistake.

## Sources

- [RFC 4271 — A Border Gateway Protocol 4 (BGP-4)](https://www.rfc-editor.org/rfc/rfc4271) — deep-dive
- [Wikipedia — Border Gateway Protocol](https://en.wikipedia.org/wiki/Border_Gateway_Protocol) — overview

## Key Concepts

- **Path-vector protocol:** each advertisement carries AS path, next hop, and attributes → loops are detected via AS_PATH, not a simple hop metric.
- **Policy over pure distance:** unlike OSPF/IS-IS, BGP optimizes who may use which paths → LOCAL_PREF, communities, and filters dominate day-to-day ops.
- **eBGP vs iBGP:** eBGP peers across [[autonomous system]] boundaries; iBGP stays inside one AS (full mesh or route reflectors) → different scaling and next-hop rules.
- **Prefix + ASN:** you advertise [[CIDR (Classless Inter-Domain Routing)]] blocks with an autonomous system number → the global table is a mesh of these announcements.

## Technical Details

BGP (RFC 4271) exchanges reachability between autonomous systems.

```
AS 65001 ──eBGP──► AS 64500 (transit) ──eBGP──► AS 15169
         announces 203.0.113.0/24 with path [65001]
```

| Term | Meaning |
|------|---------|
| eBGP | BGP between different [[autonomous system]] numbers |
| iBGP | BGP within one AS — typically full mesh or route reflectors |
| Prefix | CIDR block advertised (e.g. `198.51.100.0/24`) |
| ASN | 16- or 32-bit autonomous system number (RFC 6793) |

Attributes that matter operationally:

- **AS_PATH** — loop detection; shorter paths often preferred
- **NEXT_HOP** — where to forward
- **LOCAL_PREF** — inbound traffic preference (iBGP)
- **MED** — hint between adjacent ASes
- **Communities** — tags for remote policy (e.g. "do not export")

```bash
# On a router with FRR/BIRD/Quagga or vendor CLI — examples vary
show ip bgp summary
show ip bgp 203.0.113.0/24
```

Host-level "BGP broken" symptoms are usually upstream: prefix hijacks, leaked routes, or peering failures — check external monitoring (RIPE RIS, BGPmon) and provider status.

## Real-World Applications

ISP peering, multi-homed enterprise edge, and anycast announcements. Example: a leaked more-specific prefix pulls traffic away from the legitimate origin until the bad announcement is withdrawn — hosts see timeouts while their default route still looks fine.

## Pros/Cons or Trade-offs

- **Pro:** Scales the internet with rich policy control, communities, and multi-homing.
- **Con:** Misconfiguration (leaks, missing filters, bad LOCAL_PREF) can black-hole or hijack traffic globally; convergence and debugging are complex.

## Comparison

vs [[Internal routing]] (OSPF/IS-IS): interior protocols optimize metrics inside an AS; BGP exchanges reachability between ASes and is driven by policy, not a single shortest-path cost.

## Mistakes to Avoid

- Debugging "BGP" on a single host's default gateway — most failures are upstream peering or prefix policy.
- Advertising routes without filters — classic cause of route leaks.
- Confusing shorter AS_PATH with "always best" — LOCAL_PREF and policy often override path length.
- Ignoring more-specific prefixes — a /24 can override a /16 and steal traffic.
