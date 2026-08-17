[[Multicast]] [[IGMP]] [[Networking]] [[ARP]]

# Broadcast

> Broadcast — one sender; every host in the same Layer-2 broadcast domain receives the frame.

```txt
        Broadcast ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Classic networking: contrast unicast / broadcast / multicast, why routers sto…

## Sources
- [Wikipedia — Broadcasting (networking)](https://en.wikipedia.org/wiki/Broadcasting_(networking)) — overview
- [RFC 919 — Broadcasting Internet Datagrams](https://datatracker.ietf.org/doc/html/rfc919) — deep-dive

## Key Concepts
- **Broadcast domain:** Bounded by routers (and VLAN boundaries); switches flood within the domain.
- **Everyone pays:** Hosts receive the frame even if the application ignores it
- **Common uses:** ARP requests, DHCP discover, some legacy discovery protocols.
- **No default WAN flood:** Routers do not forward broadcasts unless specially configured (and usually sh…


- **Core:** Broadcast delivers a single transmission to all stations on a broadcast domai…

## Technical Details
```txt
        Sender
           |
   -----------------
   |   |   |   |   |
  PC1 PC2 PC3 PC4 PC5   ← all see the frame on the LAN
```

- L2: destination MAC `ff:ff:ff:ff:ff:ff`.
- Excessive broadcasts (loops, chatty protocols) degrade the segment

## Mistakes to Avoid
- **Mistake:** Expecting broadcasts to cross routers for “whole company” discov…
- **Mistake:** Building app protocols on broadcast that should be multicast or …
- **Mistake:** Ignoring broadcast storms from bridging loops

## Pros/Cons or Trade-offs
- **Pro:** Simple discovery when membership is “everyone here.”
- **Con:** Does not scale; interrupts all hosts; dangerous across large L2 fabrics.

## Comparison
- vs [[Multicast]]: multicast reaches only joined receivers (IGMP/PIM)


### Use cases
- DHCP client boots: broadcast discover on the local segment (or relayed via DH…
