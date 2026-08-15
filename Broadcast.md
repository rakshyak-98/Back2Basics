[[Multicast]] [[IGMP]] [[Networking]] [[ARP]]

# Broadcast

> Broadcast — one sender; every host in the same Layer-2 broadcast domain receives the frame.

## Interview Relevance
Classic networking: contrast unicast / broadcast / multicast, why routers stop broadcasts, and how broadcast storms and DHCP/ARP noise appear in packet captures.

## Sources
- [Wikipedia — Broadcasting (networking)](https://en.wikipedia.org/wiki/Broadcasting_(networking)) — overview
- [RFC 919 — Broadcasting Internet Datagrams](https://datatracker.ietf.org/doc/html/rfc919) — deep-dive

## Core Definition
Broadcast delivers a single transmission to all stations on a broadcast domain (typically a VLAN/subnet at L2). IPv4 limited broadcast is `255.255.255.255`; directed subnet broadcast targets a specific network’s broadcast address.

## Key Concepts
- **Broadcast domain:** Bounded by routers (and VLAN boundaries); switches flood within the domain.
- **Everyone pays:** Hosts receive the frame even if the application ignores it — wasteful at scale.
- **Common uses:** ARP requests, DHCP discover, some legacy discovery protocols.
- **No default WAN flood:** Routers do not forward broadcasts unless specially configured (and usually should not).

## Technical Details
```txt
        Sender
           |
   -----------------
   |   |   |   |   |
  PC1 PC2 PC3 PC4 PC5   ← all see the frame on the LAN
```

L2: destination MAC `ff:ff:ff:ff:ff:ff`. Excessive broadcasts (loops, chatty protocols) degrade the segment — spanning tree and storm control matter.

## Real-World Applications
DHCP client boots: broadcast discover on the local segment (or relayed via DHCP helper as unicast to a server). ARP: “who has 10.0.0.5?” is a broadcast question on the LAN.

## Pros/Cons or Trade-offs
- **Pro:** Simple discovery when membership is “everyone here.”
- **Con:** Does not scale; interrupts all hosts; dangerous across large L2 fabrics.

## Comparison
vs [[Multicast]]: multicast reaches only joined receivers (IGMP/PIM); broadcast reaches all. vs unicast: one specific destination. Related: [[IGMP]], IPTV designs prefer multicast over broadcast.

## Mistakes to Avoid
- Expecting broadcasts to cross routers for “whole company” discovery.
- Building app protocols on broadcast that should be multicast or a registry service.
- Ignoring broadcast storms from bridging loops.
