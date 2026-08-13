[[DNS server]] · [[Unbound]] · [[mDNS]] · [[TFTP]]

# dnsmasq

> dnsmasq provides DNS caching, conditional forwarding, and DHCP on small networks — one lightweight process for home routers, libvirt bridges, and Docker's embedded DNS forwarder patterns.

---

## Features

- **DNS forwarder** — caches upstream answers from ISP or [[public resolver]]
- **Local names** — `/etc/hosts` and `address=/domain/ip` overrides
- **DHCP** — hands out IPs and publishes local names
- **TFTP** — optional ([[TFTP]] PXE boot scenarios)
- **DNSSEC** — validation when configured with trust anchors

## Example `/etc/dnsmasq.conf`

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

## Docker / libvirt

Docker Desktop and Linux bridge networks often run dnsmasq to resolve container names and forward external queries.

## Debugging

```bash
sudo systemctl status dnsmasq
dig @127.0.0.1 router.home.arpa
sudo tail -f /var/log/syslog | grep dnsmasq
```

Port **53 conflicts** with systemd-resolved or [[Unbound]] — only one listener per interface.

## Security

- Do not expose unauthenticated DNS/DHCP to untrusted networks without ACLs (`interface=`, `listen-address=`)
- `stop-dns-rebind` option mitigates some [[DNS rebinding]] patterns for clients using this resolver

## vs [[Unbound]]

| dnsmasq | Unbound |
|---------|---------|
| DHCP + small LAN DNS | Full validating resolver |
| Tiny footprint | More DNSSEC rigor |

## Recall

- Why does dnsmasq read `/etc/hosts` automatically?
- What happens if both systemd-resolved and dnsmasq bind port 53?

## Sources

- [dnsmasq man page](http://www.thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html)
- [Arch Wiki — dnsmasq](https://wiki.archlinux.org/title/Dnsmasq)
