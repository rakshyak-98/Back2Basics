Unbound is an open-source recursive DNS resolver developed by NLnet Labs. It performs _recursive resolution_, _DNSSEC validation_, and _DNS caching_, allowing it to resolve domain names directly from the DNS hierarchy rather than relying on an upstream public resolver. It is widely used by network administrators, privacy-conscious users, ISPs, and infrastructure providers because of its focus on security, performance, and standards compliance. ([NLnet Labs](https://www.nlnetlabs.nl/projects/unbound/about/?utm_source=chatgpt.com "Unbound - About"))

### Core Capabilities

Unbound's primary role is to act as a **validating recursive resolver**. When a client requests a domain name, Unbound can query the DNS root servers, top-level domain servers, and authoritative servers directly to obtain an answer. It then caches results to accelerate future lookups and validates DNSSEC signatures to help protect against DNS spoofing and cache-poisoning attacks. ([NLnet Labs](https://www.nlnetlabs.nl/projects/unbound/about/?utm_source=chatgpt.com "Unbound - About"))

### Security and Privacy Features

A major reason organizations choose Unbound is its strong support for modern DNS security standards. It supports **DNSSEC**, **DNS-over-TLS (DoT)**, and **DNS-over-HTTPS (DoH)**, enabling encrypted DNS traffic and authenticated responses. It also implements privacy-focused techniques such as query name minimization, which reduces the amount of information revealed during the resolution process. ([NLnet Labs](https://www.nlnetlabs.nl/projects/unbound/about/?utm_source=chatgpt.com "Unbound - About"))

### Deployment and Performance

Unbound is designed to be lightweight and efficient. It runs on Linux, BSD systems, macOS, and Windows, and is included in the base system of several BSD operating systems. Because it is focused specifically on recursive resolution rather than authoritative DNS hosting, many administrators consider it simpler and leaner than full DNS suites such as BIND for resolver workloads. ([NLnet Labs](https://www.nlnetlabs.nl/projects/unbound/about/?utm_source=chatgpt.com "Unbound - About"))

### Common Uses

Many self-hosted and home-network setups combine Unbound with DNS filtering tools. For example, it is frequently deployed alongside Pi-hole to provide both ad-blocking and fully recursive DNS resolution without depending on third-party DNS providers. It is also commonly used by enterprises, ISPs, and large-scale infrastructure operators as a high-performance recursive DNS layer. ([Pi-hole Documentation](https://docs.pi-hole.net/guides/dns/unbound/?utm_source=chatgpt.com "unbound - Pi-hole documentation"))

### Related Software

These projects often appear in the same DNS infrastructure discussions as Unbound. BIND and PowerDNS provide broader DNS server functionality, while NSD—also developed by NLnet Labs—focuses on authoritative DNS service, complementing Unbound's recursive resolver role. ([Wikipedia](https://de.wikipedia.org/wiki/Unbound?utm_source=chatgpt.com "Unbound"))