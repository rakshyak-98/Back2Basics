[[IGMP]] [[IPTV]] [[PIM]]

# Multicast

> Multicast — one sender to many interested receivers on a multicast group.

---

## Mental model

**Say it in one breath:** Multicast — plain job, how I run it, how I know it’s broken.


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

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Multicast** | Core idea of this note | “I can explain Multicast without jargon.” |
| **mental model** | How it works in one line | “Explain it without jargon first.” |
| **failure mode** | How it breaks | “Say what you check first.” |

---

## Standard config / commands

```bash
# reproduce with minimal input
# compare working vs broken env
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Unexpected result | inputs / versions | Reproduce minimal case |
| Works on one machine | env drift | Diff config and versions |
| Silent failure | logs / metrics | Add checks and alerts |

---

## Gotchas

> [!WARNING]
> Prefer simple words you can say in an interview.

---

## When NOT to use

- Skip it when a simpler existing tool already fits.

---

## Related

[[IGMP]]] [[[IPTV]]] [[[PIM]]
