[[MTU (Maximum Transmission Unit)]] [[ICMP]] [[TCP]] [[UDP]]

# Packet Fragment

> IP fragmentation splits oversized datagrams — lose one fragment and the entire original packet is discarded.





## Interview Relevance
Interviewers ask about fragmentation to check Path MTU Discovery knowledge, IPv4 vs IPv6 differences, and why modern stacks avoid fragments (loss amplification, middlebox mishandling, attack surface).

## Sources
- [RFC 791 — IPv4 (fragmentation)](https://www.rfc-editor.org/rfc/rfc791) — deep-dive
- [RFC 8200 — IPv6](https://www.rfc-editor.org/rfc/rfc8200) — deep-dive
- [Wikipedia — IP fragmentation](https://en.wikipedia.org/wiki/IP_fragmentation) — overview

## Key Concepts
- **Split and reassemble:** oversized datagrams become fragments sharing an identification field → receiver rebuilds before delivering to [[TCP]] or [[UDP]].
- **All-or-nothing delivery:** any missing fragment drops the whole original packet → loss is amplified.
- **IPv4 vs IPv6:** IPv4 routers may fragment if DF is clear; IPv6 routers do not → only the source fragments, and PMTUD is expected.
- **Avoid on the path:** TCP MSS, sized UDP datagrams, and lower tunnel MTU → better than relying on reassembly.

## Technical Details
When a datagram exceeds the outgoing link [[MTU (Maximum Transmission Unit)]] and the Don't Fragment (DF) bit is clear, routers slice it into fragments sharing the same identification field. The receiver reassembles before delivering to [[TCP]] or [[UDP]].

```
Original 4000 byte datagram
  → Frag 1: bytes 0–1480
  → Frag 2: bytes 1481–2960
  → Frag 3: bytes 2961–4000
```

IPv6 forbids router fragmentation (RFC 8200); only the source may fragment, and PMTUD is expected.

Why it hurts performance:

- Loss of any fragment wastes the whole packet
- Middleboxes may mishandle fragments (security filters, NAT)
- Reassembly buffers are finite — fragment floods are an attack vector (RFC 1858)

Modern practice: avoid fragmentation on the path. TCP negotiates MSS; UDP apps cap datagram size; tunnels lower MTU.

```bash
tcpdump -ni any 'ip[6:2] & 0x3fff != 0'    # fragmented IPv4
```

## Real-World Applications
Diagnosing legacy apps that send large UDP datagrams, VPN paths with mismatched MTU, and security filters that drop non-initial fragments. Example: DNS responses over UDP that exceed path MTU get fragmented; one lost fragment looks like intermittent DNS failure.

## Pros/Cons or Trade-offs
- **Pro:** Lets oversized IPv4 datagrams cross smaller links without the sender knowing the path MTU in advance.
- **Con:** Fragile under loss, hostile to middleboxes, and a historical attack vector — prefer PMTUD and sizing instead.

## Comparison
vs [[MTU (Maximum Transmission Unit)]]: MTU is the size limit per link; fragmentation is the (discouraged) mechanism for exceeding it. Path MTU Discovery plus MSS clamping is the preferred alternative.

## Mistakes to Avoid
- Assuming IPv6 routers will fragment like IPv4 — they will not.
- Ignoring that one lost fragment equals total packet loss.
- Designing UDP payloads larger than ~1200–1400 bytes on the public internet without application-level chunking.
- Forgetting that some firewalls drop fragments and break paths that "should" work.
