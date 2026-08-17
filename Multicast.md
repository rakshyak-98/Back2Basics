[[IGMP]] [[IPTV]] [[PIM]] [[Broadcast]] [[Networking]]

# Multicast

> Multicast — one sender to many interested receivers; only hosts that joined the group get the traffic.





## Interview Relevance
Networking interviews contrast unicast / broadcast / multicast, IGMP on the LAN, and PIM for routing trees. Signal efficiency: one packet in, replicated only where needed.

## Sources
- [Wikipedia — Multicast](https://en.wikipedia.org/wiki/Multicast) — overview
- [RFC 1112 — Host Extensions for IP Multicasting](https://datatracker.ietf.org/doc/html/rfc1112) — deep-dive
- [RFC 7761 — PIM Sparse Mode](https://datatracker.ietf.org/doc/html/rfc7761) — deep-dive

## Core Definition
IP multicast delivers a single stream to a group address; receivers subscribe with [[IGMP]] (or MLD for IPv6). Routers build distribution trees with protocols such as [[PIM]] so links without members do not carry the traffic.

## Key Concepts
- **Group address:** IPv4 `224.0.0.0/4` (224.0.0.0–239.255.255.255).
- **Interest-based:** Unlike [[Broadcast]], non-members should not process the stream.
- **IGMP:** Host ↔ router “I want this group” on the local segment.
- **PIM / multicast routing:** How the tree spans multiple routers.
- **Use cases:** [[IPTV]], live video, market data, some discovery/gaming updates.

## Technical Details
```txt
          Sender
             |
      Multicast group (G)
             |
      -----------------
      |       |       |
     PC2     PC4     PC5   ← joined members only
```

Flow: source sends to `G` → first-hop router → PIM tree → last-hop routers → IGMP-joined hosts. Cloud/VPC networks often disable or limit multicast — design accordingly.

## Real-World Applications
Campus IPTV: encoders multicast; set-top boxes join channels via IGMP; core uses PIM-SM. Stock tick fans to many traders without N unicast copies from the exchange feed handler.

## Pros/Cons or Trade-offs
- **Pro:** Bandwidth efficient for one-to-many live data.
- **Con:** Complex ops (RPF checks, PIM, IGMP snooping); many clouds/WANs lack native support — often replaced by unicast fan-out or overlay.

## Comparison
vs [[Broadcast]]: broadcast hits everyone in the domain; multicast hits subscribers. vs unicast fan-out: simpler everywhere, wastes uplink when N is large. vs app-layer pub/sub ([[Message Broker]]): brokers run at L7 with different reliability semantics.

## Mistakes to Avoid
- Assuming AWS/GCP VPCs will route multicast like a campus LAN.
- Forgetting IGMP snooping — switches can flood multicast like broadcast.
- Using multicast for reliable file delivery without an application retry layer.
