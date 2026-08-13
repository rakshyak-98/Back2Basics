[[DNS]] · [[public resolver]] · [[name server]] · [[dnsmasq]]

# Unbound

> Unbound is a validating recursive DNS resolver designed for security and performance — run it on servers or laptops to cache queries locally, enforce DNSSEC, and forward or recurse without trusting ISP DNS.

---

## Typical deployment roles

| Role | Configuration |
|------|---------------|
| **Local recursive resolver** | Full iteration from root hints |
| **Forwarding resolver** | Forwards to [[public resolver]] or ISP |
| **DNSSEC validator** | `module-config: "validator iterator"` |
| **Corporate internal** | Split DNS with local zones + forward public |

Not to be confused with bash `set -u` (**nounset**) discussed in [[unbound variable]].

## Minimal `unbound.conf`

```yaml
server:
  interface: 127.0.0.1
  access-control: 127.0.0.0/8 allow
  do-ip6: yes
  hide-identity: yes
  hide-version: yes
  harden-glue: yes
  use-caps-for-id: yes
  prefetch: yes
  num-threads: 2

forward-zone:
  name: "."
  forward-addr: 1.1.1.1@53
  forward-addr: 8.8.8.8@53
```

Restrict `access-control` — never open recursion to `0.0.0.0/0` without rate limits.

## systemd

```bash
sudo systemctl enable --now unbound
resolvectl status   # ensure not fighting systemd-resolved on :53
```

## DNSSEC validation

When validation fails, Unbound returns `SERVFAIL`. Debug:

```bash
dig @127.0.0.1 example.com A +dnssec
unbound-control status
```

Broken parental DS records or clock skew cause false negatives.

## vs [[BIND]]

| Unbound | BIND |
|---------|------|
| Recursive focus | Authoritative + recursive |
| Lightweight | Full zone master features |
| Default on many Linux stubs | Enterprise authoritative standard |

Pair **BIND authoritative** internally with **Unbound** on clients or DMZ resolvers.

## Recall

- Why bind Unbound to localhost on a laptop?
- What symptom indicates DNSSEC validation failure?

## Sources

- [Unbound documentation](https://unbound.docs.nlnetlabs.nl/)
- [NLnet Labs — Unbound](https://nlnetlabs.nl/projects/unbound/about/)
