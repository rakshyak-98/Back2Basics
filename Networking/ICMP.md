[[TCP]] [[MTU (Maximum Transmission Unit)]] [[Packet Fragment]] [[loopback]] [[auto-pong]] [[UDP]]

# ICMP

> Internet Control Message Protocol carries network diagnostics and error signals — when ping works but TCP fails, ICMP told you reachability, not service health.

```txt
        ICMP ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask about ICMP to separate Layer-3 reachability from application…

## Sources
- [RFC 792 — Internet Control Message Protocol](https://www.rfc-editor.org/rfc/rfc792) — deep-dive
- [RFC 4443 — ICMPv6](https://www.rfc-editor.org/rfc/rfc4443) — deep-dive
- [Wikipedia — Internet Control Message Protocol](https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol) — overview

## Key Concepts
- **Control plane for IP:** ICMP rides inside IP as its own protocol number → reports problems and measur…
- **Echo / unreachable / time exceeded:** common types power `ping`, "destination unreachable," and traceroute → differ…
- **Path MTU Discovery:** ICMP "Fragmentation Needed" (type 3, code 4) tells senders the largest safe s…
- **Reachability ≠ service health:** echo reply proves L3 path only → TCP/443 or app checks still required.

## Technical Details
- ICMP (RFC 792 for IPv4

- Common message types (IPv4):

| Type | Name | Typical use |
|------|------|-------------|
| 0 / 8 | Echo Reply / Echo Request | `ping` reachability |
| 3 | Destination Unreachable | Port closed, no route, admin prohibited |
| 11 | Time Exceeded | Traceroute TTL expiry |
| 12 | Parameter Problem | Bad IP header |
| 5 | Redirect | Host/route hint (often ignored today) |

- **Path MTU Discovery:** uses ICMP "Fragmentation Needed" (type 3, code 4) so s…

```bash
ping -c 4 8.8.8.8
ping -M do -s 1472 8.8.8.8      # don't fragment — find MTU
traceroute example.com
```

- Firewalls often block ICMP echo toward servers while allowing TCP/443

- When a router cannot forward a packet, it may send ICMP unreachable back to t…
- Some stacks surface this to connected sockets ("connection refused" vs "netwo…
- [[UDP]] applications may get asynchronous ICMP errors on later sends.

- ICMP can be abused for reconnaissance and amplification attacks.
- Rate-limiting and selective blocking are common at the edge

## Mistakes to Avoid
- **Mistake:** Equating "ping works" with "the service is up."
- **Mistake:** Blocking all ICMP to "harden" the network and then wondering why…
- **Mistake:** Ignoring type/code distinctions
- **Mistake:** Treating Redirect messages as trustworthy on modern networks wit…

## Pros/Cons or Trade-offs
- **Pro:** Essential for diagnostics, PMTUD, and surfacing forwarding failures to endpoints.
- **Con:** Often filtered at the edge for security; over-blocking breaks PMTUD and troubleshooting without stopping application traffic.

## Comparison
- vs [[TCP]]/[[UDP]]: those carry application data


### Use cases
- Diagnosing "host unreachable" vs "port closed," running traceroute during out…
