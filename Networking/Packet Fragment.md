[[MTU (Maximum Transmission Unit)]] [[ICMP]] [[TCP]] [[UDP]]

# Packet Fragment

> IP fragmentation splits oversized datagrams — lose one fragment and the entire original packet is discarded.

## How fragmentation works (IPv4)

When a datagram exceeds the outgoing link [[MTU (Maximum Transmission Unit)]] and the Don't Fragment (DF) bit is clear, routers slice it into fragments sharing the same identification field. The receiver reassembles before delivering to [[TCP]] or [[UDP]].

```
Original 4000 byte datagram
  → Frag 1: bytes 0–1480
  → Frag 2: bytes 1481–2960
  → Frag 3: bytes 2961–4000
```

IPv6 forbids router fragmentation (RFC 8200); only the source may fragment, and PMTUD is expected.

## Why it hurts performance

- Loss of any fragment wastes the whole packet
- Middleboxes may mishandle fragments (security filters, NAT)
- Reassembly buffers are finite — fragment floods are an attack vector (RFC 1858)

Modern practice: avoid fragmentation on the path. TCP negotiates MSS; UDP apps cap datagram size; tunnels lower MTU.

## Detection

```bash
tcpdump -ni any 'ip[6:2] & 0x3fff != 0'    # fragmented IPv4
```

## Sources

- [RFC 791 — IPv4 (fragmentation)](https://www.rfc-editor.org/rfc/rfc791)
- [RFC 8200 — IPv6](https://www.rfc-editor.org/rfc/rfc8200)
- [Wikipedia — IP fragmentation](https://en.wikipedia.org/wiki/IP_fragmentation)
