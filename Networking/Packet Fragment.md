<!-- note-strategy: operational -->
[[Networking]] [[MTU (Maximum Transmission Unit)]] [[ICMP]] [[UDP]] [[TCP]]

# Packet Fragment

> Fragmentation splits an IP packet that is too big for the next MTU — destination reassembles, or DF drops it.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Oversized packet → fragments with same ID + offsets → receiver glues them. One lost fragment kills the whole datagram.

```txt
2000-byte IP, MTU 1500 (IPv4)
  Fragment 1: ~1480 data + IP hdr = 1500
  Fragment 2: remainder + IP hdr
  Reassemble at destination (not every hop)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Fragment** | Piece of an IP packet | “Offset + MF/flags identify the set.” |
| **DF (Don’t Fragment)** | Forbid splitting | “Too big → ICMP need-frag or silent drop.” |
| **Reassembly** | Destination rebuilds | “Middle routers forward pieces as-is.” |
| **PMTUD** | Discover min path MTU | “Avoid frag by shrinking sends.” |
| **IPv6** | No in-network frag | “Source must fragment (or better: shrink).” |

### Tiny example

| Piece | Approx size |
|-------|-------------|
| Frag 1 | 1480 data + 20 IP = 1500 |
| Frag 2 | 480 data + 20 IP = 500 |

---

## Standard config / commands

```bash
# Force DF and probe size
ping -M do -s 1472 8.8.8.8

# Watch fragments
sudo tcpdump -ni eth0 'ip[6:2] & 0x1fff != 0'

# Lower MTU to avoid frag on a tunnel
ip link set eth0 mtu 1400
```

| Knob | Why it matters |
|------|----------------|
| DF on TCP | Normal — rely on MSS/PMTUD |
| UDP payload size | App must stay under path MTU |
| Firewall reassembly | Some middleboxes drop frag sets |
| Tunnel overhead | Effective MTU shrinks |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Small OK, large fail | Frag / PMTU | Lower MTU; allow ICMP PTB; clamp MSS |
| DNS or game UDP flaky | Fragmented UDP | Keep UDP under ~1200 or enable EDNS careful sizing |
| Only through VPN broken | Encaps + frag | Set tunnel MTU; MSS clamp |
| Security device drops | Incomplete frag sets | Avoid frag; update appliance policy |
| IPv6 “frag needed” | Source too big | Shrink; don’t expect router frag |

---

## Gotchas

> [!WARNING]
> **One lost fragment = total loss** — frag amplifies drop pain.

> [!WARNING]
> **Firewalls hate fragments** — first-fragment-only ACLs mis-classify.

> [!WARNING]
> **TCP rarely IP-fragments today** — if you see TCP IP-frag, something is wrong with MSS/MTU.

---

## When NOT to use

- **Designing apps that “rely on frag”** — size to MTU; prefer PMTUD.
- **Jumbo + fragmentation as a plan** — fix end-to-end MTU instead.
- **IPv6 expecting routers to split** — they won’t.

---

## Related

[[Networking]] [[MTU (Maximum Transmission Unit)]] [[ICMP]] [[UDP]] [[TCP]]
