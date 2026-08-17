[[IGMP]] [[IPTV]] [[PIM]] [[Broadcast]] [[Networking]]

# Multicast

> Multicast — one sender to many interested receivers; only hosts that joined the group get the traffic.

```txt
        Multicast ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Networking interviews contrast unicast / broadcast / multicast, IGMP on the L…

## Sources
- [Wikipedia — Multicast](https://en.wikipedia.org/wiki/Multicast) — overview
- [RFC 1112 — Host Extensions for IP Multicasting](https://datatracker.ietf.org/doc/html/rfc1112) — deep-dive
- [RFC 7761 — PIM Sparse Mode](https://datatracker.ietf.org/doc/html/rfc7761) — deep-dive

## Key Concepts
- **Group address:** IPv4 `224.0.0.0/4` (224.0.0.0–239.255.255.255).
- **Interest-based:** Unlike [[Broadcast]], non-members should not process the stream.
- **IGMP:** Host ↔ router “I want this group” on the local segment.
- **PIM / multicast routing:** How the tree spans multiple routers.
- **Use cases:** [[IPTV]], live video, market data, some discovery/gaming updates.


- **Core:** IP multicast delivers a single stream to a group address

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

- Flow: source sends to `G` → first-hop router → PIM tree → last-hop routers → …
- Cloud/VPC networks often disable or limit multicast — design accordingly.

## Mistakes to Avoid
- **Mistake:** Assuming AWS/GCP VPCs will route multicast like a campus LAN
- **Mistake:** Forgetting IGMP snooping
- **Mistake:** Using multicast for reliable file delivery without an applicatio…

## Pros/Cons or Trade-offs
- **Pro:** Bandwidth efficient for one-to-many live data.
- **Con:** Complex ops (RPF checks, PIM, IGMP snooping); many clouds/WANs lack native support — often replaced by unicast fan-out or overlay.

## Comparison
- vs [[Broadcast]]: broadcast hits everyone in the domain


### Use cases
- Campus IPTV: encoders multicast
