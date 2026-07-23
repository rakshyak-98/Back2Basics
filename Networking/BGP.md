[[routing table]] [[CIDR (Classless Inter-Domain Routing)]] [[NAT (Network Address Translation)]]

# BGP

> One-line: path-vector protocol ASes use to exchange reachability + policy — not a replacement for your IGP — **Halabi, Internet Routing Architectures**.

## Mental model

BGP (Border Gateway Protocol) advertises **IP prefixes** (NLRI) between **Autonomous Systems** (AS). Each route carries **path attributes** — notably `AS_PATH`, `NEXT_HOP`, `LOCAL_PREF`, `MED` — used for policy-based selection, not pure shortest-path.

```
  AS 65001 (you)                    AS 64500 (upstream)
  ┌─────────────┐    eBGP session   ┌─────────────┐
  │ edge router │◄─────────────────►│   ISP peer  │
  │ 10.0.0.0/16 │                   │             │
  └──────┬──────┘                   └─────────────┘
         │ iBGP (full mesh or RR)
  ┌──────▼──────┐
  │ core routers│  same AS_PATH, NEXT_HOP often unchanged
  └─────────────┘
```

| Type | Scope | Typical use |
|------|-------|-------------|
| **eBGP** | Between different ASNs | Internet peering, transit, cloud Direct Connect |
| **iBGP** | Within one ASN | Propagate external routes to all internal routers |

**Selection order (simplified):** highest LOCAL_PREF → shortest AS_PATH → eBGP over iBGP → lowest MED → closest IGP to NEXT_HOP → router tie-break.

BGP is **slow to converge by design** (minutes possible). It assumes stability over sub-second failover — pair with BFD or IGP for fast local failure detection.

## Standard config / commands

Inspect locally (Linux FRR / Bird / vendor CLI patterns):

```shell
# FRR (common on Linux routers)
vtysh -c 'show ip bgp summary'          # session state
vtysh -c 'show ip bgp neighbors'         # timers, prefixes received
vtysh -c 'show ip bgp'                  # RIB
vtysh -c 'show ip bgp <prefix>'         # why this path won

# Bird
birdc show protocols
birdc show route for 203.0.113.0/24 all

# Generic: is the session up?
ss -tn sport = :179 or dport = :179       # BGP uses TCP/179
tcpdump -ni any port 179 -c 50
```

Cloud/hybrid peering sanity:

```shell
# AWS Direct Connect / VPN — check propagated routes in route table
aws ec2 describe-vpn-connections
aws directconnect describe-virtual-interfaces

# Confirm prefix actually installed in kernel RIB
ip route show proto bgp    # if redistributed locally
```

Minimal eBGP sanity checklist after change:
1. TCP/179 reachable (ACL, MD5/TCP-AO if configured)
2. Session `Established` (not `Active` / `Idle`)
3. Expected prefixes in `show ip bgp` / received count matches peer
4. NEXT_HOP reachable via IGP (`ping <nexthop>`, `traceroute`)
5. Prefix propagates to downstream (iBGP reflector clients, route-maps)

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Session stuck `Active` / `Idle` | `tcpdump port 179`; ACL on either side | Open TCP/179; fix MD5 mismatch; verify correct source IP on multi-homed host |
| Session flaps every ~60–180s | `show bgp neighbors` → hold timer, keepalive | MTU issue on TCP/179 (try `tcp mss` or lower interface MTU); BFD false positives |
| Prefix not received | `show ip bgp neighbors received-routes` (soft config) | Peer export policy filters you; ask peer what they advertise |
| Prefix received but not installed | `show ip bgp <prefix>` all paths | Import route-map denies; AS_PATH loop; NEXT_HOP unreachable |
| Traffic blackholed after peer up | `traceroute`; compare AS_PATH length vs expected | Longer path selected elsewhere; MED/LOCAL_PREF policy wrong |
| Partial internet outage | Multiple peers down? RPKI/ROV drop? | Check upstream status; validate ROA for your announced prefixes |
| iBGP routes missing on some routers | Full-mesh vs route-reflector topology | RR client missing; `next-hop-self` not set on edge |
| Leak / hijack suspicion | IRR/RPKI vs actual AS_PATH | Emergency withdraw; contact peer NOC; enable RPKI on imports |

## Gotchas

> [!WARNING]
> **BGP alone won't save a bad IGP.** If NEXT_HOP isn't reachable inside your AS, the route sits in RIB but never forwards.

> [!WARNING]
> **Route leaks** (advertising paths you shouldn't) are operational incidents, not theoretical. Always outbound filter what you announce.

- **eBGP multi-hop** requires explicit TTL and often fixed source IP — cloud VPN tunnels need this.
- **Private ASNs (64512–65534)** must be stripped before advertising to transit.
- **Graceful restart** helps control-plane upgrades; without it, full table withdraw causes microbursts.
- **RPKI ROV invalid** → some peers drop your prefix silently; monitor with external looking-glass tools.
- **Default route 0.0.0.0/0** from upstream is a policy choice — importing blindly can steal internal traffic.

## When NOT to use

- Don't run BGP inside a single-site LAN — use OSPF/IS-IS; BGP's policy complexity isn't worth it.
- Don't announce prefixes you don't own (even "temporarily") — upstream filtering varies and leaks propagate globally.
- Don't expect sub-second failover from BGP timers alone — add BFD or track interface state.

## Related

[[routing table]] · [[CIDR (Classless Inter-Domain Routing)]] · [[Egress traffic]] · [[ethtool]]
