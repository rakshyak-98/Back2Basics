[[IGMP]] [[IPTV]] [[PIM]]

Multicast = one sender -> Selected group of receivers.


```txt
          Sender
             |
        Multicast Group
             |
      -----------------
      |       |       |
     PC2     PC4     PC5
```
- Only devices that join the multicast group receive the traffic.

```txt 224.0.0.0 -> 239.255.255.255
```

Uses -> IPTV, Live video streaming, Stock market feeds, video conferencing, online gaming updates.

Characteristics
- Efficient bandwidth usage.
- One packet transmitted, replicated only where needed.
- Receivers join using IGMP (Internet Group Management Protocol).
- Routers use multicast routing protocols (e.g, PIM)

> [!INFO]
> A multicast sender cannot maintain a separate TCP state for thousands of receivers. Instead, the browser would need to use UDP-based transport.