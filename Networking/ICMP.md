[[TCP]] [[MTU (Maximum Transmission Unit)]] [[Packet Fragment]] [[loopback]] [[auto-pong]]

# ICMP

> Internet Control Message Protocol carries network diagnostics and error signals — when ping works but TCP fails, ICMP told you reachability, not service health.

## Role in the stack

ICMP (RFC 792 for IPv4; ICMPv6 in RFC 4443) rides inside IP as a separate protocol number. Routers and hosts use it to report problems and measure paths. It is **not** a transport for application data.

Common message types (IPv4):

| Type | Name | Typical use |
|------|------|-------------|
| 0 / 8 | Echo Reply / Echo Request | `ping` reachability |
| 3 | Destination Unreachable | Port closed, no route, admin prohibited |
| 11 | Time Exceeded | Traceroute TTL expiry |
| 12 | Parameter Problem | Bad IP header |
| 5 | Redirect | Host/route hint (often ignored today) |

**Path MTU Discovery** uses ICMP "Fragmentation Needed" (type 3, code 4) so senders learn the largest safe packet size without fragmentation.

## Ping and traceroute

```bash
ping -c 4 8.8.8.8
ping -M do -s 1472 8.8.8.8      # don't fragment — find MTU
traceroute example.com
```

Firewalls often block ICMP echo toward servers while allowing TCP/443 — [[auto-pong]] at the ICMP layer proves L3 reachability only.

## Error messages to applications

When a router cannot forward a packet, it may send ICMP unreachable back to the source. Some stacks surface this to connected sockets ("connection refused" vs "network unreachable"). UDP applications may get asynchronous ICMP errors on later sends.

## Security note

ICMP can be abused for reconnaissance and amplification attacks. Rate-limiting and selective blocking are common at the edge; document what your monitoring still needs.

## Sources

- [RFC 792 — Internet Control Message Protocol](https://www.rfc-editor.org/rfc/rfc792)
- [RFC 4443 — ICMPv6](https://www.rfc-editor.org/rfc/rfc4443)
- [Wikipedia — Internet Control Message Protocol](https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol)
