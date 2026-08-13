[[Packet Fragment]] [[ICMP]] [[TCP]] [[UDP]]

# MTU (Maximum Transmission Unit)

> MTU is the largest IP payload one link accepts without fragmentation — black-hole MTU issues show up as HTTPS that hangs on large responses but works for small pages.

## Layering

| Layer | Typical MTU |
|-------|-------------|
| Ethernet | 1500 bytes (often) |
| PPPoE | 1492 |
| GRE/VPN overlay | 1400 or lower — encap overhead |
| IPv6 minimum | 1280 (RFC 8200) |

IP header + transport header reduce usable application payload. TCP MSS is negotiated in SYN options as roughly MTU − 40 (IPv4) or − 60 (IPv6).

## Fragmentation

Routers may fragment IPv4 if DF bit clear; IPv6 routers do **not** fragment — sender must use path MTU discovery. Lost [[Packet Fragment]] drops the entire datagram.

Path MTU Discovery (RFC 1191 / RFC 8201): sender sets DF, receives ICMP "packet too big," lowers size.

## Symptoms and checks

```bash
ping -M do -s 1472 8.8.8.8        # 1472 + 28 = 1500
ip link show eth0 | grep mtu
tracepath example.com
```

| Symptom | Check |
|---------|-------|
| Small OK, large hang | MTU black hole — ICMP blocked |
| VPN flaky | Lower interface MTU on tunnel |
| TCP weird after tunnel | MSS clamping on firewall |

## MSS clamping

Firewalls often rewrite TCP MSS in SYN packets to avoid fragmentation through tunnels:

```bash
iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu
```

## Sources

- [RFC 8200 — IPv6 (minimum MTU 1280)](https://www.rfc-editor.org/rfc/rfc8200)
- [RFC 1191 — Path MTU Discovery](https://www.rfc-editor.org/rfc/rfc1191)
- [Wikipedia — Maximum transmission unit](https://en.wikipedia.org/wiki/Maximum_transmission_unit)
