[[TCP]] [[MTU (Maximum Transmission Unit)]] [[Packet Fragment]] [[loopback]] [[auto-pong]] [[UDP]]

# ICMP

> Internet Control Message Protocol carries network diagnostics and error signals — when ping works but TCP fails, ICMP told you reachability, not service health.

## Interview Relevance

Interviewers ask about ICMP to separate Layer-3 reachability from application health, and to see if you understand Path MTU Discovery, traceroute, and why blocking all ICMP breaks more than just `ping`.

## Sources

- [RFC 792 — Internet Control Message Protocol](https://www.rfc-editor.org/rfc/rfc792) — deep-dive
- [RFC 4443 — ICMPv6](https://www.rfc-editor.org/rfc/rfc4443) — deep-dive
- [Wikipedia — Internet Control Message Protocol](https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol) — overview

## Key Concepts

- **Control plane for IP:** ICMP rides inside IP as its own protocol number → reports problems and measures paths; it is not a transport for application data.
- **Echo / unreachable / time exceeded:** common types power `ping`, "destination unreachable," and traceroute → different codes mean different failure modes.
- **Path MTU Discovery:** ICMP "Fragmentation Needed" (type 3, code 4) tells senders the largest safe size → blocking it causes MTU black holes.
- **Reachability ≠ service health:** echo reply proves L3 path only → TCP/443 or app checks still required.

## Technical Details

ICMP (RFC 792 for IPv4; ICMPv6 in RFC 4443) is used by routers and hosts to report problems and measure paths.

Common message types (IPv4):

| Type | Name | Typical use |
|------|------|-------------|
| 0 / 8 | Echo Reply / Echo Request | `ping` reachability |
| 3 | Destination Unreachable | Port closed, no route, admin prohibited |
| 11 | Time Exceeded | Traceroute TTL expiry |
| 12 | Parameter Problem | Bad IP header |
| 5 | Redirect | Host/route hint (often ignored today) |

**Path MTU Discovery** uses ICMP "Fragmentation Needed" (type 3, code 4) so senders learn the largest safe packet size without fragmentation.

```bash
ping -c 4 8.8.8.8
ping -M do -s 1472 8.8.8.8      # don't fragment — find MTU
traceroute example.com
```

Firewalls often block ICMP echo toward servers while allowing TCP/443 — [[auto-pong]] at the ICMP layer proves L3 reachability only.

When a router cannot forward a packet, it may send ICMP unreachable back to the source. Some stacks surface this to connected sockets ("connection refused" vs "network unreachable"). [[UDP]] applications may get asynchronous ICMP errors on later sends.

ICMP can be abused for reconnaissance and amplification attacks. Rate-limiting and selective blocking are common at the edge; document what your monitoring still needs.

## Real-World Applications

Diagnosing "host unreachable" vs "port closed," running traceroute during outages, and tuning Path MTU Discovery through tunnels. Example: HTTPS hangs on large responses after a VPN change — `ping -M do` plus checking whether ICMP "packet too big" is filtered reveals an MTU black hole.

## Pros/Cons or Trade-offs

- **Pro:** Essential for diagnostics, PMTUD, and surfacing forwarding failures to endpoints.
- **Con:** Often filtered at the edge for security; over-blocking breaks PMTUD and troubleshooting without stopping application traffic.

## Comparison

vs [[TCP]]/[[UDP]]: those carry application data; ICMP carries control and error messages about IP delivery itself. Ping success never proves that your HTTP port is open.

## Mistakes to Avoid

- Equating "ping works" with "the service is up."
- Blocking all ICMP to "harden" the network and then wondering why large TCP transfers stall (PMTUD black hole).
- Ignoring type/code distinctions — Destination Unreachable has many codes with different meanings.
- Treating Redirect messages as trustworthy on modern networks without checking policy.
