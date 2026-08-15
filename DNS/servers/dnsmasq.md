[[DNS server]] [[Unbound]] [[mDNS]] [[TFTP]] [[public resolver]] [[DNS rebinding]]

# dnsmasq

> dnsmasq provides DNS caching, conditional forwarding, and DHCP on small networks — one lightweight process for home routers, libvirt bridges, and Docker's embedded DNS forwarder patterns.

## Interview Relevance

Interviewers use dnsmasq for edge/LAN DNS+DHCP combined roles, port-53 conflicts with systemd-resolved, and `local=` authoritative suffixes.

## Sources

- [dnsmasq man page](http://www.thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html) — deep-dive
- [Arch Wiki — dnsmasq](https://wiki.archlinux.org/title/Dnsmasq) — overview

## Key Concepts

- **Forwarder + cache:** upstream ISP or [[public resolver]] answers cached locally.
- **Local authority:** `local=/home.arpa/` serves a suffix without forwarding.
- **DHCP integration:** leased hosts publish as local names.
- **Tiny footprint:** ideal for routers and lab bridges — not a full validating Internet recursive stack.

## Technical Details

- **DNS forwarder** — caches upstream answers from ISP or [[public resolver]]
- **Local names** — `/etc/hosts` and `address=/domain/ip` overrides
- **DHCP** — hands out IPs and publishes local names
- **TFTP** — optional ([[TFTP]] PXE boot scenarios)
- **DNSSEC** — validation when configured with trust anchors

```ini
port=53
domain=home.arpa
local=/home.arpa/
server=1.1.1.1
server=8.8.8.8
cache-size=1000
dhcp-range=192.168.1.100,192.168.1.200,12h
```

`local=/home.arpa/` makes dnsmasq authoritative for that domain without forwarding.

Docker Desktop and Linux bridge networks often run dnsmasq to resolve container names and forward external queries.

```bash
sudo systemctl status dnsmasq
dig @127.0.0.1 router.home.arpa
sudo tail -f /var/log/syslog | grep dnsmasq
```

Port **53 conflicts** with systemd-resolved or [[Unbound]] — only one listener per interface.

**Security:** do not expose unauthenticated DNS/DHCP to untrusted networks without ACLs (`interface=`, `listen-address=`); `stop-dns-rebind` mitigates some [[DNS rebinding]] patterns for clients using this resolver.

| dnsmasq | Unbound |
|---------|---------|
| DHCP + small LAN DNS | Full validating resolver |
| Tiny footprint | More DNSSEC rigor |

## Real-World Applications

Home gateways, libvirt default networks, Pi-hole-adjacent setups, and container bridge name resolution.

**Example:** DHCP hands `printer` a lease; dnsmasq answers `printer.home.arpa` from the lease table while forwarding `google.com` to 1.1.1.1.

## Pros/Cons or Trade-offs

- **Pro:** One process covers DHCP + local DNS + cache — low ops for small LANs.
- **Con:** Weaker default posture than a dedicated validating [[Unbound]].
- **Con:** Easy to conflict with systemd-resolved on the same host.

## Comparison

- vs [[Unbound]]: pick Unbound for validating recursion; dnsmasq when you also need DHCP/LAN glue.
- vs [[mDNS]]: dnsmasq is unicast server-based LAN DNS; mDNS is multicast `.local` without a server.

## Mistakes to Avoid

- Binding DNS/DHCP on untrusted interfaces without `interface=` / `listen-address=` ACLs.
- Running alongside systemd-resolved both claiming `:53`.
- Treating dnsmasq as a full Internet authoritative + DNSSEC zone master.
