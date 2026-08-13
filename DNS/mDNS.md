[[DNS]] · [[localhost]] · [[UDP]]

# mDNS

> Multicast DNS resolves `*.local` hostnames on a link without a central server — printers, Chromecast, and development services use it, but untrusted networks should treat `.local` names as spoofable.

---

## Mechanism

mDNS ([RFC 6762](https://datatracker.ietf.org/doc/html/rfc6762)) sends DNS queries to **224.0.0.251:5353** (IPv4) and **ff02::fb:5353** (IPv6). Any host on the LAN may respond if it owns the name.

```
Client: "Who is myprinter.local?"
LAN multicast → printer replies A/AAAA + TXT
```

Works alongside DNS-SD ([RFC 6763](https://datatracker.ietf.org/doc/html/rfc6763)) for service discovery (`_http._tcp.local`).

## Common uses

- Apple **Bonjour** / Avahi on Linux
- IoT and media devices advertising themselves
- Local development (`myapp.local` via `/etc/nsswitch.conf` `mdns4_minimal`)

## nsswitch integration (Linux)

```
# /etc/nsswitch.conf
hosts: files mdns4_minimal [NOTFOUND=return] dns
```

`mdns4_minimal` resolves only single-label `.local` names via mDNS before falling back to DNS.

## Security considerations

On **untrusted Wi-Fi**, attackers can answer mDNS queries and impersonate services. Do not rely on mDNS for authentication. Prefer TLS with certificate validation for actual connections.

mDNS is unrelated to [[DNS rebinding]] but both exploit naming trust boundaries.

## Debugging

```bash
avahi-browse -a
dns-sd -B _http._tcp
ping mydevice.local
```

## vs [[LLMNR]]

| | mDNS | LLMNR |
|---|------|-------|
| **Multicast** | 224.0.0.251 | 224.0.0.252 |
| **Scope** | `.local` names | Single-label names on link |
| **Platforms** | macOS, Linux (Avahi) | Windows primarily |

## Recall

- Why does mDNS not require a configured [[name server]]?
- What breaks if two devices claim the same `.local` name?

## Sources

- [RFC 6762 — Multicast DNS](https://datatracker.ietf.org/doc/html/rfc6762)
- [RFC 6763 — DNS-Based Service Discovery](https://datatracker.ietf.org/doc/html/rfc6763)
