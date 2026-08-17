[[MTU (Maximum Transmission Unit)]] [[ICMP]] [[TCP]] [[UDP]]

# Packet Fragment

> IP fragmentation splits oversized datagrams — lose one fragment and the entire original packet is discarded.

```txt
        Packet Fragment ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask about fragmentation to check Path MTU Discovery knowledge, I…

## Sources
- [RFC 791 — IPv4 (fragmentation)](https://www.rfc-editor.org/rfc/rfc791) — deep-dive
- [RFC 8200 — IPv6](https://www.rfc-editor.org/rfc/rfc8200) — deep-dive
- [Wikipedia — IP fragmentation](https://en.wikipedia.org/wiki/IP_fragmentation) — overview

## Key Concepts
- **Split and reassemble:** oversized datagrams become fragments sharing an identification field → receiv…
- **All-or-nothing delivery:** any missing fragment drops the whole original packet → loss is amplified.
- **IPv4 vs IPv6:** IPv4 routers may fragment if DF is clear
- **Avoid on the path:** TCP MSS, sized UDP datagrams, and lower tunnel MTU → better than relying on r…

## Technical Details
- When a datagram exceeds the outgoing link [[MTU (Maximum Transmission Unit)]]…
- The receiver reassembles before delivering to [[TCP]] or [[UDP]].

```
Original 4000 byte datagram
  → Frag 1: bytes 0–1480
  → Frag 2: bytes 1481–2960
  → Frag 3: bytes 2961–4000
```

- IPv6 forbids router fragmentation (RFC 8200)

- Why it hurts performance:

- Loss of any fragment wastes the whole packet
- Middleboxes may mishandle fragments (security filters, NAT)
- Reassembly buffers are finite

- Modern practice: avoid fragmentation on the path.
- TCP negotiates MSS; UDP apps cap datagram size; tunnels lower MTU.

```bash
tcpdump -ni any 'ip[6:2] & 0x3fff != 0'    # fragmented IPv4
```

## Mistakes to Avoid
- **Mistake:** Assuming IPv6 routers will fragment like IPv4 — they will not
- **Mistake:** Ignoring that one lost fragment equals total packet loss
- **Mistake:** Designing UDP payloads larger than ~1200–1400 bytes on the publi…
- **Mistake:** Forgetting that some firewalls drop fragments and break paths th…

## Pros/Cons or Trade-offs
- **Pro:** Lets oversized IPv4 datagrams cross smaller links without the sender knowing the path MTU in advance.
- **Con:** Fragile under loss, hostile to middleboxes, and a historical attack vector — prefer PMTUD and sizing instead.

## Comparison
- vs [[MTU (Maximum Transmission Unit)]]: MTU is the size limit per link


### Use cases
- Diagnosing legacy apps that send large UDP datagrams, VPN paths with mismatch…
