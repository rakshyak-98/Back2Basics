[[DNS]] [[DNS server]] [[public resolver]] [[BIND]] [[PoserDNS]]

# Unbound

> Unbound — validating recursive DNS resolver: walks the hierarchy, caches answers, checks DNSSEC — not an authoritative zone host.

---

## Mental model

**Say it in one breath:** Clients ask Unbound; Unbound queries root → TLD → auth NS (or your forwarders), validates DNSSEC when present, and caches — you stop depending on ISP DNS.

```txt
Stub → Unbound (recurse + DNSSEC + cache)
            ├─→ root / TLD / auth   (full recurse)
            └─→ optional forward-zone → upstream
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Recursive resolver** | Finds answers for clients | “Unbound is recursive-only by design.” |
| **DNSSEC validation** | Cryptographic authenticity | “SERVFAIL on bogus signatures — good.” |
| **qname minimization** | Ask parents less of the name | “Privacy: don’t leak full QNAME early.” |
| **DoT / DoH** | Encrypted DNS to upstream or clients | “TLS on 853 / HTTPS for DNS.” |
| **NSD** | NLnet Labs *authoritative* sibling | “Pair NSD + Unbound for split roles.” |

Common home lab: Pi-hole → Unbound (filter then recurse).

---

## Standard config / commands

```txt
# /etc/unbound/unbound.conf.d/local.conf (sketch)
server:
  interface: 127.0.0.1
  access-control: 127.0.0.0/8 allow
  access-control: 10.0.0.0/8 allow
  hide-identity: yes
  hide-version: yes
  qname-minimisation: yes
  auto-trust-anchor-file: "/var/lib/unbound/root.key"

forward-zone:
  name: "."
  forward-tls-upstream: yes
  forward-addr: 1.1.1.1@853#cloudflare-dns.com
# Or omit forward-zone for full recursion from root
```

```bash
unbound-checkconf
systemctl reload unbound
dig @127.0.0.1 example.com
unbound-control status
unbound-control dump_cache | head
```

| Knob | Why it matters |
|------|----------------|
| `access-control` | Without it, easy to become an open resolver |
| Full recurse vs forward | Forward is simpler behind firewalls; full recurse needs outbound 53 |
| `val-permissive-mode` | Disabling hard fail weakens DNSSEC — know why you flip it |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| SERVFAIL only on signed domains | DNSSEC clock / anchor | NTP sync; update root key; check `unbound-host -v` |
| Timeout | Outbound 53/853 blocked | Allow egress; or configure forwarders |
| Works on 8.8.8.8 not Unbound | Local ACL / listen | Fix `interface` + `access-control` |
| Stale records | Cache | `unbound-control flush_zone example.com` |
| High CPU | Attack / spam queries | Rate limits; dig into top talkers |
| Pi-hole “DNS not available” | Unbound not listening | Start Unbound before Pi-hole upstream test |

---

## Gotchas

> [!WARNING]
> **Unbound does not host your `example.com` zone** — publish zones on auth ([[BIND]] / PowerDNS / NSD).

> [!WARNING]
> **DNSSEC SERVFAIL looks like “internet broken”** — middleboxes that break signatures need fixing, not `val-permissive` forever.

> [!WARNING]
> **Open `interface: 0.0.0.0` + allow any** — you will be used for amplification.

---

## When NOT to use

- **Authoritative hosting** — use NSD/BIND/PowerDNS.
- **Kubernetes Service discovery** — [[CoreDNS]].
- **Tiny appliance that only needs DHCP + a few static names** — [[dnsmasq]] may be enough.

---

## Related

[[DNS]] [[DNS server]] [[public resolver]] [[BIND]] [[PoserDNS]] [[CoreDNS]] [[dnsmasq]] [[name server]] [[unbound variable]]
