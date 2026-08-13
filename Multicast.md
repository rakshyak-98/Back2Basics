[[IGMP]] [[IPTV]] [[PIM]]

# Multicast

> Multicast — one sender to many interested receivers on a multicast group.

---

## How it works

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


---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |


## Gotchas

> [!WARNING]
> …


## Related

[[IGMP]]] [[[IPTV]]] [[[PIM]]

## Sources

- [Wikipedia — Multicast](https://en.wikipedia.org/wiki/Multicast)
