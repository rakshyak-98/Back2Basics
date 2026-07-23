[[DNS]] [[name server]] [[DNS zone]]

# mDNS

> One-line: link-local multicast DNS for `.local` names without a central server — **RFC 6762** (Bonjour / Avahi).

## Mental model

mDNS (multicast DNS) resolves hostnames on a **local link** via UDP **5353** to `224.0.0.251` (IPv4) / `ff02::fb` (IPv6). Queries and responses are multicast — any host on the segment can answer for names it owns.

```
  Laptop                    LAN (same broadcast domain)
    │  "Where is printer.local?"  ──multicast──►  all hosts
    │◄──────────────────────────────  "printer.local = 192.168.1.50"  (printer)
```

Common stacks: **Avahi** (Linux), **Bonjour** (macOS/iOS), **systemd-resolved** (stub + mDNS optional). Service discovery pairs with **DNS-SD** (`_http._tcp.local`).

Distinct from unicast [[DNS]]: no hierarchy, no caching resolver chain — purely local segment.

## Standard config / commands

```shell
# Avahi (most Linux desktops / IoT)
systemctl status avahi-daemon
avahi-browse -a -r                    # browse all services on LAN
avahi-resolve -n myhost.local

# systemd-resolved mDNS mode
resolvectl status                     # look for "MulticastDNS setting"
# /etc/systemd/resolved.conf → MulticastDNS=yes|no|resolve

# Query manually
dig @224.0.0.251 -p 5353 printer.local
dns-sd -B _http._tcp                  # macOS browse

# Firewall — mDNS must pass on trusted LAN
sudo iptables -I INPUT -p udp --dport 5353 -j ACCEPT   # tighten to link-local in prod VLANs
```

Disable mDNS on servers that shouldn't advertise (security hardening):

```shell
# Avahi
sudo systemctl disable --now avahi-daemon

# resolved
# MulticastDNS=no in /etc/systemd/resolved.conf
sudo systemctl restart systemd-resolved
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `*.local` doesn't resolve | `avahi-daemon` running? VLAN isolation? | Enable mDNS on interface; ensure same L2 segment (no mDNS across routed VLANs without reflector) |
| Works on Wi-Fi, not Ethernet | Different VLANs / AP client isolation | Move to same broadcast domain or deploy mDNS gateway/reflector (e.g. Avahi reflector, UniFi mDNS) |
| Duplicate name conflicts | `avahi-browse -a` shows multiple same names | Rename host; Avahi appends `-2` suffix on conflict |
| Chromecast / printer not found | Multicast blocked on AP/guest network | Disable guest isolation; allow UDP/5353 between IoT VLAN and client VLAN via reflector |
| K8s pod needs `.local` | Pods aren't on LAN | Use cluster DNS ([[CoreDNS]]), not mDNS |
| High multicast noise | Many devices advertising | Reduce advertised services; disable on headless servers |

## Gotchas

> [!WARNING]
> **mDNS crosses trust boundaries poorly.** A compromised LAN device can spoof `printer.local` or `_ssh._tcp.local`. Never treat mDNS answers as authenticated.

- **Not routable by default** — routers don't forward 224.0.0.251; cross-subnet needs explicit reflector/proxy.
- **`.local` vs `.localdomain`** — macOS/iOS use `.local` for mDNS; don't register `.local` in public [[DNS zone]].
- **Docker bridge** isolates multicast — container won't see host mDNS without `network_mode: host` or macvlan.
- **Wi-Fi multicast-to-unicast** conversion on some APs breaks discovery unless vendor fix enabled.

## When NOT to use

- Production service discovery across datacenters → use Consul, etcd, or K8s DNS.
- Anything requiring authoritative global naming → use unicast DNS.
- Security-sensitive authentication endpoints → never rely on mDNS for identity.

## Related

[[DNS]] · [[DNS zone]] · [[name server]] · [[DNS server]]
