[[DNS]] [[localhost]] [[UDP]] [[LLMNR]] [[DNS rebinding]]

# mDNS

> Multicast DNS resolves `*.local` hostnames on a link without a central server — printers, Chromecast, and development services use it, but untrusted networks should treat `.local` names as spoofable.

```txt
        mDNS ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask how Bonjour/Avahi find devices without DNS, and why `.local`…

## Sources
- [RFC 6762 — Multicast DNS](https://datatracker.ietf.org/doc/html/rfc6762) — deep-dive
- [RFC 6763 — DNS-Based Service Discovery](https://datatracker.ietf.org/doc/html/rfc6763) — deep-dive

## Key Concepts
- **Multicast query/response:** any host on the LAN may claim a name — no [[name server]] required.
- **`.local` TLD:** reserved for mDNS use (do not invent it as a corporate public TLD).
- **DNS-SD:** service discovery records (`_http._tcp.local`) ride alongside mDNS.
- **nsswitch:** Linux can try mDNS before unicast DNS for `.local`.

## Technical Details
- mDNS ([RFC 6762](https://datatracker.ietf.org/doc/html/rfc6762)) sends DNS qu…
- Any host on the LAN may respond if it owns the name.

```
Client: "Who is myprinter.local?"
LAN multicast → printer replies A/AAAA + TXT
```

- Works alongside DNS-SD ([RFC 6763](https://datatracker.ietf.org/doc/html/rfc6…

- **Common uses:** Apple **Bonjour** / Avahi on Linux

```
# /etc/nsswitch.conf
hosts: files mdns4_minimal [NOTFOUND=return] dns
```

- `mdns4_minimal` resolves only single-label `.local` names via mDNS before fal…

- On **untrusted Wi-Fi**, attackers can answer mDNS queries and impersonate ser…
- Do not rely on mDNS for authentication.
- Prefer TLS with certificate validation for actual connections.

- mDNS is unrelated to [[DNS rebinding]] but both exploit naming trust boundari…

```bash
avahi-browse -a
dns-sd -B _http._tcp
ping mydevice.local
```

| | mDNS | LLMNR |
|---|------|-------|
| **Multicast** | 224.0.0.251 | 224.0.0.252 |
| **Scope** | `.local` names | Single-label names on link |
| **Platforms** | macOS, Linux (Avahi) | Windows primarily |

## Mistakes to Avoid
- **Mistake:** Using `.local` as an internal corporate TLD in unicast DNS
- **Mistake:** Trusting mDNS names without TLS (or better mutual auth) on share…
- **Mistake:** Expecting multi-label `foo.bar.local` behavior identical to `mdn…

## Pros/Cons or Trade-offs
- **Pro:** Zero server setup for LAN discovery.
- **Con:** Spoofable on hostile links — not an auth mechanism.
- **Con:** Does not replace corporate unicast DNS for FQDNs and policy.

## Comparison
- vs [[DNS]]: unicast hierarchy with authoritative servers vs link-scoped multicast.
- vs [[LLMNR]]: `.local` + Bonjour/Avahi vs Windows single-label fallback.


### Use cases
- Printer and Chromecast discovery

- **Example:** Two devices both claim `printer.local`
